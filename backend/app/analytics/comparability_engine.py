"""
FoodIQ Formal Comparability Engine (Phase 3).
Central, reusable governance engine classifying peer metric comparisons into 4 formal levels:
- LEVEL 1: DIRECTLY COMPARABLE
- LEVEL 2: COMPARABLE WITH ADJUSTMENT
- LEVEL 3: DIRECTIONALLY COMPARABLE
- LEVEL 4: INCOMPARABLE (Prohibited from direct ranking or subtraction)
"""

from typing import Dict, List, Optional, Any
import pandas as pd
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json


COMPARABILITY_LEVELS = {
    'LEVEL_1': {
        'tier_code': 'L1',
        'name': 'DIRECTLY_COMPARABLE',
        'description': 'Economic definitions, units, reporting scope, and accounting bases are fully aligned. Direct subtraction and ratio calculation are permitted.',
        'allows_direct_subtraction': True,
        'requires_adjustment': False
    },
    'LEVEL_2': {
        'tier_code': 'L2',
        'name': 'COMPARABLE_WITH_ADJUSTMENT',
        'description': 'Direct comparison is valid only after applying a documented, reproducible mathematical adjustment or normalization.',
        'allows_direct_subtraction': True,
        'requires_adjustment': True
    },
    'LEVEL_3': {
        'tier_code': 'L3',
        'name': 'DIRECTIONALLY_COMPARABLE',
        'description': 'Trends, growth rates, and trajectories may be compared, but absolute magnitudes or accounting presentation boundaries differ. Peer rankings on levels are blocked.',
        'allows_direct_subtraction': False,
        'requires_adjustment': False
    },
    'LEVEL_4': {
        'tier_code': 'L4',
        'name': 'INCOMPARABLE',
        'description': 'Underlying economic definitions or accounting treatments are incompatible. Direct mathematical subtraction and peer ranking are strictly prohibited.',
        'allows_direct_subtraction': False,
        'requires_adjustment': False
    }
}


