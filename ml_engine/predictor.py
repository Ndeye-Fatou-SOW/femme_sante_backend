import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'saved_models')
os.makedirs(MODEL_PATH, exist_ok=True)


class CyclePredictor:
    """Prédit la date du prochain cycle menstruel"""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.is_trained = False

    def prepare_features(self, cycles):
        """Transforme les cycles en features pour le ML"""
        features = []
        lengths = [c.cycle_length for c in cycles if c.cycle_length]

        if len(lengths) < 2:
            return None

        for i in range(1, len(lengths)):
            feature = [
                lengths[i - 1],                              # Durée du cycle précédent
                np.mean(lengths[:i]),                        # Moyenne des cycles
                np.std(lengths[:i]) if i > 1 else 0,        # Écart-type (irrégularité)
                i,                                           # Numéro du cycle
            ]
            features.append(feature)
        return features

    def train(self, cycles):
        """Entraîne le modèle sur l'historique de l'utilisatrice"""
        lengths = [c.cycle_length for c in cycles if c.cycle_length]

        if len(lengths) < 3:
            return False

        # Préparer X et y
        X, y = [], []
        for i in range(1, len(lengths)):
            X.append([
                lengths[i - 1],
                np.mean(lengths[:i]),
                np.std(lengths[:i]) if i > 1 else 0,
                i,
            ])
            y.append(lengths[i])

        X, y = np.array(X), np.array(y)
        self.model.fit(X, y)
        self.is_trained = True
        return True

    def predict_next(self, cycles):
        """
        Prédit la durée du prochain cycle.
        Retourne (durée_prédite, score_confiance, date_prédite)
        """
        from datetime import timedelta

        lengths = [c.cycle_length for c in cycles if c.cycle_length]

        if len(lengths) < 2:
            # Pas assez de données : on utilise la moyenne standard
            avg = np.mean(lengths) if lengths else 28
            last_cycle = cycles[0] if cycles else None
            if not last_cycle:
                return None, 0.3, None

            predicted_date = last_cycle.start_date + timedelta(days=int(avg))
            return int(avg), 0.4, predicted_date

        # Entraîner si pas encore fait
        if not self.is_trained:
            self.train(cycles)

        # Prédire
        last_length = lengths[0]
        avg = np.mean(lengths)
        std = np.std(lengths)
        n = len(lengths)

        feature = np.array([[last_length, avg, std, n]])

        if self.is_trained:
            predicted_length = self.model.predict(feature)[0]
        else:
            predicted_length = avg

        # Score de confiance basé sur la régularité
        confidence = max(0.4, min(0.95, 1 - (std / avg)))

        # Calculer la date prédite
        last_cycle = cycles[0]
        predicted_date = last_cycle.start_date + timedelta(days=int(round(predicted_length)))

        return int(round(predicted_length)), round(confidence, 2), predicted_date


def get_cycle_phase(days_since_start, cycle_length=28):
    """Retourne la phase du cycle selon le nombre de jours"""
    if days_since_start < 0:
        return None
    if days_since_start <= 5:
        return {'phase': 'menstruelle', 'description': 'Période de règles', 'color': '#EF9A9A'}
    elif days_since_start <= cycle_length // 2 - 3:
        return {'phase': 'folliculaire', 'description': 'Le corps se prépare à l\'ovulation', 'color': '#A5D6A7'}
    elif days_since_start <= cycle_length // 2 + 2:
        return {'phase': 'ovulation', 'description': 'Fenêtre de fertilité', 'color': '#FFF59D'}
    else:
        return {'phase': 'lutéale', 'description': 'Phase post-ovulatoire', 'color': '#CE93D8'}


def calculate_fertility_window(cycle_start, cycle_length=28):
    """Calcule la fenêtre de fertilité"""
    from datetime import timedelta
    ovulation = cycle_start + timedelta(days=cycle_length - 14)
    fertile_start = ovulation - timedelta(days=5)
    fertile_end = ovulation + timedelta(days=1)
    return {
        'ovulation_date': ovulation,
        'fertile_start': fertile_start,
        'fertile_end': fertile_end,
    }