import sqlite3
import pandas as pd

conn = sqlite3.connect("data/foodiq.db")
c = conn.cursor()

# Check what segments we have in business_segments
c.execute("SELECT segment_id, company_id, segment_name FROM business_segments")
for row in c.fetchall():
    print(row)

conn.close()
