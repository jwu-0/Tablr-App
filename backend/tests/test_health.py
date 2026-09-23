from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_ok():
    with TestClient(create_app()) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_schema_is_generated():
    schema = create_app().openapi()
    assert schema["info"]["title"] == "Tablr API"
    assert "/v1/me" in schema["paths"]


def test_protected_endpoint_requires_a_token():
    with TestClient(create_app()) as client:
        response = client.get("/v1/me")
    assert response.status_code == 401
