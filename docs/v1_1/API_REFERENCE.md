# FoodIQ v1.1 — REST API Reference Manual
**Document Reference:** DOC-V11-09  
**Classification:** Developer API Documentation  

---

## 1. API Conventions

- **Base URL:** `http://127.0.0.1:8000/api`
- **Format:** All requests and responses are UTF-8 JSON.
- **Authentication:** Local workstation development mode requires no token; production instances support bearer token header `Authorization: Bearer <TOKEN>`.
- **Interactive OpenAPI Docs:** Available at `/docs` (Swagger UI) and `/redoc`.

---

## 2. Key Endpoint Reference

### 2.1 Metrics & Time Series
- `GET /api/metrics/definitions`: List all 85 canonical metric definitions.
- `GET /api/metrics/timeseries`: Query historical quarterly metric values.
  - Parameters: `company_id`, `metric_id`, `start_period`, `end_period`.
- `GET /api/metrics/breakdown`: Detailed segment-level margin breakdown.

### 2.2 Econometrics & Studies
- `GET /api/econometrics/studies`: Retrieve all 12 relationship studies with FDR adjustment.
- `POST /api/econometrics/regression`: Run custom OLS regression with detrending options.

### 2.3 Management Credibility
- `GET /api/credibility/scorecards`: Retrieve strict and broad credibility scores.
- `GET /api/credibility/commitments`: Query tracked commitments with evidence citations.

### 2.4 Document Evidence
- `GET /api/documents/list`: Catalog of all 14 statutory PDF filings.
- `GET /api/documents/pdf/{document_id}`: Stream primary PDF document.
- `GET /api/documents/coordinates/{observation_id}`: Bounding box coordinates for visual highlight.
