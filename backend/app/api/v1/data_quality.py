from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.models.governance import DataQualityFlag
from backend.app.schemas.governance import DataQualityFlagResponse, DataQualitySummaryResponse

router = APIRouter()

@router.get("/data-quality/summary", response_model=DataQualitySummaryResponse)
def get_data_quality_summary(db: Session = Depends(get_db)):
    total = db.query(DataQualityFlag).count()
    
    # Severity counts
    sev_counts = dict(
        db.query(DataQualityFlag.severity, func.count(DataQualityFlag.flag_id))
        .group_by(DataQualityFlag.severity).all()
    )

    # Issue code counts
    code_counts = dict(
        db.query(DataQualityFlag.issue_code, func.count(DataQualityFlag.flag_id))
        .group_by(DataQualityFlag.issue_code).all()
    )

    resolved = db.query(DataQualityFlag).filter(DataQualityFlag.is_resolved == True).count()
    unresolved = total - resolved

    return {
        "total_flags": total,
        "by_severity": sev_counts,
        "by_issue_code": code_counts,
        "resolved_count": resolved,
        "unresolved_count": unresolved
    }

@router.get("/data-quality/issues", response_model=List[DataQualityFlagResponse])
def get_data_quality_issues(
    severity: Optional[str] = Query(None, description="Filter by severity ('CRITICAL', 'HIGH', 'MEDIUM', 'INFO')"),
    is_resolved: Optional[bool] = Query(None, description="Filter by resolution status"),
    db: Session = Depends(get_db)
):
    query = db.query(DataQualityFlag)
    if severity:
        query = query.filter(DataQualityFlag.severity == severity.upper())
    if is_resolved is not None:
        query = query.filter(DataQualityFlag.is_resolved == is_resolved)
    return query.all()
