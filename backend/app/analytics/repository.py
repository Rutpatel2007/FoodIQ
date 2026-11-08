"""
Repository and data preparation for FoodIQ Financial Analytics Layer.
Materializes the normalized metrics fact table and guidance log in foodiq.db,
enabling both relational ORM queries and SQL analytical queries.
"""

import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.config import settings

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


def sanitize_for_json(obj: Any) -> Any:
    """Recursively converts numpy numbers and NaN to standard Python types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return None if np.isnan(obj) else float(obj)
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return [sanitize_for_json(v) for v in obj.tolist()]
    return obj


def _get_sqlite_path(db_path: Optional[str] = None) -> str:
    if db_path:
        return db_path
    url = getattr(settings, 'DATABASE_URL', 'sqlite:///data/foodiq.db')
    if url.startswith('sqlite:///'):
        return url.replace('sqlite:///', '')
    return 'data/foodiq.db'


def build_and_materialize_analytical_tables(db_path: Optional[str] = None) -> pd.DataFrame:
    """
    Extracts all observations from metric_observations and materializes:
    1. 'metrics' table - wide normalized fact table matching project specification.
    2. 'guidance_log' table - forward guidance tracker with delivery status.
    3. 'competitive_gaps' table - quarterly competitive comparison table.
    """
    path = _get_sqlite_path(db_path)
    conn = sqlite3.connect(path)
    
    # Extract observations
    obs_query = """
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
    df = pd.read_sql_query(obs_query, conn)
    
    df['segment'] = df['segment_id'].map(SEGMENT_MAP)
    df['company'] = df['company_id'].map(COMPANY_MAP)
    df['quarter'] = df['fiscal_quarter'] + df['fiscal_year']
    df['quarter_num'] = df['fiscal_quarter'].str.replace('Q', '').astype(int)
    
    grouped = df.groupby(['company', 'segment', 'quarter', 'fiscal_year', 'quarter_num', 'period_end_date'])
    
    rows = []
    for (comp, seg, q, fy, qn, ped), group in grouped:
        val_map = dict(zip(group['metric_id'], group['value']))
        doc = group['source_doc'].iloc[0]
        page = group['source_page'].iloc[0] if pd.notna(group['source_page'].iloc[0]) else None
        
        gov = val_map.get('swiggy_gov_cr') or val_map.get('swiggy_b2c_gov_cr') or \
              val_map.get('eternal_food_gov') or val_map.get('eternal_qcomm_gov') or \
              val_map.get('eternal_going_out_gov') or val_map.get('eternal_b2c_gov')
              
        nov = val_map.get('swiggy_nov_cr') or \
              val_map.get('eternal_food_nov') or val_map.get('eternal_qcomm_nov') or \
              val_map.get('eternal_going_out_nov') or val_map.get('eternal_b2c_nov')
              
        adj_rev = val_map.get('swiggy_adjusted_revenue_cr') or val_map.get('swiggy_revenue_cr') or \
                  val_map.get('eternal_food_adj_rev') or val_map.get('eternal_qcomm_adj_rev') or \
                  val_map.get('eternal_going_out_adj_rev') or val_map.get('eternal_hyperpure_rev') or \
                  val_map.get('eternal_consolidated_adj_rev')
                  
        adj_ebitda = val_map.get('swiggy_adjusted_ebitda_cr') or val_map.get('swiggy_consolidated_adj_ebitda_cr') or \
                     val_map.get('eternal_food_adj_ebitda') or val_map.get('eternal_qcomm_adj_ebitda') or \
                     val_map.get('eternal_going_out_adj_ebitda') or val_map.get('eternal_hyperpure_adj_ebitda') or \
                     val_map.get('eternal_consolidated_adj_ebitda')

        orders = val_map.get('swiggy_total_orders_mn') or val_map.get('swiggy_b2c_total_orders_mn')
        aov = val_map.get('swiggy_aov_inr')
        mtu = val_map.get('swiggy_mtu_mn') or val_map.get('swiggy_platform_mtu_mn')
        cm_pct = val_map.get('swiggy_contribution_margin_pct')
        ebitda_margin_pct = val_map.get('swiggy_adjusted_ebitda_margin_pct') or val_map.get('swiggy_b2c_adj_ebitda_margin_pct')
        
        # Calculate margins for Eternal if not explicit
        if comp == 'Eternal':
            base_nov_gov = nov if (nov is not None and not np.isnan(nov)) else gov
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
            'source_page': int(page) if page is not None and not np.isnan(page) else None,
            'data_quality_flag': None
        })

    wide_df = pd.DataFrame(rows)
    wide_df['fy_int'] = wide_df['fiscal_year'].str.replace('FY', '').astype(int)
    wide_df = wide_df.sort_values(['company', 'segment', 'fy_int', 'quarter_num']).drop(columns=['fy_int']).reset_index(drop=True)
    wide_df['id'] = wide_df.index + 1
    
    # Materialize 'metrics' table
    wide_df.to_sql('metrics', conn, if_exists='replace', index=False)
    
    # Build guidance_log table
    guidance_query = """
    SELECT 
        g.guidance_id as id,
        CASE WHEN g.company_id = 'SWIGGY' THEN 'Swiggy' ELSE 'Eternal' END as company,
        g.issued_in_quarter as issued_quarter,
        g.metric_targeted as metric,
        g.verbatim_quote as guidance_text,
        g.target_deadline_quarter as target_quarter,
        g.target_value_numeric as target_value,
        o.actual_value_numeric as actual_value,
        CASE 
            WHEN o.status LIKE '%MET%' OR o.status LIKE '%DELIVERED%' THEN 1
            WHEN o.status LIKE '%MISSED%' THEN 0
            ELSE NULL
        END as met,
        o.status as outcome_status,
        sd.original_file_name as source_doc,
        sp.pdf_page_number as source_page
    FROM management_guidance g
    JOIN source_pages sp ON g.source_page_id = sp.page_id
    JOIN source_documents sd ON sp.document_id = sd.document_id
    LEFT JOIN guidance_outcomes o ON g.guidance_id = o.guidance_id
    """
    guidance_df = pd.read_sql_query(guidance_query, conn)
    guidance_df.to_sql('guidance_log', conn, if_exists='replace', index=False)
    
    # Build competitive_gaps table
    e_df = wide_df[wide_df['company'] == 'Eternal'].set_index(['quarter', 'segment'])
    s_df = wide_df[wide_df['company'] == 'Swiggy'].set_index(['quarter', 'segment'])
    
    gaps = []
    gap_id = 1
    for (q, seg) in e_df.index:
        if (q, seg) in s_df.index:
            e_row = e_df.loc[(q, seg)]
            s_row = s_df.loc[(q, seg)]
            
            # Metrics to compare depending on segment
            compare_metrics = ['adj_revenue_cr', 'adj_ebitda_cr', 'take_rate_pct']
            if seg in ['Food', 'QuickCommerce', 'Platform']:
                compare_metrics.append('nov_cr')
            if seg == 'QuickCommerce':
                compare_metrics.append('dark_stores')
                
            for m in compare_metrics:
                e_val = e_row[m]
                s_val = s_row[m]
                if pd.notna(e_val) and pd.notna(s_val):
                    gap_abs = e_val - s_val
                    gap_pct = (gap_abs / abs(s_val) * 100.0) if s_val != 0 else None
                    direction = 'Eternal_ahead' if e_val > s_val else ('Swiggy_ahead' if s_val > e_val else 'Equal')
                    gaps.append({
                        'id': gap_id,
                        'quarter': q,
                        'segment': seg,
                        'metric': m,
                        'eternal_value': round(float(e_val), 2),
                        'swiggy_value': round(float(s_val), 2),
                        'gap_absolute': round(float(gap_abs), 2),
                        'gap_pct': round(float(gap_pct), 2) if gap_pct is not None else None,
                        'gap_direction': direction
                    })
                    gap_id += 1
                    
    gap_df = pd.DataFrame(gaps)
    gap_df.to_sql('competitive_gaps', conn, if_exists='replace', index=False)
    
    conn.close()
    return wide_df


def get_analytical_df(db_path: Optional[str] = None) -> pd.DataFrame:
    """Retrieves the wide analytical metrics dataframe from SQLite."""
    path = _get_sqlite_path(db_path)
    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM metrics", conn)
    conn.close()
    return df
