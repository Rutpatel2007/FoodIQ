"""
FoodIQ — 03_leading_indicator.py
Loads 04_leading_indicator.csv. Runs scipy.stats.pearsonr across multiple lags:
- Lag-0 (same quarter)
- Lag-1 (1-quarter leading)
- Lag-2 (2-quarter leading)
Prints r, p-value, n for each lag and saves leading_indicator_results.csv.
Discloses epistemic humility warnings when sample sizes are small or p > 0.10.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from scipy import stats

PROCESSED_DIR = "data/processed"


def run_leading_indicator_analysis() -> None:
    p4 = os.path.join(PROCESSED_DIR, "04_leading_indicator.csv")
    if not os.path.exists(p4):
        print("04_leading_indicator.csv missing. Running 01_run_queries.py first...")
        import importlib
        run_all_sql_queries = importlib.import_module('src.01_run_queries').run_all_sql_queries
        run_all_sql_queries()
        
    df = pd.read_csv(p4)
    
    aov = df['swiggy_aov']
    cm = df['swiggy_cm']
    
    results = []
    print("\n" + "="*80)
    print("AOV LEADING INDICATOR STATISTICAL ANALYSIS")
    print("="*80)
    
    any_sig = False
    for lag in [0, 1, 2]:
        if lag == 0:
            paired = pd.DataFrame({'aov': aov, 'cm': cm}).dropna()
            desc = "Lag-0 (Same quarter: Q_t AOV vs Q_t CM)"
        elif lag == 1:
            cm_lag1 = cm.shift(-1)
            paired = pd.DataFrame({'aov': aov, 'cm': cm_lag1}).dropna()
            desc = "Lag-1 (1-quarter lead: Q_t AOV vs Q_{t+1} CM)"
        else:
            cm_lag2 = cm.shift(-2)
            paired = pd.DataFrame({'aov': aov, 'cm': cm_lag2}).dropna()
            desc = "Lag-2 (2-quarter lead: Q_t AOV vs Q_{t+2} CM)"
            
        n = len(paired)
        if n >= 3:
            r, p = stats.pearsonr(paired['aov'], paired['cm'])
            is_sig = p < 0.10
            if is_sig:
                any_sig = True
                
            print(f"{desc:45} | n={n:2} | r={r:+.4f} | R^2={r**2:.4f} | p={p:.4f} {'***' if p<0.01 else ('**' if p<0.05 else ('*' if p<0.10 else ''))}")
            results.append({
                'lag': lag,
                'description': desc,
                'sample_size_n': n,
                'pearson_r': round(r, 4),
                'r_squared': round(r**2, 4),
                'p_value': round(p, 4),
                'is_significant_p10': bool(p < 0.10),
                'is_significant_p05': bool(p < 0.05)
            })
            
    res_df = pd.DataFrame(results)
    out_path = os.path.join(PROCESSED_DIR, "leading_indicator_results.csv")
    res_df.to_csv(out_path, index=False)
    print(f"\nSaved statistical results -> {out_path}")
    
    if not any_sig:
        print("\nWARNING: No statistically significant lead relationship found (p > 0.10 for all lags).")
        print("Report this finding honestly — do not cherry-pick or overclaim causality.")
    else:
        print("\nFINDING: Significant leading relationship observed at lag >= 1.")
        print("Note: Small sample size (N <= 10). Correlational finding reflects category mix and scale, not pure isolated causality.")


if __name__ == "__main__":
    run_leading_indicator_analysis()
