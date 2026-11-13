from datetime import datetime
from pydantic import BaseModel, Field

class Airport(BaseModel):
    ident: str
    name: str
    country: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class AircraftPosition(BaseModel):
    icao24: str = Field(min_length=6, max_length=6, pattern=r"^[0-9A-Fa-f]{6}$")
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    observed_at: datetime