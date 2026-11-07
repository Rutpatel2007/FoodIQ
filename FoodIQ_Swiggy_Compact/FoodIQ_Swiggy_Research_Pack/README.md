# FoodIQ — Swiggy Research Pack (v1)

This is the first source-grounded research handoff for FoodIQ. It structures six Swiggy quarterly shareholder letters and the user-provided seed data into a form that Antigravity can ingest and extend.

## Start here

1. `prompts/ANTIGRAVITY_MASTER_PROMPT.md`
2. `docs/ANTIGRAVITY_IMPLEMENTATION_SPEC.md`
3. `docs/EXTRACTION_SUMMARY.md`
4. `docs/DATA_QUALITY_AND_SOURCE_AUDIT.md`
5. `docs/DATA_DICTIONARY_AND_METHODS.md`
6. `docs/FOODIQ_ANALYTICAL_HYPOTHESES.md`

## Important limitation

This is **Swiggy-only**. No Eternal shareholder letters were supplied in this upload batch. Do not create competitive comparison outputs until the corresponding Eternal data has been extracted and validated.

## Data folders

- `sources/pdfs/`: original PDFs
- `sources/full_text/`: full `pdftotext -layout` extracts
- `sources/page_text/all_pages.jsonl`: page-indexed complete text archive
- `data/raw/`: long-form metrics
- `data/curated/`: wide KPI panel, definitions, reconciliation, management evidence, guidance, operational claims and initiatives
- `data/quality/`: known discrepancies and data-quality controls
- `reference/`: original project specification

All metric and commentary ledgers include source file / page references. Some values originating in the user's starter CSV are explicitly marked as unverified until each source value has been confirmed. Null values are intentional; do not convert them to zero.
