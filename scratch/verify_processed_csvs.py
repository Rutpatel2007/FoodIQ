import os
import pandas as pd

processed_dir = "data/processed"
for f in sorted(os.listdir(processed_dir)):
    p = os.path.join(processed_dir, f)
    if f.endswith('.csv'):
        df = pd.read_csv(p)
        print(f"{f:30} | {len(df):4} rows | cols: {list(df.columns)[:5]}...")
