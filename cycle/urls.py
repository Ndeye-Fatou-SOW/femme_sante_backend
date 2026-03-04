from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenstrualCycleViewSet

router = DefaultRouter()
router.register('', MenstrualCycleViewSet, basename='cycle')

urlpatterns = [path('', include(router.urls))]