import json

with open('scratch/deep_inspection.json') as f:
    d = json.load(f)

print("Tables and Row Counts:")
for t, info in d['tables'].items():
    print(f"  {t}: {info['row_count']} rows, {len(info['columns'])} cols, {len(info['foreign_keys'])} FKs")

print(f"\nTotal Tables: {len(d['tables'])}")

print("\nAnalytics Modules:")
for m in sorted(d['analytics_modules']):
    print(f"  backend/app/analytics/{m}.py")

print(f"\nTotal API Routes: {len(d['routes'])}")
for r in d['routes']:
    methods = ",".join(r['methods'])
    print(f"  [{methods}] {r['path']}")
