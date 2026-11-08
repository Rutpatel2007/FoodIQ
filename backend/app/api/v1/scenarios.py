"""
FoodIQ Scenario Lab & Simulation API Router (Phase 5).
Exposes endpoints for running segment scenario projections, sensitivity matrices,
break-even threshold analysis, Monte Carlo simulation, and scenario persistence.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Query, HTTPException, Body
from pydantic import BaseModel, Field

from backend.app.analytics.scenario_lab import (
    run_segment_scenario_simulation,
    compute_two_variable_sensitivity_matrix,
    compute_breakeven_analysis,
    run_monte_carlo_simulation,
    save_scenario_to_storage,
    list_saved_scenarios,
    get_saved_scenario_by_id
)
from backend.app.analytics.repository import sanitize_for_json

router = APIRouter(prefix="/scenarios", tags=["Scenario Lab & Simulation"])


class RunScenarioRequest(BaseModel):
    company: str
    segment: str
    scenario_type: str = "BASE"
    forecast_quarters: int = 4
    custom_assumptions: Optional[Dict[str, Any]] = None


class SaveScenarioRequest(BaseModel):
    scenario_name: str
    company: str
    segment: str
    scenario_type: str
    assumptions: Dict[str, Any]
    outputs: Dict[str, Any]
    author: str = "Research Analyst"
    notes: Optional[str] = None


@router.post("/run", response_model=Dict[str, Any])
def run_scenario(req: RunScenarioRequest):
    """Executes a scenario simulation starting from the latest reported baseline."""
    res = run_segment_scenario_simulation(
        company=req.company,
        segment=req.segment,
        scenario_type=req.scenario_type,
        forecast_quarters=req.forecast_quarters,
        custom_assumptions=req.custom_assumptions
    )
    if res.get('status') == 'ERROR':
        raise HTTPException(status_code=400, detail=res.get('message'))
    return sanitize_for_json(res)


@router.get("/sensitivity", response_model=Dict[str, Any])
def get_sensitivity_matrix(
    company: str = Query(..., description="Company: 'Eternal' or 'Swiggy'"),
    segment: str = Query(..., description="Segment: 'Food', 'QuickCommerce'"),
    var_x: str = Query("aov_change_pct", description="X variable"),
    var_y: str = Query("growth_rate_pct", description="Y variable")
):
    """Generates a 2-variable sensitivity grid for interactive heatmaps."""
    matrix = compute_two_variable_sensitivity_matrix(company=company, segment=segment, var_x=var_x, var_y=var_y)
    return sanitize_for_json(matrix)


@router.get("/breakeven", response_model=Dict[str, Any])
def get_breakeven_analysis(
    company: str = Query(..., description="Company: 'Eternal' or 'Swiggy'"),
    segment: str = Query(..., description="Segment: 'Food', 'QuickCommerce'")
):
    """Computes break-even thresholds (AOV or throughput needed for 0.0% CM/EBITDA)."""
    be = compute_breakeven_analysis(company=company, segment=segment)
    return sanitize_for_json(be)


@router.get("/monte-carlo", response_model=Dict[str, Any])
def get_monte_carlo(
    company: str = Query(..., description="Company: 'Eternal' or 'Swiggy'"),
    segment: str = Query(..., description="Segment: 'Food', 'QuickCommerce'"),
    iterations: int = Query(1000, description="Iterations (default 1,000)")
):
    """Executes a bounded Monte Carlo risk simulation."""
    mc = run_monte_carlo_simulation(company=company, segment=segment, iterations=iterations)
    return sanitize_for_json(mc)


@router.post("/save", response_model=Dict[str, Any])
def save_scenario(req: SaveScenarioRequest):
    """Persists a scenario simulation to SQLite storage."""
    scen_id = save_scenario_to_storage(
        scenario_name=req.scenario_name,
        company=req.company,
        segment=req.segment,
        scenario_type=req.scenario_type,
        assumptions=req.assumptions,
        outputs=req.outputs,
        author=req.author,
        notes=req.notes
    )
    return sanitize_for_json({
        "status": "success",
        "scenario_id": scen_id,
        "message": f"Scenario saved successfully as '{scen_id}'."
    })


@router.get("/saved", response_model=Dict[str, Any])
def list_scenarios():
    """Lists all persistently saved scenarios."""
    scenarios = list_saved_scenarios()
    return sanitize_for_json({
        "status": "success",
        "total": len(scenarios),
        "scenarios": scenarios
    })


@router.get("/saved/{scenario_id}", response_model=Dict[str, Any])
def get_scenario(scenario_id: str):
    """Retrieves full details of a saved scenario."""
    scen = get_saved_scenario_by_id(scenario_id)
    if not scen:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")
    return sanitize_for_json({
        "status": "success",
        "scenario": scen
    })
