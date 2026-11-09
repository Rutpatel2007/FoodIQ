"""
Forensic Inspection: Instamart AOV, Contribution Margin, OLS Elasticity, and Break-even Models
"""
import sqlite3
import json

conn = sqlite3.connect('data/foodiq.db')
c = conn.cursor()

print("=== 1. ALL AOV OBSERVATIONS ===")
query = """
SELECT o.observation_id, o.company_id, o.segment_id, o.metric_id, o.fiscal_year, o.fiscal_quarter, o.value, o.source_document_id, o.source_page_id, o.observation_type
FROM metric_observations o
WHERE o.metric_id LIKE '%aov%' OR o.metric_id LIKE '%AOV%'
ORDER BY o.company_id, o.segment_id, o.fiscal_year, o.fiscal_quarter
"""
for r in c.execute(query).fetchall():
    print(f"  {r[1]} | {r[2]} | {r[3]} | {r[4]}-{r[5]} | val={r[6]} | {r[7]} ({r[8]}) [{r[9]}]")

print("\n=== 2. SWIGGY INSTAMART OBSERVATIONS (GOV, Orders, AOV, CM%, CM Amount) ===")
q_im = """
SELECT o.observation_id, o.metric_id, o.fiscal_year, o.fiscal_quarter, o.value, o.source_document_id, o.source_page_id, o.observation_type
FROM metric_observations o
WHERE o.company_id = 'SWIGGY' AND (o.segment_id = 'instamart' OR o.segment_id = 'quick_commerce')
ORDER BY o.fiscal_year, o.fiscal_quarter, o.metric_id
"""
im_data = {}
for r in c.execute(q_im).fetchall():
    period = f"{r[2]}-{r[3]}"
    if period not in im_data:
        im_data[period] = {}
    im_data[period][r[1]] = (r[4], r[5], r[6], r[7])

for p in sorted(im_data.keys()):
    print(f"\nQuarter: {p}")
    for m, val in im_data[p].items():
        print(f"  {m}: {val[0]} (Doc: {val[1]} PageID: {val[2]} Type: {val[3]})")
