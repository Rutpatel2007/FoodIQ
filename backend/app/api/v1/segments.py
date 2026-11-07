from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.core import BusinessSegment
from backend.app.schemas.core import SegmentResponse

router = APIRouter()

@router.get("/segments", response_model=List[SegmentResponse])
def get_segments(
    company_id: Optional[str] = Query(None, description="Filter by company ID ('ETERNAL' or 'SWIGGY')"),
    db: Session = Depends(get_db)
):
    query = db.query(BusinessSegment)
    if company_id:
        query = query.filter(BusinessSegment.company_id == company_id.upper())
    return query.all()
