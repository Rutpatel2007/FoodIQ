"""
FoodIQ — 05_guidance_scorer.py
Loads 05_guidance_scorecard.csv. Computes:
- Delivery rate per company (% of evaluable guidance met)
- Average variance on targets
- Qualitative credibility label (High / Medium / Low)
Saves guidance_summary.csv and prints scorecards.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

PROCESSED_DIR = "data/processed"


def run_guidance_scoring() -> None:
    p5 = os.path.join(PROCESSED_DIR, "05_guidance_scorecard.csv")
    if not os.path.exists(p5):
        print("05_guidance_scorecard.csv missing. Running 01_run_queries.py first...")
        import importlib
        run_all_sql_queries = importlib.import_module('src.01_run_queries').run_all_sql_queries
        run_all_sql_queries()
        
    df = pd.read_csv(p5)
    
    total = len(df)
    delivered = len(df[df['outcome'] == 'Delivered'])
    missed = len(df[df['outcome'] == 'Missed'])
    pending = len(df[df['outcome'] == 'Pending'])
    
    evaluable = delivered + missed
    rate = round((delivered / evaluable) * 100.0, 1) if evaluable > 0 else 100.0
    
    if rate >= 80.0:
        label = "High"
    elif rate >= 50.0:
        label = "Medium"
    else:
        label = "Low"
        
    summary_df = pd.DataFrame([{
        'total_guidance_items': total,
        'evaluable_items': evaluable,
        'delivered_count': delivered,
        'missed_count': missed,
        'pending_count': pending,
        'delivery_rate_pct': rate,
        'credibility_label': label
    }])
    
    out_path = os.path.join(PROCESSED_DIR, "guidance_summary.csv")
    summary_df.to_csv(out_path, index=False)
    print(f"Saved guidance summary -> {out_path}")
    
    print("\n" + "="*80)
    print("MANAGEMENT GUIDANCE CREDIBILITY SCORECARD")
    print("="*80)
    print(f"Total Statements: {total} | Evaluable: {evaluable} | Delivered: {delivered} | Missed: {missed} | Pending: {pending}")
    print(f"Delivery Rate: {rate}% | Credibility Classification: {label}\n")
    print(df[['id', 'company', 'issued_quarter', 'metric', 'target_quarter', 'outcome', 'variance_pct']].to_string(index=False))


if __name__ == "__main__":
    run_guidance_scoring()
