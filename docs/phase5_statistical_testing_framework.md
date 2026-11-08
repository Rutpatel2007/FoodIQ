# FoodIQ Phase 5: Statistical Testing Framework & Econometric Diagnostics

## 1. Mathematical Formulas & Estimators

### 1.1 Pearson Correlation Coefficient ($r$) & Spearman Rank ($\rho$)
For a paired series of quarterly observations $(x_1, y_1), \dots, (x_N, y_N)$:
$$r = \frac{\sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^N (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^N (y_i - \bar{y})^2}}$$

### 1.2 Two-Tailed t-Distribution Significance Testing
$$t = r \sqrt{\frac{N - 2}{1 - r^2}}, \quad \text{Degrees of Freedom } df = N - 2$$
The two-tailed $p$-value is evaluated from the Student's $t$-cumulative distribution function:
$$p = 2 \times \left(1 - F_t(|t|, df)\right)$$

### 1.3 Fisher z-Transformation for 95% Confidence Intervals
To construct asymmetric, bounded confidence intervals for correlation:
$$z = \frac{1}{2} \ln \left(\frac{1 + r}{1 - r}\right) = \operatorname{arctanh}(r)$$
The standard error of $z$ is:
$$\operatorname{SE}_z = \frac{1}{\sqrt{N - 3}}$$
Constructing the 95% confidence interval on the $z$-scale:
$$z_{\text{low}} = z - 1.96 \times \operatorname{SE}_z, \quad z_{\text{high}} = z + 1.96 \times \operatorname{SE}_z$$
Back-transforming to correlation bounds:
$$r_{\text{low}} = \frac{e^{2 z_{\text{low}}} - 1}{e^{2 z_{\text{low}}} + 1}, \quad r_{\text{high}} = \frac{e^{2 z_{\text{high}}} - 1}{e^{2 z_{\text{high}}} + 1}$$

---

## 2. Detrending & First-Difference Testing

When two economic time-series both trend upward over time due to inflation, population growth, or platform maturity (e.g. AOV and Contribution Margin), standard levels regression routinely produces spurious high correlation ($r > 0.50$).

To test whether changes in variable $X$ genuinely accompany changes in variable $Y$, FoodIQ computes the **first-difference series**:
$$\Delta x_t = x_t - x_{t-1}, \quad \Delta y_t = y_t - y_{t-1}$$
The first-difference correlation is computed as:
$$r_{\Delta} = \operatorname{corr}(\Delta x, \Delta y)$$

### Institutional Case Study: Instamart AOV vs. CM
- **Levels Correlation:** $r = 0.5531, R^2 = 0.3059, p = 0.097$ (moderate-to-strong level co-movement).
- **First-Difference Correlation:** $r_{\Delta} = 0.1399, p = 0.72$.
- **Finding:** Quarter-on-quarter jumps in AOV do not synchronously drive quarter-on-quarter jumps in CM. Margin expansion compounds through warehouse automation and route density across multiple quarters.

---

## 3. Lag-1 Lead/Lag Diagnostics

To evaluate whether changes in operational inputs (e.g. dark store additions) precede subsequent margin changes with a one-quarter lag:
$$r_{\text{lag-1}} = \operatorname{corr}(x_{t-1}, y_t), \quad t \in \{2, \dots, N\}$$
Where positive, it indicates that investments in period $t-1$ begin yielding financial benefits in period $t$.
