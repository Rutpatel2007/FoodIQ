"""
FoodIQ FastAPI Corporate Disclosure Intelligence & Research Monitoring Router (Phase 8).
Exposes REST endpoints for:
- Corporate Disclosure Monitoring Dashboard
- Persistent Disclosure Register & Ingestion Queue
- New Filing Upload with SHA-256 Deduplication
- Analyst Review, Approval & Rollback Controls
- Data Quality & Financial Anomaly Scanner
- Research Impact Analysis
"""

from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

from backend.app.analytics.repository import sanitize_for_json
from backend.app.analytics.disclosure_intelligence import (
    get_disclosure_monitoring_overview,
    register_new_disclosure,
    approve_disclosure_ingestion,
    rollback_disclosure_ingestion,
    detect_data_anomalies,
    analyze_research_impact
)

router = APIRouter(prefix="/disclosures", tags=["Corporate Disclosure Intelligence & Research Monitoring"])


class RollbackRequest(BaseModel):
    reason: str = Field(..., description="Audit rationale for rolling back the disclosure")
    analyst: str = Field("Lead Data Auditor", description="Analyst name")


class ApproveRequest(BaseModel):
    analyst: str = Field("Lead Data Auditor", description="Approving analyst name")


@router.get("/monitor", summary="Corporate Disclosure Monitoring Overview")
def get_monitoring_overview() -> Dict[str, Any]:
    """Returns overview of latest corporate filings, missing quarters, and queue status."""
    return sanitize_for_json(get_disclosure_monitoring_overview())


@router.get("/register", summary="Persistent Disclosure Register")
def get_disclosure_register() -> Dict[str, Any]:
    """Lists all registered disclosures with checksums and processing statuses."""
    overview = get_disclosure_monitoring_overview()
    return sanitize_for_json({
        "status": "success",
        "total_disclosures": overview["total_disclosures_registered"],
        "data": overview["recent_disclosures"]
    })


@router.post("/upload", summary="Controlled Disclosure Upload & Ingestion")
async def upload_disclosure(
    company_id: str = Form(..., description="'ETERNAL' or 'SWIGGY'"),
    document_title: str = Form(..., description="Filing title"),
    document_category: str = Form("Shareholder Letter", description="Category: Shareholder Letter, Results, etc."),
    reporting_period: str = Form(..., description="e.g. 'Q3 FY27'"),
    source_url: Optional[str] = Form(None, description="Official BSE/NSE/IR URL"),
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    """
    Uploads a new disclosure, computes SHA-256 checksum, checks for duplicates,
    validates the document, and runs research impact analysis.
    """
    content = await file.read()
    res = register_new_disclosure(
        company_id=company_id,
        document_title=document_title,
        document_category=document_category,
        reporting_period=reporting_period,
        file_content_bytes=content,
        file_name=file.filename or "uploaded_filing.pdf",
        source_url=source_url
    )
    if res.get("status") == "DUPLICATE_REJECTED":
        raise HTTPException(status_code=409, detail=res["message"])
    return sanitize_for_json(res)


@router.post("/{disclosure_id}/approve", summary="Analyst Approval & Database Promotion")
def approve_disclosure(disclosure_id: str, req: ApproveRequest) -> Dict[str, Any]:
    """Promotes an uploaded disclosure to APPROVED status."""
    res = approve_disclosure_ingestion(disclosure_id, analyst=req.analyst)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=404, detail=res["message"])
    return sanitize_for_json(res)


@router.post("/{disclosure_id}/rollback", summary="Rollback Unapproved Ingestion")
def rollback_disclosure(disclosure_id: str, req: RollbackRequest) -> Dict[str, Any]:
    """Rolls back an unapproved or erroneous disclosure."""
    res = rollback_disclosure_ingestion(disclosure_id, reason=req.reason, analyst=req.analyst)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=404, detail=res["message"])
    return sanitize_for_json(res)


@router.get("/anomalies", summary="Data Quality & Financial Anomaly Scanner")
def get_data_anomalies() -> Dict[str, Any]:
    """Scans historical observations for broken financial identities and extreme movements."""
    anomalies = detect_data_anomalies()
    return sanitize_for_json({
        "status": "success",
        "total_anomalies_detected": len(anomalies),
        "data": anomalies
    })


@router.get("/impact/{company_id}/{reporting_period}", summary="Research Impact Analysis")
def get_research_impact(company_id: str, reporting_period: str) -> Dict[str, Any]:
    """Evaluates which studies, scorecards, and models require updating for a new period."""
    impact = analyze_research_impact(company_id, reporting_period)
    return sanitize_for_json(impact)
