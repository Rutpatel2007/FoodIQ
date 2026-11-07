from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.management import ManagementGuidance
from backend.app.schemas.governance import ManagementGuidanceResponse

router = APIRouter()

@router.get("/guidance", response_model=List[ManagementGuidanceResponse])
def get_guidance(
    company_id: Optional[str] = Query(None, description="Filter by company ID ('ETERNAL' or 'SWIGGY')"),
    guidance_type: Optional[str] = Query(None, description="Filter by guidance type"),
    db: Session = Depends(get_db)
):
    query = db.query(ManagementGuidance)
    if company_id:
        query = query.filter(ManagementGuidance.company_id == company_id.upper())
    if guidance_type:
        query = query.filter(ManagementGuidance.guidance_type == guidance_type.upper())
    return query.all()
