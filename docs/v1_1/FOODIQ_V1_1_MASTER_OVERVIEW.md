# FoodIQ v1.1 — Master System Overview & Product Architecture
**Document Reference:** DOC-V11-01  
**Classification:** Institutional Research Guide  
**Release Version:** FoodIQ v1.1 (Production Release)  

---

## 1. Product Mission & Purpose

FoodIQ is an institutional-grade corporate financial intelligence platform engineered for equity research analysts, portfolio managers, and forensic accountants covering the Indian listed internet ecosystem—specifically **Eternal Limited (Zomato / Blinkit / Hyperpure)** and **Swiggy Limited**.

Unlike consumer tracking tools or generic financial scrapers, FoodIQ operates as a deterministic, evidence-backed research workstation. Every financial assertion, unit-economic bridge, and econometric elasticity is directly traceable to primary regulatory filings submitted to the National Stock Exchange of India (NSE) and BSE Limited.

---

## 2. Core Architectural Pillars

FoodIQ is structured into six integrated intelligence layers:

```
┌─────────────────────────────────────────────────────────────────┐
│               6. Institutional Frontend Workstation             │
│   (10 Specialized Workspaces: Overview, Econometrics, PDF View) │
├─────────────────────────────────────────────────────────────────┤
│            5. Econometric & Scenario Simulation Lab             │
│     (12 Empirical Studies, Benjamini-Hochberg FDR, Monte Carlo) │
├─────────────────────────────────────────────────────────────────┤
│            4. Management Credibility & Narrative Engine         │
│     (26 Tracked Commitments, Strict & Broad Scoring Models)     │
├─────────────────────────────────────────────────────────────────┤
│            3. Competitive Intelligence & Structural Breaks      │
│     (Spread Dynamics, M&A Adjustments, Take Rate Decompositions)│
├─────────────────────────────────────────────────────────────────┤
│            2. Financial Normalization & Comparability           │
│     (GOV vs NOV Waterfalls, 4-Tier Comparability Enforcement)   │
├─────────────────────────────────────────────────────────────────┤
│            1. Data Lineage & Cryptographic Document Store       │
│     (14 Statutory Filings, 509 Indexed Pages, Coordinate BBoxes)│
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Key Capabilities in Release v1.1

1. **Reconciled Unit Economics:** Full mathematical alignment between variable Contribution Margin and Segment Adjusted EBITDA.
2. **Break-Even Elasticity Engine:** OLS-derived sensitivity modeling predicting exact AOV expansion thresholds required for profitability.
3. **Four-Tier Comparability System:** Programmatic enforcement preventing apples-to-oranges metric comparisons (such as subtracting Net Order Value from Gross Order Value).
4. **False Discovery Rate (FDR) Guardrails:** Benjamini-Hochberg corrections preventing spurious conclusions across multi-hypothesis research.
5. **Interactive Primary Evidence Viewer:** Deep-linking from high-level charts down to exact physical PDF page coordinates and tabular bounding boxes.

---

## 4. Hardware & Runtime Requirements

- **Operating System:** Windows, macOS, or Linux.
- **Python Runtime:** Python 3.10+ (tested on Python 3.11.x).
- **Database Engine:** SQLite 3.35+ with Write-Ahead Logging (WAL) enabled.
- **Backend Framework:** FastAPI / Uvicorn (Asynchronous ASGI).
- **Frontend Stack:** Modern ECMAScript / HTML5 / Tailwind CSS (Zero external node build dependencies; pure browser-native execution).
