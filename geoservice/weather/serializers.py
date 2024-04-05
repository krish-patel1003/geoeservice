from weather.models import WeatherCache
from rest_framework import serializers

class WeatherResponseSerializer(serializers.ModelSerializer):
    """Serializer for weather response data.

    Attributes:
        longitude (float): The longitude of the location.
        latitude (float): The latitude of the location.
        condition (str): The weather condition.
        description (str): The weather description.
        temperature (float): The temperature in Kelvin.
        feels_like (float): The temperature it feels like in Kelvin.
        city (str): The city name.
        icon (str): The URL of the weather icon.
        created_at (datetime): The time the cache was created.
        updated_at (datetime): The time the cache was last updated.
    """

    class Meta:
        model = WeatherCache
        fields = "__all__"

