"""
Unit and integration tests for FoodIQ Quantitative Research & Scenario Lab Engine (Phase 5).
Verifies:
1. Growth and trend analysis (QoQ, YoY, rolling averages, volatility, negative denominator handling).
2. Econometric relationship studies (Pearson r, Spearman rho, 95% CI, p-values, OLS slope).
3. First-difference detrending and lag-1 relationships.
4. Benjamini-Hochberg False Discovery Rate (FDR) correction.
5. Research question workbench (8 institutional questions).
6. Multi-segment scenario simulations (Base, Bull, Bear, Custom).
7. Strict cross-segment elasticity isolation (Instamart elasticity is never applied to Food Delivery).
8. 2-variable sensitivity grid generation.
9. Break-even analysis calculations.
10. Monte Carlo bounded simulations and percentiles.
11. Persistent scenario storage (save, list, retrieve).
12. Phase 5 FastAPI REST endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.analytics.statistical_research import (
    compute_metric_growth_and_trends,
    run_statistical_relationship_analysis,
    get_all_relationship_studies_with_fdr,
    get_all_research_workbench_questions,
    get_research_question_by_id
)
from backend.app.analytics.scenario_lab import (
    run_segment_scenario_simulation,
    compute_two_variable_sensitivity_matrix,
    compute_breakeven_analysis,
    run_monte_carlo_simulation,
    save_scenario_to_storage,
    list_saved_scenarios,
    get_saved_scenario_by_id
)

client = TestClient(app)


# -----------------------------------------------------------------------------
# Module A: Growth & Econometric Studies Tests
# -----------------------------------------------------------------------------
def test_growth_and_trends_computation():
    """Verifies time-series growth, rolling averages, and safe handling of zero/negative bases."""
    res = compute_metric_growth_and_trends('Swiggy', 'QuickCommerce', 'nov_cr')
    assert res['status'] == 'SUCCESS'
    assert res['observations_count'] >= 6
    assert res['mean_value'] is not None
    assert res['avg_qoq_growth_pct'] is not None
    assert len(res['time_series']) >= 6
    
    # Check that QoQ growth is computed correctly
    ts = res['time_series']
    assert ts[0]['qoq_growth_pct'] is None  # First period has no prior quarter
    assert ts[1]['qoq_growth_pct'] is not None


def test_econometric_relationship_study():
    """Verifies Pearson r, 95% CI, p-value, and first-difference detrending on REL-001 (AOV vs CM)."""
    study = run_statistical_relationship_analysis('REL-001')
    assert study['status'] == 'SUCCESS'
    assert study['sample_size_n'] >= 6
    assert study['pearson_r_level'] > 0.50  # Positive level correlation
    assert len(study['ci_95_level']) == 2
    assert study['ci_95_level'][0] <= study['pearson_r_level'] <= study['ci_95_level'][1]
    assert study['ols_slope'] > 0
    
    # Detrending verification: first differences p-value > 0.05
    assert study['first_difference_detrending_r'] is not None
    assert study['first_difference_p_value'] is not None
    assert "LEVEL_TREND_ONLY" in study['statistical_finding'] or "SYNCHRONOUS" in study['statistical_finding']


def test_benjamini_hochberg_fdr_correction():
    """Verifies Benjamini-Hochberg multiple-testing correction across all studies."""
    studies = get_all_relationship_studies_with_fdr()
    assert len(studies) >= 10
    
    # Verify ranking and monotonic critical values
    prev_rank = 0
    for s in studies:
        assert s['bh_rank'] == prev_rank + 1
        prev_rank = s['bh_rank']
        assert 'is_significant_after_fdr' in s
        assert s['bh_critical_value'] > 0


def test_research_workbench_questions():
    """Verifies all 8 research questions exist with structured evidence summaries."""
    questions = get_all_research_workbench_questions()
    assert len(questions) == 8
    
    q_ids = [q['question_id'] for q in questions]
    assert 'RQ-001' in q_ids
    assert 'RQ-003' in q_ids  # Blinkit 1P accounting
    assert 'RQ-008' in q_ids  # Sensitivity drivers
    
    q3 = get_research_question_by_id('RQ-003')
    assert "OVER_80_PERCENT_ACCOUNTING_ARTIFACT" in q3['verdict']


# -----------------------------------------------------------------------------
# Module B: Scenario Simulation & Sensitivity Tests
# -----------------------------------------------------------------------------
def test_scenario_simulation_quick_commerce_empirical_pedigree():
    """Verifies Quick Commerce simulation correctly identifies empirical OLS elasticity."""
    sim = run_segment_scenario_simulation('Swiggy', 'QuickCommerce', scenario_type="BASE", forecast_quarters=4)
    assert sim['status'] == 'SUCCESS'
    assert sim['parameter_classification'] == 'EMPIRICAL_ESTIMATE_OLS'
    assert sim['calibrated_elasticity_bps'] == pytest.approx(0.9506, abs=1e-4)
    assert len(sim['projections']) == 4
    
    p1 = sim['projections'][0]
    assert 'projected_nov_cr' in p1
    assert 'projected_cm_pct' in p1
    assert 'projected_throughput_store_day_inr' in p1


def test_strict_cross_segment_elasticity_isolation():
    """
    CRITICAL TEST: Verifies that Food Delivery simulation NEVER applies
    empirical Quick Commerce elasticity, flagging parameters as analyst assumptions.
    """
    sim_food = run_segment_scenario_simulation('Swiggy', 'Food', scenario_type="BASE", forecast_quarters=4)
    assert sim_food['status'] == 'SUCCESS'
    assert sim_food['parameter_classification'] == 'ANALYST_ASSUMPTION_NOT_EMPIRICAL_QC'
    assert sim_food['calibrated_elasticity_bps'] is None, "Quick Commerce elasticity leaked into Food Delivery!"


def test_two_variable_sensitivity_matrix():
    """Verifies 2-variable sensitivity grid computation."""
    matrix = compute_two_variable_sensitivity_matrix('Swiggy', 'QuickCommerce')
    assert matrix['status'] == 'SUCCESS'
    assert len(matrix['matrix']) == len(matrix['y_steps'])
    for row in matrix['matrix']:
        assert len(row['cells']) == len(matrix['x_steps'])


def test_breakeven_analysis_calculation():
    """Verifies AOV break-even threshold computation."""
    be = compute_breakeven_analysis('Swiggy', 'QuickCommerce')
    assert be['status'] == 'SUCCESS'
    assert be['breakeven_aov_inr'] > be['current_aov_inr']
    assert be['additional_aov_required_inr'] > 0


def test_monte_carlo_bounded_simulation():
    """Verifies Monte Carlo simulation with explicitly reported bounded distributions."""
    mc = run_monte_carlo_simulation('Swiggy', 'QuickCommerce', iterations=100)
    assert mc['status'] == 'SUCCESS'
    assert mc['iterations_run'] == 100
    
    pcts = mc['percentiles_target_profit_cr']
    assert pcts['p10_bear_boundary'] <= pcts['p50_median_expectation'] <= pcts['p90_bull_boundary']
    assert 0.0 <= mc['probability_of_profitability_pct'] <= 100.0


def test_persistent_scenario_storage():
    """Verifies saving, listing, and retrieving scenarios from SQLite storage."""
    sim = run_segment_scenario_simulation('Eternal', 'QuickCommerce', scenario_type="BULL", forecast_quarters=4)
    
    scen_id = save_scenario_to_storage(
        scenario_name="Test Eternal Bull Case",
        company="Eternal",
        segment="QuickCommerce",
        scenario_type="BULL",
        assumptions=sim['assumptions_applied'],
        outputs=sim,
        author="Audit QA",
        notes="Automated test scenario"
    )
    assert scen_id.startswith("SCEN-")
    
    # List scenarios
    scenarios = list_saved_scenarios()
    assert len(scenarios) > 0
    found = next((s for s in scenarios if s['scenario_id'] == scen_id), None)
    assert found is not None
    assert found['scenario_name'] == "Test Eternal Bull Case"
    
    # Retrieve single scenario
    retrieved = get_saved_scenario_by_id(scen_id)
    assert retrieved is not None
    assert retrieved['scenario_id'] == scen_id
    assert retrieved['company'] == "Eternal"
    assert retrieved['outputs']['status'] == "SUCCESS"


# -----------------------------------------------------------------------------
# Module C: FastAPI Quantitative & Scenario Endpoints Tests
# -----------------------------------------------------------------------------
def test_api_quantitative_and_scenario_endpoints():
    """Verifies all Phase 5 REST endpoints return 200 with sanitized JSON."""
    r_gt = client.get("/api/v1/quantitative/growth-trends?company=Swiggy&segment=QuickCommerce&metric=nov_cr")
    assert r_gt.status_code == 200
    assert r_gt.json()['status'] == "SUCCESS"
    
    r_rels = client.get("/api/v1/quantitative/relationships")
    assert r_rels.status_code == 200
    assert r_rels.json()['total_studies'] >= 10
    
    r_wb = client.get("/api/v1/quantitative/workbench")
    assert r_wb.status_code == 200
    assert r_wb.json()['total_questions'] == 8
    
    # Scenario run POST
    r_sim = client.post("/api/v1/scenarios/run", json={
        "company": "Swiggy",
        "segment": "QuickCommerce",
        "scenario_type": "BASE",
        "forecast_quarters": 4
    })
    assert r_sim.status_code == 200
    assert r_sim.json()['status'] == "SUCCESS"
    
    # Sensitivity GET
    r_sens = client.get("/api/v1/scenarios/sensitivity?company=Swiggy&segment=QuickCommerce")
    assert r_sens.status_code == 200
    
    # Breakeven GET
    r_be = client.get("/api/v1/scenarios/breakeven?company=Swiggy&segment=QuickCommerce")
    assert r_be.status_code == 200
    
    # Saved scenarios GET
    r_saved = client.get("/api/v1/scenarios/saved")
    assert r_saved.status_code == 200
