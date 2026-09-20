"""Tests pour l'API FastAPI."""

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
    assert isinstance(response.json(), list)


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
    assert response.status_code == 201


def test_metrics_latest():
    """Test GET /metrics/latest."""
    response = client.get("/metrics/latest")
    assert response.status_code in [200, 204]  # 204 si aucune métrique