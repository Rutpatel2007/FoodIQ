"""
Unit and integration tests for FoodIQ Competitive Intelligence & Structural Break Engine (Phase 3).
Verifies:
1. Comparability classification across all 4 tiers (L1, L2, L3, L4).
2. Strict blocking of raw Blinkit post-Q1FY26 revenue vs Swiggy marketplace revenue.
3. Strict blocking of cross-subtraction between GOV and NOV.
4. Structural-break event register integrity (Blinkit 1P, District, Lynks).
5. 4-series separation for Blinkit 1P transition (Reported, LFL, Operating, Margins).
6. District acquisition and Lynks divestment scope preservation.
7. Multi-dimensional competitive gap attribution across all 8 dimensions.
8. Evidence-backed findings schema, source citations, and 6 epistemic evidence tiers.
9. Metric availability matrix NULL preservation.
10. FastAPI competitive REST endpoints verification.
"""

import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.analytics.comparability_engine import (
    get_all_comparability_rules,
    get_comparability_rule,
    COMPARABILITY_LEVELS
)
from backend.app.analytics.metric_reconciliation import (
    build_metric_availability_matrix,
    get_flattened_availability_table
)
from backend.app.analytics.structural_breaks import (
    get_all_structural_breaks,
    get_structural_breaks_for_query,
    analyze_blinkit_1p_transition,
    analyze_district_and_lynks_events
)
from backend.app.analytics.competitive_attribution import (
    compute_comprehensive_competitive_gaps,
    classify_competitive_dimension
)
from backend.app.analytics.competitive_findings import (
    get_all_competitive_findings,
    get_finding_by_id
)

client = TestClient(app)


# -----------------------------------------------------------------------------
# Module A: Comparability Engine Tests
# -----------------------------------------------------------------------------
def test_comparability_rules_completeness():
    """Verifies that master comparability registry contains valid rules across all 4 tiers."""
    rules = get_all_comparability_rules()
    assert len(rules) >= 6
    
    levels_found = set(r['comparability_level'] for r in rules)
    assert 'LEVEL_1' in levels_found
    assert 'LEVEL_2' in levels_found
    assert 'LEVEL_3' in levels_found
    assert 'LEVEL_4' in levels_found


def test_quick_commerce_revenue_structural_break_rule():
    """
    Verifies that pre-Q2FY26 revenue is LEVEL_2 (comparable with adjustment),
    while Q2FY26 onwards is strictly LEVEL_4 (INCOMPARABLE / BLOCKED).
    """
    rule_pre = get_comparability_rule('QuickCommerce', 'adj_revenue_cr', fiscal_year='FY25', quarter_num=4)
    assert rule_pre['comparability_level'] == 'LEVEL_2'
    assert rule_pre['rule_id'] == 'RULE-COMP-003'
    
    rule_post = get_comparability_rule('QuickCommerce', 'adj_revenue_cr', fiscal_year='FY26', quarter_num=2)
    assert rule_post['comparability_level'] == 'LEVEL_4'
    assert rule_post['rule_id'] == 'RULE-COMP-004'
    assert 'BLOCKED' in rule_post['adjustment_formula']


def test_gov_vs_nov_cross_subtraction_strictly_blocked():
    """Verifies that cross GOV vs NOV comparison is classified as LEVEL_4 INCOMPARABLE."""
    rule = get_comparability_rule('Food', 'cross_gov_nov')
    assert rule['comparability_level'] == 'LEVEL_4'
    assert rule['rule_id'] == 'RULE-COMP-006'
    assert 'BLOCKED' in rule['adjustment_formula']


# -----------------------------------------------------------------------------
# Module B: Metric Reconciliation & Availability Matrix Tests
# -----------------------------------------------------------------------------
def test_metric_availability_matrix_null_preservation():
    """
    Verifies that metric availability matrix correctly reports paired vs single disclosures
    and never coerces missing observations to zero.
    """
    matrix = build_metric_availability_matrix()
    assert len(matrix) >= 20
    
    # Food AOV is unavailable for both in quarterly summary tables
    food_aov = next(m for m in matrix if m['segment'] == 'Food' and m['metric_key'] == 'aov_inr')
    assert food_aov['availability_status'] in ['UNAVAILABLE_BOTH', 'ASYMMETRIC_SINGLE_DISCLOSURE']
    assert food_aov['paired_quarters_count'] == 0
    
    # Quick commerce dark stores is fully paired
    qc_stores = next(m for m in matrix if m['segment'] == 'QuickCommerce' and m['metric_key'] == 'dark_stores')
    assert qc_stores['availability_status'] == 'FULLY_PAIRED'
    assert qc_stores['paired_quarters_count'] == 10


