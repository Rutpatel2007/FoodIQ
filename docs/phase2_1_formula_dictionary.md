# FoodIQ Formula Dictionary & Mathematical Specification (Phase 2.1)

This document specifies the exact mathematical identities, definitions, units, boundary constraints, and prohibited operations across the FoodIQ financial intelligence platform.

---

## 1. Growth Quality Decomposition Engine

### 1.1 Gross Order Value (GOV) Identity
In corporate disclosures, Gross Order Value ($GOV$) represents total customer checkout value before platform vouchers, discounts, and customer fees:
$$GOV_t = \frac{\text{Total Orders}_t (\text{mn}) \times \text{AOV}_t (\text{₹})}{10.0} \quad [\text{₹ Cr}]$$
*Scale Factor:* Division by $10.0$ converts $(\text{Millions of Orders} \times \text{Rupees}) = 10^6 \times \text{₹}$ to $\text{Crores}$ ($10^7\text{ ₹}$).

### 1.2 Exact 4-Term Waterfall Decomposition
Between consecutive quarters $t-1$ and $t$, the quarterly change in disclosed $GOV$ ($\Delta GOV_t = GOV_t - GOV_{t-1}$) is decomposed as:
$$\Delta GOV_t \equiv \text{Volume Effect}_t + \text{Basket Effect}_t + \text{Interaction Effect}_t + \text{Residual}_t$$

Where:
1. **Volume Effect (Order Count Expansion at Prior AOV):**
   $$\text{Volume Effect}_t = \frac{(O_t - O_{t-1}) \times AOV_{t-1}}{10.0} \quad [\text{₹ Cr}]$$
2. **Basket Effect (AOV Expansion at Prior Order Volume):**
   $$\text{Basket Effect}_t = \frac{O_{t-1} \times (AOV_t - AOV_{t-1})}{10.0} \quad [\text{₹ Cr}]$$
3. **Interaction Effect (Simultaneous Order & Basket Delta):**
   $$\text{Interaction Effect}_t = \frac{(O_t - O_{t-1}) \times (AOV_t - AOV_{t-1})}{10.0} \quad [\text{₹ Cr}]$$
4. **Disclosure Rounding Residual:**
   $$\text{Residual}_t = \Delta GOV_t - (\text{Volume Effect}_t + \text{Basket Effect}_t + \text{Interaction Effect}_t) \quad [\text{₹ Cr}]$$

### 1.3 Boundary Constraints & Prohibited Operations
- **Strict Rule on NOV Decomposition:** Swiggy and Eternal disclose $AOV \equiv \frac{GOV}{\text{Orders}}$. Therefore, $AOV$ cannot be applied to Net Order Value ($NOV$). Decomposing $NOV$ with $GOV$-based $AOV$ is strictly blocked (`INELIGIBLE_INVALID_METRIC_BASIS`).
- **Missing Disclosures:** Segments lacking disclosed quarterly order counts or AOVs (e.g., Blinkit, Hyperpure) are classified as `INELIGIBLE_MISSING_DISCLOSURES`. Under no circumstances are missing values coerced to zero.

---

## 2. Contribution Margin Bridge Engine

### 2.1 Accounting Identity
For segments reporting Contribution Margin ($CM\%$) on $Topline$ ($GOV$ for Swiggy; $NOV$ for Blinkit):
$$CM\%_t = \frac{\text{Contribution Profit}_t}{\text{Topline}_t} \times 100$$
$$\Delta CM(\text{bps})_t = (CM\%_t - CM\%_{t-1}) \times 100$$

### 2.2 Partial Accounting Identity Bridge
When detailed operational cost sub-components (delivery costs, dark store rent, packaging, merchant incentives) are not separately disclosed in shareholder letters, the margin change is bridged to disclosed take rates:
$$\Delta CM(\text{bps})_t \equiv \text{Take Rate Effect (bps)}_t + \text{Unallocated Operational Efficiency Effect (bps)}_t + \text{Residual}_t$$

Where:
$$\text{Take Rate Effect (bps)}_t = (\text{Take Rate}\%_t - \text{Take Rate}\%_{t-1}) \times 100$$
$$\text{Unallocated Operational Efficiency Effect (bps)}_t = \Delta CM(\text{bps})_t - \text{Take Rate Effect (bps)}_t$$
$$\text{Residual}_t \equiv 0.0\text{ bps}$$

- **Classification:** Strictly labeled as `PARTIAL_ACCOUNTING_IDENTITY_BRIDGE`. Unallocated residual efficiency is never attributed to specific unverified causal buckets.

---

## 3. Unit Economics Engine

### 3.1 Segment-Matched Metrics
All per-order metrics are evaluated strictly on segment-matched order counts:
1. **Adjusted Revenue per Order:**
   $$\text{Revenue per Order}_t = \frac{\text{Adjusted Revenue}_t (\text{₹ Cr}) \times 10.0}{\text{Segment Orders}_t (\text{mn})} \quad [\text{₹ / order}]$$
2. **Contribution Profit per Order:**
   $$\text{Contribution per Order}_t = \frac{\text{AOV}_t \times CM\%_t}{100.0} \quad [\text{₹ / order}]$$
