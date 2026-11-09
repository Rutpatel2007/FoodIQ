# FoodIQ v1.1 — Database Schema Reference Manual
**Document Reference:** DOC-V11-10  
**Classification:** Database Architecture & Relational Design  

---

## 1. Overview & SQLite Configuration

FoodIQ utilizes an embedded SQLite 3 relational database (`data/foodiq.db`) configured for high-concurrency read operations:
- `PRAGMA journal_mode = WAL;` (Write-Ahead Logging enabled)
- `PRAGMA synchronous = NORMAL;`
- `PRAGMA foreign_keys = ON;`

---

## 2. Table Specifications

### 2.1 `metric_definitions`
Defines canonical metric names, units, and comparability constraints.
- `metric_id` (TEXT, PK): Canonical string identifier (e.g. `SWIGGY_INSTAMART_GOV`).
- `canonical_name` (TEXT): Display name.
- `company_id` (TEXT): Company ownership or `NULL` for generic.
- `segment_id` (TEXT): Segment classification.
- `unit` (TEXT): Currency or quantitative unit.
- `comparability_tier` (INTEGER): 1 to 4.

### 2.2 `metric_observations`
Contains the authoritative empirical historical time series.
- `observation_id` (TEXT, PK): Unique record identifier.
- `metric_id` (TEXT, FK): References `metric_definitions`.
- `period_id` (TEXT, FK): References `reporting_periods`.
- `value` (REAL): Disclosed numerical value.
- `source_document_id` (TEXT, FK): References `source_documents`.
- `source_page_id` (TEXT, FK): References `source_pages`.

### 2.3 `management_commitments`
Tracks strategic guidance and management targets.
- `commitment_id` (TEXT, PK): E.g., `ETR-CMT-001`.
- `company_id` (TEXT, FK): References `companies`.
- `quote_text` (TEXT): Verbatim statement.
- `delivery_status` (TEXT): `DELIVERED`, `PARTIAL`, `MISSED`, `IN_PROGRESS`, `NOT_MEASURABLE`.
- `target_period` (TEXT): Target delivery quarter.