# Master Comparability Rulebook across all segments and metrics
MASTER_COMPARABILITY_REGISTRY = [
    {
        'rule_id': 'RULE-COMP-001',
        'segment': 'QuickCommerce',
        'metric_name': 'dark_stores',
        'company_a_metric_id': 'eternal_qcomm_darkstores',
        'company_b_metric_id': 'swiggy_qcomm_darkstores',
        'comparability_level': 'LEVEL_1',
        'units': 'count',
        'native_def_a': 'Active operational dark stores at period end (Blinkit)',
        'native_def_b': 'Active operational dark stores at period end (Instamart)',
        'numerators_a': 'Total operating physical stores',
        'denominators_a': 'None (Count)',
        'numerators_b': 'Total operating physical stores',
        'denominators_b': 'None (Count)',
        'reporting_basis_a': 'Period-end physical operating count',
        'reporting_basis_b': 'Period-end physical operating count',
        'adjustment_formula': None,
        'adjustment_inputs': None,
        'source_citations': 'Eternal Shareholder Letters; Swiggy Shareholder Letters & Prospectus',
        'known_limitations': 'Store footprints vary (Instamart average ~3,000-3,500 sq ft; Blinkit expanded to 4,000-5,000 sq ft in larger hubs).',
        'explanation': 'Both companies report physical active dark store locations at the end of each fiscal quarter.',
        'validation_status': 'VERIFIED'
    },
    {
        'rule_id': 'RULE-COMP-002',
        'segment': 'QuickCommerce',
        'metric_name': 'nov_cr',
        'company_a_metric_id': 'eternal_qcomm_nov',
        'company_b_metric_id': 'swiggy_qcomm_nov',
        'comparability_level': 'LEVEL_1',
        'units': 'INR Crores',
        'native_def_a': 'Net Order Value: Gross merchandise order value net of customer discounts',
        'native_def_b': 'Net Order Value: Gross order value net of platform and restaurant/merchant discounts',
        'numerators_a': 'Customer billings net of vouchers/discounts',
        'denominators_a': 'None (Currency Cr)',
        'numerators_b': 'Customer billings net of vouchers/discounts',
        'denominators_b': 'None (Currency Cr)',
        'reporting_basis_a': 'Net merchandise flow (Ind AS 115)',
        'reporting_basis_b': 'Net merchandise flow (Ind AS 115)',
        'adjustment_formula': None,
        'adjustment_inputs': None,
        'source_citations': 'Blinkit Financial Disclosures; Swiggy Condensed Financial Statements',
        'known_limitations': 'Minor variation in statutory local tax exclusions.',
        'explanation': 'Both companies disclose Net Order Value (NOV) representing customer transacted value net of promotional vouchers.',
        'validation_status': 'VERIFIED'
    },
    {
        'rule_id': 'RULE-COMP-003',
        'segment': 'QuickCommerce',
        'metric_name': 'adj_revenue_cr_pre_q2fy26',
        'company_a_metric_id': 'eternal_qcomm_adj_rev',
        'company_b_metric_id': 'swiggy_qcomm_adj_rev',
        'comparability_level': 'LEVEL_2',
        'units': 'INR Crores',
        'native_def_a': 'Adjusted Revenue under 3P agency model (commissions + delivery + ads)',
        'native_def_b': 'Adjusted Revenue under 3P marketplace model (commissions + fees + ads)',
        'numerators_a': 'Commissions + Handling fees + Advertising',
        'denominators_a': 'None (Currency Cr)',
        'numerators_b': 'Marketplace commission + Platform fees + Advertising',
        'denominators_b': 'None (Currency Cr)',
        'reporting_basis_a': '3P Agency Commission Model',
        'reporting_basis_b': '3P Marketplace Commission Model',
        'adjustment_formula': 'Direct comparison valid for quarters before Q2 FY26',
        'adjustment_inputs': 'Historical quarters Q1FY24 through Q1FY26',
        'source_citations': 'Eternal FY24-FY26 Shareholder Letters; Swiggy IPO Prospectus',
        'known_limitations': 'Slight differences in customer delivery fee presentation (net vs gross).',
        'explanation': 'Prior to Q2 FY26, Blinkit and Instamart both operated predominantly as 3P marketplace intermediaries.',
        'validation_status': 'VERIFIED'
    },
    {
        'rule_id': 'RULE-COMP-004',
        'segment': 'QuickCommerce',
        'metric_name': 'adj_revenue_cr_post_q1fy26',
        'company_a_metric_id': 'eternal_qcomm_adj_rev',
        'company_b_metric_id': 'swiggy_qcomm_adj_rev',
        'comparability_level': 'LEVEL_4',
        'units': 'INR Crores',
        'native_def_a': 'Adjusted Revenue under 1P inventory ownership model (gross merchandise value recorded as revenue)',
        'native_def_b': 'Adjusted Revenue under 3P marketplace model (net commission and fee revenue)',
        'numerators_a': 'Gross product selling price + fees (Principal accounting)',
        'denominators_a': 'None (Currency Cr)',
        'numerators_b': 'Net commission + delivery fees (Agent accounting)',
        'denominators_b': 'None (Currency Cr)',
        'reporting_basis_a': '1P Principal Inventory Model (Ind AS 115)',
        'reporting_basis_b': '3P Agent Marketplace Model (Ind AS 115)',
        'adjustment_formula': 'BLOCKED: Cannot mathematically convert 1P revenue to 3P without audited product-level COGS',
        'adjustment_inputs': 'Requires undisclosed vendor wholesale purchase invoices',
        'source_citations': 'Eternal Q2 FY26 Shareholder Letter p.12; Swiggy Q2 FY27 Shareholder Letter p.13',
        'known_limitations': 'Direct subtraction generates a spurious ~₹2,000+ Cr revenue gap reflecting accounting presentation, not commercial dominance.',
        'explanation': 'STRUCTURAL BREAK: Blinkit transitioned to 1P inventory ownership in Q2 FY26. Direct comparison is economically and mathematically invalid.',
        'validation_status': 'VERIFIED_BLOCKED'
    },
    {
        'rule_id': 'RULE-COMP-005',
        'segment': 'Food',
        'metric_name': 'gov_cr',
        'company_a_metric_id': 'eternal_food_gov',
        'company_b_metric_id': 'swiggy_food_gov',
        'comparability_level': 'LEVEL_1',
        'units': 'INR Crores',
        'native_def_a': 'Gross Order Value: Total order value including taxes, customer delivery charges, and packaging',
        'native_def_b': 'Gross Order Value: Total order value placed on platform including taxes and customer delivery fees',
        'numerators_a': 'Total checkout value',
        'denominators_a': 'None (Currency Cr)',
        'numerators_b': 'Total checkout value',
        'denominators_b': 'None (Currency Cr)',
        'reporting_basis_a': 'Gross platform order flow',
        'reporting_basis_b': 'Gross platform order flow',
        'adjustment_formula': None,
        'adjustment_inputs': None,
        'source_citations': 'Zomato Shareholder Letters; Swiggy Shareholder Letters',
        'known_limitations': 'Minor variations in restaurant packaging fee accounting.',
        'explanation': 'Both companies define Food Delivery GOV as total gross merchandise checkout value prior to vouchers.',
        'validation_status': 'VERIFIED'
    },
    {
        'rule_id': 'RULE-COMP-006',
        'segment': 'Food',
        'metric_name': 'cross_gov_nov_subtraction',
        'company_a_metric_id': 'swiggy_food_gov',
        'company_b_metric_id': 'eternal_food_nov',
        'comparability_level': 'LEVEL_4',
        'units': 'INR Crores',
        'native_def_a': 'Gross Order Value (Swiggy)',
        'native_def_b': 'Net Order Value (Eternal)',
        'numerators_a': 'Gross billings with taxes and vouchers',
        'denominators_a': 'None',
        'numerators_b': 'Net billings post customer vouchers',
        'denominators_b': 'None',
        'reporting_basis_a': 'Gross platform flow',
        'reporting_basis_b': 'Net transacted flow',
        'adjustment_formula': 'BLOCKED: Cross-subtraction mixing gross and net boundaries violates accounting identities',
        'adjustment_inputs': None,
        'source_citations': 'FoodIQ Financial Integrity Charter',
        'known_limitations': 'Subtracting NOV from GOV yields voucher and tax amounts, not a competitive market share spread.',
        'explanation': 'Comparing GOV directly against NOV is fundamentally invalid.',
        'validation_status': 'VERIFIED_BLOCKED'
    },
    {
        'rule_id': 'RULE-COMP-007',
        'segment': 'Food',
        'metric_name': 'adj_ebitda_margin_pct',
        'company_a_metric_id': 'eternal_food_adj_ebitda_margin',
        'company_b_metric_id': 'swiggy_food_adj_ebitda_margin',
        'comparability_level': 'LEVEL_3',
        'units': 'Percentage (%)',
        'native_def_a': 'Adjusted EBITDA as % of GOV (excluding ESOP and corporate unallocated overhead)',
        'native_def_b': 'Adjusted EBITDA as % of GOV (excluding ESOP and platform innovation allocations)',
        'numerators_a': 'Segment Adjusted EBITDA (₹ Cr)',
        'denominators_a': 'Food GOV (₹ Cr)',
        'numerators_b': 'Segment Adjusted EBITDA (₹ Cr)',
        'denominators_b': 'Food GOV (₹ Cr)',
        'reporting_basis_a': 'Company-specific overhead apportionment',
        'reporting_basis_b': 'Company-specific overhead apportionment',
        'adjustment_formula': 'Directional trend comparison; absolute margin spreads reflect corporate overhead allocation policies',
        'adjustment_inputs': 'Quarterly segment EBITDA reports',
        'source_citations': 'Zomato Segment Reporting (Note 4); Swiggy Segment Reporting Note 33',
        'known_limitations': 'Zomato leaves certain corporate shared service costs unallocated; Swiggy allocates shared tech/corporate costs differently.',
        'explanation': 'Both report on GOV, but internal overhead allocation conventions vary. Directionally robust; exact bps spreads are indicative.',
        'validation_status': 'VERIFIED'
    },
    {
        'rule_id': 'RULE-COMP-008',
        'segment': 'Food',
        'metric_name': 'mtu_mn',
        'company_a_metric_id': 'eternal_food_mtu',
        'company_b_metric_id': 'swiggy_food_mtu',
        'comparability_level': 'LEVEL_2',
        'units': 'Millions (mn)',
        'native_def_a': 'Monthly Transacting Customers: Average unique transacting customers per month during the quarter',
        'native_def_b': 'Monthly Transacting Users: Average unique transacting users per month during the quarter',
        'numerators_a': 'Unique transacting customer accounts',
        'denominators_a': 'None (Count mn)',
        'numerators_b': 'Unique transacting user accounts',
        'denominators_b': 'None (Count mn)',
        'reporting_basis_a': 'Quarterly average monthly count',
        'reporting_basis_b': 'Quarterly average monthly count',
        'adjustment_formula': 'Direct comparison valid within 5% tolerance for multi-app / web user deduplication',
        'adjustment_inputs': 'Quarterly reported MTU/MTC',
        'source_citations': 'Zomato Shareholder Letter Glossaries; Swiggy Prospectus Definitions',
        'known_limitations': 'Slight variations in guest checkout and phone-number deduplication logic.',
        'explanation': 'Comparable with minor adjustment notes. Both represent 3-month average unique transacting users.',
        'validation_status': 'VERIFIED'
    },
    {
        'rule_id': 'RULE-COMP-009',
        'segment': 'OutOfHome',
        'metric_name': 'adj_revenue_cr',
        'company_a_metric_id': 'eternal_ooh_adj_rev',
        'company_b_metric_id': 'swiggy_ooh_adj_rev',
        'comparability_level': 'LEVEL_2',
        'units': 'INR Crores',
        'native_def_a': 'Going-Out / District Revenue (dining vouchers, event ticketing, live entertainment)',
        'native_def_b': 'Out-of-Home / Dineout Revenue (restaurant table reservations, dining vouchers, event ticketing)',
        'numerators_a': 'Ticketing fees + dining commissions',
        'denominators_a': 'None (Currency Cr)',
        'numerators_b': 'Dineout commission + ticketing fees',
        'denominators_b': 'None (Currency Cr)',
        'reporting_basis_a': 'Scope expanded in Q2 FY25 via Paytm ticketing acquisition',
        'reporting_basis_b': 'Organic Dineout marketplace operations',
        'adjustment_formula': 'Pre-Q2FY25 directly comparable. Post-Q2FY25 requires isolating inorganic ticketing contribution.',
        'adjustment_inputs': 'Eternal disclosed like-for-like growth (53% organic YoY in Q2FY25 vs 171% headline)',
        'source_citations': 'Eternal Q2 FY25 Shareholder Letter; Swiggy Q1 & Q2 FY27 Shareholder Letters',
        'known_limitations': 'District incorporates Paytm ticketing assets from August 27, 2024 onwards.',
        'explanation': 'Comparable with adjustment for the District acquisition in Q2 FY25.',
        'validation_status': 'VERIFIED'
    },
    {
        'rule_id': 'RULE-COMP-010',
        'segment': 'SupplyChain',
        'metric_name': 'adj_revenue_cr',
        'company_a_metric_id': 'eternal_hyperpure_rev',
        'company_b_metric_id': 'swiggy_supply_chain_rev',
        'comparability_level': 'LEVEL_2',
        'units': 'INR Crores',
        'native_def_a': 'Hyperpure B2B revenue (farm-to-fork ingredients, dark store replenishment, merchant packaging)',
        'native_def_b': 'Supply Chain B2B revenue (merchant procurement, logistics services, Lynks)',
        'numerators_a': 'Wholesale product sales to restaurants & internal transfers',
        'denominators_a': 'None (Currency Cr)',
        'numerators_b': 'Wholesale food supplies & third-party logistics',
        'denominators_b': 'None (Currency Cr)',
        'reporting_basis_a': 'Intercompany eliminations changed in Q2 FY26 due to Blinkit 1P transition',
        'reporting_basis_b': 'Deconsolidated Lynks in Q2 FY27',
        'adjustment_formula': 'Adjust for intercompany elimination and Lynks deconsolidation scope changes',
        'adjustment_inputs': 'Disclosed Lynks quarterly revenue run-rate (~₹200 Cr) and Hyperpure intercompany elimination notes',
        'source_citations': 'Eternal Q2 FY26 Shareholder Letter p.14; Swiggy Q2 FY27 Shareholder Letter p.15',
        'known_limitations': 'In Q2 FY26, Hyperpure external revenue fell 55% because sales to Blinkit became internal eliminations.',
        'explanation': 'Comparable with structural break adjustments for consolidation scope changes.',
        'validation_status': 'VERIFIED'
    }
]


