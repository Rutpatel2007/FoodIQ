"""
FoodIQ Growth Quality Decomposition Engine (Audited & Repaired).
Performs exact 4-term mathematical waterfall decomposition of top-line metric changes:
ΔGOV = Volume Effect + Basket Effect + Interaction Effect + Residual

Where:
Volume Effect (Cr)      = (Orders_t - Orders_0) * AOV_0 / 10.0
Basket Effect (Cr)      = Orders_0 * (AOV_t - AOV_0) / 10.0
Interaction Effect (Cr) = (Orders_t - Orders_0) * (AOV_t - AOV_0) / 10.0
Residual (Cr)           = Actual ΔGOV - Volume Effect - Basket Effect - Interaction Effect

Financial Rules Enforced:
1. AOV defined as GOV / Orders decomposes GOV only. GOV-based AOV is NEVER used to decompose NOV.
2. Segments lacking reported order counts or matching AOVs are explicitly classified as INELIGIBLE.
3. Scale factor: (mn orders * INR) / 10.0 = INR Crore (1e6 * 1 / 1e7 = 0.1).
4. Exact Additivity: Volume + Basket + Interaction + Residual == Actual ΔGOV to 0.00 Cr precision.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json


def compute_waterfall_decomposition(
    company: str = "Swiggy",
    segment: str = "QuickCommerce",
    metric_basis: str = "gov_cr",
    df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """
    Computes exact 4-term mathematical decomposition for eligible transitions.
    """
    data = df if df is not None else get_analytical_df()
    
    # Filter by company and segment
    filtered = data[(data['company'] == company) & (data['segment'] == segment)].copy()
    if filtered.empty:
        return []
        
    filtered['fy_int'] = filtered['fiscal_year'].str.replace('FY', '').astype(int)
    filtered = filtered.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)
    
    results = []
    for i in range(1, len(filtered)):
        curr = filtered.iloc[i]
        prev = filtered.iloc[i - 1]
        
        curr_val = curr.get(metric_basis)
        prev_val = prev.get(metric_basis)
        
        curr_orders = curr.get('total_orders_mn')
        prev_orders = prev.get('total_orders_mn')
        
        curr_aov = curr.get('aov_inr')
        prev_aov = prev.get('aov_inr')
        
        has_orders = pd.notna(curr_orders) and pd.notna(prev_orders) and curr_orders > 0 and prev_orders > 0
        has_aov = pd.notna(curr_aov) and pd.notna(prev_aov) and curr_aov > 0 and prev_aov > 0
        has_values = pd.notna(curr_val) and pd.notna(prev_val)
        
        # Rule check: AOV is defined as GOV/Orders in shareholder letters
        is_gov_metric = metric_basis == 'gov_cr'
        is_eligible = has_orders and has_aov and has_values and is_gov_metric
        
        delta_val = round(float(curr_val - prev_val), 2) if has_values else None
        
        if is_eligible and delta_val is not None:
            delta_o = float(curr_orders - prev_orders)
            delta_p = float(curr_aov - prev_aov)
            p_0 = float(prev_aov)
            o_0 = float(prev_orders)
            
            # Exact 4-term formulas
            # 1. Volume effect: change in orders * prior AOV / 10.0
            vol_eff = round((delta_o * p_0) / 10.0, 2)
            # 2. Basket effect: prior orders * change in AOV / 10.0
            basket_eff = round((o_0 * delta_p) / 10.0, 2)
            # 3. Interaction effect: change in orders * change in AOV / 10.0
            interaction_eff = round((delta_o * delta_p) / 10.0, 2)
            # 4. Residual: delta_val - sum of effects (due to discrete disclosure rounding)
            sum_model = round(vol_eff + basket_eff + interaction_eff, 2)
            residual = round(delta_val - sum_model, 2)
            
            # Percentage attributions
            vol_pct = round((vol_eff / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            basket_pct = round((basket_eff / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            interaction_pct = round((interaction_eff / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            residual_pct = round((residual / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            
            # Dominant driver logic
            if abs(vol_eff) > max(abs(basket_eff), abs(interaction_eff)):
                dominant_driver = "Volume (Order Count)"
            elif abs(basket_eff) > max(abs(vol_eff), abs(interaction_eff)):
                dominant_driver = "Basket Size (AOV)"
            else:
                dominant_driver = "Interaction (Joint Expansion)"
                
            status = "ELIGIBLE_AND_RECONCILED"
            methodology_notes = (
                "Exact 4-term decomposition: Volume + Basket + Interaction + Residual == Actual ΔGOV. "
                "Residual reflects rounding in published disclosures (orders to 1 decimal place, integer AOV)."
            )
        else:
            vol_eff = None
            basket_eff = None
            interaction_eff = None
            residual = None
            vol_pct = None
            basket_pct = None
            interaction_pct = None
            residual_pct = None
            dominant_driver = "Not Decomposable"
            
            if not is_gov_metric:
                status = "INELIGIBLE_INVALID_METRIC_BASIS"
                methodology_notes = f"Financial rule violation: Disclosed AOV is GOV-based and cannot be applied to {metric_basis}."
            else:
                status = "INELIGIBLE_MISSING_DISCLOSURES"
                methodology_notes = "Segment does not disclose both quarterly order counts and matching AOVs in shareholder letters."
                
        growth_rate_pct = round((delta_val / float(prev_val)) * 100.0, 2) if (delta_val is not None and prev_val and prev_val > 0) else None

        results.append({
            'company': company,
            'segment': segment,
            'quarter': curr['quarter'],
            'fiscal_year': curr['fiscal_year'],
            'quarter_num': int(curr['quarter_num']),
            'metric_basis': metric_basis,
            'current_value': float(curr_val) if pd.notna(curr_val) else None,
            'previous_value': float(prev_val) if pd.notna(prev_val) else None,
            'delta_value': delta_val,
            'growth_rate_pct': growth_rate_pct,
            'total_orders_mn': float(curr_orders) if pd.notna(curr_orders) else None,
            'previous_orders_mn': float(prev_orders) if pd.notna(prev_orders) else None,
            'aov_inr': float(curr_aov) if pd.notna(curr_aov) else None,
            'previous_aov_inr': float(prev_aov) if pd.notna(prev_aov) else None,
            'volume_effect_cr': vol_eff,
            'basket_effect_cr': basket_eff,
            'interaction_effect_cr': interaction_eff,
            'residual_cr': residual,
            'volume_share_pct': vol_pct,
            'basket_share_pct': basket_pct,
            'interaction_share_pct': interaction_pct,
            'residual_share_pct': residual_pct,
            'dominant_driver': dominant_driver,
            'status': status,
            'methodology_notes': methodology_notes,
            'source_doc': curr.get('source_doc'),
            'source_page': curr.get('source_page')
        })
        
    return results


def get_all_segment_decompositions(df: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    """Returns waterfall decompositions for all segments and companies, explicitly classifying eligibility."""
    data = df if df is not None else get_analytical_df()
    all_results = []
    
    # 1. Swiggy Quick Commerce GOV (Fully Eligible)
    all_results.extend(compute_waterfall_decomposition("Swiggy", "QuickCommerce", "gov_cr", data))
    # 2. Swiggy Food Delivery GOV (Ineligible: Food orders/AOV not disclosed separately)
    all_results.extend(compute_waterfall_decomposition("Swiggy", "Food", "gov_cr", data))
    # 3. Eternal Food Delivery NOV (Ineligible: Orders/AOV not disclosed)
    all_results.extend(compute_waterfall_decomposition("Eternal", "Food", "nov_cr", data))
    # 4. Eternal Quick Commerce NOV (Ineligible: Orders/AOV not disclosed)
    all_results.extend(compute_waterfall_decomposition("Eternal", "QuickCommerce", "nov_cr", data))
    
    return all_results
