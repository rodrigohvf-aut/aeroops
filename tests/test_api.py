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
            closed INTEGER,
            le_latitude_deg REAL,
            le_longitude_deg REAL,
            he_latitude_deg REAL,
            he_longitude_deg REAL
        )
        """
    )
    connection.executemany(
        """
        INSERT INTO runways (
            id, airport_ident, le_ident, he_ident,
            length_ft, width_ft, surface, lighted, closed,
            le_latitude_deg, le_longitude_deg,
            he_latitude_deg, he_longitude_deg
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                1, "DAAE", "08", "26", 7874, 148, "ASP", 1, 0,
                36.71, 5.05, 36.71, 5.08,
            ),
            (
                2, "EGLL", "09L", "27R", 12799, 164, "ASP", 1, 0,
                None, None, None, None,
            ),
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

    runway = response.json()["runways"][0]
    assert runway["airport_ident"] == "DAAE"
    assert runway["le_ident"] == "08"
    assert runway["le_latitude_deg"] == 36.71
    assert runway["he_longitude_deg"] == 5.08


def test_get_runway_count(monkeypatch, tmp_path):
    from backend import services

    database_path = tmp_path / "runway_count_test.db"

    connection = sqlite3.connect(database_path)
    connection.execute(
        "CREATE TABLE runways (id INTEGER PRIMARY KEY)"
    )
    connection.executemany(
        "INSERT INTO runways (id) VALUES (?)",
        [(1,), (2,)],
    )
    connection.commit()
    connection.close()

    def test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(services, "get_connection", test_connection)

    response = client.get("/runways/count")

    assert response.status_code == 200
    assert response.json() == {"total_runways": 2}
    

def test_search_airports_by_code_name_and_country(monkeypatch, tmp_path):
    from backend import services

    database_path = tmp_path / "airport_search_test.db"

    connection = sqlite3.connect(database_path)
    connection.execute(
        """
        CREATE TABLE airports (
            id INTEGER PRIMARY KEY,
            ident TEXT NOT NULL,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
        """
    )
    connection.executemany(
        """
        INSERT INTO airports
            (id, ident, name, country, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "DAAE", "Soummam Airport", "DZ", 36.7, 5.0),
            (2, "SBGR", "Guarulhos Airport", "BR", -23.4, -46.5),
            (3, "EGLL", "Heathrow Airport", "GB", 51.4, -0.4),
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

    searches = [
        ("daae", "DAAE"),       # Código, sem diferenciar maiúsculas
        ("Heathrow", "EGLL"),   # Nome
        ("BR", "SBGR"),         # País
    ]

    for search, expected_ident in searches:
        response = client.get("/airports", params={"search": search})

        assert response.status_code == 200
        assert [airport["ident"] for airport in response.json()["airports"]] == [
            expected_ident
        ]


def test_airport_pagination(monkeypatch, tmp_path):
    from backend import services

    database_path = tmp_path / "pagination_test.db"

    connection = sqlite3.connect(database_path)
    connection.execute(
        """
        CREATE TABLE airports (
            id INTEGER PRIMARY KEY,
            ident TEXT NOT NULL,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
        """
    )
    connection.executemany(
        """
        INSERT INTO airports
            (id, ident, name, country, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "AAAA", "Alpha Airport", "BR", 0, 0),
            (2, "BBBB", "Bravo Airport", "BR", 0, 0),
            (3, "CCCC", "Charlie Airport", "PT", 0, 0),
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

    first = client.get("/airports", params={"page": 1, "limit": 2})
    second = client.get("/airports", params={"page": 2, "limit": 2})

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["total"] == second.json()["total"] == 3
    assert [item["ident"] for item in first.json()["airports"]] == [
        "AAAA", "BBBB"
    ]
    assert [item["ident"] for item in second.json()["airports"]] == [
        "CCCC"
    ]


def test_manual_aircraft_position_rejects_opensky_source():
    response = client.post(
        "/aircraft/positions",
        json={
            "icao24": "abc123",
            "latitude": -23.35,
            "longitude": -46.20,
            "observed_at": "2026-11-13T12:15:00Z",
            "source": "opensky",
        },
    )

    assert response.status_code == 422


def test_create_and_read_simulated_aircraft_position(monkeypatch, tmp_path):
    from backend import services

    database_path = tmp_path / "aircraft_positions_test.db"

    connection = sqlite3.connect(database_path)
    connection.execute(
        """
        CREATE TABLE aircraft_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icao24 TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            observed_at TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'simulated',
            UNIQUE (icao24, observed_at)
        )
        """
    )
    connection.commit()
    connection.close()

    def test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(services, "get_connection", test_connection)
    monkeypatch.setattr(services, "DATABASE_URL", None)

    created = client.post(
        "/aircraft/positions",
        json={
            "icao24": "abc123",
            "latitude": -23.35,
            "longitude": -46.20,
            "observed_at": "2026-11-13T12:15:00Z",
            "source": "simulated",
        },
    )

    assert created.status_code == 201
    assert created.json()["source"] == "simulated"

    history = client.get("/aircraft/abc123/positions")
    assert history.status_code == 200
    assert len(history.json()["positions"]) == 1
    assert history.json()["positions"][0]["source"] == "simulated"

    latest = client.get("/aircraft/positions/latest")
    assert latest.status_code == 200
    assert len(latest.json()["positions"]) == 1
    assert latest.json()["positions"][0]["source"] == "simulated"