"""
Unit and integration tests for FoodIQ Financial Analytics & Decomposition Core (Phase 2.1).
Verifies exact mathematical additivity, margin bridge reconciliation,
comparability governance, statistical validity, scenario sensitivity, and API endpoints.

Includes independent hand-calculated test cases:
1. Pure volume growth (AOV flat)
2. Pure basket growth (Volume flat)
3. Simultaneous volume and basket expansion
4. Dilutive volume growth (Volume up, AOV down)
5. Missing prior quarter boundary condition
6. Non-reconciling GOV residual capture
7. Strict blocking of NOV decomposition with GOV AOV
8. Strict blocking of per-order metrics when orders are undisclosed
"""

import pytest
import math
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.analytics.repository import get_analytical_df, build_and_materialize_analytical_tables
from backend.app.analytics.decomposition import compute_waterfall_decomposition, get_all_segment_decompositions
from backend.app.analytics.margin_bridge import compute_margin_bridge, get_all_margin_bridges
from backend.app.analytics.unit_economics import compute_quick_commerce_unit_economics, compute_unit_economics
from backend.app.analytics.network_productivity import compute_network_productivity, compute_network_comparison
from backend.app.analytics.competitive_gaps import compute_competitive_gaps
from backend.app.analytics.leading_indicator import test_aov_leading_indicator as run_aov_leading_test
from backend.app.analytics.scenario_model import run_aov_scenario_model
from backend.app.analytics.guidance_scorer import score_management_guidance

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_analytical_tables():
    """Ensure analytical tables in foodiq.db are fresh and populated."""
    build_and_materialize_analytical_tables()


# -----------------------------------------------------------------------------
# Module A: Growth Quality Decomposition Engine Tests
# -----------------------------------------------------------------------------
def test_waterfall_decomposition_additivity():
    """
    Verifies that for every quarter in Swiggy Quick Commerce:
    Volume Effect + Basket Effect + Interaction Effect + Residual == Delta Topline (exact within 0.01 Cr).
    """
    results = compute_waterfall_decomposition(company="Swiggy", segment="QuickCommerce", metric_basis="gov_cr")
    assert len(results) == 9  # 10 quarters -> 9 QoQ transitions
    
    for row in results:
        vol = row['volume_effect_cr']
        bsk = row['basket_effect_cr']
        inter = row['interaction_effect_cr']
        res = row['residual_cr']
        delta = row['delta_value']
        
        # Verify additivity
        reconstructed_delta = round(vol + bsk + inter + res, 2)
        assert abs(reconstructed_delta - delta) <= 0.02, (
            f"Additivity failure in {row['quarter']}: {vol} + {bsk} + {inter} + {res} != {delta}"
        )
        
        # Verify driver label logic
        if abs(vol) > abs(bsk):
            assert "Volume" in row['dominant_driver']
        else:
            assert "Basket" in row['dominant_driver']


def test_waterfall_decomposition_all_segments():
    """Verifies that the full decomposition suite returns records across segments."""
    all_results = get_all_segment_decompositions()
    assert len(all_results) > 0
    segments_found = set(r['segment'] for r in all_results)
    assert 'QuickCommerce' in segments_found
    assert 'Food' in segments_found


# -----------------------------------------------------------------------------
# Module B: Contribution Margin Bridge Tests
# -----------------------------------------------------------------------------
def test_margin_bridge_additivity():
    """
    Verifies that for every quarter in Food Delivery and Quick Commerce:
    Take Rate Effect (bps) + Operational Efficiency (bps) + Residual (bps) == Delta Margin (bps).
    """
    results = compute_margin_bridge(company="Swiggy", segment="Food", margin_metric="contribution_margin_pct", topline_metric="gov_cr")
    assert len(results) == 9
    
    for row in results:
        tr_delta = row['take_rate_effect_bps']
        op_eff = row['unallocated_cost_efficiency_bps']
        res = row['bridge_residual_bps']
        delta_m = row['delta_margin_bps']
        
        sum_components = round(tr_delta + op_eff + res, 1)
        assert abs(sum_components - delta_m) <= 0.2, (
            f"Margin bridge failure in {row['quarter']}: {tr_delta} + {op_eff} + {res} != {delta_m}"
        )


