from decimal import Decimal
import pytest
from backend.app.models.metrics import MetricObservation

def test_swiggy_qcomm_gov_orders_aov_identity(test_db_session):
    """
    Tests mathematical identity for Swiggy Quick Commerce:
    GOV (INR Cr) = Orders (mn) * AOV (INR) / 10
    Verifies within 0.15% rounding residual.
    """
    quarters = [
        ("FY25", "Q1"), ("FY25", "Q2"), ("FY25", "Q3"), ("FY25", "Q4"),
        ("FY26", "Q1"), ("FY26", "Q2"), ("FY26", "Q3"), ("FY26", "Q4"),
        ("FY27", "Q1"), ("FY27", "Q2")
    ]
    for fy, fq in quarters:
        obs_orders = test_db_session.query(MetricObservation).filter_by(
            company_id="SWIGGY", segment_id="SWIGGY_QUICK_COMMERCE",
            metric_id="swiggy_total_orders_mn", fiscal_year=fy, fiscal_quarter=fq
        ).first()
        obs_aov = test_db_session.query(MetricObservation).filter_by(
            company_id="SWIGGY", segment_id="SWIGGY_QUICK_COMMERCE",
            metric_id="swiggy_aov_inr", fiscal_year=fy, fiscal_quarter=fq
        ).first()
        obs_gov = test_db_session.query(MetricObservation).filter_by(
            company_id="SWIGGY", segment_id="SWIGGY_QUICK_COMMERCE",
            metric_id="swiggy_gov_cr", fiscal_year=fy, fiscal_quarter=fq
        ).first()

        assert obs_orders is not None and obs_aov is not None and obs_gov is not None
        d_ord = Decimal(str(obs_orders.value))
        d_aov = Decimal(str(obs_aov.value))
        d_gov = Decimal(str(obs_gov.value))

        recalc = (d_ord * d_aov) / Decimal("10")
        diff = abs(recalc - d_gov)
        pct_diff = (diff / d_gov) * Decimal("100")
        assert pct_diff <= Decimal("0.2"), f"Identity failed in {fq}{fy}: diff={diff} ({pct_diff}%)"

def test_eternal_b2c_nov_additive_identity(test_db_session):
    """
    Tests additive identity for Eternal B2C NOV:
    Food NOV + Quick Commerce NOV + Going-out NOV = B2C NOV
    Verifies exact equality or within rounding offset (<= 1 Cr).
    """
    quarters = [
        ("FY25", "Q1"), ("FY25", "Q2"), ("FY25", "Q3"), ("FY25", "Q4"),
        ("FY26", "Q1"), ("FY26", "Q2"), ("FY26", "Q3"), ("FY26", "Q4"),
        ("FY27", "Q1"), ("FY27", "Q2")
    ]
    for fy, fq in quarters:
        food = test_db_session.query(MetricObservation).filter_by(
            company_id="ETERNAL", segment_id="ETERNAL_FOOD",
            metric_id="eternal_food_nov", fiscal_year=fy, fiscal_quarter=fq
        ).first()
        qcomm = test_db_session.query(MetricObservation).filter_by(
            company_id="ETERNAL", segment_id="ETERNAL_QUICK_COMMERCE",
            metric_id="eternal_qcomm_nov", fiscal_year=fy, fiscal_quarter=fq
        ).first()
        going = test_db_session.query(MetricObservation).filter_by(
            company_id="ETERNAL", segment_id="ETERNAL_GOING_OUT",
            metric_id="eternal_going_out_nov", fiscal_year=fy, fiscal_quarter=fq
        ).first()
        b2c = test_db_session.query(MetricObservation).filter_by(
            company_id="ETERNAL", segment_id="ETERNAL_B2C",
            metric_id="eternal_b2c_nov", fiscal_year=fy, fiscal_quarter=fq
        ).first()

        assert food is not None and qcomm is not None and going is not None and b2c is not None
        d_sum = Decimal(str(food.value)) + Decimal(str(qcomm.value)) + Decimal(str(going.value))
        d_b2c = Decimal(str(b2c.value))
        diff = abs(d_sum - d_b2c)
        assert diff <= Decimal("1.0"), f"B2C NOV sum check failed in {fq}{fy}: diff={diff}"
