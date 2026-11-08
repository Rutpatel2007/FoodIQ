# FoodIQ Phase 4: Management Credibility & Narrative Verification Methodology

## 1. Overview & Research Philosophy

A central failure of superficial financial dashboarding is treating executive forward guidance and qualitative management commentary as either unquestioned ground truth or irrelevant public relations. 

**FoodIQ Phase 4** establishes an institutional-grade, evidence-backed framework to systematically record, track, evaluate, and verify management statements over time.

Rather than collapsing management credibility into a simplistic, arbitrary single number (e.g. "8.5/10"), FoodIQ evaluates execution through transparent, separate indicators:
- **Strict Delivery Rate:** Ratio of fully delivered commitments to evaluable completed commitments.
- **Broad Delivery Rate:** Delivery rate crediting partial delivery with 50% weight.
- **Narrative Verification Tiers:** Empirical testing of whether qualitative explanations match subsequent financial and operational observations.
- **Commitment Volume & Evaluability:** Disclosing what proportion of management statements are objectively verifiable vs aspirational.

---

## 2. Statement Repository & 16-Category Classification

Every management statement in FoodIQ is indexed with verbatim quotations, speaker identification, primary document name, and physical PDF page numbers across 16 categories:

1. `FINANCIAL_GUIDANCE`: Top-line consolidated or segment revenue and order targets.
2. `GROWTH_COMMITMENTS`: Explicit YoY or QoQ growth rates for GOV, NOV, or revenue.
3. `PROFITABILITY_TARGETS`: Segment and consolidated break-even or profit milestones.
4. `CONTRIBUTION_MARGIN_TARGETS`: Segment contribution margin corridors (e.g. Instamart 0 to -1.0%).
5. `ADJUSTED_EBITDA_TARGETS`: Adjusted EBITDA targets as % of GOV or in absolute INR Cr.
6. `STORE_EXPANSION_COMMITMENTS`: Dark store footprint milestones (e.g. Blinkit 1,000 stores by FY25).
7. `CUSTOMER_ENGAGEMENT_TARGETS`: Monthly transacting user (MTU) or active customer ambitions.
8. `ORDER_GROWTH_FREQUENCY_EXPECTATIONS`: Orders per customer or orders per store-day benchmarks.
9. `AOV_MONETISATION_EXPECTATIONS`: Average Order Value expectations and take rate milestones.
10. `CAPEX_INVESTMENT_PLANS`: Capital expenditure outlays, QIP proceeds usage, and liquidity targets.
11. `OPERATIONAL_EFFICIENCY_INITIATIVES`: Per-order cost savings, warehouse pick times, route pooling.
12. `STRATEGIC_INITIATIVES`: Core programmatic pivots (e.g. Blinkit 1P, Swiggy Bolt, District).
13. `MARKET_EXPANSION_PLANS`: City additions, geographic clustering, Tier-2/Tier-3 rollout.
14. `COMPETITIVE_POSITIONING_CLAIMS`: Claims of market share leads or structural moats.
15. `MANAGEMENT_EXPLANATIONS_OF_PAST_PERFORMANCE`: Retrospective attributions of margin/growth changes.
16. `FORWARD_LOOKING_EXPECTATIONS`: Qualitative multi-year perspectives and vision statements.

---

## 3. Commitment Lifecycle Engine

Every forward-looking commitment moves through a formal 5-stage lifecycle:
```
[ANNOUNCED] ──> [ACTIVE] ──> [DUE] ──> [EVALUATED] ──> [CLOSED]
```

### The 7-Tier Outcome Taxonomy
1. `DELIVERED`: Target fully met or exceeded within the specified timeframe.
2. `PARTIALLY_DELIVERED`: Meaningful operational progress achieved or milestone met in single exit month, but fell slightly short of full-quarter average.
3. `MISSED`: Failed to meet the target within the matured evaluation window.
4. `PENDING`: Target period has not yet matured (e.g. FY28 medium-term targets). **Strictly excluded from failure calculations**.
5. `NOT_OBJECTIVELY_MEASURABLE`: Aspirational vision statements or qualitative ambitions lacking measurable metrics or fixed dates.
6. `WITHDRAWN_OR_SUPERSEDED`: Target formally retracted or replaced with revised guidance in subsequent filings.
7. `INSUFFICIENT_EVIDENCE`: Disclosures lack the necessary metric to evaluate outcome independently.

---

## 4. Empirical Evaluation Governance

1. **Target Maturation Rule:** A commitment must NEVER be labeled `MISSED` simply because it is currently unachieved if its stated target horizon lies in the future.
2. **Denominator Isolation:** The denominator for delivery rates consists solely of `Evaluable Completed` commitments ($\text{Delivered} + \text{Partially Delivered} + \text{Missed}$). Pending and unmeasurable claims are reported separately.
3. **Anti-Aspiration Rule:** Qualitative statements (e.g. "aiming to be a beloved brand") are never converted into synthetic numeric targets.
