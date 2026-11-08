"""
FoodIQ — 02_decompositions.py
Loads 01_nov_decomposition.csv and 02_margin_bridge.csv.
Computes percentage attribution:
- What % of delta topline was volume vs. price?
- What % of delta CM was take rate vs. volume leverage vs. cost structure?
Prints summary tables for each company and saves decomposition_summary.csv.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

PROCESSED_DIR = "data/processed"


def run_decomposition_analysis() -> None:
    p1 = os.path.join(PROCESSED_DIR, "01_nov_decomposition.csv")
    p2 = os.path.join(PROCESSED_DIR, "02_margin_bridge.csv")
    
    if not os.path.exists(p1) or not os.path.exists(p2):
        print("Required CSV files missing. Running 01_run_queries.py first...")
        import importlib
        run_all_sql_queries = importlib.import_module('src.01_run_queries').run_all_sql_queries
        run_all_sql_queries()
        
    df1 = pd.read_csv(p1)
    df2 = pd.read_csv(p2)
    
    # Compute attribution percentages for Query 1
    df1['volume_pct_of_delta'] = np.where(
        df1['delta_topline_cr'] != 0,
        (df1['volume_effect_cr'] / df1['delta_topline_cr'] * 100.0).round(1),
        0.0
    )
    df1['price_pct_of_delta'] = np.where(
        df1['delta_topline_cr'] != 0,
        (df1['price_effect_cr'] / df1['delta_topline_cr'] * 100.0).round(1),
        0.0
    )
    df1['cross_term_pct_of_delta'] = np.where(
        df1['delta_topline_cr'] != 0,
        (df1['cross_term_cr'] / df1['delta_topline_cr'] * 100.0).round(1),
        0.0
    )
    
    summary_path = os.path.join(PROCESSED_DIR, "decomposition_summary.csv")
    df1.to_csv(summary_path, index=False)
    print(f"Saved decomposition summary -> {summary_path}")
    
    print("\n" + "="*80)
    print("PRICE × VOLUME DECOMPOSITION SUMMARY (QUICK COMMERCE & FOOD DELIVERY)")
    print("="*80)
    cols = ['company', 'segment', 'quarter', 'delta_topline_cr', 'volume_effect_cr', 'volume_pct_of_delta', 'price_effect_cr', 'price_pct_of_delta', 'cross_term_cr']
    print(df1[cols].dropna(subset=['volume_effect_cr']).to_string(index=False))
    
    print("\n" + "="*80)
    print("CONTRIBUTION MARGIN BRIDGE SUMMARY (BASIS POINTS)")
    print("="*80)
    bridge_cols = ['company', 'segment', 'quarter', 'delta_cm_bps', 'take_rate_delta_bps', 'volume_leverage_bps', 'cost_structure_bps']
    print(df2[bridge_cols].dropna(subset=['delta_cm_bps']).to_string(index=False))


if __name__ == "__main__":
    run_decomposition_analysis()
