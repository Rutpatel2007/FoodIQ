# FoodIQ — Relational Database Schema Specification

This document details the normalized relational schema implemented in SQLAlchemy 2.0 with Alembic migration control and SQLite/PostgreSQL parity.

## 1. Design Principles
- **Relational Integrity:** Foreign keys are strictly enforced across companies, documents, segments, pages, definitions, and observations (`PRAGMA foreign_keys=ON;`).
- **Precision:** Numeric fields use `NUMERIC(14, 4)` for exact decimal arithmetic; floating-point approximation is prohibited.
- **Null Preservation:** Missing corporate disclosures remain `NULL`; silent coercion to zero is prohibited.
- **Traceability:** Every observation references its primary `source_document_id` and granular `source_page_id`.
- **Version Control:** Historical conflicting or restated numbers are preserved via `report_version` rather than being overwritten.

---

## 2. Entity Register

### `companies`
Stores institutional entities covered by the intelligence platform.
- `company_id` (VARCHAR(32), PK): Canonical symbol (`ETERNAL`, `SWIGGY`).
- `canonical_name` (VARCHAR(128)): Official company title.
- `ticker_symbol` (VARCHAR(32)): Stock exchange ticker symbol.
- `incorporation_jurisdiction` (VARCHAR(64)): Legal jurisdiction (`India`).
- `description` (TEXT): High-level operational overview.

### `source_documents`
Authoritative filings registered with SHA-256 cryptographic hashes.
- `document_id` (VARCHAR(64), PK): Unique filing key (e.g., `SWIGGY-Q1FY26`, `ETERNAL-Q2FY27`).
- `company_id` (VARCHAR(32), FK -> companies.company_id).
- `document_type` (VARCHAR(64)): `shareholder_letter`, `overview`, `statutory_report`.
- `fiscal_year` (VARCHAR(8)): `FY25`, `FY26`, `FY27`.
- `fiscal_quarter` (VARCHAR(4)): `Q1`, `Q2`, `Q3`, `Q4`.
- `period_end_date` (DATE): Exact quarterly cut-off date.
- `publication_date` (DATE): Filing release date.
- `original_file_name` (VARCHAR(255)): Source PDF file basename.
- `file_path` (VARCHAR(512)): Workspace disk path.
- `file_checksum_sha256` (CHAR(64)): SHA-256 digest of original PDF file.
- `total_pages` (INT): Total physical page count.
- `extraction_status` (VARCHAR(32)): `VERIFIED`, `PARTIAL`, `PENDING`.

### `source_pages`
Page-level granularity enabling one-click citation proof.
- `page_id` (VARCHAR(128), PK): Formatted key (e.g., `SWIGGY-Q1FY26-P05`).
- `document_id` (VARCHAR(64), FK -> source_documents.document_id).
- `pdf_page_number` (INT): 1-indexed physical PDF page number.
- `printed_page_number` (VARCHAR(16)): Letter-printed pagination label.
- `section_hint` (VARCHAR(128)): Section header (e.g. `Annexure A`, `Financial Statements`).
- `extracted_text` (TEXT): Searchable OCR / layout text excerpt.
- `ocr_confidence_score` (NUMERIC(5, 4)): Quality metric (NULL for digital vectors).
- `has_raster_tables` (BOOLEAN): Flag indicating scanned/raster table content.

### `business_segments`
Operational and reporting perimeters.
- `segment_id` (VARCHAR(64), PK): e.g. `SWIGGY_FOOD`, `ETERNAL_QUICK_COMMERCE`.
- `company_id` (VARCHAR(32), FK -> companies.company_id).
- `segment_name` (VARCHAR(128)): Segment name.
- `commercial_brand` (VARCHAR(128)): Consumer-facing brand (`Blinkit`, `Instamart`).
- `scope_level` (VARCHAR(32)): `SEGMENT`, `B2C_GROUP`, `CONSOLIDATED`.
- `is_active` (BOOLEAN): Operational state.

### `metric_definitions`
Canonical glossary defining numerator, denominator, and scope.
- `metric_id` (VARCHAR(64), PK): Unique identifier.
- `canonical_name` (VARCHAR(128)): Normalized term.
- `company_id` (VARCHAR(32), FK -> companies.company_id).
- `native_term` (VARCHAR(128)): Company-reported title.
- `unit` (VARCHAR(32)): Unit of measure.
- `numerator_formula` (TEXT): Calculation inputs.
- `denominator_formula` (TEXT): Exact base scope (% GOV, % NOV, etc.).
- `segment_scope` (VARCHAR(64)): Segment boundary.
- `accounting_standard` (VARCHAR(64)): Standard followed (`IndAS`).
- `source_reference_page_id` (VARCHAR(128), FK -> source_pages.page_id).
- `implementation_notes` (TEXT): Boundary notes and analyst considerations.