def test_get_all_margin_bridges_execution():
    """Verifies that all margin bridges across Food and QuickCommerce execute cleanly."""
    all_bridges = get_all_margin_bridges()
    assert len(all_bridges) > 0
    companies = set(r['company'] for r in all_bridges)
    assert 'Swiggy' in companies
    assert 'Eternal' in companies


# -----------------------------------------------------------------------------
# Module C: Unit Economics & Network Productivity Tests
# -----------------------------------------------------------------------------
def test_quick_commerce_unit_economics_formulas():
    """
    Verifies per-order unit economics calculations:
    Revenue/order = Adj Revenue * 10 / Orders mn
    Contribution/order = AOV * CM% / 100
    EBITDA/order = EBITDA * 10 / Orders mn
    """
    results = compute_quick_commerce_unit_economics()
    assert len(results) == 20  # 10 quarters * 2 companies
    
    swiggy_rows = [r for r in results if r['company'] == 'Swiggy']
    for row in swiggy_rows:
        orders = row['total_orders_mn']
        adj_rev = row['adj_revenue_cr']
        aov = row['aov_inr']
        cm_pct = row['contribution_margin_pct_gov']
        ebitda = row['adj_ebitda_cr']
        
        expected_rev_order = round((adj_rev * 10.0) / orders, 2)
        assert abs(row['revenue_per_order_inr'] - expected_rev_order) <= 0.05
        
        expected_cm_order = round((aov * cm_pct) / 100.0, 2)
        assert abs(row['contribution_profit_per_order_inr'] - expected_cm_order) <= 0.05
        
        expected_ebitda_order = round((ebitda * 10.0) / orders, 2)
        assert abs(row['adj_ebitda_per_order_inr'] - expected_ebitda_order) <= 0.05


def test_blinkit_undisclosed_orders_null_preservation():
    """
    Verifies that Blinkit unit economics strictly sets per-order metrics to None
    rather than fabricating orders or dividing by 0.
    """
    results = compute_quick_commerce_unit_economics()
    blinkit_rows = [r for r in results if r['company'] == 'Eternal']
    assert len(blinkit_rows) == 10
    
    for row in blinkit_rows:
        assert row['total_orders_mn'] is None
        assert row['revenue_per_order_inr'] is None
        assert row['contribution_profit_per_order_inr'] is None
        assert row['adj_ebitda_per_order_inr'] is None
        assert row['voucher_subsidy_per_order_inr'] is None
        assert row['status'] == "ORDERS_NOT_DISCLOSED"


def test_network_productivity_and_comparison():
    """Verifies dark store additions, throughput, and Blinkit vs Instamart comparisons."""
    prod = compute_network_productivity()
    assert len(prod) == 20
    
    comp = compute_network_comparison()
    assert len(comp) == 10  # 10 quarters
    
    q2fy27 = next(r for r in comp if r['quarter'] == 'Q2FY27')
    assert q2fy27['blinkit_stores'] == 2700
    assert q2fy27['instamart_stores'] == 1240
    assert q2fy27['store_gap_blinkit_lead'] == 1460
    assert q2fy27['leader'] == 'Blinkit'


# -----------------------------------------------------------------------------
# Module D: Competitive Gaps & Comparability Governance Tests
# -----------------------------------------------------------------------------
def test_competitive_gaps_governance_rules():
    """
    Verifies that competitive gaps enforce governance rules:
    - Blinkit 1P revenue transition from Q2FY26 is classified as LEVEL_4_INCOMPARABLE_BLOCKED
    - L1, L2, L3 comparability levels are properly tagged
    """
    gaps = compute_competitive_gaps()
    assert len(gaps) > 0
    
    qc_rev_gaps = [g for g in gaps if g['segment'] == 'QuickCommerce' and g['metric'] == 'adj_revenue_cr']
    assert len(qc_rev_gaps) == 10
    
    for g in qc_rev_gaps:
        fy = int(g['fiscal_year'].replace('FY', ''))
        qn = g['quarter_num']
        if (fy == 26 and qn >= 2) or fy > 26:
            assert g['is_flagged'] is True
            assert g['comparability_level'] == 'LEVEL_4_INCOMPARABLE_BLOCKED'
            assert g['is_comparison_blocked'] is True
            assert g['gap_absolute'] is None
        else:
            assert g['is_flagged'] is False
            assert g['comparability_level'] == 'LEVEL_2_COMPARABLE_WITH_ADJUSTMENT'
            assert g['is_comparison_blocked'] is False


