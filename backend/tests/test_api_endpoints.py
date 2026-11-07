import pytest

def test_api_health(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_api_companies(client):
    res = client.get("/api/v1/companies")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    names = {c["canonical_name"] for c in data}
    assert "Swiggy Limited" in names
    assert "Eternal Limited" in names

def test_api_documents(client):
    res = client.get("/api/v1/documents")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 14

    # Test filtering by company
    swiggy_res = client.get("/api/v1/documents?company_id=SWIGGY")
    assert swiggy_res.status_code == 200
    assert len(swiggy_res.json()) == 6

def test_api_segments(client):
    res = client.get("/api/v1/segments")
    assert res.status_code == 200
    assert len(res.json()) >= 12

def test_api_metrics(client):
    res = client.get("/api/v1/metrics")
    assert res.status_code == 200
    assert len(res.json()) >= 50

def test_api_observations(client):
    res = client.get("/api/v1/observations?limit=10")
    assert res.status_code == 200
    assert len(res.json()) == 10

def test_api_observation_by_id_and_lineage(client):
    # Fetch first observation
    res = client.get("/api/v1/observations?limit=1")
    obs_id = res.json()[0]["observation_id"]

    res_single = client.get(f"/api/v1/observations/{obs_id}")
    assert res_single.status_code == 200
    assert res_single.json()["observation_id"] == obs_id

    res_lineage = client.get(f"/api/v1/observations/{obs_id}/lineage")
    assert res_lineage.status_code == 200
    lin = res_lineage.json()
    assert lin["observation_id"] == obs_id
    assert "provenance" in lin
    assert "file_checksum_sha256" in lin["provenance"]

def test_api_data_quality(client):
    res_summary = client.get("/api/v1/data-quality/summary")
    assert res_summary.status_code == 200
    data = res_summary.json()
    assert data["total_flags"] >= 20

    res_issues = client.get("/api/v1/data-quality/issues")
    assert res_issues.status_code == 200
    assert len(res_issues.json()) >= 20

def test_api_comparability_rules(client):
    res = client.get("/api/v1/comparability/rules")
    assert res.status_code == 200
    assert len(res.json()) >= 5

def test_api_guidance(client):
    res = client.get("/api/v1/guidance")
    assert res.status_code == 200
    assert len(res.json()) >= 18
