from django.db import models


# TODO: Single Model Google Maps API Cache
class GooglePlacesCache(models.Model):
    """Model for storing Google Places API data in the cache.

    Attributes:
        user_longitude (float): The longitude of the user.
        user_latitude (float): The latitude of the user.
        longitude (float): The longitude of the place.
        latitude (float): The latitude of the place.
        address (str): The address of the place.
        place_id (str): The place id of the place.
        plus_code (str): The plus code of the place.
        created_at (datetime): The time the cache was created.
        updated_at (datetime): The time the cache was last updated.
    """

    user_longitude = models.FloatField(null=True, blank=True)
    user_latitude = models.FloatField(null=True, blank=True)
    h3_id = models.CharField(max_length=255, db_index=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255, db_index=True)
    plus_code = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(choices=[('places', 'Places'), ('reverse_geocode', 'ReverseGeocode')], max_length=50)


    def __str__(self):
        return f"{self.h3_id} ({self.longitude}, {self.latitude})"
    
    class Meta:
        unique_together = ["h3_id", "place_id"]
        