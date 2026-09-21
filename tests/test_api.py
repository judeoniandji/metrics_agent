

import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_health_endpoint():
    """Test l'endpoint /health."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_get():
    """Test GET /metrics."""
    response = client.get("/metrics")
    assert response.status_code == 200
    payload = response.json()
    # L'API renvoie un dictionnaire {"total": X, "metrics": [...]}
    assert isinstance(payload, dict)
    assert "metrics" in payload
    assert isinstance(payload["metrics"], list)


def test_metrics_post():
    """Test POST /metrics."""
    metrics = {
        "timestamp": "2026-09-20T11:00:00Z",
        "hostname": "test-host",
        "cpu": {"percent": 45.2, "logical_cores": 4},
        "memory": {
            "total_bytes": 8589934592,
            "available_bytes": 4294967296,
            "used_bytes": 4294967296,
            "percent": 50.0,
        },
        "system": {"load_1m": 1.5, "load_5m": 1.2, "load_15m": 1.0},
    }
    response = client.post("/metrics", json=metrics)
    # Si le statut n'est pas 201, afficher la raison de la validation Pydantic (422)
    assert response.status_code == 201, f"Erreur validation: {response.json()}"


def test_metrics_latest():
    """Test GET /metrics/latest."""
    # Insertion préalable d'une métrique pour éviter l'erreur 404 (Not Found)
    # si l'API nécessite au moins une métrique enregistrée
    sample_metrics = {
        "timestamp": "2026-09-20T11:00:00Z",
        "hostname": "test-host",
        "cpu": {"percent": 10.0, "logical_cores": 2},
        "memory": {
            "total_bytes": 4096,
            "available_bytes": 2048,
            "used_bytes": 2048,
            "percent": 50.0,
        },
        "system": {"load_1m": 0.5, "load_5m": 0.5, "load_15m": 0.5},
    }
    client.post("/metrics", json=sample_metrics)

    response = client.get("/metrics/latest")
    assert response.status_code in [200, 204]