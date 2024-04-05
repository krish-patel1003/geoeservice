from django.urls import include
from django.urls import path
from weather.views import WeatherViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", WeatherViewSet, basename="weather")

urlpatterns = [
    path("", include(router.urls)),
]
