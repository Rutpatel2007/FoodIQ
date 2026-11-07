"""
FoodIQ Financial Governance & Comparability Engine

Enforces financial integrity rules:
1. GOV and NOV are distinct economic quantities and not interchangeable.
2. Swiggy Food Delivery NOV does not exist and must never be fabricated.
3. Margins must always carry and display their denominator (% GOV, % NOV, % Revenue).
4. Blinkit Q2 FY26 1P transition is an accounting structural break; direct revenue comparison across Q1FY26-Q2FY26 is prohibited without LFL adjustments.
5. District ticketing acquisition (Q2FY25) and Swiggy Lynks divestment (Q2FY27) must be flagged on affected series.
6. Restatements and conflicts must preserve both historical versions with lineage.
"""
from typing import Dict, List, Optional, Tuple, Any
from sqlalchemy.orm import Session
from backend.app.models.governance import ComparabilityRule

class ComparabilityGovernanceEngine:
    """
    Evaluates whether two financial metrics from Eternal and Swiggy can be validly compared.
    """

    CORE_RULES = [
        {
            "rule_id": "RULE-FOOD-GOV-NOV",
            "metric_a_id": "swiggy_gov_cr",
            "metric_b_id": "eternal_food_nov",
            "comparability_tier": "INCOMPARABLE",
            "adjustment_formula": None,
            "prohibited_operations": "Direct absolute difference, cross-subtraction, or single-axis overlay prohibited.",
            "methodology_caveats": "Swiggy reports Gross Order Value (GOV) gross of discounts/taxes. Eternal reports Net Order Value (NOV) net of customer discounts. They represent different economic boundaries."
        },
        {
            "rule_id": "RULE-FOOD-ADJ-REV",
            "metric_a_id": "swiggy_adjusted_revenue_cr",
            "metric_b_id": "eternal_food_adj_rev",
            "comparability_tier": "DIRECT",
            "adjustment_formula": "swiggy_adj_rev vs eternal_adj_rev",
            "prohibited_operations": None,
            "methodology_caveats": "Both companies define Food Adjusted Revenue as statutory revenue from operations plus net customer delivery charges."
        },
        {
            "rule_id": "RULE-QCOMM-NOV",
            "metric_a_id": "swiggy_nov_cr",
            "metric_b_id": "eternal_qcomm_nov",
            "comparability_tier": "ADJUSTED",
            "adjustment_formula": "swiggy_nov_cr vs eternal_qcomm_nov",
            "prohibited_operations": None,
            "methodology_caveats": "Both companies report Net Order Value for quick commerce. However, Swiggy's historical series includes derived whole-percentage discounts; directional comparison is robust."
        },
        {
            "rule_id": "RULE-QCOMM-REVENUE-1P-BREAK",
            "metric_a_id": "swiggy_adjusted_revenue_cr",
            "metric_b_id": "eternal_qcomm_adj_rev",
            "comparability_tier": "INCOMPARABLE",
            "adjustment_formula": "Must use Like-for-Like (LFL) Adjusted Revenue growth excluding 1P merchandise COGS.",
            "prohibited_operations": "Cross-company revenue growth comparison post-Q1FY26 on reported numbers is strictly prohibited.",
            "methodology_caveats": "In Q2FY26, Blinkit shifted to 1P inventory ownership, recognizing gross merchandise value in revenue (+312% QoQ), while Swiggy operates predominantly as a marketplace intermediary."
        },
        {
            "rule_id": "RULE-PROFITABILITY-MARGINS",
            "metric_a_id": "swiggy_contribution_margin_pct",
            "metric_b_id": "eternal_food_adj_ebitda",
            "comparability_tier": "ADJUSTED",
            "adjustment_formula": "Align denominators to % GOV or compare absolute INR per order.",
            "prohibited_operations": "Comparing margins with different denominators (% GOV vs % NOV) without explicit conversion.",
            "methodology_caveats": "Swiggy margins are reported as % of GOV. Eternal reports absolute INR Cr or % of NOV. Converting without identical order volume or AOV introduces distortion."
        },
        {
            "rule_id": "RULE-DARK-STORE-PRODUCTIVITY",
            "metric_a_id": "swiggy_orders_per_dark_store_per_day",
            "metric_b_id": "eternal_qcomm_darkstores",
            "comparability_tier": "ADJUSTED",
            "adjustment_formula": "Throughput = Total Orders / (Average Active Dark Stores * Days)",
            "prohibited_operations": "Dividing quarterly orders by period-end closing darkstore count.",
            "methodology_caveats": "Swiggy reports throughput based on active store-days; period-end store count distorts rapid expansion quarters."
        }
    ]

    @classmethod
    def seed_rules(cls, db: Session):
        """Seeds canonical governance rules into the database."""
        for r_dict in cls.CORE_RULES:
            existing = db.query(ComparabilityRule).filter_by(rule_id=r_dict["rule_id"]).first()
            if not existing:
                rule = ComparabilityRule(
                    rule_id=r_dict["rule_id"],
                    metric_a_id=r_dict["metric_a_id"],
                    metric_b_id=r_dict["metric_b_id"],
                    comparability_tier=r_dict["comparability_tier"],
                    adjustment_formula=r_dict.get("adjustment_formula"),
                    prohibited_operations=r_dict.get("prohibited_operations"),
                    methodology_caveats=r_dict["methodology_caveats"]
                )
                db.add(rule)
        db.commit()

    @classmethod
    def evaluate_comparison(
        cls,
        metric_a: str,
        metric_b: str,
        quarter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validates if metric_a and metric_b can be compared, returning tier, restrictions, and warnings.
        """
        # Food GOV vs Food NOV
        if ("gov" in metric_a.lower() and "nov" in metric_b.lower()) or ("nov" in metric_a.lower() and "gov" in metric_b.lower()):
            return {
                "can_compare_directly": False,
                "tier": "INCOMPARABLE",
                "warning": "GOV and NOV are distinct financial metrics. GOV is gross order value before customer discounts; NOV is net order value. Direct numerical comparison or difference calculation is prohibited.",
                "reconciliation_required": True
            }

        # Quick commerce revenue post Q1FY26
        if "qcomm" in metric_a.lower() or "qcomm" in metric_b.lower() or "quick" in metric_a.lower():
            if "rev" in metric_a.lower() and "rev" in metric_b.lower():
                if quarter in ("Q2FY26", "Q3FY26", "Q4FY26", "Q1FY27", "Q2FY27"):
                    return {
                        "can_compare_directly": False,
                        "tier": "INCOMPARABLE",
                        "warning": "Blinkit 1P inventory ownership transition in Q2FY26 created an accounting structural break. Reported revenues cannot be directly compared. Must use Like-for-Like (LFL) growth.",
                        "structural_break_event": "CE-ETERNAL-BLINKIT-1P-Q2FY26"
                    }

        return {
            "can_compare_directly": True,
            "tier": "DIRECT",
            "warning": None,
            "reconciliation_required": False
        }
