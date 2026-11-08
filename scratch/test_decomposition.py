import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, os.path.abspath('.'))
import pandas as pd
import numpy as np

from scratch.test_wide_metrics import wide_df

instamart = wide_df[(wide_df['company']=='Swiggy') & (wide_df['segment']=='QuickCommerce')].copy()

# Sort by fiscal_year and quarter_num
instamart['fy_int'] = instamart['fiscal_year'].str.replace('FY', '').astype(int)
instamart = instamart.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)

instamart['prev_gov'] = instamart['gov_cr'].shift(1)
instamart['prev_orders'] = instamart['total_orders_mn'].shift(1)
instamart['prev_aov'] = instamart['aov_inr'].shift(1)

# Decomposition formulas:
# Volume effect = (Orders_t - Orders_{t-1}) * AOV_{t-1} / 10.0 (in Cr)
# Price effect = (AOV_t - AOV_{t-1}) * Orders_t / 10.0 (in Cr) -- or with prev_orders
# Cross-term = delta_gov - volume_effect - price_effect
instamart['delta_gov'] = instamart['gov_cr'] - instamart['prev_gov']
instamart['volume_effect_cr'] = (instamart['total_orders_mn'] - instamart['prev_orders']) * instamart['prev_aov'] / 10.0
instamart['price_effect_cr'] = (instamart['aov_inr'] - instamart['prev_aov']) * instamart['total_orders_mn'] / 10.0
instamart['cross_term_cr'] = instamart['delta_gov'] - instamart['volume_effect_cr'] - instamart['price_effect_cr']

print("Swiggy Quick Commerce GOV Decomposition:")
cols = ['quarter', 'gov_cr', 'delta_gov', 'total_orders_mn', 'aov_inr', 'volume_effect_cr', 'price_effect_cr', 'cross_term_cr']
print(instamart[cols].dropna().to_string())
