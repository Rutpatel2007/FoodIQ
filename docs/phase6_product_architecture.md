# FoodIQ Phase 6 — Product Architecture Specification

## 1. Architectural Overview

FoodIQ is architected as an institutional-grade financial intelligence and quantitative research platform. It integrates a deterministic data pipeline, relational database, multi-tier financial engines, econometric analysis, scenario simulation, and an interactive high-density research workstation.

```mermaid
flowchart TD
    subgraph Data Tier [Phase 1 & Phase 1.1 Data Tier]
        DB[(SQLite / foodiq.db)]
        DOCS[Corporate Disclosures / PDFs]
        OCR[Page Indexer & OCR Validator]
        DOCS --> OCR --> DB
    end

    subgraph Analytics Tier [Phase 2, 3, 4, 5 Analytics Core]
        FIN[Phase 2: Financial Analytics & Unit Economics]
        COMP[Phase 3: Competitive Intelligence & Structural Breaks]
        CRED[Phase 4: Management Credibility & Narrative Verification]
        STAT[Phase 5: Econometric Research & Scenario Lab]
        DB --> FIN
        DB --> COMP
        DB --> CRED
        DB --> STAT
    end

    subgraph API Tier [FastAPI REST Gateway]
        API_A[/api/v1/analytics]
        API_C[/api/v1/competitive]
        API_CR[/api/v1/credibility]
        API_Q[/api/v1/quantitative]
        API_S[/api/v1/scenarios]
        API_D[/api/v1/documents]
        FIN --> API_A
        COMP --> API_C
        CRED --> API_CR
        STAT --> API_Q
        STAT --> API_S
        DB --> API_D
    end

    subgraph Frontend Tier [Phase 6 Research Workstation]
        STATIC[FastAPI Static File Mount]
        SHELL[Workstation Shell: index.html]
        STYLE[Terminal Styling: style.css]
        CLIENT[Analytical Client: app.js]
        CANVAS[Native Canvas Vector Charts]
        API_A & API_C & API_CR & API_Q & API_S & API_D --> CLIENT
        CLIENT --> CANVAS
        STATIC --> SHELL & STYLE & CLIENT
    end
```

---

## 2. Component Specifications

### 2.1 Backend Server & API Routing
- **Framework:** FastAPI 0.115+ running on Python 3.12 with asynchronous and synchronous execution support.
- **ORM & Database:** SQLAlchemy 2.0 with SQLite engine (`data/foodiq.db`), foreign keys enforced (`PRAGMA foreign_keys = ON`), WAL mode enabled for concurrent queries.
- **Stateless Analytical Modules:** Functional analytics modules (`backend/app/analytics/*`) perform on-demand aggregation, econometric testing, and scenario matrix mathematics with zero side effects.

### 2.2 Client-Side Single Page Workstation
- **Mounting:** Mounted via `app.mount("/static", StaticFiles(directory="frontend"), name="static")` and served at root `/`.
- **Zero Build Step:** Native modern JavaScript (ES6+), CSS3 Flexbox/Grid, and HTML5 Canvas. Requires no Node.js compilation, npm bundling, or webpack overhead.
- **Instant Hot-Loading:** Client state transitions, tab navigation, and scenario parameter updates render in under 100ms.
- **Native Canvas Graphics:** Dual-series line charts with dynamic min/max scaling, zero-line baselines, hover tooltip interpolation, and legend rendering written in pure HTML5 Canvas.

---

## 3. Data Integrity & Provenance Governance

1. **Deterministic Execution:** No synthetic, hallucinated, or extrapolated financial figures. Where corporate disclosures are silent, metrics evaluate to `NULL`.
2. **Comparability Enforcement:** Every cross-company comparison is governed by the 4-tier taxonomy (`LEVEL_1` Directly Comparable to `LEVEL_4` Incomparable). Level 4 subtractions are blocked at the engine and API level.
3. **Parameter Pedigree Isolation:** All scenario simulation inputs are explicitly tagged (`EMPIRICAL_ESTIMATE_OLS`, `MANAGEMENT_GUIDANCE`, `ANALYST_ASSUMPTION_NOT_EMPIRICAL_QC`), preventing cross-contamination between empirical estimates and subjective assumptions.
4. **Audit Trail:** Every visual card, finding, and tabular cell features a traceable source document link and physical filing page reference.
