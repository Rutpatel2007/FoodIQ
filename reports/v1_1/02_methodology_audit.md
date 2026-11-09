# FoodIQ v1.1 — Financial Methodology Audit Report
**Report ID:** AUD-V11-02  
**Category:** Financial Methodology, Waterfalls & Comparability  
**Audit Date:** 2026-11-09  
**Status:** PASS  

---

## 1. Executive Summary

This audit assesses the methodological rigor of FoodIQ v1.1's financial analytics engine. The platform processes financial statements from Eternal Limited and Swiggy Limited, enforcing strict accounting separation, waterfall logic, and four-tier comparability constraints.

Key methodology achievements:
1. **Gross Order Value (GOV) vs Net Order Value (NOV) Waterfall:** Explicitly prevents illegitimate cross-metric comparisons. GOV includes customer delivery fees, platform fees, packaging fees, and taxes, while NOV represents merchandise value post-discounts.
2. **Margin Bridges & Take Rate Harmonization:** Segregates Marketplace Commission, Customer Delivery Charges, Advertising & Monetization Revenue, and Warehousing & Fulfilment Deductions.
3. **Unit Economics Formulations:** Mathematically standardizes order-level metrics and store-level productivity curves.
4. **Gap Attribution Architecture:** Implements additive variance decomposition across Price (AOV), Volume (Order Density), Take Rate, and Cost Structure.

---

## 2. Order Value Waterfall Architecture

Food delivery and quick commerce companies report aggregate transaction sizes under different accounting standards. FoodIQ v1.1 formalizes the following waterfall:

```
[Gross Merchandise Value (GMV) - List Price]
      │
      ├── (-) Merchant / Restaurant Funded Discounts
      │
[Net Order Value (NOV) - Transaction Merchandise Value]
      │
      ├── (+) Delivery Fees Paid by Consumer
      ├── (+) Platform & Convenience Fees
      ├── (+) Packaging & Processing Surcharges
      ├── (+) Applicable Indirect Taxes (GST)
      │
[Gross Order Value (GOV) - Total Customer Checkout Value]
```

### Institutional Rules:
- **Rule WF-01:** Never subtract Swiggy Food Delivery GOV from Blinkit NOV.
- **Rule WF-02:** When calculating take rates, the denominator must be explicitly labeled:
  $$	ext{GOV Take Rate} = rac{	ext{Segment Revenue}}{	ext{GOV}}$$
  $$	ext{NOV Take Rate} = rac{	ext{Segment Revenue}}{	ext{NOV}}$$

---

## 3. Four-Tier Comparability Framework

FoodIQ enforces four distinct comparability tiers across all financial queries:

| Tier | Classification | Permitted Operations | Examples |
|:---|:---|:---|:---|
| **Tier 1** | Directly Comparable | Ratio, Spread, Growth Differential, Correlation | Food Delivery GOV, Quick Commerce GOV, Consolidated Revenue, Dark Store Count |
| **Tier 2** | Standardized Adjusted | Adjusted Ratios, Bridge Analysis, Reconciliation | Contribution Margin (standardized for delivery fee subsidies) |
| **Tier 3** | Directionally Comparable | Rank Order, Trend Analysis, Indexing | Order Frequency, Active Monthly Transacting Users |
| **Tier 4** | Prohibited / Incomparable | Direct Subtraction Blocked, Warning Enforced | Blinkit NOV vs Swiggy Food GOV, Unadjusted EBITDA vs Adjusted EBITDA |

---

## 4. Margin Bridge & Unit Economics Formulation

### 4.1 Contribution Margin Bridge
$$	ext{Contribution Margin} = 	ext{Segment Revenue} - 	ext{Variable Delivery Costs} - 	ext{Customer Support} - 	ext{Payment Gateway Charges} - 	ext{Order-Linked Incentives}$$

### 4.2 Dark Store Throughput Formulation
$$	ext{Average Throughput (₹/store-day)} = rac{	ext{Quarterly GOV (or NOV)}}{	ext{Average Active Dark Stores} 	imes 	ext{Days in Quarter}}$$
$$	ext{Where Days in Quarter} = egin{cases} 90 & 	ext{Q4 (non-leap year)} \ 91 & 	ext{Q1, Q3} \ 92 & 	ext{Q2} \ 91.25 & 	ext{Blended Quarter Baseline} \end{cases}$$

---

## 5. Certification Conclusion
The financial methodology meets the highest standards of institutional equity research. Arbitrary metric substitutions and unadjusted apples-to-oranges comparisons are programmatically impossible within the engine.
