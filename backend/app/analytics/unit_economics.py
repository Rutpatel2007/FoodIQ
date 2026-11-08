"""
FoodIQ Unit Economics Intelligence Engine (Audited & Repaired).
Computes segment-matched per-order and per-unit metrics, rigorously enforcing
denominator boundaries (never mixing platform-wide orders with segment revenues).
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json


def compute_quick_commerce_unit_economics(
    df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """
    Computes per-order unit economics for Quick Commerce strictly where segment order counts exist.
    """
    data = df if df is not None else get_analytical_df()
    
    qc_data = data[data['segment'] == 'QuickCommerce'].copy()
    qc_data['fy_int'] = qc_data['fiscal_year'].str.replace('FY', '').astype(int)
    qc_data = qc_data.sort_values(['company', 'fy_int', 'quarter_num']).reset_index(drop=True)
    
    results = []
    for _, row in qc_data.iterrows():
        company = row['company']
        orders_mn = row.get('total_orders_mn')
        aov = row.get('aov_inr')
        gov_cr = row.get('gov_cr')
        nov_cr = row.get('nov_cr')
        adj_rev_cr = row.get('adj_revenue_cr')
        cm_pct_gov = row.get('contribution_margin_pct')
        ebitda_cr = row.get('adj_ebitda_cr')
        stores = row.get('dark_stores')
        
        has_orders = pd.notna(orders_mn) and orders_mn > 0
        has_gov = pd.notna(gov_cr) and gov_cr > 0
        has_nov = pd.notna(nov_cr) and nov_cr > 0
        
        if has_orders:
            orders_val = float(orders_mn)
            # 1. Adjusted Revenue per order (₹)
            rev_per_order = round((float(adj_rev_cr) * 10.0) / orders_val, 2) if pd.notna(adj_rev_cr) else None
            
            # 2. Contribution Profit per order (₹)
            if pd.notna(aov) and pd.notna(cm_pct_gov):
                cm_per_order = round((float(aov) * float(cm_pct_gov)) / 100.0, 2)
            elif has_gov and pd.notna(cm_pct_gov):
                cm_profit_cr = (float(gov_cr) * float(cm_pct_gov)) / 100.0
                cm_per_order = round((cm_profit_cr * 10.0) / orders_val, 2)
            else:
                cm_per_order = None
                
            # 3. Adjusted EBITDA per order (₹)
            ebitda_per_order = round((float(ebitda_cr) * 10.0) / orders_val, 2) if pd.notna(ebitda_cr) else None
            
            # 4. Voucher / Subsidy per order (₹) = (GOV - NOV) * 10 / Orders
            discount_per_order = round((float(gov_cr) - float(nov_cr)) * 10.0 / orders_val, 2) if (has_gov and has_nov) else None
            
            # 5. Contribution margin on NOV (%) = CM_profit / NOV * 100
            if has_nov and pd.notna(cm_pct_gov) and has_gov:
                cm_profit_cr = (float(gov_cr) * float(cm_pct_gov)) / 100.0
                cm_pct_nov = round((cm_profit_cr / float(nov_cr)) * 100.0, 2)
            else:
                cm_pct_nov = None
                
            # 6. Adjusted EBITDA margin on reported denominator
            if pd.notna(ebitda_cr) and has_gov:
                ebitda_pct_gov = round((float(ebitda_cr) / float(gov_cr)) * 100.0, 2)
            else:
                ebitda_pct_gov = None
                
            if pd.notna(ebitda_cr) and has_nov:
                ebitda_pct_nov = round((float(ebitda_cr) / float(nov_cr)) * 100.0, 2)
            else:
                ebitda_pct_nov = None
                
            status = "CALCULATED_SEGMENT_MATCHED"
            notes = "All per-order metrics calculated using segment-matched order counts."
        else:
            rev_per_order = None
            cm_per_order = None
            ebitda_per_order = None
            discount_per_order = None
            cm_pct_nov = None
            ebitda_pct_gov = None
            ebitda_pct_nov = round((float(ebitda_cr) / float(nov_cr)) * 100.0, 2) if (pd.notna(ebitda_cr) and has_nov) else None
            status = "ORDERS_NOT_DISCLOSED"
            notes = f"{company} does not disclose quarterly order counts for Quick Commerce. Per-order division is blocked."

        # Throughput per store day (NOV ₹)
        if pd.notna(stores) and stores > 0 and has_nov:
            nov_per_store_day = round((float(nov_cr) * 1e7) / (float(stores) * 91.25), 0)
        else:
            nov_per_store_day = None

        results.append({
            'company': company,
            'segment': 'QuickCommerce',
            'quarter': row['quarter'],
            'fiscal_year': row['fiscal_year'],
            'quarter_num': int(row['quarter_num']),
            'total_orders_mn': float(orders_mn) if has_orders else None,
            'aov_inr': float(aov) if pd.notna(aov) else None,
            'gov_cr': float(gov_cr) if has_gov else None,
            'nov_cr': float(nov_cr) if has_nov else None,
            'adj_revenue_cr': float(adj_rev_cr) if pd.notna(adj_rev_cr) else None,
            'revenue_per_order_inr': rev_per_order,
            'contribution_margin_pct_gov': float(cm_pct_gov) if pd.notna(cm_pct_gov) else None,
            'contribution_margin_pct_nov': cm_pct_nov,
            'contribution_profit_per_order_inr': cm_per_order,
            'adj_ebitda_cr': float(ebitda_cr) if pd.notna(ebitda_cr) else None,
            'adj_ebitda_margin_pct_gov': ebitda_pct_gov,
            'adj_ebitda_margin_pct_nov': ebitda_pct_nov,
            'adj_ebitda_per_order_inr': ebitda_per_order,
            'voucher_subsidy_per_order_inr': discount_per_order,
            'dark_stores': int(stores) if pd.notna(stores) else None,
            'nov_per_store_day_inr': nov_per_store_day,
            'status': status,
            'methodology_notes': notes,
            'source_doc': row['source_doc'],
            'source_page': row['source_page']
        })
        
    return results


def compute_unit_economics(
    company: Optional[str] = None,
    segment: Optional[str] = None,
    df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """
    General unit economics extractor for any segment.
    QuickCommerce delegates to compute_quick_commerce_unit_economics.
    Food delivery provides segment-matched margins and revenue/EBITDA ratios.
    """
    data = df if df is not None else get_analytical_df()
    
    if segment == 'QuickCommerce':
        qc_res = compute_quick_commerce_unit_economics(data)
        if company:
            return [r for r in qc_res if r['company'] == company]
        return qc_res
        
    filtered = data.copy()
    if company:
        filtered = filtered[filtered['company'] == company]
    if segment:
        filtered = filtered[filtered['segment'] == segment]
        
    filtered['fy_int'] = filtered['fiscal_year'].str.replace('FY', '').astype(int)
    filtered = filtered.sort_values(['company', 'segment', 'fy_int', 'quarter_num']).reset_index(drop=True)
    
    results = []
    for _, row in filtered.iterrows():
        comp = row['company']
        seg = row['segment']
        orders_mn = row.get('total_orders_mn')
        aov = row.get('aov_inr')
        gov = row.get('gov_cr')
        rev = row.get('adj_revenue_cr')
        ebitda = row.get('adj_ebitda_cr')
        ebitda_margin = row.get('adj_ebitda_margin_pct')
        
        has_orders = pd.notna(orders_mn) and orders_mn > 0
        if has_orders:
            rev_per_order = round((float(rev) * 10.0) / float(orders_mn), 2) if pd.notna(rev) else None
            ebitda_per_order = round((float(ebitda) * 10.0) / float(orders_mn), 2) if pd.notna(ebitda) else None
            status = "CALCULATED_SEGMENT_MATCHED"
            notes = "Calculated from disclosed segment orders."
        else:
            rev_per_order = None
            ebitda_per_order = None
            status = "ORDERS_NOT_DISCLOSED"
            notes = f"Segment order count not disclosed for {comp} {seg}."
            
        results.append({
            'company': comp,
            'segment': seg,
            'quarter': row['quarter'],
            'fiscal_year': row['fiscal_year'],
            'quarter_num': int(row['quarter_num']),
            'total_orders_mn': float(orders_mn) if has_orders else None,
            'aov_inr': float(aov) if pd.notna(aov) else None,
            'gov_cr': float(gov) if pd.notna(gov) else None,
            'nov_cr': float(row.get('nov_cr')) if pd.notna(row.get('nov_cr')) else None,
            'adj_revenue_cr': float(rev) if pd.notna(rev) else None,
            'revenue_per_order_inr': rev_per_order,
            'adj_ebitda_cr': float(ebitda) if pd.notna(ebitda) else None,
            'adj_ebitda_margin_pct': float(ebitda_margin) if pd.notna(ebitda_margin) else None,
            'adj_ebitda_per_order_inr': ebitda_per_order,
            'status': status,
            'methodology_notes': notes,
            'source_doc': row.get('source_doc'),
            'source_page': row.get('source_page')
        })
    return results
