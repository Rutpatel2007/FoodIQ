# FoodIQ — India's Food Delivery & Quick Commerce Competitive Intelligence Engine

FoodIQ is an institutional-grade financial intelligence, quantitative econometric, and competitive intelligence platform that systematically extracts, validates, normalizes, analyzes, and interprets corporate disclosures from India's two consumer-internet duopoly leaders:
1. **Eternal Limited** (formerly Zomato Limited: Zomato, Blinkit, District, Hyperpure, Bistro)
2. **Swiggy Limited** (Food Delivery, Instamart, Out-of-Home, Supply Chain, Platform Innovations)

FoodIQ transforms unstructured corporate filings, quarterly shareholder letters, and statutory prospectuses into a traceable, mathematically defensible, statistically verified, and comparability-governed competitive intelligence system.

---

## Key Differentiators & Financial Governance

- **100% Traceable Lineage:** Every metric observation links directly to its source document, physical PDF page, and SHA-256 checksum.
- **4-Tier Comparability Governance:** Enforces Level 1 (Directly Comparable) to Level 4 (Incomparable / Blocked) rules. Prohibits invalid operations (e.g. subtracting Blinkit 1P revenue from Swiggy 3P marketplace revenue).
- **Structural Break Accounting:** Reconciles Blinkit's Q2 FY26 first-party (1P) inventory transition, distinguishing headline reported growth (+756% YoY) from Like-for-Like (LFL) organic marketplace growth.
- **Management Credibility Engine:** Evaluates 26 management forward-looking commitments across 16 categories using a 7-tier delivery taxonomy. Computes strict and broad scorecards while strictly isolating pending multi-year commitments in the denominator.
- **Rigorous Econometric Testing:** Evaluates 12 cross-sectional and temporal relationships using Pearson $r$, Spearman $\rho$, $p$-values, Fisher $z$ 95% Confidence Intervals, first-difference detrending ($r_\Delta$), and Benjamini-Hochberg False Discovery Rate (FDR) multiple-testing correction ($q = 0.05$).
- **Multi-Segment Scenario Simulation Lab:** Isolates parameter pedigrees (`EMPIRICAL_ESTIMATE_OLS`, `MANAGEMENT_GUIDANCE`, `ANALYST_ASSUMPTION_NOT_EMPIRICAL_QC`), evaluates break-even thresholds (e.g., Instamart CM break-even AOV ₹813.20), runs 1,000-draw Monte Carlo uncertainty simulations, and persists custom scenarios to SQLite.
- **Zero Hallucination / Null Preservation:** Undisclosed metrics remain strictly `NULL`; silent coercion to zero is strictly prohibited.
- **Integrated Institutional Workstation:** High-density, dark-slate research terminal UI with 10 dedicated analytical workspaces served directly by FastAPI without any Node.js/npm dependencies.

---

## System Architecture

```
FoodIQ/
├── backend/
│   ├── alembic/                # Alembic database migrations
│   ├── app/
│   │   ├── analytics/          # Financial, competitive, credibility, econometric & scenario engines
│   │   │   ├── comparability_engine.py      # 4-tier comparability governance
│   │   │   ├── competitive_attribution.py   # Multi-dimensional gap calculations
│   │   │   ├── competitive_findings.py      # 8 verified research findings & calculations
│   │   │   ├── credibility_engine.py        # 16-category repo & 26 commitment scorecards
│   │   │   ├── financial_engine.py          # Unit economics & decomposition
│   │   │   ├── metric_reconciliation.py     # Disclosed vs derived metric availability
│   │   │   ├── scenario_lab.py              # Multi-segment simulation & Monte Carlo
│   │   │   ├── statistical_research.py      # 12 econometric studies & FDR testing
│   │   │   └── structural_breaks.py         # 1P transition, District & Lynks M&A
│   │   ├── api/v1/             # FastAPI REST routers (analytics, competitive, credibility, quant, scenarios)
│   │   ├── models/             # SQLAlchemy 2.0 ORM models (core, analytics, saved scenarios)
│   │   ├── schemas/            # Pydantic v2 validation models
│   │   ├── ingestion/          # Dedicated Swiggy & Eternal ingestion pipelines
│   │   ├── services/           # Provenance lineage & governance engines
│   │   ├── config.py           # Configuration & directory settings
│   │   ├── database.py         # SQLAlchemy engine & sessionmaker
│   │   └── main.py             # FastAPI entrypoint & frontend static mount
│   └── tests/                  # Automated test suite (113 tests, 100% pass rate)
├── frontend/                   # Institutional Research Terminal Workstation
│   ├── index.html              # Shell with 10 analytical workspace panes & quick workflow bar
│   ├── style.css               # Terminal design system (dark-slate, monospace data grid)
│   └── app.js                  # Analytical client, vector canvas charting, scenario cockpit
├── data/
│   ├── foodiq.db               # SQLite database with normalized analytical tables
│   ├── processed/              # Generated analytical CSVs
│   └── reports/                # Ingestion summary, data quality, and lineage reports
├── reports/                    # Formal phase validation reports, CSVs, and JSON deliverables
├── docs/                       # Technical specifications & research methodologies
├── FoodIQ_Swiggy_Compact/      # Swiggy raw shareholder letters (PDFs) & research pack
└── FoodIQ_Eternal_Compact/     # Eternal raw shareholder letters (PDFs) & transcripts
```

