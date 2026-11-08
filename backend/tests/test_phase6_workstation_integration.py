"""
Unit and integration tests for FoodIQ Institutional Research Workstation & End-to-End Workflows (Phase 6).
Verifies:
1. Workstation static assets delivery (index.html, style.css, app.js).
2. All 10 workspace tabs present and accessible in the workstation shell.
3. End-to-End Workflow A: Competitive Research Journey.
4. End-to-End Workflow B: Management Execution & Credibility Journey.
5. End-to-End Workflow C: Quantitative Research & Econometrics Journey.
6. End-to-End Workflow D: Scenario Analysis, Breakeven & Storage Journey.
7. End-to-End Workflow E: Source Document & Page Citation Journey.
"""

import pytest
import os
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


# -----------------------------------------------------------------------------
# Module A: Workstation Assets & Shell Delivery Tests
# -----------------------------------------------------------------------------
def test_workstation_root_serves_html():
    """Verifies that accessing root '/' serves the complete FoodIQ workstation HTML."""
    r = client.get("/")
    assert r.status_code == 200
    assert "Food<span class=\"highlight\">IQ</span>" in r.text or "FoodIQ" in r.text
    assert "TERMINAL v3.1" in r.text


def test_workstation_static_assets():
    """Verifies that static assets (style.css, app.js) are properly mounted and served."""
    r_css = client.get("/static/style.css")
    assert r_css.status_code == 200
    assert "--bg-core" in r_css.text
    
    r_js = client.get("/static/app.js")
    assert r_js.status_code == 200
    assert "class FoodIQApp" in r_js.text


def test_all_10_workspace_panes_present():
    """Verifies that all 10 required workspace panes exist in the HTML shell."""
    r = client.get("/")
    assert r.status_code == 200
    html = r.text
    
    expected_panes = [
        "tab-overview",
        "tab-company",
        "tab-financials",
        "tab-competitive",
        "tab-credibility",
        "tab-quantitative",
        "tab-scenarios",
        "tab-library",
        "tab-sources",
        "tab-governance"
    ]
    for pane in expected_panes:
        assert f'id="{pane}"' in html, f"Pane {pane} missing from workstation shell!"


# -----------------------------------------------------------------------------
# Module B: 5 End-to-End Acceptance Workflows Tests
# -----------------------------------------------------------------------------
def test_e2e_workflow_a_competitive_research():
    """
    Workflow A — Competitive research:
    Select Eternal & Swiggy -> select Food Delivery -> inspect historical profitability
    -> examine monetisation -> inspect comparability -> open supporting evidence.
    """
    # 1. Inspect competitive gaps for Food Delivery
    r_gaps = client.get("/api/v1/competitive/gaps")
    assert r_gaps.status_code == 200
    gaps = r_gaps.json()['gaps']
    food_ebitda_gaps = [g for g in gaps if g['segment'] == 'Food' and g['metric'] == 'adj_ebitda_margin_pct']
    assert len(food_ebitda_gaps) > 0
    
    # 2. Inspect comparability rule for Food EBITDA margin (Level 3 Directional)
    r_comp = client.get("/api/v1/competitive/comparability")
    assert r_comp.status_code == 200
    rules = r_comp.json()['rules']
    rule_ebitda = next(r for r in rules if r['metric_name'] == 'adj_ebitda_margin_pct')
    assert rule_ebitda['comparability_level'] == 'LEVEL_3'
    
    # 3. Retrieve verified research finding 6 (Profitability gap trajectory)
    r_f6 = client.get("/api/v1/competitive/findings/FINDING-006")
    assert r_f6.status_code == 200
    assert "242" in r_f6.json()['finding']['derived_calculations']


