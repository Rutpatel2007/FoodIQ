"""
Governance entities: Comparability rules, Data Quality flags, Source Conflicts, Corporate Events
"""
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Date, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base

class ComparabilityRule(Base):
    __tablename__ = "comparability_rules"

    rule_id: Mapped[str] = mapped_column(String(64), primary_key=True) # e.g. 'RULE-FOOD-GOV-NOV'
    metric_a_id: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. 'swiggy_food_gov'
    metric_b_id: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. 'eternal_food_nov'
    comparability_tier: Mapped[str] = mapped_column(String(32), nullable=False) # 'DIRECT', 'ADJUSTED', 'DIRECTIONAL', 'INCOMPARABLE'
    adjustment_formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prohibited_operations: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # e.g. "Direct absolute subtraction prohibited"
    methodology_caveats: Mapped[str] = mapped_column(Text, nullable=False)

class DataQualityFlag(Base):
    __tablename__ = "data_quality_flags"

    flag_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    observation_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("metric_observations.observation_id"), nullable=True, index=True)
    issue_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True) # e.g. 'RESTATED_WITHOUT_NOTE', 'OCR_UNCERTAIN', 'SCOPE_MISMATCH'
    severity: Mapped[str] = mapped_column(String(16), nullable=False, index=True) # 'CRITICAL', 'HIGH', 'MEDIUM', 'INFO'
    issue_description: Mapped[str] = mapped_column(Text, nullable=False)
    audit_trail: Mapped[str] = mapped_column(Text, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    observation: Mapped[Optional["MetricObservation"]] = relationship("MetricObservation", back_populates="quality_flags")

class SourceConflict(Base):
    __tablename__ = "source_conflicts"

    conflict_id: Mapped[str] = mapped_column(String(64), primary_key=True) # e.g. 'SC-001'
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(128), nullable=False)
    quarter: Mapped[str] = mapped_column(String(16), nullable=False)
    value_a: Mapped[str] = mapped_column(String(128), nullable=False)
    source_a: Mapped[str] = mapped_column(String(255), nullable=False)
    page_a: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    value_b: Mapped[str] = mapped_column(String(128), nullable=False)
    source_b: Mapped[str] = mapped_column(String(255), nullable=False)
    page_b: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    resolution_strategy: Mapped[Optional[str]] = mapped_column(String(64), default="PRESERVE_BOTH")
    reconciliation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class CorporateEvent(Base):
    __tablename__ = "corporate_events"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False, index=True)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    quarter_impacted: Mapped[str] = mapped_column(String(16), nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False) # '1P_INVENTORY_TRANSITION', 'M_AND_A', 'DIVESTMENT', 'REPORTING_RECLASSIFICATION'
    headline: Mapped[str] = mapped_column(String(255), nullable=False)
    detailed_economic_impact: Mapped[str] = mapped_column(Text, nullable=False)
    affected_segments: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_metrics: Mapped[str] = mapped_column(String(255), nullable=False)
    source_page_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("source_pages.page_id"), nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="corporate_events")
