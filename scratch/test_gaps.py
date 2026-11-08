import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, os.path.abspath('.'))
import pandas as pd
import numpy as np

from scratch.test_wide_metrics import wide_df

food_e = wide_df[(wide_df['company']=='Eternal') & (wide_df['segment']=='Food')].set_index('quarter')
food_s = wide_df[(wide_df['company']=='Swiggy') & (wide_df['segment']=='Food')].set_index('quarter')

gaps = []
for q in food_e.index:
    if q in food_s.index:
        for m in ['adj_revenue_cr', 'adj_ebitda_cr', 'take_rate_pct']:
            e_val = food_e.loc[q, m]
            s_val = food_s.loc[q, m]
            if pd.notna(e_val) and pd.notna(s_val):
                gap_abs = e_val - s_val
                gap_pct = (gap_abs / abs(s_val) * 100.0) if s_val != 0 else None
                direction = 'Eternal_ahead' if e_val > s_val else ('Swiggy_ahead' if s_val > e_val else 'Equal')
                gaps.append({
                    'quarter': q,
                    'segment': 'Food',
                    'metric': m,
                    'eternal_value': e_val,
                    'swiggy_value': s_val,
                    'gap_absolute': round(gap_abs, 2),
                    'gap_pct': round(gap_pct, 2) if gap_pct is not None else None,
                    'gap_direction': direction
                })

gap_df = pd.DataFrame(gaps)
print("Food Gaps Sample:")
print(gap_df.head(10).to_string())
