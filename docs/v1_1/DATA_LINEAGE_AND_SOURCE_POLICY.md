# FoodIQ v1.1 — Data Lineage & Provenance Policy
**Document Reference:** DOC-V11-07  
**Classification:** Forensic Evidence & Audit Trails  

---

## 1. The Evidence Hierarchy

FoodIQ enforces a 3-tier hierarchy of source credibility:
1. **Tier 1 (Statutory Filings):** Audited Financial Statements, Limited Review Financial Results, and Shareholder Letters filed directly with BSE and NSE. These serve as the absolute authority.
2. **Tier 2 (Prospectus Disclosures):** IPO Draft Red Herring Prospectus (DRHP) and Red Herring Prospectus (RHP) reviewed by SEBI.
3. **Tier 3 (Company Presentations & Transcripts):** Official investor presentations and verbatim earnings call transcripts.

Press articles, broker summaries, and third-party aggregator statistics are strictly barred from the canonical database.

---

## 2. Coordinate-Level Lineage

Every observation in `metric_observations` links to:
- `source_document_id`: The statutory filing identifier.
- `source_page_id`: The specific document page.
- `bounding_box`: A 4-tuple coordinate `(x0, y0, x1, y1)` locating the exact table cell or paragraph on the page.

This architecture enables instant visual verification in the FoodIQ PDF Workstation.
