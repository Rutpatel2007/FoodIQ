import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("data/foodiq.db")

query = """
SELECT 
    mo.company_id,
    mo.segment_id,
    mo.fiscal_year,
    mo.fiscal_quarter,
    mo.period_end_date,
    mo.metric_id,
    mo.value,
    sd.original_file_name as source_doc,
    sp.pdf_page_number as source_page
FROM metric_observations mo
JOIN source_documents sd ON mo.source_document_id = sd.document_id
LEFT JOIN source_pages sp ON mo.source_page_id = sp.page_id
"""
df = pd.read_sql_query(query, conn)

# Map segments to normalized canonical names
SEGMENT_MAP = {
    'SWIGGY_FOOD': 'Food',
    'SWIGGY_QUICK_COMMERCE': 'QuickCommerce',
    'SWIGGY_OUT_OF_HOME': 'OutOfHome',
    'SWIGGY_SUPPLY_CHAIN': 'SupplyChain',
    'SWIGGY_PLATFORM_INNOVATIONS': 'PlatformInnovations',
    'SWIGGY_PLATFORM': 'Platform',
    'SWIGGY_CONSOLIDATED': 'Consolidated',
    'ETERNAL_FOOD': 'Food',
    'ETERNAL_QUICK_COMMERCE': 'QuickCommerce',
    'ETERNAL_GOING_OUT': 'OutOfHome',
    'ETERNAL_HYPERPURE': 'SupplyChain',
    'ETERNAL_B2C': 'Platform',
    'ETERNAL_CONSOLIDATED': 'Consolidated'
}

COMPANY_MAP = {
    'SWIGGY': 'Swiggy',
    'ETERNAL': 'Eternal'
}

df['segment'] = df['segment_id'].map(SEGMENT_MAP)
df['company'] = df['company_id'].map(COMPANY_MAP)
df['quarter'] = df['fiscal_quarter'] + df['fiscal_year']
df['quarter_num'] = df['fiscal_quarter'].str.replace('Q', '').astype(int)

# Group by (company, segment, quarter, fiscal_year, quarter_num, period_end_date)
grouped = df.groupby(['company', 'segment', 'quarter', 'fiscal_year', 'quarter_num', 'period_end_date'])

