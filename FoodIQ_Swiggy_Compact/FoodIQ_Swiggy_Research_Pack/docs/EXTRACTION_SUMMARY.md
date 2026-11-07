# FoodIQ — Swiggy source extraction summary

**Package status:** Swiggy-only source pack, covering six quarterly shareholder letters from Q1 FY26 through Q2 FY27 and historical KPI series generally spanning Q1 FY25–Q2 FY27. This is not yet the cross-company FoodIQ dataset because no Eternal letters were uploaded in this batch.

## Source inventory

The source register and original PDFs are in `sources/`. Six letters were uploaded: Q1 FY26, Q2 FY26, Q3 FY26, Q4 FY26, Q1 FY27 and Q2 FY27. PDFs have been preserved unchanged; extracted text is available as full-document `.txt` and page-indexed `all_pages.jsonl`. The latter is the durable machine-readable page archive. Original PDFs remain authoritative when charts, tables, footnotes or layout are not faithfully represented in text extraction.

## What has been structured

- `data/raw/swiggy_metrics_long.csv`: long-form observations keyed by company, quarter, segment and metric.
- `data/curated/swiggy_segment_quarterly_wide.csv`: quarterly, segment-oriented panel for convenient analysis.
- `data/curated/consolidated_reconciliations_long.csv`: 10-quarter page-16 revenue, EBITDA, cash burn, capex, cash-flow movements and cash balance series.
- `data/curated/metric_definitions.csv`: metric definition notes, scopes and margin denominators from the letters.
- `data/curated/management_evidence.csv`: structured management commentary, Q&A evidence, strategy explanations and source references. Text is explicitly tagged as verbatim excerpt or source-faithful paraphrase.
- `data/curated/management_guidance.csv`: forward targets and statements, assessment categories and as-of-Q2FY27 status.
- `data/curated/strategic_initiatives.csv`: product, operating-model, monetisation, ESG and corporate initiatives.
- `data/curated/operational_claims.csv`: store network, density, user, order, partner, reach and programme metrics.
- `data/quality/`: source discrepancies, data-quality issues and recommended handling.

## Main source-derived analytical themes

1. Food Delivery has grown GOV from ₹8,086cr in Q1FY26 to ₹10,054cr in Q2FY27. Reported adjusted EBITDA rose from ₹192cr (2.4% of GOV) to ₹341cr (3.4% of GOV). Management attributes economics to advertising, order density, shorter delivery distances and operating leverage, while also highlighting affordability and speed/selection propositions.
2. Quick commerce scaled to ₹9,230cr GOV and ₹6,594cr NOV in Q2FY27, with 130.3m orders, 14.8m MTUs, 1,240 stores and 5.21m sq ft. Quarterly contribution margin was -1.0% of GOV, despite the May 2026 monthly CM break-even milestone in Q1FY27. The Q2 decline from -0.2% to -1.0% was attributed by management to targeted user habit investments and mix, partly offset by operating leverage.
3. Out-of-Home GOV reached ₹1,508cr in Q2FY27, with 66k active restaurants and 0.5% adjusted EBITDA margin. The business was positive for seven consecutive quarters, although margin moderated from 0.9% in Q1FY27.
4. Platform scale is growing while consolidated adjusted EBITDA remains negative: Q2FY27 B2C GOV was ₹20,793cr, platform MTU 27.8m, and consolidated adjusted EBITDA loss ₹760cr. Segment profit must be distinguished from group loss.
5. Management disclosed unusually useful unit-economics details: RPO, orders per store per day, darkstore capacity/utilisation, retention, store cohorts, non-grocery mix, margin driver attribution, and scale thresholds for quick-commerce break-even.
6. Differentiation appears increasingly assortment- and retention-led: Switch, No!ce, Nectr, partner brands, Toing, Dineout experiences, and food delivery propositions.
7. Several corporate/structural items can affect comparability: QIP, Rapido stake monetisation, Indian Owned and Controlled transition, and Lynks divestment.

## Pages requiring special care

- Printed pages 5–9: historical KPI charts/tables; chart labels and footnotes may be visually encoded.
- Printed pages 10–15: management Q&A; many of the most differentiated disclosures are here.
- Printed page 16: reconciliation of adjusted revenue, adjusted EBITDA and cash movement.
- Printed pages 17–21: metric definitions.
- Printed pages 22–24 and later: financial statements, audit/limited review reports and notes. The raw page archive preserves these for further extraction.

## Coverage boundaries

This package is a structured first-pass research extraction, not a claim that every footnote from every statutory appendix has been normalised into an individual database row. All source pages are preserved so Antigravity and a human reviewer can perform deeper page-level extraction without returning to unstructured attachments. Before public release, spot-check every manually transcribed observation against the PDF page image and record the reviewer/date.
