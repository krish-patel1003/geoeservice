from django.urls import include
from django.urls import path
from gmaps.views import GooglePlacesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"places", GooglePlacesViewSet, basename="places")


urlpatterns = [
    path("", include(router.urls)),
]
