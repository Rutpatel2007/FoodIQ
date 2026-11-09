# FOODIQ — Financial & Research Methodology Handbook
**Document Reference:** `FOODIQ-METH-FIN-2026-11`  
**Governing Accounting Standards:** Ind AS 115 (Revenue from Contracts with Customers), Ind AS 108 (Operating Segments), SEBI LODR Regulations  
**Econometric Rigor Level:** Institutional Quantitative Standard (First-Difference Detrending & Benjamini-Hochberg FDR Control)

---

## 1. Financial Metric Formula Dictionary

### 1.1 Gross Order Value (GOV) vs. Net Order Value (NOV)

#### Formula & Identity:
$$\text{GOV} = \sum (\text{Item Price} + \text{Packaging} + \text{Delivery Charges} + \text{Taxes}) - \text{Discounts}$$
$$\text{NOV} = \text{GOV} - \text{Customer Taxes} - \text{Discounts Funded by Platform}$$

- **Unit:** INR Crores (₹ Cr).
- **Primary Disclosure Context:**
  - **Swiggy:** Discloses **GOV** across both Food Delivery and Quick Commerce (Instamart).
  - **Eternal:** Discloses **GOV** for Food Delivery, but discloses **NOV** for Quick Commerce (Blinkit).
- **Comparability Rule:** Direct subtraction $(\text{Instamart GOV} - \text{Blinkit NOV})$ is **strictly blocked (Level 4 Incomparable)**. They represent different economic scopes.

---

### 1.2 Waterfall Growth Decomposition (Zero Residual Proof)

#### Exact Mathematical Formulation:
Let base period be $t=0$ and final period be $t=1$:
$$\text{NOV}_0 = Q_0 \cdot P_0, \quad \text{NOV}_1 = Q_1 \cdot P_1$$
$$\Delta \text{NOV} = \text{NOV}_1 - \text{NOV}_0 = (Q_0 + \Delta Q)(P_0 + \Delta P) - Q_0 P_0$$
$$\Delta \text{NOV} = \underbrace{(\Delta Q \cdot P_0)}_{\text{Pure Volume Effect}} + \underbrace{(Q_0 \cdot \Delta P)}_{\text{Pure Basket Size (AOV) Effect}} + \underbrace{(\Delta Q \cdot \Delta P)}_{\text{Simultaneous Interaction Effect}}$$

- **Residual:** $\text{Residual} = \Delta \text{NOV} - (\text{Volume} + \text{AOV} + \text{Interaction}) \equiv \mathbf{0.00\text{ Cr}}$.
- **Validity:** Valid across any pair of historical quarters where Order Volumes ($Q$) and Average Order Values ($P$) are disclosed in primary filings.

---

### 1.3 Contribution Margin vs. Segment Adjusted EBITDA

#### Contribution Margin (CM %):
$$\text{CM \%} = \frac{\text{Reported Revenue} - \text{Variable Delivery Costs} - \text{Payment Gateway Costs}}{\text{Order Flow Denominator (GOV or NOV)}} \times 100$$

#### Segment Adjusted EBITDA Margin (%):
$$\text{Adj. EBITDA \%} = \frac{\text{Contribution Profit} - \text{Dark Store Lease/Rent} - \text{Store Utilities/Labor} - \text{Marketing}}{\text{Order Flow Denominator}} \times 100$$

#### Instamart Q2 FY27 Reconciliation:
$$\text{Instamart GOV} = ₹9,230\text{ Cr}$$
$$\text{Contribution Profit} = -1.0\% \times ₹9,230\text{ Cr} = \mathbf{-₹92.3\text{ Cr}}$$
$$\text{Segment Adjusted EBITDA} = -9.7\% \times ₹9,230\text{ Cr} = \mathbf{-₹895.0\text{ Cr}}$$

---

## 2. The Four-Tier Comparability Framework

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FOODIQ FOUR-TIER COMPARABILITY MATRIX                           │
├─────────┬──────────────────────────────┬───────────────────────────────────────────────┤
│ Tier    │ Classification               │ Permitted Mathematical Operations             │
├─────────┼──────────────────────────────┼───────────────────────────────────────────────┤
│ LEVEL 1 │ Directly Comparable          │ Subtraction, Spreads, Direct Ranking,         │
│         │ (Identical definitions)      │ Market Share Computations.                    │
│         │ e.g. Food Delivery GOV       │                                               │
├─────────┼──────────────────────────────┼───────────────────────────────────────────────┤
│ LEVEL 2 │ Comparable with Adjustment   │ Normalization required before math.           │
│         │ (Scope or Perimeter shifts)  │ e.g. District LFL organic vs. Paytm inorganic │
├─────────┼──────────────────────────────┼───────────────────────────────────────────────┤
│ LEVEL 3 │ Directionally Comparable     │ Trajectory / growth rate comparison only;     │
│         │ (Differing cost allocation)  │ Absolute spreads blocked.                     │
│         │ e.g. Segment EBITDA margins  │ (Subject to differing corporate overhead).    │
├─────────┼──────────────────────────────┼───────────────────────────────────────────────┤
│ LEVEL 4 │ Incomparable                 │ Direct mathematical comparison strictly       │
│         │ (Incompatible treatments)    │ BLOCKED by the engine.                        │
│         │ e.g. Blinkit 1P vs Swiggy 3P │                                               │
└─────────┴──────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 3. Structural Break Handling

### 3.1 Blinkit 1P Inventory Transition (Q2 FY26)
- **Accounting Shift:** Transition from third-party marketplace agent (recognizing net commission revenue) to first-party owned inventory principal under **Ind AS 115**.
- **Financial Consequence:** Headline reported revenue jumped $+128\%$ quarter-on-quarter while physical order flow expanded normally.
- **System Guard:** FoodIQ tags this event in `corporate_events` and flags Q2 FY26 as a structural break. The platform prohibits revenue-based take rate comparisons across this boundary.

### 3.2 District / Paytm Insider Acquisition (Q2 FY25)
- **Transaction:** Eternal acquired Paytm's entertainment and ticketing business for $₹2,048\text{ Cr}$.
- **Consequence:** Added $118$ percentage points of inorganic GOV growth to the Going-Out segment.
- **System Guard:** Evaluated under Level 2 Comparability, isolating organic like-for-like (LFL) trends.

---

## 4. Econometric Methodology & FDR Control

### 4.1 First-Difference Detrending
When analyzing time series in platform internet companies, common upward trends often cause high spurious correlations in levels ($R^2 > 0.80$). FoodIQ enforces differencing:
$$\Delta Y_t = Y_t - Y_{t-1}, \quad \Delta X_t = X_t - X_{t-1}$$
$$\Delta Y_t = \alpha + \beta \Delta X_t + \epsilon_t$$

### 4.2 Benjamini-Hochberg (FDR) Procedure
To test $m=10$ empirical studies without inflating Type I false discoveries:
1. Sort raw $p$-values: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
2. Find the largest $k$ such that:
   $$p_{(k)} \le \frac{k}{m} \cdot Q, \quad (Q = 0.05)$$
3. Reject all hypotheses $H_{(i)}$ for $i = 1, \dots, k$.
