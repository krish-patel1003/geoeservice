from django.urls import include
from django.urls import path
from pincode.views import PincodeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", PincodeViewSet, basename="weather")

urlpatterns = [
    path("", include(router.urls)),
]
