# FoodIQ Comparability Governance Framework & Findings (Phase 2.1 Audit)

This document formalizes the 4-tier comparability governance framework used throughout FoodIQ to prevent erroneous cross-company peer comparisons.

---

## 1. The 4-Tier Comparability Framework

| Tier | Code | Classification | Criteria & Standard | Permitted Operations |
|---|---|---|---|---|
| **Tier 1** | `L1` | **Directly Comparable** | Identical metric definition, accounting recognition standard, and reporting timeframe. | Direct subtraction, percentage spreads, ratios. |
| **Tier 2** | `L2` | **Comparable with Adjustment** | Reconcilable differences in denominator or presentation where adjustments are documented. | Subtraction permitted with published adjustment notes. |
| **Tier 3** | `L3` | **Directionally Comparable** | Different corporate overhead allocations or ESOP adjustments that cannot be mathematically harmonized. | Directional comparison only; exact spread tagged as indicative. |
| **Tier 4** | `L4` | **Incomparable / Blocked** | Economically or mathematically incompatible metrics. | Direct difference calculation is strictly **blocked**; surfaced with alert. |

---

## 2. Segment-by-Segment Audit Matrix

### 2.1 Food Delivery Segment
1. **Adjusted Revenue (`adj_revenue_cr`):**
   - *Classification:* `LEVEL_2_COMPARABLE_WITH_ADJUSTMENT` (`L2`)
   - *Audit Finding:* Both platforms operate marketplace agency models recognizing commissions, delivery fees, and advertising. Minor differences exist regarding customer loyalty program accounting (Zomato Gold subscription amortizations vs. Swiggy One allocations).
2. **Adjusted EBITDA (`adj_ebitda_cr`) & Margin (`adj_ebitda_margin_pct`):**
   - *Classification:* `LEVEL_3_DIRECTIONALLY_COMPARABLE` (`L3`)
   - *Audit Finding:* Zomato excludes ESOP expenses and corporate overhead costs from segment EBITDA differently than Swiggy's segment allocations. Directionally indicative of cash profitability, but basis point spreads reflect differing overhead allocation methodologies.
3. **Take Rate (`take_rate_pct`):**
   - *Classification:* `LEVEL_3_DIRECTIONALLY_COMPARABLE` (`L3`)
   - *Audit Finding:* Zomato reports take rate exclusively as a percentage of GOV. Swiggy discloses take rates on both GOV and NOV. Cross-comparison is aligned to GOV-based definitions.
4. **Monthly Transacting Users (`mtu_mn`):**
   - *Classification:* `LEVEL_2_COMPARABLE_WITH_ADJUSTMENT` (`L2`)
   - *Audit Finding:* Zomato defines Monthly Transacting Customers (MTC) as unique customers placing at least one order in a month. Swiggy defines MTU with slight variations regarding platform-wide cross-use. Direct comparison valid within ~5% tolerance.

---

### 2.2 Quick Commerce Segment (Blinkit vs. Instamart)
1. **Gross Order Value / Net Order Value:**
   - *Classification:* `LEVEL_1_DIRECTLY_COMPARABLE` (`L1`) when comparing GOV to GOV or NOV to NOV.
   - *Classification:* `LEVEL_4_INCOMPARABLE_BLOCKED` (`L4`) if comparing GOV to NOV.
2. **Operating Dark Stores (`dark_stores`):**
   - *Classification:* `LEVEL_1_DIRECTLY_COMPARABLE` (`L1`)
   - *Audit Finding:* Period-end physical dark store count is directly comparable. In Q2 FY27, Blinkit operated 2,700 stores vs. Instamart's 1,240 stores (+1,460 Blinkit lead).
3. **Adjusted Revenue (`adj_revenue_cr`):**
   - *Pre-Q2 FY26:* `LEVEL_2_COMPARABLE_WITH_ADJUSTMENT` (`L2`) — Both operating 3P agency models.
   - *Q2 FY26 onwards:* `LEVEL_4_INCOMPARABLE_BLOCKED` (`L4`) — Blinkit transitioned to 1P inventory recognition (gross sales recorded as revenue). Instamart maintained 3P marketplace commission recognition. Direct comparison is blocked.
4. **Contribution Margin (%):**
   - *Classification:* `LEVEL_3_DIRECTIONALLY_COMPARABLE` (`L3`)
   - *Audit Finding:* Blinkit reports CM% on Net Order Value ($NOV$); Swiggy reports CM% on Gross Order Value ($GOV$). For Swiggy, FoodIQ recomputes CM% on both GOV and NOV to permit defensible like-for-like analysis.

---

### 2.3 Out-of-Home & Supply Chain Segments
1. **District / Dining Out vs. Swiggy Dineout:**
   - *Classification:* `LEVEL_2_COMPARABLE_WITH_ADJUSTMENT` (`L2`)
   - *Audit Finding:* Reflects dining out vouchers, table reservations, and ticketing. Zomato's carve-out of District as a standalone consumer brand slightly shifts reporting boundaries relative to Swiggy Out-of-Home.
2. **Hyperpure vs. Swiggy Supply Chain:**
   - *Classification:* `LEVEL_2_COMPARABLE_WITH_ADJUSTMENT` (`L2`)
   - *Audit Finding:* Both operate B2B wholesale supply chain models to restaurants and dark stores. Inventory and logistics pricing mechanics are largely aligned under Ind AS 115.

---

## 3. Database & API Enforcement
- **Database Rules Table:** 15 active comparability rules seeded in `comparability_rules` table.
- **REST API Filter:** The `/api/v1/analytics/competitive-gaps` endpoint dynamically evaluates comparability tiers, sets `is_comparison_blocked = True`, nullifies raw mathematical differences for Level 4 comparisons, and appends the audited rule ID and warning note.
