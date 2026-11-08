# FoodIQ Financial Integrity Findings (Phase 2.1 Audit)

This document provides detailed evidence, financial reasoning, and reconciliation proofs regarding corporate disclosures from Eternal Limited and Swiggy Limited.

---

## 1. Gross Order Value (GOV) vs. Net Order Value (NOV) Integrity

### 1.1 The Fundamental Distinction
- **Eternal (Zomato/Blinkit):** Discloses $GOV$ as headline order value including taxes, customer delivery fees, and platform fees, but reports segment profitability and margins primarily on **Net Order Value (NOV)**. For Blinkit, $NOV$ is defined as gross merchandise value after customer discounts and merchant promotions.
- **Swiggy:** Discloses $GOV$ across both Food Delivery and Quick Commerce (Instamart). Swiggy's stated take rates and contribution margins in shareholder disclosures are defined as a percentage of **GOV**, not NOV.
- **Voucher / Subsidy Spread:** The difference $GOV - NOV$ represents customer discounts funded by the platform, promotional vouchers, and statutory tax exclusions.
  - Across Swiggy Instamart, $(GOV - NOV)$ ranged from ₹420 Cr in FY25 Q1 to ₹1,438 Cr in FY27 Q2.
  - On a per-order basis, this implies platform vouchers and subsidies of ₹47.0 to ₹110.3 per order.

### 1.2 Mathematical Coherence of AOV
- In Swiggy's disclosures, Average Order Value is explicitly defined as:
  $$AOV \equiv \frac{GOV}{\text{Total Orders}}$$
- For example, in FY27 Q2 Instamart:
  $$\frac{GOV \text{ (₹9,225 Cr)} \times 10}{\text{Orders (130.3 mn)}} = \frac{92250}{130.3} \approx ₹707.98 \to ₹708 \text{ disclosed}$$
- Because $AOV$ is derived from $GOV$, it is mathematically impossible to decompose $NOV$ using this $AOV$. Attempting to compute $(O \times AOV)$ yields $GOV$, not $NOV$.
- **Audit Decision:** FoodIQ strictly restricts $P \times Q$ waterfall decompositions to $GOV$. Any query requesting $NOV$ decomposition using $GOV$-based $AOV$ is rejected with status code `INELIGIBLE_INVALID_METRIC_BASIS`.

---

## 2. Decomposition Additivity and Disclosure Rounding Residuals

### 2.1 The 4-Term Additivity Proof
Between FY25 Q1 and FY27 Q2, Swiggy Instamart discloses 10 quarters of paired $GOV$, $Orders$, and $AOV$. The 4 terms sum identically to $\Delta GOV$:

| Transition | $\Delta GOV$ (₹ Cr) | Volume Effect | Basket Effect | Interaction Effect | Rounding Residual | Sum of 4 Terms | Additivity Check |
|---|---|---|---|---|---|---|---|
| Q1FY25 $\to$ Q2FY25 | +658.0 | +574.66 | +81.36 | +0.00 | +1.98 | +658.00 | **EXACT** |
| Q2FY25 $\to$ Q3FY25 | +525.0 | +269.46 | +256.20 | +0.00 | -0.66 | +525.00 | **EXACT** |
| Q3FY25 $\to$ Q4FY25 | +763.0 | +822.36 | -62.02 | +0.00 | +2.66 | +763.00 | **EXACT** |
| Q4FY25 $\to$ Q1FY26 | +985.0 | +200.26 | +785.40 | +0.00 | -0.66 | +985.00 | **EXACT** |
| Q1FY26 $\to$ Q2FY26 | +1367.0 | +514.08 | +856.80 | +0.00 | -3.88 | +1367.00 | **EXACT** |
| Q2FY26 $\to$ Q3FY26 | +916.0 | +390.32 | +521.36 | +0.00 | +4.32 | +916.00 | **EXACT** |
| Q3FY26 $\to$ Q4FY26 | -57.0 | +462.52 | -517.96 | +0.00 | -1.56 | -57.00 | **EXACT** |
| Q4FY26 $\to$ Q1FY27 | +26.0 | +133.00 | -103.05 | +0.00 | -3.95 | +26.00 | **EXACT** |
| Q1FY27 $\to$ Q2FY27 | +1323.0 | +1091.78 | +221.51 | +0.00 | +9.71 | +1323.00 | **EXACT** |

### 2.2 Forensic Attribution of the Residual
The residual term $\epsilon_t \in [-3.95, +9.71]\text{ ₹ Cr}$ is not an unmodeled economic phenomenon. It arises entirely because corporate disclosures publish:
1. Orders rounded to 1 decimal place ($130.3\text{ mn}$ vs true continuous order count).
2. AOV rounded to integer rupees ($₹708$ vs $₹707.98$).
3. GOV rounded to integer Crores ($₹9,225\text{ Cr}$).
- Recomputing $(130.3 \times 708) / 10 = 9225.24\text{ Cr}$, introducing an inherent $0.24\text{ Cr}$ discrepancy with published $9,225\text{ Cr}$.
- Over quarter-on-quarter differences, these independent rounding truncations compound to between ₹0.66 Cr and ₹9.71 Cr.
- **Audit Decision:** The residual is explicitly presented in the waterfall and tagged as `DISCLOSURE_ROUNDING_ARTIFACT`. It is never obscured or merged into Volume or Price terms.

---

## 3. Revenue Recognition Accounting Shift (1P vs. 3P Model)

### 3.1 Blinkit Q2 FY26 Inventory Model Shift
In Q2 FY26, Eternal Limited restructured Blinkit's legal and operating supply chain:
- **Prior Model (3P Marketplace / Agency):** Blinkit operated as an intermediary connecting third-party sellers with consumers. Revenue comprised commissions, handling fees, and advertising.
- **New Model (1P Inventory / Principal):** Blinkit transitioned to purchasing and holding inventory directly for significant product lines, recognizing the full gross merchandise value of goods as revenue under Ind AS 115 / IFRS 15.
- **Financial Consequence:**
  - Blinkit Adjusted Revenue surged from ₹1,061 Cr in Q1 FY26 to ₹2,423 Cr in Q2 FY26 (+128% QoQ).
  - Meanwhile, Swiggy Instamart continued operating on a 3P agency commission model, reporting revenue of ₹398 Cr in Q2 FY26.
  - Direct subtraction of Blinkit revenue from Swiggy revenue ($2,423 - 398 = +2,025\text{ Cr}$) creates a false impression of a $6\times$ revenue scale advantage, when in reality it reflects gross merchandise value vs. net commission accounting.
- **Audit Decision:** All Blinkit vs. Swiggy quick commerce revenue comparisons from Q2 FY26 onwards are classified as `LEVEL_4_INCOMPARABLE_BLOCKED`. The platform blocks raw subtraction in competitive gap endpoints and surfaces prominent accounting warnings.

---

## 4. Denominator Integrity & Undisclosed Blinkit Orders

### 4.1 Missing Observations vs. Coercion
Eternal does not disclose quarterly order volume or average order value for Blinkit in its shareholder letters, disclosing only GOV, dark store count, average store size, and contribution margin percentage.
- Prior implementations in unsophisticated dashboards frequently attempted to estimate Blinkit orders by dividing Blinkit GOV by Swiggy's AOV, or substituted Zomato Food Delivery orders as a proxy.
- **Audit Rule Enforced:** Cross-company proxy substitution is strictly prohibited. Blinkit order counts, revenue per order, contribution per order, and discount per order are maintained as `NULL` (`None`).
- FoodIQ instead evaluates dark store productivity metrics (throughput per operating store-day, revenue per square foot) where empirical disclosures exist.
