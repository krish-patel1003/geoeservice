from gmaps.models import GooglePlacesCache
from rest_framework import serializers
import re


class PlacesRequestSerializer(serializers.Serializer):
    """Serializer for places request data.

    Attributes:
        place_id (str): The place id of the place.
        longitude (float): The longitude of the location.
        latitude (float): The latitude of the location.
    """

    place_id = serializers.CharField(required=False)
    longitude = serializers.FloatField(required=False)
    latitude = serializers.FloatField(required=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        # Either place_id or longitude and latitude must be provided.
        if not (
            data.get("place_id") or (data.get("longitude") and data.get("latitude"))
        ):
            raise serializers.ValidationError(
                "Either place_id or longitude and latitude must be provided."
            )
        return data


class GooglePlacesSerializer(serializers.ModelSerializer):
    """Serializer for Google Places API request data.

    Attributes:
        user_longitude (float): The longitude of the user.
        user_latitude (float): The latitude of the user.
        longitude (float): The longitude of the location.
        latitude (float): The latitude of the location.
        address (str): The address of the place.
        place_id (str): The place id of the place.
        plus_code (str): The plus code of the place.`
        created_at (datetime): The time the cache was created.
        updated_at (datetime): The time the cache was last updated.
    """

    address = serializers.SerializerMethodField()

    class Meta:
        model = GooglePlacesCache
        fields = ["longitude", "latitude", "address", "source"]

    def __remove_plus_code(self, address):
        """Remove the plus code from the address."""
        words = address.split(" ")
        words = [word.strip() for word in words]
        words = [word for word in words if not re.match(r"^[A-Z0-9]{4}\+", word)]
        return " ".join(words)

    def get_address(self, obj):
        address = self.__remove_plus_code(obj.address)
        tokens = [token.strip() for token in address.split(",")]
        display_str = ""
        while len(display_str) < 30 and tokens:
            display_str += tokens.pop(0) + ", "
        return display_str.rstrip(", ")  # Remove the trailing comma and space
