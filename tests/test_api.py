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
            "name": "Test Airport",
            "country": "Brazil",
            "latitude": -23.5,
            "longitude": -46.6,
        },
    )

    assert response.status_code == 200

    airport = response.json()
    try:
        assert airport["ident"] == "TEST"
    finally:
        client.delete(f"/airports/{airport['id']}")

def test_create_airport_without_country():
    response = client.post(
        "/airports",
        json={
            "ident": "INVALID",
            "name": "Invalid Airport",
            "latitude": -23.5,
            "longitude": -46.6,
        },
    )

    assert response.status_code == 422


def test_delete_airport():
    create_response = client.post(
        "/airports",
        json={
            "ident": "DELETE01",
            "name": "Airport to Delete",
            "country": "Brazil",
            "latitude": -23.5,
            "longitude": -46.6,
        },
    )

    airport_id = create_response.json()["id"]

    delete_response = client.delete(f"/airports/{airport_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Airport deleted successfully"

def test_database_health_when_connection_fails(monkeypatch):
    def simulated_failure():
        raise ConnectionError("Simulated database failure")

    monkeypatch.setattr("backend.main.get_connection", simulated_failure)

    test_client = TestClient(app, raise_server_exceptions=False)
    response = test_client.get("/health/database")

    assert response.status_code == 503