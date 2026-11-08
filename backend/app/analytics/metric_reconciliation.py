"""
FoodIQ Company-Specific Metric Reconciliation Engine (Phase 3).
Maps native financial and operational disclosures for Eternal and Swiggy across
all segments and quarters, producing the official Metric Availability Matrix.
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json


# Core metrics catalog to reconcile across segments
SEGMENT_METRIC_DEFINITIONS = {
    'Food': [
        {'metric_key': 'gov_cr', 'metric_label': 'Gross Order Value (GOV)', 'unit': 'INR Cr'},
        {'metric_key': 'nov_cr', 'metric_label': 'Net Order Value (NOV)', 'unit': 'INR Cr'},
        {'metric_key': 'adj_revenue_cr', 'metric_label': 'Adjusted Revenue', 'unit': 'INR Cr'},
        {'metric_key': 'total_orders_mn', 'metric_label': 'Total Orders', 'unit': 'Millions'},
        {'metric_key': 'aov_inr', 'metric_label': 'Average Order Value (AOV)', 'unit': 'INR'},
        {'metric_key': 'take_rate_pct', 'metric_label': 'Take Rate', 'unit': '%'},
        {'metric_key': 'contribution_margin_pct', 'metric_label': 'Contribution Margin', 'unit': '%'},
        {'metric_key': 'adj_ebitda_cr', 'metric_label': 'Adjusted EBITDA', 'unit': 'INR Cr'},
        {'metric_key': 'adj_ebitda_margin_pct', 'metric_label': 'Adjusted EBITDA Margin', 'unit': '%'},
        {'metric_key': 'mtu_mn', 'metric_label': 'Monthly Transacting Users/Customers', 'unit': 'Millions'},
        {'metric_key': 'active_restaurant_partners', 'metric_label': 'Active Restaurant Partners', 'unit': 'Count'}
    ],
    'QuickCommerce': [
        {'metric_key': 'gov_cr', 'metric_label': 'Gross Order Value (GOV)', 'unit': 'INR Cr'},
        {'metric_key': 'nov_cr', 'metric_label': 'Net Order Value (NOV)', 'unit': 'INR Cr'},
        {'metric_key': 'adj_revenue_cr', 'metric_label': 'Adjusted Revenue', 'unit': 'INR Cr'},
        {'metric_key': 'total_orders_mn', 'metric_label': 'Total Orders', 'unit': 'Millions'},
        {'metric_key': 'aov_inr', 'metric_label': 'Average Order Value (AOV)', 'unit': 'INR'},
        {'metric_key': 'contribution_margin_pct', 'metric_label': 'Contribution Margin', 'unit': '%'},
        {'metric_key': 'adj_ebitda_cr', 'metric_label': 'Adjusted EBITDA', 'unit': 'INR Cr'},
        {'metric_key': 'dark_stores', 'metric_label': 'Dark Store Count', 'unit': 'Count'},
        {'metric_key': 'avg_store_size_sqft', 'metric_label': 'Average Store Area', 'unit': 'Sq Ft'},
        {'metric_key': 'orders_per_store_per_day', 'metric_label': 'Orders per Store per Day', 'unit': 'Count'},
        {'metric_key': 'nov_per_store_day_inr', 'metric_label': 'NOV per Store per Day', 'unit': 'INR'}
    ],
    'OutOfHome': [
        {'metric_key': 'gov_cr', 'metric_label': 'Gross Order Value (GOV)', 'unit': 'INR Cr'},
        {'metric_key': 'nov_cr', 'metric_label': 'Net Order Value (NOV)', 'unit': 'INR Cr'},
        {'metric_key': 'adj_revenue_cr', 'metric_label': 'Adjusted Revenue', 'unit': 'INR Cr'},
        {'metric_key': 'total_orders_mn', 'metric_label': 'Order / Ticket Volume', 'unit': 'Millions'},
        {'metric_key': 'adj_ebitda_cr', 'metric_label': 'Adjusted EBITDA', 'unit': 'INR Cr'},
        {'metric_key': 'adj_ebitda_margin_pct', 'metric_label': 'Adjusted EBITDA Margin', 'unit': '%'}
    ],
    'SupplyChain': [
        {'metric_key': 'adj_revenue_cr', 'metric_label': 'Revenue / Wholesale Supplies', 'unit': 'INR Cr'},
        {'metric_key': 'adj_ebitda_cr', 'metric_label': 'Adjusted EBITDA', 'unit': 'INR Cr'},
        {'metric_key': 'adj_ebitda_margin_pct', 'metric_label': 'Adjusted EBITDA Margin', 'unit': '%'},
        {'metric_key': 'operating_warehouses', 'metric_label': 'Operating Warehouses / Fulfillment Hubs', 'unit': 'Count'}
    ]
}


def build_metric_availability_matrix(df: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    """
    Evaluates metric availability for every segment and metric across all historical quarters,
    comparing Eternal vs Swiggy disclosure presence.
    """
    data = df if df is not None else get_analytical_df()
    
    matrix_rows = []
    
    quarters = sorted(
        data['quarter'].unique(),
        key=lambda q: (int(q[4:]), int(q[1])) # Sort by FY, then Quarter
    )
    
    for seg, metrics in SEGMENT_METRIC_DEFINITIONS.items():
        e_seg = data[(data['company'] == 'Eternal') & (data['segment'] == seg)].set_index('quarter')
        s_seg = data[(data['company'] == 'Swiggy') & (data['segment'] == seg)].set_index('quarter')
        
        for m_info in metrics:
            m_key = m_info['metric_key']
            m_label = m_info['metric_label']
            unit = m_info['unit']
            
            e_available_count = 0
            s_available_count = 0
            both_available_count = 0
            
            quarter_breakdown = {}
            for q in quarters:
                e_val = e_seg.loc[q, m_key] if (q in e_seg.index and m_key in e_seg.columns) else np.nan
                s_val = s_seg.loc[q, m_key] if (q in s_seg.index and m_key in s_seg.columns) else np.nan
                
                e_has = pd.notna(e_val)
                s_has = pd.notna(s_val)
                
                if e_has: e_available_count += 1
                if s_has: s_available_count += 1
                if e_has and s_has: both_available_count += 1
                
                quarter_breakdown[q] = {
                    'eternal_disclosed': bool(e_has),
                    'swiggy_disclosed': bool(s_has),
                    'both_disclosed': bool(e_has and s_has),
                    'eternal_val': float(e_val) if e_has else None,
                    'swiggy_val': float(s_val) if s_has else None
                }
                
            total_quarters = len(quarters)
            if both_available_count == total_quarters:
                avail_status = "FULLY_PAIRED"
            elif both_available_count > 0:
                avail_status = "PARTIALLY_PAIRED"
            elif e_available_count > 0 or s_available_count > 0:
                avail_status = "ASYMMETRIC_SINGLE_DISCLOSURE"
            else:
                avail_status = "UNAVAILABLE_BOTH"
                
            matrix_rows.append({
                'segment': seg,
                'metric_key': m_key,
                'metric_label': m_label,
                'unit': unit,
                'availability_status': avail_status,
                'total_quarters_evaluated': total_quarters,
                'eternal_quarters_disclosed': e_available_count,
                'swiggy_quarters_disclosed': s_available_count,
                'paired_quarters_count': both_available_count,
                'quarter_details': quarter_breakdown
            })
            
    return matrix_rows


def get_flattened_availability_table(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Returns a flat DataFrame suitable for exporting to CSV."""
    raw_matrix = build_metric_availability_matrix(df)
    flat_rows = []
    
    for row in raw_matrix:
        flat = {
            'segment': row['segment'],
            'metric_key': row['metric_key'],
            'metric_label': row['metric_label'],
            'unit': row['unit'],
            'availability_status': row['availability_status'],
            'eternal_disclosed_count': row['eternal_quarters_disclosed'],
            'swiggy_disclosed_count': row['swiggy_quarters_disclosed'],
            'paired_disclosed_count': row['paired_quarters_count']
        }
        for q, details in row['quarter_details'].items():
            if details['both_disclosed']:
                flat[f'{q}_status'] = 'BOTH'
            elif details['eternal_disclosed']:
                flat[f'{q}_status'] = 'ETERNAL_ONLY'
            elif details['swiggy_disclosed']:
                flat[f'{q}_status'] = 'SWIGGY_ONLY'
            else:
                flat[f'{q}_status'] = 'NONE'
        flat_rows.append(flat)
        
    return pd.DataFrame(flat_rows)
