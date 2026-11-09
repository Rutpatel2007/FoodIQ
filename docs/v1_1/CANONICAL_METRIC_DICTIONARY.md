# FoodIQ v1.1 — Canonical Metric Dictionary
**Document Reference:** DOC-V11-02  
**Classification:** Metric Definitions & Standardization Standard  

---

## 1. Overview & Taxonomy

FoodIQ maintains a strict canonical dictionary of 85 metrics spanning Food Delivery, Quick Commerce (Instamart, Blinkit), B2B Supplies (Hyperpure), and Out-of-Home Dining.

Every metric possesses:
- A unique canonical identifier (`metric_id`).
- Standardized currency unit (`INR_CRORES`, `INR_ABSOLUTE`, `PERCENT`, `COUNT`).
- Comparability tier classification.
- Primary filing line item mapping.

---

## 2. Primary Financial Metrics

| Metric Identifier | Canonical Name | Segment | Unit | Denominator / Basis | Primary Source Line Item |
|:---|:---|:---|:---:|:---|:---|
| `GOV_CONSOLIDATED` | Consolidated Gross Order Value | Group | INR Cr | Total checkout value | Shareholder Letter KPI Table |
| `GOV_FOOD_DELIVERY` | Food Delivery Gross Order Value | Food | INR Cr | Customer checkout incl. taxes & fees | Segment Performance Highlights |
| `GOV_QUICK_COMMERCE`| Quick Commerce Gross Order Value | Quick Commerce | INR Cr | Customer checkout incl. taxes & fees | Segment Performance Highlights |
| `NOV_QUICK_COMMERCE`| Quick Commerce Net Order Value | Quick Commerce | INR Cr | Merchandise value post-discounts | Blinkit Financial Highlights |
| `REVENUE_ADJ` | Adjusted Revenue | Segment/Group | INR Cr | Statutory Revenue + Delivery Incentives | Management Reconciliation |
| `CM_PCT` | Contribution Margin % | Segment | % | % of Segment GOV (or NOV) | Contribution Profit / Segment GOV |
| `CM_VAL` | Contribution Profit / (Loss) | Segment | INR Cr | $GOV 	imes CM\%$ | Derived variable contribution |
| `EBITDA_ADJ_PCT` | Adjusted EBITDA Margin % | Segment/Group | % | % of Segment GOV | Segment EBITDA / Segment GOV |
| `EBITDA_ADJ_VAL` | Adjusted EBITDA | Segment/Group | INR Cr | $GOV 	imes EBITDA\%$ | Segment Operating Profit/(Loss) |

---

## 3. Operational & Unit-Economic Metrics

| Metric Identifier | Canonical Name | Segment | Unit | Definition Formula |
|:---|:---|:---|:---:|:---|
| `AOV` | Average Order Value | Segment | INR | $rac{	ext{Quarterly GOV}}{	ext{Total Completed Orders}}$ |
| `DARK_STORES_ACTIVE` | Period-End Dark Stores | Quick Commerce | Count | Physical operational micro-warehouses at period close |
| `DARK_STORES_AVG` | Period-Average Dark Stores | Quick Commerce | Count | $rac{	ext{Store Count}_{t-1} + 	ext{Store Count}_t}{2}$ |
| `STORE_THROUGHPUT` | Blended Store Throughput | Quick Commerce | INR / day | $rac{	ext{Quarterly NOV (or GOV)}}{	ext{Period-End Stores} 	imes 91.25	ext{ days}}$ |
| `TAKE_RATE_REV` | Revenue Take Rate | Segment | % | $rac{	ext{Segment Revenue}}{	ext{Segment GOV}} 	imes 100$ |
| `TAKE_RATE_DELIVERY`| Delivery Fee Take Rate | Segment | % | $rac{	ext{Customer Delivery Charges}}{	ext{Segment GOV}} 	imes 100$ |
| `TAKE_RATE_ADS` | Advertising Take Rate | Segment | % | $rac{	ext{Merchant Advertising Revenue}}{	ext{Segment GOV}} 	imes 100$ |

---

## 4. Grounding and Integrity Policy
If a corporate entity does not disclose a metric in official regulatory filings (e.g., Swiggy Food Delivery NOV), FoodIQ assigns `NULL`. The system strictly prohibits synthetic interpolation or cross-metric imputation.
