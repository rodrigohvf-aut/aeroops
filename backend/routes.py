from fastapi import APIRouter, HTTPException, Query
from .models import Airport
from .services import (create_airport,delete_airport,list_airports,list_runways,count_runways,count_airports,count_countries,)

router = APIRouter()


@router.get("/airports")
def get_airports(
    search: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    offset = (page - 1) * limit

    return {
        "airports": list_airports(search, limit, offset),
        "total": count_airports(search),
        "page": page,
        "limit": limit,
    }


@router.post("/airports")
def post_airport(airport: Airport):
    return create_airport(airport)


@router.delete("/airports/{airport_id}")
def remove_airport(airport_id: int):
    deleted = delete_airport(airport_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Airport not found")

    return {"message": "Airport deleted successfully"}


@router.get("/airports/{airport_ident}/runways")
def get_airport_runways(airport_ident: str):
    return {"runways": list_runways(airport_ident)}


@router.get("/runways/count")
def get_runway_count():
    return {"total_runways": count_runways()}


@router.get("/countries/count")
def get_country_count():
    return {"total_countries": count_countries()}