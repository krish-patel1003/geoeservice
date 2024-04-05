from rest_framework import serializers


class PincodeResponseSerializer(serializers.Serializer):
    """
    Serializer for Pincode Response.

    Attributes:
        pincode (str): The pincode.
        city (str): The city.
        state (str): The state.
        radius (float): The radius.
        longitude (float): The longitude.
        latitude (float): The latitude.
        popularity (float): The popularity.
    """

    pincode = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    radius = serializers.FloatField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    popularity = serializers.FloatField()

