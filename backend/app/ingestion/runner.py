"""
FoodIQ Unified Ingestion Coordinator & Report Generator

Executes:
1. Swiggy Ingestion Pipeline
2. Eternal Ingestion Pipeline
3. Seeding Financial Governance Comparability Rules
4. Generates all deliverables:
   - data/reports/data_quality_report.json
   - data/reports/data_quality_report.csv
   - data/reports/ingestion_summary.json
   - data/reports/source_lineage_report.csv
   - data/reports/unresolved_observations.csv
"""
import os
import csv
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from backend.app.config import settings
from backend.app.database import SessionLocal, Base, engine
import backend.app.models
from backend.app.models.core import IngestionRun, SourceDocument, SourcePage, BusinessSegment, Company
from backend.app.models.metrics import MetricObservation, MetricDefinition
from backend.app.models.governance import DataQualityFlag, SourceConflict, ComparabilityRule, CorporateEvent
from backend.app.ingestion.swiggy_ingest import SwiggyIngestionPipeline
from backend.app.ingestion.eternal_ingest import EternalIngestionPipeline
from backend.app.services.governance_service import ComparabilityGovernanceEngine

def run_full_ingestion() -> Dict[str, Any]:
    # Ensure database schema is created
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    run_id = f"RUN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    run_record = IngestionRun(
        run_id=run_id,
        started_at=datetime.utcnow(),
        status="RUNNING",
        company_scope="ALL",
        notes="Automated Phase 1 ingestion of Swiggy and Eternal research packs."
    )
    db.add(run_record)
    db.commit()

    print(f"=== Starting Ingestion Run: {run_id} ===")

    # 1. Swiggy Pipeline
    print("Ingesting Swiggy research package...")
    swiggy_pipe = SwiggyIngestionPipeline(db)
    swiggy_stats = swiggy_pipe.run()
    print("Swiggy stats:", swiggy_stats)

    # 2. Eternal Pipeline
    print("Ingesting Eternal research package with OCR validation...")
    eternal_pipe = EternalIngestionPipeline(db)
    eternal_stats = eternal_pipe.run()
    print("Eternal stats:", eternal_stats)

    # 3. Seed Comparability Governance Rules
    print("Seeding comparability governance rules...")
    ComparabilityGovernanceEngine.seed_rules(db)

    # Aggregate counts
    total_docs = db.query(SourceDocument).count()
    total_pages = db.query(SourcePage).count()
    total_obs = db.query(MetricObservation).count()
    total_flags = db.query(DataQualityFlag).count()
    total_conflicts = db.query(SourceConflict).count()
    total_rules = db.query(ComparabilityRule).count()
    total_events = db.query(CorporateEvent).count()

    run_record.completed_at = datetime.utcnow()
    run_record.status = "COMPLETED"
    run_record.total_documents = total_docs
    run_record.total_pages = total_pages
    run_record.total_observations = total_obs
    run_record.total_flags = total_flags
    db.commit()

    summary_data = {
        "run_id": run_id,
        "completed_at": run_record.completed_at.isoformat(),
        "status": "COMPLETED",
        "counts": {
            "companies": db.query(Company).count(),
            "source_documents": total_docs,
            "source_pages": total_pages,
            "business_segments": db.query(BusinessSegment).count(),
            "metric_definitions": db.query(MetricDefinition).count(),
            "metric_observations": total_obs,
            "swiggy_observations": db.query(MetricObservation).filter_by(company_id="SWIGGY").count(),
            "eternal_observations": db.query(MetricObservation).filter_by(company_id="ETERNAL").count(),
            "data_quality_flags": total_flags,
            "source_conflicts": total_conflicts,
            "comparability_rules": total_rules,
            "corporate_events": total_events
        },
        "swiggy_pipeline_stats": swiggy_stats,
        "eternal_pipeline_stats": eternal_stats
    }

    # Generate Reports
    generate_reports(db, summary_data)

    db.close()
    print("=== Ingestion Finished Successfully ===")
    return summary_data

def generate_reports(db, summary_data: Dict[str, Any]):
    rep_dir = settings.REPORTS_DIR
    os.makedirs(rep_dir, exist_ok=True)

    # 1. Ingestion Summary JSON
    with open(rep_dir / "ingestion_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    # 2. Data Quality Report JSON & CSV
    flags = db.query(DataQualityFlag).all()
    dq_list = []
    for f in flags:
        dq_list.append({
            "flag_id": f.flag_id,
            "observation_id": f.observation_id or "",
            "issue_code": f.issue_code,
            "severity": f.severity,
            "issue_description": f.issue_description,
            "audit_trail": f.audit_trail,
            "is_resolved": f.is_resolved
        })

    with open(rep_dir / "data_quality_report.json", "w", encoding="utf-8") as f:
        json.dump(dq_list, f, indent=2)

    with open(rep_dir / "data_quality_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["flag_id", "observation_id", "issue_code", "severity", "issue_description", "audit_trail", "is_resolved"])
        writer.writeheader()
        writer.writerows(dq_list)

    # 3. Source Lineage Report CSV
    observations = db.query(MetricObservation).limit(1000).all()
    lineage_rows = []
    for o in observations:
        doc = db.query(SourceDocument).filter_by(document_id=o.source_document_id).first()
        lineage_rows.append({
            "observation_id": o.observation_id,
            "company_id": o.company_id,
            "segment_id": o.segment_id,
            "metric_id": o.metric_id,
            "fiscal_year": o.fiscal_year,
            "fiscal_quarter": o.fiscal_quarter,
            "period_end_date": str(o.period_end_date),
            "value": str(o.value) if o.value is not None else "NULL",
            "unit": o.unit,
            "source_document_id": o.source_document_id,
            "source_pdf": doc.original_file_name if doc else "",
            "pdf_checksum_sha256": doc.file_checksum_sha256 if doc else "",
            "source_page_id": o.source_page_id or "",
            "observation_type": o.observation_type,
            "validation_status": o.validation_status
        })

    with open(rep_dir / "source_lineage_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "observation_id", "company_id", "segment_id", "metric_id",
            "fiscal_year", "fiscal_quarter", "period_end_date", "value",
            "unit", "source_document_id", "source_pdf", "pdf_checksum_sha256",
            "source_page_id", "observation_type", "validation_status"
        ])
        writer.writeheader()
        writer.writerows(lineage_rows)

    # 4. Unresolved Observations CSV
    unresolved = db.query(MetricObservation).filter(MetricObservation.validation_status != "PASSED").all()
    unres_rows = []
    for u in unresolved:
        unres_rows.append({
            "observation_id": u.observation_id,
            "company_id": u.company_id,
            "metric_id": u.metric_id,
            "quarter": f"{u.fiscal_quarter}{u.fiscal_year}",
            "raw_source_value": u.raw_source_value or "",
            "verified_value": str(u.verified_value) if u.verified_value is not None else "",
            "validation_status": u.validation_status,
            "analyst_notes": u.analyst_notes or ""
        })

    with open(rep_dir / "unresolved_observations.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "observation_id", "company_id", "metric_id", "quarter",
            "raw_source_value", "verified_value", "validation_status", "analyst_notes"
        ])
        writer.writeheader()
        writer.writerows(unres_rows)

if __name__ == "__main__":
    run_full_ingestion()
