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

    # Test invalid company filter
    invalid_res = client.get("/api/v1/documents?company_id=NON_EXISTENT")
    assert invalid_res.status_code == 200
    assert len(invalid_res.json()) == 0

def test_api_segments(client):
    res = client.get("/api/v1/segments")
    assert res.status_code == 200
    assert len(res.json()) >= 12

    eternal_segs = client.get("/api/v1/segments?company_id=ETERNAL")
    assert eternal_segs.status_code == 200
    assert len(eternal_segs.json()) == 7

def test_api_metrics(client):
    res = client.get("/api/v1/metrics")
    assert res.status_code == 200
    assert len(res.json()) >= 50

    qcomm_metrics = client.get("/api/v1/metrics?segment_scope=QuickCommerce")
    assert qcomm_metrics.status_code == 200
    assert len(qcomm_metrics.json()) > 0

def test_api_observations(client):
    res = client.get("/api/v1/observations?limit=10")
    assert res.status_code == 200
    assert len(res.json()) == 10

    # Test filtering by company and fiscal year
    filtered = client.get("/api/v1/observations?company_id=SWIGGY&fiscal_year=FY26&limit=50")
    assert filtered.status_code == 200
    for obs in filtered.json():
        assert obs["company_id"] == "SWIGGY"
        assert obs["fiscal_year"] == "FY26"

    # Test pagination out of range
    empty_page = client.get("/api/v1/observations?offset=10000")
    assert empty_page.status_code == 200
    assert len(empty_page.json()) == 0

    # Test invalid limit (negative or >1000)
    bad_limit = client.get("/api/v1/observations?limit=-5")
    assert bad_limit.status_code == 422

def test_api_observation_by_id_and_lineage(client):
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

    # Test non-existent observation ID (404)
    res_404 = client.get("/api/v1/observations/NON_EXISTENT_OBS_ID")
    assert res_404.status_code == 404

    res_lin_404 = client.get("/api/v1/observations/NON_EXISTENT_OBS_ID/lineage")
    assert res_lin_404.status_code == 404

def test_api_data_quality(client):
    res_summary = client.get("/api/v1/data-quality/summary")
    assert res_summary.status_code == 200
    data = res_summary.json()
    assert data["total_flags"] >= 20
    assert "CRITICAL" in data["by_severity"]
    assert "HIGH" in data["by_severity"]

    res_issues = client.get("/api/v1/data-quality/issues")
    assert res_issues.status_code == 200
    assert len(res_issues.json()) >= 20

    crit_issues = client.get("/api/v1/data-quality/issues?severity=CRITICAL")
    assert crit_issues.status_code == 200
    assert len(crit_issues.json()) >= 2

def test_api_comparability_rules(client):
    res = client.get("/api/v1/comparability/rules")
    assert res.status_code == 200
    assert len(res.json()) >= 5

    direct_rules = client.get("/api/v1/comparability/rules?tier=DIRECT")
    assert direct_rules.status_code == 200
    assert len(direct_rules.json()) >= 1

    # Test POST evaluate endpoint
    eval_res = client.post("/api/v1/comparability/evaluate", json={
        "metric_a": "swiggy_gov_cr",
        "metric_b": "eternal_food_nov"
    })
    assert eval_res.status_code == 200
    assert eval_res.json()["can_compare_directly"] is False
    assert eval_res.json()["tier"] == "INCOMPARABLE"

def test_api_guidance(client):
    res = client.get("/api/v1/guidance")
    assert res.status_code == 200
    assert len(res.json()) >= 18
