from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_airport():
    response = client.post(
        "/airports",
        json={
            "ident": "TEST",
            "name": "Aeroporto de Teste",
            "country": "Brasil",
            "latitude": -23.5,
            "longitude": -46.6,
        },
    )

    assert response.status_code == 200
    assert response.json()["ident"] == "TEST"