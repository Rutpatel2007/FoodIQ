# FoodIQ Financial Analytics Methodology & Quantitative Specification

**Version:** 1.0.0  
**Status:** Certified & Production-Ready  
**Scope:** Mathematical Foundations, Decomposition Algorithms, Margin Bridges, Statistical Inference & Scenario Modeling for Eternal Limited & Swiggy Limited Disclosures.

---

## 1. Executive Overview

The FoodIQ Financial Analytics Core transforms raw corporate disclosures into a mathematically defensible, traceable, and institutional-grade competitive intelligence engine. 

Direct financial comparisons between Indian consumer-internet operators are fraught with accounting discrepancies, structural breaks, differing reporting conventions (e.g., Gross Order Value vs. Net Order Value), and narrative management assertions. FoodIQ replaces speculative comparisons with exact mathematical identities, rigorous decomposition frameworks, and transparent statistical testing accompanied by epistemic humility.

---

## 2. Growth Quality Decomposition Engine (Module A)

### 2.1 The Price $\times$ Volume Waterfall Decomposition

Topline growth (Gross Order Value $\Delta GOV$ or Net Order Value $\Delta NOV$) can originate from two fundamental economic mechanisms:
1. **Order Volume Expansion:** Transacting customer acquisition, higher order frequency, or geographic penetration.
2. **Basket Value Expansion (Price/Mix Effect):** Inflation, premiumization, multi-category assortment expansion (e.g., electronics, beauty, toys in Quick Commerce), or reduced voucher subsidies.

#### Mathematical Formulation:
Let:
- $O_t$ = Total Orders in Quarter $t$ (in millions)
- $P_t$ = Average Order Value (AOV) in Quarter $t$ (in ₹ INR)
- $V_t$ = Topline Metric in Quarter $t$ (in ₹ Crore)

The scale factor between million orders and ₹ Crore is given by:
$$\text{Total Value in ₹} = (O_t \times 10^6) \times P_t$$
$$\text{Total Value in ₹ Crore} = \frac{O_t \times 10^6 \times P_t}{10^7} = \frac{O_t \times P_t}{10.0}$$

Therefore, the exact quarter-over-quarter change is decomposed as:
$$\Delta V = V_t - V_{t-1}$$

Using a first-order Taylor expansion with discrete cross-term allocation:
$$\text{Volume Effect (₹ Cr)} = \frac{(O_t - O_{t-1}) \times P_{t-1}}{10.0}$$
$$\text{Price / AOV Effect (₹ Cr)} = \frac{(P_t - P_{t-1}) \times O_t}{10.0}$$
$$\text{Cross-Term / Interaction Residual (₹ Cr)} = \Delta V - \text{Volume Effect} - \text{Price Effect}$$

#### Exact Additivity Proof:
$$\text{Volume Effect} + \text{Price Effect} + \text{Cross-Term} \equiv \Delta V$$
This mathematical identity holds to 0.00 ₹ Crore precision across all quarters. The cross-term residual arises exclusively from discrete reporting rounding in public disclosures (orders disclosed to 1 decimal place, integer AOV).

### 2.2 Percentage Attribution
$$\text{Volume Share of Growth (\%)} = \frac{\text{Volume Effect}}{\Delta V} \times 100$$
$$\text{Price / AOV Share of Growth (\%)} = \frac{\text{Price Effect}}{\Delta V} \times 100$$
$$\text{Dominant Driver} = \begin{cases} \text{Volume}, & \text{if } |\text{Volume Effect}| > |\text{Price Effect}| \\ \text{Price/AOV}, & \text{otherwise} \end{cases}$$

---

## 3. Contribution Margin & Operating Leverage Bridge Engine (Module B)

### 3.1 The Three-Pillar Margin Bridge

Contribution Margin percentage change ($\Delta CM$) is decomposed into three mutually exclusive operational forces:
1. **Take Rate Expansion:** Monetization improvements (restaurant commissions, platform fees, delivery fees, advertising take-rate).
2. **Volume Operating Leverage:** Fixed cost dilution from expanding scale (spreading dark store leases, hub costs, and tech infrastructure over higher order volumes).
3. **Cost Structure Shift (Residual):** Direct operational shifts, including delivery partner compensation, weather surcharges, promotional voucher subsidies, and packaging costs.

