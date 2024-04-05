from django.urls import include
from django.urls import path
from map_tiler.views import MapImageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", MapImageViewSet, basename="map_image")

urlpatterns = [
    path("", include(router.urls)),
]
