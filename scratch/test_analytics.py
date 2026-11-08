import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("data/foodiq.db")

# Let's inspect Swiggy's Food Delivery and Quick Commerce metrics
swiggy_query = """
SELECT 
    mo.fiscal_year,
    mo.fiscal_quarter,
    bs.segment_name,
    mo.metric_id,
    mo.value
FROM metric_observations mo
JOIN business_segments bs ON mo.segment_id = bs.segment_id
WHERE mo.company_id = 'SWIGGY'
"""
df_swiggy = pd.read_sql_query(swiggy_query, conn)
piv_swiggy = df_swiggy.pivot_table(index=['fiscal_year', 'fiscal_quarter', 'segment_name'], columns='metric_id', values='value').reset_index()

print("Swiggy pivoted columns:")
print(piv_swiggy.columns.tolist())

# Let's inspect Eternal's Food Delivery and Quick Commerce metrics
eternal_query = """
SELECT 
    mo.fiscal_year,
    mo.fiscal_quarter,
    bs.segment_name,
    mo.metric_id,
    mo.value
FROM metric_observations mo
JOIN business_segments bs ON mo.segment_id = bs.segment_id
WHERE mo.company_id = 'ETERNAL'
"""
df_eternal = pd.read_sql_query(eternal_query, conn)
piv_eternal = df_eternal.pivot_table(index=['fiscal_year', 'fiscal_quarter', 'segment_name'], columns='metric_id', values='value').reset_index()

print("\nEternal pivoted columns:")
print(piv_eternal.columns.tolist())

conn.close()