---

## Quickstart & Local Execution

### 1. Requirements
- Python 3.12+
- Dependencies installed via `pip install -r requirements.txt` (or requirements-dev.txt)

### 2. Launching the FoodIQ Research Workstation
Run the FastAPI application from the project root:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Once launched, open your web browser and navigate to:
- **Research Workstation UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc API Docs:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 3. Running Automated Test Suites
Run the entire 113-test backend test suite:
```bash
python -m pytest backend/tests/
```
Run specific phase verification suites:
```bash
# Phase 4 Credibility Engine (9 tests)
python -m pytest backend/tests/test_phase4_credibility_engine.py

# Phase 5 Quantitative Engine & Scenario Lab (11 tests)
python -m pytest backend/tests/test_phase5_quantitative_engine.py

# Phase 6 Institutional Workstation Integration (8 tests)
python -m pytest backend/tests/test_phase6_workstation_integration.py
```

---

## 10 Analytical Workstation Panes

1. **Executive Overview (`overview`):** Head-to-head KPI cards (Food GOV, QC GOV, Dark Stores, Food Margins, QC Margins), dynamic trend viewer, and competitive summary.
2. **Competitive Intelligence (`competitive`):** 4-tier comparability governance rules, cross-company gap analysis, 8 primary research findings, and structural break register.
3. **Food Delivery Core (`food-delivery`):** Multi-quarter historical GOV, order count, AOV, take rate, contribution margin, and Adjusted EBITDA margin comparisons.
4. **Quick Commerce Core (`quick-commerce`):** Blinkit vs Instamart store expansion, throughput (INR/store-day), density economics, and margin breakeven path.
5. **Management Credibility (`credibility`):** Guidance scorecards across 26 commitments and 16 categories, strict vs broad delivery rates, and isolated pending denominators.
6. **Narrative Verification (`narratives`):** 5 deep case studies testing corporate narratives against empirical facts, separating correlation from causality.
7. **Quantitative Research (`quantitative`):** 12 econometric studies with Pearson $r$, Spearman $\rho$, $p$-values, Fisher $z$ CIs, detrended $\Delta$ correlations, and Benjamini-Hochberg FDR correction.
8. **Scenario Lab (`scenarios`):** Multi-segment financial simulation with Base/Bull/Bear presets, 2D sensitivity grids, break-even solver, 1,000-draw Monte Carlo distributions, and SQLite scenario saving.
9. **Structural Breaks (`structural-breaks`):** 4 documented corporate structural breaks, including Blinkit 1P inventory model transition and M&A reconciliations.
10. **Lineage & Audit (`lineage`):** Document catalog, page registers, confidence scores, extraction provenance, and raw data lineage.

---

## 5 Guided Acceptance Workflows

The workstation toolbar includes one-click shortcuts to verify the platform's core research workflows:
- **Workflow A — Competitive Research:** Food delivery margin divergence, comparability governance, and 242 bps spread attribution.
- **Workflow B — Management Execution:** Track record inspection, strict delivery scorecard (Eternal: 83.3%, Swiggy: 75.0%), and commitment lifecycle tracking.
- **Workflow C — Quantitative Research:** Instamart AOV vs CM regression audit ($r = 0.5531$, but detrended $r_\Delta = 0.1399$), proving lack of synchronous margin causality.
- **Workflow D — Scenario Analysis:** Multi-segment stress testing, Instamart break-even AOV solver (₹813.20), Monte Carlo simulation, and scenario persistence.
- **Workflow E — Source Verification:** Finding 1 Blinkit store throughput calculation (₹849,924 / store-day, +22.0% growth) traced to physical shareholder letter page.

---

## Verification & Deliverables Summary

| Deliverable | Description | Location | Status |
| :--- | :--- | :--- | :--- |
| **Phase 4 Deliverables** | Commitments, scorecards, narrative case studies & methodologies | `reports/phase4_*`, `docs/phase4_*` | **VERIFIED (9/9 Tests Passed)** |
| **Phase 5 Deliverables** | 12 econometric studies, scenario validation, research limitations | `reports/phase5_*`, `docs/phase5_*` | **VERIFIED (11/11 Tests Passed)** |
| **Phase 6 Deliverables** | Workstation UI, acceptance test results, quality audit, API docs | `reports/phase6_*`, `docs/phase6_*` | **VERIFIED (8/8 Tests Passed)** |
| **Master Deliverables** | Architecture specs, canonical data dictionary, research methodology | `docs/foodiq_*`, `reports/phase4_5_6_*`| **VERIFIED (113/113 Tests Passed)** |
