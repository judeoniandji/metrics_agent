"""Tests pour le collecteur de métriques."""

import platform
import pytest
from app.collector import collect_system_metrics, MetricsCollectionError


def test_collect_system_metrics():
    """Test la collecte des métriques système."""
    metrics = collect_system_metrics()
    
    # Vérifier la structure
    assert "timestamp" in metrics
    assert "hostname" in metrics
    assert "cpu" in metrics
    assert "memory" in metrics
    assert "system" in metrics
    
    # Vérifier les valeurs CPU
    assert "percent" in metrics["cpu"]
    assert "logical_cores" in metrics["cpu"]
    assert 0 <= metrics["cpu"]["percent"] <= 100
    
    # Vérifier les valeurs mémoire
    assert "total_bytes" in metrics["memory"]
    assert "used_bytes" in metrics["memory"]
    assert metrics["memory"]["total_bytes"] > 0


def test_collect_system_metrics_windows():
    """Test que load_average retourne None sur Windows."""
    if platform.system().lower().startswith("win"):
        metrics = collect_system_metrics()
        assert metrics["system"]["load_1m"] is None
        assert metrics["system"]["load_5m"] is None
        assert metrics["system"]["load_15m"] is None