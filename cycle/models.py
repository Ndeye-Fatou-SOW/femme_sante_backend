# from django.db import models

# # Create your models here.

from django.db import models
from users.models import User
import uuid


class MenstrualCycle(models.Model):
    """Un cycle menstruel"""
    FLOW_CHOICES = [
        ('light', 'Léger'), ('medium', 'Moyen'),
        ('heavy', 'Abondant'), ('very_heavy', 'Très abondant'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycles')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    flow_intensity = models.CharField(max_length=15, choices=FLOW_CHOICES, default='medium')
    cycle_length = models.IntegerField(null=True, blank=True)
    is_predicted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcule automatiquement la durée du cycle
        if not self.cycle_length:
            prev = MenstrualCycle.objects.filter(
                user=self.user,
                start_date__lt=self.start_date,
                is_predicted=False
            ).order_by('-start_date').first()
            if prev:
                self.cycle_length = (self.start_date - prev.start_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cycle {self.user.email} - {self.start_date}"

    class Meta:
        db_table = 'menstrual_cycles'
        ordering = ['-start_date']


class CycleSymptom(models.Model):
    """Symptômes liés au cycle"""
    SYMPTOM_CHOICES = [
        ('cramps', 'Crampes'), ('headache', 'Maux de tête'),
        ('bloating', 'Ballonnements'), ('back_pain', 'Douleurs dos'),
        ('nausea', 'Nausées'), ('fatigue', 'Fatigue'),
        ('acne', 'Acné'), ('mood_swings', 'Sautes d\'humeur'),
        ('breast_pain', 'Douleurs seins'), ('other', 'Autre'),
    ]

    cycle = models.ForeignKey(MenstrualCycle, on_delete=models.CASCADE, related_name='symptoms')
    symptom = models.CharField(max_length=30, choices=SYMPTOM_CHOICES)
    severity = models.IntegerField(default=1)  # 1=léger, 2=modéré, 3=sévère
    date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'cycle_symptoms'
