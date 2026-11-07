import pytest
from backend.app.ingestion.swiggy_ingest import SwiggyIngestionPipeline
from backend.app.ingestion.eternal_ingest import EternalIngestionPipeline
from backend.app.models.metrics import MetricObservation
from backend.app.models.core import SourceDocument

def test_ingestion_counts(test_db_session):
    docs = test_db_session.query(SourceDocument).all()
    assert len(docs) == 14 # 6 Swiggy + 8 Eternal

    swiggy_obs = test_db_session.query(MetricObservation).filter_by(company_id="SWIGGY").count()
    assert swiggy_obs == 400

    eternal_obs = test_db_session.query(MetricObservation).filter_by(company_id="ETERNAL").count()
    assert eternal_obs >= 150

def test_ingestion_idempotency(test_db_session):
    initial_count = test_db_session.query(MetricObservation).count()

    # Run Swiggy pipeline again
    swiggy_pipe = SwiggyIngestionPipeline(test_db_session)
    stats_swiggy = swiggy_pipe.run()
    # No new observations should be inserted
    assert stats_swiggy["observations"] == 0

    # Run Eternal pipeline again
    eternal_pipe = EternalIngestionPipeline(test_db_session)
    stats_eternal = eternal_pipe.run()
    assert stats_eternal["observations"] == 0

    final_count = test_db_session.query(MetricObservation).count()
    assert final_count == initial_count
