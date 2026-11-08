# FoodIQ — Quantitative & Financial Research Methodology

## 1. Research Governance & Principles

FoodIQ enforces institutional research standards across all quantitative modeling, competitive attribution, and executive credibility analysis:
1. **Statutory Primacy:** All baseline facts originate from primary corporate filings (SEBI disclosures, quarterly shareholder letters, audited financial statements, IPO prospectuses). Secondary market commentary is strictly excluded.
2. **Deterministic Computation:** Analytical derivations (such as store throughput, contribution margin per order, and margin spreads) follow explicit formulas with complete mathematical lineage.
3. **Epistemic Classification:** Every analytical assertion is explicitly tagged into one of seven epistemic tiers:
   - `REPORTED_FACT`: Disclosed directly by company.
   - `DERIVED_FACT`: Reconciled calculation from reported facts.
   - `MANAGEMENT_EXPLANATION`: Management commentary or rationale.
   - `MANAGEMENT_COMMITMENT`: Forward-looking guidance or milestone.
   - `EMPIRICAL_ESTIMATE`: Statistically estimated parameter (e.g. OLS elasticity).
   - `ANALYST_ASSUMPTION`: Explicit scenario stress assumption.
   - `HYPOTHESIS`: Unverified empirical assertion.

---

## 2. Quantitative Econometric Framework

### 2.1 Correlation & Association Testing
For any paired quarterly series $(X_t, Y_t)$:
- **Pearson Product-Moment Correlation Coefficient ($r$):**
  $$r = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum (X_i - \bar{X})^2 \sum (Y_i - \bar{Y})^2}}$$
- **Spearman Rank Correlation ($\rho$):** Non-parametric monotonic dependence to protect against non-linear dynamics and outliers.
- **Statistical Significance ($p$-value):** Two-tailed Student's $t$-test with $N - 2$ degrees of freedom:
  $$t = r \sqrt{\frac{N - 2}{1 - r^2}}$$
- **Fisher $z$-Transformation 95% Confidence Intervals:**
  $$z = \frac{1}{2} \ln \left( \frac{1+r}{1-r} \right), \quad \text{SE}_z = \frac{1}{\sqrt{N - 3}}$$
  $$\text{CI}_{95\%} = \tanh \left( z \pm 1.96 \cdot \text{SE}_z \right)$$

### 2.2 First-Difference Detrending ($r_\Delta$)
To prevent spurious correlation arising from shared macro-economic time trends or concurrent business scaling, FoodIQ computes first-difference correlations:
$$\Delta X_t = X_t - X_{t-1}, \quad \Delta Y_t = Y_t - Y_{t-1}$$
$$r_\Delta = \text{Corr}(\Delta X_t, \Delta Y_t)$$
A relationship is confirmed as a direct synchronous operational driver **only if both $r$ and $r_\Delta$ remain statistically significant**.

### 2.3 Multiple-Testing Controls (Benjamini-Hochberg FDR)
To prevent Type I error inflation across 12 simultaneous econometric studies:
1. Sort raw $p$-values in ascending order: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$ where $m = 12$.
2. Calculate the Benjamini-Hochberg critical value for each rank $k$:
   $$c_k = \frac{k}{m} \times q^*, \quad \text{with } q^* = 0.05$$
3. Find the largest $k$ such that $p_{(k)} \le c_k$. All hypotheses with $p \le p_{(k)}$ are declared statistically significant at a false discovery rate of 5%.

---

## 3. Management Credibility & Delivery Scoring

### 3.1 Taxonomy of Evaluation
Management forward-looking statements are tracked across 16 categories and evaluated against empirical outcomes using a 7-tier taxonomy:
1. `DELIVERED`: Objective threshold fully achieved within guided timeframe.
2. `PARTIALLY_DELIVERED`: Significant progress achieved (>70% of target) or delivered with moderate delay.
3. `MISSED`: Quantitative target not achieved, or timeline expired without fulfillment.
4. `PENDING`: Target date remains in the future (e.g. IPO prospectus commitments for FY28).
5. `NOT_OBJECTIVELY_MEASURABLE`: Qualitative vision without quantitative milestones.
6. `WITHDRAWN_OR_SUPERSEDED`: Target formally retracted or revised by subsequent disclosures.
7. `INSUFFICIENT_EVIDENCE`: Corporate disclosure discontinued before verification.

### 3.2 Denominator-Isolated Scorecard Formulas
To prevent penalizing companies for active multi-year commitments, pending targets are isolated:
$$\text{Evaluated Commitments} = N_{\text{DELIVERED}} + N_{\text{PARTIALLY\_DELIVERED}} + N_{\text{MISSED}}$$
$$\text{Strict Delivery Rate} = \frac{N_{\text{DELIVERED}}}{\text{Evaluated Commitments}} \times 100$$
$$\text{Broad Delivery Rate} = \frac{N_{\text{DELIVERED}} + 0.5 \times N_{\text{PARTIALLY\_DELIVERED}}}{\text{Evaluated Commitments}} \times 100$$

---

## 4. Multi-Segment Scenario Simulation Lab

### 4.1 Parameter Pedigree Isolation
Parameters are categorized to prevent confounding empirical estimates with subjective assumptions:
- `EMPIRICAL_ESTIMATE_OLS`: Derived from statistical regression (e.g. Instamart CM elasticity of $0.9506 \text{ bps} / \text{₹1}$).
- `MANAGEMENT_GUIDANCE`: Disclosed corporate milestone (e.g. 2,000 dark stores).
- `ANALYST_ASSUMPTION_NOT_EMPIRICAL_QC`: Stress testing parameters chosen for sensitivity exploration.

### 4.2 Monte Carlo Uncertainty Simulation
- 1,000 independent random draws using Gaussian distributions centered around base assumptions with empirical standard errors.
- Generates 10th percentile, 50th percentile (median), and 90th percentile outcome boundaries for projected Gross Order Value and Contribution Margins.
