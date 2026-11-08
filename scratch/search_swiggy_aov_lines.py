import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, re

sources_dir = 'FoodIQ_Swiggy_Compact/FoodIQ_Swiggy_Research_Pack/sources/full_text'
for f in os.listdir(sources_dir):
    p = os.path.join(sources_dir, f)
    with open(p, 'r', encoding='utf-8') as file:
        text = file.read()
        lines = text.split('\n')
        for i, l in enumerate(lines):
            if 'AOV' in l:
                print(f"{f} L{i+1}: {l.strip()[:100]}")
