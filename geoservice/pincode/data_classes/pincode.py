from dataclasses import dataclass

@dataclass
class PincodeData:
    """Dataclass for storing pincode data."""

    pincode: str
    city: str
    state: str
    radius: float
    longitude: float
    latitude: float
    coordinates: list[tuple[float, float]]
    popularity: float
