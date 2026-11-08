"""
FoodIQ FastAPI Institutional Research Reports Router (Phase 7).
Exposes REST endpoints for:
- 9 Supported Report Types
- Report Generation & Automated Verification
- Report Catalog & Historical Retrieval
- Multi-Format Exports: HTML, PDF, DOCX, CSV
- Citation Auditing & Lineage Verification
"""

import os
from fastapi import APIRouter, Query, HTTPException, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

from backend.app.analytics.repository import sanitize_for_json
from backend.app.analytics.report_engine import (
    REPORT_TYPES,
    generate_institutional_report,
    list_generated_reports,
    get_generated_report_by_id,
    export_report_to_html,
    export_report_to_pdf,
    export_report_to_docx,
    export_report_to_csv,
    verify_complete_report
)

router = APIRouter(prefix="/reports", tags=["Institutional Research Report Generation"])


class GenerateReportRequest(BaseModel):
    report_type: str = Field("COMPREHENSIVE", description="Report type code")
    company: Optional[str] = Field(None, description="Optional company filter ('Eternal' or 'Swiggy')")
    segment: Optional[str] = Field(None, description="Optional segment filter ('Food', 'QuickCommerce')")
    period_cutoff: str = Field("Q2FY27", description="Reporting period cutoff")
    included_sections: Optional[List[str]] = Field(None, description="Optional list of specific section IDs to include")
    author: str = Field("Institutional Research Analyst", description="Author attribution")


@router.get("/types", summary="Supported Institutional Report Types")
def get_report_types() -> Dict[str, Any]:
    """Returns catalog of all 9 institutional research report types."""
    return sanitize_for_json({
        "status": "success",
        "total_types": len(REPORT_TYPES),
        "data": REPORT_TYPES,
        "types": REPORT_TYPES
    })


@router.post("/generate", summary="Generate Institutional Research Report")
def generate_report(req: GenerateReportRequest) -> Dict[str, Any]:
    """Generates a complete, verified research report from live database records."""
    report = generate_institutional_report(
        report_type=req.report_type,
        company=req.company,
        segment=req.segment,
        period_cutoff=req.period_cutoff,
        included_sections=req.included_sections,
        author=req.author
    )
    return sanitize_for_json({
        "status": "success",
        "report_id": report["report_id"],
        "verification_status": report["verification_status"],
        "data": report,
        "report": report
    })


@router.get("/list", summary="List Generated Historical Reports")
def list_reports() -> Dict[str, Any]:
    """Lists saved historical reports for auditability and reproducibility."""
    reports = list_generated_reports()
    return sanitize_for_json({
        "status": "success",
        "total_reports": len(reports),
        "data": reports,
        "reports": reports
    })


@router.get("/{report_id}", summary="Get Full Report JSON")
def get_report(report_id: str) -> Dict[str, Any]:
    """Retrieves full JSON structure of a specific saved report."""
    report = get_generated_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")
    return sanitize_for_json({
        "status": "success",
        "data": report,
        "report": report
    })


@router.post("/{report_id}/verify", summary="Run Automated Report Verification Audit")
def verify_report(report_id: str) -> Dict[str, Any]:
    """Runs automated institutional financial and citation checks on a report."""
    report = get_generated_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")
    scorecard = verify_complete_report(report)
    return sanitize_for_json({
        "status": "success",
        "report_id": report_id,
        "verification_status": scorecard["status"],
        "scorecard": scorecard
    })


@router.get("/{report_id}/citations", summary="Get Report Citation Lineage Audit")
def get_report_citations(report_id: str) -> Dict[str, Any]:
    """Retrieves source citations and physical page verification audit for a report."""
    report = get_generated_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")
    return sanitize_for_json({
        "status": "success",
        "report_id": report_id,
        "citation_verification": report.get("citation_verification", {})
    })


@router.get("/{report_id}/export/{export_format}", summary="Export Report in HTML, PDF, DOCX, or CSV")
def export_report(report_id: str, export_format: str):
    """Compiles and downloads the report in the requested file format."""
    # Path traversal protection
    if ".." in report_id or "/" in report_id or "\\" in report_id:
        raise HTTPException(status_code=400, detail="Invalid report_id format.")

    report = get_generated_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")
        
    export_dir = os.path.abspath("data/reports/exports")
    os.makedirs(export_dir, exist_ok=True)
    
    fmt = export_format.lower()
    if fmt == "html":
        out_path = os.path.join(export_dir, f"{report_id}.html")
        export_report_to_html(report, out_path)
        return FileResponse(out_path, media_type="text/html", filename=f"{report_id}.html")
    elif fmt == "pdf":
        out_path = os.path.join(export_dir, f"{report_id}.pdf")
        export_report_to_pdf(report, out_path)
        return FileResponse(out_path, media_type="application/pdf", filename=f"{report_id}.pdf")
    elif fmt == "docx":
        out_path = os.path.join(export_dir, f"{report_id}.docx")
        export_report_to_docx(report, out_path)
        return FileResponse(out_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=f"{report_id}.docx")
    elif fmt == "csv":
        out_path = os.path.join(export_dir, f"{report_id}.csv")
        export_report_to_csv(report, out_path)
        return FileResponse(out_path, media_type="text/csv", filename=f"{report_id}.csv")
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format '{export_format}'. Use html, pdf, docx, or csv.")
