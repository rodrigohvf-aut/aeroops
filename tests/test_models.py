import pytest
from pydantic import ValidationError
from backend.models import Airport


def test_airport_valid():
    airport = Airport(
        ident="SBGR",
        name="Aeroporto Internacional de Guarulhos",
        country="Brasil",
        latitude=-23.4356,
        longitude=-46.4731,
    )

    assert airport.ident == "SBGR"
    assert airport.country == "Brasil"


def test_airport_requires_ident():
    with pytest.raises(ValidationError):
        Airport(
            name="Aeroporto de Teste",
            country="Brasil",
            latitude=10,
            longitude=10,
        )