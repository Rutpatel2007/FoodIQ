from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.governance import ComparabilityRule
from backend.app.schemas.governance import ComparabilityRuleResponse
from backend.app.services.governance_service import ComparabilityGovernanceEngine

router = APIRouter()

class EvaluationRequest(BaseModel):
    metric_a: str
    metric_b: str
    quarter: Optional[str] = None

@router.get("/comparability/rules", response_model=List[ComparabilityRuleResponse])
def get_comparability_rules(
    tier: Optional[str] = Query(None, description="Filter by comparability tier ('DIRECT', 'ADJUSTED', 'DIRECTIONAL', 'INCOMPARABLE')"),
    db: Session = Depends(get_db)
):
    query = db.query(ComparabilityRule)
    if tier:
        query = query.filter(ComparabilityRule.comparability_tier == tier.upper())
    return query.all()

@router.post("/comparability/evaluate")
def evaluate_comparison(payload: EvaluationRequest):
    return ComparabilityGovernanceEngine.evaluate_comparison(
        metric_a=payload.metric_a,
        metric_b=payload.metric_b,
        quarter=payload.quarter
    )
