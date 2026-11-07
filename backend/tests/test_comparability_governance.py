import pytest
from backend.app.services.governance_service import ComparabilityGovernanceEngine
from backend.app.models.governance import ComparabilityRule

def test_comparability_rules_seeded(test_db_session):
    rules = test_db_session.query(ComparabilityRule).all()
    assert len(rules) >= 5
    rule_ids = {r.rule_id for r in rules}
    assert "RULE-FOOD-GOV-NOV" in rule_ids
    assert "RULE-QCOMM-REVENUE-1P-BREAK" in rule_ids

def test_gov_nov_direct_comparison_blocked():
    res = ComparabilityGovernanceEngine.evaluate_comparison(
        metric_a="swiggy_gov_cr",
        metric_b="eternal_food_nov"
    )
    assert res["can_compare_directly"] is False
    assert res["tier"] == "INCOMPARABLE"
    assert "GOV and NOV are distinct" in res["warning"]

def test_qcomm_revenue_1p_break_blocked():
    res = ComparabilityGovernanceEngine.evaluate_comparison(
        metric_a="swiggy_qcomm_adj_rev",
        metric_b="eternal_qcomm_adj_rev",
        quarter="Q2FY26"
    )
    assert res["can_compare_directly"] is False
    assert res["tier"] == "INCOMPARABLE"
    assert "1P inventory ownership transition" in res["warning"]