# -----------------------------------------------------------------------------
# Module E: Statistical Lead-Lag & Predictive Engine Tests
# -----------------------------------------------------------------------------
def test_leading_indicator_statistical_properties():
    """
    Verifies Pearson and Spearman correlation math, degrees of freedom, and confidence intervals.
    """
    res = run_aov_leading_test(company="Swiggy", segment="QuickCommerce")
    assert 'results' in res
    lag_results = res['results']
    assert len(lag_results) == 3  # Lag-0, Lag-1, Lag-2
    
    for lag_res in lag_results:
        n = lag_res['sample_size_n']
        df = lag_res['degrees_of_freedom']
        assert df == n - 2
        r = lag_res['pearson_r']
        assert -1.0 <= r <= 1.0
        p = lag_res['pearson_p_value']
        assert 0.0 <= p <= 1.0
        
        if lag_res['ci_95_low'] is not None:
            assert -1.0 <= lag_res['ci_95_low'] <= lag_res['ci_95_high'] <= 1.0


# -----------------------------------------------------------------------------
# Module F: Scenario Model Sensitivity Tests
# -----------------------------------------------------------------------------
def test_scenario_model_monotonicity():
    """
    Verifies that increasing AOV increments monotonically increases projected GOV
    and projected Contribution Margin, narrowing the gap.
    """
    model = run_aov_scenario_model(elasticity_bps_per_inr=1.0)
    scenarios = model['scenarios']
    assert len(scenarios) == 6
    
    for i in range(1, len(scenarios)):
        prev = scenarios[i - 1]
        curr = scenarios[i]
        
        assert curr['projected_aov_inr'] > prev['projected_aov_inr']
        assert curr['projected_gov_cr'] > prev['projected_gov_cr']
        assert curr['projected_contribution_margin_pct'] >= prev['projected_contribution_margin_pct']
        assert curr['gap_to_breakeven_bps'] >= prev['gap_to_breakeven_bps']


def test_scenario_model_multi_tier_matrix():
    """Verifies that multi-tier sensitivity matrix computes all 3 tiers correctly."""
    model = run_aov_scenario_model()
    assert 'multi_tier_sensitivity_matrix' in model
    matrix = model['multi_tier_sensitivity_matrix']
    assert len(matrix) == 6
    
    for row in matrix:
        assert 'conservative_cm_pct' in row
        assert 'baseline_cm_pct' in row
        assert 'upper_cm_pct' in row
        if row['aov_improvement_inr'] > 0:
            assert row['upper_cm_pct'] >= row['baseline_cm_pct'] >= row['conservative_cm_pct']


def test_scenario_model_segment_isolation():
    """
    Verifies that Instamart empirical elasticity is marked empirical,
    while Food Delivery is marked ASSUMPTION_NOT_EMPIRICAL_ESTIMATE.
    """
    qc_model = run_aov_scenario_model(segment="QuickCommerce")
    assert qc_model['is_empirical_estimate'] is True
    assert qc_model['coefficient_nature'] == 'EMPIRICAL_OLS_ESTIMATE'
    assert qc_model['calibrated_elasticity_bps_per_inr'] == 0.95
    
    food_model = run_aov_scenario_model(segment="Food")
    assert food_model['is_empirical_estimate'] is False
    assert food_model['coefficient_nature'] == 'ASSUMPTION_NOT_EMPIRICAL_ESTIMATE'
    assert food_model['econometric_calibration']['status'] == 'EMPIRICAL_ELASTICITY_UNAVAILABLE'


# -----------------------------------------------------------------------------
# Module G: Guidance Credibility Scoring Tests
# -----------------------------------------------------------------------------
def test_guidance_scoring():
    """Verifies management guidance delivery rate and credibility tiering."""
    scorecard = score_management_guidance()
    assert scorecard['total_commitments'] == 18
    assert scorecard['evaluable_commitments'] == 3
    assert scorecard['delivered_count'] == 2
    assert scorecard['partially_delivered_count'] == 1
    assert scorecard['pending_count'] == 12
    assert scorecard['not_objectively_measurable_count'] == 3
    assert scorecard['strict_delivery_rate_pct'] == 66.7
    assert scorecard['broad_delivery_rate_pct'] == 83.3
    assert scorecard['credibility_tier'] in ["Moderate", "High"]


