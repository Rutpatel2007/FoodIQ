"""
FoodIQ Structural Break & Corporate Event Engine (Phase 3).
Formally registers, quantifies, and annotates corporate structural business changes:
1. Blinkit 1P Inventory Model Transition (Q2 FY26)
2. Eternal District / Ticketing Acquisition (Q2 FY25)
3. Swiggy Lynks Divestment & Supply Chain Deconsolidation (Q2 FY27)
4. Swiggy Dineout / Out-of-Home Reporting Carve-Out (Q1 FY26)
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json


MASTER_STRUCTURAL_BREAK_REGISTER = [
    {
        'event_id': 'SB-001',
        'company': 'Eternal',
        'affected_segment': 'QuickCommerce',
        'event_category': '1P_INVENTORY_TRANSITION',
        'announcement_date': '2025-07-20',
        'effective_date': '2025-08-01',
        'first_affected_quarter': 'Q2FY26',
        'last_affected_quarter': 'Ongoing',
        'headline': 'Blinkit Transition to First-Party (1P) Owned Inventory Model',
        'before_event_treatment': (
            "3P Marketplace Agency Model: Blinkit acted as an intermediary connecting third-party sellers with buyers. "
            "Revenue was recognized as net commissions, customer delivery fees, handling fees, and merchant advertising."
        ),
        'after_event_treatment': (
            "1P Principal Inventory Model (Ind AS 115 / IFRS 15): Blinkit purchases, owns, and holds inventory in dark stores. "
            "Gross merchandise value of goods sold is recorded directly as Adjusted Revenue. Merchandise purchase costs are recognized in COGS."
        ),
        'affected_metrics': 'adj_revenue_cr, take_rate_pct, gross_margin_pct, hyperpure_intercompany_eliminations',
        'original_disclosure': (
            "In Q2FY26, Blinkit restructured its operating model to take inventory ownership across high-velocity product categories. "
            "Reported Adjusted Revenue surged from ₹1,061 Cr in Q1FY26 to ₹2,423 Cr in Q2FY26 (+128% QoQ, +312% YoY) due to gross merchandise recognition. "
            "Sales from Hyperpure to Blinkit became internal eliminations."
        ),
        'source_doc': 'Eternal-Q2FY26-Shareholder-letter.pdf',
        'source_page': 12,
        'financial_impact_quantified': 'Adjusted revenue expanded by +₹1,362 Cr QoQ; Hyperpure external revenue dropped 55% due to intercompany elimination.',
        'lfl_adjustment_possible': False,
        'lfl_adjustment_methodology': (
            "BLOCKED: Management did not disclose product-level merchant purchase prices (COGS). "
            "Fabricating an estimated 3P commission rate without auditable invoice data violates financial data integrity standards. "
            "Peer comparison of reported revenue against Swiggy 3P marketplace revenue is strictly prohibited."
        ),
        'confidence_level': 'HIGH_CONFIDENCE_ACCOUNTING_BREAK',
        'unresolved_limitations': 'External analysts cannot reconstruct exact 3P take rates for Blinkit post-Q1FY26 without proprietary wholesale vendor contracts.'
    },
    {
        'event_id': 'SB-002',
        'company': 'Eternal',
        'affected_segment': 'OutOfHome',
        'event_category': 'ACQUISITION_SCOPE_EXPANSION',
        'announcement_date': '2024-08-21',
        'effective_date': '2024-08-27',
        'first_affected_quarter': 'Q2FY25',
        'last_affected_quarter': 'Ongoing',
        'headline': 'Acquisition of Entertainment Ticketing Business (Paytm Insider / TicketNew) & District Launch',
        'before_event_treatment': (
            "Organic Dining-Out Directory: Zomato Dining Out focused on restaurant discovery, table reservations, "
            "and dining payment vouchers (Zomato Pay)."
        ),
        'after_event_treatment': (
            "Comprehensive Going-Out / Entertainment Platform: Consolidated live event ticketing, movie bookings, "
            "and concert experiences following the ₹2,048 Cr acquisition of Paytm's entertainment ticketing business, rebranded as District."
        ),
        'affected_metrics': 'gov_cr, nov_cr, adj_revenue_cr, total_orders_mn',
        'original_disclosure': (
            "Transaction closed on August 27, 2024. Going-out numbers for Q2FY25 incorporate ~1 month of acquired ticketing business, "
            "and Q3FY25 incorporates the full quarter. In Q2FY25, like-for-like YoY GOV growth was 53% compared to 171% headline reported growth."
        ),
        'source_doc': 'Eternal-Q2FY25-Shareholder-letter.pdf',
        'source_page': 8,
        'financial_impact_quantified': 'Headline GOV grew 171% YoY in Q2FY25, of which organic like-for-like growth was 53% (inorganic bump: ~118% pts).',
        'lfl_adjustment_possible': True,
        'lfl_adjustment_methodology': (
            "Disclosed Organic Growth Anchor: Use Eternal's disclosed 53% YoY like-for-like organic growth rate for Q2FY25 "
            "to isolate the acquired ticketing volume from the core dining directory business."
        ),
        'confidence_level': 'HIGH_CONFIDENCE_DISCLOSED_LFL',
        'unresolved_limitations': 'Ticketing margins vs dining-out margins are not separately broken down in note disclosures.'
    },
    {
        'event_id': 'SB-003',
        'company': 'Swiggy',
        'affected_segment': 'SupplyChain',
        'event_category': 'DIVESTMENT_DECONSOLIDATION',
        'announcement_date': '2026-07-15',
        'effective_date': '2026-09-30',
        'first_affected_quarter': 'Q2FY27',
        'last_affected_quarter': 'Q3FY27',
        'headline': 'Sale of Stake in Lynks & Supply Chain Deconsolidation',
        'before_event_treatment': (
            "Consolidated B2B Logistics: Lynks logistics operations were fully consolidated in Swiggy's Supply Chain segment revenue and EBITDA."
        ),
        'after_event_treatment': (
            "Deconsolidated Equity Investment: Swiggy divested its controlling stake. Lynks ceases to be consolidated from Q3 FY27 onwards."
        ),
        'affected_metrics': 'adj_revenue_cr, adj_ebitda_cr, segment_ebitda_margin_pct',
        'original_disclosure': (
            "Swiggy completed the sale of its stake in Lynks during Q2FY27. Lynks ceases to be consolidated from Q3FY27 onwards, "
            "resulting in an expected ~₹20 crore quarterly adjusted EBITDA benefit in the Supply Chain segment."
        ),
        'source_doc': 'Swiggy-Q2FY27-Shareholder-letter.pdf',
        'source_page': 15,
        'financial_impact_quantified': 'Estimated recurring ~₹20 Cr quarterly EBITDA improvement from eliminating Lynks operating losses; ~₹200 Cr quarterly revenue reduction.',
        'lfl_adjustment_possible': True,
        'lfl_adjustment_methodology': (
            "Scope Normalization: Adjust pre-Q3FY27 Supply Chain revenues down by ~₹200 Cr per quarter and add back ~₹20 Cr EBITDA "
            "to assess core restaurant merchant procurement efficiency without third-party trucking drag."
        ),
        'confidence_level': 'HIGH_CONFIDENCE_MANAGEMENT_QUANTIFIED',
        'unresolved_limitations': 'Exact month-by-month transition in Q2 FY27 involves minor closing date stub adjustments.'
    },
    {
        'event_id': 'SB-004',
        'company': 'Swiggy',
        'affected_segment': 'OutOfHome',
        'event_category': 'SEGMENT_RECLASSIFICATION',
        'announcement_date': '2025-05-10',
        'effective_date': '2025-06-30',
        'first_affected_quarter': 'Q1FY26',
        'last_affected_quarter': 'Ongoing',
        'headline': 'Swiggy Dineout Formal Segment Carve-Out and Expansion',
        'before_event_treatment': (
            "Dineout numbers were partially reported within other platform services or consolidated without standalone quarterly run-rates."
        ),
        'after_event_treatment': (
            "Standalone Segment Reporting: Out-of-Home established with distinct GOV run-rate milestones (targeting ₹10,000 Cr annualised by FY29)."
        ),
        'affected_metrics': 'gov_cr, adj_revenue_cr, adj_ebitda_cr',
        'original_disclosure': (
            "Swiggy carved out Out-of-Home as an independent core reporting segment following Dineout expansion to 40+ cities, "
            "incorporating dining vouchers, table bookings, and SteppinOut live event ticketing."
        ),
        'source_doc': 'Swiggy-Q1FY26-Shareholder-letter.pdf',
        'source_page': 9,
        'financial_impact_quantified': 'Established baseline segment GOV starting at ~₹650 Cr quarterly.',
        'lfl_adjustment_possible': True,
        'lfl_adjustment_methodology': 'Compare to Eternal District with appropriate geographic footprint and live ticketing adjustments.',
        'confidence_level': 'HIGH_CONFIDENCE_REPORTED',
        'unresolved_limitations': 'Historical numbers pre-FY25 are not fully restated on a quarterly basis in IPO filings.'
    }
]


def get_all_structural_breaks() -> List[Dict[str, Any]]:
    """Returns the master list of all documented structural breaks."""
    return [dict(e) for e in MASTER_STRUCTURAL_BREAK_REGISTER]


def get_structural_breaks_for_query(company: Optional[str] = None, segment: Optional[str] = None, quarter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns structural breaks affecting a specific analytical query.
    """
    results = []
    for sb in MASTER_STRUCTURAL_BREAK_REGISTER:
        match_co = (company is None or sb['company'].lower() == company.lower())
        match_seg = (segment is None or sb['affected_segment'].lower() == segment.lower())
        
        # Quarter matching
        match_q = True
        if quarter and sb['first_affected_quarter']:
            # Check if query quarter is >= first_affected_quarter
            q_fy = int(quarter.replace('FY', '').replace('Q1', '').replace('Q2', '').replace('Q3', '').replace('Q4', ''))
            q_num = int(quarter[1])
            sb_fy = int(sb['first_affected_quarter'].replace('FY', '').replace('Q1', '').replace('Q2', '').replace('Q3', '').replace('Q4', ''))
            sb_num = int(sb['first_affected_quarter'][1])
            
            if q_fy < sb_fy or (q_fy == sb_fy and q_num < sb_num):
                match_q = False
                
        if match_co and match_seg and match_q:
            results.append(dict(sb))
            
    return results


