# from django.shortcuts import render

# # Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from cycle.models import MenstrualCycle
from .predictor import CyclePredictor, get_cycle_phase, calculate_fertility_window


class PredictCycleView(APIView):
    """GET /api/ml/predict/ — Prédit le prochain cycle"""

    def get(self, request):
        cycles = MenstrualCycle.objects.filter(
            user=request.user, is_predicted=False
        ).order_by('-start_date')[:12]

        if not cycles.exists():
            return Response({
                'message': 'Enregistre au moins un cycle pour obtenir des prédictions.',
                'has_prediction': False
            })

        predictor = CyclePredictor()
        predicted_length, confidence, predicted_date = predictor.predict_next(list(cycles))

        # Phase actuelle
        last_cycle = cycles[0]
        days_since = (date.today() - last_cycle.start_date).days
        phase = get_cycle_phase(days_since, predicted_length or 28)

        # Fenêtre de fertilité
        fertility = calculate_fertility_window(last_cycle.start_date, predicted_length or 28)

        return Response({
            'has_prediction': True,
            'next_cycle': {
                'predicted_start_date': predicted_date,
                'predicted_length_days': predicted_length,
                'confidence_score': confidence,
                'confidence_label': 'Haute' if confidence > 0.75 else 'Moyenne' if confidence > 0.5 else 'Faible',
            },
            'current_phase': phase,
            'current_day_of_cycle': days_since + 1,
            'fertility_window': {
                'ovulation_date': fertility['ovulation_date'],
                'fertile_start': fertility['fertile_start'],
                'fertile_end': fertility['fertile_end'],
            },
            'cycles_analyzed': cycles.count(),
        })


class AnomalyDetectionView(APIView):
    """GET /api/ml/anomalies/ — Détecte des anomalies dans le cycle"""

    def get(self, request):
        cycles = MenstrualCycle.objects.filter(
            user=request.user, is_predicted=False
        ).order_by('-start_date')[:12]

        lengths = [c.cycle_length for c in cycles if c.cycle_length]

        if len(lengths) < 3:
            return Response({'message': 'Pas assez de données pour la détection.', 'anomalies': []})

        import numpy as np
        mean = np.mean(lengths)
        std = np.std(lengths)
        anomalies = []

        for cycle in cycles:
            if cycle.cycle_length:
                z_score = abs(cycle.cycle_length - mean) / std if std > 0 else 0
                if z_score > 2 or cycle.cycle_length < 21 or cycle.cycle_length > 35:
                    anomalies.append({
                        'date': cycle.start_date,
                        'cycle_length': cycle.cycle_length,
                        'type': 'Cycle court' if cycle.cycle_length < 21 else 'Cycle long',
                        'recommendation': 'Consulte un professionnel de santé si cela se répète.',
                    })

        return Response({
            'anomalies': anomalies,
            'has_anomalies': len(anomalies) > 0,
            'average_cycle': round(mean, 1),
            'variability': round(std, 1),
        })