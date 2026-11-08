"""
FoodIQ — 04_scenario_model.py
Loads 06_scenario_model.csv. Adds:
- quarters_to_close: estimated quarters until gap closes at current trajectory
- implied_additional_gov_cr: extra topline revenue from AOV lift
Saves scenario_extended.csv and prints scenario tables.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

PROCESSED_DIR = "data/processed"


def run_scenario_modeling() -> None:
    p6 = os.path.join(PROCESSED_DIR, "06_scenario_model.csv")
    if not os.path.exists(p6):
        print("06_scenario_model.csv missing. Running 01_run_queries.py first...")
        import importlib
        run_all_sql_queries = importlib.import_module('src.01_run_queries').run_all_sql_queries
        run_all_sql_queries()
        
    df = pd.read_csv(p6)
    
    # Historical AOV trajectory: Swiggy Instamart AOV expanded ~₹15 to ₹25 per quarter on average
    historical_quarterly_lift_inr = 20.0  # ₹20/quarter baseline pace
    
    base_gov = df.loc[df['aov_improvement_inr'] == 0, 'projected_gov_cr'].iloc[0]
    df['implied_additional_gov_cr'] = (df['projected_gov_cr'] - base_gov).round(1)
    
    # Quarters to achieve increment
    df['quarters_to_achieve'] = np.where(
        df['aov_improvement_inr'] > 0,
        (df['aov_improvement_inr'] / historical_quarterly_lift_inr).round(1),
        0.0
    )
    
    out_path = os.path.join(PROCESSED_DIR, "scenario_extended.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved extended scenario model -> {out_path}")
    
    print("\n" + "="*80)
    print("SWIGGY QUICK COMMERCE GAP-CLOSING SCENARIO MODEL")
    print("="*80)
    print(f"Base Quarter: Q2FY27 | Base AOV: ₹{df['projected_aov'].iloc[0]:.0f} | Base CM: {df['projected_cm_pct'].iloc[0]}%")
    print(f"Assumed AOV Velocity: ₹{historical_quarterly_lift_inr:.0f} / quarter | Elasticity: 1.0 bps CM per ₹1 AOV\n")
    print(df[['aov_improvement_inr', 'projected_aov', 'implied_additional_gov_cr', 'projected_gov_cr', 'projected_cm_pct', 'remaining_gap_bps', 'quarters_to_achieve']].to_string(index=False))


if __name__ == "__main__":
    run_scenario_modeling()
