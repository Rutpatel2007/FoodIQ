# FoodIQ Phase 5: Quantitative Research Methodology & Econometric Framework

## 1. Overview & Research Principles

A common failure in amateur financial data science is applying complex machine learning or high-dimensional black-box algorithms to small, non-stationary corporate time-series datasets. 

Corporate financial reports for newly listed companies like Eternal Limited and Swiggy Limited comprise a concise, high-value history of **10 fiscal quarters** (Q1 FY25 through Q2 FY27). On an $N=10$ sample, deep neural networks or 50-variable multi-collinear regressions will overfit and produce uninterpretable hallucinations.

**FoodIQ Phase 5** enforces transparent statistical methodology, econometric rigor, and economic reasoning:
- **Sample-Size Transparency:** Every statistical test explicitly discloses sample size ($N$).
- **Level vs. First-Difference Segregation:** Separates high level correlations ($r > 0.50$) from growth-rate change correlations ($r_{\Delta}$).
- **Multiple-Testing Correction:** Controls for False Discovery Rate (FDR) using the Benjamini-Hochberg procedure across all econometric relationship tests.
- **Strict Parameter Pedigrees:** Empirically calibrated parameters (e.g. Instamart OLS slope 0.9506 bps/₹1) are strictly isolated and never applied across different business models.

---

## 2. Statistical Analysis Dimensions

### 2.1 Growth, Acceleration & Volatility
For each financial and operational metric:
- **Quarter-on-Quarter (QoQ):** $\frac{X_t - X_{t-1}}{X_{t-1}} \times 100$ (safely suppressed if base $X_{t-1} \le 0$).
- **Year-on-Year (YoY):** $\frac{X_t - X_{t-4}}{X_{t-4}} \times 100$.
- **Growth Acceleration:** $\Delta \text{QoQ} = \text{QoQ}_t - \text{QoQ}_{t-1}$.
- **Coefficient of Variation (CV):** $\frac{\sigma}{\mu} \times 100$, quantifying operational volatility.

### 2.2 Relationship Studies Matrix
FoodIQ tracks 12 core operational relationships:
1. `AOV vs. Contribution Margin (Instamart)`: Tests basket-size fixed cost amortization.
2. `Dark Store Scale vs. Operating Margin (Blinkit)`: Tests network cluster density economics.
3. `Dark Store Scale vs. Contribution Margin (Instamart)`: Tests new store gestation drag.
4. `Food Delivery Scale vs. EBITDA Margin (Eternal)`: Tests delivery platform operating leverage.
5. `Food Delivery Scale vs. EBITDA Margin (Swiggy)`: Tests food operating leverage and gap convergence.
6. `Instamart Order Density vs. AOV`: Tests assortment depth and consumer basket expansion.
7. `Blinkit Store Count vs. Throughput per Store-Day`: Tests cannibalization vs cluster maturation.
8. `Food Take Rate vs. Food EBITDA Margin (Swiggy)`: Tests flow-through of advertising monetization.
9. `Quick Commerce Scale (NOV) vs. Loss per Order (Instamart)`: Tests unit loss contraction.
10. `Food MTU vs. Food GOV Growth (Eternal)`: Tests user growth vs order frequency drivers.
11. `Instamart Dark Store Count vs. NOV Scale`: Tests capital allocation to physical footprint.
12. `Blinkit Store Count vs. Disclosed NOV Scale`: Tests network expansion flow-through.

---

## 3. Multiple Testing & False Discovery Rate (FDR) Governance

When testing 12 distinct hypotheses simultaneously at $\alpha = 0.05$, the cumulative probability of at least one false positive (Type I error) under standard Bonferroni uncorrected testing is:
$$\text{Family-Wise Error Rate} = 1 - (1 - 0.05)^{12} \approx 46.0\%$$

To eliminate false discoveries without imposing overly punitive conservative bounds, FoodIQ applies the **Benjamini-Hochberg (BH) False Discovery Rate Procedure** at $q = 0.05$:
1. Order all $m$ tests by their $p$-values in ascending order: $P_{(1)} \le P_{(2)} \le \dots \le P_{(m)}$.
2. For each rank $k \in \{1, \dots, m\}$, calculate the BH critical threshold:
   $$\text{Threshold}_k = \left(\frac{k}{m}\right) \times q$$
3. Find the largest rank $k^*$ such that $P_{(k^*)} \le \text{Threshold}_{k^*}$.
4. Declare all hypotheses with rank $k \le k^*$ statistically significant.
