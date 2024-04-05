from core.serializers import CoordinateRequestSerializer
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from map_tiler.serializers import MapImageResponseSerializer
from map_tiler.utils import aerial_view_utils
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# Create your views here.


class MapImageViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get image of the location.",
        responses={
            status.HTTP_200_OK: MapImageResponseSerializer,
        },
        query_serializer=CoordinateRequestSerializer,
    )
    def list(self, request):
        """Get image of the location."""
        request_serializer = CoordinateRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        latitude = request_serializer.validated_data["latitude"]
        longitude = request_serializer.validated_data["longitude"]

        image_url = aerial_view_utils.upload_aerial_view(
            latitude=latitude, longitude=longitude
        )

        serializer = MapImageResponseSerializer(data={"image_url": image_url})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
