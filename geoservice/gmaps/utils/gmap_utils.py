import threading

import requests
from django.conf import settings
from django.utils import timezone
from gmaps.constants import GMapsConstants
from gmaps.models import GooglePlacesCache
import h3


class GooglePlacesAPIWrapper:
    CACHE_TTL = GMapsConstants.PLACES_CACHE_TTL
    CACHE_UPDDATE_IN_PROGRESS = False

    def __init__(self):
        self.api_key = settings.GOOGLE_PLACES_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/"

    def _get(self, endpoint: str, params: dict) -> dict:
        """Make a GET request to the API.

        Args:
            endpoint (str): The endpoint to make the request to.
            params (dict): The query parameters to pass in the request.


        Returns:
            dict: The response data.
        """
        params["key"] = self.api_key
        response = requests.get(self.base_url + endpoint, params=params)
        response.raise_for_status()
        return response.json()


    def is_update_required(self, cache: GooglePlacesCache) -> bool:
        """Check if the cache needs to be updated.


        Args:
            cache (GooglePlacesCache): The cache object.

        Returns:
            bool: True if the cache needs to be updated, False otherwise.
        """
        current_time = timezone.now()
        time_difference = current_time - cache.updated_at

        if time_difference.total_seconds() > self.CACHE_TTL:
            return True
        

    def _get_reverse_geocode_data(self, longitude: float, latitude: float) -> dict:
        """Get reverse geocode data for a longitude and latitude.

        Args:
            longitude (float): The longitude of the place.
            latitude (float): The latitude of the place.

        Returns:
            dict: The reverse geocode data.
        """
        params = {
            "latlng": f"{latitude},{longitude}",
        }
        reverse_geocode_data = self._get("geocode/json", params)
        return reverse_geocode_data


    def _parse_reverse_geocode_data(self, reverse_geocode_data: dict) -> dict:
        """Parse reverse geocode data.

        Args:
            reverse_geocode_data (dict): The reverse geocode data.

        Returns:
            dict: The parsed reverse geocode data.
        """
        print(reverse_geocode_data)
        parsed_data = {
            "longitude": reverse_geocode_data["results"][0]["geometry"]["location"][
                "lng"
            ],
            "latitude": reverse_geocode_data["results"][0]["geometry"]["location"][
                "lat"
            ],
            "address": reverse_geocode_data["results"][0]["formatted_address"],
            "place_id": reverse_geocode_data["results"][0]["place_id"],
            "plus_code": reverse_geocode_data["plus_code"]["compound_code"] if "compound_code" in reverse_geocode_data["plus_code"] else None,
        }

        return parsed_data


    def _get_geocode_data(self, place_id: str) -> dict:
        """Get geocode data for a place id.

        Args:
            place_id (str): The place id of the place.


        Returns:
            dict: The geocode data.
        """
        params = {
            "place_id": place_id,
        }
        geocode_data = self._get("geocode/json", params)
        return geocode_data
        

    def _parse_geocode_data(self, geocode_data: dict) -> dict:
        """Parse geocode data.

        Args:
            geocode_data (dict): The geocode data.
            address (str): The address of the place.


        Returns:
            dict: The parsed geocode data.
        """
        parsed_data = {
            "longitude": geocode_data["results"][0]["geometry"]["location"]["lng"],
            "latitude": geocode_data["results"][0]["geometry"]["location"]["lat"],
            "address": geocode_data["results"][0]["formatted_address"],
        }

        return parsed_data
    

    def fetch_reverse_geocode_data(self, longitude: float, latitude: float) -> dict:
        """Fetch reverse geocode data from the API, and parse data.

        Args:
            longitude (float): The longitude of the place.
            latitude (float): The latitude of the place.

        Returns:
            dict: The parsed reverse geocode data.
        """
        reverse_geocode_data = self._get_reverse_geocode_data(
            longitude=longitude, latitude=latitude
        )
        parsed_data = self._parse_reverse_geocode_data(
            reverse_geocode_data=reverse_geocode_data
        )
        
        return parsed_data


    def fetch_geocode_data(self, place_id: str) -> dict:
        """Fetch geocode data from the API, and parse data.

        Args:
            place_id (str): The place id of the place.
            address (str): The address of the place.


        Returns:
            dict: The parsed geocode data.
        """
        geocode_data = self._get_geocode_data(place_id)

        prased_data = self._parse_geocode_data(
            geocode_data=geocode_data
        )
        return prased_data
    

    def set_places_cache(self, longitude: float=None, latitude: float=None, place_id: str=None) -> GooglePlacesCache:
        """
        Set the cache object for a place id or Lat and Long.
        If the cache does not exist, create it.

        Args:
            longitude (float): The longitude of the place.
            latitude (float): The latitude of the place.
            place_id (str): The place id of the place.
        """
        if place_id:
            data = self.fetch_geocode_data(place_id=place_id)
            h3_id = h3.geo_to_h3(lat=data["latitude"], lng=data["longitude"], resolution=12)
            cache, _ = GooglePlacesCache.objects.update_or_create(
                place_id=place_id,
                h3_id=h3_id,
                source='places',
                defaults=data,
            )
            return cache
        
        elif longitude and latitude:
            data = self.fetch_reverse_geocode_data(longitude=longitude, latitude=latitude)
            h3_id = h3.geo_to_h3(lat=latitude, lng=longitude, resolution=12)
            cache, _ = GooglePlacesCache.objects.update_or_create(
                user_longitude=longitude,
                user_latitude=latitude,
                h3_id=h3_id,
                source='reverse_geocode',
                defaults=data,
            )
            return cache
        else:
            raise ValueError("Either place_id or longitude and latitude must be provided.")


    def update_places_cache(self, longitude: float=None, latitude: float=None, place_id: str=None, update_reverse_geocode: bool=True) -> None:
        """Update the cache, if required.

        Args:
            longitude (float): The longitude of the place.
            latitude (float): The latitude of the place.
        """
        if not self.CACHE_UPDDATE_IN_PROGRESS:
            self.CACHE_UPDDATE_IN_PROGRESS = True
            if update_reverse_geocode:  
                self.set_places_cache(longitude=longitude, latitude=latitude)
            else:
                self.set_places_cache(place_id=place_id)
            self.CACHE_UPDDATE_IN_PROGRESS = False

    
    def get_places_cache(self, longitude: float=None, latitude: float=None, place_id: str=None) -> GooglePlacesCache:
        """Get the cache object for a place id or Lat and Long.
        If the cache does not exist, create it.

        Args:
            longitude (float): The longitude of the place.
            latitude (float): The latitude of the place.
            place_id (str): The place id of the place.

        Returns:
            GooglePlacesCache: The GooglePlacesCache object.
        """
        if place_id:
            update_reverse_geocode = False
            caches = GooglePlacesCache.objects.filter(place_id=place_id)
            places_cache = [cache for cache in caches if cache.source == 'places']
            reverse_geocode_cache = [cache for cache in caches if cache.source == 'reverse_geocode']

            if places_cache:
                cache = places_cache[0]
            elif reverse_geocode_cache:
                cache = reverse_geocode_cache[0]
            else:
                cache = self.set_places_cache(place_id=place_id)
                
        elif longitude and latitude:
            update_reverse_geocode = True
            h3_id = h3.geo_to_h3(lat=latitude, lng=longitude, resolution=12)
            caches = GooglePlacesCache.objects.filter(h3_id=h3_id)
            places_cache = [cache for cache in caches if cache.source == 'places']
            reverse_geocode_cache = [cache for cache in caches if cache.source == 'reverse_geocode']

            if reverse_geocode_cache:
                cache = reverse_geocode_cache[0]
            elif places_cache:
                cache = places_cache[0]
            else:
                cache = self.set_places_cache(longitude=longitude, latitude=latitude)
        else:
            raise ValueError("Either place_id or longitude and latitude must be provided.")

        if self.is_update_required(cache):
            threading.Thread(target=self.update_places_cache, args=(longitude, latitude, place_id, update_reverse_geocode)).start()

        return cache