# FoodIQ — India's Food Delivery & Quick Commerce Competitive Intelligence Engine

**Release Version:** `v3.1.0-RELEASE`  
**Certification Verdict:** **PASS (100% Test Pass Rate, 139 / 139 Tests Passing, 91% Statement Coverage)**  
**Target Entities:** **Eternal Limited** (Zomato, Blinkit, District, Hyperpure) & **Swiggy Limited** (Food Delivery, Instamart, Out-of-Home, Supply Chain)

---

## 1. Executive Overview

FoodIQ is an institutional-grade corporate financial intelligence, quantitative econometric, and competitive intelligence platform. It systematically extracts, normalizes, analyzes, and interprets statutory corporate disclosures from India's consumer-internet food and delivery duopoly leaders.

FoodIQ is not a generic stock-market dashboard or financial ratio calculator. It is a research workstation and report-generation system that transforms unstructured shareholder letters, quarterly results, and IPO prospectuses into a traceable, mathematically defensible, statistically verified, and comparability-governed competitive intelligence system.

---

## 2. Platform Architecture Across All 10 Phases

```mermaid
flowchart TD
    subgraph Data Foundation [Phases 1, 1.1, 8 — Ingestion & Governance]
        PDF[Statutory Filings & Disclosures]
        REG[Persistent Disclosure Register · SHA-256]
        ING[10-Stage Controlled Ingestion Pipeline]
        DB[(Relational Core: SQLite / foodiq.db)]
        ANOM[Automated Anomaly & Identity Scanner]
        PDF --> REG --> ING --> DB
        DB --> ANOM
    end

    subgraph Analytical Engines [Phases 2, 3, 4, 5 — Quantitative & Financial Core]
        FIN[Phase 2: Financial Decomposition & Margin Bridges]
        COMP[Phase 3: 4-Tier Comparability & Structural Breaks]
        CRED[Phase 4: Management Credibility & Narrative Verification]
        ECON[Phase 5: 12 Econometric Studies & BH FDR q=0.05]
        SCEN[Phase 5: Scenario Lab · Break-Even · Monte Carlo]
        DB --> FIN & COMP & CRED & ECON & SCEN
    end

    subgraph Gateway & Services [Phases 6, 7, 9 — API Gateway & Reporting]
        REST[FastAPI REST API Gateway · 14 Routers]
        REP[Phase 7: Modular Report Studio Engine]
        EXP[Multi-Format Compiler: HTML / PDF / DOCX / CSV]
        SEC[Phase 9: Security · Path Traversal · Online Backup]
        FIN & COMP & CRED & ECON & SCEN --> REST
        REST --> REP --> EXP
        REST --> SEC
    end

    subgraph User Experience [Phases 6, 10 — Workstation & Workflows]
        UI[Institutional Research Terminal Workstation]
        CANVAS[High-Performance HTML5 Vector Canvas Engine]
        WORKFLOWS[7 End-to-End Certified Workflows A-G]
        REST --> UI
        UI --> CANVAS & WORKFLOWS
    end
```

---

## 3. Key Financial Capabilities & Institutional Guardrails

