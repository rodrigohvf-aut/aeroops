from fastapi import APIRouter
from .models import Airport
from .services import create_airport, list_airports

router = APIRouter()

@router.get("/airports")
def get_airports():
    return {"airports": list_airports()}


@router.post("/airports")
def post_airport(airport: Airport):
    return create_airport(airport)