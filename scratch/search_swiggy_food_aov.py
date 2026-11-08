import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, re

sources_dir = 'FoodIQ_Swiggy_Compact/FoodIQ_Swiggy_Research_Pack/sources/full_text'
for f in os.listdir(sources_dir):
    p = os.path.join(sources_dir, f)
    with open(p, 'r', encoding='utf-8') as file:
        text = file.read()
        matches = re.findall(r'.{0,50}(?:food delivery|food).{0,30}(?:AOV|average order value|order count).{0,50}', text, re.IGNORECASE)
        if matches:
            print(f"=== {f} ({len(matches)} matches) ===")
            for m in matches[:3]:
                print(f"  {m.strip().replace('\n', ' ')}")