- **Zero Data Hallucination:** Undisclosed metrics remain strictly `NULL`. No synthetic values are ever imputed.
- **Traceable Lineage (6-Layer Reconciliation):** Every factual observation traces from UI $\to$ API $\to$ Analytical Engine $\to$ Database Record $\to$ Source Filing $\to$ Physical PDF Page.
- **4-Tier Comparability Governance:** Enforces Level 1 (Directly Comparable) through Level 4 (Incomparable / Blocked). Directly blocks mathematical subtractions across fundamentally different business models (e.g. Blinkit 1P inventory revenue vs. Swiggy 3P marketplace commission revenue).
- **Repaired Network Productivity:** Blinkit dark store throughput verified at **₹849,924 / store-day (+22.0% growth)** using true disclosed Net Order Value (NOV: ₹20,940 Cr) across 2,700 guided stores.
- **Management Guidance Scorecard:** 26 commitments tracked across 16 categories using a 7-tier delivery taxonomy. Multi-year commitments (e.g. Swiggy's 11 IPO prospectus targets for FY28) are strictly isolated in the denominator to avoid artificial delivery penalties.
- **12 Econometric Studies with Detrending & FDR:** Proves that synchronous quarter-on-quarter jumps in Instamart AOV do **not** explain same-quarter margin expansion ($r=0.5531$, but detrended first-difference correlation collapses to $r_\Delta = 0.1399, p=0.72$). Multiple testing controlled via Benjamini-Hochberg FDR ($q=0.05$).
- **Scenario Simulation Cockpit:** Solves for **Instamart Contribution Margin Break-Even AOV: ₹813.20** (+₹105.20 from Q2 FY27 level of ₹708.00). Runs 1,000-draw Monte Carlo simulations and persists custom scenarios to SQLite.
- **9 Institutional Report Types:** Generates publication-ready reports in **HTML, PDF (via headless Chromium), DOCX (OpenXML), and CSV** with automated verification scorecards.
- **Disclosure Intelligence:** Persistent register with SHA-256 deduplication, analyst approval/rollback controls, and automated anomaly scanner.
- **Operational Reliability:** Sub-100ms analytical queries, zero-downtime online SQLite backups, and portable path architecture.

---

## 4. Quickstart & Installation

### Option A: Local Execution (Windows)
```bat
REM 1. Clone repository
git clone https://github.com/Rut-1704/FoodIQ.git
cd FoodIQ

REM 2. Install production dependencies
pip install -r requirements.txt

REM 3. Launch FoodIQ Workstation & API
run_foodiq.bat
```

### Option B: Local Execution (Linux / macOS)
```bash
# 1. Install production dependencies
pip3 install -r requirements.txt

# 2. Grant script permissions and launch
chmod +x run_foodiq.sh
./run_foodiq.sh
```

### Option C: Docker Container Deployment
```bash
docker compose up -d --build
```

Once launched:
- **Research Workstation UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger REST API:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Deep Readiness Probe:** [http://127.0.0.1:8000/api/v1/health/ready](http://127.0.0.1:8000/api/v1/health/ready)

---

## 5. Running the Complete Automated Test Suite

FoodIQ includes 139 automated unit, integration, performance, and certification tests:

```bash
# Run all 139 tests across Phases 1 through 10
python -m pytest backend/tests/

# Run with statement coverage measurement
python -m pytest backend/tests/ --cov=backend/app --cov-report=term
```

### Individual Test Suites
- `test_analytics_engines.py`: Phase 2 waterfall decomposition, margin bridges, unit economics (28 tests).
- `test_comparability_governance.py`: Phase 3 4-tier comparability rules and Level 4 blocking (3 tests).
- `test_phase3_1_audit.py`: Phase 3.1 audit fixes and Blinkit throughput verification (11 tests).
- `test_phase4_credibility_engine.py`: Phase 4 management credibility and narrative case studies (9 tests).
- `test_phase5_quantitative_engine.py`: Phase 5 econometric studies, FDR testing, scenario lab (11 tests).
- `test_phase6_workstation_integration.py`: Phase 6 workstation shell and browser integration (8 tests).
- `test_phase7_reporting_engine.py`: Phase 7 9 report types, verification scorecard, HTML/PDF/DOCX/CSV exports (7 tests).
- `test_phase8_disclosure_intelligence.py`: Phase 8 disclosure register, SHA-256 deduplication, approval/rollback (6 tests).
- `test_phase9_production_engineering.py`: Phase 9 readiness probes, path traversal security, online backup/restore (5 tests).
- `test_phase10_final_certification.py`: Phase 10 7 E2E workflows and 6-layer financial truth audit (8 tests).

---

## 6. How to Generate Institutional Research Reports

### Via Terminal Workstation (UI)
1. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.
2. Click on the **Report Studio** or **Research Library** tab.
3. Select the desired report type (e.g. `Comprehensive Eternal vs. Swiggy Report`).
4. Click **Generate Report**.
5. Inspect the preview, verify the automated quality scorecard, and download in **HTML, PDF, DOCX, or CSV**.

### Via REST API
```bash
# Generate Comprehensive Report
curl -X POST "http://127.0.0.1:8000/api/v1/reports/generate" \
     -H "Content-Type: application/json" \
     -d '{"report_type": "COMPREHENSIVE", "period_cutoff": "Q2FY27", "author": "Equity Research Lead"}'

# Download as PDF
curl -O "http://127.0.0.1:8000/api/v1/reports/{report_id}/export/pdf"

# Download as DOCX
curl -O "http://127.0.0.1:8000/api/v1/reports/{report_id}/export/docx"
```

---

## 7. Database Backup and Disaster Recovery

### Create Zero-Downtime Online Backup
```bash
python scripts/backup_db.py
```
Output archive is verified with `PRAGMA integrity_check` and stored at `data/backups/foodiq_backup_YYYYMMDD_HHMMSS.db`.

### Restore Backup with Integrity Validation
```bash
python scripts/restore_db.py --backup data/backups/foodiq_backup_YYYYMMDD_HHMMSS.db --target data/foodiq.db
```

---

## 8. 7 End-to-End Certified Workflows

- **Workflow A — Corporate Financial Research:** Food Delivery EBITDA margin spread attribution (242 bps spread), Level 3 comparability annotation, and primary source citation.
- **Workflow B — Management Credibility:** Multi-category commitment tracking, strict delivery scorecards (Eternal: 83.33%, Swiggy: 75.00%), and unexpired milestone denominator isolation.
- **Workflow C — Quantitative Analysis:** Instamart AOV vs. CM econometric study ($r=0.5531$, detrended $r_\Delta = 0.1399, p=0.72$), confirming that AOV expansion does not synchronously drive margin turnaround.
- **Workflow D — Scenario Modelling:** Instamart break-even AOV solver (₹813.20), 1,000-draw Monte Carlo uncertainty simulations, and persistent SQLite scenario saving.
- **Workflow E — Report Production:** Assembling 26-section comprehensive report, running automated verification scorecards, and compiling HTML/PDF/DOCX/CSV exports.
- **Workflow F — New Disclosure Ingestion:** Registering filings with SHA-256 deduplication, running research impact analysis, and analyst approval/rollback.
- **Workflow G — Disaster Recovery:** Online SQLite backup, integrity verification, and safe target restoration.

---

## 9. Deliverables & Documentation Index

| Phase | Core Deliverable | Technical Documentation |
| :--- | :--- | :--- |
| **Foundation (1 & 1.1)** | `data/foodiq.db` (570 observations) | [`docs/database_schema.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/database_schema.md) |
| **Financial Core (2 & 2.1)**| `reports/phase2_1_reconciliation.csv` | [`docs/financial_analytics_methodology.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/financial_analytics_methodology.md) |
| **Competitive (3 & 3.1)** | `reports/phase3_competitive_findings.json` | [`docs/phase3_competitive_intelligence_methodology.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase3_competitive_intelligence_methodology.md) |
| **Credibility (4)** | `reports/phase4_guidance_scorecard.csv` | [`docs/phase4_management_credibility_methodology.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase4_management_credibility_methodology.md) |
| **Quantitative (5)** | `reports/phase5_statistical_research.json` | [`docs/phase5_quantitative_research_methodology.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase5_quantitative_research_methodology.md) |
| **Workstation (6)** | `frontend/index.html` (10 workspaces) | [`docs/phase6_product_architecture.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase6_product_architecture.md) |
| **Reporting (7)** | `reports/phase7_report_validation.json` | [`docs/phase7_report_generation_methodology.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase7_report_generation_methodology.md) |
| **Disclosures (8)** | `reports/phase8_source_coverage.csv` | [`docs/phase8_ingestion_architecture.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase8_ingestion_architecture.md) |
| **Production (9)** | `reports/phase9_deployment_validation.json`| [`docs/phase9_deployment_guide.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase9_deployment_guide.md) |
| **Certification (10)** | `reports/phase10_final_audit.json` | [`docs/phase10_independent_system_audit.md`](file:///c:/Users/Rut%20Patel/OneDrive/Documents/GitHub/FoodIQ/docs/phase10_independent_system_audit.md) |
