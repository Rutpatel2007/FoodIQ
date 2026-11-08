# FoodIQ Phase 7 — Citation & Verification Framework

## 1. Citation Lineage Architecture

The credibility of equity research depends on the absolute verifiability of its underlying data. FoodIQ enforces a strict, multi-tiered citation lineage framework:

Every material factual statement, table cell, and derived calculation in a generated report must resolve to an immutable chain of custody:

$$\text{Report Statement} \longrightarrow \text{Derived Calculation} \longrightarrow \text{Database Metric Observation} \longrightarrow \text{Physical PDF Page} \longrightarrow \text{Statutory Filing (SHA-256 Checksum)}$$

---

## 2. Citation Schema & Data Structure

Every citation collected during report generation is recorded in the report's `citation_verification` register:

```json
{
  "company": "ETERNAL",
  "source_doc": "ETERNAL-Q2FY27",
  "page": "P13",
  "metric": "eternal_qcomm_nov",
  "resolution_status": "RESOLVED"
}
```

### Verification Fields
- `company`: The reporting legal entity (`ETERNAL`, `SWIGGY`, or `CONSOLIDATED`).
- `source_doc`: The canonical statutory document ID (e.g. `ETERNAL-Q2FY27`, `SWIGGY-Q2FY27-SHL`).
- `page`: The exact physical page number in the published PDF (e.g. `P13`, `P07`).
- `metric`: The canonical metric identifier or research finding ID.
- `resolution_status`: Automated verification flag (`RESOLVED` or `UNRESOLVED`).

---

## 3. Automated Citation Verification Engine

Before any generated report is marked `VERIFIED`, the citation verification engine runs an automated SQL audit against `foodiq.db`:

1. **Document Resolution Check:**
   Queries `source_documents` to verify that `source_doc` exists in the statutory filing catalog and matches the recorded SHA-256 hash.
2. **Page Existence Check:**
   Cross-references `source_pages` to confirm that the physical page exists and contains the extracted OCR text corresponding to the metric.
3. **Resolution Threshold:**
   A report requires $\ge 90.0\%$ citation resolution rate to receive a `VERIFIED` status. Reports with broken or fabricated citations are flagged with `FLAGGED_WITH_WARNINGS` and prohibited from institutional distribution.

---

## 4. Report Quality & Integrity Scorecard

The report engine runs four automated integrity checks:

| Check Name | Acceptance Criteria | Operational Implementation |
| :--- | :--- | :--- |
| **Section Completeness** | $\ge 4$ analytical sections present | Validates that required sections for the chosen report type are fully constructed. |
| **Citation Integrity** | $\ge 90.0\%$ citation resolution rate | Every cited filing and page must resolve against the database source registers. |
| **Comparability Enforcement**| 100% adherence to 4-tier rules | Level 4 subtractions blocked; Level 3 comparisons carry directional notes. |
| **Period Consistency** | Period cutoff matches database | Ensures reported metrics reflect the stated cutoff (e.g. Q2 FY27). |

---

## 5. Report Audit Trail & Persistence

All generated reports are assigned a unique, immutable report ID:
$$\text{REP}-\text{YYYYMMDDHHMMSS}-\text{UUID6}$$
The complete report payload, including generation timestamp, author, section contents, citation registers, and the verification scorecard, is persisted to the `generated_reports` table in `data/foodiq.db` to guarantee historical reproducibility.
