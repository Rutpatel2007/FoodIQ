# FoodIQ — India's Food Delivery & Quick Commerce Competitive Intelligence Engine

FoodIQ is a research-grade financial intelligence and quantitative data platform that systematically extracts, validates, normalizes, analyzes, and interprets corporate disclosures from India's two leading consumer-internet platforms:
1. **Eternal Limited** (formerly Zomato Limited: Zomato, Blinkit, District, Hyperpure, Bistro)
2. **Swiggy Limited** (Food Delivery, Instamart, Out-of-Home, Supply Chain, Platform Innovations)

FoodIQ transforms unstructured shareholder letters and quarterly filings into a traceable, mathematically defensible, and comparability-governed competitive intelligence engine.

---

## Key Differentiators & Financial Governance
- **Source-to-Insight Provenance:** Every metric observation links directly to its source document, physical PDF page, and SHA-256 checksum.
- **Comparability Rules Engine:** Blocks invalid financial comparisons (e.g., Gross Order Value vs. Net Order Value).
- **Structural Break Accounting:** Adjusts for Blinkit's Q2 FY26 first-party (1P) inventory ownership transition, distinguishing reported growth (+756% YoY) from Like-for-Like (LFL) organic growth.
- **Dual-Pass OCR Validation:** Scanned table extractions are cross-referenced against multi-quarter comparative disclosures to resolve OCR errors.
- **Null Preservation:** Undisclosed metrics remain strictly `NULL`; silent coercion to zero is prohibited.
- **Longitudinal Guidance Tracker:** Evaluates management forward-looking commitments against subsequently reported metrics.

---

## Repository Structure
```
FoodIQ/
├── backend/
│   ├── alembic/                # Alembic database migrations
│   ├── app/
│   │   ├── api/v1/             # FastAPI REST endpoints
│   │   ├── models/             # SQLAlchemy 2.0 ORM models (16 tables)
│   │   ├── schemas/            # Pydantic v2 validation models
│   │   ├── ingestion/          # Dedicated Swiggy & Eternal ingestion pipelines
│   │   ├── services/           # Provenance lineage & governance engines
│   │   ├── config.py           # Configuration & directory settings
│   │   ├── database.py         # SQLAlchemy engine & sessionmaker
│   │   └── main.py             # FastAPI entrypoint
│   └── tests/                  # Automated test suite (27 unit & integration tests)
├── data/
│   ├── foodiq.db               # SQLite database with foreign keys & indexes
│   └── reports/                # Ingestion summary, data quality, and lineage reports
├── docs/                       # Technical specifications & documentation
│   ├── database_schema.md
│   ├── ingestion_architecture.md
│   ├── source_lineage.md
│   ├── data_quality.md
│   ├── comparability_governance.md
│   ├── api_reference.md
│   └── phase1_completion_report.md
├── FoodIQ_Swiggy_Compact/      # Swiggy raw shareholder letters (PDFs) & research pack
└── FoodIQ_Eternal_Compact/     # Eternal raw shareholder letters (PDFs) & transcripts
```

---

## Quickstart & Local Execution

### 1. Requirements
- Python 3.12+
- `pip install sqlalchemy pydantic fastapi uvicorn pytest alembic pandas httpx`

### 2. Apply Database Migrations
```bash
cd backend
alembic upgrade head
cd ..
```

### 3. Run Automated Ingestion & Generate Reports
```bash
python -m backend.app.ingestion.runner
```

### 4. Execute Automated Test Suite
```bash
pytest backend/tests -v
```

### 5. Launch FastAPI Server
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Phase Status
- [x] **Phase 0:** Source Audit & Architecture Specification
- [x] **Phase 1:** Complete Data Foundation, Ingestion, Provenance & Governance Backend
- [ ] **Phase 2:** Financial Analytics & Decomposition Core (Next)
- [ ] **Phase 3:** Competitive Intelligence & Structural Break Adjustments
- [ ] **Phase 4:** Management Intelligence & Guidance Credibility Scorecard
- [ ] **Phase 5:** Statistical Research Lab & Scenario Simulator
- [ ] **Phase 6:** Research Workstation Frontend (Next.js)
- [ ] **Phase 7:** Automated Institutional Report Generator
