import sqlite3

conn = sqlite3.connect("data/foodiq.db")
c = conn.cursor()
for table in ["source_documents", "source_pages", "business_segments", "metric_observations", "management_guidance", "guidance_outcomes"]:
    c.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in c.fetchall()]
    print(f"{table:22} : {', '.join(cols)}")
conn.close()
