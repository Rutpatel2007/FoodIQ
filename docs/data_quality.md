# FoodIQ — Data Quality & Integrity Specification

## 1. Principles of Data Integrity
1. **Never Fill Missing Values with Zero:** In corporate disclosures, an undisclosed figure is an unknown, not zero. Converting null to zero destroys mathematical ratios and distorts historical trends.
2. **Never Fabricate Numbers:** Swiggy does not publish Food Delivery NOV or Out-of-Home NOV. The platform rejects any attempt to fabricate or back-calculate these without explicit source support.
3. **Preserve Conflicting Disclosures:** When two shareholder letters report different numbers for the same historical period (e.g. Swiggy Q1FY27 Platform MTU reported as 27.5m in Q1FY27 letter and 26.2m in Q2FY27 chart), both numbers are preserved with their source document citations.

---

## 2. Severity Classification

| Severity Level | Definition | Handling Protocol |
|---|---|---|
| **CRITICAL** | Undisclosed headline metrics or corrupted values with no baseline | Operation blocked or metric marked as unsupported |
| **HIGH** | Historical restatements without footnotes; structural accounting shifts | Warning banner displayed; comparative cross-check enforced |
| **MEDIUM** | Minor variance in operational KPIs across reporting periods | Dual lineage maintained with analyst note |
| **INFO** | Informational notes regarding acquisitions or divestments | Source conflict / event registered |

---

## 3. Registered Data Quality Issues Summary

FoodIQ logs 22 discrete data quality issues across Swiggy and Eternal:
- **DQ-001 (Critical):** Original pack was Swiggy-only; now solved via Phase 1 ingestion of Eternal disclosures.
- **DQ-002 (High):** Q1FY27 Platform MTU conflict (27.5m in Q1FY27 p.5 vs 26.2m in Q2FY27 p.5). Preserved in `source_conflicts` SC-001.
- **DQ-003 (Medium):** Platform frequency history variances across filings (SC-002, SC-003).
- **DQ-004 (Critical):** Swiggy Food Delivery NOV is explicitly unpublished. Blocked from calculation.
- **DQ-005 (High):** Swiggy Out-of-Home NOV is explicitly unpublished. Blocked from calculation.
- **DQ-006 (High):** Scope mixing in seed data: B2C GOV was placed alongside Consolidated Adjusted Revenue and EBITDA. Normalized into separate segment models.
- **DQ-007 (High):** Margin denominators differ by segment (% GOV vs % Revenue). Normalized into `metric_definitions`.
- **DQ-008 (High):** Swiggy QComm NOV derived ratios vs absolute metrics.
- **DQ-010 (High):** QComm break-even claims: May 2026 monthly break-even was achieved, but quarterly average contribution margins remained negative (-0.2% in Q1FY27 and -1.0% in Q2FY27).
- **DQ-011 (High):** Swiggy Lynks divestment in Q2FY27 and subsequent deconsolidation from Q3FY27.
- **DQ-ETERNAL-OCR-Q2FY25-food_nov (High):** Raster OCR misread `g281` corrected to `8281.0` via comparative cross-check.
- **DQ-ETERNAL-OCR-Q2FY25-going_out_nov (High):** Raster OCR misread `4582258888` corrected to `1562.0` via comparative cross-check.
