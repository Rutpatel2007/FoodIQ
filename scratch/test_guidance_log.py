import sqlite3
import pandas as pd

conn = sqlite3.connect("data/foodiq.db")

query = """
SELECT 
    g.guidance_id as id,
    c.canonical_name as company,
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
JOIN companies c ON g.company_id = c.company_id
LEFT JOIN guidance_outcomes o ON g.guidance_id = o.guidance_id
LEFT JOIN source_pages sp ON g.source_page_id = sp.page_id
LEFT JOIN source_documents sd ON sp.document_id = sd.document_id
"""
df = pd.read_sql_query(query, conn)
print(f"Guidance rows: {len(df)}")
print(df[['company', 'issued_quarter', 'metric', 'outcome_status', 'met']].to_string())

conn.close()
