# FoodIQ Phase 8 — Data Quality & Anomaly Detection Framework

## 1. Automated Anomaly Detection Taxonomy

FoodIQ's automated scanner evaluates all observations in `foodiq.db` across four algorithmic rules:

| Anomaly Type | Severity | Detection Rule | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Broken Financial Identity** | `LOW` to `MEDIUM` | $\|(\text{Orders} \times \text{AOV}) - \text{GOV}\| / \text{GOV} > 6.0\%$ | Flag for review; evaluate tax/packaging inclusions. |
| **Extreme QoQ Movement** | `HIGH` | $\Delta \text{Metric} > +100\%$ or $< -50\%$ QoQ | Flag for structural break (e.g. 1P shift or M&A). |
| **Sign Inversion** | `HIGH` | Operating metric changes sign (e.g. CM positive to negative) | Verify disclosure footnotes for non-recurring charges. |
| **Duplicate Observation** | `CRITICAL` | More than 1 observation for same (company, segment, metric, quarter) | Enforce unique database constraint; trigger rollback. |

---

## 2. Research Impact Attribution

When a new disclosure is registered, the Research Update Engine automatically classifies existing downstream research objects:

| Status Code | Meaning | Downstream Action |
| :--- | :--- | :--- |
| `UNCHANGED` | Historical facts unaffected | No recalculation required. |
| `NEW_EVIDENCE_AVAILABLE` | New quarter available | Historical report preserved; new draft created. |
| `REQUIRES_RECALCULATION`| Statistical or ratio metric affected | Recompute regression slope, $r$, and FDR $p$-values. |
| `REQUIRES_ANALYST_REVIEW`| Milestone maturity date reached | Analyst inspects commitment outcome in credibility engine. |
| `POTENTIALLY_SUPERSEDED` | Baseline parameters updated | Scenario models notify user of rolled-forward base quarter. |
