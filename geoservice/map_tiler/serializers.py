from rest_framework import serializers


class MapImageResponseSerializer(serializers.Serializer):
    """Serializer for Map Image Response.

    Attributes:
        image_url (str): The image url.
    """

    image_url = serializers.CharField()
