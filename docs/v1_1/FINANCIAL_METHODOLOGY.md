# FoodIQ v1.1 — Financial Methodology & Normalization Guide
**Document Reference:** DOC-V11-03  
**Classification:** Accounting & Valuation Methodology  

---

## 1. The Order Value Waterfall

Corporate disclosures in the on-demand economy utilize diverging top-line metrics. FoodIQ establishes an explicit waterfall separating Gross Merchandise Value (GMV), Net Order Value (NOV), and Gross Order Value (GOV).

```
  Gross Merchandise Value (GMV)
  [-] Restaurant / Merchant Funded Discounts
  ===========================================
  Net Order Value (NOV) [Merchandise Value]
  [+] Consumer Delivery Charges
  [+] Platform & Convenience Surcharges
  [+] Packaging Fees
  [+] Goods and Services Tax (GST)
  ===========================================
  Gross Order Value (GOV) [Total Customer Outlay]
```

### Governing Methodological Principles:
1. **Take Rate Basis:** When comparing Take Rates, the denominator must be standardized. Eternal frequently quotes Take Rate on NOV for Blinkit and GOV for Food Delivery. FoodIQ normalizes and discloses both:
   $$	ext{Take Rate}_{	ext{GOV}} = rac{	ext{Revenue}}{	ext{GOV}}, \quad 	ext{Take Rate}_{	ext{NOV}} = rac{	ext{Revenue}}{	ext{NOV}}$$
2. **Subsidized Delivery Costs:** Customer delivery fees do not reflect full logistics costs. The net delivery cost per order is defined as:
   $$	ext{Net Delivery Burn} = 	ext{Delivery Partner Pay} - 	ext{Consumer Delivery Fee}$$

---

## 2. Margin Bridges: From Take Rate to Adjusted EBITDA

FoodIQ constructs an additive 5-step bridge for each operating segment:

$$egin{aligned}
	ext{Step 1: Gross Take Rate} & = 	ext{Commissions} + 	ext{Delivery Fees} + 	ext{Ad Tech Revenue} \
	ext{Step 2: (-) Variable Fulfilment} & = 	ext{Delivery Rider Payouts} + 	ext{Packing Supplies} \
	ext{Step 3: (-) Payment & Tech Costs} & = 	ext{Payment Gateway (1.2-1.5%)} + 	ext{Customer Support} \
	ext{Step 4: (=) Contribution Margin} & = 	ext{Take Rate} - 	ext{Variable Costs} \
	ext{Step 5: (-) Fixed Overhead} & = 	ext{Store Rent/Leases} + 	ext{Store Utilities} + 	ext{HQ Tech/Salaries} \
	ext{Step 6: (=) Segment Adjusted EBITDA} & = 	ext{Contribution Margin} - 	ext{Fixed Operating Overhead}
\end{aligned}$$

---

## 3. Quick Commerce Unit Economics & Store Cohorts

### 3.1 Network Blended Throughput
Throughput measures the average daily sales processed per dark store:
$$	ext{Throughput} = rac{	ext{Quarterly Order Value}}{	ext{Active Store Count} 	imes 91.25}$$

### 3.2 Mature vs Immature Store Economics
A dark store cohort typically requires 6 to 9 months to achieve contribution break-even:
- **Months 0–3:** Capital expenditure, fit-out, negative throughput (< ₹2.5 lakh/day).
- **Months 4–9:** Utilization ramp, local density capture (₹5.0 – ₹8.0 lakh/day), CM neutral.
- **Months 10+:** Mature steady-state (> ₹10.0 lakh/day), positive EBITDA contribution.
