from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.metrics import MetricDefinition
from backend.app.schemas.metrics import MetricDefinitionResponse

router = APIRouter()

@router.get("/metrics", response_model=List[MetricDefinitionResponse])
def get_metrics(
    company_id: Optional[str] = Query(None, description="Filter by company ID ('ETERNAL' or 'SWIGGY')"),
    segment_scope: Optional[str] = Query(None, description="Filter by segment scope"),
    db: Session = Depends(get_db)
):
    query = db.query(MetricDefinition)
    if company_id:
        query = query.filter(MetricDefinition.company_id == company_id.upper())
    if segment_scope:
        query = query.filter(MetricDefinition.segment_scope.ilike(f"%{segment_scope}%"))
    return query.all()
