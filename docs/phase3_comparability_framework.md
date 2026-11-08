# FoodIQ Formal Comparability Framework (Phase 3)

This document formalizes the 4-tier comparability governance framework used throughout FoodIQ to prevent erroneous cross-company peer comparisons between Eternal Limited and Swiggy Limited.

---

## 1. Governance Philosophy & Standards

In consumer internet platforms, companies often use identical financial labels (e.g., "Adjusted Revenue", "Take Rate", "EBITDA Margin") to describe economically divergent reporting boundaries. Direct comparisons without harmonization lead to severe analytical errors:
- Gross Merchandise billing vs. Net Commission agency billing.
- Order values gross of customer vouchers vs. net order values.
- Segment overhead allocations vs. corporate unallocated costs.

The FoodIQ Comparability Framework establishes 4 mandatory tiers that govern all analytical queries, charts, and API endpoints.

---

## 2. Four-Tier Classification Architecture

### LEVEL 1 — DIRECTLY COMPARABLE (`L1`)
- **Criteria:** Economic definitions, units, reporting scope, and underlying accounting bases are fully aligned.
- **Allowed Operations:** Direct mathematical subtraction, spread calculation, ratio analysis, and peer rankings.
- **Examples:**
  - `dark_stores`: Physical period-end active dark store count.
  - `nov_cr`: Net Order Value for Quick Commerce where both platforms report transacted merchandise flow net of customer promotional vouchers.
  - `gov_cr`: Food Delivery Gross Order Value (checkout value before vouchers and platform discounts).

### LEVEL 2 — COMPARABLE WITH ADJUSTMENT (`L2`)
- **Criteria:** Direct comparison is valid only after applying a documented, reproducible mathematical adjustment or normalization.
- **Allowed Operations:** Subtraction and ratio analysis permitted accompanied by published adjustment notes.
- **Examples:**
  - `mtu_mn`: Monthly Transacting Customers (Eternal) vs Monthly Transacting Users (Swiggy), valid within ~5% deduplication tolerance.
  - `adj_revenue_cr` (Quick Commerce pre-Q2FY26): Both platforms operated 3P agency commission models with minor delivery fee presentation differences.
  - `OutOfHome` Revenue: Requires isolating the inorganic ticketing contribution from Eternal's Paytm Insider acquisition (Q2 FY25).

### LEVEL 3 — DIRECTIONALLY COMPARABLE (`L3`)
- **Criteria:** Trends, growth rates, and operational trajectories may be compared, but absolute magnitudes or accounting presentation boundaries differ.
- **Allowed Operations:** Trajectory, correlation, and directional comparisons only. Direct level subtractions are tagged as indicative. Peer rankings on levels are blocked.
- **Examples:**
  - `adj_ebitda_margin_pct` (Food Delivery): Both report margins on GOV, but internal ESOP expense exclusions and shared tech/corporate overhead apportionments differ.
  - `take_rate_pct`: Eternal defines take rate on GOV net of certain customer discounts; Swiggy reports total take rate gross of delivery fee markups.

### LEVEL 4 — INCOMPARABLE (`L4`)
- **Criteria:** Underlying economic definitions or accounting recognition standards are incompatible.
- **Allowed Operations:** Direct mathematical subtraction and peer ranking are **strictly prohibited**. The engine nullifies raw mathematical differences and surfaces prominent structural break warnings.
- **Examples:**
  - `adj_revenue_cr` (Quick Commerce Q2FY26 onwards): Blinkit transitioned to 1P principal inventory ownership (gross sales recognized as revenue), whereas Swiggy Instamart operates on 3P marketplace commission recognition. Raw subtraction yields an artificial ~₹2,000+ Cr gap reflecting accounting conventions, not commercial volume.
  - `cross_gov_nov_subtraction`: Direct subtraction of Net Order Value from Gross Order Value across platforms.

---

## 3. Comparability Registry Summary

| Segment | Metric | Classification | Code | Adjustment / Governance Note |
|---|---|---|---|---|
| **Quick Commerce** | `dark_stores` | Directly Comparable | `L1` | Period-end physical active operating dark store count. |
| **Quick Commerce** | `nov_cr` | Directly Comparable | `L1` | Net merchandise value after customer vouchers. |
| **Quick Commerce** | `adj_revenue_cr` (Pre-Q2FY26) | Comparable with Adjustment | `L2` | 3P agency marketplace commission model. |
| **Quick Commerce** | `adj_revenue_cr` (Q2FY26+) | **INCOMPARABLE (BLOCKED)** | `L4` | **STRUCTURAL BREAK:** Blinkit 1P inventory recognition vs Swiggy 3P commission. |
| **Food Delivery** | `gov_cr` | Directly Comparable | `L1` | Gross platform customer checkout value. |
| **Food Delivery** | `gov_vs_nov` | **INCOMPARABLE (BLOCKED)** | `L4` | Direct cross-subtraction between GOV and NOV is strictly prohibited. |
| **Food Delivery** | `adj_ebitda_margin_pct` | Directionally Comparable | `L3` | Internal shared overhead and corporate cost allocations differ. |
| **Food Delivery** | `take_rate_pct` | Directionally Comparable | `L3` | Differing presentation of customer delivery fee gross-ups. |
| **Food Delivery** | `mtu_mn` | Comparable with Adjustment | `L2` | Monthly transacting customers vs monthly transacting users. |
| **Going-Out** | `adj_revenue_cr` | Comparable with Adjustment | `L2` | Requires adjusting for Paytm ticketing acquisition in Q2 FY25. |
| **Supply Chain** | `adj_revenue_cr` | Comparable with Adjustment | `L2` | Requires adjusting for Lynks divestment (Q2 FY27) and Hyperpure 1P eliminations. |
