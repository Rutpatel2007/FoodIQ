from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.core import SourceDocument
from backend.app.schemas.core import DocumentResponse

router = APIRouter()

@router.get("/documents", response_model=List[DocumentResponse])
def get_documents(
    company_id: Optional[str] = Query(None, description="Filter by company ID ('ETERNAL' or 'SWIGGY')"),
    fiscal_year: Optional[str] = Query(None, description="Filter by fiscal year (e.g. 'FY26')"),
    fiscal_quarter: Optional[str] = Query(None, description="Filter by quarter (e.g. 'Q1')"),
    db: Session = Depends(get_db)
):
    query = db.query(SourceDocument)
    if company_id:
        query = query.filter(SourceDocument.company_id == company_id.upper())
    if fiscal_year:
        query = query.filter(SourceDocument.fiscal_year == fiscal_year.upper())
    if fiscal_quarter:
        query = query.filter(SourceDocument.fiscal_quarter == fiscal_quarter.upper())
    return query.order_by(SourceDocument.period_end_date.asc()).all()
