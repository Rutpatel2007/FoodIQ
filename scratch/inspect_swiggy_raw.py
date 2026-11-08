import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df = pd.read_csv('FoodIQ_Swiggy_Compact/FoodIQ_Swiggy_Research_Pack/data/raw/swiggy_metrics_long.csv')
print(f"Total rows: {len(df)}")
print(f"Segments: {df['segment'].unique()}")
print(f"Metrics: {df['metric_name'].unique()}")
print(f"Quarters: {df['quarter'].unique()}")