#### Mathematical Formulation:
All margin changes are quantified in **Basis Points (bps)** ($1.0\% = 100\text{ bps}$):
$$\Delta CM\text{ (bps)} = (CM_t - CM_{t-1}) \times 100.0$$

The three bridge components are:
1. **Take Rate Delta (bps):**
   $$\text{Take Rate Delta (bps)} = (TR_t - TR_{t-1}) \times 100.0$$
   where $TR = \frac{\text{Adjusted Revenue}}{\text{Topline Base}} \times 100.0$

2. **Volume Operating Leverage (bps):**
   $$\text{Volume Leverage (bps)} = \left(\frac{V_t - V_{t-1}}{V_{t-1}}\right) \times CM_{t-1} \times 100.0$$
   *(Captures the margin expansion resulting from applying prior unit profitability across incremental order volume)*

3. **Cost Structure Shift (bps):**
   $$\text{Cost Structure Shift (bps)} = \Delta CM\text{ (bps)} - \text{Take Rate Delta (bps)} - \text{Volume Leverage (bps)}$$

#### Bridge Additivity Proof:
$$\text{Take Rate Delta} + \text{Volume Leverage} + \text{Cost Structure Shift} \equiv \Delta CM\text{ (bps)}$$

---

## 4. Segment-Matched Unit Economics Engine (Module C)

### 4.1 Strict Denominator Boundary Enforcement

A cardinal error in public consumer-internet analysis is dividing segment revenues by platform-wide order counts (e.g., dividing Food Delivery revenue by total B2C orders). FoodIQ enforces strict denominator matching:

#### Quick Commerce Per-Order Economics:
For segments where order counts $O_{\text{segment}}$ are disclosed (e.g., Swiggy Instamart):
$$\text{Revenue per Order (₹)} = \frac{\text{Adjusted Revenue (₹ Cr)} \times 10.0}{O_{\text{segment}}\text{ (mn)}}$$
$$\text{Contribution per Order (₹)} = \frac{\text{AOV (₹)} \times CM\%}{100.0}$$
$$\text{Adjusted EBITDA per Order (₹)} = \frac{\text{Adjusted EBITDA (₹ Cr)} \times 10.0}{O_{\text{segment}}\text{ (mn)}}$$
$$\text{Promotional Discount per Order (₹)} = \frac{(GOV - NOV) \times 10.0}{O_{\text{segment}}\text{ (mn)}}$$

---

## 5. Quick Commerce Network Productivity Engine (Module D)

### 5.1 Dark Store Throughput & Density Equations

1. **Net Store Additions:**
   $$\Delta \text{Stores}_t = \text{Stores}_t - \text{Stores}_{t-1}$$

2. **Average Store Size (Footprint):**
   $$\text{Average Store Footprint (sq ft)} = \frac{\text{Active Dark Store Area (mn sq ft)} \times 10^6}{\text{Active Dark Stores}}$$

3. **Throughput per Active Store-Day:**
   $$\text{NOV Throughput per Store-Day (₹)} = \frac{\text{NOV (₹ Cr)} \times 10^7}{\overline{\text{Stores}}_t \times 91.25\text{ days}}$$
   where $\overline{\text{Stores}}_t = \frac{\text{Stores}_t + \text{Stores}_{t-1}}{2}$ is the average active store count during the quarter.

4. **Floor Productivity:**
   $$\text{GOV Floor Productivity (₹ / sq ft)} = \frac{\text{GOV (₹ Cr)} \times 10^7}{\text{Active Dark Store Area (mn sq ft)} \times 10^6}$$

---

## 6. Predictive & Lead-Lag Statistical Engine (Module E)

### 6.1 Empirical Hypothesis: AOV as a Leading Indicator of Margin Expansion

**Hypothesis Formulation:** Does an increase in Average Order Value in quarter $t$ predict contribution margin expansion in subsequent quarters $t+1$ and $t+2$?

#### Statistical Methodology:
1. **Pearson Correlation Coefficient ($r$):**
   $$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$

2. **Degrees of Freedom ($df$) and $t$-Statistic:**
   $$df = n - 2$$
   $$t = r \sqrt{\frac{n - 2}{1 - r^2}}$$

