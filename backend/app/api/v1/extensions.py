"""
FoodIQ Extensible Architecture & Plugin Registry API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from backend.app.analytics.extension_framework import (
    registry,
    CompanyPlugin,
    MetricDefinitionExtension,
    BusinessSegmentDefinition
)

router = APIRouter(prefix="/extensions", tags=["Extensible Architecture & Plugins"])


class ExtensionInfoResponse(BaseModel):
    total_companies: int
    total_extensible_metrics: int
    total_analytics_modules: int
    companies: List[str]
    modules: List[Dict[str, Any]]


@router.get("/info", response_model=ExtensionInfoResponse)
def get_extension_registry_info():
    """Returns overview of all registered companies, metrics, and pluggable analytical modules."""
    companies = registry.list_companies()
    metrics = registry.list_metrics()
    modules = registry.list_modules()
    return ExtensionInfoResponse(
        total_companies=len(companies),
        total_extensible_metrics=len(metrics),
        total_analytics_modules=len(modules),
        companies=[c.company_id for c in companies],
        modules=modules
    )


@router.get("/companies", response_model=List[CompanyPlugin])
def list_registered_companies():
    """Lists all registered company definitions and their supported business segments."""
    return registry.list_companies()


@router.get("/companies/{company_id}", response_model=CompanyPlugin)
def get_company_plugin(company_id: str):
    """Retrieve details for a specific registered company plugin."""
    c = registry.get_company(company_id.upper())
    if not c:
        raise HTTPException(status_code=404, detail=f"Company plugin '{company_id}' not found")
    return c


@router.post("/companies", response_model=CompanyPlugin)
def register_new_company(company: CompanyPlugin):
    """Register a new company and business segment definition in the FoodIQ ecosystem."""
    registry.register_company(company)
    return company


@router.get("/metrics", response_model=List[MetricDefinitionExtension])
def list_registered_metrics():
    """Lists all extensible metric definitions, formulas, and validation rules."""
    return registry.list_metrics()


@router.post("/metrics", response_model=MetricDefinitionExtension)
def register_new_metric(metric: MetricDefinitionExtension):
    """Register an extensible metric definition with formula and validation bounds."""
    registry.register_metric(metric)
    return metric


@router.get("/modules", response_model=List[Dict[str, Any]])
def list_registered_analytics_modules():
    """Lists all active analytics module plugins and their required metric dependencies."""
    return registry.list_modules()


@router.post("/modules/{module_id}/execute")
def execute_analytics_module(module_id: str, parameters: Optional[Dict[str, Any]] = None):
    """Execute a registered analytical module plugin."""
    mod = registry.get_module(module_id)
    if not mod:
        raise HTTPException(status_code=404, detail=f"Module '{module_id}' not found")
    return mod.execute(session=None, parameters=parameters)
