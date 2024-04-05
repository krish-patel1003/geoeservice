from rest_framework import serializers


class CoordinateRequestSerializer(serializers.Serializer):
    """Serializer for weather request data.

    Attributes:
        longitude (float): The longitude of the location.
        latitude (float): The latitude of the location.
    """

    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
