import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, os.path.abspath('.'))
import pandas as pd
import numpy as np

from scratch.test_wide_metrics import wide_df

swiggy_food = wide_df[(wide_df['company']=='Swiggy') & (wide_df['segment']=='Food')].copy()
swiggy_food['fy_int'] = swiggy_food['fiscal_year'].str.replace('FY', '').astype(int)
swiggy_food = swiggy_food.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)

swiggy_food['prev_gov'] = swiggy_food['gov_cr'].shift(1)
swiggy_food['prev_cm'] = swiggy_food['contribution_margin_pct'].shift(1)
swiggy_food['prev_tr'] = swiggy_food['take_rate_pct'].shift(1)

# In bps (1% = 100 bps)
swiggy_food['delta_cm_bps'] = (swiggy_food['contribution_margin_pct'] - swiggy_food['prev_cm']) * 100.0
swiggy_food['take_rate_delta_bps'] = (swiggy_food['take_rate_pct'] - swiggy_food['prev_tr']) * 100.0
swiggy_food['volume_leverage_bps'] = ((swiggy_food['gov_cr'] - swiggy_food['prev_gov']) / swiggy_food['prev_gov']) * swiggy_food['prev_cm'] * 100.0
swiggy_food['cost_structure_bps'] = swiggy_food['delta_cm_bps'] - swiggy_food['take_rate_delta_bps'] - swiggy_food['volume_leverage_bps']

cols = ['quarter', 'gov_cr', 'take_rate_pct', 'contribution_margin_pct', 'delta_cm_bps', 'take_rate_delta_bps', 'volume_leverage_bps', 'cost_structure_bps']
print("Swiggy Food Delivery Margin Bridge (bps):")
print(swiggy_food[cols].dropna().round(1).to_string())
