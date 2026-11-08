import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
import pandas as pd
import numpy as np
from scipy import stats

conn = sqlite3.connect('data/foodiq.db')
qc_s = pd.read_sql_query("SELECT * FROM metrics WHERE company='Swiggy' AND segment='QuickCommerce' ORDER BY CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num", conn)
conn.close()

aov = qc_s['aov_inr'].values
cm = qc_s['contribution_margin_pct'].values

# First differences
delta_aov = np.diff(aov)
delta_cm = np.diff(cm)

print(f"Total Quarters: {len(aov)}")

# Test Lags 0, 1, 2
lags = [0, 1, 2]
p_values = []
rows = []

for lag in lags:
    if lag == 0:
        x, y = aov, cm
        label = "Lag-0 (Coincident Levels)"
    elif lag == 1:
        x, y = aov[:-1], cm[1:]
        label = "Lag-1 (1-Quarter Lead Levels)"
    else:
        x, y = aov[:-2], cm[2:]
        label = "Lag-2 (2-Quarter Lead Levels)"
        
    n = len(x)
    r_pearson, p_pearson = stats.pearsonr(x, y)
    r_spearman, p_spearman = stats.spearmanr(x, y)
    
    # Fisher z 95% CI
    z = np.arctanh(r_pearson)
    se_z = 1.0 / np.sqrt(max(1, n - 3)) if n > 3 else 0.5
    ci_low, ci_high = np.tanh(z - 1.96 * se_z), np.tanh(z + 1.96 * se_z)
    
    p_values.append(p_pearson)
    rows.append({
        'test': label,
        'n': n,
        'pearson_r': round(r_pearson, 4),
        'pearson_p': round(p_pearson, 4),
        'spearman_rho': round(r_spearman, 4),
        'spearman_p': round(p_spearman, 4),
        'ci_95_low': round(ci_low, 4),
        'ci_95_high': round(ci_high, 4)
    })

# First difference test (growth changes: detrended)
r_diff, p_diff = stats.pearsonr(delta_aov, delta_cm)
rho_diff, p_rho_diff = stats.spearmanr(delta_aov, delta_cm)
rows.append({
    'test': "First Differences (Delta AOV vs Delta CM, Lag-0)",
    'n': len(delta_aov),
    'pearson_r': round(r_diff, 4),
    'pearson_p': round(p_diff, 4),
    'spearman_rho': round(rho_diff, 4),
    'spearman_p': round(p_rho_diff, 4),
    'ci_95_low': None,
    'ci_95_high': None
})

# Multiple testing correction (Bonferroni: alpha = 0.05 / 3 = 0.0167)
bonferroni_threshold = 0.05 / 3.0

res_df = pd.DataFrame(rows)
print(res_df.to_string(index=False))
print(f"\nBonferroni Adjusted Significance Threshold (m=3): {bonferroni_threshold:.4f}")
for r in rows[:3]:
    sig = r['pearson_p'] < bonferroni_threshold
    print(f"  {r['test']}: p={r['pearson_p']} -> {'PASSES Bonferroni' if sig else 'FAILS Bonferroni'}")
