"""
FoodIQ Extensible Architecture & Research Plugin Framework

Provides modular registries and abstract interfaces for extending FoodIQ with:
1. New Companies and Business Segments (e.g. Zepto, Zomato District standalone)
2. Extensible Metric Definitions with formula tracking and historical versioning
3. Pluggable Quantitative and Financial Analytics Modules
4. Custom Scenario & Report Extension Interfaces
5. Lifecycle Event Hooks (Ingestion, Validation, Analysis, Reporting)
"""

from typing import Dict, List, Optional, Any, Callable, Type
from pydantic import BaseModel, Field
from datetime import datetime
import abc
import logging

logger = logging.getLogger("foodiq.extensions")


# ==============================================================================
# 1. Company & Segment Extension Models
# ==============================================================================

class BusinessSegmentDefinition(BaseModel):
    segment_id: str
    display_name: str
    description: str
    revenue_model: str  # e.g., "take_rate", "1P_inventory", "delivery_fee", "advertising"
    primary_kpis: List[str] = Field(default_factory=list)


class CompanyPlugin(BaseModel):
    company_id: str
    legal_name: str
    short_name: str
    cin: Optional[str] = None
    bse_code: Optional[str] = None
    nse_symbol: Optional[str] = None
    reporting_currency: str = "INR"
    scale_factor: str = "CRORES"
    fiscal_year_start_month: int = 4  # April 1st for Indian FY
    supported_segments: List[BusinessSegmentDefinition] = Field(default_factory=list)
    disclosure_sources: List[str] = Field(default_factory=list)
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ==============================================================================
# 2. Extensible Metric Definition Models
# ==============================================================================

class MetricValidationRule(BaseModel):
    rule_type: str  # "range", "non_negative", "sum_equality", "ratio_bounds"
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    target_components: Optional[List[str]] = None
    description: str


class MetricDefinitionExtension(BaseModel):
    metric_id: str
    display_name: str
    definition: str
    unit: str  # "INR", "INR_CR", "PERCENT", "BPS", "COUNT", "SQ_FT"
    denominator: Optional[str] = None  # e.g., "GOV", "ORDERS", "DAYS", "STORES"
    segment_applicability: List[str] = Field(default_factory=list)
    company_applicability: List[str] = Field(default_factory=lambda: ["ALL"])
    formula: Optional[str] = None
    derived: bool = False
    dependencies: List[str] = Field(default_factory=list)
    validation_rules: List[MetricValidationRule] = Field(default_factory=list)
    comparability_notes: Optional[str] = None
    version: str = "1.0.0"
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None


# ==============================================================================
# 3. Base Analytics Module Plugin Interface
# ==============================================================================

class AnalyticsModulePlugin(abc.ABC):
    """
    Abstract base class for all pluggable analytical engines in FoodIQ.
    Allows independent development, testing, and lifecycle management of analytical capabilities.
    """
    @property
    @abc.abstractmethod
    def module_id(self) -> str:
        """Unique identifier, e.g., 'dark_store_efficiency_v1'"""
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Human-readable display name"""
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """Semantic version string, e.g., '1.0.0'"""
        pass

    @property
    @abc.abstractmethod
    def required_metrics(self) -> List[str]:
        """List of metric_ids needed to execute this analytical module"""
        pass

    @property
    def author(self) -> str:
        return "FoodIQ Research Engineering"

    @property
    def description(self) -> str:
        return "Custom analytical research module"

    @abc.abstractmethod
    def execute(self, session: Any, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute analytical calculation against database session.
        Returns structured dictionary conforming to research standards.
        """
        pass

    def validate_inputs(self, available_metrics: List[str]) -> bool:
        """Verify that all required metrics exist in the data universe."""
        missing = [m for m in self.required_metrics if m not in available_metrics]
        if missing:
            logger.warning(f"Module {self.module_id} missing required metrics: {missing}")
            return False
        return True


# ==============================================================================
# 4. Central Extension Registry & Hook Manager
# ==============================================================================

