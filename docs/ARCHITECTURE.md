# FoodIQ — System Architecture & Technical Design

## 1. Architectural Overview

FoodIQ is an institutional-grade corporate financial intelligence platform engineered for equity research analysts, quantitative researchers, and corporate strategy teams. It provides deep-dive analytics, econometric modelling, management credibility tracking, and coordinate-grounded source traceability for India's listed on-demand internet duopoly: **Eternal Limited (Zomato / Blinkit / Hyperpure)** and **Swiggy Limited**.

The platform is designed around deterministic financial integrity, strict comparability standards, and verifiable primary disclosures.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Frontend Workstation UI                         │
│  - Vanilla JavaScript (ES6+), Modern Semantic HTML5, Tailwind CSS      │
│  - 10 Specialized Workspaces (Overview, Intel, Econometrics, Scenarios)│
│  - Interactive Document Viewer with Coordinate Bounding-Box Overlays   │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │ HTTP / REST / JSON
┌───────────────────────────────────▼────────────────────────────────────┐
│                       FastAPI Application Layer                        │
│  - Uvicorn ASGI Server (Asynchronous High-Throughput Processing)       │
│  - Domain-Driven API Routers (/metrics, /analytics, /econometrics, etc)│
│  - Pydantic V2 Request Validation and Serialized Data Contracts        │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                       Analytics & Research Core                        │
│  - Financial Core: Take rate bridges, margin decompositions, AOV       │
│  - Econometric Lab: 12 empirical studies, Benjamini-Hochberg FDR       │
│  - Credibility Engine: 26 tracked commitments, strict/broad scorecards │
│  - Scenario Simulator: Monte Carlo engine, deterministic elasticity    │
│  - Governance: 4-tier comparability rules, structural break registry   │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │ Parameterized SQL
┌───────────────────────────────────▼────────────────────────────────────┐
│                        Data & Storage Subsystem                        │
│  - SQLite 3 with Write-Ahead Logging (WAL) Mode                        │
│  - 24 Relational Tables, 1,883 Records, 570 Canonical Metric Values    │
│  - PyMuPDF Vector Document Extraction & Coordinate Cache               │
│  - 14 Primary Regulatory Filings (BSE & NSE Statutory Disclosures)     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Directory Structure

```text
FoodIQ/
├── backend/
│   ├── alembic/                 # Database migrations
│   ├── app/
│   │   ├── analytics/           # 21 domain analytics modules
│   │   ├── api/v1/              # FastAPI REST endpoints
│   │   ├── core/                # Core utilities, logging, errors
│   │   ├── db/                  # SQLite connection and session lifecycle
│   │   ├── ingestion/           # Data ingestion and OCR pipelines
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic schemas and data contracts
│   │   ├── services/            # Business services and validation
│   │   ├── config.py            # Application settings and paths
│   │   └── main.py              # Application entrypoint and router mount
│   ├── tests/                   # 145 unit, integration, and regression tests
│   └── requirements.txt         # Backend dependencies
├── frontend/
│   ├── assets/                  # Logos and visual icons
│   ├── css/                     # Styling rules
│   ├── js/                      # Modular workstation logic
│   └── index.html               # 10-workspace institutional interface
├── data/
│   ├── processed/               # Canonical wide metric datasets
│   ├── reports/                 # Generated export directories
│   └── foodiq.db                # Primary SQLite database
├── docs/                        # Technical documentation
│   ├── ARCHITECTURE.md          # System architecture (this document)
│   ├── DATA_AND_METHODOLOGY.md  # Financial & econometric methodology
│   ├── API.md                   # REST API documentation
│   └── DEVELOPMENT.md           # Development, testing, and operations
├── FoodIQ_Eternal_Compact/      # Eternal primary filings and extracted text
├── FoodIQ_Swiggy_Compact/       # Swiggy primary filings and extracted text
├── scripts/                     # Operational utilities (backup, verify)
├── .env.example                 # Environment variables template
├── .gitignore                   # Production repository exclusions
├── Dockerfile                   # Production container definition
├── docker-compose.yml           # Multi-container orchestration
├── README.md                    # Main repository presentation
├── requirements.txt             # Primary production requirements
└── run_foodiq.bat / .sh         # One-click startup scripts
```

---

## 3. Database Architecture

The SQLite relational core (`data/foodiq.db`) is configured for high concurrency using `PRAGMA journal_mode = WAL;` and foreign key enforcement.

### Key Schema Entities:
- **`companies`**: Registry of tracked corporate entities (`Eternal`, `Swiggy`, and reference peers).
- **`reporting_periods`**: Fiscal calendar quarters (`Q1 FY24` through `Q2 FY27`).
- **`segments`**: Operating divisions (`Food Delivery`, `Quick Commerce`, `Hyperpure / B2B`, `Going-Out`).
- **`metric_definitions`**: 85 canonical metrics with standardized units, denominators, and comparability tiers.
- **`metric_observations`**: 570 verified empirical time-series data points linking directly to source documents.
- **`source_documents`**: 14 statutory filings with cryptographic SHA-256 hashes and publication metadata.
- **`source_pages`**: 509 cataloged pages with coordinate bounding-box indices.
- **`comparability_rules`**: 6 formal governance rules restricting invalid cross-company operations.
- **`structural_breaks`**: 12 corporate actions (acquisitions, fee changes, IPOs) modifying reporting bases.
- **`management_commitments`**: 26 executive guidance statements with verification status and verbatim citations.

---

## 4. Analytical Subsystem Modules

The analytics suite in `backend/app/analytics/` contains 21 specialized modules:

1. **`financial_core.py`**: Multi-segment normalization, take rate calculations, and order value waterfalls.
2. **`margin_bridge.py`**: Five-tier margin bridge (Take Rate $\to$ Variable Costs $\to$ CM $\to$ Leases $\to$ Adjusted EBITDA).
3. **`network_productivity.py`**: Dark store throughput modeling, store cohort maturity curves, and density metrics.
4. **`statistical_research.py`**: 12 empirical relationship studies with Benjamini-Hochberg FDR control.
5. **`scenario_simulator.py`**: Deterministic AOV elasticity calculations and 10,000-run Monte Carlo simulations.
6. **`credibility_engine.py`**: Strict and broad management delivery scorecards.
7. **`comparability_engine.py`**: Four-tier comparability enforcement preventing invalid metric arithmetic.
8. **`report_engine.py`**: Multi-format research report compilation (HTML, PDF, DOCX, CSV).
