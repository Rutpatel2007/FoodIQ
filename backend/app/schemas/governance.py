"""
Pydantic v2 schemas for Governance & Management entities
"""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class DataQualityFlagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    flag_id: str
    observation_id: Optional[str] = None
    issue_code: str
    severity: str
    issue_description: str
    audit_trail: str
    is_resolved: bool

class DataQualitySummaryResponse(BaseModel):
    total_flags: int
    by_severity: dict
    by_issue_code: dict
    resolved_count: int
    unresolved_count: int

class ComparabilityRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rule_id: str
    metric_a_id: str
    metric_b_id: str
    comparability_tier: str
    adjustment_formula: Optional[str] = None
    prohibited_operations: Optional[str] = None
    methodology_caveats: str

class GuidanceOutcomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    outcome_id: str
    guidance_id: str
    evaluation_quarter: str
    actual_value_numeric: Optional[float] = None
    status: str
    variance_absolute: Optional[float] = None
    variance_percentage: Optional[float] = None
    analyst_commentary: Optional[str] = None

class ManagementGuidanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    guidance_id: str
    company_id: str
    segment_id: Optional[str] = None
    issued_in_quarter: str
    source_page_id: Optional[str] = None
    verbatim_quote: str
    metric_targeted: str
    guidance_type: str
    target_value_numeric: Optional[float] = None
    target_range_low: Optional[float] = None
    target_range_high: Optional[float] = None
    target_deadline_quarter: str
    contingent_conditions: Optional[str] = None
    outcomes: List[GuidanceOutcomeResponse] = []
