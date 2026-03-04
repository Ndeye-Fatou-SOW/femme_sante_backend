from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalConsultationViewSet, ReminderViewSet

router = DefaultRouter()
router.register('consultations', MedicalConsultationViewSet, basename='consultation')
router.register('reminders', ReminderViewSet, basename='reminder')

urlpatterns = [path('', include(router.urls))]