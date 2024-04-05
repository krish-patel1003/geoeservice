from django.db import models
from weather.constants import WeatherConstants

# Create your models here.
class WeatherCache(models.Model):
    """Model for storing weather data in the cache.

    Attributes:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        condition (str): The weather condition.
        description (str): The weather description.
        temperature (float): The temperature in Kelvin.
        feels_like (float): The temperature it feels like in Kelvin.
        city (str): The city name.
        icon (str): The URL of the weather icon.
        created_at (datetime): The time the cache was created.
        updated_at (datetime): The time the cache was last updated.

    Note:
        Latitude and Longitude are unique together.
    """

    latitude = models.FloatField()
    longitude = models.FloatField()
    condition = models.CharField(
        max_length=20,
        choices=WeatherConstants.WEATHER_CONDITION_CHOICES,
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    feels_like = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    icon = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["latitude", "longitude"]
