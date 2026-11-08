import sqlite3

conn = sqlite3.connect("data/foodiq.db")
c = conn.cursor()
c.execute("SELECT type, name FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY type, name")
for t, n in c.fetchall():
    print(f"{t:6} : {n}")
conn.close()
