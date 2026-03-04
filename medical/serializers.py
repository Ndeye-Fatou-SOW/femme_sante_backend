from rest_framework import serializers
from .models import MedicalConsultation, Reminder


class MedicalConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalConsultation
        exclude = ('user',)
        read_only_fields = ('id', 'created_at')


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        exclude = ('user',)
        read_only_fields = ('id', 'created_at', 'is_sent')