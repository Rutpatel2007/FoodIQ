import sqlite3
import pandas as pd

conn = sqlite3.connect("data/foodiq.db")

# Query metric observations
query = """
SELECT 
    mo.company_id,
    c.canonical_name,
    bs.segment_name,
    mo.segment_id,
    mo.fiscal_year,
    mo.fiscal_quarter,
    mo.period_end_date,
    mo.metric_id,
    mo.value,
    sd.file_name,
    sp.pdf_page_number
FROM metric_observations mo
JOIN companies c ON mo.company_id = c.company_id
JOIN business_segments bs ON mo.segment_id = bs.segment_id
JOIN source_documents sd ON mo.source_document_id = sd.document_id
LEFT JOIN source_pages sp ON mo.source_page_id = sp.page_id
"""
df = pd.read_sql_query(query, conn)
print(f"Total rows: {len(df)}")
print(f"Companies: {df['company_id'].unique()}")
print(f"Segments: {df['segment_id'].unique()}")
print(f"Quarters: {df['fiscal_quarter'].unique()}")
print(f"Fiscal Years: {df['fiscal_year'].unique()}")

conn.close()
