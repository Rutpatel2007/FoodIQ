"""
FoodIQ FastAPI Competitive Intelligence & Structural Break Router (Phase 3).
Exposes REST endpoints for:
- 4-Tier Comparability Rules
- Metric Reconciliation & Availability Matrix
- Multi-Dimensional Competitive Gap Attribution
- Structural Break Event Register & Deep Analyses
- Evidence-Backed Research Findings
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List, Optional, Any

from backend.app.analytics.repository import sanitize_for_json
from backend.app.analytics.comparability_engine import get_all_comparability_rules, get_comparability_rule
from backend.app.analytics.metric_reconciliation import build_metric_availability_matrix
from backend.app.analytics.structural_breaks import (
    get_all_structural_breaks,
    get_structural_breaks_for_query,
    analyze_blinkit_1p_transition,
    analyze_district_and_lynks_events
)
from backend.app.analytics.competitive_attribution import compute_comprehensive_competitive_gaps
from backend.app.analytics.competitive_findings import get_all_competitive_findings, get_finding_by_id

router = APIRouter(prefix="/competitive", tags=["Competitive Intelligence & Structural Break Engine"])


@router.get("/comparability", summary="Master 4-Tier Comparability Rules")
def get_comparability_rules(
    segment: Optional[str] = Query(None, description="Filter rules by segment (e.g. 'Food', 'QuickCommerce')")
) -> Dict[str, Any]:
    """
    Returns the formal 4-tier comparability governance rules:
    LEVEL 1 (Directly Comparable), LEVEL 2 (Comparable with Adjustment),
    LEVEL 3 (Directionally Comparable), and LEVEL 4 (Incomparable / Blocked).
    """
    rules = get_all_comparability_rules()
    if segment:
        rules = [r for r in rules if r['segment'].lower() == segment.lower()]
        
    return sanitize_for_json({
        "status": "success",
        "total_rules": len(rules),
        "data": rules,
        "rules": rules
    })


@router.get("/metric-matrix", summary="Company Metric Reconciliation & Availability Matrix")
def get_metric_availability_matrix() -> Dict[str, Any]:
    """
    Returns the quarterly disclosure availability matrix across all segments and metrics,
    tracking whether each metric is disclosed for Eternal, Swiggy, both, or neither.
    """
    matrix = build_metric_availability_matrix()
    return sanitize_for_json({
        "status": "success",
        "total_metrics_mapped": len(matrix),
        "data": matrix
    })


@router.get("/gaps", summary="Multi-Dimensional Competitive Gap Attribution")
def get_competitive_gaps(
    segment: Optional[str] = Query(None, description="Segment filter: 'Food', 'QuickCommerce', 'OutOfHome', 'SupplyChain'")
) -> Dict[str, Any]:
    """
    Computes side-by-side quarterly competitive comparisons across 8 dimensions
    (scale, growth, monetisation, unit economics, profitability, network productivity, customer engagement, capital efficiency).
    Blocks raw Level 4 subtractions (e.g., Blinkit 1P revenue vs Swiggy 3P marketplace).
    """
    gaps = compute_comprehensive_competitive_gaps(segment=segment)
    return sanitize_for_json({
        "status": "success",
        "total_gap_records": len(gaps),
        "data": gaps,
        "gaps": gaps
    })


@router.get("/events", summary="Corporate Structural-Break Event Register")
def get_corporate_events(
    company: Optional[str] = Query(None, description="Company filter: 'Eternal' or 'Swiggy'"),
    segment: Optional[str] = Query(None, description="Segment filter")
) -> Dict[str, Any]:
    """
    Returns documented structural business changes:
    - Blinkit 1P inventory model transition (Q2 FY26)
    - Eternal District ticketing acquisition (Q2 FY25)
    - Swiggy Lynks divestment and supply chain deconsolidation (Q2 FY27)
    - Swiggy Dineout segment carve-out (Q1 FY26)
    """
    events = get_structural_breaks_for_query(company=company, segment=segment)
    return sanitize_for_json({
        "status": "success",
        "total_events": len(events),
        "data": events
    })


@router.get("/structural-breaks", summary="Deep Structural Break Financial Analysis")
def get_structural_breaks_analysis(
    topic: str = Query("blinkit_1p", description="Topic: 'blinkit_1p' or 'm_and_a_divestment'")
) -> Dict[str, Any]:
    """
    Returns deep financial analyses of structural breaks:
    - 'blinkit_1p': 4-series breakdown of Blinkit inventory ownership transition.
    - 'm_and_a_divestment': District acquisition organic vs reported growth and Lynks divestment scope.
    """
    if topic == "blinkit_1p":
        data = analyze_blinkit_1p_transition()
    else:
        data = analyze_district_and_lynks_events()
        
    return sanitize_for_json({
        "status": "success",
        "topic": topic,
        "analysis": data
    })


@router.get("/findings", summary="Evidence-Backed Competitive Intelligence Findings")
def get_competitive_findings(
    finding_id: Optional[str] = Query(None, description="Specific finding ID (e.g. 'FINDING-001')")
) -> Dict[str, Any]:
    """
    Returns analytical findings answering the 8 core research questions,
    categorized by epistemic evidence tiers (REPORTED FACT, DERIVED FACT, MANAGEMENT EXPLANATION, etc.).
    """
    if finding_id:
        f = get_finding_by_id(finding_id)
        if not f:
            raise HTTPException(status_code=404, detail=f"Finding {finding_id} not found.")
        return sanitize_for_json({"status": "success", "data": f})
        
    findings = get_all_competitive_findings()
    return sanitize_for_json({
        "status": "success",
        "total_findings": len(findings),
        "data": findings,
        "findings": findings
    })


@router.get("/findings/{finding_id}", summary="Evidence-Backed Competitive Finding by ID")
def get_competitive_finding_by_id(finding_id: str) -> Dict[str, Any]:
    """Returns a specific research finding by ID."""
    f = get_finding_by_id(finding_id)
    if not f:
        raise HTTPException(status_code=404, detail=f"Finding {finding_id} not found.")
    return sanitize_for_json({"status": "success", "data": f, "finding": f})
