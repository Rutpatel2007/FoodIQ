# FoodIQ Structural Break & Event Analysis Methodology (Phase 3)

This document specifies the accounting principles, event registers, and mathematical treatment for corporate structural breaks across Eternal Limited and Swiggy Limited.

---

## 1. Principles of Structural Break Governance

A corporate structural break occurs when a company changes its consolidation perimeter, commercial contracting model, or accounting presentation standard in a manner that renders historical time-series non-comparable without normalization.

FoodIQ enforces three core principles:
1. **Never fabricate unverified reconstructions:** If management does not disclose the necessary audit inputs (e.g. product-level wholesale purchase prices/COGS), external analysts must not fabricate an artificial "like-for-like" series. Incomparable periods must be explicitly labeled and blocked from direct subtraction.
2. **Distinguish temporal dates:** Every event distinguishes:
   - *Announcement Date:* When management publicly disclosed the transaction or shift.
   - *Effective Date:* When legal ownership or operational contracting changed.
   - *First Affected Reporting Quarter:* The first fiscal quarter whose published financial tables reflect the new treatment.
3. **Preserve multiple analytical views:** Separate series are maintained for reported headline numbers, verified organic like-for-like figures, and underlying physical volume metrics that remain economically invariant.

---

## 2. Event Deep Dive: Blinkit 1P Inventory Ownership Transition

### 2.1 The Commercial and Accounting Shift
- **Event ID:** `SB-001`
- **First Affected Reporting Quarter:** Q2 FY26 (Quarter ending September 30, 2025).
- **Accounting Standard:** Ind AS 115 / IFRS 15 (Revenue from Contracts with Customers — Principal vs. Agent Considerations).
  - *Pre-Q2 FY26 (Agent / 3P Model):* Blinkit connected independent sellers with consumers. Under paragraph B34-B38 of Ind AS 115, Blinkit did not control goods before transfer. Revenue was recognized as net commissions, delivery charges, and handling fees.
  - *Post-Q1 FY26 (Principal / 1P Model):* Blinkit restructured commercial contracts to purchase and hold inventory in its dark stores. Because Blinkit obtains physical control, bears inventory risk, and sets customer retail prices, Ind AS 115 mandates recognizing the **gross selling price** of merchandise as Adjusted Revenue.
- **Financial Consequence:**
  - Reported Adjusted Revenue surged from ₹1,061 Cr in Q1 FY26 to ₹2,423 Cr in Q2 FY26 (+128% QoQ, +312% YoY).
  - External wholesale revenue of Hyperpure dropped 55% QoQ (from ₹1,023 Cr to ₹460 Cr) because intercompany ingredient sales to Blinkit dark stores were eliminated in consolidation.

### 2.2 The 4 Analytical Series Architecture
To analyze Blinkit accurately without distortion, FoodIQ constructs 4 separate series:
1. **Series A — Reported Adjusted Revenue:**
   Presents published statutory numbers. Reflects the surge from ₹1,061 Cr to ₹2,423 Cr.
2. **Series B — Like-for-Like Revenue Assessment:**
   Because Eternal does not disclose product-level purchase invoices or merchant gross margins, constructing a synthetic 3P commission series requires arbitrary gross margin assumptions. FoodIQ classifies this series as `LFL_BLOCKED_UNAUDITED_COGS` and prohibits direct revenue subtractions against Swiggy Instamart (Level 4).
3. **Series C — Invariant Operating Measures:**
   Net Order Value ($NOV$) and operating dark store counts represent actual customer transacted volume and physical network footprint. These metrics remain economically valid across the transition:
   - Q1 FY26: Blinkit NOV ₹5,655 Cr vs Instamart NOV ₹3,900 Cr (1.45x scale).
   - Q2 FY26: Blinkit NOV ₹7,022 Cr vs Instamart NOV ₹4,600 Cr (1.53x scale).
4. **Series D — Profitability Margins with Native Denominators:**
   Blinkit Contribution Margin is maintained on its disclosed denominator ($NOV$), while Swiggy is tracked on $GOV$.

---

## 3. Event Deep Dive: District Entertainment Ticketing Acquisition

### 3.1 Inorganic Scope Expansion
- **Event ID:** `SB-002`
- **First Affected Reporting Quarter:** Q2 FY25 (Quarter ending September 30, 2024).
- **Transaction Overview:** Eternal acquired the entertainment ticketing business of One97 Communications (Paytm Insider and TicketNew) for an enterprise value of ₹2,048 Cr, closing on August 27, 2024.
- **Reporting Impact:**
  - Pre-acquisition Going-Out represented dining directory advertising, table reservations, and dining payment vouchers (Zomato Pay).
  - Post-acquisition Going-Out expanded to consolidate live concerts, movie ticketing, sports events, and theatrical bookings, rebranded as District.
  - Q2 FY25 reflected ~1 month of acquired operations; Q3 FY25 incorporated the full quarter.
- **Disclosed Like-for-Like Anchor:**
  - Headline reported Going-Out GOV grew **+171% YoY** in Q2 FY25.
  - Eternal management explicitly disclosed that organic like-for-like GOV growth excluding acquired ticketing was **+53% YoY**.
  - **FoodIQ Treatment:** The 53% organic anchor is preserved to isolate true dining directory demand from inorganic scope expansion.

---

## 4. Event Deep Dive: Swiggy Lynks Divestment & Deconsolidation

### 4.1 Supply Chain Perimeter Adjustment
- **Event ID:** `SB-003`
- **Effective Quarter:** Q2 FY27 (Closing September 30, 2026).
- **Deconsolidation Date:** Beginning Q3 FY27.
- **Transaction Overview:** Swiggy divested its controlling stake in Lynks Logistics. Lynks ceased to be consolidated in Swiggy's Supply Chain segment.
- **Financial Consequence:**
  - Eliminates ~₹20 Cr of quarterly adjusted EBITDA losses in the Supply Chain segment.
  - Reduces reported Supply Chain revenue run-rate by ~₹200 Cr per quarter.
- **FoodIQ Treatment:** Analysts are cautioned not to interpret the post-Q2FY27 EBITDA improvement in Supply Chain as recurring operational efficiency in restaurant procurement. It reflects the structural elimination of third-party trucking drag.
