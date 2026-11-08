# FoodIQ Phase 3 Limitations & Epistemic Boundaries

This document formalizes the methodological boundaries, unobservable data limitations, and epistemic constraints of the Phase 3 Competitive Intelligence Engine.

---

## 1. Unobservable Corporate Data

### 1.1 Blinkit Product-Level Cost of Goods Sold (COGS)
- **The Limitation:** Eternal Limited discloses Blinkit Adjusted Revenue post-Q1FY26 on a 1P inventory basis (gross merchandise selling price) without disclosing wholesale purchase costs, supplier rebates, or category gross margins.
- **Analytical Impact:** Constructing an exact "like-for-like" 3P marketplace revenue series for Blinkit post-Q1FY26 is impossible without proprietary vendor contracts. Any attempt by external analysts to subtract an estimated COGS represents speculative modeling rather than verifiable financial data.
- **Engine Policy:** FoodIQ classifies post-Q1FY26 revenue comparisons as `LEVEL_4_INCOMPARABLE` and strictly blocks direct mathematical subtractions.

### 1.2 Blinkit Quarterly Order Volumes
- **The Limitation:** Eternal does not disclose quarterly order volume or average order value for Blinkit in its shareholder letters.
- **Analytical Impact:** Exact head-to-head order density (orders per dark store per day) and per-order customer metrics (revenue per order, contribution per order, discount per order) cannot be computed for Blinkit.
- **Engine Policy:** Missing observations are preserved as `NULL` (`None`). Cross-company order proxies are prohibited.

---

## 2. Denominator Differences in Profitability Margins

### 2.1 Food Delivery Overhead Apportionment
- **The Limitation:** Zomato and Swiggy use different internal allocation methodologies to distribute corporate shared technology, human resources, legal, and headquarters costs across business segments.
- **Analytical Impact:** While both report Adjusted EBITDA margins on $GOV$, basis point spreads between Zomato's food margin (5.8%) and Swiggy's food margin (3.4%) reflect differing corporate cost allocation conventions in addition to true underlying operational profitability.
- **Engine Policy:** Food Delivery EBITDA margins are classified as `LEVEL_3_DIRECTIONALLY_COMPARABLE`. Directional trends are valid; absolute basis point spreads are indicative.

---

## 3. Epistemic Evidence Standards

To maintain research integrity, FoodIQ mandates that every output is stamped with an epistemic evidence tier:
1. `REPORTED FACT`: Auditable, verbatim disclosures from signed financial statements or shareholder letters.
2. `DERIVED FACT`: Exact mathematical transformations derived from reported facts using documented identities.
3. `MANAGEMENT EXPLANATION`: Forward commentary, strategic narratives, or rationale provided by corporate executives. Never treated as independently verified causation.
4. `ANALYST INTERPRETATION`: Rigorous deductive conclusions drawn from verified data, accompanied by stated assumptions.
5. `HYPOTHESIS`: Testable propositions regarding competitive dynamics requiring future data points.
6. `UNVERIFIED / INSUFFICIENT EVIDENCE`: Areas where public disclosures do not contain sufficient granularity to support definitive conclusions.
