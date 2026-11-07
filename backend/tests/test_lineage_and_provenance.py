import pytest
from backend.app.models.core import SourceDocument
from backend.app.models.metrics import MetricObservation
from backend.app.services.lineage_service import ProvenanceLineageService

def test_source_document_sha256_checksums(test_db_session):
    docs = test_db_session.query(SourceDocument).all()
    for doc in docs:
        assert len(doc.file_checksum_sha256) == 64, f"Doc {doc.document_id} has invalid sha256 checksum length"
        assert all(c in "0123456789abcdef" for c in doc.file_checksum_sha256.lower())

def test_lineage_service_retrieval(test_db_session):
    obs = test_db_session.query(MetricObservation).filter_by(company_id="SWIGGY").first()
    assert obs is not None
    lineage = ProvenanceLineageService.get_lineage(test_db_session, obs.observation_id)
    assert lineage is not None
    assert lineage["observation_id"] == obs.observation_id
    assert lineage["company"]["id"] == "SWIGGY"
    assert "file_checksum_sha256" in lineage["provenance"]
    assert len(lineage["provenance"]["file_checksum_sha256"]) == 64

def test_lineage_service_non_existent(test_db_session):
    lineage = ProvenanceLineageService.get_lineage(test_db_session, "NON_EXISTENT_OBS_ID")
    assert lineage is None