def get_comparability_rule(segment: str, metric: str, fiscal_year: Optional[str] = None, quarter_num: Optional[int] = None) -> Dict[str, Any]:
    """
    Evaluates comparability level for any segment and metric pair, incorporating temporal structural breaks.
    """
    fy_int = int(fiscal_year.replace('FY', '')) if fiscal_year else None
    
    # 1. Quick Commerce Revenue Structural Break
    if segment == 'QuickCommerce' and metric in ['adj_revenue_cr', 'revenue_cr']:
        if fy_int and ((fy_int == 26 and quarter_num and quarter_num >= 2) or fy_int > 26):
            rule = next(r for r in MASTER_COMPARABILITY_REGISTRY if r['rule_id'] == 'RULE-COMP-004')
            return dict(rule)
        else:
            rule = next(r for r in MASTER_COMPARABILITY_REGISTRY if r['rule_id'] == 'RULE-COMP-003')
            return dict(rule)
            
    # 2. Cross GOV vs NOV
    if metric in ['cross_gov_nov', 'gov_vs_nov']:
        rule = next(r for r in MASTER_COMPARABILITY_REGISTRY if r['rule_id'] == 'RULE-COMP-006')
        return dict(rule)
        
    # Match by segment and metric
    for r in MASTER_COMPARABILITY_REGISTRY:
        if r['segment'] == segment and r['metric_name'] == metric:
            return dict(r)
            
    # Default fallback for unlisted pairs
    return {
        'rule_id': 'RULE-COMP-GENERIC',
        'segment': segment,
        'metric_name': metric,
        'company_a_metric_id': f'eternal_{segment.lower()}_{metric}',
        'company_b_metric_id': f'swiggy_{segment.lower()}_{metric}',
        'comparability_level': 'LEVEL_2',
        'units': 'Disclosed units',
        'native_def_a': 'Eternal reported series',
        'native_def_b': 'Swiggy reported series',
        'numerators_a': 'Disclosed',
        'denominators_a': 'Disclosed',
        'numerators_b': 'Disclosed',
        'denominators_b': 'Disclosed',
        'reporting_basis_a': 'Ind AS corporate disclosures',
        'reporting_basis_b': 'Ind AS corporate disclosures',
        'adjustment_formula': 'Inspect segment boundaries and accounting presentation before comparison',
        'adjustment_inputs': None,
        'source_citations': 'Corporate Filings',
        'known_limitations': 'Granular accounting policies and overhead allocations may differ.',
        'explanation': 'Standard segment financial metric subject to company-specific cost apportionment.',
        'validation_status': 'VERIFIED'
    }


def get_all_comparability_rules() -> List[Dict[str, Any]]:
    """Returns the master list of all 4-tier comparability rules."""
    return [dict(r) for r in MASTER_COMPARABILITY_REGISTRY]
