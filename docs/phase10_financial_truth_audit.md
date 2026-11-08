# FoodIQ Phase 10 — Financial Truth Audit

## 1. Multi-Layer Truth Reconciliation Methodology

To certify research integrity, core financial and operational metrics across both companies were audited across all six operating layers:
1. **Primary Source Disclosure:** Statutory quarterly shareholder letter or SEBI filing.
2. **Database Record:** Observation in `metric_observations` in `data/foodiq.db`.
3. **Analytical Engine Output:** Derived computation in `backend/app/analytics/*`.
4. **FastAPI REST Endpoint:** Serialized JSON response via `/api/v1/*`.
5. **UI Workstation Display:** Rendered DOM card or table cell in `frontend/`.
6. **Generated Institutional Report:** Formatted research table in generated report.

---

## 2. Six-Layer Audit Reconciliation Matrix

### Trace 1: Blinkit Store Network Throughput (Q2 FY27)
- **Layer 1 (Source):** Eternal Q2 FY27 Shareholder Letter, Page 13 (NOV: ₹20,940 Cr) and Page 7 (2,700 dark stores guided).
- **Layer 2 (Database):** `eternal_qcomm_nov` = 20,940, `eternal_qcomm_darkstores` = 2,700.
- **Layer 3 (Analytics):** $(20,940 \times 10^7) / (2,700 \times 91.25) = ₹849,923.90 \text{ / store-day}$.
- **Layer 4 (API):** `/api/v1/competitive/findings/FINDING-001` returns `849,924` and `+22.0%`.
- **Layer 5 (UI):** Rendered in Quick Commerce Core workspace and finding card.
- **Layer 6 (Report):** Comprehensive Report `key_findings` table displays ₹849,924 / store-day.
- **Verdict:** **RECONCILED (100% Truth Match)**

### Trace 2: Swiggy Instamart AOV & Break-Even Basket (Q2 FY27)
- **Layer 1 (Source):** Swiggy Q2 FY27 Shareholder Letter, Page 7 (AOV: ₹708.00; CM: -1.0%).
- **Layer 2 (Database):** `swiggy_aov_inr` = 708, `swiggy_contribution_margin_pct` = -1.0.
- **Layer 3 (Analytics):** Break-Even AOV = $708.00 + (1.0 \times 100 / 0.9506) = \mathbf{₹813.20}$.
- **Layer 4 (API):** `/api/v1/scenarios/breakeven` returns `breakeven_aov_inr: 813.20`.
- **Layer 5 (UI):** Rendered in Scenario Lab Cockpit Break-Even Card.
- **Layer 6 (Report):** Comprehensive Report `scenario_analysis` states required AOV ₹813.20.
- **Verdict:** **RECONCILED (100% Truth Match)**

### Trace 3: Food Delivery Adjusted EBITDA Margin Spread (Q2 FY27)
- **Layer 1 (Source):** Eternal Q2 FY27 filing (3.86% EBITDA margin); Swiggy Q2 FY27 filing (1.44% EBITDA margin).
- **Layer 2 (Database):** Reconciled across `eternal_food_adj_ebitda` and `swiggy_adjusted_ebitda_margin_pct`.
- **Layer 3 (Analytics):** Spread = $3.86\% - 1.44\% = \mathbf{242\text{ bps}}$.
- **Layer 4 (API):** `/api/v1/competitive/findings/FINDING-006` returns 242 bps spread.
- **Layer 5 (UI):** Rendered in Competitive Intelligence workspace with Level 3 Comparability pill.
- **Layer 6 (Report):** Comprehensive Report `competitive_comparison` annotates 242 bps spread.
- **Verdict:** **RECONCILED (100% Truth Match)**
