import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

# Load wide metrics
df = pd.read_csv('data/processed/network_productivity.csv') # or from foodiq.db
import sqlite3
conn = sqlite3.connect('data/foodiq.db')
metrics = pd.read_sql_query("SELECT * FROM metrics WHERE company='Swiggy' AND segment='QuickCommerce' ORDER BY CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num", conn)
conn.close()

results = []
for i in range(1, len(metrics)):
    curr = metrics.iloc[i]
    prev = metrics.iloc[i-1]
    
    q = curr['quarter']
    gov_curr = curr['gov_cr']
    gov_prev = prev['gov_cr']
    delta_gov = round(gov_curr - gov_prev, 2)
    
    o_curr = curr['total_orders_mn']
    o_prev = prev['total_orders_mn']
    delta_o = o_curr - o_prev
    
    p_curr = curr['aov_inr']
    p_prev = prev['aov_inr']
    delta_p = p_curr - p_prev
    
    # 4-term decomposition:
    # Scale factor: (mn orders * INR) / 10.0 = INR Crore
    vol_eff = round((delta_o * p_prev) / 10.0, 2)
    basket_eff = round((o_prev * delta_p) / 10.0, 2)
    interaction_eff = round((delta_o * delta_p) / 10.0, 2)
    
    sum_effects = round(vol_eff + basket_eff + interaction_eff, 2)
    residual = round(delta_gov - sum_effects, 2)
    
    results.append({
        'quarter': q,
        'gov_prev': gov_prev,
        'gov_curr': gov_curr,
        'delta_gov': delta_gov,
        'orders_prev': o_prev,
        'orders_curr': o_curr,
        'aov_prev': p_prev,
        'aov_curr': p_curr,
        'volume_effect_cr': vol_eff,
        'basket_effect_cr': basket_eff,
        'interaction_effect_cr': interaction_eff,
        'sum_effects_cr': sum_effects,
        'residual_cr': residual
    })

res_df = pd.DataFrame(results)
print(res_df[['quarter', 'delta_gov', 'volume_effect_cr', 'basket_effect_cr', 'interaction_effect_cr', 'sum_effects_cr', 'residual_cr']].to_string(index=False))
