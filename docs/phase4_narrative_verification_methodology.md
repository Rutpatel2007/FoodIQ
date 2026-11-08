# FoodIQ Phase 4: Narrative Verification & Causal Audit Methodology

## 1. Principles of Narrative Verification

Corporate managements routinely provide qualitative explanations for changes in reported performance. Examples include:
- "Contribution margins improved because of higher average order values."
- "Food delivery margins declined due to seasonal reverse migration of delivery riders."
- "Dark store throughput diluted because newer stores are in early gestation."

The **FoodIQ Narrative Verification Engine** systematically subjects these claims to empirical testing:
1. Identify the verbatim statement, speaker, document, and page citation.
2. Isolate the claimed operational driver and the affected financial metric.
3. Retrieve actual quantitative observations before and after the statement period.
4. Test whether the empirical trend supports, partially supports, or contradicts the narrative.
5. **Separate Statistical Association from Causal Verification**: Explicitly distinguish whether two variables merely moved together versus whether an exclusive causal relationship is proven.

---

## 2. Epistemic Verification Tiers

Claims are evaluated against empirical observations and assigned to one of five tiers:

1. `SUPPORTED_BY_DISCLOSED_EVIDENCE`: Empirical metrics move consistently with management's claim, and corroborating cost breakdowns are disclosed.
2. `PARTIALLY_SUPPORTED`: A general directional correlation exists on level series, but contemporaneous causal timing or first-difference testing rejects naive direct causation.
3. `CONTRADICTED_BY_DISCLOSED_EVIDENCE`: Reported numbers directly contradict management's narrative (e.g. claiming superior core commission extraction when the spread is driven by grossed-up delivery fees).
4. `NOT_TESTABLE`: Disclosures lack the granular data (e.g. store vintage P&Ls) necessary to audit the claim from public filings.
5. `INSUFFICIENT_DISCLOSURE`: Disclosure is completely omitted or asymmetric across peers.

---

## 3. Case Studies in Narrative Verification

### Case 1: Swiggy Instamart AOV vs. Contribution Margin Expansion
- **Management Claim:** Instamart contribution margins expanded from -4.5% to -1.0% because AOV increased from ₹487 to ₹708, diluting fixed delivery costs.
- **Empirical Check:** On quarterly levels, $r = 0.9014 (p < 0.001)$ across 6 quarters.
- **Econometric Detrending:** First-difference testing ($\Delta CM\% \sim \Delta AOV$) yields $r = 0.1399, p = 0.72$.
- **Audit Determination:** `PARTIALLY_SUPPORTED`. While basket size expansion provides mechanical leverage over fixed rider costs, quarter-on-quarter jumps in AOV do not synchronously determine margin jumps in the same quarter. Dark store labor automation and route clustering compound gradually.

### Case 2: Swiggy Food Delivery Take Rate Superiority
- **Management Claim:** Swiggy extracts a superior take rate (~24.0% of GOV) due to advertiser penetration and premium partner curation.
- **Empirical Check:** Swiggy includes gross customer delivery charges and platform fees in its take rate denominator. Eternal reports Adjusted Revenue net of customer delivery subsidies.
- **Audit Determination:** `CONTRADICTED_BY_DISCLOSED_EVIDENCE`. When delivery fee subsidies are normalized, core contractual restaurant commissions on both platforms are virtually identical (~18-20%). The perceived +380 bps lead is primarily an accounting presentation divergence.

### Case 3: Blinkit 1P Inventory Ownership & Sequential Revenue Surge
- **Management Claim:** 1P inventory model was adopted to guarantee availability, resulting in a reported revenue leap.
- **Empirical Check:** Adjusted Revenue surged +128.4% QoQ in Q2 FY26, while underlying consumer merchandise volume ($NOV$) grew +24.2% QoQ.
- **Audit Determination:** `SUPPORTED_BY_DISCLOSED_EVIDENCE`. Over 80% of the sequential revenue surge was an Ind AS 115 principal billing artifact, corroborating management's statement that accounting recognition drove headline revenue growth.
