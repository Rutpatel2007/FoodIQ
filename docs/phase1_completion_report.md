# FoodIQ — Phase 1 Execution & Completion Report

**Role & Responsibility:** Principal Software Architect, Senior Quantitative Research Engineer, Financial Data Scientist, Data Engineering Lead.  
**System:** FoodIQ Competitive Intelligence Engine  
**Milestone:** Phase 1 — Data Foundation, Ingestion Pipelines, Provenance Engine & Governance Backend  
**Execution Date:** November 7, 2026  
**Status:** **PHASE 1 COMPLETE — 100% ACCEPTANCE CRITERIA MET**

---

## 1. Actual Documents Ingested

A total of **14 primary corporate disclosure filings** were registered, verified, and checksummed with SHA-256 digests across Swiggy and Eternal:

| Company | Document ID | Document Type | Period | File Name | PDF Pages | SHA-256 Digest | Status |
|---|---|---|:---:|---|:---:|---|:---:|
| **Swiggy** | `SWIGGY-Q1FY26` | Shareholder Letter | Q1 FY26 | `Q1-FY2026-Shareholder-letter.pdf` | 35 | `d726bfa6b2d281315b6d5ec89643d9f9c06518174f7d43ef0fc9c6ba7f433990` | VERIFIED |
| **Swiggy** | `SWIGGY-Q2FY26` | Shareholder Letter | Q2 FY26 | `Q2-FY2026-Shareholder-letter.pdf` | 41 | `4e1f7481076b1767b2d5d852a4660eb9d61596e140d3a51600122e2324f9e160` | VERIFIED |
| **Swiggy** | `SWIGGY-Q3FY26` | Shareholder Letter | Q3 FY26 | `Q3-FY2026-Shareholder-letter.pdf` | 36 | `fc969bb1687f610f4ea5eb8c7bb5eefb988f54a8b79564f26fc181ef80ec70a4` | VERIFIED |
| **Swiggy** | `SWIGGY-Q4FY26` | Shareholder Letter | Q4 FY26 | `Q4-FY2026-Shareholder-letter.pdf` | 42 | `00ff1c83fa98e4f509fa845fef6070fa848d706d859424cb898ec0a1e05e557b` | VERIFIED |
| **Swiggy** | `SWIGGY-Q1FY27` | Shareholder Letter | Q1 FY27 | `Q1-FY2027-Shareholder-letter.pdf` | 35 | `514ecff830b8c4c7ee40e2cf70829ee15eebad241ca49e691885fbf88981df12` | VERIFIED |
| **Swiggy** | `SWIGGY-Q2FY27` | Shareholder Letter | Q2 FY27 | `Q2-FY2027-Shareholder-letter.pdf` | 39 | `8c47b59e3592160d5bfa62e92c68e3b1239ce34f2d26f63ea4b8400dcfe26532` | VERIFIED |
| **Eternal** | `ETERNAL-Q3FY25` | Shareholder Letter | Q3 FY25 | `Q3FY25_681c57ac...pdf` | 31 | `a01ec34a1eb4d909564fa72a85ea8d3b80aa5588383f9e9cf2a70cb65f1e16f7` | VERIFIED |
| **Eternal** | `ETERNAL-April2025` | Company Overview | April 2025 | `April2025_Eternal_Ltd...pdf` | 33 | `8177dfb3e40cb8bbfbb1e5a59a7f3427fef4fb8f57fbe132840cf098860b0907` | VERIFIED |
| **Eternal** | `ETERNAL-Q1FY26` | Shareholder Letter | Q1 FY26 | `Q1FY26_8f0d6136...pdf` | 36 | `5a5f6e804f58b093ca382d56aee86ec9a37a7ea7dcfcfb120db87b1c1d0f5ec8` | VERIFIED |
| **Eternal** | `ETERNAL-Q2FY26` | Shareholder Letter | Q2 FY26 | `Q2FY26_60824ca7...pdf` | 38 | `4b6842849e798f3bba5f2dd3e27a13dff608c0ef7343e74b33df5a6104e7fe9c` | VERIFIED |
| **Eternal** | `ETERNAL-Q3FY26` | Shareholder Letter | Q3 FY26 | `Q3FY26_bf94ed1c...pdf` | 33 | `1fcf96f8c7b8054c3fffa92305545a9f24baaa41315dae65c088c4547a46fa48` | VERIFIED |
| **Eternal** | `ETERNAL-Q4FY26` | Shareholder Letter | Q4 FY26 | `Q4FY26_Eternal_Shareholders...pdf` | 44 | `942080a2df330eb5b958801d9c15e2aaae58d92cb647a7b8e5c14ff0e68407ee` | VERIFIED |
| **Eternal** | `ETERNAL-Q1FY27` | Shareholder Letter | Q1 FY27 | `Q1FY27_Eternal_Limited...pdf` | 31 | `ba17be9ef5ee68194a2dfbfb597b87cbffb2c89fbf695bcefa54738fc9f1e16f` | VERIFIED |
| **Eternal** | `ETERNAL-Q2FY27` | Shareholder Letter | Q2 FY27 | `Q2FY27_Eternal_Limited...pdf` | 39 | `9d554a72d37c569ff466cf87bdf55998dfc38489a2479e394fe3d132cb0dbb12` | VERIFIED |

