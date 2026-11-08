# FOODIQ — FUTURE DEVELOPMENT ROADMAP
## Strategic Backlog & Engineering Roadmap for Platform Evolution

**Platform:** FoodIQ Corporate Intelligence Engine  
**Status:** Post-Maturity Baseline (v1.0.0 Production Certified)  
**Planning Horizon:** 2026 – 2028  
**Governance Standard:** Institutional Research Quality & Extensible Architecture  

---

## 1. Roadmap Architecture & Prioritization Principles

Following the successful completion and certification of the original FoodIQ vision (Phases 1 through 10), future engineering work is structured into five distinct categories. In accordance with project governance rules, future items represent an actionable, prioritized development backlog and are not triggered automatically without explicit mandate.

```
       ┌────────────────────────────────────────────────────────┐
       │             FOODIQ STRATEGIC ROADMAP                    │
       └──────────────────────────┬─────────────────────────────┘
                                  │
    ┌──────────────┬──────────────┼──────────────┬──────────────┐
    ▼              ▼              ▼              ▼              ▼
Category A     Category B     Category C     Category D     Category E
Research       Company &      Data           Research       Product
Capability     Industry       Intelligence   Productivity   Engineering
Expansion      Expansion      & Ingestion    & UI Tools     & Scale
```

---

## 2. Category A — Research Capability Expansion

| Item ID | Capability | Description | Target Horizon | Priority | Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RES-001** | High-Frequency Proxy Integration | Incorporate monthly high-frequency proxy indicators (e.g., credit card spend trends, app traffic rank) as leading indicators for quarterly GOV outturns. | Q1 2027 | High | Medium |
| **RES-002** | Non-Linear Elasticity Models | Extend the linear OLS elasticity model ($\beta = 0.9506$ bps/₹) into piecewise spline regressions capturing diminishing returns to AOV expansion. | Q2 2027 | Medium | High |
| **RES-003** | Dark Store Cohort Decay Analysis | Model mature vs. ramping dark store margin curves with vintage vintage cohorting to estimate cluster-level steady-state EBITDA. | Q2 2027 | High | Medium |
| **RES-004** | Advertising Monetization Matrix | Decompose FMCG advertising revenue into search placement, sponsored carousels, and co-marketing brand funding. | Q3 2027 | Medium | Medium |
| **RES-005** | Delivery Fleet Economics | Model gig-worker payout structures, fuel inflation pass-through, and batching efficiency ratios per delivery partner. | Q4 2027 | Low | High |

---

## 3. Category B — Company & Industry Expansion

| Item ID | Capability | Description | Target Horizon | Priority | Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP-001** | Zepto Quick Commerce Onboarding | Integrate KiranaKart Technologies (Zepto) disclosures (MCA/ROC MGT-7 filings) via `CompanyPlugin` interface to create a triopoly intelligence engine. | Q1 2027 | High | Medium |
| **EXP-002** | Logistical Ecosystem Integration | Benchmark against 3P logistics operators (Delhivery, Shadowfax) handling food and parcel deliveries to isolate cost advantages. | Q2 2027 | Medium | High |
| **EXP-003** | Indian Consumer-Tech Benchmarking | Expand platform coverage to Info Edge (Naukri/99acres), Nykaa (FSN E-Commerce), and Honasa Consumer (Mamaearth) for cross-industry tech valuation metrics. | Q3 2027 | Low | High |
| **EXP-004** | Zomato District Standalone Reporting | Restructure segmental tables to accommodate Eternal's planned carve-out and standalone reporting of the District (Out-of-Home/Live Events) business. | Q1 2027 | High | Low |

---

## 4. Category C — Data Intelligence & Automated Ingestion

| Item ID | Capability | Description | Target Horizon | Priority | Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DAT-001** | BSE / NSE Automated Feed Scraper | Implement automated polling of BSE India and NSE corporate announcement RSS/APIs to trigger new filing downloads within 60 seconds of publication. | Q1 2027 | High | Medium |
| **DAT-002** | Multi-Modal Visual Table OCR | Integrate vision-language model table parsers to extract complex multi-header operational grids from non-standard investor presentations. | Q2 2027 | High | High |
| **DAT-003** | Earnings Call Audio Transcription | Transcribe raw earnings call MP3 recordings directly to text, synchronizing executive vocal tone with transcript sentiment analysis. | Q3 2027 | Medium | High |
| **DAT-004** | Automated Revision Audit Engine | Programmatically diff restated historical numbers in new annual reports against originally published quarterly figures. | Q2 2027 | High | Medium |

---

## 5. Category D — Research Productivity & Analyst Workflows

| Item ID | Capability | Description | Target Horizon | Priority | Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PROD-001** | Analyst Annotation Drawer | Allow research analysts to highlight text directly in the embedded document PDF viewer and attach persistent research notes to metric cells. | Q1 2027 | High | Medium |
| **PROD-002** | Report Version Diffing | Visual side-by-side comparison of successive quarterly reports to highlight changed management tones, modified guidance, or revised estimates. | Q2 2027 | Medium | Medium |
| **PROD-003** | Interactive Scenario Workspace Share | Generate unique shareable URLs encoding specific scenario slider assumptions for institutional investment committee presentations. | Q1 2027 | Medium | Low |
| **PROD-004** | Natural Language Query Engine | Enable natural-language search over the 509-page disclosure corpus (e.g., "Find all mentions of Blinkit delivery partner incentives in FY26"). | Q2 2027 | Medium | High |

---

## 6. Category E — Production Engineering & Enterprise Scale

| Item ID | Capability | Description | Target Horizon | Priority | Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ENG-001** | Role-Based Access Control (RBAC) | Implement OAuth2 / JWT authentication with role partitioning (Analyst, Senior Associate, Portfolio Manager, Administrator). | Q2 2027 | High | Medium |
| **ENG-002** | Asynchronous Worker Task Queue | Offload heavy 10,000-draw Monte Carlo simulations and multi-page PDF generation to Celery / Redis background worker pools. | Q3 2027 | High | Medium |
| **ENG-003** | Automated Cloud Database Replication | Implement continuous WAL streaming and automated daily encrypted offsite snapshot sync to AWS S3 or Google Cloud Storage. | Q1 2027 | High | Low |
| **ENG-004** | Multi-Region Container Orchestration | Kubernetes Helm charts for deploying multi-region read replicas of the FoodIQ API gateway with sub-10ms global latency. | Q4 2027 | Low | High |

---

## 7. Execution Governance

All roadmap initiatives must adhere to the core tenets established in the FoodIQ Charter:
1. Zero synthetic or fabricated data.
2. 100% citation provenance to primary disclosures.
3. Separation of empirical observation from conditional analytical scenario assumptions.
4. Continuous automated test coverage >90%.
