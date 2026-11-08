# FoodIQ — Canonical Data Dictionary

This document specifies the canonical financial and operating metrics tracked, derived, and governed within FoodIQ.

---

## 1. Core Financial & Operating Metrics

| Metric Key | Canonical Name | Unit | Formula / Definition | Comparability Level | Source Disclosure Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `gov` | Gross Order Value | INR Cr | Total monetary value of all orders placed by customers, inclusive of taxes, delivery fees, and customer packaging. | **LEVEL_1** | Disclosed by both Eternal and Swiggy across Food and Quick Commerce. |
| `orders_count` | Total Orders | Millions | Total count of completed customer deliveries within the period. | **LEVEL_1** | Disclosed directly or derived via $\text{GOV} / \text{AOV}$. |
| `aov` | Average Order Value | INR | Mean Gross Order Value per customer order: $\text{GOV} / \text{Orders}$. | **LEVEL_1** | Directly disclosed in shareholder letters. |
| `revenue` | Reported Revenue | INR Cr | Statutory revenue from operations recognised in accordance with Ind AS 115. | **LEVEL_4 (QC)** / **LEVEL_2 (Food)** | **Incomparable in Quick Commerce** after Blinkit's transition to 1P merchant-of-record model in Q2 FY26. |
| `take_rate_pct` | Revenue Take Rate | % of GOV | Statutory Revenue expressed as a percentage of Gross Order Value: $(\text{Revenue} / \text{GOV}) \times 100$. | **LEVEL_4 (QC)** / **LEVEL_2 (Food)** | Subject to revenue accounting divergence in Quick Commerce. |
| `contribution_margin_inr` | Contribution Margin | INR Cr | Order-level profit after direct delivery, packaging, gateway, and fulfillment costs, before general corporate overhead. | **LEVEL_2** | Reconciled across both firms with minor adjustments. |
| `contribution_margin_pct` | Contribution Margin % | % of GOV | Contribution Margin expressed as a percentage of Gross Order Value: $(\text{CM} / \text{GOV}) \times 100$. | **LEVEL_2** | Key measure of unit economic viability. |
| `adj_ebitda_inr` | Adjusted EBITDA | INR Cr | Operating earnings before interest, tax, depreciation, amortisation, and exceptional items. | **LEVEL_3** | Directionally comparable. Excludes ESOP and corporate overhead in Eternal; includes certain shared costs in Swiggy. |
| `adj_ebitda_margin_pct` | Adj. EBITDA Margin % | % of GOV | Adjusted EBITDA expressed as a percentage of Gross Order Value. | **LEVEL_3** | Governed by Level 3 rule: directional spread analysis permitted; raw subtraction requires disclosure reconciliation. |
| `active_dark_stores` | Active Dark Stores | Count | Total operational micro-warehouses / dark stores active at end of quarter. | **LEVEL_1** | Directly disclosed by Blinkit and Instamart. |
| `store_throughput_daily` | Dark Store Daily Throughput | INR / store-day | Average Net/Gross Order Value processed per dark store per day: $(\text{Quarterly GOV/NOV} \times 10^7) / (\text{Stores} \times 91.25)$. | **LEVEL_2** | Reconciled metric. Requires using disclosed NOV for Blinkit and GOV for Instamart. |

---

## 2. 4-Tier Comparability Classification System

1. **LEVEL 1 — Directly Comparable:**
   - Both companies define, calculate, and report the metric using identical accounting principles and economic boundaries.
   - *Examples:* Gross Order Value (GOV), Active Dark Store Count, Food Delivery AOV.
2. **LEVEL 2 — Comparable with Documented Adjustment:**
   - Underlying economic concepts match, but minor reporting differences (e.g. 91.25 days per quarter, customer packaging inclusions) require standardized normalization.
   - *Examples:* Contribution Margin, Dark Store Daily Throughput, MTUs.
3. **LEVEL 3 — Directionally Comparable:**
   - Structural differences in overhead allocation, ESOP exclusion, or non-cash items exist. Directional trends and spreads are valid, but exact mathematical subtraction carries accounting noise.
   - *Examples:* Adjusted EBITDA Margin % of GOV, Segment Take Rates.
4. **LEVEL 4 — Incomparable / Blocked:**
   - Fundamental accounting or business model divergence renders mathematical comparison economically invalid and misleading. Subtractions are blocked by the system.
   - *Examples:* Quick Commerce Reported Revenue (Blinkit 1P gross inventory accounting vs. Swiggy Instamart 3P net commission marketplace accounting).

---

## 3. Database Entity Schema Summary

- `companies`: Primary key `id` (`ETERNAL`, `SWIGGY`), `name`, `cin`, `incorporation_year`.
- `source_documents`: Primary key `id`, `company_id`, `doc_type`, `fiscal_year`, `fiscal_quarter`, `file_hash`.
- `source_pages`: Composite foreign key to `source_documents`, `page_number`, `ocr_text`, `quality_score`.
- `business_segments`: Primary key `id`, `company_id`, `segment_code`, `segment_name`.
- `metric_definitions`: Primary key `metric_name`, `canonical_name`, `formula`, `unit_type`.
- `metric_observations`: Primary key `id`, `company_id`, `segment_id`, `metric_id`, `fiscal_year`, `fiscal_quarter`, `value_numeric`, `source_page_id`, `confidence_score`.
- `comparability_rules`: Primary key `rule_id`, `metric_name`, `segment`, `comparability_level`, `governance_note`.
- `saved_scenarios`: Primary key `id`, `scenario_name`, `parameters_json`, `results_json`, `created_at`.
