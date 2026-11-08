"""
Unit and integration tests for FoodIQ Management Credibility & Narrative Verification Engine (Phase 4).
Verifies:
1. Statement extraction integrity, categories, and PDF source page citations.
2. Commitment lifecycle stages (ANNOUNCED -> ACTIVE -> DUE -> EVALUATED -> CLOSED).
3. Strict 7-tier outcome taxonomy (DELIVERED, PARTIALLY_DELIVERED, MISSED, PENDING, NOT_OBJECTIVELY_MEASURABLE, WITHDRAWN, INSUFFICIENT).
4. Pending commitments never penalized as missed before target period maturation.
5. Scorecard denominator isolation (evaluable completed strictly excludes pending and non-measurable).
6. Strict and broad delivery rate sensitivities.
7. Company execution breakdown (Eternal vs Swiggy).
8. Narrative verification engine and correlation vs causation qualifications.
9. Strategic initiative tracker integrity.
10. Phase 4 FastAPI REST endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.analytics.credibility_engine import (
    get_all_management_statements,
    get_commitment_by_id,
    calculate_management_credibility_scorecard,
    get_all_narrative_verifications,
    get_all_strategic_initiatives,
    get_company_credibility_comparison,
    STATEMENT_CATEGORIES
)

client = TestClient(app)


# -----------------------------------------------------------------------------
# Module A: Statement Extraction & Lifecycle Tests
# -----------------------------------------------------------------------------
def test_management_statements_repository():
    """Verifies that statements are extracted with required metadata and valid categories."""
    statements = get_all_management_statements()
    assert len(statements) >= 20  # Contains both Swiggy and Eternal commitments
    
    for s in statements:
        assert s['commitment_id'] is not None
        assert s['company'] in ['Eternal', 'Swiggy']
        assert s['speaker'] is not None
        assert len(s['verbatim_quote']) > 0
        assert s['source_doc'].endswith('.pdf')
        assert s['source_page'] > 0
        assert s['category'] in STATEMENT_CATEGORIES
        assert s['lifecycle_stage'] in ['ANNOUNCED', 'ACTIVE', 'DUE', 'EVALUATED', 'CLOSED']


def test_commitment_lifecycle_and_taxonomy():
    """Verifies that all commitments map to the 7-tier outcome taxonomy."""
    valid_outcomes = {
        'DELIVERED', 'PARTIALLY_DELIVERED', 'MISSED', 'PENDING',
        'NOT_OBJECTIVELY_MEASURABLE', 'WITHDRAWN_OR_SUPERSEDED', 'INSUFFICIENT_EVIDENCE'
    }
    statements = get_all_management_statements()
    for s in statements:
        assert s['outcome_status'] in valid_outcomes


def test_pending_commitments_not_marked_as_missed():
    """
    Ensures that active commitments whose target periods have not matured
    are classified as PENDING and not MISSED.
    """
    comm_sw_2 = get_commitment_by_id('COMM-SW-002')
    assert comm_sw_2['target_period'] == 'Medium-term (FY28+)'
    assert comm_sw_2['outcome_status'] == 'PENDING'
    assert comm_sw_2['lifecycle_stage'] == 'ACTIVE'
    
    comm_et_6 = get_commitment_by_id('COMM-ET-006')
    assert comm_et_6['outcome_status'] == 'PENDING'


def test_target_vs_actual_variance_reconciliation():
    """Verifies that variance and achievement percentages are mathematically exact."""
    # Blinkit store target: 1000 guided, 1300 actual
    comm_et_1 = get_commitment_by_id('COMM-ET-001')
    assert comm_et_1['target_value'] == 1000.0
    assert comm_et_1['actual_value_reported'] == 1300.0
    assert comm_et_1['variance'] == 300.0
    assert comm_et_1['pct_achievement'] == 130.0
    assert comm_et_1['outcome_status'] == 'DELIVERED'
    
    # Swiggy store target: 1200 guided, 1240 actual
    comm_sw_6 = get_commitment_by_id('COMM-SW-006')
    assert comm_sw_6['target_value'] == 1200.0
    assert comm_sw_6['actual_value_reported'] == 1240.0
    assert comm_sw_6['variance'] == 40.0
    assert comm_sw_6['pct_achievement'] == pytest.approx(103.3, abs=0.1)
    assert comm_sw_6['outcome_status'] == 'DELIVERED'


# -----------------------------------------------------------------------------
# Module B: Scorecard & Denominator Isolation Tests
# -----------------------------------------------------------------------------
def test_scorecard_denominator_isolation():
    """
    Verifies that the evaluable completed denominator strictly excludes
    pending and non-measurable statements.
    """
    scorecard = calculate_management_credibility_scorecard()
    
    total = scorecard['total_commitments']
    evaluable = scorecard['evaluable_completed']
    delivered = scorecard['delivered_count']
    partially = scorecard['partially_delivered_count']
    missed = scorecard['missed_count']
    pending = scorecard['pending_count']
    unmeasurable = scorecard['not_objectively_measurable_count']
    
    assert total == evaluable + pending + unmeasurable + scorecard['withdrawn_count']
    assert evaluable == delivered + partially + missed
    
    # Strict delivery rate
    expected_strict = round((delivered / evaluable * 100), 2)
    assert scorecard['strict_delivery_rate_pct'] == expected_strict
    
    # Broad delivery rate
    expected_broad = round(((delivered + 0.5 * partially) / evaluable * 100), 2)
    assert scorecard['broad_delivery_rate_pct'] == expected_broad


def test_company_credibility_breakdown():
    """Verifies separate execution analysis for Eternal and Swiggy."""
    comp = get_company_credibility_comparison()
    assert comp['comparability_status'] == 'LEVEL_3_DIRECTIONALLY_COMPARABLE'
    
    et = comp['eternal']
    sw = comp['swiggy']
    
    assert et['company_filter'] == 'Eternal'
    assert sw['company_filter'] == 'Swiggy'
    
    assert et['strict_delivery_rate_pct'] >= 75.0
    assert sw['strict_delivery_rate_pct'] >= 70.0
    
    assert et['delivered_count'] >= 4
    assert sw['delivered_count'] >= 2


# -----------------------------------------------------------------------------
# Module C: Narrative Verification & Strategic Initiatives Tests
# -----------------------------------------------------------------------------
def test_narrative_verification_tiers():
    """Verifies that qualitative explanations are tested against empirical metrics."""
    narratives = get_all_narrative_verifications()
    assert len(narratives) >= 5
    
    valid_tiers = {
        'SUPPORTED_BY_DISCLOSED_EVIDENCE', 'PARTIALLY_SUPPORTED',
        'CONTRADICTED_BY_DISCLOSED_EVIDENCE', 'NOT_TESTABLE', 'INSUFFICIENT_DISCLOSURE'
    }
    
    for n in narratives:
        assert n['verification_tier'] in valid_tiers
        assert len(n['relevant_metrics']) > 0
        assert len(n['correlation_vs_causation_note']) > 0
        assert n['document'].endswith('.pdf')
        assert n['page'] > 0


def test_strategic_initiative_tracking():
    """Verifies that strategic initiatives are logged across both companies."""
    initiatives = get_all_strategic_initiatives()
    assert len(initiatives) >= 7
    
    cos = set(init['company'] for init in initiatives)
    assert 'Eternal' in cos
    assert 'Swiggy' in cos
    
    for init in initiatives:
        assert init['status'] in ['SCALING', 'MATURE', 'DISCONTINUED / RESTRUCTURED', 'PILOT', 'DISCONTINUED']
        assert init['launch_period'] is not None
        assert len(init['financial_evidence']) > 0
        assert len(init['risks']) > 0


# -----------------------------------------------------------------------------
# Module D: FastAPI REST Endpoints Tests
# -----------------------------------------------------------------------------
def test_api_credibility_endpoints():
    """Verifies all Phase 4 FastAPI REST endpoints return 200 with sanitized JSON."""
    r_stmts = client.get("/api/v1/credibility/statements")
    assert r_stmts.status_code == 200
    assert r_stmts.json()['status'] == "success"
    assert len(r_stmts.json()['statements']) > 0
    
    r_comms = client.get("/api/v1/credibility/commitments")
    assert r_comms.status_code == 200
    assert r_comms.json()['status'] == "success"
    
    r_sc = client.get("/api/v1/credibility/scorecard")
    assert r_sc.status_code == 200
    assert r_sc.json()['scorecard']['strict_delivery_rate_pct'] is not None
    
    r_narr = client.get("/api/v1/credibility/narratives")
    assert r_narr.status_code == 200
    assert len(r_narr.json()['narratives']) > 0
    
    r_inits = client.get("/api/v1/credibility/initiatives")
    assert r_inits.status_code == 200
    assert len(r_inits.json()['initiatives']) > 0
    
    r_comp = client.get("/api/v1/credibility/comparison")
    assert r_comp.status_code == 200
    assert "eternal" in r_comp.json()['comparison']
    assert "swiggy" in r_comp.json()['comparison']
