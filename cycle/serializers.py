from rest_framework import serializers
from .models import MenstrualCycle, CycleSymptom


class CycleSymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CycleSymptom
        fields = '__all__'
        read_only_fields = ('cycle',)


class MenstrualCycleSerializer(serializers.ModelSerializer):
    symptoms = CycleSymptomSerializer(many=True, read_only=True)
    duration_days = serializers.SerializerMethodField()
    current_phase = serializers.SerializerMethodField()

    class Meta:
        model = MenstrualCycle
        exclude = ('user',)
        read_only_fields = ('id', 'created_at', 'cycle_length')

    def get_duration_days(self, obj):
        if obj.end_date:
            return (obj.end_date - obj.start_date).days + 1
        return None

    def get_current_phase(self, obj):
        from datetime import date
        today = date.today()
        if obj.start_date <= today:
            days = (today - obj.start_date).days
            length = obj.cycle_length or 28
            if days < 5:
                return 'menstruelle'
            elif days < length // 2 - 2:
                return 'folliculaire'
            elif days < length // 2 + 2:
                return 'ovulation'
            else:
                return 'lutéale'
        return None