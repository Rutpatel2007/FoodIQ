import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("data/foodiq.db")

# Read metric observations
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

print(f"Total observations loaded: {len(df)}")
conn.close()
