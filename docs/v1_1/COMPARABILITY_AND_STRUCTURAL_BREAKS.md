# FoodIQ v1.1 — Comparability Framework & Structural Breaks
**Document Reference:** DOC-V11-04  
**Classification:** Research Governance & Event Study Methodology  

---

## 1. Four-Tier Comparability Classification

To protect analysts from erroneous conclusions, FoodIQ enforces a four-tier comparability engine across all queries:

| Comparability Tier | Definition | Allowed Mathematical Operations | Examples |
|:---|:---|:---|:---|
| **Tier 1: Directly Comparable** | Standardized accounting definitions across both entities | Ratios, spreads, growth rates, regressions | Food Delivery GOV, Quick Commerce GOV, Consolidated Revenue |
| **Tier 2: Standardized Adjusted** | Comparable after mathematical adjustment for line item differences | Adjusted ratios, bridge reconciliations | Contribution Margin (adjusted for delivery subsidies) |
| **Tier 3: Directionally Comparable** | Different underlying sampling or disclosure cadence | Trend analysis, ordinal ranking | MTU, Order Frequency |
| **Tier 4: Non-Comparable** | Fundamental definition divergence; operations blocked | None (subtraction and ratios programmatically blocked) | Blinkit NOV vs Swiggy Food GOV |

---

## 2. Structural Breaks & Corporate Actions Registry

FoodIQ catalogs 12 structural events that altered reporting structures or baseline trajectories:

1. **BRK-001 (Blinkit Acquisition by Zomato - August 2022):** Shifted Eternal from pure-play food delivery into dual-engine quick commerce.
2. **BRK-002 (Platform Fee Introduction - August 2023):** Introduction of ₹2 to ₹10 convenience fee per order, expanding food delivery take rate by 60–110 bps.
3. **BRK-003 (Gold / One Membership Overhauls - FY24):** Restructuring loyalty free-delivery programs to curb delivery cost subsidies.
4. **BRK-004 (Swiggy IPO Listing - November 2024):** Transition from unlisted DRHP disclosures to audited quarterly public filings.
5. **BRK-005 (District App Separation - Q2 FY25):** Eternal spun out Going-Out and ticketing into a dedicated third app.
6. **BRK-006 to BRK-012:** Major dark store accelerated expansion waves (1,000 to 2,700 store rollout cycles).

---

## 3. Handling Breakpoints in Time Series
When computing rolling averages or longitudinal regressions spanning a structural break, FoodIQ automatically flags the discontinuity and offers piecewise regression or dummy variable controls ($D_{	ext{event}}$).
