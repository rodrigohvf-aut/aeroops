from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_openapi_contains_required_routes():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    paths = schema["paths"]

    assert "/" in paths
    assert "/health" in paths
    assert "/airports" in paths
    assert "get" in paths["/airports"]
    assert "post" in paths["/airports"]