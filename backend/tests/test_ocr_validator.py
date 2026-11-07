import pytest
from backend.app.ingestion.ocr_validator import EternalOCRValidator

def test_ocr_clean_match():
    res = EternalOCRValidator.validate_and_reconcile(
        quarter="Q1FY26",
        segment="ETERNAL_FOOD",
        metric="food_nov",
        raw_ocr="8967",
        source_doc="ETERNAL-Q1FY26",
        source_page=12
    )
    assert res.validation_status == "VERIFIED_CLEAN"
    assert res.verified_value == 8967.0
    assert "perfectly matches" in res.evidence

def test_ocr_malformed_correction():
    # Corrupted OCR token from Q2FY26 Annexure p.12
    res = EternalOCRValidator.validate_and_reconcile(
        quarter="Q2FY25",
        segment="ETERNAL_FOOD",
        metric="food_nov",
        raw_ocr="g281",
        source_doc="ETERNAL-Q2FY26",
        source_page=12
    )
    assert res.validation_status == "CORRECTED_VIA_COMPARATIVE"
    assert res.verified_value == 8281.0
    assert res.flag_code == "OCR_CORRECTED_VIA_COMPARATIVE"
    assert res.severity == "HIGH"
    assert "corrected to 8281.0" in res.evidence

def test_ocr_unresolved_handling():
    res = EternalOCRValidator.validate_and_reconcile(
        quarter="Q9FY99", # Unknown quarter
        segment="UNKNOWN",
        metric="non_existent",
        raw_ocr="corrupted_text_XYZ",
        source_doc="DOC",
        source_page=1
    )
    assert res.validation_status == "UNRESOLVED_FLAGGED"
    assert res.verified_value is None
    assert res.severity == "CRITICAL"
