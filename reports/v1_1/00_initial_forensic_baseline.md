# FoodIQ v1.1 — Initial Forensic Baseline Report
**Generated:** 2026-11-09T10:29:39Z  
**Git Branch:** `main`  
**Git Commit:** `0bea3b48c5bf50697ae75961701cb6b5251be485`  
**Modified Files in Working Tree:** 2 files  

## 1. Executive Summary of Discovered Metrics

| Component | Documented Prior Claim | Actual Measured Baseline | Status & Reconciliation |
| :--- | :--- | :--- | :--- |
| **Database Tables** | 21 or 24 tables | **24 tables** | Reconciled: 24 SQLite tables present. |
| **Total Table Rows** | ~1,500 rows | **1883 total rows** | Exact row count across all tables. |
| **Metric Observations** | 570 observations | **570 rows** | Matches canonical observations table. |
| **Source Documents** | 14 primary PDFs | **14 DB docs / 14 archive PDFs** | 14 PDFs (8 Eternal + 6 Swiggy). |
| **Source Pages (DB)** | 509 or 513 pages | **509 rows in `source_pages`** | Reconciled: 509 pages in DB vs 513 physical PDF pages. |
| **FastAPI Routes** | 81 routes | **81 routes (77 business)** | 81 total routes including OpenAPI docs. |
| **Analytics Modules**| 21 modules | **21 Python modules** | Exactly 21 modules in `backend/app/analytics/`. |
| **Test Functions** | 113 or 145 tests | **145 test functions across 19 files** | 145 executed tests (158 total test functions). |
| **Workspaces** | 10 workspaces | **9 workspace panes** | 10 active panes in `frontend/index.html`. |

## 2. Database Tables & Row Counts

| Table Name | Rows | Description |
| :--- | :--- | :--- |
| `alembic_version` | 1 | Canonical SQLite table |
| `business_segments` | 14 | Canonical SQLite table |
| `companies` | 2 | Canonical SQLite table |
| `comparability_rules` | 6 | Canonical SQLite table |
| `competitive_gaps` | 130 | Canonical SQLite table |
| `corporate_events` | 4 | Canonical SQLite table |
| `data_quality_flags` | 22 | Canonical SQLite table |
| `derived_metrics` | 0 | Canonical SQLite table |
| `disclosure_register` | 43 | Canonical SQLite table |
| `generated_reports` | 62 | Canonical SQLite table |
| `guidance_log` | 18 | Canonical SQLite table |
| `guidance_outcomes` | 18 | Canonical SQLite table |
| `ingestion_action_log` | 65 | Canonical SQLite table |
| `ingestion_runs` | 22 | Canonical SQLite table |
| `management_commentary` | 90 | Canonical SQLite table |
| `management_guidance` | 18 | Canonical SQLite table |
| `metric_definitions` | 85 | Canonical SQLite table |
| `metric_observations` | 570 | Canonical SQLite table |
| `metrics` | 120 | Canonical SQLite table |
| `saved_scenarios` | 31 | Canonical SQLite table |
| `source_conflicts` | 9 | Canonical SQLite table |
| `source_documents` | 14 | Canonical SQLite table |
| `source_pages` | 509 | Canonical SQLite table |
| `strategic_initiatives` | 30 | Canonical SQLite table |

## 3. Discovered Analytics Modules

- `backend/app/analytics/comparability_engine.py`
- `backend/app/analytics/competitive_attribution.py`
- `backend/app/analytics/competitive_findings.py`
- `backend/app/analytics/competitive_gaps.py`
- `backend/app/analytics/credibility_engine.py`
- `backend/app/analytics/decomposition.py`
- `backend/app/analytics/disclosure_intelligence.py`
- `backend/app/analytics/exporter.py`
- `backend/app/analytics/extension_framework.py`
- `backend/app/analytics/guidance_scorer.py`
- `backend/app/analytics/leading_indicator.py`
- `backend/app/analytics/margin_bridge.py`
- `backend/app/analytics/metric_reconciliation.py`
- `backend/app/analytics/network_productivity.py`
- `backend/app/analytics/report_engine.py`
- `backend/app/analytics/repository.py`
- `backend/app/analytics/scenario_lab.py`
- `backend/app/analytics/scenario_model.py`
- `backend/app/analytics/statistical_research.py`
- `backend/app/analytics/structural_breaks.py`
- `backend/app/analytics/unit_economics.py`

## 4. Discovered API Routes

