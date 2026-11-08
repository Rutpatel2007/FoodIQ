# FoodIQ Phase 6 — Workstation API Integration Guide

## 1. API Architecture

The FoodIQ Research Workstation interacts seamlessly with the backend FastAPI service via standard RESTful JSON interfaces. All endpoints follow predictable URL structures, provide structured error envelopes, and support high-throughput, low-latency analytical queries.

Base URL: `http://localhost:8000/api/v1`

---

## 2. API Endpoint Matrix

| Domain | Method & Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| **System & Health** | `GET /health` | None | Returns backend status, DB connection, and version. |
| **Documents** | `GET /documents` | `company_id`, `fiscal_year`, `fiscal_quarter` | Lists all indexed statutory filings and letters. |
| **Analytics Core** | `GET /analytics/head-to-head` | `metric_names` | Returns comparative latest-quarter KPIs for both companies. |
| **Analytics Core** | `GET /analytics/time-series` | `company_id`, `segment_code`, `metric_name` | Retrieves ordered historical quarterly observations. |
| **Competitive Engine** | `GET /competitive/gaps` | `segment` | Calculates segment-level competitive gap records. |
| **Competitive Engine** | `GET /competitive/comparability` | `segment` | Retrieves 4-tier comparability governance rules. |
| **Competitive Engine** | `GET /competitive/findings` | `finding_id` | Returns evidence-backed research findings. |
| **Competitive Engine** | `GET /competitive/findings/{id}` | Path: `id` | Returns a specific research finding by unique ID. |
| **Competitive Engine** | `GET /competitive/events` | `company`, `segment` | Documented corporate structural breaks and M&A events. |
| **Competitive Engine** | `GET /competitive/structural-breaks` | `topic` (`blinkit_1p`, `m_and_a_divestment`) | Deep 4-series accounting reconciliation of breaks. |
| **Credibility Engine** | `GET /credibility/scorecard` | `company_id` | Computes strict and broad guidance delivery scorecards. |
| **Credibility Engine** | `GET /credibility/commitments` | `company_id`, `status` | Repository of 26 management commitments. |
| **Credibility Engine** | `GET /credibility/narratives` | `company_id` | Narrative verification matrix separating causality from correlation. |
| **Credibility Engine** | `GET /credibility/initiatives` | `company_id` | Status of strategic initiatives (Bolt, District, etc.). |
| **Quantitative Engine**| `GET /quantitative/studies` | `study_id` | 12 econometric studies with Pearson, Spearman, CIs, and FDR. |
| **Quantitative Engine**| `GET /quantitative/diagnostics` | `company_id`, `segment_code` | Growth, acceleration, and volatility diagnostics. |
| **Quantitative Engine**| `GET /quantitative/research-questions`| None | Answers to the 8 core institutional research questions. |
| **Scenario Lab** | `GET /scenarios/presets` | None | Retrieves BASE, BULL, and BEAR configuration presets. |
| **Scenario Lab** | `POST /scenarios/simulate` | JSON payload | Executes multi-segment simulation and sensitivity matrix. |
| **Scenario Lab** | `GET /scenarios/list` | None | Lists saved custom scenarios from SQLite. |
| **Scenario Lab** | `POST /scenarios/save` | JSON payload | Persists a custom scenario to the SQLite database. |

---

## 3. Client-Side API Handling Best Practices

1. **Sanitized Response Handling:**
   All endpoints utilize `backend.app.analytics.repository.sanitize_for_json` to clean NaN, Inf, and non-standard float representations into standard JSON `null` values.
2. **Asynchronous Fetching:**
   The client workstation utilizes native `async/await` and `Promise.allSettled` to fetch multiple analytical datasets concurrently without UI blocking.
3. **Error Resilience:**
   API errors surface localized, non-destructive error badges rather than crashing the workstation.
4. **Offline Capability:**
   Because all assets and data are served locally from FastAPI, the workstation functions completely offline without internet connectivity.
