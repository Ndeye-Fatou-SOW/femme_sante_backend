# from django.db import models

# # Create your models here.

from django.db import models
from users.models import User
import uuid


class MedicalConsultation(models.Model):
    """Consultation médicale enregistrée"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations')
    date = models.DateField()
    doctor_name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100, blank=True)
    reason = models.TextField()
    diagnosis = models.TextField(blank=True)
    prescriptions = models.TextField(blank=True)
    next_appointment = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medical_consultations'
        ordering = ['-date']

    def __str__(self):
        return f"Consultation {self.user.email} - {self.date}"


class Reminder(models.Model):
    """Rappels et notifications"""
    TYPE_CHOICES = [
        ('pill', 'Pilule'), ('appointment', 'Rendez-vous'),
        ('cycle', 'Cycle'), ('exam', 'Examen'), ('other', 'Autre'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reminders'
        ordering = ['scheduled_date']
