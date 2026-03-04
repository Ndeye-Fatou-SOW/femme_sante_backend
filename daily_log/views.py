# from django.shortcuts import render

# # Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date, timedelta
from .models import DailyLog
from .serializers import DailyLogSerializer


class DailyLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyLogSerializer

    def get_queryset(self):
        return DailyLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """GET /api/logs/today/ — Log d'aujourd'hui"""
        log, created = DailyLog.objects.get_or_create(
            user=request.user,
            date=date.today(),
        )
        return Response(DailyLogSerializer(log).data)

    @action(detail=False, methods=['get'])
    def last_week(self, request):
        """GET /api/logs/last_week/ — Les 7 derniers jours"""
        start = date.today() - timedelta(days=7)
        logs = DailyLog.objects.filter(user=request.user, date__gte=start)
        return Response(DailyLogSerializer(logs, many=True).data)