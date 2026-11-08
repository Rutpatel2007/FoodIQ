# FoodIQ Phase 3.1: Research Integrity & Epistemic Standards

## 1. Principles of Institutional Research Integrity

The **FoodIQ Platform** was designed to reject superficial vanity metrics and enforce the rigorous evidentiary standards demanded by institutional equity research analysts. 

Research integrity in FoodIQ rests on three pillars:
1. **Verifiable Primary Traceability:** Every factual observation must trace directly to a verified corporate disclosure with a PDF document identifier and page number.
2. **Epistemic Classification:** Analytical statements must never masquerade as reported corporate disclosures. Every finding must state its exact evidentiary pedigree.
3. **Refusal of Fabrication:** Missing disclosures must remain `NULL`. The platform strictly prohibits zero-filling, forward-filling, or unverified statistical interpolation to manufacture artificial peer comparisons.

---

## 2. The 6-Tier Epistemic Evidence Framework

FoodIQ classifies every finding, table, and narrative claim into one of six mutually exclusive evidentiary tiers:

```
[TIER 1: REPORTED FACT]
  └── Audited financial figures directly reported in official company filings.
      Example: Swiggy Q2 FY27 Food GOV = ₹10,054 Cr.

[TIER 2: DERIVED FACT]
  └── Exact mathematical computations derived from Reported Facts via public accounting identities.
      Example: Blinkit Q2 FY27 Throughput = NOV * 10^7 / (Stores * 91.25) = ₹849,924 / store-day.

[TIER 3: MANAGEMENT EXPLANATION]
  └── Qualitative justifications or causal explanations provided by executive management in letters/calls.
      Example: "New dark stores in emerging clusters require 6-9 months of cohort maturation."

[TIER 4: ANALYST INTERPRETATION]
  └── Professional deductions, synthesis, and industry benchmarking produced by financial analysts.
      Example: "Over 80% of Blinkit's sequential revenue surge was an Ind AS 115 gross billing artifact."

[TIER 5: HYPOTHESIS]
  └── Plausible analytical conjectures requiring data not currently disclosed in public filings.
      Example: "When customer delivery subsidies are normalized, net merchant commission spreads are within 100 bps."

[TIER 6: UNVERIFIED / INSUFFICIENT EVIDENCE]
  └── Questions where disclosures are incomplete or asymmetric, rendering definitive ranking impossible.
      Example: "Blinkit daily order count per store-day cannot be verified without audited order disclosures."
```

---

## 3. Dissecting Optical Illusions & Analytical Bias

### Optical Illusion 1: Blinkit's "6x Revenue Dominance"
- **The Optical Trap:** In Q2 FY26, Blinkit reported Adjusted Revenue of ₹2,423 Cr vs. Swiggy Instamart's ₹398 Cr (a 6.08x multiple). Naive observers hailed this as 6x commercial dominance.
- **The Reality:** Blinkit recognized 100% of product retail price as revenue under 1P inventory principal accounting (Ind AS 115). Swiggy recognized only net marketplace commissions (~12–15% of cart value).
- **The Integrity Correction:** When evaluated on customer transacted Net Order Value ($NOV$), Blinkit transacted ₹11,679 Cr vs. Swiggy's ₹4,915 Cr (a 2.37x commercial lead, not 6.08x). FoodIQ strictly blocks direct peer revenue subtraction for post-Q1FY26 periods.

### Optical Illusion 2: Swiggy's "380 bps Monetization Premium"
- **The Optical Trap:** Swiggy reported a total Food Delivery Take Rate of ~24.0% of GOV vs. Eternal's ~20.2% Adjusted Revenue Take Rate, suggesting Swiggy extracts 380 bps higher fees from restaurant merchants.
- **The Reality:** Swiggy's take rate is presented gross of customer delivery fees and platform fees. Eternal's Adjusted Revenue nets out certain customer delivery fee discounts and customer loyalty subsidies.
- **The Integrity Correction:** Direct peer ranking on take rates is classified as **LEVEL 3 DIRECTIONALLY COMPARABLE**. FoodIQ explicitly labels claims of exact 100 bps parity as an **ANALYST HYPOTHESIS**, preserving research transparency until companies publish unbundled voucher tables.

---

## 4. Null Preservation & Anti-Smoothing Guarantee

In conventional corporate dashboards, missing metrics are routinely filled with `0` or interpolated using rolling averages. FoodIQ strictly prohibits this practice:
- If Swiggy does not disclose Food AOV in quarterly letters, the metric is stored as `NULL`.
- If Blinkit does not disclose quarterly order volume, the metric is stored as `NULL`.
- Calculations consuming a `NULL` metric evaluate to `None` and are labeled `ASYMMETRIC_SINGLE_DISCLOSURE` or `UNAVAILABLE_BOTH`.
- Under no circumstances does the platform invent data points to satisfy visual symmetry.
