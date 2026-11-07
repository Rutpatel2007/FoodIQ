# FoodIQ — Antigravity implementation specification

## Mission
Build a reproducible financial and competitive intelligence engine from public shareholder disclosures. The supplied pack is a Swiggy-only first tranche. The application and database must support Eternal, but must not fabricate Eternal observations or display peer comparisons until the user supplies matched Eternal source letters.

## Non-negotiable engineering principles

1. `sources/pdfs/` are immutable source documents. Never rewrite them.
2. The long-form observation model is canonical. A wide CSV is only a derived convenience view.
3. Every source-reported number must have `document_id`, `pdf_page`, `printed_page` if known, `source_section`, `extraction_method`, `value_status` and report version.
4. Distinguish reported data, calculated data, management estimates, user-supplied unverified values and modelling assumptions.
5. Never fill missing values with 0. Null is not zero.
6. Never invent Food/Out-of-Home NOV for Swiggy; use GOV unless source explicitly discloses NOV.
7. Never mix B2C GOV with consolidated revenue/EBITDA in one scope or calculate an implied group take-rate/margin from mismatched denominators.
8. Keep AOV and nAOV separate; keep monthly milestone and quarterly average margin separate.
9. Source conflicts are first-class records, not overwritten data.
10. All charts and claims must show scope, unit, denominator, period and evidence/source.
11. Statistical inference must be modest; small sample size must be visible.
12. Any change to extraction / calculated values requires tests and updated provenance.

## Suggested repository structure

```text
foodiq/
  data/
    source/                 # immutable uploaded PDFs, git-annex/LFS or local gitignored
    raw/                    # source transcriptions CSV/JSONL as delivered
    curated/                # curated ledgers from this pack
    processed/              # generated outputs only
  src/foodiq/
    ingestion/               # PDF text, table, chart and page extraction interfaces
    normalization/           # units, quarter keys, definitions, mapping
    database/                # schema, migrations, loaders, repositories
    validation/              # source reconciliation, range and integrity checks
    analytics/               # decomposition, unit economics, guidance, stats
    scenarios/               # parameterised scenario engine
    reporting/               # charts, HTML/PDF brief
    cli.py
  templates/
  outputs/
  tests/
  docs/
```

## Database design

Implement a normalized SQLite database with, at minimum:

- `companies(company_id, canonical_name, ticker, home_market)`
- `documents(document_id, company_id, quarter, title, publication_date, file_path, sha256, page_count, source_type)`
- `document_pages(page_id, document_id, pdf_page, printed_page, section, extracted_text, extraction_quality)`
- `metric_definitions(metric_id, metric_name, company_id_nullable, segment, definition, numerator, denominator, unit, effective_from, effective_to, source_document_id, source_page, comparability_notes)`
- `metric_observations(observation_id, company_id, quarter_id, segment, metric_id, value, unit, denominator, scope, value_status, source_document_id, source_page, source_excerpt, report_version, created_at)`
- `qualitative_evidence(evidence_id, document_id, page, section, theme, segment, text, text_type, evidence_type, analyst_interpretation, tags)`
- `management_guidance(guidance_id, document_id, issued_quarter, metric_id_nullable, statement, target_period, target_operator, target_value, target_unit, scope, guidance_class, assessment_status, assessment_notes)`
- `operational_claims(claim_id, document_id, page, segment, metric, value, unit, period, population, definition, source_text, status)`
- `strategic_initiatives(initiative_id, name, segment, start_quarter, status, description, intended_mechanism)`
- `initiative_evidence(initiative_id, document_id, page, metric, value, unit, text, period)`
- `financial_reconciliations(reconciliation_id, document_id, quarter, metric, value, unit, scope, page)`
- `source_conflicts(conflict_id, metric_id, quarter, observation_a_id, observation_b_id, reason, resolution_status, note)`
- `structural_breaks(event_id, company_id, quarter, event_type, description, affected_segments, source_document_id, source_page)`
- `scenario_assumptions(assumption_id, model_name, variable, low_value, base_value, high_value, unit, rationale, evidence_status, source_reference)`
- `data_quality_issues(issue_id, severity, area, issue, impact, required_action, status)`

