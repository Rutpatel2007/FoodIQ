# FoodIQ Research Limitations & Epistemic Caveats (Phase 2.1 Audit)

This document formalizes the empirical boundaries, sample size constraints, collinearity limitations, and modeling caveats governing all analytical outputs in FoodIQ.

---

## 1. Small Sample Size and Statistical Power

### 1.1 Quarterly Degrees of Freedom
- Corporate disclosures from Swiggy Limited cover 10 historical quarters (FY24 Q1 through FY26 Q2 / FY27 Q2).
- At sample size $n = 10$, statistical degrees of freedom for bivariate regressions and correlations are $df = n - 2 = 8$.
- For Lag-1 lead analysis, effective sample size drops to $n = 9$ ($df = 7$); for Lag-2, $n = 8$ ($df = 6$).
- **Statistical Consequence:**
  - Standard errors of correlation coefficients are inherently wide. Under Fisher's $z$-transformation, a correlation of $r = +0.55$ at $n=10$ yields a 95% confidence interval of $[-0.12, +0.87]$, spanning zero.
  - While Lag-2 correlation achieves $r = +0.9149$ ($p = 0.0014$, surviving Bonferroni correction at $\alpha = 0.0167$), the small number of time points renders the statistic sensitive to potential regime shifts.
  - **Platform Standard:** All statistical outputs are explicitly tagged as `EXPLORATORY_HYPOTHESIS_TESTING` rather than definitive causal laws.

---

## 2. Secular Trend Collinearity (Co-Trending Bias)

### 2.1 Level Correlations vs. First Differences
In rapid-growth consumer internet sectors, multiple operational metrics trend upward concurrently over multi-year horizons:
- Dark store networks expand $\to$ Geographic density increases $\to$ Assortment widens $\to$ AOV rises $\to$ Operating margins improve.
- High bivariate correlation between level series (e.g. $AOV_t$ vs. $CM_{t+2}$) may simply reflect this shared underlying secular trend (omitted variable bias: platform maturation and density expansion).
- **First-Difference Robustness Test:**
  When we detrend the series by testing quarterly increments ($\Delta AOV_t$ vs. $\Delta CM_t$), the correlation collapses:
  $$r_{\Delta} = +0.1399 \quad (p = 0.7196, \quad n=9)$$
- **Empirical Interpretation:**
  Quarter-to-quarter surges in AOV do **not** reliably produce immediate same-quarter or adjacent-quarter surges in margin. Long-term margin improvement is driven by dark store route density, warehouse automation, labor productivity, and advertising take rates, with AOV acting as one complementary factor among many.

---

## 3. Scenario Model Elasticity Grounding

### 3.1 Econometric Calibration vs. Simulation Assumptions
- The baseline specification parameter ($\epsilon = 3.0\text{ bps / ₹}$) represents an aggressive operational synergy scenario where higher basket sizes achieve maximal labor and vehicle amortization.
- Empirical OLS regression of Swiggy Instamart CM% on AOV over 10 quarters yields:
  $$\beta_{\text{OLS}} = 0.9506\text{ bps / ₹} \quad (R^2 = 0.3059, \quad SE = 0.506\text{ bps / ₹}, \quad p = 0.0974)$$
  - 95% Confidence Interval: $[-0.22, +2.12]\text{ bps / ₹}$.
- **Sensitivity Matrix Architecture:**
  FoodIQ avoids reliance on any single assumed parameter by providing a multi-tier sensitivity matrix:
  1. **Conservative:** $0.50\text{ bps / ₹}$ (minimal fixed cost leverage)
  2. **Baseline Empirical OLS:** $0.95\text{ bps / ₹}$ (empirically observed trend)
  3. **Upper Spec Illustrative:** $3.00\text{ bps / ₹}$ (idealized logistics density threshold)
- Users of the engine are cautioned that elasticity is an assumed simulation parameter, not an unvarying constant.

---

## 4. Partial-Quarter Dark Store Operating Bias

### 4.1 Period-End vs. Active-Store-Days Denominators
- Swiggy publishes dark store counts as period-end snapshots (e.g., 1,240 stores at the close of Q2 FY27).
- However, Swiggy's reported orders per store per day metric ($O / \text{store-day}$) is computed internally using **active store operating days** across the quarter.
- Stores opened in month 3 of a quarter contribute only ~30 operating days, whereas stores operating throughout contribute ~91.25 days.
- Dividing quarterly orders by period-end store counts ($O / (\text{Period-End Stores} \times 91.25)$) creates a downward bias during quarters of aggressive expansion.
- FoodIQ explicitly distinguishes:
  - `REPORTED_ACTIVE_STORE_DAYS_BASIS`: Official reported company throughput.
  - `DERIVED_PERIOD_AVERAGE_APPROXIMATION`: Orders divided by mean of beginning and ending store counts.
  - `DERIVED_PERIOD_END_APPROXIMATION`: Orders divided by ending store count.

---

## 5. Management Guidance Verification Horizons

### 5.1 Maturation Horizon Limits
- Out of 18 audited management guidance statements in corporate disclosures:
  - Only 3 commitments have reached their stated maturity date (FY26 GOV growth, May 2024 CM break-even, Q2 net store additions).
  - 12 commitments target future fiscal horizons (FY27, FY28, FY29, FY31).
  - 3 commitments are non-verifiable qualitative ambitions or vision statements.
- **Reporting Rule:** Unmatured milestones cannot be scored as delivered or missed. Delivery rates are evaluated with explicit strict (66.7%) and broad (83.3%) sensitivities over evaluable commitments only, with pending items reported separately.
