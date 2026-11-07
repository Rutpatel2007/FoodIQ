# FoodIQ — REST API Reference Specification

Base URL: `http://localhost:8000/api/v1`

## 1. System Health
- **`GET /health`**
  - **Description:** Verifies database connectivity and API runtime health.
  - **Response:**
    ```json
    {
      "status": "healthy",
      "service": "FoodIQ Competitive Intelligence Engine",
      "version": "1.0.0",
      "database": "connected"
    }
    ```

---

## 2. Companies
- **`GET /companies`**
  - **Description:** Retrieves all covered companies (`ETERNAL`, `SWIGGY`) with ticker symbols and corporate descriptions.
  - **Response:** Array of `CompanyResponse`.

---

## 3. Source Documents
- **`GET /documents`**
  - **Description:** Returns authoritative registered disclosure documents with SHA-256 checksums and page counts.
  - **Query Parameters:**
    - `company_id` (optional): Filter by `ETERNAL` or `SWIGGY`.
    - `fiscal_year` (optional): e.g. `FY26`.
    - `fiscal_quarter` (optional): e.g. `Q1`.
  - **Response:** Array of `DocumentResponse`.

---

## 4. Business Segments
- **`GET /segments`**
  - **Description:** Returns operating and reporting segments.
  - **Query Parameters:**
    - `company_id` (optional): Filter by `ETERNAL` or `SWIGGY`.
  - **Response:** Array of `SegmentResponse`.

---

## 5. Metric Definitions
- **`GET /metrics`**
  - **Description:** Returns metric definitions, units, denominator formulas, and IndAS references.
  - **Query Parameters:**
    - `company_id` (optional): Filter by company.
    - `segment_scope` (optional): Filter by segment.
  - **Response:** Array of `MetricDefinitionResponse`.

---

## 6. Metric Observations & Lineage
- **`GET /observations`**
  - **Description:** Query longitudinal financial observations.
  - **Query Parameters:**
    - `company_id` (optional): `ETERNAL`, `SWIGGY`.
    - `segment_id` (optional): e.g. `SWIGGY_FOOD`.
    - `metric_id` (optional): e.g. `swiggy_gov_cr`.
    - `fiscal_year` (optional): `FY25`, `FY26`, `FY27`.
    - `fiscal_quarter` (optional): `Q1`, `Q2`, `Q3`, `Q4`.
    - `limit` (default: 100, max: 1000).
    - `offset` (default: 0).
  - **Response:** Array of `MetricObservationResponse`.

- **`GET /observations/{observation_id}`**
  - **Description:** Retrieves a single observation by ID.

- **`GET /observations/{observation_id}/lineage`**
  - **Description:** Retrieves full source-to-insight provenance, including physical PDF page citation, file SHA-256 checksum, raw unparsed value, verified value, and associated data quality flags.

---

## 7. Data Quality & Integrity
- **`GET /data-quality/summary`**
  - **Description:** Aggregate counts of quality flags grouped by severity (`CRITICAL`, `HIGH`, `MEDIUM`, `INFO`), issue code, and resolution status.

- **`GET /data-quality/issues`**
  - **Description:** List granular quality issues and historical restatement records.
  - **Query Parameters:**
    - `severity` (optional): `CRITICAL`, `HIGH`, `MEDIUM`, `INFO`.
    - `is_resolved` (optional): boolean.

---

## 8. Financial Comparability Governance
- **`GET /comparability/rules`**
  - **Description:** Returns rules governing metric comparisons.
  - **Query Parameters:**
    - `tier` (optional): `DIRECT`, `ADJUSTED`, `DIRECTIONAL`, `INCOMPARABLE`.

- **`POST /comparability/evaluate`**
  - **Description:** Validates whether two metrics can be compared for a specific quarter, returning restrictions and warnings.
  - **Payload:**
    ```json
    {
      "metric_a": "swiggy_gov_cr",
      "metric_b": "eternal_food_nov",
      "quarter": "Q1FY26"
    }
    ```

---

## 9. Management Guidance & Commitments
- **`GET /guidance`**
  - **Description:** Longitudinal tracker of management forward-looking commitments, target dates, and evaluated outcomes.
  - **Query Parameters:**
    - `company_id` (optional): Filter by company.
    - `guidance_type` (optional): `EXACT_VALUE`, `NUMERICAL_RANGE`, `BREAK_EVEN`, `QUALITATIVE`.
