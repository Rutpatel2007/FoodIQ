"""
FoodIQ Management Credibility & Narrative Verification API Router (Phase 4).
Exposes endpoints for management statements, commitment tracking, execution scorecards,
narrative evidence verification, and strategic initiative monitoring.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Query, HTTPException

from backend.app.analytics.credibility_engine import (
    get_all_management_statements,
    get_commitment_by_id,
    calculate_management_credibility_scorecard,
    get_all_narrative_verifications,
    get_all_strategic_initiatives,
    get_company_credibility_comparison,
    STATEMENT_CATEGORIES
)
from backend.app.analytics.repository import sanitize_for_json

router = APIRouter(prefix="/credibility", tags=["Management Credibility"])


@router.get("/statements", response_model=Dict[str, Any])
def list_management_statements(
    company: Optional[str] = Query(None, description="Filter by company: 'Eternal' or 'Swiggy'"),
    category: Optional[str] = Query(None, description="Filter by statement category")
):
    """Retrieves the master repository of management statements with source citations."""
    statements = get_all_management_statements(company=company, category=category)
    return sanitize_for_json({
        "status": "success",
        "total": len(statements),
        "company_filter": company,
        "category_filter": category,
        "categories_available": STATEMENT_CATEGORIES,
        "statements": statements
    })


@router.get("/commitments", response_model=Dict[str, Any])
def list_commitments(
    company: Optional[str] = Query(None, description="Filter by company"),
    segment: Optional[str] = Query(None, description="Filter by segment"),
    status: Optional[str] = Query(None, description="Filter by outcome status: DELIVERED, PENDING, etc.")
):
    """Retrieves tracked management commitments across their full lifecycle."""
    commitments = get_all_management_statements(company=company)
    if segment:
        commitments = [c for c in commitments if c['segment'].lower() == segment.lower()]
    if status:
        commitments = [c for c in commitments if c['outcome_status'].upper() == status.upper()]
        
    return sanitize_for_json({
        "status": "success",
        "total": len(commitments),
        "commitments": commitments
    })


@router.get("/commitments/{commitment_id}", response_model=Dict[str, Any])
def get_commitment(commitment_id: str):
    """Retrieves detailed tracking and evidence for a specific commitment."""
    c = get_commitment_by_id(commitment_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Commitment '{commitment_id}' not found.")
    return sanitize_for_json({
        "status": "success",
        "commitment": c
    })


@router.get("/scorecard", response_model=Dict[str, Any])
def get_credibility_scorecard(
    company: Optional[str] = Query(None, description="Filter by company ('Eternal', 'Swiggy', or all)")
):
    """Calculates management guidance delivery scorecards with transparent denominators."""
    scorecard = calculate_management_credibility_scorecard(company=company)
    return sanitize_for_json({
        "status": "success",
        "scorecard": scorecard
    })


@router.get("/narratives", response_model=Dict[str, Any])
def list_narrative_verifications(
    company: Optional[str] = Query(None, description="Filter by company")
):
    """Evaluates qualitative management explanations against retrospective empirical evidence."""
    narratives = get_all_narrative_verifications(company=company)
    return sanitize_for_json({
        "status": "success",
        "total": len(narratives),
        "narratives": narratives
    })


@router.get("/initiatives", response_model=Dict[str, Any])
def list_strategic_initiatives(
    company: Optional[str] = Query(None, description="Filter by company"),
    segment: Optional[str] = Query(None, description="Filter by segment")
):
    """Monitors corporate strategic initiatives across operational and financial dimensions."""
    initiatives = get_all_strategic_initiatives(company=company, segment=segment)
    return sanitize_for_json({
        "status": "success",
        "total": len(initiatives),
        "initiatives": initiatives
    })


@router.get("/comparison", response_model=Dict[str, Any])
def get_credibility_comparison():
    """Provides a comparative credibility and execution benchmark between Eternal and Swiggy."""
    comp = get_company_credibility_comparison()
    return sanitize_for_json({
        "status": "success",
        "comparison": comp
    })
