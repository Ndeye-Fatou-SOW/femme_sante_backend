# from django.shortcuts import render

# # Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
from .models import MenstrualCycle, CycleSymptom
from .serializers import MenstrualCycleSerializer, CycleSymptomSerializer


class MenstrualCycleViewSet(viewsets.ModelViewSet):
    """CRUD complet pour les cycles menstruels"""
    serializer_class = MenstrualCycleSerializer

    def get_queryset(self):
        # Chaque utilisatrice ne voit QUE ses propres cycles
        return MenstrualCycle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """GET /api/cycle/statistics/ — Statistiques du cycle"""
        cycles = MenstrualCycle.objects.filter(
            user=request.user, is_predicted=False
        ).order_by('-start_date')[:12]

        if not cycles.exists():
            return Response({'message': 'Pas encore assez de données.'})

        lengths = [c.cycle_length for c in cycles if c.cycle_length]
        period_lengths = [
            (c.end_date - c.start_date).days + 1
            for c in cycles if c.end_date
        ]

        return Response({
            'total_cycles_enregistres': cycles.count(),
            'duree_cycle_moyenne': round(sum(lengths) / len(lengths), 1) if lengths else 28,
            'duree_regles_moyenne': round(sum(period_lengths) / len(period_lengths), 1) if period_lengths else 5,
            'cycles': MenstrualCycleSerializer(cycles, many=True).data,
        })

    @action(detail=True, methods=['post'])
    def add_symptom(self, request, pk=None):
        """POST /api/cycle/{id}/add_symptom/ — Ajouter un symptôme"""
        cycle = self.get_object()
        serializer = CycleSymptomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cycle=cycle)
        return Response(serializer.data, status=201)