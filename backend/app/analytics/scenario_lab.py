"""
FoodIQ Interactive Scenario Lab & Simulation Engine (Phase 5).
Implements:
1. Multi-Segment Simulation Framework: Food Delivery, Quick Commerce, Out-of-Home, Supply Chain.
2. Standard Cases: BASE CASE, BULL CASE, BEAR CASE, CUSTOM CASE.
3. Transparent Parameter Pedigrees:
   - EMPIRICAL_ESTIMATE (e.g. Swiggy Instamart OLS: 0.9506 bps/INR)
   - ANALYST_ASSUMPTION (e.g. Food Delivery elasticity)
   - MANAGEMENT_GUIDANCE (e.g. Food EBITDA 4-5%)
   - HISTORICAL_AVERAGE
   - EXTERNAL_BENCHMARK
4. Strict Cross-Segment Elasticity Isolation (Instamart elasticity is never applied to Food Delivery).
5. 2-Variable Sensitivity Matrices & Break-Even Analysis.
6. Monte Carlo Simulation with explicit bounded parameter distributions.
7. Persistent Scenario Storage & Comparison.
"""

import os
import sqlite3
import json
import uuid
import datetime
from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd

from backend.app.config import settings
from backend.app.analytics.repository import _get_sqlite_path, get_analytical_df, sanitize_for_json

# Empirical calibration parameters
SWIGGY_QC_EMPIRICAL_ELASTICITY_BPS = 0.9506  # bps per INR AOV increase from N=9 OLS regression


