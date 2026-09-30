from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_route_exists():
    response = client.get("/health")
    assert response.status_code in (200, 503)

def test_analyze_validation():
    response = client.post("/analyze", json={})
    assert response.status_code == 422
