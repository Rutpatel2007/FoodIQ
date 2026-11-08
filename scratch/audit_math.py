import sys, sqlite3
sys.stdout.reconfigure(encoding="utf-8")
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd

DB_PATH = r"c:\Users\Rut Patel\OneDrive\Documents\GitHub\FoodIQ\data\foodiq.db"
conn = sqlite3.connect(DB_PATH)

print("=== 1. SWIGGY QUICK COMMERCE: GOV = (Orders * AOV) / 10 ===")
cursor = conn.cursor()
cursor.execute("""
    SELECT 
        o.fiscal_year, o.fiscal_quarter,
        MAX(CASE WHEN o.metric_id = 'swiggy_total_orders_mn' THEN o.value END) as orders_mn,
        MAX(CASE WHEN o.metric_id = 'swiggy_aov_inr' THEN o.value END) as aov_inr,
        MAX(CASE WHEN o.metric_id = 'swiggy_gov_cr' THEN o.value END) as gov_cr
    FROM metric_observations o
    WHERE o.segment_id = 'SWIGGY_QUICK_COMMERCE'
    GROUP BY o.fiscal_year, o.fiscal_quarter
    ORDER BY o.fiscal_year, o.fiscal_quarter;
""")
qcomm_math = cursor.fetchall()
for fy, fq, ord_mn, aov, gov in qcomm_math:
    if ord_mn and aov and gov:
        d_ord = Decimal(str(ord_mn))
        d_aov = Decimal(str(aov))
        d_gov = Decimal(str(gov))
        recalc_gov = (d_ord * d_aov) / Decimal("10")
        diff = abs(recalc_gov - d_gov)
        pct_diff = (diff / d_gov) * Decimal("100")
        passed = diff <= Decimal("5.0") or pct_diff <= Decimal("0.5") # rounding tolerance
        print(f"[{fq}{fy}] Orders: {ord_mn}m | AOV: INR {aov} | Disclosed GOV: INR {gov} | Recalc GOV: INR {recalc_gov:.2f} | Diff: INR {diff:.2f} ({pct_diff:.2f}%) | {'PASS' if passed else 'FAIL'}")

print("\n=== 2. SWIGGY QUICK COMMERCE: NOV / GOV RATIO ===")
cursor.execute("""
    SELECT 
        o.fiscal_year, o.fiscal_quarter,
        MAX(CASE WHEN o.metric_id = 'swiggy_nov_cr' THEN o.value END) as nov_cr,
        MAX(CASE WHEN o.metric_id = 'swiggy_gov_cr' THEN o.value END) as gov_cr,
        MAX(CASE WHEN o.metric_id = 'swiggy_nov_pct_of_gov' THEN o.value END) as reported_pct
    FROM metric_observations o
    WHERE o.segment_id = 'SWIGGY_QUICK_COMMERCE'
    GROUP BY o.fiscal_year, o.fiscal_quarter
    ORDER BY o.fiscal_year, o.fiscal_quarter;
""")
for fy, fq, nov, gov, rep_pct in cursor.fetchall():
    if nov and gov and rep_pct:
        d_nov = Decimal(str(nov))
        d_gov = Decimal(str(gov))
        d_rep = Decimal(str(rep_pct))
        recalc_pct = (d_nov / d_gov) * Decimal("100")
        diff = abs(recalc_pct - d_rep)
        passed = diff <= Decimal("1.0") # whole-percentage rounding tolerance in disclosure
        print(f"[{fq}{fy}] NOV: INR {nov} | GOV: INR {gov} | Reported %: {rep_pct}% | Recalc %: {recalc_pct:.2f}% | Diff: {diff:.2f}% | {'PASS' if passed else 'FAIL'}")

print("\n=== 3. ETERNAL B2C NOV SUM: Food NOV + QComm NOV + Going-out NOV == B2C NOV ===")
cursor.execute("""
    SELECT 
        o.fiscal_year, o.fiscal_quarter,
        MAX(CASE WHEN o.metric_id = 'eternal_food_nov' THEN o.value END) as food_nov,
        MAX(CASE WHEN o.metric_id = 'eternal_qcomm_nov' THEN o.value END) as qcomm_nov,
        MAX(CASE WHEN o.metric_id = 'eternal_going_out_nov' THEN o.value END) as going_out_nov,
        MAX(CASE WHEN o.metric_id = 'eternal_b2c_nov' THEN o.value END) as b2c_nov
    FROM metric_observations o
    WHERE o.company_id = 'ETERNAL'
    GROUP BY o.fiscal_year, o.fiscal_quarter
    ORDER BY o.fiscal_year, o.fiscal_quarter;
""")
for fy, fq, f_nov, q_nov, g_nov, b2c in cursor.fetchall():
    if f_nov and q_nov and g_nov and b2c:
        d_f = Decimal(str(f_nov))
        d_q = Decimal(str(q_nov))
        d_g = Decimal(str(g_nov))
        d_b2c = Decimal(str(b2c))
        recalc_sum = d_f + d_q + d_g
        diff = abs(recalc_sum - d_b2c)
        passed = diff <= Decimal("1.0") # rounding tolerance
        print(f"[{fq}{fy}] Food: INR {f_nov} + QComm: INR {q_nov} + GoingOut: INR {g_nov} = Recalc: INR {recalc_sum} | Disclosed B2C: INR {b2c} | Diff: INR {diff} | {'PASS' if passed else 'FAIL'}")

conn.close()
