# FoodIQ v1.1 — Quantitative Research & Econometric Methodology
**Document Reference:** DOC-V11-05  
**Classification:** Econometrics, Statistics & Simulation Specification  

---

## 1. Econometric Framework for Small-N Horizons

In Indian internet corporate research, empirical time series span 10 to 14 quarters. Standard regression analysis in small samples faces two major threats:
1. **Spurious Correlation:** Two trending series (e.g., store count and consolidated revenue) will yield high $R^2$ even if no economic causality exists.
2. **Multi-Hypothesis Testing:** Testing dozens of metric combinations inevitably yields low p-values by random chance.

FoodIQ resolves both through **First-Difference Detrending** and **Benjamini-Hochberg False Discovery Rate (FDR) Control**.

---

## 2. Benjamini-Hochberg Step-Down Procedure

For a family of $M = 12$ simultaneous relationship studies:
1. Sort raw p-values: $P_{(1)} \le P_{(2)} \le \dots \le P_{(M)}$.
2. Compute the Benjamini-Hochberg critical value for each rank $i$:
   $$Q_i = rac{i}{M} 	imes lpha \quad (lpha = 0.05)$$
3. Identify the largest index $k$ such that $P_{(k)} \le Q_k$.
4. Declare all hypotheses $H_{(1)}, \dots, H_{(k)}$ statistically significant after FDR adjustment.

---

## 3. The 12 Empirical Relationship Studies

| Study ID | Independent Variable ($X$) | Dependent Variable ($Y$) | Economic Mechanism | FDR Verdict |
|:---:|:---|:---|:---|:---:|
| `REL-001` | Dark Store Density (stores/$km^2$) | Instamart Delivery Time (min) | Proximity reduces transit time | **Significant** |
| `REL-002` | Blinkit AOV (₹) | Contribution Margin (bps) | Fixed packing/delivery cost absorption | **Significant** |
| `REL-003` | Instamart AOV (₹) | Contribution Margin (bps) | Unit economic leverage | **Significant** |
| `REL-004` | Food Delivery AOV (₹) | Food Delivery CM (bps) | Basket size efficiency | **Significant** |
| `REL-005` | Active Dark Stores | Network Average Throughput | Saturation vs scale effects | Not Sig |
| `REL-006` | Ad Monetization Take Rate (%) | Contribution Margin (bps) | Pure gross margin flow-through | **Significant** |
| `REL-007` | Zomato Food GOV | Swiggy Food GOV | Duopoly competitive spread | **Significant** |
| `REL-008` | Quick Commerce GOV | Food Delivery GOV | Consumer wallet share shift | Spurious Trend |
| `REL-009` | Dark Store Additions ($\Delta N$) | Cash Burn / Free Cash Flow | Capex & initial opex drag | **Significant** |
| `REL-010` | Monthly Transacting Users | Order Frequency | Engagement deepening | Not Sig |
| `REL-011` | Blinkit Take Rate | Instamart Take Rate | Pricing power divergence | **Significant** |
| `REL-012` | Dark Store Network Scale | Group Operating Leverage | Central G&A cost dilution | **Significant** |

---

## 4. Scenario Simulation Engine

FoodIQ provides two simulation modalities:
1. **Deterministic Elasticity Modeling:** Leverages empirical OLS coefficients ($eta$) to test targeted changes in AOV, Take Rate, or Store additions.
2. **Monte Carlo Simulation:** Runs 10,000 parameter iterations across stochastic distributions (Normal, Log-Normal, Triangular) to generate probabilistic confidence bands for future EBITDA and cash flow.
