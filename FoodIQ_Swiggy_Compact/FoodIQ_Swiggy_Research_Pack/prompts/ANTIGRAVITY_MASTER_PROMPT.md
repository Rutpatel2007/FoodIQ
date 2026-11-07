# Antigravity master prompt — FoodIQ

You are implementing **FoodIQ — India Food Delivery Competitive Intelligence Engine**, a source-grounded financial and competitive research system.

Read the entire `FoodIQ_Swiggy_Research_Pack` before coding, especially:
- `docs/ANTIGRAVITY_IMPLEMENTATION_SPEC.md`
- `docs/DATA_DICTIONARY_AND_METHODS.md`
- `docs/DATA_QUALITY_AND_SOURCE_AUDIT.md`
- `docs/FOODIQ_ANALYTICAL_HYPOTHESES.md`
- `docs/EXTRACTION_SUMMARY.md`
- all CSV/JSONL files under `data/` and `sources/`

## Non-negotiable source rules

1. The six uploaded shareholder letters are Swiggy-only. **Do not invent, infer or synthesize Eternal data.** Build support for Eternal in the schema, but disable peer comparison until real Eternal letters and extracted metrics are loaded.
2. Preserve the uploaded PDFs unchanged. Their extracted text and page JSONL are navigational aids; the PDFs are authoritative for visual tables, chart labels and footnotes.
3. Every displayed financial or operational value must have provenance: source PDF, PDF page, reporting quarter, metric definition and value status.
4. Distinguish company-reported, calculated/derived, management estimate, user-supplied-unverified and model assumption.
5. Do not turn null into zero.
6. Swiggy does not publish Food Delivery NOV or Out-of-Home NOV in the supplied letters. Do not fabricate either. Use GOV for those businesses.
7. B2C GOV, consolidated adjusted revenue, consolidated adjusted EBITDA and segment results have different scopes. Keep them separate.
8. Margin denominator varies by segment. Store it and validate it.
9. AOV and nAOV are distinct. Do not overwrite or substitute.
10. Preserve platform MTU/frequency historical discrepancies as separate document-version observations.
11. Preserve the monthly May-2026 QComm CM break-even milestone separately from quarterly averages (-0.2% in Q1FY27; -1.0% in Q2FY27).
12. Mark Lynks disposal as a Supply Chain structural break from Q3FY27.
13. Guidance and long-term aspirations are not the same. Do not mark pending medium-/long-term ambitions missed.
14. Correlation with a small quarterly sample is exploratory, not causal.
15. Never hardcode the spec's original 0.03bps-per-₹1 AOV elasticity. Estimate, validate and sensitivity-test any relationship; if data are insufficient, leave it as an explicit assumption range.

## Build approach

Work in phases, keep each phase runnable, and do not generate a huge monolithic application in one pass.

**Phase 0 — repository and source inventory**
- Create a professional Python project with the structure in the implementation spec.
- Inventory all source files and hash original PDFs.
- Load all supplied curated/raw CSV and JSONL files without deleting source versions.
- Generate a coverage report showing six Swiggy letters and missing Eternal quarter set.

**Phase 1 — database and data contracts**
- Create normalized SQLite tables per the implementation spec.
- Implement staging-to-core loaders with type checks, foreign keys, unique keys that preserve report versions, migrations and idempotent upserts.
- Create tests for all known quality issues and provenance rules.
- Do not start financial modelling until all hard validation failures are resolved or consciously waived with documented reasons.

**Phase 2 — Swiggy-only historical analysis**
- Build segment panels for Platform, Food, QuickCommerce, OutOfHome, SupplyChain and PlatformInnovations.
- Add Q2FY27 observations.
- Produce descriptive trends, YoY / QoQ, growth decomposition where data is valid, monetary contribution margins, adjusted EBITDA margins with correct denominator, quick-commerce store productivity, AOV/nAOV distinction and consolidated reconciliation trends.
- Keep all charts source-linked.

**Phase 3 — guidance and narrative intelligence**
- Implement management guidance ledger, claim-to-outcome tracker and strategic initiative register.
- Classify formal guidance, milestone, scale threshold, medium-term ambition, long-term aspiration and qualitative strategy.
- Build a transparent scorecard using only mature, comparable, measurable targets. Explain exclusions.

**Phase 4 — scenario engine**
- Create low/base/high assumptions for AOV, order growth, advertising/RPO, delivery cost, store productivity, inventory transition and working capital.
- Separate management-provided target bridge from independent analyst assumptions.
- Add sensitivity analysis and warnings about non-linear relationships and unobserved cost structure.

**Phase 5 — research brief**
- Generate a professional analyst PDF/HTML brief with key observations, charts, methodology, management guidance, scenario sensitivity, source register and data-quality disclosures.
- Make the brief read like a junior equity-research / strategy analyst deliverable, not a college dashboard.
- No unsupported investment recommendation or causal claim.

**Phase 6 — Eternal integration (only after source upload)**
- Wait for matched Eternal letters, extract and validate them with the same source provenance discipline.
- Build the comparable metric-definition bridge before peer comparisons.
- Only then implement gap decomposition and cross-company lag tests.

## Required deliverables

- Working Python repository and CLI.
- SQLite schema and database.
- Reproducible ingestion pipeline.
- Unit, integration and data-quality tests.
- Swiggy-only analysis exports and visualisations.
- Guidance/strategy/evidence ledgers.
- Sensitivity model with explicit assumptions.
- Analyst research brief PDF and editable HTML.
- README with setup/run/test/build instructions.
- `methodology.md`, `data_dictionary.md`, and known-limitations documentation.

## Definition of done

The build is complete only when another developer can clone the repository, install dependencies, rebuild the database, run tests, reproduce every displayed metric, click through to the source page and understand which claims are source-derived versus analytical. A polished dashboard without defensible calculations does not count as completion.

Start by reporting the source inventory, then implement Phase 0 and Phase 1. Do not skip ahead to a flashy front end.
