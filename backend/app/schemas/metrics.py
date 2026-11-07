"""
Pydantic v2 schemas for Metrics & Observations
"""
from datetime import date, datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict

class MetricDefinitionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metric_id: str
    canonical_name: str
    company_id: Optional[str] = None
    native_term: str
    unit: str
    denominator_formula: Optional[str] = None
    segment_scope: Optional[str] = None
    accounting_standard: str
    source_reference_page_id: Optional[str] = None
    implementation_notes: Optional[str] = None

class MetricObservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    observation_id: str
    company_id: str
    segment_id: str
    metric_id: str
    fiscal_year: str
    fiscal_quarter: str
    period_end_date: date
    value: Optional[float] = None
    unit: str
    denominator_basis: Optional[str] = None
    observation_type: str
    source_document_id: str
    source_page_id: Optional[str] = None
    report_version: int
    validation_status: str
    raw_source_value: Optional[str] = None
    verified_value: Optional[float] = None
    analyst_notes: Optional[str] = None

class LineageResponse(BaseModel):
    observation_id: str
    company: Dict[str, Any]
    segment: Dict[str, Any]
    metric: Dict[str, Any]
    time_period: Dict[str, Any]
    provenance: Dict[str, Any]
    quality_flags: List[Dict[str, Any]]
    analyst_notes: Optional[str] = None
    created_at: Optional[str] = None
