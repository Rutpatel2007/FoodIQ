# FOODIQ — Institutional User Manual & Research Workflows
**Document Reference:** `FOODIQ-MANUAL-USER-2026-11`  
**System Target:** FoodIQ Research Workstation (`http://localhost:8000`)  
**Audience:** Equity Research Analysts, Financial Associates, Portfolio Managers, Data Auditors

---

## 1. Quick Start & Application Launch

### 1.1 Installation
```bash
# Clone the repository
git clone https://github.com/rutpatel/FoodIQ.git
cd FoodIQ

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Starting the Platform
```bash
# Windows quick launcher:
run_foodiq.bat

# Or direct CLI command:
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Open your browser to: **`http://localhost:8000`**  
Open OpenAPI Swagger Documentation to: **`http://localhost:8000/docs`**

---

## 2. Navigating the 10 Analytical Workspaces

The top navigation bar provides one-click access across all 10 core workspaces (on mobile devices, use the `#mobile-workspace-select` dropdown):

```
[Overview] [Company] [Financials] [Competitive] [Credibility] [Quantitative] [Scenarios] [Library] [Sources] [Governance]
```

### 2.1 Workspace 1: Executive Overview
- **Executive KPI Deck:** 6 dynamic cards displaying Eternal Food GOV, Swiggy Food GOV, Blinkit NOV, Instamart GOV, Food EBITDA Spread, and Guidance Delivery.
- **Dual-Axis Order Flow Chart:** Visualizes 10 quarters of GOV/NOV (left axis) and Dark Store counts (right axis) with interactive hover tooltips and the Q2 FY26 Ind AS 115 transition marker.
- **8 Empirical Findings Summary:** High-signal summaries of verified research discoveries with one-click page coordinate inspection.

### 2.2 Workspace 2: Company Analysis
- Switch between **Eternal Limited** and **Swiggy Limited** via sub-navigation pills.
- Displays segment-level order flows, reported revenues, and strictly distinguished **Contribution Margin (% and ₹ Cr)** vs. **Segment Adjusted EBITDA (% and ₹ Cr)**.
- Reconciles Instamart's -1.0% CM (-₹92.3 Cr) vs. -9.7% EBITDA (-₹895.0 Cr) and Blinkit's ₹8.50 lakh/day blended network throughput.

### 2.3 Workspace 3: Financial Performance
- **Waterfall Growth Decomposition:** Explores volume vs. basket size vs. interaction effects with zero residual.
- **Sequential Contribution Margin Bridges:** Explores quarterly changes broken down by AOV leverage, delivery cost efficiency, and advertising mix.
- **Unit Economics Breakdown:** Per-order unit economics across food delivery and quick commerce.

### 2.4 Workspace 4: Competitive Intelligence
- **Duopoly Gap Analysis:** Spreads across Food Delivery EBITDA, Quick Commerce dark store density, and take rates.
- **Structural Break Register:** Catalog of accounting and perimeter shifts (Paytm acquisition, Blinkit 1P shift, Lynks divestment).

### 2.5 Workspace 5: Management Credibility
- **26 Tracked Commitments:** Historical guidance statements categorized as `MET_EXCEEDED`, `MET_IN_LINE`, `MISSED`, or `PENDING`.
- Isolates unexpired multi-year IPO commitments from the scoring denominator.

### 2.6 Workspace 6: Quantitative Research Engine
- **10 Econometric Studies:** Correlation, regression, and detrending outputs.
- **Benjamini-Hochberg FDR Gating:** Highlights which relationships withstand multiple-testing adjustments at $\alpha = 0.05$.

### 2.7 Workspace 7: Scenario & Sensitivity Lab
- Interactive sliders for AOV growth, dark store expansion, and take rate expansion.
- **Break-Even Solver:** Calculates the exact AOV required for Instamart contribution neutrality (₹813.20).
- **2-Variable Sensitivity Grid:** Stress-tests margins across AOV and dark store counts.
- **Monte Carlo Simulator:** Runs 1,000 bounded draws to generate probability distributions of quarterly profitability.

### 2.8 Workspace 8: Research Library
- Lists all saved scenarios with author names, timestamps, and parameters.
- Reopen any scenario to review its underlying assumptions.

### 2.9 Workspace 9: Data & Disclosures
- Complete catalog of 14 primary statutory documents (509 pages).
- Inspect physical PDF page numbers, SHA-256 checksums, and OCR extraction coordinates.

### 2.10 Workspace 10: Comparability Governance
- Four-tier comparability rules matrix.
- Direct links to OpenAPI Swagger documentation and system health status.

---

## 3. Five End-to-End Research Workflows

### Workflow A: Food Delivery Duopoly Benchmark
1. Navigate to **Competitive Intelligence** (`tab-competitive`) $\rightarrow$ Click **Gaps & Spreads**.
2. Compare Eternal Food GOV (₹10,769 Cr) with Swiggy Food GOV (₹10,054 Cr).
3. Verify that Swiggy's Food EBITDA margin expanded by +260 bps from 0.8% in Q1 FY25 to 3.40% in Q2 FY27, narrowing the gap against Eternal (5.82%) to 242 bps.

### Workflow B: Quick Commerce Store Productivity & Unit Economics
1. Navigate to **Company Analysis** (`tab-company`) $\rightarrow$ Select **Eternal**.
2. Observe Blinkit Q2 FY27 NOV (₹20,940 Cr) across 2,700 stores. Note the blended network throughput of ₹849,924 / store-day.
3. Switch to **Swiggy** $\rightarrow$ Observe Instamart Q2 FY27 GOV (₹9,230 Cr) across 1,240 exit stores.
4. Verify that Instamart's contribution loss is -₹92.3 Cr (-1.0% CM), while its segment Adjusted EBITDA loss is -₹895.0 Cr (-9.7% of GOV).

### Workflow C: Management Credibility Assessment
1. Navigate to **Management Credibility** (`tab-credibility`).
2. Review the scorecard: Eternal has delivered 83.33% of its guidance commitments (Tier: HIGH); Swiggy has delivered 75.00% strict (Tier: MEDIUM-HIGH).
3. Inspect Swiggy commitment `CMT-SWIGGY-004` (IPO dark store expansion) and verify that 11 unexpired commitments are properly tagged as `PENDING`.

### Workflow D: Quantitative Hypothesis Testing & Detrending
1. Navigate to **Quantitative Research** (`tab-quantitative`).
2. Inspect Study `STUDY-002` (Swiggy Instamart AOV vs. Contribution Margin).
3. Note the contrast: in raw levels, $r = 0.5531$ ($p = 0.0972$); upon first-difference detrending, $r_\Delta = 0.1399$ ($p = 0.7200$).
4. Conclude that quarterly basket size fluctuations do not synchronously explain margin improvements.

### Workflow E: Scenario Stress-Testing & Report Generation
1. Navigate to **Scenario Lab** (`tab-scenarios`).
2. Click **Run Scenario Simulation** with base parameters.
3. Inspect the resulting 4-quarter trajectory and observe the AOV break-even threshold (₹813.20).
4. Save the scenario with title *"Instamart Breakeven Path"* and open it in the **Research Library**.
5. Trigger report compilation via `POST /api/v1/reports/generate` to produce a fully cited PDF and DOCX dossier.
