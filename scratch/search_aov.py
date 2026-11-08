with open("scratch/full_spec.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'aov', text, re.IGNORECASE)]
print(f"Total mentions of aov: {len(matches)}")
for idx in matches[:15]:
    snippet = text[max(0, idx-100):idx+200].replace('\n', ' ')
    print(f"- {snippet}")
