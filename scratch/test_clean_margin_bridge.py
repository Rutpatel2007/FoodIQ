import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/foodiq.db')
food = pd.read_sql_query("SELECT * FROM metrics WHERE company='Swiggy' AND segment='Food' ORDER BY CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num", conn)
conn.close()

rows = []
for i in range(1, len(food)):
    curr = food.iloc[i]
    prev = food.iloc[i-1]
    
    q = curr['quarter']
    cm_curr = curr['contribution_margin_pct']
    cm_prev = prev['contribution_margin_pct']
    delta_cm_pct = round(cm_curr - cm_prev, 2)
    delta_cm_bps = round(delta_cm_pct * 100.0, 1)
    
    tr_curr = curr['take_rate_pct']
    tr_prev = prev['take_rate_pct']
    delta_tr_pct = round(tr_curr - tr_prev, 2)
    delta_tr_bps = round(delta_tr_pct * 100.0, 1)
    
    # Exact accounting identity:
    # CM% = TakeRate% - CostRatio%
    # Delta CM = Delta TakeRate - Delta CostRatio
    # Delta CostRatio = Delta TakeRate - Delta CM
    # Cost Efficiency Effect = - Delta CostRatio = Delta CM - Delta TakeRate
    cost_eff_bps = round(delta_cm_bps - delta_tr_bps, 1)
    
    # Reconstructed delta CM
    reconstructed_cm_bps = round(delta_tr_bps + cost_eff_bps, 1)
    
    rows.append({
        'quarter': q,
        'cm_prev_pct': cm_prev,
        'cm_curr_pct': cm_curr,
        'delta_cm_bps': delta_cm_bps,
        'take_rate_prev_pct': tr_prev,
        'take_rate_curr_pct': tr_curr,
        'take_rate_effect_bps': delta_tr_bps,
        'unallocated_cost_eff_bps': cost_eff_bps,
        'reconstructed_cm_bps': reconstructed_cm_bps,
        'bridge_residual_bps': round(delta_cm_bps - reconstructed_cm_bps, 1)
    })

b_df = pd.DataFrame(rows)
print(b_df.to_string(index=False))
