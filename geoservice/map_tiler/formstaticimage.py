import asyncio
from io import BytesIO

import cv2
import geotiler
import numpy as np
from core.constants import S3Constants
from core.utils import s3_utils


class FormStaticImage:
    def __init__(self) -> None:
        pass

    def run(self, longitude: float, latitude: float, key: str):
        """This function is used to serialize the execution of generating static map of the location, adding marker to the location and tilting the map.

        Args:
            longitude (float): Longitude of the location.
            latitude (float): Latitude of the location.
            key (str): Key to save the image.
        """
        height = 540
        width = int((4 / 3) * height)

        fetched_map = geotiler.Map(
            center=(longitude, latitude), zoom=16, size=(width, height)
        )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        aerial_view = geotiler.render_map(fetched_map)
        aerial_view = cv2.cvtColor(np.array(aerial_view), cv2.COLOR_BGR2RGB)

        BytesIO()
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 50]
        _, encoded_image = cv2.imencode(key, np.array(aerial_view), encode_param)
        image_data = encoded_image.tobytes()

        response = s3_utils.put_object(
            key=key, body=image_data, bucket_name=S3Constants.AERIAL_VIEW_BUCKET_NAME
        )

        return response