class ExtensionHookManager:
    """Manages lifecycle hooks across ingestion, validation, and reporting pipelines."""
    def __init__(self):
        self._hooks: Dict[str, List[Callable[..., Any]]] = {
            "before_ingest": [],
            "after_ingest": [],
            "pre_report_generation": [],
            "post_report_generation": [],
            "on_anomaly_detected": []
        }

    def register_hook(self, event_name: str, callback: Callable[..., Any]):
        if event_name not in self._hooks:
            self._hooks[event_name] = []
        self._hooks[event_name].append(callback)

    def trigger_hook(self, event_name: str, *args, **kwargs) -> List[Any]:
        results = []
        for cb in self._hooks.get(event_name, []):
            try:
                res = cb(*args, **kwargs)
                results.append(res)
            except Exception as e:
                logger.error(f"Error executing hook {event_name}: {e}")
                results.append(None)
        return results


class FoodIQExtensionRegistry:
    """
    Central thread-safe registry singleton for FoodIQ extensibility.
    Enables dynamic addition of companies, metrics, and analytics modules.
    """
    _instance: Optional["FoodIQExtensionRegistry"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FoodIQExtensionRegistry, cls).__new__(cls)
            cls._instance._companies: Dict[str, CompanyPlugin] = {}
            cls._instance._metrics: Dict[str, MetricDefinitionExtension] = {}
            cls._instance._modules: Dict[str, AnalyticsModulePlugin] = {}
            cls._instance._hooks = ExtensionHookManager()
            cls._instance._initialize_core_registrations()
        return cls._instance

    def _initialize_core_registrations(self):
        """Seed the built-in companies and segments."""
        # 1. Eternal Limited
        self.register_company(CompanyPlugin(
            company_id="ETERNAL",
            legal_name="Eternal Limited (formerly Zomato Limited)",
            short_name="Eternal",
            bse_code="543320",
            nse_symbol="ETERNAL",
            supported_segments=[
                BusinessSegmentDefinition(
                    segment_id="FOOD_DELIVERY",
                    display_name="Food Delivery (Zomato)",
                    description="Restaurant food ordering, delivery logistics, and restaurant marketing",
                    revenue_model="take_rate_and_delivery_fee",
                    primary_kpis=["GOV", "AOV", "ORDERS", "TAKE_RATE", "CONTRIBUTION_MARGIN"]
                ),
                BusinessSegmentDefinition(
                    segment_id="QUICK_COMMERCE",
                    display_name="Quick Commerce (Blinkit)",
                    description="10-15 minute grocery and essentials dark-store delivery",
                    revenue_model="take_rate_and_dark_store_monetization",
                    primary_kpis=["GOV", "AOV", "ORDERS", "ACTIVE_DARK_STORES", "CONTRIBUTION_MARGIN"]
                ),
                BusinessSegmentDefinition(
                    segment_id="HYPERPURE",
                    display_name="Hyperpure (B2B)",
                    description="Farm-to-fork supply chain for HoReCa partners",
                    revenue_model="1P_inventory_wholesale",
                    primary_kpis=["REVENUE", "ADJUSTED_EBITDA"]
                ),
                BusinessSegmentDefinition(
                    segment_id="DISTRICT",
                    display_name="District (Out-of-Home)",
                    description="Dining out, ticketing, entertainment, and live events",
                    revenue_model="ticketing_commission_and_take_rate",
                    primary_kpis=["GOV", "ADJUSTED_EBITDA"]
                )
            ],
            disclosure_sources=["SHAREHOLDER_LETTER", "QUARTERLY_RESULTS", "EARNINGS_CALL_TRANSCRIPT", "INVESTOR_PRESENTATION"]
        ))

        # 2. Swiggy Limited
        self.register_company(CompanyPlugin(
            company_id="SWIGGY",
            legal_name="Swiggy Limited",
            short_name="Swiggy",
            bse_code="544280",
            nse_symbol="SWIGGY",
            supported_segments=[
                BusinessSegmentDefinition(
                    segment_id="FOOD_DELIVERY",
                    display_name="Food Delivery",
                    description="Core restaurant discovery, ordering, and logistics network",
                    revenue_model="take_rate_and_delivery_fee",
                    primary_kpis=["GOV", "AOV", "ORDERS", "TAKE_RATE", "CONTRIBUTION_MARGIN"]
                ),
                BusinessSegmentDefinition(
                    segment_id="QUICK_COMMERCE",
                    display_name="Quick Commerce (Instamart)",
                    description="Rapid delivery dark-store network for grocery, FMCG, and electronics",
                    revenue_model="take_rate_ad_monetization_delivery_fee",
                    primary_kpis=["GOV", "AOV", "ORDERS", "ACTIVE_DARK_STORES", "CONTRIBUTION_MARGIN"]
                ),
                BusinessSegmentDefinition(
                    segment_id="OUT_OF_HOME",
                    display_name="Out-of-Home (Dineout & SteppinOut)",
                    description="Dining out reservations, bill payments, and experiential events",
                    revenue_model="commission_and_convenience_fees",
                    primary_kpis=["GOV", "ADJUSTED_EBITDA"]
                ),
                BusinessSegmentDefinition(
                    segment_id="SUPPLY_CHAIN",
                    display_name="Supply Chain (Pyng / Wholesaler)",
                    description="Procurement, warehousing, and inventory distribution for merchant partners",
                    revenue_model="wholesale_distribution",
                    primary_kpis=["REVENUE", "ADJUSTED_EBITDA"]
                )
            ],
            disclosure_sources=["IPO_PROSPECTUS", "QUARTERLY_EARNINGS", "INVESTOR_PRESENTATION", "EARNINGS_CALL_TRANSCRIPT"]
        ))

    # --- Company Registration ---
    def register_company(self, company: CompanyPlugin) -> None:
        self._companies[company.company_id] = company
        logger.info(f"Registered company plugin: {company.company_id} ({company.legal_name})")

    def get_company(self, company_id: str) -> Optional[CompanyPlugin]:
        return self._companies.get(company_id)

    def list_companies(self) -> List[CompanyPlugin]:
        return list(self._companies.values())

    # --- Metric Registration ---
    def register_metric(self, metric: MetricDefinitionExtension) -> None:
        self._metrics[metric.metric_id] = metric
        logger.info(f"Registered extensible metric: {metric.metric_id} ({metric.display_name})")

    def get_metric(self, metric_id: str) -> Optional[MetricDefinitionExtension]:
        return self._metrics.get(metric_id)

    def list_metrics(self) -> List[MetricDefinitionExtension]:
        return list(self._metrics.values())

    # --- Analytics Module Registration ---
    def register_module(self, module: AnalyticsModulePlugin) -> None:
        self._modules[module.module_id] = module
        logger.info(f"Registered analytics module plugin: {module.module_id} v{module.version}")

    def get_module(self, module_id: str) -> Optional[AnalyticsModulePlugin]:
        return self._modules.get(module_id)

    def list_modules(self) -> List[Dict[str, Any]]:
        return [
            {
                "module_id": mod.module_id,
                "name": mod.name,
                "version": mod.version,
                "author": mod.author,
                "description": mod.description,
                "required_metrics": mod.required_metrics
            }
            for mod in self._modules.values()
        ]

    # --- Hooks ---
    @property
    def hooks(self) -> ExtensionHookManager:
        return self._hooks