Use foreign keys, unique constraints that do not destroy source-version observations, and indexes on company/quarter/segment/metric/source document.

## Ingestion and validation

- Load all delivered CSV/JSONL into staging tables.
- Validate document identifiers and page references against `source_register.csv` and page archive.
- Validate uniqueness by company + quarter + segment + metric + source_document_version (not merely company/quarter/segment; that would erase historical source conflicts).
- Validate units, denominator, fiscal quarter sequence, required columns and types.
- Do not set universal arbitrary bounds for metrics; make outliers warnings unless impossible under the definition.
- Validate exact mathematical identities only where expected (e.g. EBITDA margin × denominator ≈ EBITDA, allowing source rounding).
- Reconcile segment sums to group numbers only when scopes and eliminations permit.
- Every unresolved data issue must appear in a report warning panel and CI test output.

## Analytics modules

### 1. Growth and decomposition
- GOV quarterly and annual growth.
- Price / volume decomposition from order counts and AOV when source series share the same definition.
- Display rounding residual; do not force exact reconciliation by silently changing source values.
- For Food use GOV, not invented NOV.

### 2. Unit economics
- Monetary contribution margin = GOV × CM%.
- Adjusted EBITDA margin with segment-specific denominator.
- RPO, orders/store/day, GOV/sqft, NOV/GOV, store counts/area, MTU, frequency and retention.
- Store maturity / capacity / utilisation panel only where source definitions permit.

### 3. Management guidance
- Guidance classification, target and outcome tracker.
- Separate target value from latest actual; statuses include pending, achieved milestone, in range, approximately met, missed, not assessable.
- Calculate hit rates only on comparable, mature, measurable commitments; show denominators and exclusion reasons.

### 4. Management narrative evidence
- Theme tagging and claim-to-outcome crosswalk.
- Distinguish source statement from analyst interpretation.
- Use “supported / partially supported / contradicted / untestable” only when a measurable future observation exists.

### 5. Scenario analysis
- Parameterise AOV, order volume, discount/mix, RPO/take-rate, delivery cost, store productivity, inventory ownership and working capital.
- Display low/base/high and tornado / sensitivity outputs.
- Preserve management scenario separately from FoodIQ independent scenario.
- Explicitly label simplified assumptions, unknown cost elasticities and non-linear effects.

### 6. Comparative analysis (blocked pending Eternal data)
- Schema supports Eternal but UI/data reports must show “waiting for matched source data” rather than empty-as-zero values.
- Comparable-quarter mapping and metric-definition bridge required.
- Lead/lag tests use explicit sequence joins.
- Include sample size and confidence limits.

## Reporting outputs

1. Analyst research brief (4–8 pages, generated, editable HTML plus PDF).
2. Source-linked metric tables / CSV exports.
3. Guidance scorecard.
4. Growth-quality and unit-economics panel.
5. Scenario sensitivity report.
6. Quality / source-conflict appendix.
7. Optional web dashboard as a supporting view, not the main deliverable.

The primary product is an evidence-backed analyst brief, not a generic dashboard.

## Test requirements

- Unit tests for all financial formulas, unit conversions and quarter alignment.
- Ingestion idempotency tests.
- Source page existence tests.
- Null-versus-zero tests.
- Conflict-preservation tests.
- Metric denominator consistency tests.
- Reconciliation tests for monetary margin and disclosed arithmetic.
- Guidance status tests: not-yet-due ambition cannot be scored missed.
- Regression tests for Q1FY27 MTU/frequency source conflicts.
- Tests verifying no Swiggy Food/OOH NOV is fabricated.
- Snapshot tests for at least one chart and report rendered from the current data.

## Acceptance criteria

- User can rebuild SQLite from source data in one command.
- User can run tests and see clear results.
- Every key finding links to source document/page and states reported / derived / management estimate / assumption.
- No synthetic Eternal data, no assumed Food/OOH NOV, no unlabelled scenario coefficient.
- Q2FY27 is included in all applicable Swiggy series.
- Historical source conflict observations survive ingestion and reporting.
- PDF brief includes limitations, not only positive findings.
- All major calculations can be explained line by line in an internship interview.
