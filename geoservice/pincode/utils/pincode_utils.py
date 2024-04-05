import re

from pincode.constants import PincodeConstants
from pincode.data_classes.pincode import PincodeData
from pykml import parser
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.strtree import STRtree


class PincodeUtils:
    def __init__(self):
        """Initializes the PincodeUtils class.
        It parses the pincode data from the KML file and creates a spatial index.
        """
        self.kml_data = self._parse_kml()
        self.spatial_index = self._create_spatial_index(self.kml_data)

    @staticmethod
    def _parse_kml() -> list[PincodeData]:
        """Parses the pincode data from the KML file.

        Returns:
            list[PincodeData]: A list of PincodeData instances containing the pincode
            data.
        """
        kml_data = []
        with open(PincodeConstants.KML_FILE_PATH, "r") as kml_file:
            doc = parser.parse(kml_file).getroot()
            fld = doc.Document.Folder

            for placemark in list(fld.Placemark):
                pincode = placemark.name.text
                simple_data = placemark.ExtendedData.SchemaData.SimpleData
                state = simple_data[1].text
                city = simple_data[2].text
                popularity = simple_data[4].text
                longitute = simple_data[5].text
                latitude = simple_data[6].text
                radius = simple_data[7].text

                # Handle MultiGeometry and iterate through each Polygon
                coordinates_text = ""
                try:
                    multi_geometry = placemark.MultiGeometry
                except AttributeError:
                    multi_geometry = None
                if multi_geometry is not None:
                    for polygon in multi_geometry.Polygon:
                        coordinates_text += (
                            " " + polygon.outerBoundaryIs.LinearRing.coordinates.text
                        )

                else:
                    coordinates_text = (
                        placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text
                    )

                cleaned_coordinates = re.sub(r"\s*,\s*", ",", coordinates_text)

                coords = tuple(cleaned_coordinates.split())
                coordinates = [tuple(map(float, c.split(","))) for c in coords]

                pincode_info = PincodeData(
                    pincode=pincode,
                    city=city,
                    state=state,
                    radius=radius,
                    longitude=longitute,
                    latitude=latitude,
                    popularity=popularity,
                    coordinates=coordinates,
                )

                kml_data.append(pincode_info)

        return kml_data

    @staticmethod
    def _create_spatial_index(pincodes_data: list[PincodeData]) -> STRtree:
        """Creates a spatial index for the pincode data.

        Returns:
            STRtree: The spatial index for the pincode data.
        """
        polygons = []
        for pincode_info in pincodes_data:
            coordinates = pincode_info.coordinates

            polygon = Polygon(coordinates)
            polygons.append(polygon)

        spatial_index = STRtree(polygons)

        return spatial_index

    def get_pincode_data(self, longitude: float, latitude: float) -> PincodeData:
        """Finds the pincode for the given longitude and latitude.

        Args:
            longitude (float): The longitude of the location.
            latitude (float): The latitude of the location.

        Returns:
            City: The city model object.
            Pincode: The pincode model object.
        """
        point = Point(longitude, latitude)
        intersecting_polygons_idx = self.spatial_index.query(point).tolist()

        if not intersecting_polygons_idx:
            return None

        matching_pincodes = []
        for idx in intersecting_polygons_idx:
            pincode_info = self.kml_data[idx]
            matching_pincodes.append(pincode_info)
        pincode_data = max(matching_pincodes, key=lambda x: x.popularity)

        pincode_obj = PincodeData(
            pincode=pincode_data.pincode,
            city=pincode_data.city,
            state=pincode_data.state,
            radius=pincode_data.radius,
            longitude=pincode_data.longitude,
            latitude=pincode_data.latitude,
            coordinates=pincode_data.coordinates,
            popularity=pincode_data.popularity,
        )

        return pincode_obj
