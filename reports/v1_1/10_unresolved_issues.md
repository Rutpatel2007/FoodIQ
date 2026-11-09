# FoodIQ v1.1 — Unresolved Issues & Methodological Boundaries Report
**Report ID:** AUD-V11-10  
**Category:** Known Disclosures Gaps & Research Boundaries  
**Audit Date:** 2026-11-09  
**Status:** FULLY DISCLOSED AND GOVERNED  

---

## 1. Executive Summary

In adherence to institutional research integrity, FoodIQ v1.1 explicitly catalogues all structural data limitations and non-disclosures in public company reporting. Rather than interpolating or synthesizing missing numbers, FoodIQ transparently documents them as permanent research boundaries.

---

## 2. Inventory of Unresolved Disclosure Boundaries

### 1. Swiggy Food Delivery Net Order Value (NOV) Non-Disclosure
- **Boundary Description:** Swiggy discloses Food Delivery Gross Order Value (GOV) but does NOT publish Net Order Value (NOV) in statutory quarterly financial statements or shareholder letters.
- **FoodIQ Handling:** The field `SWIGGY_FOOD_NOV` remains strictly `NULL`.
- **Methodological Rule:** Cross-company subtraction between Blinkit NOV and Swiggy Food GOV is strictly blocked under Tier 4 Incomparable.

### 2. Private Status and Asymmetric Disclosures of Zepto
- **Boundary Description:** Zepto is a private, unlisted entity. It does not file quarterly shareholder letters with stock exchanges. Available figures derive from secondary funding press releases and MCA annual filings.
- **FoodIQ Handling:** Zepto data is sequestered in reference tables and excluded from statutory OLS econometric studies and management credibility scoring.

### 3. Swiggy Out-of-Home / Dineout Segment NOV
- **Boundary Description:** Swiggy reports Dineout transaction value as part of Out-of-Home GOV, but does not provide standalone segment NOV or customer delivery charges.
- **FoodIQ Handling:** Stored strictly as reported GOV without imputed deductions.

---

## 3. Risk Mitigation for Institutional Users

| Boundary | Analytical Risk | FoodIQ Programmatic Mitigation |
|:---|:---|:---|
| Unpublished Swiggy NOV | User attempts to compute take rate on NOV basis | System disables NOV take rate calculation for Swiggy Food Delivery |
| Zepto Private Status | False assumption of quarterly audit parity | System labels Zepto metrics with [UNAUDITED PRIVATE BENCHMARK] tag |
| Qualitative Commitments | Subjective scoring bias | Excluded from strict credibility scoring denominator |

---

## 4. Certification Conclusion
These boundaries represent structural constraints of corporate disclosure, not defects in FoodIQ. By maintaining strict disclosure discipline, FoodIQ protects researchers from synthetic artifacts.