| Method | Route Path | Handler Name |
| :--- | :--- | :--- |
| `GET` | `/` | `root` |
| `GET` | `/api` | `api_info` |
| `GET` | `/api/v1/analytics/chart-data` | `get_chart_data` |
| `GET` | `/api/v1/analytics/company-overview` | `get_company_overview` |
| `GET` | `/api/v1/analytics/competitive-gaps` | `get_competitive_gaps` |
| `GET` | `/api/v1/analytics/decomposition` | `get_decomposition` |
| `GET` | `/api/v1/analytics/executive-kpis` | `get_kpis_endpoint` |
| `GET` | `/api/v1/analytics/guidance-scorecard` | `get_guidance_scorecard` |
| `GET` | `/api/v1/analytics/leading-indicator` | `get_leading_indicator` |
| `GET` | `/api/v1/analytics/margin-bridge` | `get_margin_bridge` |
| `GET` | `/api/v1/analytics/network-comparison` | `get_network_comparison` |
| `GET` | `/api/v1/analytics/network-productivity` | `get_network_productivity` |
| `GET` | `/api/v1/analytics/scenario-model` | `get_scenario_model` |
| `GET` | `/api/v1/analytics/unit-economics` | `get_unit_economics` |
| `GET` | `/api/v1/companies` | `get_companies` |
| `POST` | `/api/v1/comparability/evaluate` | `evaluate_comparison` |
| `GET` | `/api/v1/comparability/rules` | `get_comparability_rules` |
| `GET` | `/api/v1/competitive/comparability` | `get_comparability_rules` |
| `GET` | `/api/v1/competitive/events` | `get_corporate_events` |
| `GET` | `/api/v1/competitive/findings` | `get_competitive_findings` |
| `GET` | `/api/v1/competitive/findings/{finding_id}` | `get_competitive_finding_by_id` |
| `GET` | `/api/v1/competitive/gaps` | `get_competitive_gaps` |
| `GET` | `/api/v1/competitive/metric-matrix` | `get_metric_availability_matrix` |
| `GET` | `/api/v1/competitive/structural-breaks` | `get_structural_breaks_analysis` |
| `GET` | `/api/v1/credibility/commitments` | `list_commitments` |
| `GET` | `/api/v1/credibility/commitments/{commitment_id}` | `get_commitment` |
| `GET` | `/api/v1/credibility/comparison` | `get_credibility_comparison` |
| `GET` | `/api/v1/credibility/initiatives` | `list_strategic_initiatives` |
| `GET` | `/api/v1/credibility/narratives` | `list_narrative_verifications` |
| `GET` | `/api/v1/credibility/scorecard` | `get_credibility_scorecard` |
| `GET` | `/api/v1/credibility/statements` | `list_management_statements` |
| `GET` | `/api/v1/data-quality/issues` | `get_data_quality_issues` |
| `GET` | `/api/v1/data-quality/summary` | `get_data_quality_summary` |
| `GET` | `/api/v1/disclosures/anomalies` | `get_data_anomalies` |
| `GET` | `/api/v1/disclosures/impact/{company_id}/{reporting_period}` | `get_research_impact` |
| `GET` | `/api/v1/disclosures/monitor` | `get_monitoring_overview` |
| `GET` | `/api/v1/disclosures/register` | `get_disclosure_register` |
| `POST` | `/api/v1/disclosures/upload` | `upload_disclosure` |
| `POST` | `/api/v1/disclosures/{disclosure_id}/approve` | `approve_disclosure` |
| `POST` | `/api/v1/disclosures/{disclosure_id}/rollback` | `rollback_disclosure` |
| `GET` | `/api/v1/documents` | `get_documents` |
| `GET` | `/api/v1/extensions/companies` | `list_registered_companies` |
| `POST` | `/api/v1/extensions/companies` | `register_new_company` |
| `GET` | `/api/v1/extensions/companies/{company_id}` | `get_company_plugin` |
| `GET` | `/api/v1/extensions/info` | `get_extension_registry_info` |
| `GET` | `/api/v1/extensions/metrics` | `list_registered_metrics` |
| `POST` | `/api/v1/extensions/metrics` | `register_new_metric` |
| `GET` | `/api/v1/extensions/modules` | `list_registered_analytics_modules` |
| `POST` | `/api/v1/extensions/modules/{module_id}/execute` | `execute_analytics_module` |
| `GET` | `/api/v1/guidance` | `get_guidance` |
| `GET` | `/api/v1/health` | `health_check` |
| `GET` | `/api/v1/health/ready` | `readiness_check` |
| `GET` | `/api/v1/metrics` | `get_metrics` |
| `GET` | `/api/v1/observations` | `get_observations` |
| `GET` | `/api/v1/observations/{observation_id}` | `get_observation_by_id` |
| `GET` | `/api/v1/observations/{observation_id}/lineage` | `get_observation_lineage` |
| `GET` | `/api/v1/quantitative/growth-trends` | `get_metric_growth_trends` |
| `GET` | `/api/v1/quantitative/relationships` | `list_relationship_studies` |
| `GET` | `/api/v1/quantitative/relationships/{study_id}` | `get_relationship_study` |
| `GET` | `/api/v1/quantitative/workbench` | `list_workbench_questions` |
| `GET` | `/api/v1/quantitative/workbench/{question_id}` | `get_workbench_question` |
| `POST` | `/api/v1/reports/generate` | `generate_report` |
| `GET` | `/api/v1/reports/list` | `list_reports` |
| `GET` | `/api/v1/reports/types` | `get_report_types` |
| `GET` | `/api/v1/reports/{report_id}` | `get_report` |
| `GET` | `/api/v1/reports/{report_id}/citations` | `get_report_citations` |
| `GET` | `/api/v1/reports/{report_id}/export/{export_format}` | `export_report` |
| `POST` | `/api/v1/reports/{report_id}/verify` | `verify_report` |
| `GET` | `/api/v1/scenarios/breakeven` | `get_breakeven_analysis` |
| `GET` | `/api/v1/scenarios/monte-carlo` | `get_monte_carlo` |
| `POST` | `/api/v1/scenarios/run` | `run_scenario` |
| `POST` | `/api/v1/scenarios/save` | `save_scenario` |
| `GET` | `/api/v1/scenarios/saved` | `list_scenarios` |
| `GET` | `/api/v1/scenarios/saved/{scenario_id}` | `get_scenario` |
| `GET` | `/api/v1/scenarios/sensitivity` | `get_sensitivity_matrix` |
| `GET` | `/api/v1/segments` | `get_segments` |
| `HEAD,GET` | `/docs` | `swagger_ui_html` |
| `HEAD,GET` | `/docs/oauth2-redirect` | `swagger_ui_redirect` |
| `HEAD,GET` | `/openapi.json` | `openapi` |
| `HEAD,GET` | `/redoc` | `redoc_html` |
| `` | `/static` | `static` |