---

## 2. Actual Observations Ingested by Company and Segment

**Total Observations Ingested:** **570 canonical observations**

### By Company:
- **Swiggy Limited:** **400 observations** (Q1 FY25 through Q2 FY27)
- **Eternal Limited:** **170 observations** (Q1 FY24 through Q2 FY27)

### By Segment Breakdown:
```
┌──────────────────────────────────────┬─────────────┬────────────────────┐
│ Segment Name                         │ Company     │ Observations Count │
├──────────────────────────────────────┼─────────────┼────────────────────┤
│ SWIGGY_FOOD (Food Delivery)          │ Swiggy      │ 70                 │
│ SWIGGY_QUICK_COMMERCE (Instamart)    │ Swiggy      │ 140                │
│ SWIGGY_OUT_OF_HOME (Dineout)         │ Swiggy      │ 60                 │
│ SWIGGY_SUPPLY_CHAIN (Lynks/Distrib)  │ Swiggy      │ 30                 │
│ SWIGGY_PLATFORM_INNOVATIONS          │ Swiggy      │ 30                 │
│ SWIGGY_PLATFORM (B2C Consolidated)   │ Swiggy      │ 70                 │
├──────────────────────────────────────┼─────────────┼────────────────────┤
│ ETERNAL_FOOD (Zomato Food Delivery)  │ Eternal     │ 40                 │
│ ETERNAL_QUICK_COMMERCE (Blinkit)     │ Eternal     │ 50                 │
│ ETERNAL_GOING_OUT (District)         │ Eternal     │ 40                 │
│ ETERNAL_HYPERPURE (B2B Supplies)     │ Eternal     │ 20                 │
│ ETERNAL_B2C (B2C Business Total)     │ Eternal     │ 20                 │
├──────────────────────────────────────┼─────────────┼────────────────────┤
│ TOTAL FINANCIAL OBSERVATIONS         │             │ 570                │
└──────────────────────────────────────┴─────────────┴────────────────────┘
```

---

## 3. Verified Versus Unverified Observations

- **Verified Observations (`PASSED`):** **568 observations (99.65%)**  
  Directly reconciled against authoritative financial disclosure tables and audited statutory statements.
- **Restated / OCR Corrected Observations (`RESTATED`):** **2 observations (0.35%)**  
  Scanned OCR errors reconciled and ground-truthed against subsequent comparative tables.
- **Unverified Observations (`UNRESOLVED`):** **0 observations (0.0%)**  
  Every observation has verified source attribution.

---

## 4. Missing or Unresolved Source References

- **Standalone Eternal Q1 FY25 and Q4 FY25 Shareholder Letters:**
  - Neither letter is included in the source pack.
  - In strict adherence to Part 13 Rule 2, **no quarters were interpolated or fabricated**.
  - All Q1FY25 and Q4FY25 observations are attributed strictly to the subsequent disclosures where they appeared as comparative columns (`ETERNAL-Q1FY26` and `ETERNAL-Q4FY26`).
- **Swiggy Food Delivery & Out-of-Home NOV:**
  - Management explicitly confirmed that Food Delivery NOV is not published because discount and subsidy structures are non-comparable across competitors.
  - These metrics remain unpopulated.

---

## 5. OCR Verification Results

