# FoodIQ Phase 6 — End-to-End User Workflows Guide

This document specifies the step-by-step operation of the five primary research workflows built into the FoodIQ Research Workstation.

---

## Workflow A — Competitive Research & Gap Attribution

**Analytical Objective:** Investigate why Eternal and Swiggy exhibit diverging profitability in Food Delivery despite operating in the same duopoly market.

1. **Accessing the Workspace:**
   - Click the **Competitive** tab in the main navigation (or click `Workflow A` in the top workflow toolbar).
2. **Reviewing the Findings Matrix:**
   - Locate **Finding 6: Food Delivery Adjusted EBITDA Margin Divergence**.
   - Note the reported 242 bps margin spread (Eternal: 3.86% vs Swiggy: 1.44% in Q2 FY25).
3. **Checking Comparability Governance:**
   - Scroll to the **Comparability Governance Matrix**.
   - Identify the rule for `adj_ebitda_margin_pct` in Food Delivery.
   - Note that it is classified as **Level 3 (Directionally Comparable)**: Eternal excludes share-based payment expense (ESOP) and corporate overhead allocations, whereas Swiggy includes certain corporate costs. Direct subtraction is informative directionally but requires analytical adjustment for exact parity.
4. **Inspecting Historical Time-Series:**
   - Switch to the **Food Delivery Core** workspace tab.
   - The interactive canvas chart renders the multi-quarter trajectory of Food Delivery GOV, AOV, take rates, and contribution margins for both firms.
5. **Verifying Evidence Lineage:**
   - Click the citation link on Finding 6 to open the Audit Modal, viewing the exact source filings and shareholder letters.

---

## Workflow B — Management Execution & Credibility Audit

**Analytical Objective:** Evaluate whether corporate management teams reliably deliver on guidance, or systematically over-promise.

1. **Accessing the Workspace:**
   - Click the **Credibility** tab (or click `Workflow B`).
2. **Reviewing the Guidance Scorecards:**
   - Inspect the **Eternal Limited Guidance Scorecard**:
     - Strict Delivery Rate: **83.33%** (5 Delivered out of 6 evaluable).
     - Broad Delivery Rate: **91.67%** (including 1 Partially Delivered).
     - Matured commitments: 6; Pending multi-year targets: 2.
   - Inspect the **Swiggy Limited Guidance Scorecard**:
     - Strict Delivery Rate: **75.00%** (3 Delivered out of 4 evaluable).
     - Broad Delivery Rate: **87.50%** (including 1 Partially Delivered).
     - Matured commitments: 4; Pending multi-year targets: 11 (from IPO prospectus).
3. **Examining Commitment Lifecycle:**
   - In the **Commitments Register**, filter by company or status (`DELIVERED`, `MISSED`, `PENDING`).
   - Click on Deepinder Goyal's commitment: *"Blinkit target to reach 2,000 stores by end of 2026"* (Status: `DELIVERED` - Target achieved early by Q2 FY27 with 2,700 stores guided).
4. **Exploring Strategic Initiatives:**
   - Click on the **Narratives** tab to review the 7 tracked strategic initiatives, including Swiggy Bolt (10-minute food delivery) and Eternal District (lifestyle ticketing app).

---

## Workflow C — Quantitative Research & Econometric Validation

**Analytical Objective:** Test whether industry narratives (e.g., "AOV expansion drives quick commerce margin turnaround") survive rigorous econometric testing.

1. **Accessing the Workspace:**
   - Click the **Quantitative** tab (or click `Workflow C`).
2. **Inspecting the 12 Econometric Studies:**
   - View the table displaying Pearson $r$, Spearman $\rho$, $p$-values, Fisher $z$ 95% Confidence Intervals, OLS slopes, and detrended first-difference correlations ($r_\Delta$).
3. **Evaluating Study 2 (Swiggy Instamart AOV vs. Contribution Margin):**
   - **Level Correlation:** $r = 0.5531$, $p = 0.0972$ (Statistically weak at $\alpha = 0.05$).
   - **First-Difference Correlation:** $r_\Delta = 0.1399$, $p_\Delta = 0.7194$ (Completely uncorrelated!).
   - **Econometric Conclusion:** Synchronous quarter-on-quarter jumps in Instamart AOV do **not** explain same-quarter margin expansion. The observed level correlation is driven by secular shared time trends and store maturation, not pure order-size elasticity.
4. **Reviewing Multiple-Testing Controls:**
   - Note the **Benjamini-Hochberg FDR** column ($q = 0.05$). Only 5 of the 12 relationships survive false-discovery rate correction.

---

## Workflow D — Scenario Simulation & Break-Even Modelling

**Analytical Objective:** Simulate future financial outcomes under varying operational assumptions while enforcing parameter pedigree isolation.

1. **Accessing the Workspace:**
   - Click the **Scenarios** tab (or click `Workflow D`).
2. **Selecting Presets:**
   - Click **Load Base Case**, **Load Bull Case**, or **Load Bear Case** to populate segment growth and margin assumptions.
3. **Testing Instamart Break-Even:**
   - View the automated **Break-Even Analysis Card**: Instamart requires an AOV of **₹813.20** (an increase of ₹315.20 from current ₹498.00) at current cost structures to achieve break-even contribution margin.
4. **Simulating Custom Trajectories:**
   - Adjust the **Swiggy Instamart AOV** slider to ₹600.
   - Adjust the **Dark Stores** target to 1,200.
   - Notice the real-time re-computation of Projected GOV (₹7,200 Cr) and Contribution Margin (-0.93%).
5. **Evaluating Monte Carlo Uncertainty:**
   - Review the **1,000-Draw Monte Carlo Simulation Distribution** displaying the 10th percentile, median, and 90th percentile bounds.
6. **Saving Custom Scenarios:**
   - Click **Save Scenario**, enter a descriptive scenario name (e.g., `FY26_Instamart_Optimization`), and confirm. The scenario is saved into the SQLite database.

---

## Workflow E — Source Verification & Lineage Tracing

**Analytical Objective:** Independently verify an analytical finding against its primary statutory disclosure and physical PDF page.

1. **Accessing the Workspace:**
   - Click the **Lineage** tab (or click `Workflow E`).
2. **Tracing Finding 1 (Blinkit Store Throughput):**
   - Finding 1 proves Blinkit store throughput grew +22.0% (from ₹6.96L to ₹8.50L/store-day).
   - Click on the source filing citation `ETERNAL-Q2FY25-SHL-p14`.
3. **Inspecting Primary Source Document:**
   - The Audit Modal opens displaying:
     - Document Title: *Eternal Limited Q2 FY25 Shareholder Letter*
     - Fiscal Period: Q2 FY25
     - Physical Page: Page 14
     - Extracted Content Snippet: *"Blinkit Net Order Value grew to ₹4,061 Cr with 639 active stores..."*
     - Exact Verification Formula: $(4061 \times 10^7) / (639 \times 91.25) = 696,482 \text{ INR/store-day}$.
