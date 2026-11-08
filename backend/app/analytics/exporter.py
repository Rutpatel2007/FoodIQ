"""
FoodIQ Analytics Artifact Exporter.
Executes the analytical engines and saves all standard processed CSV deliverables
into data/processed/ matching the project specification requirements.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

from backend.app.config import settings
from backend.app.analytics.repository import (
    build_and_materialize_analytical_tables,
    get_analytical_df,
    _get_sqlite_path
)
from backend.app.analytics.decomposition import compute_waterfall_decomposition, get_all_segment_decompositions
from backend.app.analytics.margin_bridge import compute_margin_bridge, get_all_margin_bridges
from backend.app.analytics.competitive_gaps import compute_competitive_gaps
from backend.app.analytics.leading_indicator import test_aov_leading_indicator
from backend.app.analytics.scenario_model import run_aov_scenario_model
from backend.app.analytics.guidance_scorer import score_management_guidance
from backend.app.analytics.network_productivity import compute_network_productivity, compute_network_comparison
from backend.app.analytics.unit_economics import compute_unit_economics


def export_all_analytical_artifacts(output_dir: str = "data/processed", db_path: Optional[str] = None) -> Dict[str, str]:
    """
    Generates and writes all Core Analytical query outputs and extended models to CSV files.
    """
    os.makedirs(output_dir, exist_ok=True)
    path = _get_sqlite_path(db_path)
    
    # Ensure tables are materialized
    wide_df = build_and_materialize_analytical_tables(path)
    
    exported_files = {}
    
    # -------------------------------------------------------------
    # 1. 01_nov_decomposition.csv & decomposition_summary.csv
    # -------------------------------------------------------------
    decomp_list = get_all_segment_decompositions(wide_df)
    decomp_df = pd.DataFrame(decomp_list)
    decomp_path = os.path.join(output_dir, "01_nov_decomposition.csv")
    decomp_df.to_csv(decomp_path, index=False)
    exported_files["01_nov_decomposition"] = decomp_path
    
    # Summary table
    summary_path = os.path.join(output_dir, "decomposition_summary.csv")
    decomp_df.to_csv(summary_path, index=False)
    exported_files["decomposition_summary"] = summary_path
    
    # -------------------------------------------------------------
    # 2. 02_margin_bridge.csv
    # -------------------------------------------------------------
    bridge_list = get_all_margin_bridges(wide_df)
    bridge_df = pd.DataFrame(bridge_list)
    bridge_path = os.path.join(output_dir, "02_margin_bridge.csv")
    bridge_df.to_csv(bridge_path, index=False)
    exported_files["02_margin_bridge"] = bridge_path
    
    # -------------------------------------------------------------
    # 3. 03_competitive_gaps.csv
    # -------------------------------------------------------------
    gaps_list = compute_competitive_gaps(df=wide_df)
    gaps_df = pd.DataFrame(gaps_list)
    gaps_path = os.path.join(output_dir, "03_competitive_gaps.csv")
    gaps_df.to_csv(gaps_path, index=False)
    exported_files["03_competitive_gaps"] = gaps_path
    
    # -------------------------------------------------------------
    # 4. 04_leading_indicator.csv & leading_indicator_results.csv
    # -------------------------------------------------------------
    lead_res = test_aov_leading_indicator(company="Swiggy", segment="QuickCommerce", df=wide_df)
    
    qc_s = wide_df[(wide_df['company'] == 'Swiggy') & (wide_df['segment'] == 'QuickCommerce')].sort_values(['fiscal_year', 'quarter_num'])
    lead_raw_df = pd.DataFrame({
        'quarter': qc_s['quarter'].values,
        'fiscal_year': qc_s['fiscal_year'].values,
        'quarter_num': qc_s['quarter_num'].values,
        'swiggy_aov_inr': qc_s['aov_inr'].values,
        'swiggy_cm_pct': qc_s['contribution_margin_pct'].values,
        'swiggy_cm_next_q': qc_s['contribution_margin_pct'].shift(-1).values
    })
    lead_raw_path = os.path.join(output_dir, "04_leading_indicator.csv")
    lead_raw_df.to_csv(lead_raw_path, index=False)
    exported_files["04_leading_indicator"] = lead_raw_path
    
    # Results summary table
    lead_results_df = pd.DataFrame(lead_res.get('results', []))
    lead_res_path = os.path.join(output_dir, "leading_indicator_results.csv")
    lead_results_df.to_csv(lead_res_path, index=False)
    exported_files["leading_indicator_results"] = lead_res_path
    
    # -------------------------------------------------------------
    # 5. 05_guidance_scorecard.csv & guidance_summary.csv
    # -------------------------------------------------------------
    guidance_data = score_management_guidance(path)
    guidance_df = pd.DataFrame(guidance_data.get('commitments', []))
    guidance_path = os.path.join(output_dir, "05_guidance_scorecard.csv")
    guidance_df.to_csv(guidance_path, index=False)
    exported_files["05_guidance_scorecard"] = guidance_path
    
    guidance_summary_df = pd.DataFrame([{
        'total_commitments': guidance_data['total_commitments'],
        'evaluable_commitments': guidance_data['evaluable_commitments'],
        'delivered_count': guidance_data['delivered_count'],
        'missed_count': guidance_data['missed_count'],
        'partially_delivered_count': guidance_data['partially_delivered_count'],
        'pending_count': guidance_data['pending_count'],
        'not_objectively_measurable_count': guidance_data['not_objectively_measurable_count'],
        'strict_delivery_rate_pct': guidance_data['strict_delivery_rate_pct'],
        'broad_delivery_rate_pct': guidance_data['broad_delivery_rate_pct'],
        'credibility_tier': guidance_data['credibility_tier'],
        'credibility_notes': guidance_data['credibility_notes']
    }])
    guidance_sum_path = os.path.join(output_dir, "guidance_summary.csv")
    guidance_summary_df.to_csv(guidance_sum_path, index=False)
    exported_files["guidance_summary"] = guidance_sum_path
    
    # -------------------------------------------------------------
    # 6. 06_scenario_model.csv & scenario_extended.csv
    # -------------------------------------------------------------
    scenario_res = run_aov_scenario_model(tier='baseline', df=wide_df)
    scenario_df = pd.DataFrame(scenario_res.get('scenarios', []))
    scenario_path = os.path.join(output_dir, "06_scenario_model.csv")
    scenario_df.to_csv(scenario_path, index=False)
    exported_files["06_scenario_model"] = scenario_path
    
    # Multi-tier sensitivity matrix
    matrix_df = pd.DataFrame(scenario_res.get('multi_tier_sensitivity_matrix', []))
    matrix_path = os.path.join(output_dir, "06_scenario_sensitivity_matrix.csv")
    matrix_df.to_csv(matrix_path, index=False)
    exported_files["06_scenario_sensitivity_matrix"] = matrix_path
    
    scenario_ext_df = scenario_df.copy()
    scenario_ext_df['base_aov_inr'] = scenario_res['base_aov_inr']
    scenario_ext_df['base_cm_pct'] = scenario_res['base_cm_pct']
    scenario_ext_df['calibrated_elasticity_bps_per_inr'] = scenario_res['calibrated_elasticity_bps_per_inr']
    scenario_ext_path = os.path.join(output_dir, "scenario_extended.csv")
    scenario_ext_df.to_csv(scenario_ext_path, index=False)
    exported_files["scenario_extended"] = scenario_ext_path
    
    # -------------------------------------------------------------
    # 7. network_productivity.csv
    # -------------------------------------------------------------
    net_prod = compute_network_productivity(wide_df)
    net_prod_df = pd.DataFrame(net_prod)
    net_prod_path = os.path.join(output_dir, "network_productivity.csv")
    net_prod_df.to_csv(net_prod_path, index=False)
    exported_files["network_productivity"] = net_prod_path

    # -------------------------------------------------------------
    # 8. unit_economics_summary.csv
    # -------------------------------------------------------------
    ue_list = []
    for comp in ['Eternal', 'Swiggy']:
        for seg in ['Food', 'QuickCommerce']:
            ue_list.extend(compute_unit_economics(comp, seg, df=wide_df))
    ue_df = pd.DataFrame(ue_list)
    ue_path = os.path.join(output_dir, "unit_economics_summary.csv")
    ue_df.to_csv(ue_path, index=False)
    exported_files["unit_economics_summary"] = ue_path

    return exported_files


if __name__ == "__main__":
    files = export_all_analytical_artifacts()
    print("Exported files:")
    for k, v in files.items():
        print(f"  {k:30} -> {v}")
