from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from weather.serializers import (
    WeatherResponseSerializer,
)
from core.serializers import CoordinateRequestSerializer
from weather.utils import weather_utils

# Create your views here.
class WeatherViewSet(ViewSet):
    """ViewSet for /maps/weather API."""

    serializer_class = WeatherResponseSerializer

    @swagger_auto_schema(
        query_serializer=CoordinateRequestSerializer,
        operation_summary="Get weather data for a location",
        operation_description="""
            Get weather data for a location.
            The location is specified by the latitude and longitude.
            Latitude and longitude are floating point numbers.
            It should be passed as query parameters.

            Example:
            /maps/weather?latitude=12.34&longitude=56.78

            Response will be a object of WeatherCache model.
            Response will contain latitude, longitude, data, create_at, and updated_at.
            The response will be cached for 30 minutes.
            If the same request is made within 30 minutes,
            the response will be served from the DB.
            After 30 minutes, the response will be fetched from the API
            and updated in the DB on separate thread.
            And while the update is in progress,
            the response will be served from the DB.
            """,
        responses={200: WeatherResponseSerializer},
    )
    def list(self, request):
        """Get weather data for a location."""
        request_serializer = CoordinateRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        latitude = request_serializer.validated_data["latitude"]
        longitude = request_serializer.validated_data["longitude"]

        weather_object = weather_utils.get_data(longitude=longitude, latitude=latitude)

        response_serializer = self.serializer_class(instance=weather_object)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
