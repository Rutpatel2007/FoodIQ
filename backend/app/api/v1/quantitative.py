"""
FoodIQ Quantitative Research & Statistical API Router (Phase 5).
Exposes endpoints for growth and trend diagnostics, econometric relationship studies,
Benjamini-Hochberg FDR correction, and the Research Question Workbench.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Query, HTTPException

from backend.app.analytics.statistical_research import (
    compute_metric_growth_and_trends,
    run_statistical_relationship_analysis,
    get_all_relationship_studies_with_fdr,
    get_all_research_workbench_questions,
    get_research_question_by_id,
    RELATIONSHIP_STUDIES
)
from backend.app.analytics.repository import sanitize_for_json

router = APIRouter(prefix="/quantitative", tags=["Quantitative Research & Statistics"])


@router.get("/growth-trends", response_model=Dict[str, Any])
def get_metric_growth_trends(
    company: str = Query(..., description="Company: 'Eternal' or 'Swiggy'"),
    segment: str = Query(..., description="Segment: 'Food', 'QuickCommerce', 'OutOfHome', 'SupplyChain'"),
    metric: str = Query(..., description="Metric code: 'gov_cr', 'nov_cr', 'aov_inr', 'dark_stores', etc.")
):
    """Computes time-series growth rates (QoQ, YoY), rolling averages, acceleration, and volatility."""
    res = compute_metric_growth_and_trends(company=company, segment=segment, metric_code=metric)
    if res.get('status') == 'NO_DATA':
        raise HTTPException(status_code=404, detail=f"No data for {company} {segment}")
    return sanitize_for_json(res)


@router.get("/relationships", response_model=Dict[str, Any])
def list_relationship_studies():
    """Lists all 12 core econometric relationship studies with Benjamini-Hochberg FDR correction."""
    studies = get_all_relationship_studies_with_fdr()
    return sanitize_for_json({
        "status": "success",
        "total_studies": len(studies),
        "fdr_q_threshold": 0.05,
        "studies": studies
    })


@router.get("/relationships/{study_id}", response_model=Dict[str, Any])
def get_relationship_study(study_id: str):
    """Retrieves deep econometric study for a specific relationship (Pearson r, 95% CI, p-value, detrending, lag-1)."""
    study = run_statistical_relationship_analysis(study_id=study_id)
    if study.get('status') == 'STUDY_NOT_FOUND':
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found.")
    return sanitize_for_json(study)


@router.get("/workbench", response_model=Dict[str, Any])
def list_workbench_questions():
    """Retrieves the 8 institutional research questions evaluated with statistical evidence."""
    questions = get_all_research_workbench_questions()
    return sanitize_for_json({
        "status": "success",
        "total_questions": len(questions),
        "questions": questions
    })


@router.get("/workbench/{question_id}", response_model=Dict[str, Any])
def get_workbench_question(question_id: str):
    """Retrieves detailed analysis, metrics, and evidence for a single research question."""
    q = get_research_question_by_id(question_id)
    if not q:
        raise HTTPException(status_code=404, detail=f"Research question '{question_id}' not found.")
    return sanitize_for_json({
        "status": "success",
        "question": q
    })
