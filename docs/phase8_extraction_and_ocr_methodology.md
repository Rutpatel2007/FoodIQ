# FoodIQ Phase 8 — Extraction & OCR Methodology

## 1. Dual-Layer Extraction Governance

Extracting financial figures from corporate PDF filings presents risks of OCR misreads (e.g. `8` misread as `B` or `3`, decimal points dropped). FoodIQ enforces dual-layer extraction governance:

1. **Raw OCR Preservation:**
   Every extracted text block is stored in its unaltered, raw string representation (`raw_source_value` in `metric_observations` and `ocr_text` in `source_pages`).
2. **Normalized Numerical Values:**
   Clean numerical floats are stored separately in the `value` column after standardized parsing and unit validation.
3. **Traceability:**
   Any correction or normalization is accompanied by `analyst_notes` explaining the rationale (e.g., "Normalized from thousands to millions", "Decimal point restored based on prior quarter comparative column").

---

## 2. Multi-Quarter Comparative Cross-Referencing

Indian statutory filings publish multi-quarter comparative disclosures:
- In Q2 FY26 filings, the company reports Q2 FY26 along with comparative columns for Q1 FY26 and Q2 FY25.
- FoodIQ's OCR validator cross-references extracted numbers against identical quarters reported in subsequent filings.
- If a subsequent filing reports a restated or adjusted figure, the system logs a `source_conflict` record rather than overwriting historical observations.