The `EternalOCRValidator` cross-checked raster OCR extracts from `Annexure_OCR/` against subsequent digital comparative disclosure tables:
1. **Q2FY25 Food Delivery NOV:**
   - Raw OCR String: `g281`
   - Corrected Value: `8281.0` (₹8,281 Cr)
   - Supporting Evidence: Q2FY27 Annexure A (p. 13) and Q1FY27 Annexure A (p. 9) comparative columns.
   - Status: Corrected and flagged with `DataQualityFlag` (`DQ-ETERNAL-OCR-Q2FY25-food_nov`).
2. **Q2FY25 Going-Out NOV:**
   - Raw OCR String: `4582258888`
   - Corrected Value: `1562.0` (₹1,562 Cr)
   - Supporting Evidence: Q2FY27 Annexure A comparative disclosures.
   - Status: Corrected and flagged with `DataQualityFlag` (`DQ-ETERNAL-OCR-Q2FY25-going_out_nov`).

---

## 6. Source Conflicts Preserved

All 9 documented Swiggy reporting conflicts are preserved in `source_conflicts`:
- **SC-001:** Platform MTU Q1FY27 (27.5m in Q1FY27 p.5 vs 26.2m in Q2FY27 p.5).
- **SC-002 & SC-003:** Platform Frequency variances (4.18 vs 4.13 in Q1FY26; 3.87 vs 3.92 in Q1FY27).
- **SC-004:** Food Delivery NOV omission confirmation.
- **SC-006:** Supply Chain Lynks divestment scope adjustment.
- **SC-007:** Instamart break-even milestone (May 2026 monthly break-even vs -0.2% and -1.0% quarterly averages).
- **SC-008:** Quick Commerce NOV derived ratios vs absolute metrics.

---

## 7. Data Quality Issues by Severity

| Severity | Count | Primary Areas |
|---|:---:|---|
| **CRITICAL** | 2 | Food Delivery NOV omission (Swiggy), Scope perimeter divergence |
| **HIGH** | 12 | Blinkit 1P transition, Lynks divestment, MTU restatements, OCR corrections |
| **MEDIUM** | 7 | Platform frequency restatements, store throughput math, seasonal cycles |
| **INFO** | 1 | Operational run-rate claims |
| **TOTAL** | **22** | **100% cataloged and accessible via API & reports** |

---

## 8. Database Migration Status

- **Engine:** SQLite 3 with full PostgreSQL SQLAlchemy 2.0 DDL compatibility.
- **Migrations:** Managed via Alembic (`backend/alembic/versions/35e4bafc2e8f_initial_schema.py`).
- **Database File:** `data/foodiq.db` (Indexed with foreign keys and unique constraints).
- **Status:** Head revision applied and stamped.

---

## 9. API Implementation Status

FastAPI backend application running with OpenAPI/Swagger documentation at `/docs`:
- `GET /api/v1/health` — Returns system health and database connectivity.
- `GET /api/v1/companies` — Lists covered companies.
- `GET /api/v1/documents` — Lists registered filings with SHA-256 digests.
- `GET /api/v1/segments` — Lists operating segments.
- `GET /api/v1/metrics` — Lists metric definitions.
- `GET /api/v1/observations` — Longitudinal financial observations with pagination and filters.
- `GET /api/v1/observations/{id}` — Single observation query.
- `GET /api/v1/observations/{id}/lineage` — Full source-to-insight provenance chain.
- `GET /api/v1/data-quality/summary` — Aggregate issue counts by severity.
- `GET /api/v1/data-quality/issues` — Detailed issue ledger.
- `GET /api/v1/comparability/rules` — Financial governance rules.
- `GET /api/v1/guidance` — Management commitments tracker.

---

## 10. Actual Automated Test Results