### `metric_observations`
Core longitudinal fact table storing time-series financial observations.
- `observation_id` (VARCHAR(128), PK): Structured identifier.
- `company_id` (VARCHAR(32), FK -> companies.company_id).
- `segment_id` (VARCHAR(64), FK -> business_segments.segment_id).
- `metric_id` (VARCHAR(64), FK -> metric_definitions.metric_id).
- `fiscal_year` (VARCHAR(8)): Reporting year.
- `fiscal_quarter` (VARCHAR(4)): Reporting quarter.
- `period_end_date` (DATE): Reporting cut-off date.
- `value` (NUMERIC(14, 4), NULLABLE): Verified numerical value.
- `unit` (VARCHAR(32)): Monetary/volume unit.
- `denominator_basis` (VARCHAR(128)): Denominator context.
- `observation_type` (VARCHAR(32)): `REPORTED`, `DERIVED`, `MANAGEMENT_ESTIMATE`, `OCR_VERIFIED`, `RESTATED`.
- `source_document_id` (VARCHAR(64), FK -> source_documents.document_id).
- `source_page_id` (VARCHAR(128), FK -> source_pages.page_id).
- `report_version` (INT): Incremental version number.
- `validation_status` (VARCHAR(32)): `PASSED`, `WARNING`, `RESTATED`, `UNRESOLVED`.
- `raw_source_value` (VARCHAR(255)): Raw unparsed string extracted from document.
- `verified_value` (NUMERIC(14, 4)): Cross-checked validated number.
- `analyst_notes` (TEXT): Traceability notes and audit remarks.

### `data_quality_flags`
Audit log tracking extraction issues, conflicts, and restatements.
- `flag_id` (VARCHAR(64), PK).
- `observation_id` (VARCHAR(128), FK -> metric_observations.observation_id, NULLABLE).
- `issue_code` (VARCHAR(64)): Categorical code (`OCR_CORRECTION`, `RESTATED_WITHOUT_NOTE`).
- `severity` (VARCHAR(16)): `CRITICAL`, `HIGH`, `MEDIUM`, `INFO`.
- `issue_description` (TEXT): Detailed explanation of discrepancy.
- `audit_trail` (TEXT): Resolution action and cross-check evidence.
- `is_resolved` (BOOLEAN): Resolution state.

### `source_conflicts`
Captures multi-source reporting variances.
- `conflict_id` (VARCHAR(64), PK).
- `company_id` (VARCHAR(32), FK -> companies.company_id).
- `metric_name` (VARCHAR(128)).
- `quarter` (VARCHAR(16)).
- `value_a` (VARCHAR(128)): First reported value.
- `source_a` (VARCHAR(255)): First disclosure citation.
- `page_a` (VARCHAR(32)): Page in first disclosure.
- `value_b` (VARCHAR(128)): Subsequent comparative value.
- `source_b` (VARCHAR(255)): Second disclosure citation.
- `page_b` (VARCHAR(32)): Page in second disclosure.
- `resolution_strategy` (VARCHAR(64)): `PRESERVE_BOTH_RECORDS`.
- `reconciliation_notes` (TEXT).

### `comparability_rules`
Governance matrix preventing invalid cross-company or cross-period comparisons.
- `rule_id` (VARCHAR(64), PK).
- `metric_a_id` (VARCHAR(64)).
- `metric_b_id` (VARCHAR(64)).
- `comparability_tier` (VARCHAR(32)): `DIRECT`, `ADJUSTED`, `DIRECTIONAL`, `INCOMPARABLE`.
- `adjustment_formula` (TEXT).
- `prohibited_operations` (TEXT).
- `methodology_caveats` (TEXT).

### `corporate_events`
Accounting structural breaks and corporate reorganizations.
- `event_id` (VARCHAR(64), PK).
- `company_id` (VARCHAR(32), FK -> companies.company_id).
- `event_date` (DATE).
- `quarter_impacted` (VARCHAR(16)).
- `event_type` (VARCHAR(64)): `1P_INVENTORY_TRANSITION`, `M_AND_A`, `DIVESTMENT`.
- `headline` (VARCHAR(255)).
- `detailed_economic_impact` (TEXT).
- `affected_segments` (VARCHAR(255)).
- `affected_metrics` (VARCHAR(255)).
- `source_page_id` (VARCHAR(128), FK -> source_pages.page_id).

### `management_guidance` & `guidance_outcomes`
Forward-looking commitments tracking and evaluation scorecard.
- `guidance_id` (VARCHAR(64), PK).
- `company_id` (VARCHAR(32), FK -> companies.company_id).
- `issued_in_quarter` (VARCHAR(16)).
- `verbatim_quote` (TEXT).
- `metric_targeted` (VARCHAR(128)).
- `guidance_type` (VARCHAR(32)): `EXACT_VALUE`, `NUMERICAL_RANGE`, `BREAK_EVEN`, `QUALITATIVE`.
- `target_deadline_quarter` (VARCHAR(16)).
- Evaluated via `guidance_outcomes` linking actual observation outcomes and status (`ACHIEVED`, `MISSED`, `PENDING`).
