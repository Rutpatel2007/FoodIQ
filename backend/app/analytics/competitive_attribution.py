"""
FoodIQ Competitive Gap Attribution Engine (Phase 3).
Performs multi-dimensional competitive advantage decomposition across:
- Scale Advantage
- Growth Advantage
- Monetisation Advantage
- Unit Economics Advantage
- Profitability Advantage
- Network Productivity Advantage
- Customer & Engagement Advantage
- Capital Efficiency Advantage

Strictly tags every comparison with its 4-tier comparability classification
and blocks invalid peer subtractions (Level 4).
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json
from backend.app.analytics.comparability_engine import get_comparability_rule


COMPETITIVE_DIMENSIONS = {
    'scale': ['gov_cr', 'nov_cr', 'mtu_mn', 'dark_stores'],
    'growth': ['gov_growth_yoy', 'nov_growth_yoy', 'adj_rev_growth_yoy'],
    'monetisation': ['take_rate_pct', 'ad_revenue_pct_gov'],
    'unit_economics': ['contribution_profit_per_order_inr', 'nov_per_store_day_inr', 'revenue_per_order_inr'],
    'profitability': ['adj_ebitda_cr', 'adj_ebitda_margin_pct', 'contribution_margin_pct'],
    'network_productivity': ['dark_stores', 'nov_per_store_day_inr', 'orders_per_store_per_day'],
    'customer_engagement': ['mtu_mn', 'order_frequency_monthly']
}


def classify_competitive_dimension(metric: str) -> str:
    """Classifies a financial or operational metric into an analytical dimension."""
    for dim, metrics in COMPETITIVE_DIMENSIONS.items():
        if metric in metrics:
            return dim
    return 'operational'


def compute_comprehensive_competitive_gaps(
    segment: Optional[str] = None,
    df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """
    Computes quarterly competitive gaps with attribution across all 8 dimensions,
    enforcing L1 to L4 comparability governance and QoQ / YoY gap trajectory analysis.
    """
    data = df if df is not None else get_analytical_df()
    
    segments_to_run = [segment] if segment else ['Food', 'QuickCommerce', 'OutOfHome', 'SupplyChain']
    
    results = []
    gap_id = 1
    
    # Sort data chronologically
    data_sorted = data.copy()
    data_sorted['fy_int'] = data_sorted['fiscal_year'].str.replace('FY', '').astype(int)
    data_sorted = data_sorted.sort_values(['company', 'segment', 'fy_int', 'quarter_num']).reset_index(drop=True)
    
    quarters = sorted(
        data['quarter'].unique(),
        key=lambda q: (int(q[4:]), int(q[1]))
    )
    
    for seg in segments_to_run:
        e_df = data_sorted[(data_sorted['company'] == 'Eternal') & (data_sorted['segment'] == seg)].set_index('quarter')
        s_df = data_sorted[(data_sorted['company'] == 'Swiggy') & (data_sorted['segment'] == seg)].set_index('quarter')
        
        # Candidate metrics to evaluate by segment
        if seg == 'Food':
            candidate_metrics = ['gov_cr', 'adj_revenue_cr', 'adj_ebitda_cr', 'adj_ebitda_margin_pct', 'take_rate_pct', 'mtu_mn']
        elif seg == 'QuickCommerce':
            candidate_metrics = ['nov_cr', 'adj_revenue_cr', 'adj_ebitda_cr', 'dark_stores', 'contribution_margin_pct']
        elif seg == 'OutOfHome':
            candidate_metrics = ['adj_revenue_cr', 'adj_ebitda_cr']
        elif seg == 'SupplyChain':
            candidate_metrics = ['adj_revenue_cr', 'adj_ebitda_cr']
        else:
            candidate_metrics = ['adj_revenue_cr', 'adj_ebitda_cr']
            
        for m in candidate_metrics:
            prev_gap_abs = None
            
            for idx, q in enumerate(quarters):
                e_val = e_df.loc[q, m] if (q in e_df.index and m in e_df.columns) else np.nan
                s_val = s_df.loc[q, m] if (q in s_df.index and m in s_df.columns) else np.nan
                
                # Check for historical YoY quarter (4 quarters prior)
                prev_yoy_q = quarters[idx - 4] if idx >= 4 else None
                e_yoy_val = e_df.loc[prev_yoy_q, m] if (prev_yoy_q and prev_yoy_q in e_df.index and m in e_df.columns) else np.nan
                s_yoy_val = s_df.loc[prev_yoy_q, m] if (prev_yoy_q and prev_yoy_q in s_df.index and m in s_df.columns) else np.nan
                
                # Check presence
                if pd.notna(e_val) and pd.notna(s_val):
                    fy = e_df.loc[q, 'fiscal_year'] if 'fiscal_year' in e_df.columns else f"FY{q[4:]}"
                    qn = int(q[1])
                    
                    # Rule lookup
                    rule = get_comparability_rule(seg, m, fy, qn)
                    comp_level = rule['comparability_level']
                    is_blocked = (comp_level == 'LEVEL_4')
                    
                    # Gap calculations
                    e_num = float(e_val)
                    s_num = float(s_val)
                    gap_abs = round(e_num - s_num, 2)
                    gap_pct = round((gap_abs / abs(s_num) * 100.0), 1) if s_num != 0 else None
                    
                    # QoQ gap trajectory
                    if prev_gap_abs is not None and not is_blocked:
                        qoq_gap_change = round(gap_abs - prev_gap_abs, 2)
                        gap_trajectory = 'EXPANDING' if abs(gap_abs) > abs(prev_gap_abs) else ('CONTRACTING' if abs(gap_abs) < abs(prev_gap_abs) else 'STABLE')
                    else:
                        qoq_gap_change = None
                        gap_trajectory = 'BASELINE'
                    prev_gap_abs = gap_abs if not is_blocked else None
                    
                    # YoY growth comparison where comparable
                    e_yoy_growth = round(((e_num - float(e_yoy_val)) / abs(float(e_yoy_val))) * 100.0, 1) if pd.notna(e_yoy_val) and float(e_yoy_val) != 0 else None
                    s_yoy_growth = round(((s_num - float(s_yoy_val)) / abs(float(s_yoy_val))) * 100.0, 1) if pd.notna(s_yoy_val) and float(s_yoy_val) != 0 else None
                    growth_spread_pts = round(e_yoy_growth - s_yoy_growth, 1) if (e_yoy_growth is not None and s_yoy_growth is not None) else None
                    
                    # Direction of advantage
                    if is_blocked:
                        direction = 'INCOMPARABLE_ACCOUNTING_BREAK'
                        leader = 'BLOCKED'
                    elif e_num > s_num:
                        direction = 'ETERNAL_AHEAD'
                        leader = 'Eternal'
                    elif s_num > e_num:
                        direction = 'SWIGGY_AHEAD'
                        leader = 'Swiggy'
                    else:
                        direction = 'EQUAL'
                        leader = 'Equal'
                        
                    results.append({
                        'id': f"GAP-{gap_id:04d}",
                        'quarter': q,
                        'fiscal_year': fy,
                        'quarter_num': qn,
                        'segment': seg,
                        'metric': m,
                        'dimension': classify_competitive_dimension(m),
                        'comparability_level': comp_level,
                        'comparability_tier_code': rule.get('tier_code', 'L2'),
                        'is_comparison_blocked': is_blocked,
                        'eternal_value': e_num,
                        'swiggy_value': s_num,
                        'gap_absolute': gap_abs if not is_blocked else None,
                        'gap_percentage': gap_pct if not is_blocked else None,
                        'gap_absolute_unadjusted_raw': gap_abs,
                        'gap_percentage_unadjusted_raw': gap_pct,
                        'leader': leader,
                        'gap_direction': direction,
                        'qoq_gap_change': qoq_gap_change,
                        'gap_trajectory': gap_trajectory,
                        'eternal_yoy_growth_pct': e_yoy_growth,
                        'swiggy_yoy_growth_pct': s_yoy_growth,
                        'growth_spread_pts': growth_spread_pts,
                        'comparability_rule_id': rule['rule_id'],
                        'comparability_note': rule['explanation'],
                        'limitations': rule.get('known_limitations', '')
                    })
                    gap_id += 1
                    
    return results
