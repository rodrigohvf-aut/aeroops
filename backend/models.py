from pydantic import BaseModel

class Airport(BaseModel):
    ident: str
    name: str
    country: str
    latitude: float
    longitude: float