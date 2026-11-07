"""
FoodIQ Source-to-Insight Provenance & Lineage Service

Exposes full audit lineage for any financial metric observation:
Observation -> Business Segment -> Metric Definition -> Source Page -> Source Document -> SHA-256 Checksum
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.metrics import MetricObservation
from backend.app.models.core import SourcePage, SourceDocument, BusinessSegment, Company
from backend.app.models.governance import DataQualityFlag

class ProvenanceLineageService:
    @classmethod
    def get_lineage(cls, db: Session, observation_id: str) -> Optional[Dict[str, Any]]:
        obs = db.query(MetricObservation).filter_by(observation_id=observation_id).first()
        if not obs:
            return None

        # Fetch page & document
        page = db.query(SourcePage).filter_by(page_id=obs.source_page_id).first() if obs.source_page_id else None
        doc = db.query(SourceDocument).filter_by(document_id=obs.source_document_id).first() if obs.source_document_id else None
        seg = db.query(BusinessSegment).filter_by(segment_id=obs.segment_id).first()
        company = db.query(Company).filter_by(company_id=obs.company_id).first()
        flags = db.query(DataQualityFlag).filter_by(observation_id=observation_id).all()

        return {
            "observation_id": obs.observation_id,
            "company": {
                "id": company.company_id if company else obs.company_id,
                "name": company.canonical_name if company else obs.company_id,
                "ticker": company.ticker_symbol if company else ""
            },
            "segment": {
                "id": seg.segment_id if seg else obs.segment_id,
                "name": seg.segment_name if seg else "",
                "brand": seg.commercial_brand if seg else "",
                "scope": seg.scope_level if seg else ""
            },
            "metric": {
                "id": obs.metric_id,
                "value": float(obs.value) if obs.value is not None else None,
                "raw_source_value": obs.raw_source_value,
                "verified_value": float(obs.verified_value) if obs.verified_value is not None else None,
                "unit": obs.unit,
                "denominator_basis": obs.denominator_basis,
                "observation_type": obs.observation_type,
                "validation_status": obs.validation_status
            },
            "time_period": {
                "fiscal_year": obs.fiscal_year,
                "fiscal_quarter": obs.fiscal_quarter,
                "period_end_date": str(obs.period_end_date)
            },
            "provenance": {
                "source_document_id": doc.document_id if doc else obs.source_document_id,
                "original_file_name": doc.original_file_name if doc else "",
                "file_checksum_sha256": doc.file_checksum_sha256 if doc else "",
                "total_pages": doc.total_pages if doc else None,
                "source_page_id": page.page_id if page else obs.source_page_id,
                "pdf_page_number": page.pdf_page_number if page else None,
                "printed_page_number": page.printed_page_number if page else None,
                "section_hint": page.section_hint if page else "",
                "has_raster_tables": page.has_raster_tables if page else False,
                "extracted_text_preview": page.extracted_text[:200] if page and page.extracted_text else None
            },
            "quality_flags": [
                {
                    "flag_id": f.flag_id,
                    "issue_code": f.issue_code,
                    "severity": f.severity,
                    "description": f.issue_description,
                    "audit_trail": f.audit_trail,
                    "is_resolved": f.is_resolved
                }
                for f in flags
            ],
            "analyst_notes": obs.analyst_notes,
            "created_at": obs.created_at.isoformat() if obs.created_at else None
        }
