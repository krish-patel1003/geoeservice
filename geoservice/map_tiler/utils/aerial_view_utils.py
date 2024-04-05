import asyncio
from uuid import uuid4

from map_tiler.formstaticimage import FormStaticImage


class AerialViewUtils:
    def __init__(self) -> None:
        self.form_static_image = FormStaticImage()

    def upload_aerial_view(self, latitude: float, longitude: float) -> str:
        """Get image of the location."""
        key = str(uuid4()) + ".png"
        self.form_static_image.run(
            longitude=float(longitude), latitude=float(latitude), key=key
        )

        return f"https://ariel-view-bucket.s3.ap-south-1.amazonaws.com/{key}"
