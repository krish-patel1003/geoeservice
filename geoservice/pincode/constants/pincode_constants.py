import os

from django.conf import settings


class PincodeConstants:
    KML_FILE_PATH = os.path.join(
        settings.BASE_DIR, "pincode/data/compiled_pincodes_data.kml"
    )
