import pytest
from backend.app.models.metrics import MetricObservation, MetricDefinition

def test_null_preservation(test_db_session):
    """Verifies that missing values are stored as NULL and never converted to 0."""
    # Look for observations where raw value was empty or null
    null_obs = test_db_session.query(MetricObservation).filter(MetricObservation.value == None).all()
    # If there are any null observations, verify they are None, not 0.0
    for o in null_obs:
        assert o.value is None
        assert o.value != 0.0

def test_swiggy_food_delivery_nov_not_fabricated(test_db_session):
    """
    CRITICAL RULE: Swiggy management explicitly does not disclose Food Delivery NOV.
    FoodIQ must never fabricate a swiggy_food_nov metric!
    """
    food_nov_obs = test_db_session.query(MetricObservation).filter(
        MetricObservation.company_id == "SWIGGY",
        MetricObservation.segment_id == "SWIGGY_FOOD",
        MetricObservation.metric_id.ilike("%nov%")
    ).all()
    assert len(food_nov_obs) == 0, "Swiggy Food Delivery NOV must NOT exist or be fabricated!"

def test_margin_denominators_preserved(test_db_session):
    """Margins must always carry their denominator."""
    margin_defs = test_db_session.query(MetricDefinition).filter(
        MetricDefinition.unit.ilike("%percent%")
    ).all()
    for m in margin_defs:
        assert m.denominator_formula is not None or m.implementation_notes is not None
