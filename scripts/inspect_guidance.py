import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/foodiq.db')
df = pd.read_sql('SELECT id, company, issued_quarter, target_quarter, metric, guidance_text, source_doc, source_page FROM guidance_log ORDER BY id', conn)
for _, r in df.iterrows():
    print(f"[{r['id']}] {r['company']} {r['issued_quarter']} -> {r['target_quarter']} ({r['metric']})")
    print(f"   Source: {r['source_doc']} p.{r['source_page']}")
    print(f"   Quote:  {r['guidance_text']}\n")
