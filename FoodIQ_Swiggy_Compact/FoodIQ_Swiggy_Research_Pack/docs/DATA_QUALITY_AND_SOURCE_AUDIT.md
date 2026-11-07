# FoodIQ — Data quality and source audit

## Stop-the-line issues

1. **No Eternal letters in this upload batch.** This package is Swiggy-only. Do not compute competitive gaps, peer-relative claims or Eternal-leading indicators until comparable Eternal disclosures are loaded.
2. **Food NOV and Out-of-Home NOV are not published by Swiggy.** Management explicitly says it does not publish these values because discount/subsidy patterns are not structurally comparable. Food and Out-of-Home analysis must use GOV unless a future source explicitly reports another basis.
3. **Scope mixing in the seed CSV.** B2C GOV excludes Platform Innovations, while consolidated Adjusted Revenue and Adjusted EBITDA are consolidated numbers. Store them as separate scope-specific metrics; do not place in one implied segment denominator.
4. **Platform MTU / frequency history conflicts.** See `source_conflicts.csv`. Preserve report-specific values; do not overwrite silently.
5. **Quick-commerce NOV absolute values.** Some values in the seed CSV may be derived from rounded NOV/GOV ratios; later values are explicitly stated in narratives, but earlier values require page-level validation. The dataset retains provenance/status tags.
6. **AOV and nAOV are not interchangeable.** The letters show AOV and nAOV as distinct values (e.g. Q2FY27 chart AOV ₹708 versus CEO/Q&A nAOV ₹506). Retain separate fields and seek the full definition before use.
7. **Take rate must not be guessed.** Management-reported values such as Food 25.8% / 26.1% and Quick Commerce 14.8% must be retained with source references. Do not calculate take rate as adjusted revenue divided by NOV unless a source definition confirms that formula and matching scope.
8. **Quick-commerce break-even requires three fields:** monthly milestone and date, quarter-average CM, and subsequent reinvestment explanation. Q1FY27 monthly break-even (May 2026) coexists with quarter average -0.2%; Q2FY27 average was -1.0%.
9. **Lynks disposal creates a Supply Chain structural break from Q3FY27.** Q2FY27 disclosed the sale; reported segment composition changes subsequently.
10. **Margin denominators differ.** Record numerator, denominator, segment and scope for every margin. Never compare percentages with different denominators as if equivalent.

## User-provided seed data audit

The seed table is useful as a starter, but the fields need to be mapped into a richer observation model:

- Rename `Consolidated.gov_cr` to `b2c_gov_cr` where it refers to consumer-facing GOV.
- Separate consolidated adjusted revenue and consolidated adjusted EBITDA from B2C GOV.
- Keep `adj_ebitda_margin_pct` with a required `margin_denominator` field.
- Add Q2FY27 observations now available in the most recent uploaded letter.
- Preserve the user-supplied QuickCommerce NOV series with a validation status; do not present it as fully source-verified until each quarter has a direct source reference.
- Add `nAOV` as a distinct metric where management discloses it; do not substitute for KPI chart AOV.
- Use the source's page number (PDF physical page plus printed-page label where helpful), not a copied filename alone.
- Keep original report-version values when later letters revise or re-display historical values.

## Statistical integrity rules

- Roughly ten quarterly points do not support robust causal inference. Describe lead/lag correlation as exploratory.
- Report sample size, Pearson/Spearman coefficient as appropriate, p-value, confidence interval and caveats; examine first differences and common trends.
- A non-significant result is an acceptable finding.
- Do not hard-code an AOV-to-margin elasticity before estimating it and validating stability. Sensitivity scenarios may use explicit assumptions, but label them as assumptions.
- A margin bridge must reconcile in currency or basis points using disclosed component data. If line items are missing, report the residual and avoid fabricated allocation.
- Seasonality matters: Q1 has monsoon, reverse migration and salary-cycle impacts; Q3/Q4 have festive/seasonal patterns. Prefer YoY alongside QoQ.

A machine-readable list is in `data/quality/data_quality_issues.csv`.
