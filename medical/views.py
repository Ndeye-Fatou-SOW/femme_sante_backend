from rest_framework import viewsets
from .models import MedicalConsultation, Reminder
from .serializers import MedicalConsultationSerializer, ReminderSerializer


class MedicalConsultationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalConsultationSerializer

    def get_queryset(self):
        return MedicalConsultation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)