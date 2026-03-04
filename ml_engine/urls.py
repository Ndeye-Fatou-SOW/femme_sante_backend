from django.urls import path
from .views import PredictCycleView, AnomalyDetectionView

urlpatterns = [
    path('predict/', PredictCycleView.as_view(), name='predict'),
    path('anomalies/', AnomalyDetectionView.as_view(), name='anomalies'),
]