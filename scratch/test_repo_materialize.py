import sys, os
sys.path.insert(0, os.path.abspath('.'))
from backend.app.analytics.repository import build_and_materialize_analytical_tables, get_analytical_df
import sqlite3

df = build_and_materialize_analytical_tables()
print(f"Materialized metrics table with {len(df)} rows.")

conn = sqlite3.connect("data/foodiq.db")
c = conn.cursor()
c.execute("SELECT count(*) FROM metrics")
print("Metrics count in DB:", c.fetchone()[0])

c.execute("SELECT count(*) FROM guidance_log")
print("Guidance log count in DB:", c.fetchone()[0])

c.execute("SELECT count(*) FROM competitive_gaps")
print("Competitive gaps count in DB:", c.fetchone()[0])

conn.close()
