from pydantic import BaseModel, Field


class Airport(BaseModel):
    ident: str
    name: str
    country: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)