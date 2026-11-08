# FoodIQ Phase 7 — Institutional Report Generation Methodology

## 1. Principles of Institutional Financial Reporting

FoodIQ's Report Generation Engine is designed to produce audit-grade corporate financial research reports for institutional asset managers, buy-side equity analysts, and corporate strategy teams. It is not an export of dashboard screenshots; rather, it is an analytical synthesizer operating directly on the relational database and analytical engines.

### Core Principles
1. **Zero Hallucination / Zero Imputation:**
   Every fact, ratio, and growth rate in the report is retrieved from audited disclosures or derived via deterministic formulas. Where data is undisclosed, the report acknowledges the reporting omission rather than synthesizing values.
2. **Dynamic Multi-Engine Synthesis:**
   The report engine queries the unit economics core (Phase 2), competitive attribution engine (Phase 3), management credibility engine (Phase 4), econometric research workbench (Phase 5), and scenario lab (Phase 5).
3. **Traceability to Statutory Filings:**
   Every section compiles a traceable citation trail linking every observation to its statutory filing, physical page index, and extraction confidence score.
4. **Epistemic Labeling:**
   The narrative strictly distinguishes `REPORTED_FACT` (directly disclosed), `DERIVED_FACT` (calculated from reported facts), `EMPIRICAL_ESTIMATE` (OLS regression results), `MANAGEMENT_EXPLANATION` (corporate narrative), and `ANALYST_ASSUMPTION` (scenario parameters).

---

## 2. 9 Supported Report Types

| Code | Title | Target Audience | Primary Focus |
| :--- | :--- | :--- | :--- |
| `COMPREHENSIVE` | Comprehensive Eternal vs. Swiggy Report | Institutional Equity Research | Full 26-section comparative analysis of both firms across all dimensions. |
| `COMPANY_SPECIFIC` | Company-Specific Research Report | Fundamental Investors | Deep dive into either Eternal Limited or Swiggy Limited independently. |
| `BUSINESS_SEGMENT` | Business Segment Analysis Report | Industry / Sector Analysts | Specialized analysis of Food Delivery, Quick Commerce, Out-of-Home, or Supply Chain. |
| `QUARTERLY_PERFORMANCE`| Quarterly Performance Trajectory | Earnings Season Review | Focus on latest reported period (Q2 FY27) performance versus prior quarters. |
| `MANAGEMENT_EXECUTION` | Management Execution & Credibility | Governance & Risk Teams | 26 management commitments evaluated against empirical outcomes across 16 categories. |
| `COMPETITIVE_INTELLIGENCE`| Competitive Positioning & Structural Breaks| Strategy & M&A Teams | Gap analysis, 4-tier comparability governance, Blinkit 1P accounting shift. |
| `QUANTITATIVE_RESEARCH`| Quantitative Research & Econometrics | Quantitative Analysts | 12 econometric relationship studies with detrended $\Delta$ correlations and FDR controls. |
| `SCENARIOS_AND_SENSITIVITY`| Scenario Simulation & Sensitivity | Financial Modeling / Planning | Multi-segment forecasting, break-even threshold analysis, 1,000-draw Monte Carlo. |
| `EXECUTIVE_BRIEF` | Executive Investment Research Brief | Senior Leadership / CIOs | High-density brief with core findings, competitive spreads, key risks, and open questions. |

---

## 3. Modular Section Architecture

Reports are constructed from modular, independently verifiable sections:
- `cover`: Formal title, author attribution, statutory disclaimers.
- `metadata`: Reporting coverage, database version, filing archive metrics.
- `exec_summary`: Core narrative synthesizing scale, network throughput, and profitability trends.
- `key_findings`: Top 6 verified research findings with derived calculations and source pages.
- `historical_financials`: Standardized cross-company financial tables (GOV, NOV, AOV, CM, EBITDA).
- `competitive_comparison`: Margin spread attribution (e.g. Food Delivery 242 bps spread) and comparability governance.
- `management_credibility`: Strict and broad guidance delivery scorecards, pending commitment isolation.
- `quantitative_research`: Econometric studies, Pearson $r$, Spearman $\rho$, $p$-values, first-difference detrending ($r_\Delta$), and Benjamini-Hochberg FDR results ($q=0.05$).
- `scenario_analysis`: Quick commerce break-even analysis (Instamart break-even AOV ₹813.20) and Monte Carlo confidence intervals.
- `citations_register`: Compilation of all statutory citations with resolution verification status.

---

## 4. Multi-Format Compilation Pipeline

1. **HTML:** Generates clean, standalone HTML documents styled with A4 print media stylesheets, responsive typography, and tabular formatting.
2. **PDF:** Compiled via headless Google Chrome (`--headless=new --print-to-pdf`), ensuring exact visual fidelity, page margins, and vector chart rendering without native C compiler dependencies.
3. **DOCX:** Generates valid, editable OpenXML (.docx) archives directly using Python's standard `zipfile` and structured WordprocessingML XML payloads.
4. **CSV:** Extracts all embedded structured data tables into comma-separated tabular files for Excel modeling.
