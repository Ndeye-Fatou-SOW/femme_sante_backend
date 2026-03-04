from rest_framework import serializers
from .models import DailyLog


class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        exclude = ('user',)
        read_only_fields = ('id', 'created_at')