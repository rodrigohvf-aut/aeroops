import sqlite3
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


def test_cors_allows_local_frontend():
    response = client.options(
        "/airports",
        headers={
            "Origin": "http://127.0.0.1:5500",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"


def test_delete_airport_that_does_not_exist():
    response = client.delete("/airports/999999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Airport not found"}



def test_rejects_invalid_coordinates():
    invalid_coordinates = [
        (91, 0),
        (-91, 0),
        (0, 181),
        (0, -181),
    ]

    for latitude, longitude in invalid_coordinates:
        response = client.post(
            "/airports",
            json={
                "ident": "INVALID",
                "name": "Invalid Airport",
                "country": "Brazil",
                "latitude": latitude,
                "longitude": longitude,
            },
        )

        assert response.status_code == 422

def test_get_airport_runways(monkeypatch, tmp_path):
    from backend import services

    database_path = tmp_path / "runways_test.db"

    connection = sqlite3.connect(database_path)
    connection.execute(
        """
        CREATE TABLE runways (
            id INTEGER PRIMARY KEY,
            airport_ident TEXT,
            le_ident TEXT,
            he_ident TEXT,
            length_ft INTEGER,
            width_ft INTEGER,
            surface TEXT,
            lighted INTEGER,
            closed INTEGER
        )
        """
    )
    connection.executemany(
        """
        INSERT INTO runways
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "DAAE", "08", "26", 7874, 148, "ASP", 1, 0),
            (2, "EGLL", "09L", "27R", 12799, 164, "ASP", 1, 0),
        ],
    )
    connection.commit()
    connection.close()

    def test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(services, "get_connection", test_connection)
    monkeypatch.setattr(services, "DATABASE_URL", None)

    response = client.get("/airports/DAAE/runways")

    assert response.status_code == 200
    assert len(response.json()["runways"]) == 1
    assert response.json()["runways"][0]["le_ident"] == "08"
    assert response.json()["runways"][0]["airport_ident"] == "DAAE"