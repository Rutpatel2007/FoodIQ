from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.core import Company
from backend.app.schemas.core import CompanyResponse

router = APIRouter()

@router.get("/companies", response_model=List[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()