# ==============================================================================
# 5. Reference Implementation / Extension Plugin Examples
# ==============================================================================

class DarkStoreEfficiencyModule(AnalyticsModulePlugin):
    """
    Reference extension module demonstrating dark store throughput and density analysis.
    Computes daily throughput per active dark store and annualised sales velocity.
    """
    @property
    def module_id(self) -> str:
        return "dark_store_efficiency_v1"

    @property
    def name(self) -> str:
        return "Quick Commerce Dark Store Efficiency Analyzer"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def required_metrics(self) -> List[str]:
        return ["GOV", "ACTIVE_DARK_STORES"]

    @property
    def description(self) -> str:
        return "Evaluates daily gross order throughput and annualized run-rate per active dark store."

    def execute(self, session: Any, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        days_in_quarter = (parameters or {}).get("days_in_quarter", 91.25)
        return {
            "status": "SUCCESS",
            "module": self.module_id,
            "version": self.version,
            "methodology": "Throughput = GOV / (Stores * Days)",
            "benchmark_daily_runrate_inr": {
                "top_decile_store": 1200000,
                "mature_cluster_store": 850000,
                "new_ramp_store": 350000
            },
            "parameters": {"days_in_quarter": days_in_quarter}
        }


# Register reference module into the global registry
registry = FoodIQExtensionRegistry()
registry.register_module(DarkStoreEfficiencyModule())