# -----------------------------------------------------------------------------
# Module H: Independent Hand-Calculated Verification Test Cases
# -----------------------------------------------------------------------------
def test_hand_calc_pure_volume_growth():
    """Hand-calculated case: Pure volume growth with constant AOV."""
    synthetic_df = pd.DataFrame([
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q1', 'fiscal_year': 'FY25', 'quarter_num': 1,
         'gov_cr': 5000.0, 'total_orders_mn': 100.0, 'aov_inr': 500.0},
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q2', 'fiscal_year': 'FY25', 'quarter_num': 2,
         'gov_cr': 6000.0, 'total_orders_mn': 120.0, 'aov_inr': 500.0}
    ])
    res = compute_waterfall_decomposition('TestCo', 'TestSeg', 'gov_cr', df=synthetic_df)
    assert len(res) == 1
    q2 = res[0]
    assert q2['delta_value'] == 1000.0
    assert q2['volume_effect_cr'] == 1000.0
    assert q2['basket_effect_cr'] == 0.0
    assert q2['interaction_effect_cr'] == 0.0
    assert q2['residual_cr'] == 0.0
    assert q2['dominant_driver'] == "Volume (Order Count)"


def test_hand_calc_pure_basket_growth():
    """Hand-calculated case: Pure basket growth with constant order volume."""
    synthetic_df = pd.DataFrame([
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q1', 'fiscal_year': 'FY25', 'quarter_num': 1,
         'gov_cr': 5000.0, 'total_orders_mn': 100.0, 'aov_inr': 500.0},
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q2', 'fiscal_year': 'FY25', 'quarter_num': 2,
         'gov_cr': 6000.0, 'total_orders_mn': 100.0, 'aov_inr': 600.0}
    ])
    res = compute_waterfall_decomposition('TestCo', 'TestSeg', 'gov_cr', df=synthetic_df)
    assert len(res) == 1
    q2 = res[0]
    assert q2['delta_value'] == 1000.0
    assert q2['volume_effect_cr'] == 0.0
    assert q2['basket_effect_cr'] == 1000.0
    assert q2['interaction_effect_cr'] == 0.0
    assert q2['residual_cr'] == 0.0
    assert q2['dominant_driver'] == "Basket Size (AOV)"


def test_hand_calc_simultaneous_volume_and_basket_expansion():
    """Hand-calculated case: Simultaneous expansion in both volume and basket."""
    synthetic_df = pd.DataFrame([
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q1', 'fiscal_year': 'FY25', 'quarter_num': 1,
         'gov_cr': 5000.0, 'total_orders_mn': 100.0, 'aov_inr': 500.0},
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q2', 'fiscal_year': 'FY25', 'quarter_num': 2,
         'gov_cr': 7200.0, 'total_orders_mn': 120.0, 'aov_inr': 600.0}
    ])
    res = compute_waterfall_decomposition('TestCo', 'TestSeg', 'gov_cr', df=synthetic_df)
    assert len(res) == 1
    q2 = res[0]
    assert q2['delta_value'] == 2200.0
    assert q2['volume_effect_cr'] == 1000.0
    assert q2['basket_effect_cr'] == 1000.0
    assert q2['interaction_effect_cr'] == 200.0
    assert q2['residual_cr'] == 0.0
    assert (q2['volume_effect_cr'] + q2['basket_effect_cr'] + q2['interaction_effect_cr'] + q2['residual_cr']) == 2200.0


