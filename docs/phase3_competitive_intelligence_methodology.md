# FoodIQ Competitive Intelligence & Attribution Methodology (Phase 3)

This document specifies the quantitative methods, dimensional gap models, and attribution algorithms powering the FoodIQ Competitive Intelligence Engine.

---

## 1. Multi-Dimensional Competitive Advantage Model

FoodIQ evaluates corporate performance between Eternal Limited and Swiggy Limited across eight distinct competitive dimensions:

1. **Scale Advantage:**
   Measures absolute transacted customer volume and network footprint ($GOV$, $NOV$, $MTU$, $Dark\ Stores$).
   $$\text{Scale Ratio} = \frac{\text{Eternal Volume}}{\text{Swiggy Volume}}$$
2. **Growth Advantage:**
   Measures organic customer demand velocity (QoQ and YoY growth rates on matched metrics), stripping out inorganic M&A bumps.
   $$\text{Growth Spread (pts)} = \text{Eternal YoY Growth}\% - \text{Swiggy YoY Growth}\%$$
3. **Monetisation Advantage:**
   Measures platform revenue extraction per unit of order flow (Take Rates, merchant advertising penetration, platform convenience fees).
4. **Unit Economics Advantage:**
   Measures per-order contribution profit and throughput per operating store-day.
   $$\text{Throughput Spread} = \text{Blinkit Throughput / Store-Day} - \text{Instamart Throughput / Store-Day}$$
5. **Profitability Advantage:**
   Measures operating leverage conversion into cash generation (Adjusted EBITDA, Adjusted EBITDA margin %, quarterly break-even trajectory).
6. **Network Productivity Advantage:**
   Evaluates dark store density, expansion velocity, and store area productivity (revenue/sq ft).
7. **Customer & Engagement Advantage:**
   Tracks transacting user counts (MTU/MTC), user order frequencies, and multi-service engagement.
8. **Capital Efficiency Advantage:**
   Assesses cash EBITDA generation relative to capex and dark store expansion pace.

---

## 2. Competitive Gap Attribution Algorithm

Between Eternal ($A$) and Swiggy ($B$) for any metric $m$ at quarter $t$:

### 2.1 Absolute and Relative Spreads
$$\text{Absolute Gap}_t = A_{m, t} - B_{m, t}$$
$$\text{Relative Gap}\%_t = \frac{A_{m, t} - B_{m, t}}{|B_{m, t}|} \times 100\% \quad (\text{if } B_{m, t} \ne 0)$$

### 2.2 Quarter-over-Quarter Trajectory
$$\Delta \text{Gap}_t = \text{Absolute Gap}_t - \text{Absolute Gap}_{t-1}$$
$$\text{Trajectory}_t = \begin{cases}
\text{EXPANDING} & \text{if } |\text{Absolute Gap}_t| > |\text{Absolute Gap}_{t-1}| \\
\text{CONTRACTING} & \text{if } |\text{Absolute Gap}_t| < |\text{Absolute Gap}_{t-1}| \\
\text{STABLE} & \text{otherwise}
\end{cases}$$

### 2.3 Strict Governance Blocking
If the metric comparison is classified as `LEVEL_4_INCOMPARABLE` under the Comparability Framework:
- $\text{Absolute Gap}_t \gets \text{None}$
- $\text{Relative Gap}\%_t \gets \text{None}$
- $\text{Direction} \gets \text{"INCOMPARABLE\_ACCOUNTING\_BREAK"}$
- $\text{Leader} \gets \text{"BLOCKED"}$
- The raw unadjusted difference is preserved only in audit fields (`gap_absolute_unadjusted_raw`) alongside prominent accounting explanations.

---

## 3. Absence of Arbitrary Composite Scores

Conventional dashboards frequently compute an unweighted or arbitrarily weighted "overall score" to declare a single "winning" company. FoodIQ explicitly prohibits arbitrary composite ranking because:
1. Different metrics possess different comparability tiers (L1 cannot be averaged with L3).
2. Capital allocation trade-offs (e.g. trading near-term EBITDA for 2x dark store footprint) cannot be ranked objectively without subjective investor risk preferences.
3. Every dimension must stand on its own empirical merits.
