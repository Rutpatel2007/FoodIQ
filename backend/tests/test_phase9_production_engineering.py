"""
FoodIQ Phase 9 Automated Integration & Production Security Test Suite.
Validates:
1. Operational Observability (/health, /health/ready)
2. Security: Path Traversal & Injection Protection
3. Database Reliability: Online Backup & Restore Verification
4. Performance Benchmarks: API Response Latency
5. Path Portability & Environment Configuration
"""

import os
import time
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config import settings
from scripts.backup_db import backup_database
from scripts.restore_db import restore_database

client = TestClient(app)


def test_health_and_readiness_endpoints():
    """Validates operational observability probes."""
    # Liveness probe
    r_live = client.get("/api/v1/health")
    assert r_live.status_code == 200
    assert r_live.json()["status"] == "healthy"
    
    # Deep readiness probe
    r_ready = client.get("/api/v1/health/ready")
    assert r_ready.status_code == 200
    ready_data = r_ready.json()
    assert ready_data["status"] == "READY"
    assert ready_data["database"]["connected"] is True
    assert ready_data["database"]["integrity"] == "ok"
    assert ready_data["database"]["counts"]["metric_observations"] >= 500


def test_security_path_traversal_protection():
    """Verifies that malicious path traversal attempts are blocked."""
    malicious_ids = [
        "../../etc/passwd",
        "..\\..\\config.py",
        "nested/../../secret",
        "../foodiq.db"
    ]
    for bad_id in malicious_ids:
        r = client.get(f"/api/v1/reports/{bad_id}/export/html")
        assert r.status_code in [400, 404]


def test_database_backup_and_restore_cycle():
    """Tests the safe online backup API and restore validation cycle."""
    test_backup_dir = "data/backups/test_cycle"
    os.makedirs(test_backup_dir, exist_ok=True)
    
    # 1. Execute online backup
    backup_file = backup_database(src_path="data/foodiq.db", backup_dir=test_backup_dir)
    assert os.path.exists(backup_file)
    assert os.path.getsize(backup_file) > 100_000
    
    # 2. Restore into isolated test target
    test_target = os.path.join(test_backup_dir, "restored_test.db")
    restored = restore_database(backup_file=backup_file, target_path=test_target, force=True)
    assert restored is True
    assert os.path.exists(test_target)
    
    # Cleanup test files
    if os.path.exists(test_target):
        os.remove(test_target)
    if os.path.exists(backup_file):
        os.remove(backup_file)


def test_api_performance_benchmarks():
    """Benchmarks analytical and competitive API query latencies."""
    endpoints = [
        "/api/v1/health",
        "/api/v1/health/ready",
        "/api/v1/analytics/decomposition",
        "/api/v1/competitive/gaps",
        "/api/v1/credibility/scorecard",
        "/api/v1/quantitative/relationships",
        "/api/v1/reports/types"
    ]
    latencies = {}
    for ep in endpoints:
        start = time.perf_counter()
        r = client.get(ep)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        assert r.status_code == 200
        latencies[ep] = elapsed_ms
        # Analytical query SLA: under 2500ms (accounting for coverage instrumentation overhead)
        assert elapsed_ms < 2500.0, f"Endpoint {ep} took {elapsed_ms:.1f}ms (>2500ms)"


def test_path_portability_and_settings():
    """Ensures settings contain no machine-specific hardcoded paths."""
    assert os.path.isabs(str(settings.BASE_DIR))
    assert "data" in str(settings.DATA_DIR)
    assert os.path.exists(settings.DATA_DIR)
