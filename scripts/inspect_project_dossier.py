"""
Deep Inspection Script for FoodIQ Master Dossier
Inspects SQLite DB tables, columns, rows, foreign keys, routes, analytics engines, and source packages.
"""
import sqlite3
import os
import json
from fastapi.testclient import TestClient
from backend.app.main import app

def inspect_db():
    conn = sqlite3.connect('data/foodiq.db')
    c = conn.cursor()
    tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
    table_info = {}
    for t in tables:
        count = c.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
        cols = c.execute(f'PRAGMA table_info("{t}")').fetchall()
        fks = c.execute(f'PRAGMA foreign_key_list("{t}")').fetchall()
        table_info[t] = {
            "row_count": count,
            "columns": [{"name": col[1], "type": col[2], "notnull": bool(col[3]), "pk": bool(col[5])} for col in cols],
            "foreign_keys": [{"from": fk[3], "table": fk[2], "to": fk[4]} for fk in fks]
        }
    return table_info

def inspect_routes():
    routes = []
    for route in app.routes:
        methods = getattr(route, "methods", None)
        path = getattr(route, "path", None)
        name = getattr(route, "name", None)
        if path:
            routes.append({
                "path": path,
                "name": name,
                "methods": list(methods) if methods else []
            })
    return sorted(routes, key=lambda x: x["path"])

def inspect_analytics():
    import backend.app.analytics as ana
    modules = [f[:-3] for f in os.listdir("backend/app/analytics") if f.endswith(".py") and f != "__init__.py"]
    return modules

def main():
    db_data = inspect_db()
    routes_data = inspect_routes()
    ana_modules = inspect_analytics()
    
    out = {
        "tables_count": len(db_data),
        "tables": db_data,
        "routes_count": len(routes_data),
        "routes": routes_data,
        "analytics_modules_count": len(ana_modules),
        "analytics_modules": ana_modules
    }
    
    with open("scratch/deep_inspection.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    
    print(f"Deep inspection complete. Tables: {len(db_data)}, Routes: {len(routes_data)}, Analytics modules: {len(ana_modules)}")

if __name__ == "__main__":
    main()
