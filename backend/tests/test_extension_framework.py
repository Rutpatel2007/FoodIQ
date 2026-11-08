"""
Test Suite for FoodIQ Extensible Architecture & Plugin Registry
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.analytics.extension_framework import (
    registry,
    CompanyPlugin,
    BusinessSegmentDefinition,
    MetricDefinitionExtension,
    MetricValidationRule,
    AnalyticsModulePlugin
)

client = TestClient(app)


def test_core_companies_registered():
    companies = registry.list_companies()
    comp_ids = [c.company_id for c in companies]
    assert "ETERNAL" in comp_ids
    assert "SWIGGY" in comp_ids
    
    eternal = registry.get_company("ETERNAL")
    assert eternal is not None
    assert len(eternal.supported_segments) >= 4
    seg_ids = [s.segment_id for s in eternal.supported_segments]
    assert "FOOD_DELIVERY" in seg_ids
    assert "QUICK_COMMERCE" in seg_ids


def test_custom_company_registration():
    zepto_plugin = CompanyPlugin(
        company_id="ZEPTO",
        legal_name="KiranaKart Technologies Private Limited",
        short_name="Zepto",
        supported_segments=[
            BusinessSegmentDefinition(
                segment_id="QUICK_COMMERCE",
                display_name="Zepto Quick Commerce",
                description="Dark store fast grocery delivery",
                revenue_model="take_rate_and_delivery_fee",
                primary_kpis=["GOV", "ACTIVE_DARK_STORES"]
            )
        ],
        disclosure_sources=["AUDITED_FINANCIALS", "ROC_FILINGS"]
    )
    registry.register_company(zepto_plugin)
    retrieved = registry.get_company("ZEPTO")
    assert retrieved is not None
    assert retrieved.legal_name == "KiranaKart Technologies Private Limited"


def test_metric_extension_registration():
    custom_metric = MetricDefinitionExtension(
        metric_id="DARK_STORE_SALES_PER_SQFT",
        display_name="Dark Store Sales per Sq Ft",
        definition="Annualized GOV divided by total dark store carpet area",
        unit="INR",
        denominator="SQ_FT",
        derived=True,
        dependencies=["GOV", "TOTAL_DARK_STORE_SQFT"],
        validation_rules=[
            MetricValidationRule(rule_type="non_negative", min_value=0.0, description="Cannot be negative")
        ]
    )
    registry.register_metric(custom_metric)
    retrieved = registry.get_metric("DARK_STORE_SALES_PER_SQFT")
    assert retrieved is not None
    assert retrieved.unit == "INR"
    assert retrieved.derived is True


def test_analytics_module_execution():
    modules = registry.list_modules()
    assert len(modules) >= 1
    mod_ids = [m["module_id"] for m in modules]
    assert "dark_store_efficiency_v1" in mod_ids
    
    mod = registry.get_module("dark_store_efficiency_v1")
    assert mod is not None
    res = mod.execute(session=None, parameters={"days_in_quarter": 90})
    assert res["status"] == "SUCCESS"
    assert "benchmark_daily_runrate_inr" in res


def test_extension_api_endpoints():
    # 1. Info endpoint
    resp = client.get("/api/v1/extensions/info")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_companies"] >= 2
    assert "ETERNAL" in data["companies"]
    assert "SWIGGY" in data["companies"]

    # 2. Companies list
    resp = client.get("/api/v1/extensions/companies")
    assert resp.status_code == 200
    comps = resp.json()
    assert len(comps) >= 2

    # 3. Company by ID
    resp = client.get("/api/v1/extensions/companies/ETERNAL")
    assert resp.status_code == 200
    assert resp.json()["company_id"] == "ETERNAL"

    # 4. Modules list
    resp = client.get("/api/v1/extensions/modules")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # 5. Execute module endpoint
    resp = client.post("/api/v1/extensions/modules/dark_store_efficiency_v1/execute", json={"days_in_quarter": 92})
    assert resp.status_code == 200
    assert resp.json()["status"] == "SUCCESS"


def test_extension_hooks():
    hook_called = []
    def sample_hook(company_id):
        hook_called.append(company_id)
    
    registry.hooks.register_hook("before_ingest", sample_hook)
    registry.hooks.trigger_hook("before_ingest", company_id="ETERNAL")
    assert "ETERNAL" in hook_called