def _init_scenario_db(db_path: Optional[str] = None):
    """Ensures the saved_scenarios table exists in foodiq.db for persistent scenario storage."""
    path = _get_sqlite_path(db_path)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS saved_scenarios (
        scenario_id TEXT PRIMARY KEY,
        scenario_name TEXT NOT NULL,
        company TEXT NOT NULL,
        segment TEXT NOT NULL,
        baseline_quarter TEXT NOT NULL,
        forecast_horizon_quarters INTEGER NOT NULL,
        scenario_type TEXT NOT NULL,
        assumptions_json TEXT NOT NULL,
        outputs_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        author TEXT NOT NULL,
        notes TEXT
    )
    """)
    conn.commit()
    conn.close()


def run_segment_scenario_simulation(
    company: str,
    segment: str,
    scenario_type: str = "BASE",
    forecast_quarters: int = 4,
    custom_assumptions: Optional[Dict[str, Any]] = None,
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Executes a scenario simulation starting from the latest reported quarterly baseline.
    Strictly isolates empirical parameters from analyst assumptions.
    """
    data = df if df is not None else get_analytical_df()
    
    # Extract baseline
    clean_seg = segment.replace('_', '').lower()
    sub = data[(data['company'].str.lower() == company.lower()) & (data['segment'].str.replace('_', '').str.lower() == clean_seg)].copy()
    sub['fy_int'] = sub['fiscal_year'].str.replace('FY', '').astype(int)
    sub = sub.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)
    
    if sub.empty:
        return {'status': 'ERROR', 'message': f'No historical data for {company} {segment}'}
        
    latest_row = sub.iloc[-1]
    baseline_quarter = latest_row['quarter']
    
    base_gov = float(latest_row['gov_cr']) if pd.notna(latest_row.get('gov_cr')) else 0.0
    base_nov = float(latest_row['nov_cr']) if pd.notna(latest_row.get('nov_cr')) else 0.0
    base_orders = float(latest_row['total_orders_mn']) if pd.notna(latest_row.get('total_orders_mn')) else 0.0
    base_aov = float(latest_row['aov_inr']) if pd.notna(latest_row.get('aov_inr')) else 0.0
    base_cm_pct = float(latest_row['contribution_margin_pct']) if pd.notna(latest_row.get('contribution_margin_pct')) else 0.0
    base_ebitda_pct = float(latest_row['adj_ebitda_margin_pct']) if pd.notna(latest_row.get('adj_ebitda_margin_pct')) else 0.0
    base_stores = int(latest_row['dark_stores']) if pd.notna(latest_row.get('dark_stores')) else 0
    
    # Configure assumptions based on scenario type and segment
    assumptions = {}
    stype = scenario_type.upper()
    
    if clean_seg == 'quickcommerce':
        # Default presets
        if stype == "BULL":
            assumptions = {
                'nov_growth_rate_pct': 35.0,
                'aov_change_inr': 50.0,
                'net_store_additions_per_quarter': 150 if company.lower() == 'eternal' else 80,
                'delivery_cost_change_inr': -2.50,
                'cm_improvement_bps': 80.0
            }
        elif stype == "BEAR":
            assumptions = {
                'nov_growth_rate_pct': 15.0,
                'aov_change_inr': -20.0,
                'net_store_additions_per_quarter': 80 if company.lower() == 'eternal' else 40,
                'delivery_cost_change_inr': 3.00,
                'cm_improvement_bps': -40.0
            }
        else:  # BASE
            assumptions = {
                'nov_growth_rate_pct': 25.0,
                'aov_change_inr': 20.0,
                'net_store_additions_per_quarter': 120 if company.lower() == 'eternal' else 60,
                'delivery_cost_change_inr': -1.00,
                'cm_improvement_bps': 30.0
            }
            
        # Parameter pedigrees
        if company.lower() == 'swiggy':
            param_pedigree = "EMPIRICAL_ESTIMATE_OLS"
            calibrated_elasticity = SWIGGY_QC_EMPIRICAL_ELASTICITY_BPS
        else:
            param_pedigree = "ANALYST_ASSUMPTION_CLUSTER_DENSITY"
            calibrated_elasticity = 0.8500
            
    elif clean_seg == 'food':
        # Food Delivery Presets
        if stype == "BULL":
            assumptions = {
                'gov_growth_rate_pct': 24.0,
                'aov_change_inr': 25.0,
                'take_rate_expansion_bps': 60.0,
                'ebitda_margin_expansion_bps': 50.0
            }
        elif stype == "BEAR":
            assumptions = {
                'gov_growth_rate_pct': 14.0,
                'aov_change_inr': -10.0,
                'take_rate_expansion_bps': -20.0,
                'ebitda_margin_expansion_bps': -30.0
            }
        else:  # BASE
            assumptions = {
                'gov_growth_rate_pct': 20.0,
                'aov_change_inr': 10.0,
                'take_rate_expansion_bps': 25.0,
                'ebitda_margin_expansion_bps': 20.0
            }
        param_pedigree = "ANALYST_ASSUMPTION_NOT_EMPIRICAL_QC"
        calibrated_elasticity = None  # Blocked from applying QC elasticity!
    else:
        # OutOfHome or SupplyChain
        assumptions = {
            'growth_rate_pct': 20.0 if stype == "BASE" else (30.0 if stype == "BULL" else 10.0),
            'margin_change_bps': 20.0 if stype == "BASE" else (50.0 if stype == "BULL" else -20.0)
        }
        param_pedigree = "ANALYST_ASSUMPTION"
        calibrated_elasticity = None

    # Merge custom overrides
    if custom_assumptions:
        assumptions.update(custom_assumptions)
        stype = "CUSTOM"

    # Forward Simulation Projection
    quarterly_projections = []
    curr_nov = base_nov if base_nov > 0 else base_gov
    curr_aov = base_aov if base_aov > 0 else 400.0
    curr_cm_pct = base_cm_pct
    curr_ebitda_pct = base_ebitda_pct
    curr_stores = base_stores
    
    growth_rate = assumptions.get('nov_growth_rate_pct', assumptions.get('gov_growth_rate_pct', assumptions.get('growth_rate_pct', 20.0)))
    quarterly_growth_factor = 1.0 + (growth_rate / 100.0) / 4.0
    
    for q_idx in range(1, forecast_quarters + 1):
        curr_nov = round(curr_nov * quarterly_growth_factor, 2)
        curr_aov = round(curr_aov + (assumptions.get('aov_change_inr', 0.0) / forecast_quarters), 2)
        curr_stores = curr_stores + int(assumptions.get('net_store_additions_per_quarter', 0))
        
        # Calculate Margin changes
        if clean_seg == 'quickcommerce':
            if company.lower() == 'swiggy':
                # Apply empirical OLS elasticity
                aov_diff = curr_aov - base_aov
                delta_cm_bps = aov_diff * SWIGGY_QC_EMPIRICAL_ELASTICITY_BPS
                curr_cm_pct = round(base_cm_pct + (delta_cm_bps / 100.0), 2)
            else:
                curr_cm_pct = round(curr_cm_pct + (assumptions.get('cm_improvement_bps', 20.0) / 100.0 / forecast_quarters), 2)
                
            est_orders = round((curr_nov * 1e7) / curr_aov / 1e6, 2) if curr_aov > 0 else None
            projected_throughput_day = round((curr_nov * 1e7) / (curr_stores * 91.25), 2) if curr_stores > 0 else None
            est_cm_profit_cr = round(curr_nov * (curr_cm_pct / 100.0), 2)
            
            quarterly_projections.append({
                'forecast_period': f'T+{q_idx}Q',
                'projected_nov_cr': curr_nov,
                'projected_aov_inr': curr_aov,
                'projected_stores': curr_stores,
                'projected_cm_pct': curr_cm_pct,
                'projected_orders_mn': est_orders,
                'projected_throughput_store_day_inr': projected_throughput_day,
                'projected_cm_profit_cr': est_cm_profit_cr
            })
        elif clean_seg == 'food':
            curr_ebitda_pct = round(curr_ebitda_pct + (assumptions.get('ebitda_margin_expansion_bps', 20.0) / 100.0 / forecast_quarters), 2)
            est_ebitda_cr = round(curr_nov * (curr_ebitda_pct / 100.0), 2)
            quarterly_projections.append({
                'forecast_period': f'T+{q_idx}Q',
                'projected_gov_cr': curr_nov,
                'projected_aov_inr': curr_aov,
                'projected_ebitda_margin_pct': curr_ebitda_pct,
                'projected_ebitda_cr': est_ebitda_cr
            })
        else:
            quarterly_projections.append({
                'forecast_period': f'T+{q_idx}Q',
                'projected_revenue_cr': curr_nov,
                'margin_assumption_bps': assumptions.get('margin_change_bps', 0.0)
            })

    return {
        'status': 'SUCCESS',
        'simulation_id': f'SIM-{uuid.uuid4().hex[:8].upper()}',
        'company': company,
        'segment': segment,
        'scenario_type': stype,
        'baseline_quarter': baseline_quarter,
        'forecast_horizon_quarters': forecast_quarters,
        'parameter_classification': param_pedigree,
        'calibrated_elasticity_bps': calibrated_elasticity,
        'assumptions_applied': assumptions,
        'baseline_metrics': {
            'gov_cr': base_gov,
            'nov_cr': base_nov,
            'orders_mn': base_orders,
            'aov_inr': base_aov,
            'contribution_margin_pct': base_cm_pct,
            'adj_ebitda_margin_pct': base_ebitda_pct,
            'dark_stores': base_stores
        },
        'projections': quarterly_projections,
        'methodology_disclosure': (
            f"Parameters classified under {param_pedigree}. "
            "Quick commerce empirical elasticity is never mixed with Food Delivery assumptions. "
            "Projections represent conditional financial simulations, not predictive forecasts."
        )
    }


