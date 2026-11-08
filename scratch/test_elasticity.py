import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, os.path.abspath('.'))
import pandas as pd
import numpy as np
from scipy import stats

from scratch.test_wide_metrics import wide_df

qc_swiggy = wide_df[(wide_df['company']=='Swiggy') & (wide_df['segment']=='QuickCommerce')].sort_values(['fiscal_year', 'quarter_num']).reset_index(drop=True)

slope, intercept, r_value, p_value, std_err = stats.linregress(qc_swiggy['aov_inr'], qc_swiggy['contribution_margin_pct'])
print(f"Instamart Linear Regression CM % on AOV (INR):")
print(f"  Slope: {slope:.6f} (% per INR) = {slope*100:.4f} bps per INR")
print(f"  Intercept: {intercept:.4f}")
print(f"  R^2: {r_value**2:.4f}")
print(f"  p-value: {p_value:.4f}")
print(f"  Standard Error: {std_err:.6f}")
