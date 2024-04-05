import threading

import requests
from django.conf import settings
from django.utils import timezone
from weather.constants import WeatherConstants
from weather.models import WeatherCache


class WeatherUtils:
    CACHE_TTL = WeatherConstants.WEATHER_CACHE_TTL
    CACHE_UPDDATE_IN_PROGRESS = False

    @staticmethod
    def create_icon_url(icon: str) -> str:
        """Generates the URL for the weather icon.

        Args:
            icon (str): The icon code.

        Returns:
            str: The URL of the weather icon.
        """
        url = f"https://openweathermap.org/img/wn/{icon}.png"
        return url

    @staticmethod
    def parse_data(data: dict) -> dict:
        """Parses the weather data from the OpenWeatherMap API.

        Args:
            data (dict): The weather data fetched from the API.

        Returns:
            dict: A dictionary containing the parsed weather data.
        """
        icon = data["weather"][0]["icon"]
        icon_url = WeatherUtils.create_icon_url(icon)

        parsed_data = {
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "city": data["name"],
            "icon": icon_url,
        }

        return parsed_data

    @staticmethod
    def fetch_data(longitude: float, latitude: float) -> dict:
        """Fetches weather data from the OpenWeatherMap API.

        Args:
            longitude (float): The longitude of the location.
            latitude (float): The latitude of the location.

        Returns:
            dict: A dictionary containing the weather data.
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={settings.OPENWEATHER_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = WeatherUtils.parse_data(response.json())
        return data

    def get_cache(self, longitude: float, latitude: float) -> WeatherCache:
        """Retrieves weather data from the cache or
        fetches from the API and updates the cache.

        Args:
            longitude (float): The longitude of the location.
            latitude (float): The latitude of the location.

        Returns:
            WeatherCache: The WeatherCache object containing the weather data.
        """
        data = self.fetch_data(longitude=longitude, latitude=latitude)
        weather_object, created = WeatherCache.objects.update_or_create(
            longitude=longitude, latitude=latitude, defaults=data
        )

        return weather_object

    def is_update_required(self, weather_object: WeatherCache) -> bool:
        """Checks if the weather data needs to be updated based on the cache TTL.

        Args:
            weather_object (WeatherCache): The WeatherCache object to be checked.

        Returns:
            bool: True if the weather data needs to be updated, False otherwise.
        """
        current_time = timezone.now()
        time_difference = current_time - weather_object.updated_at

        if time_difference.total_seconds() > self.CACHE_TTL:
            return True

        return False

    def update_cache(self, longitude: float, latitude: float):
        """Updates the weather data in the cache for a given location.

        Args:
            longitude (float): The longitude of the location.
            latitude (float): The latitude of the location.
        """
        if not self.CACHE_UPDDATE_IN_PROGRESS:
            self.CACHE_UPDDATE_IN_PROGRESS = True
            self.get_cache(longitude=longitude, latitude=latitude)
            self.CACHE_UPDDATE_IN_PROGRESS = False

    def get_data(self, longitude: float, latitude: float) -> WeatherCache:
        """Retrieves weather data from the cache or API,
        and triggers a cache update if required.

        Args:
            longitude (float): The longitude of the location.
            latitude (float): The latitude of the location.

        Returns:
            WeatherCache: The WeatherCache object containing the weather data.
        """
        try:
            weather_object = WeatherCache.objects.get(
                longitude=longitude, latitude=latitude
            )

        except WeatherCache.DoesNotExist:
            # fetch new data from the API and update the data
            weather_object = self.get_cache(longitude=longitude, latitude=latitude)

        if self.is_update_required(weather_object):
            threading.Thread(
                target=self.update_cache, args=(longitude, latitude)
            ).start()

        return weather_object