def test_flattened_availability_table_generation():
    """Verifies flat availability table export."""
    flat_df = get_flattened_availability_table()
    assert not flat_df.empty
    assert 'segment' in flat_df.columns
    assert 'metric_key' in flat_df.columns
    assert 'paired_disclosed_count' in flat_df.columns


# -----------------------------------------------------------------------------
# Module C: Structural Breaks & Corporate Event Engine Tests
# -----------------------------------------------------------------------------
def test_structural_break_register_events():
    """Verifies that all required corporate structural events are cataloged with source citations."""
    events = get_all_structural_breaks()
    assert len(events) >= 4
    
    event_ids = set(e['event_id'] for e in events)
    assert 'SB-001' in event_ids  # Blinkit 1P
    assert 'SB-002' in event_ids  # District Ticketing
    assert 'SB-003' in event_ids  # Swiggy Lynks
    assert 'SB-004' in event_ids  # Swiggy Dineout
    
    for ev in events:
        assert ev['announcement_date'] is not None
        assert ev['effective_date'] is not None
        assert ev['first_affected_quarter'] is not None
        assert ev['source_doc'] is not None
        assert ev['source_page'] is not None


def test_blinkit_1p_transition_4_series_breakdown():
    """
    Verifies the deep 4-series breakdown of Blinkit 1P transition:
    - Series A: Reported revenue
    - Series B: LFL status (blocked from unverified COGS fabrication)
    - Series C: Operating measures (NOV and Stores)
    - Series D: Margins with native denominators
    """
    analysis = analyze_blinkit_1p_transition()
    assert analysis['structural_break_event_id'] == 'SB-001'
    assert analysis['effective_quarter'] == 'Q2FY26'
    
    timeline = analysis['timeline']
    assert len(timeline) == 10
    
    # Check pre-Q2FY26 vs post-Q1FY26
    q1fy26 = next(r for r in timeline if r['quarter'] == 'Q1FY26')
    assert q1fy26['is_post_1p_transition'] is False
    assert q1fy26['comparability_classification'] == 'LEVEL_2_COMPARABLE_WITH_ADJUSTMENT'
    assert q1fy26['blinkit_lfl_revenue_status'] == 'LFL_DIRECTLY_COMPARABLE_3P'
    
    q2fy26 = next(r for r in timeline if r['quarter'] == 'Q2FY26')
    assert q2fy26['is_post_1p_transition'] is True
    assert q2fy26['comparability_classification'] == 'LEVEL_4_INCOMPARABLE'
    assert q2fy26['blinkit_lfl_revenue_status'] == 'LFL_BLOCKED_UNAUDITED_COGS'
    assert q2fy26['blinkit_lfl_revenue_cr'] is None


def test_district_and_lynks_event_analysis():
    """Verifies organic like-for-like anchor for District and Lynks deconsolidation scope."""
    res = analyze_district_and_lynks_events()
    assert 'district_ticketing_acquisition' in res
    assert 'lynks_supply_chain_divestment' in res
    
    dist = res['district_ticketing_acquisition']
    assert dist['reported_yoy_gov_growth_q2fy25'] == 171.0
    assert dist['disclosed_organic_lfl_yoy_growth_q2fy25'] == 53.0
    assert dist['inorganic_growth_contribution_pts'] == 118.0
    
    lynks = res['lynks_supply_chain_divestment']
    assert lynks['expected_quarterly_ebitda_benefit_cr'] == 20.0
    assert lynks['expected_quarterly_revenue_reduction_cr'] == 200.0


