"""
FoodIQ Gap-Closing Scenario & Sensitivity Model Engine.
Simulates the impact of Average Order Value (AOV) improvements on segment
contribution margin trajectory, quantifying remaining competitive gaps and quarters to parity.

Phase 2.1 & Phase 3 Financial Integrity Rules:
1. Strict segment isolation: Never apply Quick Commerce (Instamart) elasticity to Food Delivery,
   and never apply Food Delivery elasticity to Instamart.
2. Segment-specific empirical calibration: Instamart empirical OLS elasticity is derived from
   paired disclosures (N=10 quarters). For Food Delivery, quarterly AOV is undisclosed, so
   empirical elasticity is marked UNAVAILABLE.
3. Transparent assumption labeling: Any simulation on Food Delivery must be explicitly labeled
   as an ASSUMPTION_NOT_EMPIRICAL_ESTIMATE.
4. Multi-tier sensitivity matrix: Conservative (0.5 bps/₹), Baseline Empirical (0.95 bps/₹), Upper/Spec (3.0 bps/₹).
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.analytics.repository import get_analytical_df


# Econometric OLS Calibration for Swiggy Instamart (FY24 Q1 - FY26 Q2 / FY27 Q2, N=10)
INSTAMART_OLS_METADATA = {
    'company': 'Swiggy',
    'segment': 'QuickCommerce',
    'sample_period': 'FY25 Q1 - FY27 Q2 (10 quarters)',
    'sample_size_quarters': 10,
    'dependent_variable': 'contribution_margin_pct_gov',
    'independent_variable': 'aov_inr',
    'ols_slope_pct_per_inr': 0.009506,
    'ols_slope_bps_per_inr': 0.9506,
    'standard_error_bps_per_inr': 0.506,
    'r_squared': 0.3059,
    'p_value': 0.0974,
    'ci_95_lower_bps_per_inr': -0.216,
    'ci_95_upper_bps_per_inr': 2.117,
    'is_empirical': True,
    'status': 'EMPIRICAL_OLS_ESTIMATE',
    'methodology_notes': (
        "Empirical OLS regression of Swiggy Instamart CM% on AOV yields a slope of "
        "+0.9506 bps CM expansion per ₹1 increase in AOV (R² = 0.3059, SE = 0.506 bps/₹). "
        "The 95% confidence interval spans [-0.22, +2.12] bps/₹. "
        "Strict Rule: This elasticity is specific to quick commerce dark-store economics and "
        "must NEVER be applied to Food Delivery."
    )
}

FOOD_DELIVERY_CALIBRATION_METADATA = {
    'company': 'Swiggy',
    'segment': 'Food',
    'sample_period': 'FY25 Q1 - FY27 Q2 (10 quarters)',
    'sample_size_quarters': 10,
    'dependent_variable': 'contribution_margin_pct_gov',
    'independent_variable': 'aov_inr',
    'ols_slope_pct_per_inr': None,
    'ols_slope_bps_per_inr': None,
    'standard_error_bps_per_inr': None,
    'r_squared': None,
    'p_value': None,
    'ci_95_lower_bps_per_inr': None,
    'ci_95_upper_bps_per_inr': None,
    'is_empirical': False,
    'status': 'EMPIRICAL_ELASTICITY_UNAVAILABLE',
    'methodology_notes': (
        "Quarterly AOV time-series is not disclosed in quarterly financial reporting for Swiggy Food Delivery. "
        "Empirical OLS regression is impossible without fabricating quarterly observations. "
        "Any scenario simulation for Food Delivery must use an explicit assumed parameter "
        "(e.g., 3.0 bps/₹ as in the spec illustration) and be labeled ASSUMPTION_NOT_EMPIRICAL_ESTIMATE."
    )
}

SENSITIVITY_TIERS_QC = {
    'conservative': {'bps_per_inr': 0.50, 'label': 'Conservative Scenario (0.50 bps/₹)'},
    'baseline': {'bps_per_inr': 0.95, 'label': 'Baseline Empirical OLS Scenario (0.95 bps/₹)'},
    'upper': {'bps_per_inr': 3.00, 'label': 'Upper / Specification Illustrative Scenario (3.00 bps/₹)'}
}

SENSITIVITY_TIERS_FOOD = {
    'conservative': {'bps_per_inr': 1.00, 'label': 'Conservative Assumed Scenario (1.00 bps/₹)'},
    'baseline': {'bps_per_inr': 2.00, 'label': 'Baseline Assumed Scenario (2.00 bps/₹)'},
    'upper': {'bps_per_inr': 3.00, 'label': 'Upper Specification Illustrative Scenario (3.00 bps/₹)'}
}


def run_aov_scenario_model(
    company: str = 'Swiggy',
    segment: str = 'QuickCommerce',
    elasticity_bps_per_inr: Optional[float] = None,
    tier: Optional[str] = 'baseline',
    aov_increments: Optional[List[int]] = None,
    assumed_base_aov: Optional[float] = None,
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Simulates AOV improvement scenarios for a specific company and segment.
    
    Enforces:
    - Never apply Instamart elasticity to Food Delivery, and vice-versa.
    - If empirical data is unavailable (Food Delivery), label clearly as assumption.
    """
    increments = aov_increments if aov_increments is not None else [0, 20, 40, 60, 80, 100]
    data = df if df is not None else get_analytical_df()
    
    seg_clean = 'QuickCommerce' if 'quick' in segment.lower() else ('Food' if 'food' in segment.lower() else segment)
    tiers_map = SENSITIVITY_TIERS_QC if seg_clean == 'QuickCommerce' else SENSITIVITY_TIERS_FOOD
    meta = INSTAMART_OLS_METADATA if seg_clean == 'QuickCommerce' else FOOD_DELIVERY_CALIBRATION_METADATA
    
    # Filter segment data
    seg_df = data[(data['company'] == company) & (data['segment'] == seg_clean)].copy()
    if seg_df.empty:
        return {
            'status': 'ERROR_NO_DATA',
            'company': company,
            'segment': seg_clean,
            'message': f"No metric observations found for {company} {seg_clean}."
        }
        
    seg_df['fy_int'] = seg_df['fiscal_year'].str.replace('FY', '').astype(int)
    seg_df = seg_df.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)
    latest = seg_df.iloc[-1]
    
    current_aov = latest.get('aov_inr')
    current_orders = latest.get('total_orders_mn')
    current_cm_pct = latest.get('contribution_margin_pct')
    current_gov_cr = latest.get('gov_cr')
    
    # Handle missing AOV in Food Delivery
    if pd.isna(current_aov) or current_aov is None:
        if assumed_base_aov is not None:
            current_aov = float(assumed_base_aov)
            aov_is_assumed = True
        elif seg_clean == 'Food':
            # Industry disclosed average annual baseline ~₹425
            current_aov = 425.0
            aov_is_assumed = True
        else:
            return {
                'status': 'MISSING_AOV_DISCLOSURE',
                'company': company,
                'segment': seg_clean,
                'message': f"AOV is not disclosed for {company} {seg_clean}. Provide assumed_base_aov to simulate."
            }
    else:
        current_aov = float(current_aov)
        aov_is_assumed = False
        
    current_orders = float(current_orders) if pd.notna(current_orders) else (
        round((float(current_gov_cr) * 10.0) / current_aov, 1) if pd.notna(current_gov_cr) else 100.0
    )
    current_cm_pct = float(current_cm_pct) if pd.notna(current_cm_pct) else 0.0
    current_gov_cr = float(current_gov_cr) if pd.notna(current_gov_cr) else round((current_orders * current_aov) / 10.0, 1)
    
    # Determine effective elasticity
    if elasticity_bps_per_inr is not None:
        effective_elasticity = float(elasticity_bps_per_inr)
        tier_label = f"Custom Assumed ({effective_elasticity:.2f} bps/₹)"
        is_empirical_run = False
    else:
        tier_clean = tier.lower() if tier and tier.lower() in tiers_map else 'baseline'
        effective_elasticity = tiers_map[tier_clean]['bps_per_inr']
        tier_label = tiers_map[tier_clean]['label']
        is_empirical_run = (seg_clean == 'QuickCommerce' and tier_clean == 'baseline')

    # Calculate historical quarterly AOV pace (where historical AOV exists)
    valid_aovs = seg_df['aov_inr'].dropna().values
    if len(valid_aovs) >= 2:
        aov_diffs = np.diff(valid_aovs[-5:])
        avg_quarterly_aov_lift = round(float(np.mean(aov_diffs)), 1) if len(aov_diffs) > 0 else 15.0
    else:
        avg_quarterly_aov_lift = 15.0  # Industry standard assumption
        
    target_cm_pct = 0.0 if seg_clean == 'QuickCommerce' else 8.0  # QC breakeven 0%, Food target 8%
    
    scenario_rows = []
    for inc in increments:
        proj_aov = current_aov + inc
        proj_gov_cr = round((current_orders * proj_aov) / 10.0, 1)
        implied_additional_gov_cr = round(proj_gov_cr - current_gov_cr, 1)
        
        cm_lift_pct = (inc * effective_elasticity) / 100.0
        proj_cm_pct = round(current_cm_pct + cm_lift_pct, 2)
        gap_to_target_bps = round((proj_cm_pct - target_cm_pct) * 100.0, 1)
        quarters_to_achieve = round(inc / avg_quarterly_aov_lift, 1) if avg_quarterly_aov_lift > 0 and inc > 0 else 0.0
        
        scenario_rows.append({
            'aov_improvement_inr': inc,
            'projected_aov_inr': proj_aov,
            'implied_additional_gov_cr': implied_additional_gov_cr,
            'projected_gov_cr': proj_gov_cr,
            'contribution_margin_lift_bps': round(cm_lift_pct * 100.0, 1),
            'projected_contribution_margin_pct': proj_cm_pct,
            'gap_to_target_bps': gap_to_target_bps,
            'gap_to_breakeven_bps': gap_to_target_bps,
            'estimated_quarters_at_current_pace': quarters_to_achieve
        })
        
    multi_tier_comparison = []
    for inc in increments:
        row = {'aov_improvement_inr': inc, 'projected_aov_inr': current_aov + inc}
        for t_name, t_meta in tiers_map.items():
            t_lift = (inc * t_meta['bps_per_inr']) / 100.0
            t_proj_cm = round(current_cm_pct + t_lift, 2)
            row[f'{t_name}_cm_pct'] = t_proj_cm
            row[f'{t_name}_gap_target_bps'] = round((t_proj_cm - target_cm_pct) * 100.0, 1)
        multi_tier_comparison.append(row)

    return {
        'company': company,
        'segment': seg_clean,
        'base_quarter': latest['quarter'],
        'base_aov_inr': current_aov,
        'base_aov_is_assumed': aov_is_assumed,
        'base_orders_mn': current_orders,
        'base_gov_cr': current_gov_cr,
        'base_cm_pct': current_cm_pct,
        'target_cm_pct': target_cm_pct,
        'historical_quarterly_aov_velocity_inr': avg_quarterly_aov_lift,
        'selected_tier': tier_label,
        'calibrated_elasticity_bps_per_inr': effective_elasticity,
        'is_empirical_estimate': is_empirical_run,
        'coefficient_nature': 'EMPIRICAL_OLS_ESTIMATE' if is_empirical_run else 'ASSUMPTION_NOT_EMPIRICAL_ESTIMATE',
        'econometric_calibration': meta,
        'sensitivity_tiers_available': tiers_map,
        'scenarios': scenario_rows,
        'multi_tier_sensitivity_matrix': multi_tier_comparison
    }
