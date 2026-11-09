# FoodIQ — REST API Reference Manual

The FoodIQ API is built on FastAPI and serves structured financial, operational, and research intelligence.

- **Base URL:** `http://127.0.0.1:8000/api/v1`
- **Interactive Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc Documentation:** `http://127.0.0.1:8000/redoc`

---

## 1. System Health

### `GET /api/v1/health`
Checks backend and database connectivity.
- **Response:**
  ```json
  {
    "status": "healthy",
    "service": "FoodIQ Competitive Intelligence Engine",
    "version": "3.1.0",
    "database": "connected"
  }
  ```

---

## 2. Companies & Segments

### `GET /api/v1/companies`
Lists all tracked companies.

### `GET /api/v1/segments`
Lists operating segments across Food Delivery, Quick Commerce, Hyperpure, and Dining.

---

## 3. Financial Metrics & Observations

### `GET /api/v1/metrics`
Returns canonical metric definitions, units, and comparability tiers.

### `GET /api/v1/observations`
Query historical quarterly observations.
- **Query Parameters:**
  - `company_id` (optional): `Eternal` | `Swiggy`
  - `metric_id` (optional): Canonical metric name
  - `period_id` (optional): E.g., `Q2FY27`
- **Response Structure:** Array of observation records with period, value, and source document citations.

### `GET /api/v1/observations/{observation_id}/lineage`
Returns the exact PDF document ID, page number, and vector bounding box `(x0, y0, x1, y1)` for coordinate highlighting.

---

## 4. Analytics & Margin Bridges

### `GET /api/v1/analytics/company-overview`
Overview KPI dashboard data for a given company and quarter.
- **Query Parameters:** `company` (`Eternal` | `Swiggy`), `quarter` (`Q2FY27`)

### `GET /api/v1/analytics/executive-kpis`
Macro duopoly summary for executive cards.

### `GET /api/v1/analytics/margin-bridge`
5-step segment margin breakdown from Take Rate to Adjusted EBITDA.

### `GET /api/v1/analytics/unit-economics`
Store-level unit economics, order-level contribution, and throughput models.

---

## 5. Quantitative Research & Studies

### `GET /api/v1/quantitative/relationships`
Returns empirical studies with sample size, Pearson correlation, p-values, and Benjamini-Hochberg FDR significance status.

### `GET /api/v1/quantitative/relationships/{study_id}`
Detailed regression diagnostics, scatter data points, and detrended growth correlations.

---

## 6. Management Credibility

### `GET /api/v1/credibility/scorecard`
Strict and broad credibility percentages for Eternal and Swiggy.

### `GET /api/v1/credibility/commitments`
List of 26 management commitments with status (`DELIVERED`, `PARTIAL`, `MISSED`, `IN_PROGRESS`).

---

## 7. Scenarios & Simulations

### `POST /api/v1/scenarios/sensitivity`
Deterministic sensitivity modeling for AOV expansion and contribution margin response.

### `POST /api/v1/scenarios/monte-carlo`
Runs 10,000 parameter iterations across store expansion and margin trajectories.

---

## 8. Research Reports

### `GET /api/v1/reports/types`
List available institutional report templates.

### `POST /api/v1/reports/generate`
Generates an institutional research brief with verified citations.

### `GET /api/v1/reports/{report_id}/export/{format}`
Exports report to `html`, `pdf`, `docx`, or `csv`.
