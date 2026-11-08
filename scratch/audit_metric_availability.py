import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/foodiq.db")

# Query metric observations with segment, metric def, doc, page
query = """
SELECT 
    mo.company_id,
    c.canonical_name as company_name,
    bs.segment_name,
    bs.segment_id,
    mo.fiscal_year,
    mo.fiscal_quarter,
    mo.period_end_date,
    mo.metric_id,
    md.canonical_name as metric_canonical_name,
    md.unit,
    md.denominator_formula,
    mo.value,
    sd.document_id,
    sd.original_file_name,
    sp.pdf_page_number
FROM metric_observations mo
JOIN companies c ON mo.company_id = c.company_id
JOIN business_segments bs ON mo.segment_id = bs.segment_id
JOIN metric_definitions md ON mo.metric_id = md.metric_id
JOIN source_documents sd ON mo.source_document_id = sd.document_id
LEFT JOIN source_pages sp ON mo.source_page_id = sp.page_id
"""
df = pd.read_sql_query(query, conn)
print(f"Total observations in DB: {len(df)}")

# Matrix of available metrics by company, segment, quarter
piv = df.pivot_table(index=['company_id', 'segment_id', 'metric_id'], columns=['fiscal_year', 'fiscal_quarter'], values='value', aggfunc='first')
print(f"\nTotal unique (company, segment, metric) series: {len(piv)}")

# Check NULLs vs 0s
zeros = df[df['value'] == 0]
print(f"\nZero values in DB: {len(zeros)}")
for _, r in zeros.iterrows():
    print(f"  Zero entry: {r['company_id']} | {r['segment_id']} | {r['metric_id']} | {r['fiscal_quarter']}{r['fiscal_year']}")

conn.close()
