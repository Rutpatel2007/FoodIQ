# FoodIQ Phase 5: Scenario Simulation & Risk Modeling Methodology

## 1. Overview & Simulation Architecture

The **FoodIQ Scenario Lab** enables equity analysts and corporate strategists to model forward financial outcomes under alternative operating assumptions without corrupting historical reported observations.

### Key Architectural Safeguards:
1. **Dynamic Baseline:** Projections start from the latest reported quarterly disclosures (Q2 FY27), never hardcoded estimates.
2. **Pedigree Classification:** Every parameter is explicitly tagged with its evidentiary origin:
   - `EMPIRICAL_ESTIMATE_OLS`: Empirically calibrated from econometrically audited regressions.
   - `ANALYST_ASSUMPTION`: Discretionary sensitivity assumptions supplied by the researcher.
   - `MANAGEMENT_GUIDANCE`: Anchored in management's stated guidance corridors.
   - `HISTORICAL_AVERAGE`: Computed from historical averages across available quarters.
3. **Cross-Segment Isolation:** Quick commerce delivery dynamics are strictly segregated from Food Delivery.

---

## 2. Multi-Segment Simulation Framework

### 2.1 Quick Commerce Simulation
- **Volume Expansion:** $\text{NOV}_{t} = \text{NOV}_{t-1} \times (1 + g_{\text{quarterly}})$
- **Basket Size:** $\text{AOV}_t = \text{AOV}_{t-1} + \Delta \text{AOV}_{\text{quarterly}}$
- **Store Additions:** $\text{Stores}_t = \text{Stores}_{t-1} + \Delta \text{Stores}$
- **Throughput per Store-Day:**
  $$\text{Throughput}_t = \frac{\text{NOV}_t \times 10^7}{\text{Stores}_t \times 91.25}$$
- **Contribution Margin Trajectory (Swiggy):**
  $$\text{CM\%}_t = \text{Base CM\%} + \beta_{\text{OLS}} \times (\text{AOV}_t - \text{Base AOV}) / 100$$
  Where $\beta_{\text{OLS}} = 0.9506\text{ bps / ₹1 AOV increase}$.

### 2.2 Food Delivery Simulation
- **Volume Expansion:** $\text{GOV}_t = \text{GOV}_{t-1} \times (1 + g_{\text{quarterly}})$
- **EBITDA Margin:** $\text{EBITDA\%}_t = \text{Base EBITDA\%} + \Delta \text{Bps}_{\text{quarterly}} / 100$
- **Parameter Pedigree:** Explicitly labeled as `ANALYST_ASSUMPTION_NOT_EMPIRICAL_QC`.

---

## 3. Sensitivity Matrices & Break-Even Analytics

### 3.1 Two-Variable Sensitivity Matrix
Computes a $5 \times 5$ grid benchmarking target contribution profit or EBITDA against simultaneous changes in:
- Variable X: AOV change (-10% to +10%)
- Variable Y: Annualized Growth rate (10% to 30%)

### 3.2 Break-Even Threshold Analysis
Calculates the exact operational hurdle required to reach 0.0% contribution margin:
$$\Delta \text{AOV}_{\text{needed}} = \frac{-\text{Current CM\%} \times 100}{\beta_{\text{OLS}}}$$
$$\text{Breakeven AOV} = \text{Current AOV} + \Delta \text{AOV}_{\text{needed}}$$
For Swiggy Instamart at -1.0% CM and ₹708 AOV:
$$\Delta \text{AOV}_{\text{needed}} = \frac{-(-1.0) \times 100}{0.9506} = \mathbf{+₹105.20} \implies \text{Breakeven AOV} = \mathbf{₹813.20}$$

---

## 4. Monte Carlo Risk Simulation

To model uncertainty without fabricating arbitrary distributions:
- **AOV Change:** Modeled as $N(\mu=20, \sigma=15)$, bounded between $[-30, +70]$ INR.
- **Volume Growth:** Modeled as $N(\mu=22, \sigma=6)$, bounded between $[+5, +40]$ percent.
- **Iterations:** 1,000 reproducible simulation draws (seeded with $seed=42$).
- **Outputs:** Evaluates p10 (Bearish boundary), p50 (Median expectation), p90 (Bullish boundary), and the empirical probability of achieving positive contribution profit.