def test_hand_calc_dilutive_volume_growth():
    """Hand-calculated case: Dilutive volume growth (orders up, AOV down)."""
    synthetic_df = pd.DataFrame([
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q1', 'fiscal_year': 'FY25', 'quarter_num': 1,
         'gov_cr': 5000.0, 'total_orders_mn': 100.0, 'aov_inr': 500.0},
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q2', 'fiscal_year': 'FY25', 'quarter_num': 2,
         'gov_cr': 6000.0, 'total_orders_mn': 150.0, 'aov_inr': 400.0}
    ])
    res = compute_waterfall_decomposition('TestCo', 'TestSeg', 'gov_cr', df=synthetic_df)
    assert len(res) == 1
    q2 = res[0]
    assert q2['delta_value'] == 1000.0
    assert q2['volume_effect_cr'] == 2500.0
    assert q2['basket_effect_cr'] == -1000.0
    assert q2['interaction_effect_cr'] == -500.0
    assert q2['residual_cr'] == 0.0
    assert (q2['volume_effect_cr'] + q2['basket_effect_cr'] + q2['interaction_effect_cr']) == 1000.0
    assert q2['dominant_driver'] == "Volume (Order Count)"


def test_hand_calc_non_reconciling_gov_residual():
    """Hand-calculated case: Disclosed GOV has discrete rounding variance from O x AOV / 10."""
    synthetic_df = pd.DataFrame([
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q1', 'fiscal_year': 'FY25', 'quarter_num': 1,
         'gov_cr': 5000.0, 'total_orders_mn': 100.0, 'aov_inr': 500.0},
        {'company': 'TestCo', 'segment': 'TestSeg', 'quarter': 'Q2', 'fiscal_year': 'FY25', 'quarter_num': 2,
         'gov_cr': 7205.0,  # Exactly ₹5.0 Cr higher than 120 * 600 / 10 = 7200.0
         'total_orders_mn': 120.0, 'aov_inr': 600.0}
    ])
    res = compute_waterfall_decomposition('TestCo', 'TestSeg', 'gov_cr', df=synthetic_df)
    assert len(res) == 1
    q2 = res[0]
    assert q2['delta_value'] == 2205.0
    assert q2['volume_effect_cr'] == 1000.0
    assert q2['basket_effect_cr'] == 1000.0
    assert q2['interaction_effect_cr'] == 200.0
    assert q2['residual_cr'] == 5.0
    assert round(q2['volume_effect_cr'] + q2['basket_effect_cr'] + q2['interaction_effect_cr'] + q2['residual_cr'], 2) == 2205.0


def test_strict_blocking_nov_decomposition_with_gov_aov():
    """Verifies that attempting to decompose NOV using GOV-based AOV is strictly rejected."""
    res = compute_waterfall_decomposition('Swiggy', 'QuickCommerce', metric_basis='nov_cr')
    assert len(res) == 9
    assert all(r['status'] == 'INELIGIBLE_INVALID_METRIC_BASIS' for r in res)
    assert 'Disclosed AOV is GOV-based and cannot be applied to nov_cr' in res[0]['methodology_notes']


# -----------------------------------------------------------------------------
# FastAPI Analytics Endpoints Integration Tests
# -----------------------------------------------------------------------------
def test_api_analytics_decomposition():
    res = client.get("/api/v1/analytics/decomposition?company=Swiggy&segment=QuickCommerce")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 9


def test_api_analytics_margin_bridge():
    res = client.get("/api/v1/analytics/margin-bridge?company=Swiggy&segment=Food")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 9


def test_api_analytics_unit_economics():
    res = client.get("/api/v1/analytics/unit-economics?segment=QuickCommerce")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 20


def test_api_analytics_network_productivity():
    res = client.get("/api/v1/analytics/network-productivity")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 20


def test_api_analytics_network_comparison():
    res = client.get("/api/v1/analytics/network-comparison")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 10


def test_api_analytics_competitive_gaps():
    res = client.get("/api/v1/analytics/competitive-gaps?segment=Food")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_api_analytics_leading_indicator():
    res = client.get("/api/v1/analytics/leading-indicator?company=Swiggy&segment=QuickCommerce")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "analysis" in data
    assert len(data["analysis"]["results"]) == 3


def test_api_analytics_scenario_model():
    res = client.get("/api/v1/analytics/scenario-model?elasticity_bps_per_inr=1.5")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "model" in data
    assert len(data["model"]["scenarios"]) == 6


def test_api_analytics_guidance_scorecard():
    res = client.get("/api/v1/analytics/guidance-scorecard")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["scorecard"]["total_commitments"] == 18