def analyze_blinkit_1p_transition(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Provides the deep analytical breakdown of Blinkit's 1P transition across 4 distinct series:
    Series A: Reported Adjusted Revenue
    Series B: Like-for-Like Revenue Assessment
    Series C: Economic Operating Measures (NOV, Dark Stores, Throughput)
    Series D: Margin & Profitability Metrics
    """
    data = df if df is not None else get_analytical_df()
    
    # Extract Blinkit data
    b_df = data[(data['company'] == 'Eternal') & (data['segment'] == 'QuickCommerce')].copy()
    b_df['fy_int'] = b_df['fiscal_year'].str.replace('FY', '').astype(int)
    b_df = b_df.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)
    
    # Extract Instamart data for context
    i_df = data[(data['company'] == 'Swiggy') & (data['segment'] == 'QuickCommerce')].copy()
    i_df['fy_int'] = i_df['fiscal_year'].str.replace('FY', '').astype(int)
    i_df = i_df.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)
    
    series_rows = []
    for _, row in b_df.iterrows():
        q = row['quarter']
        fy = int(row['fiscal_year'].replace('FY', ''))
        qn = int(row['quarter_num'])
        
        is_post_1p = (fy == 26 and qn >= 2) or fy > 26
        
        # Swiggy match
        s_match = i_df[i_df['quarter'] == q]
        s_rev = float(s_match['adj_revenue_cr'].iloc[0]) if not s_match.empty and pd.notna(s_match['adj_revenue_cr'].iloc[0]) else None
        s_nov = float(s_match['nov_cr'].iloc[0]) if not s_match.empty and pd.notna(s_match['nov_cr'].iloc[0]) else None
        
        b_rev = float(row['adj_revenue_cr']) if pd.notna(row.get('adj_revenue_cr')) else None
        b_nov = float(row['nov_cr']) if pd.notna(row.get('nov_cr')) else None
        b_cm = float(row['contribution_margin_pct']) if pd.notna(row.get('contribution_margin_pct')) else None
        b_stores = int(row['dark_stores']) if pd.notna(row.get('dark_stores')) else None
        
        # Series A: Reported Adjusted Revenue
        # Series B: LFL Status
        if is_post_1p:
            lfl_status = "LFL_BLOCKED_UNAUDITED_COGS"
            lfl_revenue_cr = None
            comparability_label = "LEVEL_4_INCOMPARABLE"
            raw_rev_gap = round(b_rev - s_rev, 2) if b_rev and s_rev else None
            economic_interpretation = (
                f"Blinkit reported ₹{b_rev} Cr vs Swiggy ₹{s_rev} Cr. Raw spread of +₹{raw_rev_gap} Cr is an "
                "accounting artifact of 1P principal inventory gross billing vs 3P agent commission billing."
            )
        else:
            lfl_status = "LFL_DIRECTLY_COMPARABLE_3P"
            lfl_revenue_cr = b_rev
            comparability_label = "LEVEL_2_COMPARABLE_WITH_ADJUSTMENT"
            raw_rev_gap = round(b_rev - s_rev, 2) if b_rev and s_rev else None
            economic_interpretation = "Both platforms operating 3P marketplace commission agency models."
            
        # Series C: Operating measures (NOV & Stores are economically meaningful)
        nov_gap = round(b_nov - s_nov, 2) if b_nov and s_nov else None
        
        series_rows.append({
            'quarter': q,
            'is_post_1p_transition': is_post_1p,
            'comparability_classification': comparability_label,
            # Series A
            'blinkit_reported_adj_revenue_cr': b_rev,
            'swiggy_reported_adj_revenue_cr': s_rev,
            'reported_revenue_gap_cr': raw_rev_gap,
            # Series B
            'blinkit_lfl_revenue_status': lfl_status,
            'blinkit_lfl_revenue_cr': lfl_revenue_cr,
            # Series C: Operating measures unaffected by 1P shift
            'blinkit_nov_cr': b_nov,
            'swiggy_nov_cr': s_nov,
            'nov_gap_blinkit_lead_cr': nov_gap,
            'blinkit_dark_stores': b_stores,
            # Series D: Profitability metrics with native denominators preserved
            'blinkit_cm_pct_on_nov': b_cm,
            'economic_interpretation': economic_interpretation
        })
        
    return {
        'analysis_name': 'Blinkit 1P Inventory Accounting Transition Analysis',
        'structural_break_event_id': 'SB-001',
        'effective_quarter': 'Q2FY26',
        'accounting_framework_shift': 'Ind AS 115 Agent (3P) to Principal (1P)',
        'series_summary': {
            'series_A': 'Reported Adjusted Revenue (Surged 128% QoQ due to gross sales accounting)',
            'series_B': 'Like-for-Like Revenue (Blocked from fabrication; cannot subtract estimated COGS without disclosed invoices)',
            'series_C': 'Operating Measures (NOV and Dark Stores remain economically comparable across transition)',
            'series_D': 'Profitability Margins (Native denominators preserved: Blinkit on NOV, Swiggy on GOV)'
        },
        'timeline': series_rows
    }


def analyze_district_and_lynks_events(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Analyzes the economic impact of Eternal's District acquisition and Swiggy's Lynks divestment.
    """
    return {
        'district_ticketing_acquisition': {
            'event_id': 'SB-002',
            'company': 'Eternal',
            'effective_quarter': 'Q2FY25',
            'deal_value_inr_cr': 2048.0,
            'reported_yoy_gov_growth_q2fy25': 171.0,
            'disclosed_organic_lfl_yoy_growth_q2fy25': 53.0,
            'inorganic_growth_contribution_pts': 118.0,
            'scope_preservation_policy': (
                "FoodIQ tags pre-Q2FY25 Going-Out as organic dining directory. "
                "Post-Q2FY25 includes live event and entertainment ticketing. "
                "Organic growth calculations use the disclosed 53% anchor."
            )
        },
        'lynks_supply_chain_divestment': {
            'event_id': 'SB-003',
            'company': 'Swiggy',
            'effective_quarter': 'Q2FY27',
            'deconsolidation_start_quarter': 'Q3FY27',
            'expected_quarterly_ebitda_benefit_cr': 20.0,
            'expected_quarterly_revenue_reduction_cr': 200.0,
            'scope_preservation_policy': (
                "Do not assume recurring operating improvements without evidence. "
                "Isolate the ~₹20 Cr quarterly EBITDA loss elimination from organic restaurant supply efficiency gains."
            )
        }
    }