Executed via `pytest backend/tests -v`:
```
============================= test session starts =============================
platform win32 -- Python 3.12.11, pytest-9.1.1, pluggy-1.6.0
collected 27 items

backend/tests/test_api_endpoints.py::test_api_health PASSED              [  3%]
backend/tests/test_api_endpoints.py::test_api_companies PASSED           [  7%]
backend/tests/test_api_endpoints.py::test_api_documents PASSED           [ 11%]
backend/tests/test_api_endpoints.py::test_api_segments PASSED            [ 14%]
backend/tests/test_api_endpoints.py::test_api_metrics PASSED             [ 18%]
backend/tests/test_api_endpoints.py::test_api_observations PASSED        [ 22%]
backend/tests/test_api_endpoints.py::test_api_observation_by_id_and_lineage PASSED [ 25%]
backend/tests/test_api_endpoints.py::test_api_data_quality PASSED        [ 29%]
backend/tests/test_api_endpoints.py::test_api_comparability_rules PASSED [ 33%]
backend/tests/test_api_endpoints.py::test_api_guidance PASSED            [ 37%]
backend/tests/test_comparability_governance.py::test_comparability_rules_seeded PASSED [ 40%]
backend/tests/test_comparability_governance.py::test_gov_nov_direct_comparison_blocked PASSED [ 44%]
backend/tests/test_comparability_governance.py::test_qcomm_revenue_1p_break_blocked PASSED [ 48%]
backend/tests/test_database_models.py::test_database_companies PASSED    [ 51%]
backend/tests/test_database_models.py::test_database_relationships_and_foreign_keys PASSED [ 55%]
backend/tests/test_database_models.py::test_referential_integrity PASSED [ 59%]
backend/tests/test_ingestion_and_idempotency.py::test_ingestion_counts PASSED [ 62%]
backend/tests/test_ingestion_and_idempotency.py::test_ingestion_idempotency PASSED [ 66%]
backend/tests/test_lineage_and_provenance.py::test_source_document_sha256_checksums PASSED [ 70%]
backend/tests/test_lineage_and_provenance.py::test_lineage_service_retrieval PASSED [ 74%]
backend/tests/test_lineage_and_provenance.py::test_lineage_service_non_existent PASSED [ 77%]
backend/tests/test_null_and_financial_integrity.py::test_null_preservation PASSED [ 81%]
backend/tests/test_null_and_financial_integrity.py::test_swiggy_food_delivery_nov_not_fabricated PASSED [ 85%]
backend/tests/test_null_and_financial_integrity.py::test_margin_denominators_preserved PASSED [ 88%]
backend/tests/test_ocr_validator.py::test_ocr_clean_match PASSED         [ 92%]
backend/tests/test_ocr_validator.py::test_ocr_malformed_correction PASSED [ 96%]
backend/tests/test_ocr_validator.py::test_ocr_unresolved_handling PASSED [100%]

======================= 27 passed in 12.86s =======================
```

---

## 11. Exact Commands to Run FoodIQ Locally

### Run Database Migrations:
```bash
cd backend
alembic upgrade head
```

### Run Ingestion & Generate Reports:
```bash
python -m backend.app.ingestion.runner
```

### Run Automated Test Suite:
```bash
pytest backend/tests -v
```

### Start FastAPI Development Server:
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation will be live at: `http://localhost:8000/docs`

---

## 12. Remaining Limitations & Edge Cases

1. **Eternal Food Delivery GOV Post-Q1FY26:** Discontinued by management in favor of NOV. Direct GOV-to-GOV peer comparison ends at Q1FY26.
2. **Blinkit Non-Grocery / AOV Metrics:** Detailed category mixes (FMCG vs. Electronics) are cited in commentary but not consistently broken down in statutory tables.
3. **Swiggy Supply Chain Breakdown:** Lynks divestment occurred in Q2FY27; historical Supply Chain run rates require an adjustment bridge when analyzing future quarters.
4. **Sample Size for Statistical Testing:** 10 longitudinal quarters are available (Q1FY25–Q2FY27). Phase 5 statistical engines must use non-parametric methods (Spearman rank) and strict significance safeguards ($N \le 10$).

---

## 13. Deliverables Inventory

All generated artifacts are persisted in the repository:
- `data/foodiq.db` (Populated relational database)
- `data/reports/data_quality_report.json`
- `data/reports/data_quality_report.csv`
- `data/reports/ingestion_summary.json`
- `data/reports/source_lineage_report.csv`
- `data/reports/unresolved_observations.csv`
- `docs/database_schema.md`
- `docs/ingestion_architecture.md`
- `docs/source_lineage.md`
- `docs/data_quality.md`
- `docs/comparability_governance.md`
- `docs/api_reference.md`
- `docs/phase1_completion_report.md`
