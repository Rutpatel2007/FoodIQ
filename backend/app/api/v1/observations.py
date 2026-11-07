from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.metrics import MetricObservation
from backend.app.schemas.metrics import MetricObservationResponse, LineageResponse
from backend.app.services.lineage_service import ProvenanceLineageService

router = APIRouter()

@router.get("/observations", response_model=List[MetricObservationResponse])
def get_observations(
    company_id: Optional[str] = Query(None, description="Filter by company ID ('ETERNAL' or 'SWIGGY')"),
    segment_id: Optional[str] = Query(None, description="Filter by segment ID"),
    metric_id: Optional[str] = Query(None, description="Filter by metric ID"),
    fiscal_year: Optional[str] = Query(None, description="Filter by fiscal year (e.g. 'FY26')"),
    fiscal_quarter: Optional[str] = Query(None, description="Filter by quarter (e.g. 'Q1')"),
    limit: int = Query(100, ge=1, le=1000, description="Page limit"),
    offset: int = Query(0, ge=0, description="Page offset"),
    db: Session = Depends(get_db)
):
    query = db.query(MetricObservation)
    if company_id:
        query = query.filter(MetricObservation.company_id == company_id.upper())
    if segment_id:
        query = query.filter(MetricObservation.segment_id == segment_id)
    if metric_id:
        query = query.filter(MetricObservation.metric_id == metric_id)
    if fiscal_year:
        query = query.filter(MetricObservation.fiscal_year == fiscal_year.upper())
    if fiscal_quarter:
        query = query.filter(MetricObservation.fiscal_quarter == fiscal_quarter.upper())

    return query.order_by(MetricObservation.period_end_date.asc()).offset(offset).limit(limit).all()

@router.get("/observations/{observation_id}", response_model=MetricObservationResponse)
def get_observation_by_id(observation_id: str, db: Session = Depends(get_db)):
    obs = db.query(MetricObservation).filter_by(observation_id=observation_id).first()
    if not obs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Observation '{observation_id}' not found")
    return obs

@router.get("/observations/{observation_id}/lineage", response_model=LineageResponse)
def get_observation_lineage(observation_id: str, db: Session = Depends(get_db)):
    lineage = ProvenanceLineageService.get_lineage(db, observation_id)
    if not lineage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Observation '{observation_id}' not found")
    return lineage
