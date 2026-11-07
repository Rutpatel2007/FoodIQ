"""
Management entities: Guidance, Outcomes, Commentary, Strategic Initiatives
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base

class ManagementGuidance(Base):
    __tablename__ = "management_guidance"

    guidance_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False, index=True)
    segment_id: Mapped[Optional[str]] = mapped_column(String(64), ForeignKey("business_segments.segment_id"), nullable=True)
    issued_in_quarter: Mapped[str] = mapped_column(String(16), nullable=False) # e.g. 'Q1FY26'
    source_page_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("source_pages.page_id"), nullable=True)
    verbatim_quote: Mapped[str] = mapped_column(Text, nullable=False)
    metric_targeted: Mapped[str] = mapped_column(String(128), nullable=False)
    guidance_type: Mapped[str] = mapped_column(String(32), nullable=False) # 'EXACT_VALUE', 'NUMERICAL_RANGE', 'BREAK_EVEN', 'QUALITATIVE'
    target_value_numeric: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True)
    target_range_low: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True)
    target_range_high: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True)
    target_deadline_quarter: Mapped[str] = mapped_column(String(16), nullable=False) # e.g. 'Q1FY27'
    contingent_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="guidance")
    outcomes: Mapped[List["GuidanceOutcome"]] = relationship("GuidanceOutcome", back_populates="guidance", cascade="all, delete-orphan")

class GuidanceOutcome(Base):
    __tablename__ = "guidance_outcomes"

    outcome_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    guidance_id: Mapped[str] = mapped_column(String(64), ForeignKey("management_guidance.guidance_id"), nullable=False, index=True)
    evaluation_quarter: Mapped[str] = mapped_column(String(16), nullable=False)
    actual_value_numeric: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False) # 'ACHIEVED', 'MISSED', 'PARTIALLY_ACHIEVED', 'PENDING', 'SUPERSEDED', 'NOT_EVALUABLE'
    variance_absolute: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True)
    variance_percentage: Mapped[Optional[float]] = mapped_column(Numeric(8, 4), nullable=True)
    evidence_observation_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("metric_observations.observation_id"), nullable=True)
    analyst_commentary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    guidance: Mapped["ManagementGuidance"] = relationship("ManagementGuidance", back_populates="outcomes")

class ManagementCommentary(Base):
    __tablename__ = "management_commentary"

    commentary_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False, index=True)
    quarter: Mapped[str] = mapped_column(String(16), nullable=False)
    segment_id: Mapped[Optional[str]] = mapped_column(String(64), ForeignKey("business_segments.segment_id"), nullable=True)
    speaker: Mapped[Optional[str]] = mapped_column(String(128), nullable=True) # e.g. 'Sriharsha Majety (CEO)', 'Deepinder Goyal (CEO)'
    quotation: Mapped[str] = mapped_column(Text, nullable=False)
    topic: Mapped[str] = mapped_column(String(128), nullable=False) # e.g. 'monetization', 'store_expansion', 'operating_leverage'
    statement_type: Mapped[str] = mapped_column(String(32), nullable=False) # 'HISTORICAL', 'EXPLANATORY', 'FORWARD_LOOKING', 'STRATEGIC'
    source_page_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("source_pages.page_id"), nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="commentary")

class StrategicInitiative(Base):
    __tablename__ = "strategic_initiatives"

    initiative_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False, index=True)
    segment_id: Mapped[Optional[str]] = mapped_column(String(64), ForeignKey("business_segments.segment_id"), nullable=True)
    initiative_name: Mapped[str] = mapped_column(String(128), nullable=False)
    launch_period: Mapped[str] = mapped_column(String(16), nullable=False) # e.g. 'Q2FY26'
    initiative_type: Mapped[str] = mapped_column(String(64), nullable=False) # 'SPEED', 'SUBSCRIPTION', 'ASSORTMENT', 'FORMAT'
    stated_objective: Mapped[str] = mapped_column(Text, nullable=False)
    economic_mechanism: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status_as_of_latest: Mapped[str] = mapped_column(String(64), nullable=False) # 'SCALING', 'MATURE', 'DISCONTINUED', 'PILOT'
    analytical_risks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_page_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("source_pages.page_id"), nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="strategic_initiatives")
