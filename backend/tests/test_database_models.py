import pytest
from backend.app.models.core import Company, SourceDocument, BusinessSegment
from backend.app.models.metrics import MetricDefinition, MetricObservation
from backend.app.models.governance import ComparabilityRule, DataQualityFlag, SourceConflict

def test_database_companies(test_db_session):
    companies = test_db_session.query(Company).all()
    assert len(companies) == 2
    ids = {c.company_id for c in companies}
    assert ids == {"SWIGGY", "ETERNAL"}

def test_database_relationships_and_foreign_keys(test_db_session):
    swiggy = test_db_session.query(Company).filter_by(company_id="SWIGGY").first()
    assert swiggy is not None
    assert len(swiggy.documents) == 6
    assert len(swiggy.segments) >= 6
    assert len(swiggy.observations) > 0

    eternal = test_db_session.query(Company).filter_by(company_id="ETERNAL").first()
    assert eternal is not None
    assert len(eternal.documents) == 8
    assert len(eternal.segments) >= 6
    assert len(eternal.observations) > 0

def test_referential_integrity(test_db_session):
    # Every observation must have a valid document and valid company
    obs = test_db_session.query(MetricObservation).limit(50).all()
    for o in obs:
        assert o.company_id in ("SWIGGY", "ETERNAL")
        doc = test_db_session.query(SourceDocument).filter_by(document_id=o.source_document_id).first()
        assert doc is not None, f"Observation {o.observation_id} references non-existent doc {o.source_document_id}"