rows = []
for (comp, seg, q, fy, qn, ped), group in grouped:
    val_map = dict(zip(group['metric_id'], group['value']))
    doc = group['source_doc'].iloc[0]
    page = group['source_page'].iloc[0]
    
    # Determine gov_cr
    gov = val_map.get('swiggy_gov_cr') or val_map.get('swiggy_b2c_gov_cr') or \
          val_map.get('eternal_food_gov') or val_map.get('eternal_qcomm_gov') or \
          val_map.get('eternal_going_out_gov') or val_map.get('eternal_b2c_gov')
          
    # Determine nov_cr
    nov = val_map.get('swiggy_nov_cr') or \
          val_map.get('eternal_food_nov') or val_map.get('eternal_qcomm_nov') or \
          val_map.get('eternal_going_out_nov') or val_map.get('eternal_b2c_nov')
          
    # Determine adj_revenue_cr
    adj_rev = val_map.get('swiggy_adjusted_revenue_cr') or val_map.get('swiggy_revenue_cr') or \
              val_map.get('eternal_food_adj_rev') or val_map.get('eternal_qcomm_adj_rev') or \
              val_map.get('eternal_going_out_adj_rev') or val_map.get('eternal_hyperpure_rev') or \
              val_map.get('eternal_consolidated_adj_rev')
              
    # Determine adj_ebitda_cr
    adj_ebitda = val_map.get('swiggy_adjusted_ebitda_cr') or val_map.get('swiggy_consolidated_adj_ebitda_cr') or \
                 val_map.get('eternal_food_adj_ebitda') or val_map.get('eternal_qcomm_adj_ebitda') or \
                 val_map.get('eternal_going_out_adj_ebitda') or val_map.get('eternal_hyperpure_adj_ebitda') or \
                 val_map.get('eternal_consolidated_adj_ebitda')

    # Swiggy specific
    orders = val_map.get('swiggy_total_orders_mn') or val_map.get('swiggy_b2c_total_orders_mn')
    aov = val_map.get('swiggy_aov_inr')
    mtu = val_map.get('swiggy_mtu_mn') or val_map.get('swiggy_platform_mtu_mn')
    cm_pct = val_map.get('swiggy_contribution_margin_pct')
    ebitda_margin_pct = val_map.get('swiggy_adjusted_ebitda_margin_pct') or val_map.get('swiggy_b2c_adj_ebitda_margin_pct')
    
    # Calculate margins for Eternal if not explicit
    if comp == 'Eternal':
        base_nov_gov = nov if nov is not None and not np.isnan(nov) else gov
        if adj_ebitda is not None and base_nov_gov is not None and base_nov_gov > 0:
            ebitda_margin_pct = round((adj_ebitda / base_nov_gov) * 100.0, 2)
            
    # Take rate
    take_rate = None
    base_val = nov if (nov is not None and not np.isnan(nov)) else gov
    if adj_rev is not None and base_val is not None and base_val > 0:
        take_rate = round((adj_rev / base_val) * 100.0, 2)
        
    nov_pct_gov = val_map.get('swiggy_nov_pct_of_gov')
    if nov_pct_gov is None and gov is not None and nov is not None and gov > 0:
        nov_pct_gov = round((nov / gov) * 100.0, 1)
        
    dark_stores = val_map.get('swiggy_active_dark_stores_exit') or val_map.get('eternal_qcomm_darkstores')
    dark_store_area = val_map.get('swiggy_active_dark_store_area_mn_sqft')
    orders_per_store_day = val_map.get('swiggy_orders_per_dark_store_per_day')
    gov_per_sqft = val_map.get('swiggy_gov_per_unit_area_inr_per_sqft')
    active_rest = val_map.get('swiggy_active_restaurant_partners_k') or val_map.get('swiggy_active_restaurants_k')

    rows.append({
        'company': comp,
        'quarter': q,
        'fiscal_year': fy,
        'quarter_num': qn,
        'period_end_date': ped,
        'segment': seg,
        'gov_cr': gov,
        'nov_cr': nov,
        'adj_revenue_cr': adj_rev,
        'total_orders_mn': orders,
        'mtu_mn': mtu,
        'aov_inr': aov,
        'nov_pct_of_gov': nov_pct_gov,
        'take_rate_pct': take_rate,
        'contribution_margin_pct': cm_pct,
        'adj_ebitda_cr': adj_ebitda,
        'adj_ebitda_margin_pct': ebitda_margin_pct,
        'active_restaurants_k': active_rest,
        'dark_stores': dark_stores,
        'dark_store_area_mn_sqft': dark_store_area,
        'orders_per_dark_store_per_day': orders_per_store_day,
        'gov_per_unit_area_inr_per_sqft': gov_per_sqft,
        'source_doc': doc,
        'source_page': page
    })

wide_df = pd.DataFrame(rows)
print(f"Wide metrics rows created: {len(wide_df)}")
print(wide_df.groupby(['company', 'segment'])['quarter'].count())

# Let's inspect Food segment
food = wide_df[wide_df['segment']=='Food']
print("\nFood segment sample:")
print(food[['company', 'quarter', 'gov_cr', 'nov_cr', 'adj_revenue_cr', 'adj_ebitda_cr', 'take_rate_pct', 'contribution_margin_pct', 'adj_ebitda_margin_pct']].head(10).to_string())

# Let's inspect QuickCommerce segment
qc = wide_df[wide_df['segment']=='QuickCommerce']
print("\nQuickCommerce segment sample:")
print(qc[['company', 'quarter', 'nov_cr', 'adj_revenue_cr', 'total_orders_mn', 'aov_inr', 'dark_stores']].head(10).to_string())

conn.close()
