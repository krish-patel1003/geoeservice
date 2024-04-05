from django.shortcuts import render
from core.serializers import CoordinateRequestSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .utils import pincode_utils
from pincode.serializers import PincodeResponseSerializer


# Create your views here.
class PincodeViewSet(ViewSet):
    """ViewSet for /maps/pincode API."""

    serializer_class = CoordinateRequestSerializer

    @swagger_auto_schema(
        query_serializer=CoordinateRequestSerializer,
        operation_summary="Get Pincode Data",
        operation_description="""
        Get Pincode Data.
        The location is specified by the latitude and longitude.
        Latitude and longitude are floating point numbers.
        It should be passed as query parameters.

        Example:
        /maps/weather?latitude=12.34&longitude=56.78

        Response will be a object of PincodeResponseSerializer.
        Response will contain pincode and city.

        Response:
            200: Returns PincodeData for the location.
            204: No Content, Pincode data does not exist for the given coordinates.
            400: Invalid Request Coordinates,
        """,
        responses={200: PincodeResponseSerializer, 400: "Invalid Request Coordinates"},
    )
    def list(self, request):
        """Get Pincode Data."""
        request_serializer = self.serializer_class(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        latitude = request_serializer.validated_data["latitude"]
        longitude = request_serializer.validated_data["longitude"]

        pincode_obj = pincode_utils.get_pincode_data(
            longitude=longitude, latitude=latitude
        )

        if pincode_obj is None:
            return Response(
                {
                    "pincode": None,
                    "message": "Pincode data does not exist for the given coordinates.",
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        serializer = PincodeResponseSerializer(
            data=pincode_obj.__dict__,
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
