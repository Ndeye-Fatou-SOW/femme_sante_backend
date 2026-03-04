from django.contrib import admin
from .models import MenstrualCycle, CycleSymptom

@admin.register(MenstrualCycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'flow_intensity', 'cycle_length', 'is_predicted')
    list_filter = ('flow_intensity', 'is_predicted')
    search_fields = ('user__email',)

@admin.register(CycleSymptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('cycle', 'symptom', 'severity', 'date')