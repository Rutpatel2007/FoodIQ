# FoodIQ v1.1 — System Architecture Specification
**Document Reference:** DOC-V11-08  
**Classification:** Technical System Design & Engineering  

---

## 1. Architectural Topology

FoodIQ is built as a high-performance, single-node asynchronous research engine:

```
┌────────────────────────────────────────────────────────┐
│               Frontend Presentation Layer              │
│  - Single Page Application (HTML5 / ES6 Modules / CSS) │
│  - Zero Node Build Step; Instant Hot Reloading         │
│  - 10 Specialized Research Workspaces                  │
└───────────────────────────▲────────────────────────────┘
                            │ REST / JSON (HTTP)
┌───────────────────────────▼────────────────────────────┐
│               Backend Application Layer                │
│  - FastAPI (Python 3.11 Asynchronous Framework)        │
│  - Uvicorn ASGI Server                                 │
│  - 21 Analytics Modules (Econometrics, Bridges, Monte) │
│  - Pydantic V2 Request & Response Data Contracts       │
└───────────────────────────▲────────────────────────────┘
                            │ Parameterized SQL
┌───────────────────────────▼────────────────────────────┐
│                Data & Storage Engine                   │
│  - SQLite 3.35+ with Write-Ahead Logging (WAL)         │
│  - 24 Relational Tables                                │
│  - PyMuPDF Vector PDF Coordinate Cache                 │
└────────────────────────────────────────────────────────┘
```

---

## 2. Analytics Subsystem Organization

All analytical computation resides in `backend/app/analytics/`:
- `financial_core.py`: Normalization, waterfalls, and segment calculations.
- `statistical_research.py`: Empirical studies REL-001–012, FDR control.
- `credibility_engine.py`: Commitment registers and credibility scorecards.
- `scenario_simulator.py`: Monte Carlo engine and deterministic AOV sensitivity.
- `comparability_engine.py`: Rule validation and cross-company operation filters.
- `lineage_engine.py`: Coordinate grounding and PDF bounding box extraction.