def test_e2e_workflow_b_management_execution():
    """
    Workflow B — Management execution:
    Select company -> open management credibility -> inspect commitment
    -> compare target with actual -> inspect original statement.
    """
    # 1. Retrieve commitments for Eternal
    r_comms = client.get("/api/v1/credibility/commitments?company=Eternal")
    assert r_comms.status_code == 200
    comms = r_comms.json()['commitments']
    assert len(comms) >= 6
    
    # 2. Inspect Blinkit 1,000 dark store target
    comm_1 = next(c for c in comms if c['commitment_id'] == 'COMM-ET-001')
    assert comm_1['target_value'] == 1000.0
    assert comm_1['actual_value_reported'] == 1300.0
    assert comm_1['outcome_status'] == 'DELIVERED'
    
    # 3. Verify execution scorecard
    r_sc = client.get("/api/v1/credibility/scorecard?company=Eternal")
    assert r_sc.status_code == 200
    assert r_sc.json()['scorecard']['strict_delivery_rate_pct'] == 83.33


def test_e2e_workflow_c_quantitative_research():
    """
    Workflow C — Quantitative research:
    Select metric relationship -> inspect observations -> run statistical analysis
    -> inspect uncertainty / FDR -> inspect research question.
    """
    # 1. Run study REL-001 (AOV vs CM for Instamart)
    r_study = client.get("/api/v1/quantitative/relationships/REL-001")
    assert r_study.status_code == 200
    st = r_study.json()
    assert st['pearson_r_level'] > 0.50
    assert st['first_difference_detrending_r'] is not None
    assert st['first_difference_p_value'] > 0.05  # Rejects naive instantaneous causation
    
    # 2. Retrieve research question workbench item
    r_q = client.get("/api/v1/quantitative/workbench/RQ-005")
    assert r_q.status_code == 200
    assert "CONFIRMED_ON_LEVELS" in r_q.json()['question']['verdict']


def test_e2e_workflow_d_scenario_analysis():
    """
    Workflow D — Scenario analysis:
    Select company and segment -> set assumptions -> run base/bull case
    -> inspect outputs -> inspect breakeven -> save and reopen scenario.
    """
    # 1. Run simulation
    r_run = client.post("/api/v1/scenarios/run", json={
        "company": "Swiggy",
        "segment": "QuickCommerce",
        "scenario_type": "BULL",
        "forecast_quarters": 4,
        "custom_assumptions": {"nov_growth_rate_pct": 30.0, "aov_change_inr": 40.0}
    })
    assert r_run.status_code == 200
    sim_data = r_run.json()
    assert len(sim_data['projections']) == 4
    
    # 2. Inspect breakeven threshold
    r_be = client.get("/api/v1/scenarios/breakeven?company=Swiggy&segment=QuickCommerce")
    assert r_be.status_code == 200
    assert r_be.json()['breakeven_aov_inr'] > 708.0
    
    # 3. Save scenario
    r_save = client.post("/api/v1/scenarios/save", json={
        "scenario_name": "E2E Test Bull Scenario",
        "company": "Swiggy",
        "segment": "QuickCommerce",
        "scenario_type": "BULL",
        "assumptions": {"nov_growth_rate_pct": 30.0},
        "outputs": sim_data,
        "author": "E2E Test Runner"
    })
    assert r_save.status_code == 200
    scen_id = r_save.json()['scenario_id']
    
    # 4. Reopen saved scenario
    r_reopen = client.get(f"/api/v1/scenarios/saved/{scen_id}")
    assert r_reopen.status_code == 200
    assert r_reopen.json()['scenario']['scenario_name'] == "E2E Test Bull Scenario"


def test_e2e_workflow_e_source_verification():
    """
    Workflow E — Source verification:
    Open research finding -> inspect calculations -> navigate to source document and physical page.
    """
    # 1. Open Finding 1
    r_f1 = client.get("/api/v1/competitive/findings/FINDING-001")
    assert r_f1.status_code == 200
    f1 = r_f1.json()['finding']
    assert "849,924" in f1['derived_calculations'] or "+22.0%" in f1['derived_calculations']
    
    # 2. Navigate to source documents catalog
    r_docs = client.get("/api/v1/documents")
    assert r_docs.status_code == 200
    docs = r_docs.json()
    assert len(docs) >= 6
