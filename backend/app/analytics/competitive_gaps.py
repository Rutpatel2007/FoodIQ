"""
FoodIQ Competitive Gap Engine.
Computes peer comparison datasets between Eternal and Swiggy across all business segments,
strictly enforcing the 4-tier comparability governance framework and flagging structural breaks.

Phase 2.1 Comparability Governance Framework:
- LEVEL_1_DIRECTLY_COMPARABLE: Identical definition, unit, and accounting standard (e.g. dark store count).
- LEVEL_2_COMPARABLE_WITH_ADJUSTMENT: Reconcilable with explicit mathematical or policy adjustments.
- LEVEL_3_DIRECTIONALLY_COMPARABLE: Informative for directional trend analysis, but accounting boundaries differ.
- LEVEL_4_INCOMPARABLE_BLOCKED: Economically invalid comparison; direct subtraction is flagged/blocked.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.analytics.repository import get_analytical_df


COMPARABILITY_TIERS = {
    'LEVEL_1_DIRECTLY_COMPARABLE': {
        'code': 'L1',
        'description': 'Identical metric definition, recognition standard, and timing. Direct subtraction valid.'
    },
    'LEVEL_2_COMPARABLE_WITH_ADJUSTMENT': {
        'code': 'L2',
        'description': 'Reconcilable with explicit disclosed adjustments or baseline normalizations.'
    },
    'LEVEL_3_DIRECTIONALLY_COMPARABLE': {
        'code': 'L3',
        'description': 'Directionally informative; underlying cost/revenue allocations differ across companies.'
    },
    'LEVEL_4_INCOMPARABLE_BLOCKED': {
        'code': 'L4',
        'description': 'Economically and mathematically invalid comparison. Direct difference calculation is blocked.'
    }
}


def classify_comparability(segment: str, metric: str, fiscal_year: str, quarter_num: int) -> Dict[str, Any]:
    """
    Classifies peer metric comparisons into the 4-tier comparability framework.
    """
    fy_int = int(fiscal_year.replace('FY', ''))
    
    # Structural Break: Blinkit 1P Inventory Transition in Q2 FY26
    if segment == 'QuickCommerce' and metric == 'adj_revenue_cr':
        if (fy_int == 26 and quarter_num >= 2) or fy_int > 26:
            return {
                'level': 'LEVEL_4_INCOMPARABLE_BLOCKED',
                'rule_id': 'RULE-COMP-004',
                'is_flagged': True,
                'note': (
                    "STRUCTURAL BREAK: Blinkit transitioned to 1P inventory recognition in Q2 FY26 "
                    "(gross merchandise sales recorded as revenue). Swiggy Instamart operates on 3P marketplace "
                    "commission accounting. Direct comparison of reported revenue is economically invalid."
                )
            }
        else:
            return {
                'level': 'LEVEL_2_COMPARABLE_WITH_ADJUSTMENT',
                'rule_id': 'RULE-COMP-002',
                'is_flagged': False,
                'note': "Pre-Q2FY26 both platforms recognized quick commerce revenue primarily under 3P agency commission model."
            }

    # Physical counts
    if metric == 'dark_stores':
        return {
            'level': 'LEVEL_1_DIRECTLY_COMPARABLE',
            'rule_id': 'RULE-COMP-001',
            'is_flagged': False,
            'note': "Directly comparable physical operating dark store counts at period-end."
        }
        
    # Food Delivery Adjusted EBITDA & Margins
    if segment == 'Food' and metric in ['adj_ebitda_cr', 'adj_ebitda_margin_pct']:
        return {
            'level': 'LEVEL_3_DIRECTIONALLY_COMPARABLE',
            'rule_id': 'RULE-COMP-003',
            'is_flagged': False,
            'note': "Directionally comparable. Note differences in corporate ESOP adjustments and shared overhead allocation methodologies."
        }
        
    # Take rates
    if metric == 'take_rate_pct':
        return {
            'level': 'LEVEL_3_DIRECTIONALLY_COMPARABLE',
            'rule_id': 'RULE-COMP-003',
            'is_flagged': False,
            'note': "Directionally comparable. Eternal defines take rate on GOV; Swiggy disclosures track take rate on both GOV and NOV."
        }
        
    # MTU (Monthly Transacting Users)
    if metric == 'mtu_mn':
        return {
            'level': 'LEVEL_2_COMPARABLE_WITH_ADJUSTMENT',
            'rule_id': 'RULE-COMP-002',
            'is_flagged': False,
            'note': "Comparable with adjustment. Zomato reports average monthly transacting customers; Swiggy reports average monthly transacting users."
        }

    # Order values (GOV vs NOV protection)
    if metric in ['gov_cr', 'nov_cr']:
        return {
            'level': 'LEVEL_1_DIRECTLY_COMPARABLE',
            'rule_id': 'RULE-COMP-001',
            'is_flagged': False,
            'note': f"Direct comparison of matched {metric.upper()} metric."
        }

    # General financial metrics
    return {
        'level': 'LEVEL_2_COMPARABLE_WITH_ADJUSTMENT',
        'rule_id': 'RULE-COMP-002',
        'is_flagged': False,
        'note': "Segment financial comparison subject to company-specific cost apportionment and disclosure granularity."
    }


def compute_competitive_gaps(
    segment: Optional[str] = None,
    df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """
    Computes side-by-side quarterly competitive comparisons between Eternal and Swiggy.
    
    Rules enforced:
    1. GOV and NOV are never subtracted directly (cross-comparison blocked).
    2. Blinkit Q2FY26+ Adjusted Revenue is classified as LEVEL_4_INCOMPARABLE_BLOCKED.
    3. Missing metrics are preserved as None, never assumed or fabricated.
    4. Every gap record is tagged with an audited comparability level (L1 to L4).
    """
    data = df if df is not None else get_analytical_df()
    
    segments_to_compare = [segment] if segment else ['Food', 'QuickCommerce', 'OutOfHome', 'SupplyChain', 'Platform', 'Consolidated']
    
    results = []
    gap_id = 1
    for seg in segments_to_compare:
        e_df = data[(data['company'] == 'Eternal') & (data['segment'] == seg)].copy()
        s_df = data[(data['company'] == 'Swiggy') & (data['segment'] == seg)].copy()
        
        if e_df.empty or s_df.empty:
            continue
            
        e_df['fy_int'] = e_df['fiscal_year'].str.replace('FY', '').astype(int)
        e_df = e_df.sort_values(['fy_int', 'quarter_num']).set_index('quarter')
        
        s_df['fy_int'] = s_df['fiscal_year'].str.replace('FY', '').astype(int)
        s_df = s_df.sort_values(['fy_int', 'quarter_num']).set_index('quarter')
        
        # Determine metrics to compare by segment
        if seg == 'Food':
            metrics = ['adj_revenue_cr', 'adj_ebitda_cr', 'adj_ebitda_margin_pct', 'take_rate_pct', 'mtu_mn']
        elif seg == 'QuickCommerce':
            metrics = ['nov_cr', 'adj_revenue_cr', 'adj_ebitda_cr', 'dark_stores']
        elif seg == 'OutOfHome':
            metrics = ['adj_revenue_cr', 'adj_ebitda_cr']
        elif seg == 'SupplyChain':
            metrics = ['adj_revenue_cr', 'adj_ebitda_cr']
        elif seg in ['Platform', 'Consolidated']:
            metrics = ['adj_revenue_cr', 'adj_ebitda_cr']
        else:
            metrics = ['adj_revenue_cr', 'adj_ebitda_cr']
            
        for q in e_df.index:
            if q in s_df.index:
                e_row = e_df.loc[q]
                s_row = s_df.loc[q]
                
                for m in metrics:
                    e_val = e_row.get(m)
                    s_val = s_row.get(m)
                    
                    if pd.notna(e_val) and pd.notna(s_val):
                        # Governance classification
                        governance = classify_comparability(
                            seg, m, e_row['fiscal_year'], int(e_row['quarter_num'])
                        )
                        
                        comp_level = governance['level']
                        is_blocked = (comp_level == 'LEVEL_4_INCOMPARABLE_BLOCKED')
                        
                        # If blocked, calculate raw numerical gap for audit purposes but mark comparison blocked
                        gap_abs = round(float(e_val - s_val), 2)
                        gap_pct = round((gap_abs / abs(float(s_val)) * 100.0), 2) if float(s_val) != 0 else None
                        
                        if e_val > s_val:
                            direction = 'Eternal_ahead'
                        elif s_val > e_val:
                            direction = 'Swiggy_ahead'
                        else:
                            direction = 'Equal'

                        results.append({
                            'id': gap_id,
                            'quarter': q,
                            'fiscal_year': e_row['fiscal_year'],
                            'quarter_num': int(e_row['quarter_num']),
                            'segment': seg,
                            'metric': m,
                            'comparability_level': comp_level,
                            'comparability_tier_code': COMPARABILITY_TIERS[comp_level]['code'],
                            'is_comparison_blocked': is_blocked,
                            'eternal_value': float(e_val),
                            'swiggy_value': float(s_val),
                            'gap_absolute': gap_abs if not is_blocked else None,
                            'gap_percentage': gap_pct if not is_blocked else None,
                            'gap_absolute_unadjusted_raw': gap_abs,
                            'gap_percentage_unadjusted_raw': gap_pct,
                            'gap_direction': direction if not is_blocked else 'INCOMPARABLE_ACCOUNTING_BREAK',
                            'is_flagged': governance['is_flagged'],
                            'comparability_rule_id': governance['rule_id'],
                            'comparability_note': governance['note']
                        })
                        gap_id += 1
                        
    return results