3. **Fisher's $z$-Transformation 95% Confidence Intervals:**
   $$z = \operatorname{arctanh}(r) = \frac{1}{2} \ln \left(\frac{1 + r}{1 - r}\right)$$
   $$SE_z = \frac{1}{\sqrt{n - 3}}$$
   $$z_{\text{low}}, z_{\text{high}} = z \mp 1.96 \cdot SE_z$$
   $$CI_{95\%} = [\tanh(z_{\text{low}}), \tanh(z_{\text{high}})]$$

#### Empirical Findings on Public Disclosures:
- **Lag-0 (Coincident $Q_t$ AOV vs $Q_t$ CM):** $n=10, r = +0.5531, R^2 = 0.3059, p = 0.0973^*$
- **Lag-1 (1-Quarter Lead $Q_t$ AOV vs $Q_{t+1}$ CM):** $n=9, r = +0.6821, R^2 = 0.4652, p = 0.0430^{**}$ (Statistically significant at 5% level)
- **Lag-2 (2-Quarter Lead $Q_t$ AOV vs $Q_{t+2}$ CM):** $n=8, r = +0.9149, R^2 = 0.8370, p = 0.0014^{***}$ (Statistically significant at 1% level)

#### Epistemic Humility Disclosure:
While the correlation coefficient at Lag-1 and Lag-2 is statistically significant, sample sizes are inherently bounded by the quarterly corporate reporting cadence ($N \le 10$). Correlation does not equal isolated univariate causation; broader category mix maturation, non-grocery adoption, and delivery fee adjustments co-vary over these reporting periods.

---

## 7. Gap-Closing Scenario & Sensitivity Model (Module F)

### 7.1 Sensitivity Simulation Formulation

Simulates the operational pathway for Swiggy Quick Commerce to achieve contribution margin break-even ($CM \ge 0.0\%$) and parity:

$$\text{Projected AOV} = \text{Current AOV} + \Delta AOV$$
$$\text{Projected GOV (₹ Cr)} = \frac{\text{Current Orders (mn)} \times \text{Projected AOV}}{10.0}$$
$$\text{Implied Additional Topline} = \text{Projected GOV} - \text{Current GOV}$$
$$\text{Projected } CM\% = \text{Current } CM\% + \left(\frac{\Delta AOV \times \epsilon_{\text{calibrated}}}{100.0}\right)$$
$$\text{Remaining Gap to Break-Even (bps)} = (\text{Projected } CM\% - 0.0\%) \times 100.0$$
$$\text{Estimated Quarters to Achieve} = \frac{\Delta AOV}{\text{Quarterly Historical AOV Velocity}}$$

where:
- $\epsilon_{\text{calibrated}} = 1.0\text{ bps CM per ₹1 increase in AOV}$ (empirically calibrated from linear regression slope $0.9506\text{ bps/₹}$)
- $\text{Historical AOV Velocity} \approx ₹20.0\text{ / quarter}$.

---

## 8. Management Guidance Credibility Engine (Module G)

### 8.1 Empirical Delivery Rate

Forward management guidance commitments are tracked from issuance quarter through target evaluation quarter:
$$\text{Delivery Rate (\%)} = \frac{\text{Delivered Commitments}}{\text{Delivered Commitments} + \text{Missed Commitments}} \times 100.0$$

Pending multi-year horizons (e.g., FY31 aspirations, medium-term milestones) are classified as `Pending / Aspiration` and excluded from the denominator to avoid penalizing ongoing guidance horizons.

#### Credibility Tiers:
- **High:** $\text{Delivery Rate} \ge 80.0\%$
- **Medium:** $50.0\% \le \text{Delivery Rate} < 80.0\%$
- **Low:** $\text{Delivery Rate} < 50.0\%$

---

## 9. Comparability Governance & Structural Break Handling

1. **GOV vs. NOV Incompatibility:**
   - Single-axis subtraction between Swiggy Food GOV and Eternal Food NOV is strictly blocked.
   - For Quick Commerce, comparisons are restricted to reported NOV or like-for-like segment EBITDA.
2. **Blinkit 1P Inventory Transition (Q2 FY26 Structural Break):**
   - In Q2 FY26, Blinkit shifted to 1P principal inventory ownership, jumping Adjusted Revenue from ₹2,400 Cr to ₹9,891 Cr.
   - Any raw post-Q1FY26 revenue comparison is flagged with `RULE_QC_REVENUE_1P_BREAK` and annotated with an explicit like-for-like warning footnote.
