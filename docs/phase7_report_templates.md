# FoodIQ Phase 7 — Report Templates Specification

This document details the structure, default section blueprints, and analytical scopes for all nine institutional research report types.

---

## 1. Standard 26-Section Comprehensive Report Blueprint (`COMPREHENSIVE`)

The flagship output of FoodIQ is the Comprehensive Eternal vs. Swiggy Institutional Research Report:

1. **Cover Page (`cover`):** Document title, platform branding, confidentiality classification, statutory SEBI disclaimer.
2. **Metadata & Parameters (`metadata`):** Reporting horizon, database version, filing catalog metrics.
3. **Executive Summary (`exec_summary`):** High-level synthesis of competitive scale, store productivity, and margin trajectories.
4. **Key Research Findings (`key_findings`):** Top 6 findings from Phase 3 with derived calculations and source pages.
5. **Company Overview (`company_overview`):** Corporate history, operating entities, business models.
6. **Segment Structure (`segment_structure`):** Segment definitions across Food, QC, Out-of-Home, and B2B.
7. **Historical Financial Performance (`historical_financials`):** Multi-quarter standardized financial tables.
8. **Growth Decomposition (`growth_decomposition`):** Price vs Volume waterfall breakdowns.
9. **Revenue & Monetisation (`revenue_monetisation`):** Take rate trends and merchant commission structures.
10. **Unit Economics (`unit_economics`):** Order-level economics, contribution margins, delivery costs.
11. **Profitability & EBITDA Analysis (`profitability_ebitda`):** Segment Adjusted EBITDA and corporate overheads.
12. **Competitive Comparison (`competitive_comparison`):** Margin spread attribution and duopoly dynamics.
13. **Quick Commerce Network Productivity (`qc_network_productivity`):** Store count, throughput (INR/store-day), density.
14. **Food Delivery Economics (`food_delivery_economics`):** AOV expansion, restaurant commissions, delivery subsidies.
15. **Structural Accounting Events (`structural_breaks`):** Blinkit 1P inventory shift, District ticketing, Lynks divestment.
16. **Management Guidance & Credibility (`management_credibility`):** Guidance delivery scorecards across 16 categories.
17. **Strategic Initiative Progress (`strategic_initiatives`):** Status of Swiggy Bolt, Eternal District, Hyperpure expansion.
18. **Statistical Research Findings (`quantitative_research`):** 12 econometric studies, detrended $\Delta$ correlations, BH FDR.
19. **Scenario Modelling (`scenario_analysis`):** Multi-segment forecasts, Instamart break-even AOV, Monte Carlo distributions.
20. **Risks & Uncertainties (`risks_uncertainties`):** Competitive intensity, regulatory risks, quick commerce capex burden.
21. **Analyst Interpretation (`analyst_interpretation`):** Independent synthesis of strategic moats and unit economic durability.
22. **Unanswered Research Questions (`unanswered_questions`):** Open empirical questions requiring future disclosures.
23. **Methodology (`methodology`):** Overview of data ingestion, comparability rules, and econometric testing.
24. **Data Coverage & Limitations (`limitations`):** Granularity gaps, disclosure omissions, non-imputation rules.
25. **Source Register & Citations (`citations_register`):** Master table of all primary filings and page citations.
26. **Appendix Calculations (`appendix_calculations`):** Mathematical formulas, derivation steps, statistical test tables.

---

## 2. Specialized Report Templates

### Template B: Company-Specific Report (`COMPANY_SPECIFIC`)
- **Focus:** Single-company deep dive (Eternal Limited or Swiggy Limited).
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `company_overview`, `historical_financials`, `unit_economics`, `management_credibility`, `scenario_analysis`, `risks_uncertainties`, `citations_register`.

### Template C: Business Segment Report (`BUSINESS_SEGMENT`)
- **Focus:** Single-segment cross-company comparison (e.g. Quick Commerce: Blinkit vs. Instamart).
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `segment_structure`, `historical_financials`, `unit_economics`, `competitive_comparison`, `quantitative_research`, `citations_register`.

### Template D: Quarterly Performance Report (`QUARTERLY_PERFORMANCE`)
- **Focus:** Review of the latest quarterly disclosures (Q2 FY27) versus prior quarters.
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `historical_financials`, `growth_decomposition`, `profitability_ebitda`, `citations_register`.

### Template E: Management Execution Report (`MANAGEMENT_EXECUTION`)
- **Focus:** Corporate governance, commitment fulfillment, and narrative consistency.
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `management_credibility`, `strategic_initiatives`, `analyst_interpretation`, `citations_register`.

### Template F: Competitive Intelligence Report (`COMPETITIVE_INTELLIGENCE`)
- **Focus:** Duopoly market share, 4-tier comparability governance, structural break accounting.
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `competitive_comparison`, `structural_breaks`, `qc_network_productivity`, `food_delivery_economics`, `citations_register`.

### Template G: Quantitative Research Report (`QUANTITATIVE_RESEARCH`)
- **Focus:** Statistical relationships, hypothesis testing, detrended correlations, and FDR controls.
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `quantitative_research`, `risks_uncertainties`, `methodology`, `limitations`, `citations_register`.

### Template H: Scenario & Sensitivity Report (`SCENARIOS_AND_SENSITIVITY`)
- **Focus:** Conditional financial forecasts, break-even thresholds, 2D sensitivity grids, and Monte Carlo risk simulations.
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `scenario_analysis`, `risks_uncertainties`, `appendix_calculations`, `citations_register`.

### Template I: Executive Investment Brief (`EXECUTIVE_BRIEF`)
- **Focus:** Concise, decision-oriented brief for investment committees and senior leadership.
- **Default Sections:** `cover`, `metadata`, `exec_summary`, `key_findings`, `competitive_comparison`, `management_credibility`, `risks_uncertainties`, `unanswered_questions`, `citations_register`.
