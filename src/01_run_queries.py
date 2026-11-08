"""
FoodIQ — 01_run_queries.py
Executes the 6 core analytical SQL queries against foodiq.db and saves each result
as a CSV file under data/processed/.

This file contains zero business logic — it only executes SQL and saves output.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd
from backend.app.analytics.repository import build_and_materialize_analytical_tables, _get_sqlite_path

PROCESSED_DIR = "data/processed"


def run_all_sql_queries(db_path: str = "data/foodiq.db") -> None:
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    # Ensure wide tables are fresh
    build_and_materialize_analytical_tables(db_path)
    
    # -------------------------------------------------------------------------
    # Query 1 — GOV/NOV Decomposition (Price × Volume)
    # Answers: What fraction of each quarter's revenue change came from more orders vs. higher AOV?
    # -------------------------------------------------------------------------
    q1 = """
    WITH ordered AS (
        SELECT
            company, segment, quarter, fiscal_year, quarter_num,
            gov_cr, nov_cr, total_orders_mn, aov_inr,
            LAG(gov_cr) OVER w AS prev_gov,
            LAG(nov_cr) OVER w AS prev_nov,
            LAG(total_orders_mn) OVER w AS prev_orders,
            LAG(aov_inr) OVER w AS prev_aov
        FROM metrics
        WHERE segment IN ('QuickCommerce', 'Food')
        WINDOW w AS (PARTITION BY company, segment ORDER BY CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num)
    )
    SELECT
        company,
        segment,
        quarter,
        fiscal_year,
        quarter_num,
        COALESCE(gov_cr, nov_cr) AS current_topline_cr,
        COALESCE(prev_gov, prev_nov) AS prev_topline_cr,
        ROUND(COALESCE(gov_cr, nov_cr) - COALESCE(prev_gov, prev_nov), 2) AS delta_topline_cr,
        -- Volume effect: change in orders * prior AOV / 10
        ROUND((total_orders_mn - prev_orders) * prev_aov / 10.0, 2) AS volume_effect_cr,
        -- Price effect: change in AOV * current orders / 10
        ROUND((aov_inr - prev_aov) * total_orders_mn / 10.0, 2) AS price_effect_cr,
        -- Cross-term residual
        ROUND(
            (COALESCE(gov_cr, nov_cr) - COALESCE(prev_gov, prev_nov))
            - ((total_orders_mn - prev_orders) * prev_aov / 10.0)
            - ((aov_inr - prev_aov) * total_orders_mn / 10.0),
            2
        ) AS cross_term_cr
    FROM ordered
    WHERE prev_topline_cr IS NOT NULL
    ORDER BY company, segment, CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num;
    """
    df1 = pd.read_sql_query(q1, conn)
    p1 = os.path.join(PROCESSED_DIR, "01_nov_decomposition.csv")
    df1.to_csv(p1, index=False)
    print(f"Query 1 saved -> {p1} ({len(df1)} rows)")

    # -------------------------------------------------------------------------
    # Query 2 — Contribution Margin Bridge
    # Answers: What drove the change in contribution margin from one quarter to the next?
    # -------------------------------------------------------------------------
    q2 = """
    WITH ordered AS (
        SELECT
            company, segment, quarter, fiscal_year, quarter_num,
            gov_cr, nov_cr, adj_revenue_cr, contribution_margin_pct, take_rate_pct,
            LAG(COALESCE(gov_cr, nov_cr)) OVER w AS prev_topline,
            LAG(adj_revenue_cr) OVER w AS prev_adj_rev,
            LAG(contribution_margin_pct) OVER w AS prev_cm_pct,
            LAG(take_rate_pct) OVER w AS prev_take_rate
        FROM metrics
        WHERE segment IN ('Food', 'QuickCommerce')
        WINDOW w AS (PARTITION BY company, segment ORDER BY CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num)
    )
    SELECT
        company,
        segment,
        quarter,
        fiscal_year,
        quarter_num,
        ROUND((contribution_margin_pct - prev_cm_pct) * 100.0, 1) AS delta_cm_bps,
        -- Take rate contribution to margin change (in bps)
        ROUND((take_rate_pct - prev_take_rate) * 100.0, 1) AS take_rate_delta_bps,
        -- Volume leverage: same CM% on higher base
        ROUND(
            ((COALESCE(gov_cr, nov_cr) - prev_topline) / prev_topline) * prev_cm_pct * 100.0,
            1
        ) AS volume_leverage_bps,
        -- Residual = cost structure changes
        ROUND(
            ((contribution_margin_pct - prev_cm_pct) * 100.0)
            - ((take_rate_pct - prev_take_rate) * 100.0)
            - (((COALESCE(gov_cr, nov_cr) - prev_topline) / prev_topline) * prev_cm_pct * 100.0),
            1
        ) AS cost_structure_bps
    FROM ordered
    WHERE prev_cm_pct IS NOT NULL
    ORDER BY company, segment, CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num;
    """
    df2 = pd.read_sql_query(q2, conn)
    p2 = os.path.join(PROCESSED_DIR, "02_margin_bridge.csv")
    df2.to_csv(p2, index=False)
    print(f"Query 2 saved -> {p2} ({len(df2)} rows)")

    # -------------------------------------------------------------------------
    # Query 3 — Competitive Gap Tracker
    # Answers: Which metrics is each company winning on, and by how much, every quarter?
    # -------------------------------------------------------------------------
    q3 = """
    SELECT
        id,
        quarter,
        segment,
        metric,
        eternal_value,
        swiggy_value,
        gap_absolute,
        gap_pct,
        gap_direction
    FROM competitive_gaps
    ORDER BY segment, quarter, metric;
    """
    df3 = pd.read_sql_query(q3, conn)
    p3 = os.path.join(PROCESSED_DIR, "03_competitive_gaps.csv")
    df3.to_csv(p3, index=False)
    print(f"Query 3 saved -> {p3} ({len(df3)} rows)")

    # -------------------------------------------------------------------------
    # Query 4 — AOV Leading Indicator Test Series
    # Answers: Extracting the series for statistical lag testing
    # -------------------------------------------------------------------------
    q4 = """
    WITH swiggy_series AS (
        SELECT
            quarter, fiscal_year, quarter_num,
            aov_inr AS swiggy_aov,
            contribution_margin_pct AS swiggy_cm,
            LEAD(contribution_margin_pct, 1) OVER (ORDER BY CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num) AS swiggy_cm_next_q
        FROM metrics
        WHERE company = 'Swiggy' AND segment = 'QuickCommerce'
    )
    SELECT
        quarter,
        fiscal_year,
        quarter_num,
        swiggy_aov,
        swiggy_cm,
        swiggy_cm_next_q
    FROM swiggy_series
    ORDER BY CAST(REPLACE(fiscal_year, 'FY', '') AS INT), quarter_num;
    """
    df4 = pd.read_sql_query(q4, conn)
    p4 = os.path.join(PROCESSED_DIR, "04_leading_indicator.csv")
    df4.to_csv(p4, index=False)
    print(f"Query 4 saved -> {p4} ({len(df4)} rows)")

    # -------------------------------------------------------------------------
    # Query 5 — Guidance Accuracy Scorecard
    # Answers: When management said X would happen by quarter Y, did it?
    # -------------------------------------------------------------------------
    q5 = """
    SELECT
        id,
        company,
        issued_quarter,
        metric,
        guidance_text,
        target_quarter,
        target_value,
        actual_value,
        CASE
            WHEN met = 1 THEN 'Delivered'
            WHEN met = 0 THEN 'Missed'
            ELSE 'Pending'
        END AS outcome,
        CASE
            WHEN target_value IS NOT NULL AND actual_value IS NOT NULL AND target_value != 0
            THEN ROUND((actual_value - target_value) / ABS(target_value) * 100.0, 1)
            ELSE NULL
        END AS variance_pct
    FROM guidance_log
    ORDER BY company, issued_quarter;
    """
    df5 = pd.read_sql_query(q5, conn)
    p5 = os.path.join(PROCESSED_DIR, "05_guidance_scorecard.csv")
    df5.to_csv(p5, index=False)
    print(f"Query 5 saved -> {p5} ({len(df5)} rows)")

    # -------------------------------------------------------------------------
    # Query 6 — Scenario Model: What Would It Take to Close the Gap?
    # -------------------------------------------------------------------------
    # Pulled from base actuals in latest quarter
    q6 = """
    WITH base AS (
        SELECT
            company, quarter, aov_inr, gov_cr, total_orders_mn, contribution_margin_pct
        FROM metrics
        WHERE segment = 'QuickCommerce' AND quarter = 'Q2FY27' AND company = 'Swiggy'
    )
    SELECT
        s.company,
        sc.inc AS aov_improvement_inr,
        s.aov_inr + sc.inc AS projected_aov,
        ROUND((s.total_orders_mn * (s.aov_inr + sc.inc)) / 10.0, 1) AS projected_gov_cr,
        ROUND(s.contribution_margin_pct + (sc.inc * 0.01), 2) AS projected_cm_pct,
        0.0 AS break_even_target_cm_pct,
        ROUND((s.contribution_margin_pct + (sc.inc * 0.01)) * 100.0, 1) AS remaining_gap_bps
    FROM base s
    CROSS JOIN (
        SELECT 0 AS inc UNION ALL SELECT 20 UNION ALL SELECT 40 UNION ALL
        SELECT 60 UNION ALL SELECT 80 UNION ALL SELECT 100
    ) sc;
    """
    df6 = pd.read_sql_query(q6, conn)
    p6 = os.path.join(PROCESSED_DIR, "06_scenario_model.csv")
    df6.to_csv(p6, index=False)
    print(f"Query 6 saved -> {p6} ({len(df6)} rows)")

    conn.close()


if __name__ == "__main__":
    run_all_sql_queries()