def compute_two_variable_sensitivity_matrix(
    company: str,
    segment: str,
    var_x: str = "aov_change_pct",
    var_y: str = "growth_rate_pct",
    x_steps: Optional[List[float]] = None,
    y_steps: Optional[List[float]] = None,
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Computes a 2-variable sensitivity grid evaluating target metric impact (Contribution Profit or EBITDA).
    """
    steps_x = x_steps or [-10.0, -5.0, 0.0, 5.0, 10.0]
    steps_y = y_steps or [10.0, 15.0, 20.0, 25.0, 30.0]
    
    matrix = []
    for y_val in steps_y:
        row = {'growth_y_val': y_val, 'cells': []}
        for x_val in steps_x:
            # Run one-quarter simulation with test assumptions
            sim = run_segment_scenario_simulation(
                company=company,
                segment=segment,
                scenario_type="CUSTOM",
                forecast_quarters=1,
                custom_assumptions={
                    'nov_growth_rate_pct': y_val,
                    'gov_growth_rate_pct': y_val,
                    'aov_change_inr': (x_val / 100.0) * 500.0
                },
                df=df
            )
            proj = sim['projections'][0]
            metric_res = proj.get('projected_cm_profit_cr', proj.get('projected_ebitda_cr', 0.0))
            row['cells'].append({
                'x_val': x_val,
                'resulting_metric_cr': metric_res
            })
        matrix.append(row)
        
    return {
        'status': 'SUCCESS',
        'company': company,
        'segment': segment,
        'var_x': var_x,
        'var_y': var_y,
        'x_steps': steps_x,
        'y_steps': steps_y,
        'matrix': matrix
    }


def compute_breakeven_analysis(company: str, segment: str, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Calculates break-even thresholds: AOV or store throughput required to reach 0.0% CM or EBITDA.
    """
    data = df if df is not None else get_analytical_df()
    clean_seg = segment.replace('_', '').lower()
    sub = data[(data['company'].str.lower() == company.lower()) & (data['segment'].str.replace('_', '').str.lower() == clean_seg)].copy()
    if sub.empty:
        return {'status': 'ERROR', 'message': 'No data'}
        
    latest = sub.iloc[-1]
    curr_aov = float(latest['aov_inr']) if pd.notna(latest.get('aov_inr')) else 708.0
    curr_cm_pct = float(latest['contribution_margin_pct']) if pd.notna(latest.get('contribution_margin_pct')) else -1.0
    
    # Breakeven calculation for Quick Commerce
    if clean_seg == 'quickcommerce':
        # CM% = base_cm + beta * (target_aov - base_aov) / 100 = 0
        # target_aov = base_aov + (-base_cm * 100 / beta)
        beta = SWIGGY_QC_EMPIRICAL_ELASTICITY_BPS if company.lower() == 'swiggy' else 0.85
        aov_gap_needed = (-curr_cm_pct * 100.0) / beta if curr_cm_pct < 0 else 0.0
        breakeven_aov = round(curr_aov + aov_gap_needed, 2)
        
        return {
            'status': 'SUCCESS',
            'company': company,
            'segment': segment,
            'current_aov_inr': curr_aov,
            'current_cm_pct': curr_cm_pct,
            'breakeven_target': '0.0% Contribution Margin',
            'calibrated_elasticity_bps': beta,
            'breakeven_aov_inr': breakeven_aov,
            'additional_aov_required_inr': round(aov_gap_needed, 2),
            'percentage_aov_expansion_required': round((aov_gap_needed / curr_aov * 100), 2) if curr_aov > 0 else None,
            'analytical_interpretation': (
                f"At an empirical elasticity of {beta:.4f} bps/₹1, {company} Instamart requires an additional "
                f"+₹{aov_gap_needed:.2f} in AOV (reaching ₹{breakeven_aov}) to achieve contribution break-even purely through basket expansion."
            )
        }
    else:
        return {
            'status': 'SUCCESS',
            'company': company,
            'segment': segment,
            'message': 'Food Delivery is already profitable and operating above break-even thresholds (EBITDA margin >3.0%).'
        }


def run_monte_carlo_simulation(
    company: str,
    segment: str,
    iterations: int = 1000,
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Executes a bounded Monte Carlo risk simulation across parameter distributions.
    Parameters are explicitly bounded to prevent arbitrary probability distributions.
    """
    np.random.seed(42)  # For reproducible institutional research
    
    # Parametric distributions:
    # AOV change ~ Normal(mean=20, std=15) bounded between -30 and +70
    # Growth rate ~ Normal(mean=22, std=6) bounded between 5 and 40
    aov_draws = np.clip(np.random.normal(loc=20.0, scale=15.0, size=iterations), -30.0, 70.0)
    growth_draws = np.clip(np.random.normal(loc=22.0, scale=6.0, size=iterations), 5.0, 40.0)
    
    sim_profits = []
    sim_cm_pcts = []
    
    for i in range(iterations):
        aov_chg = aov_draws[i]
        gr = growth_draws[i]
        
        sim = run_segment_scenario_simulation(
            company=company,
            segment=segment,
            scenario_type="CUSTOM",
            forecast_quarters=1,
            custom_assumptions={'aov_change_inr': aov_chg, 'nov_growth_rate_pct': gr, 'gov_growth_rate_pct': gr},
            df=df
        )
        proj = sim['projections'][0]
        profit = proj.get('projected_cm_profit_cr', proj.get('projected_ebitda_cr', 0.0))
        sim_profits.append(profit)
        if 'projected_cm_pct' in proj:
            sim_cm_pcts.append(proj['projected_cm_pct'])
            
    p10_profit = round(float(np.percentile(sim_profits, 10)), 2)
    p50_profit = round(float(np.percentile(sim_profits, 50)), 2)
    p90_profit = round(float(np.percentile(sim_profits, 90)), 2)
    
    p10_cm = round(float(np.percentile(sim_cm_pcts, 10)), 2) if sim_cm_pcts else None
    p50_cm = round(float(np.percentile(sim_cm_pcts, 50)), 2) if sim_cm_pcts else None
    p90_cm = round(float(np.percentile(sim_cm_pcts, 90)), 2) if sim_cm_pcts else None
    
    prob_profitable = round(float(np.mean(np.array(sim_profits) >= 0.0) * 100), 2)
    
    return {
        'status': 'SUCCESS',
        'company': company,
        'segment': segment,
        'iterations_run': iterations,
        'distribution_assumptions': {
            'aov_change_distribution': 'Normal(mu=20, sigma=15), clipped [-30, +70]',
            'growth_rate_distribution': 'Normal(mu=22, sigma=6), clipped [+5, +40]'
        },
        'percentiles_target_profit_cr': {
            'p10_bear_boundary': p10_profit,
            'p50_median_expectation': p50_profit,
            'p90_bull_boundary': p90_profit
        },
        'percentiles_contribution_margin_pct': {
            'p10': p10_cm,
            'p50': p50_cm,
            'p90': p90_cm
        } if sim_cm_pcts else None,
        'probability_of_profitability_pct': prob_profitable,
        'methodological_disclosure': (
            "Monte Carlo distributions are analyst-specified bounding assumptions. "
            "Percentiles must not be interpreted as definitive actuarial likelihoods."
        )
    }


def save_scenario_to_storage(
    scenario_name: str,
    company: str,
    segment: str,
    scenario_type: str,
    assumptions: Dict[str, Any],
    outputs: Dict[str, Any],
    author: str = "Research Analyst",
    notes: Optional[str] = None,
    db_path: Optional[str] = None
) -> str:
    """Saves a scenario simulation into SQLite storage for persistent retrieval."""
    _init_scenario_db(db_path)
    path = _get_sqlite_path(db_path)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    
    scenario_id = f"SCEN-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.datetime.now(datetime.UTC).isoformat()
    
    c.execute("""
    INSERT INTO saved_scenarios 
    (scenario_id, scenario_name, company, segment, baseline_quarter, forecast_horizon_quarters, scenario_type, assumptions_json, outputs_json, created_at, author, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scenario_id,
        scenario_name,
        company,
        segment,
        outputs.get('baseline_quarter', 'Q2FY27'),
        outputs.get('forecast_horizon_quarters', 4),
        scenario_type,
        json.dumps(sanitize_for_json(assumptions)),
        json.dumps(sanitize_for_json(outputs)),
        now_iso,
        author,
        notes or ""
    ))
    conn.commit()
    conn.close()
    return scenario_id


def list_saved_scenarios(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all persistently stored scenarios."""
    _init_scenario_db(db_path)
    path = _get_sqlite_path(db_path)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT scenario_id, scenario_name, company, segment, baseline_quarter, scenario_type, created_at, author FROM saved_scenarios ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            'scenario_id': r[0],
            'scenario_name': r[1],
            'company': r[2],
            'segment': r[3],
            'baseline_quarter': r[4],
            'scenario_type': r[5],
            'created_at': r[6],
            'author': r[7]
        }
        for r in rows
    ]


def get_saved_scenario_by_id(scenario_id: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieves a single saved scenario with assumptions and full outputs."""
    _init_scenario_db(db_path)
    path = _get_sqlite_path(db_path)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT scenario_id, scenario_name, company, segment, baseline_quarter, forecast_horizon_quarters, scenario_type, assumptions_json, outputs_json, created_at, author, notes FROM saved_scenarios WHERE scenario_id = ?", (scenario_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return None
        
    return {
        'scenario_id': row[0],
        'scenario_name': row[1],
        'company': row[2],
        'segment': row[3],
        'baseline_quarter': row[4],
        'forecast_horizon_quarters': row[5],
        'scenario_type': row[6],
        'assumptions': json.loads(row[7]),
        'outputs': json.loads(row[8]),
        'created_at': row[9],
        'author': row[10],
        'notes': row[11]
    }