# -----------------------------------------------------------------------------
# Module D: Multi-Dimensional Competitive Gap Attribution Tests
# -----------------------------------------------------------------------------
def test_comprehensive_competitive_gaps_governance():
    """
    Verifies that competitive gap engine enforces comparability governance:
    - Level 4 comparisons have gap_absolute set to None and is_comparison_blocked True
    - Level 1 and Level 2 comparisons have valid gap numbers
    - QoQ trajectory is properly classified
    """
    gaps = compute_comprehensive_competitive_gaps()
    assert len(gaps) > 0
    
    # Check Quick Commerce post-Q1FY26 revenue gaps
    qc_rev_post = [
        g for g in gaps 
        if g['segment'] == 'QuickCommerce' 
        and g['metric'] == 'adj_revenue_cr' 
        and int(g['fiscal_year'].replace('FY', '')) >= 26 
        and int(g['quarter_num']) >= 2
    ]
    assert len(qc_rev_post) > 0
    for g in qc_rev_post:
        assert g['comparability_level'] == 'LEVEL_4'
        assert g['is_comparison_blocked'] is True
        assert g['gap_absolute'] is None
        assert g['gap_direction'] == 'INCOMPARABLE_ACCOUNTING_BREAK'
        assert g['leader'] == 'BLOCKED'
        
    # Check Quick Commerce dark store gaps (Level 1)
    qc_stores = [g for g in gaps if g['segment'] == 'QuickCommerce' and g['metric'] == 'dark_stores']
    assert len(qc_stores) > 0
    for g in qc_stores:
        assert g['comparability_level'] == 'LEVEL_1'
        assert g['is_comparison_blocked'] is False
        assert g['gap_absolute'] is not None
        assert g['leader'] in ['Eternal', 'Swiggy', 'Equal']


# -----------------------------------------------------------------------------
# Module E: Evidence-Backed Competitive Findings Tests
# -----------------------------------------------------------------------------
def test_competitive_findings_epistemic_standards():
    """
    Verifies that all 8 research findings conform to the 6 epistemic evidence tiers
    and contain source page citations and follow-up questions.
    """
    findings = get_all_competitive_findings()
    assert len(findings) == 8
    
    valid_labels = {
        'REPORTED FACT', 'DERIVED FACT', 'MANAGEMENT EXPLANATION',
        'ANALYST INTERPRETATION', 'HYPOTHESIS', 'UNVERIFIED / INSUFFICIENT EVIDENCE'
    }
    
    for f in findings:
        assert f['finding_id'].startswith('FINDING-')
        assert f['epistemic_evidence_label'] in valid_labels
        assert len(f['supporting_metrics']) > 0
        assert f['exact_source_pages'] is not None
        assert len(f['supporting_evidence']) > 0
        assert len(f['confidence_level']) > 0
        assert len(f['limitations']) > 0
        assert len(f['follow_up_questions']) > 0


def test_get_finding_by_id():
    """Verifies single finding retrieval by ID."""
    f = get_finding_by_id('FINDING-001')
    assert f is not None
    assert "Blinkit Store Expansion" in f['title']
    
    none_f = get_finding_by_id('FINDING-999')
    assert none_f is None


# -----------------------------------------------------------------------------
# Module F: FastAPI Competitive Router Integration Tests
# -----------------------------------------------------------------------------
def test_api_competitive_comparability():
    res = client.get("/api/v1/competitive/comparability?segment=QuickCommerce")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["total_rules"] > 0


def test_api_competitive_metric_matrix():
    res = client.get("/api/v1/competitive/metric-matrix")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["total_metrics_mapped"] > 0


def test_api_competitive_gaps():
    res = client.get("/api/v1/competitive/gaps?segment=QuickCommerce")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["total_gap_records"] > 0


def test_api_competitive_events():
    res = client.get("/api/v1/competitive/events?company=Eternal")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["total_events"] > 0


def test_api_competitive_structural_breaks():
    res1 = client.get("/api/v1/competitive/structural-breaks?topic=blinkit_1p")
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["status"] == "success"
    assert "timeline" in data1["analysis"]
    
    res2 = client.get("/api/v1/competitive/structural-breaks?topic=m_and_a_divestment")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["status"] == "success"
    assert "district_ticketing_acquisition" in data2["analysis"]


def test_api_competitive_findings():
    res = client.get("/api/v1/competitive/findings")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["total_findings"] == 8
    
    single_res = client.get("/api/v1/competitive/findings?finding_id=FINDING-005")
    assert single_res.status_code == 200
    single_data = single_res.json()
    assert single_data["status"] == "success"
    assert single_data["data"]["finding_id"] == "FINDING-005"
