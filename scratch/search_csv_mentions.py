with open("scratch/full_spec.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "swiggy_raw" in l or "eternal_raw" in l or "csv" in l.lower():
        print(f"L{i+1}: {l.strip()[:100]}")
