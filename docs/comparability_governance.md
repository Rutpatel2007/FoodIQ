# FoodIQ — Financial Comparability Governance Specification

## 1. The Comparability Problem
Eternal and Swiggy compete in overlapping Indian consumer internet markets, but their financial disclosures differ significantly:
- Companies report different headline order values (**Gross Order Value vs. Net Order Value**).
- Denominators for profitability margins differ (**% of GOV vs. % of NOV vs. % of Revenue**).
- Segment perimeters vary (Swiggy separates Supply Chain; Eternal separates Hyperpure).
- Strategic business model changes create **structural breaks in revenue recognition** (Blinkit 1P inventory switch in Q2 FY26).

FoodIQ implements a rules-based financial governance engine in the backend to prevent invalid, misleading, or mathematically incorrect comparisons.

---

## 2. Four-Tier Comparability Classification

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FOODIQ COMPARABILITY TIERS                      │
├─────────────────┬──────────────────────────────────────────────────────┤
│ Tier            │ Rule & Governance Restriction                        │
├─────────────────┼──────────────────────────────────────────────────────┤
│ DIRECT          │ Metrics share identical economic & IndAS accounting  │
│                 │ definitions. Direct comparison and subtraction valid.│
├─────────────────┼──────────────────────────────────────────────────────┤
│ ADJUSTED        │ Metrics differ by known formula or denominator basis. │
│                 │ Comparison permitted only after documented adjustment│
├─────────────────┼──────────────────────────────────────────────────────┤
│ DIRECTIONAL     │ Underlying business trends align, but absolute       │
│                 │ numbers are not directly comparable. Dual axes req.  │
├─────────────────┼──────────────────────────────────────────────────────┤
│ INCOMPARABLE    │ Structurally non-equivalent economic quantities.     │
│                 │ Single-axis cross plotting is strictly blocked.      │
└─────────────────┴──────────────────────────────────────────────────────┘
```

---

## 3. Core Enforced Rules

### Rule 1: Food Delivery Order Values (GOV vs. NOV)
- **Swiggy Metric:** Food Delivery GOV (Gross Order Value). Swiggy explicitly does not disclose Food Delivery NOV.
- **Eternal Metric:** Food Delivery NOV (Net Order Value). Historical GOV was disclosed only up to Q1FY26.
- **Governance Enforcement:** Direct subtraction or single-axis comparison is **BLOCKED (`INCOMPARABLE`)**. The platform renders split dual-axis visualizations with explicit warnings.

### Rule 2: Blinkit Q2 FY26 1P Transition (Revenue Structural Break)
- **Accounting Shift:** In Q2 FY26, Blinkit changed from a pure marketplace agency model to an owned inventory model for a substantial portion of merchandise.
- **Impact on Adjusted Revenue:**
  - Q1 FY26 Blinkit Adjusted Revenue: ₹2,400 Cr.
  - Q2 FY26 Blinkit Adjusted Revenue: ₹9,891 Cr (**+312% QoQ, +756% YoY**).
  - Simultaneously, Hyperpure B2B supplies dropped from ₹2,295 Cr to ₹1,023 Cr (-55% QoQ) due to the elimination of intercompany wholesale billing.
- **Governance Enforcement:** Raw post-Q1FY26 revenue comparisons between Blinkit and Instamart are **BLOCKED (`INCOMPARABLE`)**. Analytical models must use **Like-for-Like (LFL) Adjusted Revenue** (which subtracts merchandise COGS).

### Rule 3: Margin Denominators
- Swiggy reports Contribution Margin and Adjusted EBITDA Margin as **% of GOV**.
- Eternal reports Adjusted EBITDA as absolute ₹ Cr or as **% of GOV / NOV**.
- **Governance Enforcement:** Margins are labeled with their denominator basis (`% of GOV` or `% of NOV`). Ratios with different denominators are never directly subtracted without normalisation.

### Rule 4: Quick Commerce Dark Store Throughput
- Swiggy computes Orders per Store per Day using **active store-days**.
- Dividing total quarterly orders by closing period-end store count creates an artificially depressed throughput estimate during rapid expansion quarters.
- **Governance Enforcement:** System enforces active store-days math or explicitly flags exit store approximations.
