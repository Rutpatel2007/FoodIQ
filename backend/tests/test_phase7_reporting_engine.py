"""
FoodIQ Phase 7 Automated Integration Test Suite.
Validates:
1. 9 Institutional Report Types
2. Modular Report Generation from live analytical engines
3. Evidence & Citation Verification Engine
4. Automated Report Verification Scorecard
5. Multi-Format Exports (HTML, PDF, DOCX, CSV)
6. REST API Endpoints (/api/v1/reports/*)
7. Report Persistence & Versioning
"""

import os
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.analytics.report_engine import (
    REPORT_TYPES,
    generate_institutional_report,
    verify_report_citations,
    verify_complete_report,
    export_report_to_html,
    export_report_to_pdf,
    export_report_to_docx,
    export_report_to_csv,
    list_generated_reports,
    get_generated_report_by_id
)

client = TestClient(app)


def test_supported_report_types():
    """Confirms all 9 mandated report types are defined and accessible."""
    assert len(REPORT_TYPES) == 9
    required_types = [
        "COMPREHENSIVE", "COMPANY_SPECIFIC", "BUSINESS_SEGMENT",
        "QUARTERLY_PERFORMANCE", "MANAGEMENT_EXECUTION", "COMPETITIVE_INTELLIGENCE",
        "QUANTITATIVE_RESEARCH", "SCENARIOS_AND_SENSITIVITY", "EXECUTIVE_BRIEF"
    ]
    for rt in required_types:
        assert rt in REPORT_TYPES
        assert len(REPORT_TYPES[rt]["default_sections"]) > 0


def test_generate_comprehensive_report():
    """Generates a full comprehensive report and verifies all sections."""
    rep = generate_institutional_report(
        report_type="COMPREHENSIVE",
        period_cutoff="Q2FY27",
        author="Senior Equity Analyst"
    )
    assert rep["report_id"].startswith("REP-")
    assert rep["report_type"] == "COMPREHENSIVE"
    assert rep["verification_status"] in ["VERIFIED", "FLAGGED_WITH_WARNINGS"]
    assert len(rep["sections"]) >= 8
    
    # Check key sections are present
    sec_ids = [s["section_id"] for s in rep["sections"]]
    assert "cover" in sec_ids
    assert "exec_summary" in sec_ids
    assert "key_findings" in sec_ids
    assert "historical_financials" in sec_ids
    assert "management_credibility" in sec_ids
    assert "quantitative_research" in sec_ids
    assert "scenario_analysis" in sec_ids


def test_company_and_segment_report_generation():
    """Tests company-specific and segment-specific report generation."""
    # Eternal company report
    rep_et = generate_institutional_report(
        report_type="COMPANY_SPECIFIC",
        company="Eternal",
        period_cutoff="Q2FY27"
    )
    assert rep_et["company_filter"] == "Eternal"
    
    # Quick commerce segment report
    rep_qc = generate_institutional_report(
        report_type="BUSINESS_SEGMENT",
        segment="QuickCommerce",
        period_cutoff="Q2FY27"
    )
    assert rep_qc["segment_filter"] == "QuickCommerce"


def test_citation_verification_engine():
    """Validates that citation resolution verifies citations against real filings."""
    sample_cits = [
        {"company": "ETERNAL", "doc": "ETERNAL-Q2FY27", "page": "P13", "metric": "eternal_qcomm_nov"},
        {"company": "SWIGGY", "doc": "SWIGGY-Q2FY27", "page": "P07", "metric": "swiggy_gov_cr"}
    ]
    audit = verify_report_citations(sample_cits)
    assert audit["total_citations"] == 2
    assert audit["resolved_citations"] == 2
    assert audit["resolution_rate_pct"] == 100.0
    assert audit["status"] == "PASS"


def test_report_verification_scorecard():
    """Tests the automated report quality and integrity audit."""
    rep = generate_institutional_report(report_type="EXECUTIVE_BRIEF")
    scorecard = verify_complete_report(rep)
    assert "status" in scorecard
    assert scorecard["total_checks"] >= 4
    assert scorecard["checks_passed"] >= 3


def test_report_exports():
    """Tests HTML, PDF, DOCX, and CSV exports."""
    rep = generate_institutional_report(report_type="EXECUTIVE_BRIEF")
    export_dir = "data/reports/exports_test"
    os.makedirs(export_dir, exist_ok=True)
    
    # HTML Export
    html_path = os.path.join(export_dir, f"{rep['report_id']}.html")
    export_report_to_html(rep, html_path)
    assert os.path.exists(html_path)
    assert os.path.getsize(html_path) > 500
    
    # DOCX Export
    docx_path = os.path.join(export_dir, f"{rep['report_id']}.docx")
    export_report_to_docx(rep, docx_path)
    assert os.path.exists(docx_path)
    assert os.path.getsize(docx_path) > 500
    
    # CSV Export
    csv_path = os.path.join(export_dir, f"{rep['report_id']}.csv")
    export_report_to_csv(rep, csv_path)
    assert os.path.exists(csv_path)
    assert os.path.getsize(csv_path) > 100

    # PDF Export (conditional on Chrome availability)
    chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_bin):
        pdf_path = os.path.join(export_dir, f"{rep['report_id']}.pdf")
        export_report_to_pdf(rep, pdf_path)
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 1000


def test_api_report_endpoints():
    """Tests FastAPI REST endpoints for reports."""
    # 1. Types endpoint
    r_types = client.get("/api/v1/reports/types")
    assert r_types.status_code == 200
    assert len(r_types.json()["data"]) == 9
    
    # 2. Generate endpoint
    payload = {
        "report_type": "EXECUTIVE_BRIEF",
        "company": "Eternal",
        "period_cutoff": "Q2FY27",
        "author": "QA Auditor"
    }
    r_gen = client.post("/api/v1/reports/generate", json=payload)
    assert r_gen.status_code == 200
    rep_id = r_gen.json()["report_id"]
    assert rep_id.startswith("REP-")
    
    # 3. List endpoint
    r_list = client.get("/api/v1/reports/list")
    assert r_list.status_code == 200
    assert any(r["report_id"] == rep_id for r in r_list.json()["data"])
    
    # 4. Get by ID
    r_get = client.get(f"/api/v1/reports/{rep_id}")
    assert r_get.status_code == 200
    assert r_get.json()["data"]["report_id"] == rep_id
    
    # 5. Verify endpoint
    r_ver = client.post(f"/api/v1/reports/{rep_id}/verify")
    assert r_ver.status_code == 200
    assert "verification_status" in r_ver.json()
    
    # 6. Citations endpoint
    r_cit = client.get(f"/api/v1/reports/{rep_id}/citations")
    assert r_cit.status_code == 200
    assert "citation_verification" in r_cit.json()
    
    # 7. Export endpoint (HTML)
    r_exp = client.get(f"/api/v1/reports/{rep_id}/export/html")
    assert r_exp.status_code == 200
    assert "text/html" in r_exp.headers.get("content-type", "")
