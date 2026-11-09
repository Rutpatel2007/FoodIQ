# FoodIQ

An evidence-driven financial and competitive intelligence platform analysing the operating performance, unit economics and competitive positioning of Eternal Limited and Swiggy Limited.

---

## Overview

FoodIQ is an institutional-quality financial intelligence platform engineered for equity research analysts, quantitative researchers, and corporate strategy teams covering the Indian listed internet ecosystem. The platform systematically normalises, analyses, and models statutory corporate disclosures filed with the National Stock Exchange of India (NSE) and BSE Limited for **Eternal Limited (Zomato / Blinkit / Hyperpure)** and **Swiggy Limited**.

FoodIQ addresses a fundamental problem in on-demand platform research: corporate disclosures in food delivery and quick commerce frequently utilise divergent metric definitions, non-standardized denominators, and shifting accounting scopes. FoodIQ resolves this by enforcing strict financial normalization waterfalls, a four-tier comparability governance engine, econometric validation with False Discovery Rate (FDR) control, and coordinate-grounded source traceability linking every data point back to primary filings.

---

## Key Capabilities

- **Financial Performance Analysis:** Standardized order value waterfalls separating Gross Merchandise Value (GMV), Net Order Value (NOV), and Gross Order Value (GOV).
- **Segment-Level Comparisons:** Detailed segmental tracking across Food Delivery, Quick Commerce, B2B Supplies (Hyperpure), and Out-of-Home Dining.
- **Unit Economics & Margin Bridges:** 5-step additive margin bridges from Take Rate to Variable Costs, Contribution Margin, Dark Store Leases, and Segment Adjusted EBITDA.
- **Competitive Intelligence:** Real-time gap analysis across GOV market share, average order value (AOV), dark store density, and take rates.
- **Structural-Break Analysis:** Event-study framework tracking the quantitative impact of corporate actions (Blinkit 1P-to-3P transition, convenience platform fees, IPO listing).
- **Management Commitment Tracking:** Objective evaluation of 26 forward-looking executive guidance statements using strict and broad delivery scoring algorithms.
- **Quantitative Research:** Econometric suite comprising 12 empirical relationship studies with Benjamini-Hochberg FDR control and first-difference detrending.
- **Scenario Modelling:** Deterministic AOV elasticity calculations and 10,000-run Monte Carlo simulations for quick commerce dark store expansion.
- **Source Traceability:** Primary document store indexing 14 statutory filings with vector bounding box coordinates `(x0, y0, x1, y1)` for one-click audit verification.
- **Research Report Generation:** Automated compilation of institutional equity research briefs with verified citations across HTML, PDF, DOCX, and CSV formats.

---

## Technology Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn (ASGI)
- **Database:** SQLite 3 (Write-Ahead Logging enabled), SQLAlchemy, Alembic
- **Analytics & Statistics:** Pandas, NumPy, SciPy (OLS regressions, FDR step-down, Monte Carlo)
- **Document Processing:** PyMuPDF (fitz) for vector coordinate extraction
- **Frontend:** HTML5, CSS3, JavaScript (ES6+ modular architecture, Tailwind CSS)
- **Testing:** Pytest, HTTPX, Coverage

---

## Architecture

The platform follows a layered, deterministic data and analytical flow:

```text
[Primary Regulatory Filings (BSE / NSE PDFs)]
                     │
                     ▼
  [Vector PDF Extraction & Coordinate Indexing]
                     │
                     ▼
      [Relational Database (SQLite / WAL)]
  - Canonical Metric Definitions & Observations
  - Governance Rules & Structural Breaks
                     │
                     ▼
          [Financial Analytics Core]
  - Order Value Waterfalls & Margin Bridges
  - Econometric Suite & Credibility Engine
                     │
                     ▼
             [FastAPI REST API]
  - Domain Endpoints (/metrics, /analytics, etc.)
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
[Institutional Workstation] [Research Reports]
  (10 Interactive Workspaces) (HTML, PDF, DOCX)
```

---

## Project Structure

```text
FoodIQ/
├── backend/
│   ├── alembic/                 # Database schema migrations
│   ├── app/
│   │   ├── analytics/           # 21 domain analytical modules
│   │   ├── api/v1/              # FastAPI REST routes
│   │   ├── core/                # Core utilities, logging, config
│   │   ├── db/                  # SQLite connection and session setup
│   │   ├── ingestion/           # Data ingestion pipelines
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic schemas and data contracts
│   │   ├── services/            # Business validation services
│   │   ├── config.py            # Application settings and paths
│   │   └── main.py              # Application entrypoint
│   └── tests/                   # 145 unit and integration tests
├── frontend/
│   ├── assets/                  # Logos and visual icons
│   ├── css/                     # Styling sheets
│   ├── js/                      # Workstation UI logic
│   └── index.html               # Single-page workstation interface
├── data/
│   ├── processed/               # Canonical normalized datasets
│   ├── reports/                 # Research report templates and exports
│   └── foodiq.db                # Primary SQLite database
├── docs/
│   ├── ARCHITECTURE.md          # Comprehensive architecture overview
│   ├── DATA_AND_METHODOLOGY.md  # Detailed financial & econometric formulas
│   ├── API.md                   # REST API documentation
│   └── DEVELOPMENT.md           # Setup, testing, and operations guide
├── archive/                     # Archived raw filings and research packages (local)
├── scripts/
│   ├── backup_db.py             # Database snapshot utility
│   ├── restore_db.py            # Database recovery utility
│   └── verify_workflows.py      # End-to-end integration test runner
├── .env.example                 # Environment configuration template
├── .gitignore                   # Repository exclusion rules
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Container orchestration
├── requirements.txt             # Production dependencies
├── run_foodiq.bat               # Windows startup script
└── run_foodiq.sh                # Linux/macOS startup script
```

---

## Installation and Execution

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Setup Environment
```bash
git clone https://github.com/rutpatel/FoodIQ.git
cd FoodIQ

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Application
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
- **Web Workstation UI:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Documentation (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Documentation (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testing

Execute the complete regression test suite:

```bash
pytest backend/tests/ -v
```

Current test suite baseline: **145 tests passed across 19 test modules**.

---

## Data and Methodology Notes

- **Metric Comparability:** Company-reported metrics often use different accounting bases. For instance, Swiggy reports Quick Commerce contribution margin as a percentage of GOV, while early Blinkit disclosures referenced NOV. Direct cross-company subtractions between metrics with mismatched denominators are programmatically blocked under Tier 4 of the Comparability Framework.
- **Data Integrity:** Values not explicitly disclosed in primary regulatory filings (e.g., Swiggy Food Delivery Net Order Value) are stored strictly as `NULL`. FoodIQ does not interpolate or fabricate missing financial data points.
- **Econometric Guardrails:** Due to small sample sizes ($N = 10 \text{ to } 14$ quarters), all empirical regressions are subjected to Benjamini-Hochberg False Discovery Rate (FDR) adjustments at $q = 0.05$ and first-difference detrending to guard against spurious trending correlations.

---

## Limitations

- **Private Entity Comparisons:** Peer data for Zepto represents unlisted, unaudited secondary disclosures from funding filings and MCA records. These are designated as reference benchmarks and excluded from statutory econometric models.
- **Reporting Horizon:** Indian quick commerce public filings span a limited time horizon (commencing FY24/FY25). Statistical relationships must be interpreted within their reported sample size boundaries.
- **Non-Disclosed Segments:** Segmental Net Order Value for Swiggy Food Delivery remains unpublished by the company, preventing like-for-like NOV comparisons with Blinkit.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
