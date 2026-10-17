from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_existing_routes_still_work():
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/airports").status_code == 200