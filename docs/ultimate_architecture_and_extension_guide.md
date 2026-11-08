# FOODIQ — ARCHITECTURE & EXTENSION GUIDE
## Comprehensive Guide to the Modular Architecture, Data Model, and Extension Framework

**Platform:** FoodIQ Corporate Intelligence Engine  
**Version:** 1.0.0 Production Release  
**Audience:** Quantitative Developers, Financial Data Engineers, and System Architects  
**Date:** November 8, 2026  

---

## 1. System Architecture Overview

FoodIQ is structured as a decoupled, reproducible, and extensible financial intelligence platform. It rejects monolithic coupling by separating raw document extraction, structured data storage, analytical decomposition, econometric simulation, and interactive presentation.

```
                      ┌─────────────────────────────────────────┐
                      │        Primary Corporate Disclosures    │
                      │  (Shareholder Letters, IPO Prospectus)  │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │        Ingestion & OCR Pipeline         │
                      │   - PDF Text & Table Extractor          │
                      │   - Page-Level Bounding Box Coordinates │
                      │   - SHA-256 Deduplication & Anomaly Scan│
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │        Relational Data Warehouse        │
                      │   - 21 SQLite Relational Tables         │
                      │   - Immutable Source Lineage & Provenance│
                      │   - Strict NULL vs. 0.0 Semantic Guard   │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │        Analytics & Econometric Core     │
                      │   - Financial Normalization (GOV/Take)  │
                      │   - Duopoly Gap & Structural Breaks     │
                      │   - Management Credibility Tracker      │
                      │   - Statistical Workbench & FDR Control │
                      │   - Scenario Lab & Monte Carlo Risk     │
                      └────────────┬───────────────┬────────────┘
                                   │               │
                 ┌─────────────────┴─┐           ┌─┴─────────────────┐
                 ▼                   ▼           ▼                   ▼
      ┌────────────────────┐ ┌───────────────┐ ┌───────────────────┐
      │  FastAPI REST API  │ │ Report Studio │ │ Extension Registry│
      │  (15 Endpoints)    │ │ (HTML/PDF/DOC)│ │ (Plugins/Metrics) │
      └──────────┬─────────┘ └───────────────┘ └───────────────────┘
                 │
                 ▼
      ┌─────────────────────────────────────────┐
      │   Institutional Research Workstation    │
      │   (Zero-Build HTML5 / Vector Canvas)    │
      └─────────────────────────────────────────┘
```

---

## 2. Core Relational Data Model (21 Tables)

The storage layer is built on SQLite with strict foreign key constraints (`PRAGMA foreign_keys = ON`), providing ACID guarantees without the operational overhead of external database servers.

1. **Entity & Filing Hierarchy:**
   - `companies`: Primary entity master (Company ID, legal name, ticker, CIN).
   - `business_segments`: Segmental taxonomy (e.g. `FOOD_DELIVERY`, `QUICK_COMMERCE`, `HYPERPURE`).
   - `source_documents`: Master filing register (SHA-256 checksums, filing date, period).
   - `document_pages`: Page-level index with OCR extracted text and bounding-box coordinates.

2. **Metrics & Provenance:**
   - `metric_definitions`: Master taxonomy of financial, operating, and unit economic indicators.
   - `metric_observations`: Quarterly empirical values, period identifiers, and strict NULL governance.
   - `observation_lineage`: Exact page, paragraph, and table coordinate audit trails for every number.
   - `data_quality_flags`: Automated variance warnings, restatement tracking, and sanity alerts.

3. **Competitive & Governance Structures:**
   - `comparability_rules`: Accounting reconciliation directives (e.g., Blinkit 1P to 3P transition).
   - `structural_breaks`: Chronology of corporate actions, acquisitions, and regulatory shocks.
   - `management_commitments`: Forward-looking guidance targets and realization status.
   - `narrative_verifications`: Management tone shifts and strategic commitment audits.

4. **Research, Simulation & Reporting:**
   - `saved_scenarios`: Stored parameter assumptions, elasticity calibrations, and run outputs.
   - `generated_reports`: Persistent institutional report artifacts with embedded citation proofs.
   - `disclosure_register`: Staging and lifecycle tracking for new corporate disclosures.

---

## 3. Extensible Architecture Framework

FoodIQ provides a dedicated extension subsystem in `backend/app/analytics/extension_framework.py` that enables developers to add new companies, metrics, and analytical engines without altering core code.

### 3.1 Adding a New Company Plugin (e.g., Zepto)
To register a new corporate entity in the FoodIQ duopoly or expand into a triopoly:

```python
from backend.app.analytics.extension_framework import registry, CompanyPlugin, BusinessSegmentDefinition

zepto_plugin = CompanyPlugin(
    company_id="ZEPTO",
    legal_name="KiranaKart Technologies Private Limited",
    short_name="Zepto",
    cin="U72900MH2020PTC349584",
    reporting_currency="INR",
    scale_factor="CRORES",
    supported_segments=[
        BusinessSegmentDefinition(
            segment_id="QUICK_COMMERCE",
            display_name="Zepto Quick Commerce",
            description="10-minute grocery delivery via high-density dark store network",
            revenue_model="take_rate_and_delivery_fee",
            primary_kpis=["GOV", "AOV", "ACTIVE_DARK_STORES", "CONTRIBUTION_MARGIN"]
        ),
        BusinessSegmentDefinition(
            segment_id="ZEPTO_POST",
            display_name="Zepto Post (Cafe / Add-on)",
            description="High-margin impulse snacks and hot beverages",
            revenue_model="food_margin",
            primary_kpis=["AOV", "ATTACH_RATE"]
        )
    ],
    disclosure_sources=["AUDITED_FINANCIALS", "ROC_MGT7_FILINGS", "MCA_STATEMENTS"]
)

# Register into the global singleton
registry.register_company(zepto_plugin)
```

### 3.2 Defining an Extensible Financial Metric
New derived or disclosed metrics can be defined dynamically with formulas, validation bounds, and comparability constraints:

```python
from backend.app.analytics.extension_framework import (
    registry,
    MetricDefinitionExtension,
    MetricValidationRule
)

dark_store_capex_metric = MetricDefinitionExtension(
    metric_id="DARK_STORE_CAPEX_PER_SQFT",
    display_name="Dark Store Fit-Out Capex per Sq Ft",
    definition="Racks, chilling infrastructure, and leasehold fit-out investment divided by carpet area",
    unit="INR",
    denominator="SQ_FT",
    segment_applicability=["QUICK_COMMERCE"],
    company_applicability=["ALL"],
    derived=True,
    formula="TOTAL_STORE_CAPEX / TOTAL_CARPET_AREA_SQFT",
    dependencies=["TOTAL_STORE_CAPEX", "TOTAL_CARPET_AREA_SQFT"],
    validation_rules=[
        MetricValidationRule(
            rule_type="range",
            min_value=500.0,
            max_value=3500.0,
            description="Fit-out capex must fall within typical Indian warehousing ranges (₹500 - ₹3,500/sqft)"
        )
    ],
    version="1.0.0"
)

registry.register_metric(dark_store_capex_metric)
```

### 3.3 Authoring a Pluggable Analytics Module
Custom econometric or operational research modules inherit from `AnalyticsModulePlugin`:

```python
from backend.app.analytics.extension_framework import AnalyticsModulePlugin, registry
from typing import Dict, Any, List, Optional

class AdvertisingMonetizationModule(AnalyticsModulePlugin):
    @property
    def module_id(self) -> str:
        return "ad_monetization_deepdive_v1"

    @property
    def name(self) -> str:
        return "Quick Commerce Advertising Monetization Analyzer"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def required_metrics(self) -> List[str]:
        return ["ADVERTISING_REVENUE", "GOV"]

    @property
    def description(self) -> str:
        return "Calculates FMCG brand advertising take-rate as % of GOV and incremental margin contribution."

    def execute(self, session: Any, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Execution logic against analytical dataframe or database session
        return {
            "status": "SUCCESS",
            "module_id": self.module_id,
            "version": self.version,
            "average_ad_take_rate_bps": 280.0,
            "top_monetized_categories": ["Beauty & Personal Care", "Packaged Snacks", "Beverages"],
            "margin_flowthrough_pct": 85.0
        }

# Register module into ecosystem
registry.register_module(AdvertisingMonetizationModule())
```

### 3.4 Hooking into System Lifecycle Events
FoodIQ allows registering interceptors and callback hooks before or after data events:

```python
# Register an alert hook triggered whenever a data anomaly is flagged
def on_data_anomaly_alert(company_id, metric_id, variance_pct):
    print(f"ANOMALY ALERT: {company_id} {metric_id} deviated by {variance_pct}%")

registry.hooks.register_hook("on_anomaly_detected", on_data_anomaly_alert)
```

---

## 4. Extension API Endpoints

The extension framework exposes a full REST interface:
- `GET /api/v1/extensions/info`: Summary of registered plugins, metrics, and modules.
- `GET /api/v1/extensions/companies`: List all supported company plugins.
- `POST /api/v1/extensions/companies`: Dynamically register a new company.
- `GET /api/v1/extensions/metrics`: List extensible metric definitions and validation bounds.
- `POST /api/v1/extensions/metrics`: Register a new metric definition.
- `GET /api/v1/extensions/modules`: List active analytical modules.
- `POST /api/v1/extensions/modules/{module_id}/execute`: Execute an analytics plugin.

---

## 5. Architectural Invariants & Best Practices

1. **Never Bypass Provenance:** Every new observation must link to a valid `document_id` and page reference.
2. **Never Fabricate Data:** If a metric is not disclosed for a given quarter, store `NULL`, not `0.0`.
3. **Isolate Segment Elasticity:** Never apply Quick Commerce elasticity models to Food Delivery or Out-of-Home.
4. **Isolate Pending Guidance:** Never score unexpired forward commitments as misses in credibility scorecards.
