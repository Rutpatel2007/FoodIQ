"""
FoodIQ Quick Commerce Network Productivity & Dark Store Expansion Engine (Audited & Repaired).
Tracks dark store count additions, average footprints, throughput per store-day,
and floor productivity across Blinkit and Swiggy Instamart.

Financial & Operational Distinctions Enforced:
1. Distinguishes REPORTED_ACTIVE_STORE_DAYS_BASIS from DERIVED_PERIOD_AVERAGE_APPROXIMATION.
2. Explains partial-quarter operating bias when using quarter-end store counts.
3. Documents Blinkit Q2 FY26 1P inventory transition effect on revenue throughput vs NOV throughput.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json


def compute_network_productivity(
    df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """
    Computes dark store network expansion and productivity metrics.
    """
    data = df if df is not None else get_analytical_df()
    
    qc_data = data[data['segment'] == 'QuickCommerce'].copy()
    qc_data['fy_int'] = qc_data['fiscal_year'].str.replace('FY', '').astype(int)
    qc_data = qc_data.sort_values(['company', 'fy_int', 'quarter_num']).reset_index(drop=True)
    
    results = []
    for company in ['Eternal', 'Swiggy']:
        comp_df = qc_data[qc_data['company'] == company].reset_index(drop=True)
        
        for i in range(len(comp_df)):
            curr = comp_df.iloc[i]
            prev = comp_df.iloc[i - 1] if i > 0 else None
            
            stores = curr.get('dark_stores')
            prev_stores = prev.get('dark_stores') if prev is not None else None
            
            area_mn_sqft = curr.get('dark_store_area_mn_sqft')
            nov_cr = curr.get('nov_cr')
            gov_cr = curr.get('gov_cr')
            adj_rev_cr = curr.get('adj_revenue_cr')
            reported_orders_per_store_day = curr.get('orders_per_dark_store_per_day')
            reported_gov_per_sqft = curr.get('gov_per_unit_area_inr_per_sqft')
            
            # Net additions
            if pd.notna(stores) and prev is not None and pd.notna(prev_stores):
                net_additions = int(stores - prev_stores)
                expansion_pct = round((net_additions / float(prev_stores)) * 100.0, 1)
                avg_stores_in_qtr = (float(stores) + float(prev_stores)) / 2.0
            else:
                net_additions = None
                expansion_pct = None
                avg_stores_in_qtr = float(stores) if pd.notna(stores) else None
                
            # Average store size (sq ft)
            if pd.notna(area_mn_sqft) and pd.notna(stores) and stores > 0:
                avg_store_size_sqft = round((float(area_mn_sqft) * 1e6) / float(stores), 0)
            else:
                avg_store_size_sqft = None
                
            # Throughput per store day (NOV ₹)
            # Calculated on period-average store count (91.25 days per quarter)
            if pd.notna(nov_cr) and avg_stores_in_qtr and avg_stores_in_qtr > 0:
                nov_per_store_day_avg = round((float(nov_cr) * 1e7) / (avg_stores_in_qtr * 91.25), 0)
                nov_per_store_day_exit = round((float(nov_cr) * 1e7) / (float(stores) * 91.25), 0)
            else:
                nov_per_store_day_avg = None
                nov_per_store_day_exit = None
                
            # Throughput per store day (GOV ₹)
            if pd.notna(gov_cr) and avg_stores_in_qtr and avg_stores_in_qtr > 0:
                gov_per_store_day = round((float(gov_cr) * 1e7) / (avg_stores_in_qtr * 91.25), 0)
            else:
                gov_per_store_day = None

            # Revenue throughput per store day (₹)
            if pd.notna(adj_rev_cr) and avg_stores_in_qtr and avg_stores_in_qtr > 0:
                rev_per_store_day = round((float(adj_rev_cr) * 1e7) / (avg_stores_in_qtr * 91.25), 0)
            else:
                rev_per_store_day = None

            # Accounting notes on throughput
            if company == 'Eternal' and int(curr['fiscal_year'].replace('FY', '')) >= 26 and curr['quarter_num'] >= 2:
                inventory_note = "1P INVENTORY TRANSITION: Blinkit 1P accounting inflates reported revenue per store-day from Q2 FY26. NOV throughput remains unaffected."
            else:
                inventory_note = "3P Marketplace model."

            results.append({
                'company': company,
                'brand': 'Blinkit' if company == 'Eternal' else 'Instamart',
                'quarter': curr['quarter'],
                'fiscal_year': curr['fiscal_year'],
                'quarter_num': int(curr['quarter_num']),
                'active_dark_stores_exit': int(stores) if pd.notna(stores) else None,
                'previous_dark_stores_exit': int(prev_stores) if pd.notna(prev_stores) else None,
                'net_store_additions': net_additions,
                'store_expansion_rate_pct': expansion_pct,
                'dark_store_area_mn_sqft': float(area_mn_sqft) if pd.notna(area_mn_sqft) else None,
                'avg_store_size_sqft': avg_store_size_sqft,
                'reported_orders_per_store_day': float(reported_orders_per_store_day) if pd.notna(reported_orders_per_store_day) else None,
                'reported_orders_basis': 'ACTIVE_STORE_DAYS' if pd.notna(reported_orders_per_store_day) else 'NOT_REPORTED',
                'nov_throughput_store_day_period_avg_inr': nov_per_store_day_avg,
                'nov_throughput_store_day_exit_inr': nov_per_store_day_exit,
                'gov_throughput_store_day_period_avg_inr': gov_per_store_day,
                'revenue_throughput_store_day_period_avg_inr': rev_per_store_day,
                'reported_gov_per_sqft_inr': float(reported_gov_per_sqft) if pd.notna(reported_gov_per_sqft) else None,
                'inventory_accounting_note': inventory_note,
                'source_doc': curr['source_doc'],
                'source_page': curr['source_page']
            })
            
    return results


def compute_network_comparison(df: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    """Generates side-by-side comparative table of Blinkit vs Instamart network expansion."""
    prod = compute_network_productivity(df)
    p_df = pd.DataFrame(prod)
    
    b_df = p_df[p_df['company'] == 'Eternal'].set_index('quarter')
    s_df = p_df[p_df['company'] == 'Swiggy'].set_index('quarter')
    
    comparisons = []
    for q in b_df.index:
        if q in s_df.index:
            b_row = b_df.loc[q]
            s_row = s_df.loc[q]
            
            b_stores = b_row['active_dark_stores_exit']
            s_stores = s_row['active_dark_stores_exit']
            
            b_adds = b_row['net_store_additions']
            s_adds = s_row['net_store_additions']
            
            b_nov_tput = b_row['nov_throughput_store_day_period_avg_inr']
            s_nov_tput = s_row['nov_throughput_store_day_period_avg_inr']
            
            store_gap = (b_stores - s_stores) if (pd.notna(b_stores) and pd.notna(s_stores)) else None
            adds_gap = (b_adds - s_adds) if (pd.notna(b_adds) and pd.notna(s_adds)) else None
            tput_gap = (b_nov_tput - s_nov_tput) if (pd.notna(b_nov_tput) and pd.notna(s_nov_tput)) else None
            
            comparisons.append({
                'quarter': q,
                'blinkit_stores': b_stores,
                'instamart_stores': s_stores,
                'store_gap_blinkit_lead': store_gap,
                'blinkit_net_additions': b_adds,
                'instamart_net_additions': s_adds,
                'net_additions_gap': adds_gap,
                'blinkit_nov_throughput_store_day_avg': b_nov_tput,
                'instamart_nov_throughput_store_day_avg': s_nov_tput,
                'nov_throughput_gap': tput_gap,
                'throughput_comparison_basis': 'PERIOD_AVERAGE_STORE_COUNT_91_25_DAYS',
                'leader': 'Blinkit' if (store_gap and store_gap > 0) else 'Instamart'
            })
            
    return comparisons
