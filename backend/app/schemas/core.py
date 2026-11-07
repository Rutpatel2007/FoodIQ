"""
Pydantic v2 schemas for Core entities
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_id: str
    canonical_name: str
    ticker_symbol: str
    incorporation_jurisdiction: str
    description: Optional[str] = None

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: str
    company_id: str
    document_type: str
    fiscal_year: str
    fiscal_quarter: str
    period_end_date: date
    publication_date: Optional[date] = None
    original_file_name: str
    file_checksum_sha256: str
    total_pages: int
    extraction_status: str

class SegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    segment_id: str
    company_id: str
    segment_name: str
    commercial_brand: str
    scope_level: str
    is_active: bool
