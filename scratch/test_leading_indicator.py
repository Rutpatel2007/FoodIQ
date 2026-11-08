import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, os.path.abspath('.'))
import pandas as pd
import numpy as np
from scipy import stats

from scratch.test_wide_metrics import wide_df

qc_swiggy = wide_df[(wide_df['company']=='Swiggy') & (wide_df['segment']=='QuickCommerce')].sort_values(['fiscal_year', 'quarter_num']).reset_index(drop=True)

# Test Swiggy Instamart AOV vs Instamart CM
aov = qc_swiggy['aov_inr']
cm = qc_swiggy['contribution_margin_pct']

# Lag-0 (same quarter)
valid_0 = pd.DataFrame({'aov': aov, 'cm': cm}).dropna()
r0, p0 = stats.pearsonr(valid_0['aov'], valid_0['cm'])
print(f"Instamart AOV vs CM (Lag-0): r = {r0:.4f}, p = {p0:.4f}, n = {len(valid_0)}")

# Lag-1 (AOV_t vs CM_{t+1})
cm_lag1 = cm.shift(-1)
valid_1 = pd.DataFrame({'aov': aov, 'cm_next': cm_lag1}).dropna()
r1, p1 = stats.pearsonr(valid_1['aov'], valid_1['cm_next'])
print(f"Instamart AOV_t vs CM_{{t+1}} (Lag-1): r = {r1:.4f}, p = {p1:.4f}, n = {len(valid_1)}")

# Lag-2 (AOV_t vs CM_{t+2})
cm_lag2 = cm.shift(-2)
valid_2 = pd.DataFrame({'aov': aov, 'cm_next2': cm_lag2}).dropna()
r2, p2 = stats.pearsonr(valid_2['aov'], valid_2['cm_next2'])
print(f"Instamart AOV_t vs CM_{{t+2}} (Lag-2): r = {r2:.4f}, p = {p2:.4f}, n = {len(valid_2)}")
