"""
FoodIQ FastAPI Analytics Router.
Exposes REST endpoints for all financial decomposition engines, margin bridges,
predictive lead-lag statistics, network productivity, scenario models, and guidance scoring.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List, Optional, Any

from backend.app.analytics.repository import sanitize_for_json
from backend.app.analytics.decomposition import compute_waterfall_decomposition, get_all_segment_decompositions
from backend.app.analytics.margin_bridge import compute_margin_bridge, get_all_margin_bridges
from backend.app.analytics.unit_economics import compute_quick_commerce_unit_economics
from backend.app.analytics.network_productivity import compute_network_productivity, compute_network_comparison
from backend.app.analytics.competitive_gaps import compute_competitive_gaps
from backend.app.analytics.leading_indicator import test_aov_leading_indicator
from backend.app.analytics.scenario_model import run_aov_scenario_model
from backend.app.analytics.guidance_scorer import score_management_guidance

router = APIRouter(prefix="/analytics", tags=["Financial Analytics & Decomposition Core"])


@router.get("/decomposition", summary="Price x Volume Waterfall Decomposition")
def get_decomposition(
    company: Optional[str] = Query(None, description="Company name: 'Swiggy' or 'Eternal'"),
    segment: Optional[str] = Query(None, description="Segment name: 'QuickCommerce' or 'Food'"),
    metric_basis: str = Query("gov_cr", description="Metric to decompose: 'gov_cr' or 'nov_cr'")
) -> Dict[str, Any]:
    """
    Computes exact mathematical waterfall decomposition:
    ΔMetric = Volume Effect + Price/AOV Effect + Cross Term (residual).
    """
    if company and segment:
        results = compute_waterfall_decomposition(company=company, segment=segment, metric_basis=metric_basis)
    else:
        results = get_all_segment_decompositions()
        
    return sanitize_for_json({
        "status": "success",
        "total_records": len(results),
        "data": results
    })


@router.get("/margin-bridge", summary="Contribution Margin & Operating Leverage Bridge")
def get_margin_bridge(
    company: Optional[str] = Query(None, description="Company name: 'Swiggy' or 'Eternal'"),
    segment: Optional[str] = Query(None, description="Segment name: 'Food' or 'QuickCommerce'"),
    margin_metric: str = Query("contribution_margin_pct", description="Margin metric: 'contribution_margin_pct' or 'adj_ebitda_margin_pct'")
) -> Dict[str, Any]:
    """
    Decomposes quarter-over-quarter margin changes (in basis points) into:
    - Take Rate Delta (bps)
    - Volume Operating Leverage (bps)
    - Cost Structure / Efficiency Shift (bps)
    """
    if company and segment:
        topline = "nov_cr" if company == "Eternal" else "gov_cr"
        results = compute_margin_bridge(company=company, segment=segment, margin_metric=margin_metric, topline_metric=topline)
    else:
        results = get_all_margin_bridges()
        
    return sanitize_for_json({
        "status": "success",
        "total_records": len(results),
        "data": results
    })


@router.get("/unit-economics", summary="Segment-Matched Per-Order Unit Economics")
def get_unit_economics(
    segment: str = Query("QuickCommerce", description="Segment name")
) -> Dict[str, Any]:
    """
    Returns per-order metrics strictly mapped to segment boundaries:
    - Revenue per order (₹)
    - Contribution per order (₹)
    - Adjusted EBITDA per order (₹)
    - Discount / subsidy per order (₹)
    """
    if segment == "QuickCommerce":
        results = compute_quick_commerce_unit_economics()
    else:
        results = []
        
    return sanitize_for_json({
        "status": "success",
        "segment": segment,
        "total_records": len(results),
        "data": results
    })


@router.get("/network-productivity", summary="Dark Store Network Productivity & Expansion")
def get_network_productivity(
    company: Optional[str] = Query(None, description="Filter by company: 'Eternal' (Blinkit) or 'Swiggy' (Instamart)")
) -> Dict[str, Any]:
    """
    Returns store expansion velocity, average store footprints (sq ft),
    orders/store/day, and throughput per store-day.
    """
    results = compute_network_productivity()
    if company:
        results = [r for r in results if r['company'].lower() == company.lower()]
        
    return sanitize_for_json({
        "status": "success",
        "total_records": len(results),
        "data": results
    })


@router.get("/network-comparison", summary="Blinkit vs Instamart Head-to-Head Comparison")
def get_network_comparison() -> Dict[str, Any]:
    """
    Returns side-by-side comparative table of Blinkit vs Instamart store network expansion.
    """
    results = compute_network_comparison()
    return sanitize_for_json({
        "status": "success",
        "total_records": len(results),
        "data": results
    })


@router.get("/competitive-gaps", summary="Peer Comparison & Competitive Gap Engine")
def get_competitive_gaps(
    segment: Optional[str] = Query(None, description="Filter by segment: 'Food', 'QuickCommerce', 'OutOfHome', 'SupplyChain', 'Platform', 'Consolidated'")
) -> Dict[str, Any]:
    """
    Returns like-for-like quarterly competitive gaps with governance flags.
    Blocks raw GOV vs NOV cross-subtraction and flags Blinkit 1P accounting breaks.
    """
    results = compute_competitive_gaps(segment=segment)
    return sanitize_for_json({
        "status": "success",
        "total_records": len(results),
        "data": results
    })


@router.get("/leading-indicator", summary="AOV Leading Indicator Statistical Hypothesis Test")
def get_leading_indicator(
    company: str = Query("Swiggy", description="Company to test"),
    segment: str = Query("QuickCommerce", description="Segment to test")
) -> Dict[str, Any]:
    """
    Executes Pearson correlation test for Lag-0, Lag-1, and Lag-2 relationships
    between AOV and Contribution Margin with Fisher z-transform 95% CIs and epistemic caveats.
    """
    results = test_aov_leading_indicator(company=company, segment=segment)
    return sanitize_for_json({
        "status": "success",
        "analysis": results
    })


@router.get("/scenario-model", summary="Gap-Closing Scenario & Sensitivity Model")
def get_scenario_model(
    company: str = Query("Swiggy", description="Company name: 'Swiggy' or 'Eternal'"),
    segment: str = Query("QuickCommerce", description="Segment name: 'QuickCommerce' or 'Food'"),
    elasticity_bps_per_inr: Optional[float] = Query(None, description="Custom CM expansion (bps) per ₹1 AOV increase"),
    tier: Optional[str] = Query("baseline", description="Sensitivity tier: 'conservative', 'baseline', or 'upper'")
) -> Dict[str, Any]:
    """
    Simulates AOV improvement steps (+₹20, +₹40, +₹60, +₹80, +₹100) and calculates
    projected margins, remaining gap (bps), and estimated quarters to parity.
    Strictly separates Quick Commerce empirical OLS from Food Delivery assumptions.
    """
    results = run_aov_scenario_model(
        company=company,
        segment=segment,
        elasticity_bps_per_inr=elasticity_bps_per_inr,
        tier=tier
    )
    return sanitize_for_json({
        "status": "success",
        "model": results
    })


@router.get("/guidance-scorecard", summary="Management Guidance Credibility Scorecard")
def get_guidance_scorecard() -> Dict[str, Any]:
    """
    Evaluates management forward guidance commitments against retrospective disclosures,
    calculating delivery rate % and credibility tier.
    """
    results = score_management_guidance()
    return sanitize_for_json({
        "status": "success",
        "scorecard": results
    })
