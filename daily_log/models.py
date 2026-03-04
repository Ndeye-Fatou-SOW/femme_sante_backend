# from django.db import models

# # Create your models here.
from django.db import models
from users.models import User
import uuid


class DailyLog(models.Model):
    """Journal quotidien de santé"""
    MOOD_CHOICES = [
        ('great', 'Super'), ('good', 'Bien'), ('neutral', 'Neutre'),
        ('bad', 'Mauvais'), ('terrible', 'Terrible'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, null=True, blank=True)
    energy_level = models.IntegerField(null=True, blank=True)   # 1 à 10
    stress_level = models.IntegerField(null=True, blank=True)   # 1 à 10
    sleep_hours = models.FloatField(null=True, blank=True)
    water_intake = models.FloatField(null=True, blank=True)     # en litres
    physical_activity = models.IntegerField(null=True, blank=True)  # minutes
    basal_temperature = models.FloatField(null=True, blank=True)    # en °C
    symptoms = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_logs'
        ordering = ['-date']
        unique_together = ('user', 'date')   # Un seul log par jour par utilisatrice

    def __str__(self):
        return f"Log {self.user.email} - {self.date}"