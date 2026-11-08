"""
FoodIQ Phase 8 Automated Integration Test Suite.
Validates:
1. Corporate Disclosure Monitoring Engine
2. Persistent Disclosure Register & Ingestion Queue
3. SHA-256 Checksum Calculation & Deduplication
4. Analyst Review, Approval & Rollback Controls
5. Data Quality & Financial Anomaly Scanner
6. Research Impact Analysis
7. REST API Endpoints (/api/v1/disclosures/*)
"""

import io
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.analytics.disclosure_intelligence import (
    get_disclosure_monitoring_overview,
    register_new_disclosure,
    approve_disclosure_ingestion,
    rollback_disclosure_ingestion,
    detect_data_anomalies,
    analyze_research_impact
)

client = TestClient(app)


def test_monitoring_overview():
    """Validates monitoring overview statistics, missing periods, and company coverage."""
    ov = get_disclosure_monitoring_overview()
    assert ov["status"] == "success"
    assert ov["total_disclosures_registered"] >= 14
    assert "ETERNAL" in ov["coverage_by_company"]
    assert "SWIGGY" in ov["coverage_by_company"]
    assert ov["coverage_by_company"]["ETERNAL"]["latest_period"] == "Q2 FY27"
    assert ov["coverage_by_company"]["SWIGGY"]["latest_period"] == "Q2 FY27"
    assert len(ov["next_anticipated_disclosures"]) == 2


def test_register_and_deduplicate_disclosure():
    """Tests SHA-256 computation, unique registration, and duplicate rejection."""
    import uuid
    nonce = uuid.uuid4().hex.encode()
    dummy_pdf = b"%PDF-1.4 Mock test filing for Q3 FY27 results disclosure " + nonce
    
    # First registration
    res1 = register_new_disclosure(
        company_id="ETERNAL",
        document_title="Eternal Limited Q3 FY27 Preliminary Results",
        document_category="Results Release",
        reporting_period="Q3 FY27",
        file_content_bytes=dummy_pdf,
        file_name="eternal_q3fy27_prelim.pdf"
    )
    assert res1["status"] == "REGISTERED_PENDING_REVIEW"
    disc_id = res1["disclosure_id"]
    assert disc_id.startswith("DISC-ETERNAL-Q3FY27-")
    assert "sha256_checksum" in res1
    
    # Duplicate registration attempt with identical bytes
    res2 = register_new_disclosure(
        company_id="ETERNAL",
        document_title="Eternal Limited Q3 FY27 Duplicate File",
        document_category="Results Release",
        reporting_period="Q3 FY27",
        file_content_bytes=dummy_pdf,
        file_name="duplicate_upload.pdf"
    )
    assert res2["status"] == "DUPLICATE_REJECTED"


def test_approval_and_rollback_controls():
    """Tests analyst approval and rollback of unapproved ingestions."""
    import uuid
    nonce = uuid.uuid4().hex.encode()
    test_pdf = b"%PDF-1.4 Mock filing to be approved and rolled back " + nonce
    reg = register_new_disclosure(
        company_id="SWIGGY",
        document_title="Swiggy Q3 FY27 Earnings Presentation",
        document_category="Presentation",
        reporting_period="Q3 FY27",
        file_content_bytes=test_pdf,
        file_name="swiggy_q3fy27_pres.pdf"
    )
    disc_id = reg["disclosure_id"]
    
    # 1. Approve
    app_res = approve_disclosure_ingestion(disc_id, analyst="Senior Data Lead")
    assert app_res["status"] == "APPROVED"
    assert app_res["disclosure_id"] == disc_id
    
    # 2. Rollback
    rb_res = rollback_disclosure_ingestion(disc_id, reason="Correction in disclosed restaurant take rates", analyst="Senior Data Lead")
    assert rb_res["status"] == "ROLLED_BACK"
    assert rb_res["new_status"] == "REJECTED"


def test_data_anomalies_scanner():
    """Validates the automated anomaly and financial identity scanner."""
    anomalies = detect_data_anomalies()
    assert isinstance(anomalies, list)
    # Ensure every anomaly has standard structure
    for anom in anomalies:
        assert "type" in anom
        assert "company" in anom
        assert "segment" in anom
        assert "quarter" in anom
        assert "detail" in anom


def test_research_impact_analysis():
    """Tests impact evaluation on downstream research objects."""
    impact = analyze_research_impact("SWIGGY", "Q3 FY27")
    assert impact["company"] == "SWIGGY"
    assert impact["status"] == "NEW_EVIDENCE_AVAILABLE"
    assert len(impact["affected_research_objects"]) >= 3
    obj_types = [o["object_type"] for o in impact["affected_research_objects"]]
    assert "STATISTICAL_STUDIES" in obj_types
    assert "SCENARIO_LAB" in obj_types


def test_api_disclosure_endpoints():
    """Tests FastAPI REST endpoints for disclosure intelligence."""
    # 1. Monitor endpoint
    r_mon = client.get("/api/v1/disclosures/monitor")
    assert r_mon.status_code == 200
    assert r_mon.json()["status"] == "success"
    
    # 2. Register endpoint
    r_reg = client.get("/api/v1/disclosures/register")
    assert r_reg.status_code == 200
    assert r_reg.json()["total_disclosures"] >= 14
    
    # 3. Anomalies endpoint
    r_anom = client.get("/api/v1/disclosures/anomalies")
    assert r_anom.status_code == 200
    assert "total_anomalies_detected" in r_anom.json()
    
    # 4. Impact endpoint
    r_imp = client.get("/api/v1/disclosures/impact/ETERNAL/Q3FY27")
    assert r_imp.status_code == 200
    assert len(r_imp.json()["affected_research_objects"]) >= 3
    
    # 5. Upload endpoint (multipart form)
    import uuid
    nonce = uuid.uuid4().hex.encode()
    file_bytes = b"%PDF-1.4 Unique API uploaded shareholder letter " + nonce
    files = {"file": ("api_upload_q3fy27.pdf", file_bytes, "application/pdf")}
    data = {
        "company_id": "ETERNAL",
        "document_title": "Eternal Q3 FY27 API Filing",
        "document_category": "Shareholder Letter",
        "reporting_period": "Q3 FY27"
    }
    r_up = client.post("/api/v1/disclosures/upload", data=data, files=files)
    assert r_up.status_code == 200
    uploaded_id = r_up.json()["disclosure_id"]
    
    # 6. Approve endpoint
    r_app = client.post(f"/api/v1/disclosures/{uploaded_id}/approve", json={"analyst": "API QA Auditor"})
    assert r_app.status_code == 200
    assert r_app.json()["status"] == "APPROVED"
    
    # 7. Rollback endpoint
    r_rb = client.post(f"/api/v1/disclosures/{uploaded_id}/rollback", json={"reason": "Test rollback via API", "analyst": "API QA Auditor"})
    assert r_rb.status_code == 200
    assert r_rb.json()["status"] == "ROLLED_BACK"
