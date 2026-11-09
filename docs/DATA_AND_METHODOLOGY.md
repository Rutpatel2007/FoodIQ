# FoodIQ — Financial & Quantitative Research Methodology

## 1. The Order Value Waterfall

Food delivery and quick commerce companies report aggregate transactions using diverging top-line metrics. FoodIQ establishes an explicit waterfall separating Gross Merchandise Value (GMV), Net Order Value (NOV), and Gross Order Value (GOV).

```text
  Gross Merchandise Value (GMV) [List Catalog Value]
  [-] Merchant / Restaurant Funded Discounts
  ===========================================
  Net Order Value (NOV) [Actual Transaction Flow]
  [+] Consumer Delivery Fees
  [+] Platform & Convenience Surcharges
  [+] Packaging Fees
  [+] Goods and Services Tax (GST)
  ===========================================
  Gross Order Value (GOV) [Total Customer Checkout Value]
```

### Governing Methodological Principles:
- **Take Rate Harmonization:** When calculating Take Rates, the denominator must be standardized. Eternal quotes Take Rate on NOV for Blinkit and GOV for Food Delivery. FoodIQ reports both:
  $$\text{Take Rate}_{\text{GOV}} = \frac{\text{Revenue}}{\text{GOV}}, \quad \text{Take Rate}_{\text{NOV}} = \frac{\text{Revenue}}{\text{NOV}}$$
- **Unpublished Fields:** Swiggy does not disclose Food Delivery NOV in quarterly statutory filings. FoodIQ stores `SWIGGY_FOOD_NOV` strictly as `NULL` and programmatically blocks direct subtraction against Blinkit NOV.

---

## 2. Four-Tier Comparability Framework

FoodIQ enforces four distinct comparability tiers across all analytical routines:

| Tier | Classification | Permitted Operations | Examples |
|:---:|:---|:---|:---|
| **Tier 1** | Directly Comparable | Ratios, spreads, growth differentials, regressions | Food Delivery GOV, Quick Commerce GOV, Consolidated Revenue, Dark Store Counts |
| **Tier 2** | Standardized Adjusted | Adjusted ratios, bridge reconciliations | Contribution Margin (adjusted for delivery subsidies) |
| **Tier 3** | Directionally Comparable | Rank order, trend analysis, indexing | Monthly Transacting Users (MTU), Order Frequency |
| **Tier 4** | Incomparable / Blocked | Direct subtraction blocked, warning raised | Blinkit NOV vs Swiggy Food GOV, Unadjusted vs Adjusted EBITDA |

---

## 3. Margin Bridges: Take Rate to Adjusted EBITDA

FoodIQ constructs an additive 5-step margin bridge for each operating segment:

$$\begin{aligned}
\text{Step 1: Gross Take Rate} & = \text{Marketplace Commissions} + \text{Customer Delivery Charges} + \text{Ad Tech Revenue} \\
\text{Step 2: (-) Variable Logistics} & = \text{Delivery Partner Pay} + \text{Packing Supplies} \\
\text{Step 3: (-) Payment & Support} & = \text{Payment Gateway (1.2–1.5\%)} + \text{Customer Support} \\
\text{Step 4: (=) Contribution Margin} & = \text{Take Rate} - \text{Variable Logistics} - \text{Payment/Support} \\
\text{Step 5: (-) Fixed Operating Overhead} & = \text{Dark Store Leases/Rent} + \text{Utilities} + \text{HQ/Corporate G&A} \\
\text{Step 6: (=) Segment Adjusted EBITDA} & = \text{Contribution Margin} - \text{Fixed Operating Overhead}
\end{aligned}$$

### Reconciled Example (Swiggy Instamart Q2 FY27):
- **Reported GOV:** ₹9,230 Cr
- **Contribution Margin:** -1.0% of GOV $\implies$ **-₹92.3 Cr** variable contribution deficit.
- **Segment Adjusted EBITDA Margin:** -9.7% of GOV $\implies$ **-₹895.0 Cr** total operating deficit (including ₹802.7 Cr of dark store leases, utilities, packing manpower, and overhead).

---

## 4. Dark Store Throughput Formulation

Network throughput measures the daily order value processed per operational dark store:
$$\text{Average Throughput (₹/store-day)} = \frac{\text{Quarterly Order Value}}{\text{Active Store Count} \times 91.25\text{ days}}$$

### Blinkit Q2 FY27 Verification:
$$\text{Throughput} = \frac{₹20,940 \times 10^7}{2,700 \times 91.25} = \mathbf{₹849,924\text{ / store-day}} \quad (\approx ₹8.50\text{ lakh/day})$$
*(Mature dark store cohorts > 12 months operate at ~₹11.20 lakh/day).*

---

## 5. Quantitative Research & Econometric Studies

Empirical quarterly series in Indian quick commerce span $N = 10 \text{ to } 14$ quarters. To eliminate spurious correlation and false discoveries, FoodIQ implements **First-Difference Detrending** and **Benjamini-Hochberg False Discovery Rate (FDR) Control** ($q = 0.05$).

### The 12 Empirical Studies:
1. `REL-001`: Dark Store Density vs Instamart Delivery Time ($r = -0.874, p = 0.0009$ — Significant)
2. `REL-002`: Blinkit AOV vs Contribution Margin ($r = +0.912, p = 0.0002$ — Significant)
3. `REL-003`: Instamart AOV vs Contribution Margin ($r = +0.940, p < 0.0001$ — Significant; OLS Slope $\beta = 0.9506$ bps/₹1)
4. `REL-004`: Food Delivery AOV vs Contribution Margin ($r = +0.825, p = 0.0033$ — Significant)
5. `REL-005`: Store Count vs Network Throughput ($r = +0.645, p = 0.0441$ — Non-Significant after FDR)
6. `REL-006`: Ad Monetization Take Rate vs CM ($r = +0.891, p = 0.0005$ — Significant)
7. `REL-007`: Zomato vs Swiggy Food GOV Spread ($r = +0.958, p < 0.0001$ — Significant)
8. `REL-008`: Quick Commerce vs Food Delivery GOV ($r = +0.982, p < 0.0001$ — Spurious Trend, detrended $r = 0.450$)
9. `REL-009`: Dark Store Additions vs Cash Flow Drag ($r = -0.763, p = 0.0102$ — Significant)
10. `REL-010`: MTU Growth vs Order Frequency ($r = +0.582, p = 0.0774$ — Non-Significant)
11. `REL-011`: Cross-Platform Quick Commerce Take Rate Divergence ($r = +0.844, p = 0.0021$ — Significant)
12. `REL-012`: Dark Store Scale vs Operating Leverage ($r = +0.887, p = 0.0006$ — Significant)

---

## 6. Management Credibility Scoring Engine

The platform tracks 26 corporate commitments across earnings calls, shareholder letters, and IPO filings.

$$\text{Strict Score} = \frac{\text{Delivered}}{\text{Delivered} + \text{Partial} + \text{Missed}} \times 100$$
$$\text{Broad Score} = \frac{\text{Delivered} + 0.5 \times \text{Partial}}{\text{Delivered} + \text{Partial} + \text{Missed}} \times 100$$

- **Eternal Limited (8 Commitments):** 6 evaluable (5 Delivered, 1 Partial, 0 Missed) $\implies$ **Strict: 83.33%**, **Broad: 91.67%**.
- **Swiggy Limited (18 Commitments):** 4 evaluable (3 Delivered, 1 Partial, 0 Missed), 11 pending unexpired IPO milestones, 3 qualitative $\implies$ **Strict: 75.00%**, **Broad: 87.50%**.
