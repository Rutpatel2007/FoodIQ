"""
Metric definitions, observations, and derived metrics models
"""
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Date, DateTime, Numeric, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base

class MetricDefinition(Base):
    __tablename__ = "metric_definitions"

    metric_id: Mapped[str] = mapped_column(String(64), primary_key=True) # e.g. 'gov_cr', 'nov_cr', 'adj_ebitda_cr'
    canonical_name: Mapped[str] = mapped_column(String(128), nullable=False)
    company_id: Mapped[Optional[str]] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=True, index=True)
    native_term: Mapped[str] = mapped_column(String(128), nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False) # 'INR crore', 'percent', 'million', 'count', 'INR'
    numerator_formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    denominator_formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    segment_scope: Mapped[Optional[str]] = mapped_column(String(64), nullable=True) # 'Food', 'QuickCommerce', 'Consolidated', etc.
    accounting_standard: Mapped[str] = mapped_column(String(64), default="IndAS")
    source_reference_page_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("source_pages.page_id"), nullable=True)
    implementation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    company: Mapped[Optional["Company"]] = relationship("Company", back_populates="metric_definitions")
    observations: Mapped[List["MetricObservation"]] = relationship("MetricObservation", back_populates="metric_def")

class MetricObservation(Base):
    __tablename__ = "metric_observations"

    observation_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False, index=True)
    segment_id: Mapped[str] = mapped_column(String(64), ForeignKey("business_segments.segment_id"), nullable=False, index=True)
    metric_id: Mapped[str] = mapped_column(String(64), ForeignKey("metric_definitions.metric_id"), nullable=False, index=True)
    fiscal_year: Mapped[str] = mapped_column(String(8), nullable=False, index=True) # 'FY25', 'FY26', 'FY27'
    fiscal_quarter: Mapped[str] = mapped_column(String(4), nullable=False, index=True) # 'Q1', 'Q2', 'Q3', 'Q4'
    period_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    value: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True) # Null is preserved!
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    denominator_basis: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    observation_type: Mapped[str] = mapped_column(String(32), default="REPORTED") # REPORTED, DERIVED, MANAGEMENT_ESTIMATE, RESTATED, OCR_VERIFIED
    source_document_id: Mapped[str] = mapped_column(String(64), ForeignKey("source_documents.document_id"), nullable=False, index=True)
    source_page_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("source_pages.page_id"), nullable=True, index=True)
    report_version: Mapped[int] = mapped_column(Integer, default=1)
    validation_status: Mapped[str] = mapped_column(String(32), default="PASSED") # PASSED, WARNING, UNRESOLVED, RESTATED
    raw_source_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verified_value: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True)
    analyst_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("company_id", "segment_id", "metric_id", "fiscal_year", "fiscal_quarter", "report_version", name="uq_metric_obs_version"),
        Index("ix_obs_lookup", "company_id", "segment_id", "fiscal_year", "fiscal_quarter")
    )

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="observations")
    segment: Mapped["BusinessSegment"] = relationship("BusinessSegment", back_populates="observations")
    metric_def: Mapped["MetricDefinition"] = relationship("MetricDefinition", back_populates="observations")
    source_document: Mapped["SourceDocument"] = relationship("SourceDocument", back_populates="observations")
    source_page: Mapped[Optional["SourcePage"]] = relationship("SourcePage", back_populates="observations")
    quality_flags: Mapped[List["DataQualityFlag"]] = relationship("DataQualityFlag", back_populates="observation", cascade="all, delete-orphan")

class DerivedMetric(Base):
    __tablename__ = "derived_metrics"

    derived_metric_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    metric_name: Mapped[str] = mapped_column(String(128), nullable=False)
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False)
    segment_id: Mapped[str] = mapped_column(String(64), ForeignKey("business_segments.segment_id"), nullable=False)
    fiscal_year: Mapped[str] = mapped_column(String(8), nullable=False)
    fiscal_quarter: Mapped[str] = mapped_column(String(4), nullable=False)
    formula: Mapped[str] = mapped_column(Text, nullable=False)
    calculated_value: Mapped[Optional[float]] = mapped_column(Numeric(14, 4), nullable=True)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    assumptions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    calculation_version: Mapped[int] = mapped_column(Integer, default=1)
    input_observation_ids: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # JSON list of input IDs
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
