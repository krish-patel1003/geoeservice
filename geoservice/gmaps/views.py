from drf_yasg.utils import swagger_auto_schema
from gmaps.serializers import PlacesRequestSerializer
from gmaps.serializers import GooglePlacesSerializer
from gmaps.utils import gmap_utils
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


# Create your views here.
class GooglePlacesViewSet(ViewSet):
    serializer_class = GooglePlacesSerializer

    @swagger_auto_schema(
        operation_summary="Get places data for a location",
        operation_description="""Get places data for a location.
            The location is given in the query.

            Example:
                /maps/places?place_id=
                OR
                /maps/places?longitude=&latitude=

            ** Query Parameters **
            place_id (str): The place id of the place.
            longitude (float): The longitude of the location.
            latitude (float): The latitude of the location.

            Response will be a object of GooglePlacesCache model.
            Response will contain latitude, longitude, address, place_id, h3_id, created_at, and updated_at.
            The response will be cached for 30 days.
        """,
        query_serializer=PlacesRequestSerializer,
        responses={200: GooglePlacesSerializer},
    )
    def list(self, request):
        """Get places data for a location."""
        request_serializer = PlacesRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        place_id = request_serializer.validated_data.get("place_id")
        longitude = request_serializer.validated_data.get("longitude")
        latitude = request_serializer.validated_data.get("latitude")

        place_obj = gmap_utils.get_places_cache(
            place_id=place_id, longitude=longitude, latitude=latitude
        )
        
        serializer = self.serializer_class(instance=place_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)



