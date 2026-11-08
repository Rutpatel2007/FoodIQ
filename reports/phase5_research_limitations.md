# FoodIQ Phase 5: Quantitative Research & Statistical Limitations

## 1. Small Sample Size (N = 10 Quarters)
- All statistical tests operate on a finite historical sample (Q1 FY25 to Q2 FY27).
- While Pearson r and Spearman rho capture directional co-movements, degrees of freedom ($df = N - 2 = 8$) mean critical t-values are high ($t_{crit} = 2.306$ at $lpha=0.05$).
- Machine learning, complex neural forecasting, and autoregressive integrated models are deliberately excluded to avoid catastrophic overfitting on a 10-point series.

## 2. Detrending and First-Difference Findings
- Variables with strong secular upward trends (e.g. AOV and Contribution Margin) exhibit high levels correlation ($r > 0.55$).
- First-difference testing ($\Delta Y \sim \Delta X$) removes macro trend co-movement and reveals that quarter-on-quarter changes are not synchronously coupled ($p = 0.72$).
- The platform reports both levels and differences to prevent false causal assertions.

## 3. Parameter Elasticity Segregation
- The empirical elasticity of 0.9506 bps per ₹1 AOV increase is strictly bounded to Swiggy Quick Commerce.
- Applying this parameter to Food Delivery, Eternal Blinkit, or Out-of-Home is strictly blocked at the analytics layer.