3. **Adjusted EBITDA per Order:**
   $$\text{EBITDA per Order}_t = \frac{\text{Adjusted EBITDA}_t (\text{₹ Cr}) \times 10.0}{\text{Segment Orders}_t (\text{mn})} \quad [\text{₹ / order}]$$
4. **Voucher / Subsidy per Order:**
   $$\text{Subsidy per Order}_t = \frac{(GOV_t - NOV_t) \times 10.0}{\text{Segment Orders}_t (\text{mn})} \quad [\text{₹ / order}]$$

### 3.2 Throughput per Operating Store-Day
$$\text{Throughput per Store-Day} = \frac{NOV_t (\text{₹ Cr}) \times 10^7}{\text{Stores}_t \times 91.25\text{ days}} \quad [\text{₹ / store-day}]$$
- Denominator represents period-average or period-end active store counts over an idealized 91.25-day quarter ($365 / 4$).

---

## 4. Statistical Lead-Lag & Predictive Engine

### 4.1 Pearson Product-Moment Correlation
$$r = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2 \sum_{i=1}^n (y_i - \bar{y})^2}}$$
- Degrees of freedom: $df = n - 2$.
- Test statistic: $t = r \sqrt{\frac{n - 2}{1 - r^2}}$.
- $p$-value: Two-tailed student's $t$-distribution with $df = n - 2$.

### 4.2 Fisher $z$-Transformation 95% Confidence Interval
$$z = \frac{1}{2} \ln\left(\frac{1 + r}{1 - r}\right) = \operatorname{arctanh}(r)$$
$$SE_z = \frac{1}{\sqrt{n - 3}}$$
$$z_{\text{lower}} = z - 1.96 \cdot SE_z, \quad z_{\text{upper}} = z + 1.96 \cdot SE_z$$
$$r_{\text{lower}} = \tanh(z_{\text{lower}}), \quad r_{\text{upper}} = \tanh(z_{\text{upper}})$$

### 4.3 Multiple Testing & Secular Detrending
- **Bonferroni Adjusted Significance:** Across $m=3$ quarterly lag hypotheses (Lag-0, Lag-1, Lag-2), family-wise significance threshold is:
  $$\alpha_{\text{adjusted}} = \frac{0.05}{3} \approx 0.0167$$
- **First-Difference Detrending Test:**
  $$\Delta x_t = x_t - x_{t-1}, \quad \Delta y_t = y_t - y_{t-1}$$
  $$r_{\Delta} = \operatorname{corr}(\Delta x_t, \Delta y_t)$$
  Tests whether quarterly accelerations in AOV immediately correlate with quarterly margin expansions, stripping out secular multi-year upward trends.

---

## 5. Scenario & Sensitivity Model Engine

### 5.1 Sensitivity Formula
$$\Delta AOV \in \{0, 20, 40, 60, 80, 100\}\text{ ₹}$$
$$\text{Projected } GOV_t = \frac{\text{Current Orders}_t \times (\text{Current } AOV_t + \Delta AOV)}{10.0} \quad [\text{₹ Cr}]$$
$$\text{Projected } CM\% = \text{Current } CM\% + \left(\frac{\Delta AOV \times \epsilon_{\text{bps}}}{100.0}\right) \quad [\%]$$
$$\text{Gap to Break-Even (bps)} = (\text{Projected } CM\% - 0.0) \times 100$$
$$\text{Quarters to Parity} = \frac{\Delta AOV}{\text{Historical Quarterly } AOV \text{ Velocity}}$$

### 5.2 Calibrated Elasticity Tiers
1. **Conservative:** $\epsilon = 0.50\text{ bps / ₹}$
2. **Baseline Empirical OLS:** $\epsilon = 0.95\text{ bps / ₹}$ ($R^2 = 0.3059$, $SE = 0.506\text{ bps / ₹}$, $95\%\text{ CI: } [-0.22, 2.12]$)
3. **Upper Specification Scenario:** $\epsilon = 3.00\text{ bps / ₹}$ (Aggressive operational scale assumption)

---

## 6. Management Guidance Credibility Scorer

### 6.1 Outcome Taxonomy
- $\text{DELIVERED}$: Verifiable disclosure achieves or exceeds stated numeric milestone.
- $\text{MISSED}$: Verifiable disclosure fails to achieve milestone within specified timeframe.
- $\text{PARTIALLY\_DELIVERED}$: Milestone achieved in discrete exit period (e.g. single month) but full quarterly period average fell short.
- $\text{PENDING}$: Target quarter or fiscal period remains in the future.
- $\text{NOT\_OBJECTIVELY\_MEASURABLE}$: Qualitative ambition or aspirational statement without verifiable numeric milestone.

### 6.2 Credibility Scoring Formulas
$$\text{Evaluable Commitments} = N_{\text{DELIVERED}} + N_{\text{MISSED}} + N_{\text{PARTIALLY\_DELIVERED}}$$
$$\text{Strict Delivery Rate} = \frac{N_{\text{DELIVERED}}}{\text{Evaluable Commitments}} \times 100\%$$
$$\text{Broad Delivery Rate} = \frac{N_{\text{DELIVERED}} + 0.5 \times N_{\text{PARTIALLY\_DELIVERED}}}{\text{Evaluable Commitments}} \times 100\%$$
