import sqlite3
import pandas as pd

conn = sqlite3.connect('data/foodiq.db')
query = """
SELECT company, segment, quarter, gov_cr, nov_cr, adj_revenue_cr, adj_ebitda_cr, contribution_margin_pct, dark_stores, source_doc, source_page
FROM metrics
WHERE segment = 'QuickCommerce'
ORDER BY quarter, company
"""
df = pd.read_sql_query(query, conn)
print(df.to_string())
conn.close()
