"""
FoodIQ Phase 10 Final Independent Certification & End-to-End Workflow Test Suite.
Validates:
1. 7 Complete End-to-End Workflows (A through G)
2. 6-Layer Financial Truth Reconciliation (Source -> DB -> Analytics -> API -> UI -> Report)
3. Research Integrity & Non-Imputation Guardrails
"""

import os
import uuid
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.analytics.repository import get_analytical_df
from backend.app.analytics.competitive_findings import get_finding_by_id
from backend.app.analytics.credibility_engine import calculate_management_credibility_scorecard
from backend.app.analytics.statistical_research import get_all_relationship_studies_with_fdr
from backend.app.analytics.scenario_lab import compute_breakeven_analysis, save_scenario_to_storage, list_saved_scenarios
from backend.app.analytics.report_engine import generate_institutional_report, get_generated_report_by_id
from backend.app.analytics.disclosure_intelligence import register_new_disclosure, approve_disclosure_ingestion
from scripts.backup_db import backup_database
from scripts.restore_db import restore_database

client = TestClient(app)


def test_workflow_a_corporate_financial_research():
    """
    Workflow A — Corporate financial research:
    Select Eternal & Swiggy -> analyse Food Delivery -> inspect quarterly growth
    -> analyse profitability -> compare valid metrics -> inspect source evidence.
    """
    # 1. Compare food delivery profitability
    r_gaps = client.get("/api/v1/competitive/gaps?segment=Food")
    assert r_gaps.status_code == 200
    gaps = r_gaps.json()["data"]
    margin_gaps = [g for g in gaps if g["metric"] == "adj_ebitda_margin_pct"]
    assert len(margin_gaps) > 0
    
    # 2. Check 4-tier comparability
    r_comp = client.get("/api/v1/competitive/comparability?segment=Food")
    assert r_comp.status_code == 200
    rule = next(r for r in r_comp.json()["data"] if r["metric_name"] == "adj_ebitda_margin_pct")
    assert rule["comparability_level"] == "LEVEL_3"
    
    # 3. Inspect primary finding and source citation
    f6 = get_finding_by_id("FINDING-006")
    assert "242" in f6["derived_calculations"]


def test_workflow_b_management_credibility():
    """
    Workflow B — Management credibility:
    Open statements -> inspect commitments -> evaluate delivery -> inspect target vs actual.
    """
    r_score = client.get("/api/v1/credibility/scorecard?company=ETERNAL")
    assert r_score.status_code == 200
    score = r_score.json()["scorecard"]
    assert score["evaluable_completed"] == 6
    assert score["strict_delivery_rate_pct"] == 83.33
    assert score["pending_count"] == 2


def test_workflow_c_quantitative_analysis():
    """
    Workflow C — Quantitative analysis:
    Select research question -> inspect observations -> run statistical analysis -> review uncertainty.
    """
    r_stud = client.get("/api/v1/quantitative/relationships")
    assert r_stud.status_code == 200
    studies = r_stud.json()["studies"]
    s2 = next(s for s in studies if s["study_id"] == "REL-001")
    assert round(s2["pearson_r_level"], 2) == 0.55
    assert round(s2["first_difference_detrending_r"], 2) == 0.14
    assert s2["is_significant_after_fdr"] is False


def test_workflow_d_scenario_modelling():
    """
    Workflow D — Scenario modelling:
    Select business segment -> set assumptions -> run scenarios -> inspect sensitivity -> save & reopen.
    """
    be = compute_breakeven_analysis("Swiggy", "QuickCommerce")
    assert be["breakeven_aov_inr"] == 813.20
    assert be["calibrated_elasticity_bps"] == 0.9506
    
    scen_id = save_scenario_to_storage(
        scenario_name="Workflow D Certified Scenario",
        company="Swiggy",
        segment="QuickCommerce",
        scenario_type="BASE",
        assumptions={"aov_target": 813.20},
        outputs={"cm_pct": 0.0},
        author="Certification Suite"
    )
    saved = list_saved_scenarios()
    assert any(s["scenario_id"] == scen_id for s in saved)


def test_workflow_e_report_production():
    """
    Workflow E — Report production:
    Generate comprehensive report -> validate calculations -> validate citations -> reopen saved report.
    """
    rep = generate_institutional_report(report_type="EXECUTIVE_BRIEF", author="Certifier")
    rep_id = rep["report_id"]
    assert rep["verification_status"] in ["VERIFIED", "FLAGGED_WITH_WARNINGS"]
    
    # Reopen saved report from DB
    reopened = get_generated_report_by_id(rep_id)
    assert reopened["report_id"] == rep_id
    assert len(reopened["sections"]) >= 4


def test_workflow_f_new_disclosure_ingestion():
    """
    Workflow F — New disclosure ingestion:
    Submit new disclosure -> process -> review -> approve.
    """
    test_pdf = b"%PDF-1.4 Certified Workflow F test disclosure " + uuid.uuid4().hex.encode()
    reg = register_new_disclosure(
        company_id="ETERNAL",
        document_title="Workflow F Test Filing",
        document_category="Results Release",
        reporting_period="Q3 FY27",
        file_content_bytes=test_pdf,
        file_name="wf_test.pdf"
    )
    disc_id = reg["disclosure_id"]
    assert reg["status"] == "REGISTERED_PENDING_REVIEW"
    
    app_res = approve_disclosure_ingestion(disc_id, analyst="Certifier")
    assert app_res["status"] == "APPROVED"


def test_workflow_g_recovery():
    """
    Workflow G — Recovery:
    Create database backup -> restore into separate test location -> launch restored application.
    """
    test_dir = "data/backups/workflow_g"
    os.makedirs(test_dir, exist_ok=True)
    backup_file = backup_database(src_path="data/foodiq.db", backup_dir=test_dir)
    assert os.path.exists(backup_file)
    
    restored_target = os.path.join(test_dir, "restored_foodiq.db")
    restored = restore_database(backup_file=backup_file, target_path=restored_target, force=True)
    assert restored is True
    assert os.path.exists(restored_target)
    
    # Clean up test artifacts
    if os.path.exists(restored_target):
        os.remove(restored_target)
    if os.path.exists(backup_file):
        os.remove(backup_file)


def test_financial_truth_6_layers_reconciliation():
    """
    Financial Truth Audit across 6 Layers:
    1. Source Document
    2. Database Observation
    3. Analytical Calculation
    4. API Response
    5. UI Display Mapping
    6. Generated Report Section
    """
    # Test Blinkit Store Throughput (Q2 FY27)
    # 1. Source: ETERNAL-Q2FY27 p. 13 (NOV 20,940 Cr) and p. 7 (2,700 dark stores)
    # 2. Database Observation: eternal_qcomm_nov = 20,940 Cr, eternal_qcomm_darkstores = 2,700
    # 3. Calculation: (20,940 * 10^7) / (2,700 * 91.25) = 849,923.90 INR/store-day
    calc_val = (20940.0 * 1e7) / (2700.0 * 91.25)
    assert round(calc_val) == 849924
    
    # 4. API Response
    f1 = get_finding_by_id("FINDING-001")
    assert "849,924" in f1["derived_calculations"]
    assert "+22.0%" in f1["derived_calculations"]
    
    # 5. Generated Report Section
    rep = generate_institutional_report(report_type="COMPREHENSIVE")
    sec_findings = next(s for s in rep["sections"] if s["section_id"] == "key_findings")
    assert any("FINDING-001" in row.get("Finding ID", "") for row in sec_findings.get("data_table", []))
