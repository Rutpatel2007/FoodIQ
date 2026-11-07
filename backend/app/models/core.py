"""
Core entities: Companies, Source Documents, Source Pages, Business Segments, Ingestion Runs
"""
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import String, Integer, Date, DateTime, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base

class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="RUNNING") # RUNNING, COMPLETED, FAILED
    company_scope: Mapped[str] = mapped_column(String(32)) # 'SWIGGY', 'ETERNAL', 'ALL'
    total_documents: Mapped[int] = mapped_column(Integer, default=0)
    total_pages: Mapped[int] = mapped_column(Integer, default=0)
    total_observations: Mapped[int] = mapped_column(Integer, default=0)
    total_flags: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class Company(Base):
    __tablename__ = "companies"

    company_id: Mapped[str] = mapped_column(String(32), primary_key=True) # 'ETERNAL', 'SWIGGY'
    canonical_name: Mapped[str] = mapped_column(String(128), nullable=False)
    ticker_symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    incorporation_jurisdiction: Mapped[str] = mapped_column(String(64), default="India")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    documents: Mapped[List["SourceDocument"]] = relationship("SourceDocument", back_populates="company", cascade="all, delete-orphan")
    segments: Mapped[List["BusinessSegment"]] = relationship("BusinessSegment", back_populates="company", cascade="all, delete-orphan")
    metric_definitions: Mapped[List["MetricDefinition"]] = relationship("MetricDefinition", back_populates="company")
    observations: Mapped[List["MetricObservation"]] = relationship("MetricObservation", back_populates="company")
    guidance: Mapped[List["ManagementGuidance"]] = relationship("ManagementGuidance", back_populates="company")
    commentary: Mapped[List["ManagementCommentary"]] = relationship("ManagementCommentary", back_populates="company")
    strategic_initiatives: Mapped[List["StrategicInitiative"]] = relationship("StrategicInitiative", back_populates="company")
    corporate_events: Mapped[List["CorporateEvent"]] = relationship("CorporateEvent", back_populates="company")

class SourceDocument(Base):
    __tablename__ = "source_documents"

    document_id: Mapped[str] = mapped_column(String(64), primary_key=True) # e.g. 'SWIGGY-Q1FY26', 'ETERNAL-Q1FY27'
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False, index=True)
    document_type: Mapped[str] = mapped_column(String(64), nullable=False) # 'shareholder_letter', 'overview', 'statutory_report'
    fiscal_year: Mapped[str] = mapped_column(String(8), nullable=False, index=True) # 'FY25', 'FY26', 'FY27'
    fiscal_quarter: Mapped[str] = mapped_column(String(4), nullable=False, index=True) # 'Q1', 'Q2', 'Q3', 'Q4'
    period_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    publication_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    original_file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    total_pages: Mapped[int] = mapped_column(Integer, nullable=False)
    extraction_status: Mapped[str] = mapped_column(String(32), default="VERIFIED") # VERIFIED, PARTIAL, PENDING

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="documents")
    pages: Mapped[List["SourcePage"]] = relationship("SourcePage", back_populates="document", cascade="all, delete-orphan")
    observations: Mapped[List["MetricObservation"]] = relationship("MetricObservation", back_populates="source_document")

class SourcePage(Base):
    __tablename__ = "source_pages"

    page_id: Mapped[str] = mapped_column(String(128), primary_key=True) # e.g. 'SWIGGY-Q1FY26-P05'
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("source_documents.document_id"), nullable=False, index=True)
    pdf_page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    printed_page_number: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    section_hint: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ocr_confidence_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 4), nullable=True)
    has_raster_tables: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    document: Mapped["SourceDocument"] = relationship("SourceDocument", back_populates="pages")
    observations: Mapped[List["MetricObservation"]] = relationship("MetricObservation", back_populates="source_page")

class BusinessSegment(Base):
    __tablename__ = "business_segments"

    segment_id: Mapped[str] = mapped_column(String(64), primary_key=True) # e.g. 'SWIGGY_FOOD', 'ETERNAL_QUICK_COMMERCE'
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("companies.company_id"), nullable=False, index=True)
    segment_name: Mapped[str] = mapped_column(String(128), nullable=False)
    commercial_brand: Mapped[str] = mapped_column(String(128), nullable=False) # 'Food Delivery', 'Blinkit', 'Instamart'
    scope_level: Mapped[str] = mapped_column(String(32), nullable=False) # 'SEGMENT', 'B2C_GROUP', 'CONSOLIDATED'
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="segments")
    observations: Mapped[List["MetricObservation"]] = relationship("MetricObservation", back_populates="segment")
