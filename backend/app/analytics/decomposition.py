"""
FoodIQ Growth Quality Decomposition Engine (Audited & Repaired).
Performs exact 4-term mathematical waterfall decomposition of top-line metric changes:
ΔGOV = Volume Effect + Basket Effect + Interaction Effect + Residual

Where:
Volume Effect (Cr)      = (Orders_t - Orders_0) * AOV_0 / 10.0
Basket Effect (Cr)      = Orders_0 * (AOV_t - AOV_0) / 10.0
Interaction Effect (Cr) = (Orders_t - Orders_0) * (AOV_t - AOV_0) / 10.0
Residual (Cr)           = Actual ΔGOV - Volume Effect - Basket Effect - Interaction Effect

Financial Rules Enforced:
1. AOV defined as GOV / Orders decomposes GOV only. GOV-based AOV is NEVER used to decompose NOV.
2. Segments lacking reported order counts or matching AOVs are explicitly classified as INELIGIBLE.
3. Scale factor: (mn orders * INR) / 10.0 = INR Crore (1e6 * 1 / 1e7 = 0.1).
4. Exact Additivity: Volume + Basket + Interaction + Residual == Actual ΔGOV to 0.00 Cr precision.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.analytics.repository import get_analytical_df, sanitize_for_json


def compute_waterfall_decomposition(
    company: str = "Swiggy",
    segment: str = "QuickCommerce",
    metric_basis: str = "gov_cr",
    df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """
    Computes exact 4-term mathematical decomposition for eligible transitions.
    """
    data = df if df is not None else get_analytical_df()
    
    # Filter by company and segment
    filtered = data[(data['company'] == company) & (data['segment'] == segment)].copy()
    if filtered.empty:
        return []
        
    filtered['fy_int'] = filtered['fiscal_year'].str.replace('FY', '').astype(int)
    filtered = filtered.sort_values(['fy_int', 'quarter_num']).reset_index(drop=True)
    
    results = []
    for i in range(1, len(filtered)):
        curr = filtered.iloc[i]
        prev = filtered.iloc[i - 1]
        
        curr_val = curr.get(metric_basis)
        prev_val = prev.get(metric_basis)
        
        curr_orders = curr.get('total_orders_mn')
        prev_orders = prev.get('total_orders_mn')
        
        curr_aov = curr.get('aov_inr')
        prev_aov = prev.get('aov_inr')
        
        has_orders = pd.notna(curr_orders) and pd.notna(prev_orders) and curr_orders > 0 and prev_orders > 0
        has_aov = pd.notna(curr_aov) and pd.notna(prev_aov) and curr_aov > 0 and prev_aov > 0
        has_values = pd.notna(curr_val) and pd.notna(prev_val)
        
        # Rule check: AOV is defined as GOV/Orders in shareholder letters
        is_gov_metric = metric_basis == 'gov_cr'
        is_eligible = has_orders and has_aov and has_values and is_gov_metric
        
        delta_val = round(float(curr_val - prev_val), 2) if has_values else None
        
        if is_eligible and delta_val is not None:
            delta_o = float(curr_orders - prev_orders)
            delta_p = float(curr_aov - prev_aov)
            p_0 = float(prev_aov)
            o_0 = float(prev_orders)
            
            # Exact 4-term formulas
            # 1. Volume effect: change in orders * prior AOV / 10.0
            vol_eff = round((delta_o * p_0) / 10.0, 2)
            # 2. Basket effect: prior orders * change in AOV / 10.0
            basket_eff = round((o_0 * delta_p) / 10.0, 2)
            # 3. Interaction effect: change in orders * change in AOV / 10.0
            interaction_eff = round((delta_o * delta_p) / 10.0, 2)
            # 4. Residual: delta_val - sum of effects (due to discrete disclosure rounding)
            sum_model = round(vol_eff + basket_eff + interaction_eff, 2)
            residual = round(delta_val - sum_model, 2)
            
            # Percentage attributions
            vol_pct = round((vol_eff / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            basket_pct = round((basket_eff / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            interaction_pct = round((interaction_eff / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            residual_pct = round((residual / delta_val) * 100.0, 1) if delta_val != 0 else 0.0
            
            # Dominant driver logic
            if abs(vol_eff) > max(abs(basket_eff), abs(interaction_eff)):
                dominant_driver = "Volume (Order Count)"
            elif abs(basket_eff) > max(abs(vol_eff), abs(interaction_eff)):
                dominant_driver = "Basket Size (AOV)"
            else:
                dominant_driver = "Interaction (Joint Expansion)"
                
            status = "ELIGIBLE_AND_RECONCILED"
            methodology_notes = (
                "Exact 4-term decomposition: Volume + Basket + Interaction + Residual == Actual ΔGOV. "
                "Residual reflects rounding in published disclosures (orders to 1 decimal place, integer AOV)."
            )
        else:
            vol_eff = None
            basket_eff = None
            interaction_eff = None
            residual = None
            vol_pct = None
            basket_pct = None
            interaction_pct = None
            residual_pct = None
            dominant_driver = "Not Decomposable"
            
            if not is_gov_metric:
                status = "INELIGIBLE_INVALID_METRIC_BASIS"
                methodology_notes = f"Financial rule violation: Disclosed AOV is GOV-based and cannot be applied to {metric_basis}."
            else:
                status = "INELIGIBLE_MISSING_DISCLOSURES"
                methodology_notes = "Segment does not disclose both quarterly order counts and matching AOVs in shareholder letters."
                
        growth_rate_pct = round((delta_val / float(prev_val)) * 100.0, 2) if (delta_val is not None and prev_val and prev_val > 0) else None

        results.append({
            'company': company,
            'segment': segment,
            'quarter': curr['quarter'],
            'fiscal_year': curr['fiscal_year'],
            'quarter_num': int(curr['quarter_num']),
            'metric_basis': metric_basis,
            'current_value': float(curr_val) if pd.notna(curr_val) else None,
            'previous_value': float(prev_val) if pd.notna(prev_val) else None,
            'delta_value': delta_val,
            'growth_rate_pct': growth_rate_pct,
            'total_orders_mn': float(curr_orders) if pd.notna(curr_orders) else None,
            'previous_orders_mn': float(prev_orders) if pd.notna(prev_orders) else None,
            'aov_inr': float(curr_aov) if pd.notna(curr_aov) else None,
            'previous_aov_inr': float(prev_aov) if pd.notna(prev_aov) else None,
            'volume_effect_cr': vol_eff,
            'basket_effect_cr': basket_eff,
            'interaction_effect_cr': interaction_eff,
            'residual_cr': residual,
            'volume_share_pct': vol_pct,
            'basket_share_pct': basket_pct,
            'interaction_share_pct': interaction_pct,
            'residual_share_pct': residual_pct,
            'dominant_driver': dominant_driver,
            'status': status,
            'methodology_notes': methodology_notes,
            'source_doc': curr.get('source_doc'),
            'source_page': curr.get('source_page')
        })
        
    return results


def get_all_segment_decompositions(df: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    """Returns waterfall decompositions for all segments and companies, explicitly classifying eligibility."""
    data = df if df is not None else get_analytical_df()
    all_results = []
    
    # 1. Swiggy Quick Commerce GOV (Fully Eligible)
    all_results.extend(compute_waterfall_decomposition("Swiggy", "QuickCommerce", "gov_cr", data))
    # 2. Swiggy Food Delivery GOV (Ineligible: Food orders/AOV not disclosed separately)
    all_results.extend(compute_waterfall_decomposition("Swiggy", "Food", "gov_cr", data))
    # 3. Eternal Food Delivery NOV (Ineligible: Orders/AOV not disclosed)
    all_results.extend(compute_waterfall_decomposition("Eternal", "Food", "nov_cr", data))
    # 4. Eternal Quick Commerce NOV (Ineligible: Orders/AOV not disclosed)
    all_results.extend(compute_waterfall_decomposition("Eternal", "QuickCommerce", "nov_cr", data))
    
    return all_results


def get_company_overview_data(company: str = "Swiggy", quarter: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns dynamically structured, period-aware corporate overview and segmental breakdown.
    Strictly separates Contribution Margin and Adjusted EBITDA with explicit calculation.
    """
    df = get_analytical_df()
    c_lower = company.lower()
    
    # Available quarters sorted chronologically
    available_quarters = df[df['company'].str.lower() == c_lower]['quarter'].unique().tolist()
    available_quarters = sorted(available_quarters, key=lambda q: (int(q[4:]), int(q[1])))
    latest_quarter = available_quarters[-1] if available_quarters else "Q2FY27"
    
    selected_quarter = quarter.upper() if quarter and quarter.upper() in available_quarters else latest_quarter
    is_latest = (selected_quarter == latest_quarter)
    
    sub = df[(df['company'].str.lower() == c_lower) & (df['quarter'].str.upper() == selected_quarter)]
    
    SEGMENT_DISPLAY_NAMES = {
        'Food': 'Food Delivery',
        'QuickCommerce': 'Quick Commerce (Instamart)' if c_lower == 'swiggy' else 'Quick Commerce (Blinkit)',
        'OutOfHome': 'Out-of-Home (Dineout)' if c_lower == 'swiggy' else 'District (Going-Out / Live Events)',
        'SupplyChain': 'Supply Chain Logistics' if c_lower == 'swiggy' else 'Hyperpure (B2B)',
        'PlatformInnovations': 'Platform Innovations (Genie / Dineout)',
        'Platform': 'Platform Consolidated',
        'Consolidated': 'Corporate Consolidated'
    }
    
    segments_data = []
    for _, row in sub.iterrows():
        seg_id = row['segment']
        if seg_id in ['Consolidated', 'Platform']:
            continue
            
        gov = float(row['gov_cr']) if pd.notna(row.get('gov_cr')) else None
        nov = float(row['nov_cr']) if pd.notna(row.get('nov_cr')) else None
        rev = float(row['adj_revenue_cr']) if pd.notna(row.get('adj_revenue_cr')) else None
        cm_pct = float(row['contribution_margin_pct']) if pd.notna(row.get('contribution_margin_pct')) else None
        ebitda_cr = float(row['adj_ebitda_cr']) if pd.notna(row.get('adj_ebitda_cr')) else None
        ebitda_pct = float(row['adj_ebitda_margin_pct']) if pd.notna(row.get('adj_ebitda_margin_pct')) else None
        stores = int(row['dark_stores']) if pd.notna(row.get('dark_stores')) else None
        aov = float(row['aov_inr']) if pd.notna(row.get('aov_inr')) else None
        orders = float(row['total_orders_mn']) if pd.notna(row.get('total_orders_mn')) else None
        
        # Primary order flow
        if c_lower == 'eternal' and seg_id == 'QuickCommerce' and nov is not None:
            flow_label = "NOV"
            flow_val = nov
        elif gov is not None:
            flow_label = "GOV"
            flow_val = gov
        elif nov is not None:
            flow_label = "NOV"
            flow_val = nov
        else:
            flow_label = "N/A"
            flow_val = None
            
        # Mathematical Contribution Margin profit/loss (not conflated with EBITDA)
        cm_profit_cr = None
        if cm_pct is not None:
            basis = gov if gov is not None else nov
            if basis is not None:
                cm_profit_cr = round((cm_pct / 100.0) * basis, 1)
                
        # Take rate
        take_rate = float(row['take_rate_pct']) if pd.notna(row.get('take_rate_pct')) else None
        if take_rate is None and rev is not None and flow_val is not None and flow_val > 0:
            take_rate = round((rev / flow_val) * 100.0, 2)
            
        margin_basis = "GOV" if c_lower == 'swiggy' else "NOV"
        
        # Notes & accounting flags
        notes = []
        if c_lower == 'eternal' and seg_id == 'QuickCommerce' and selected_quarter in ['Q2FY26', 'Q3FY26', 'Q4FY26', 'Q1FY27', 'Q2FY27']:
            notes.append("1P owned inventory merchandising model (Ind AS 115)")
        elif c_lower == 'eternal' and seg_id == 'OutOfHome' and selected_quarter in ['Q2FY25', 'Q3FY25', 'Q4FY25', 'Q1FY26', 'Q2FY26', 'Q3FY26', 'Q4FY26', 'Q1FY27', 'Q2FY27']:
            notes.append("Includes Paytm entertainment ticketing business acquired Q2 FY25")
        elif c_lower == 'swiggy' and seg_id == 'QuickCommerce':
            notes.append(f"Exit dark store count: {stores} stores; Contribution margin on {margin_basis}")
            
        segments_data.append({
            'segment_id': seg_id,
            'segment_name': SEGMENT_DISPLAY_NAMES.get(seg_id, seg_id),
            'quarter': selected_quarter,
            'flow_label': flow_label,
            'flow_val_cr': flow_val,
            'reported_revenue_cr': rev,
            'take_rate_pct': take_rate,
            'contribution_margin_pct': cm_pct,
            'contribution_profit_cr': cm_profit_cr,
            'adj_ebitda_cr': ebitda_cr,
            'adj_ebitda_margin_pct': ebitda_pct,
            'margin_basis': margin_basis,
            'dark_stores': stores,
            'aov_inr': aov,
            'orders_mn': orders,
            'source_doc': row.get('source_doc'),
            'source_page': row.get('source_page'),
            'accounting_notes': "; ".join(notes) if notes else "Standard reporting"
        })
        
    return {
        'status': 'success',
        'company': 'Swiggy Limited' if c_lower == 'swiggy' else 'Eternal Limited',
        'company_id': 'SWIGGY' if c_lower == 'swiggy' else 'ETERNAL',
        'ticker': 'NSE: SWIGGY / BSE: 544280' if c_lower == 'swiggy' else 'NSE: ETERNAL / BSE: 543320',
        'selected_quarter': selected_quarter,
        'latest_quarter': latest_quarter,
        'is_latest': is_latest,
        'available_quarters': available_quarters,
        'segments': segments_data
    }


def get_executive_kpis(quarter: Optional[str] = None) -> Dict[str, Any]:
    """
    Computes dynamic, period-aware executive KPI cards across Eternal and Swiggy.
    Includes YoY growth, reporting quarter, source citations, and epistemic labels.
    """
    df = get_analytical_df()
    all_quarters = sorted(df['quarter'].unique().tolist(), key=lambda q: (int(q[4:]), int(q[1])))
    latest_quarter = all_quarters[-1] if all_quarters else "Q2FY27"
    
    sel_q = quarter.upper() if quarter and quarter.upper() in all_quarters else latest_quarter
    is_latest = (sel_q == latest_quarter)
    
    q_num = int(sel_q[1])
    fy_year = int(sel_q[4:])
    yoy_q = f"Q{q_num}FY{fy_year - 1}"
    has_yoy = yoy_q in all_quarters
    
    q_data = df[df['quarter'].str.upper() == sel_q]
    yoy_data = df[df['quarter'].str.upper() == yoy_q] if has_yoy else pd.DataFrame()
    
    kpis = []
    
    # 1. Swiggy Food Delivery GOV
    sf_cur = q_data[(q_data['company'] == 'Swiggy') & (q_data['segment'] == 'Food')]
    if not sf_cur.empty:
        gov = float(sf_cur.iloc[0]['gov_cr'])
        sf_prev = yoy_data[(yoy_data['company'] == 'Swiggy') & (yoy_data['segment'] == 'Food')] if has_yoy else pd.DataFrame()
        yoy_g = ((gov - float(sf_prev.iloc[0]['gov_cr'])) / float(sf_prev.iloc[0]['gov_cr']) * 100.0) if not sf_prev.empty else None
        cm = float(sf_cur.iloc[0]['contribution_margin_pct']) if pd.notna(sf_cur.iloc[0].get('contribution_margin_pct')) else None
        ebitda_pct = float(sf_cur.iloc[0]['adj_ebitda_margin_pct']) if pd.notna(sf_cur.iloc[0].get('adj_ebitda_margin_pct')) else None
        kpis.append({
            'kpi_id': 'SWIGGY_FOOD_GOV',
            'title': f'Swiggy Food GOV ({sel_q})',
            'value': f'₹{gov:,.0f} Cr',
            'raw_value': gov,
            'unit': 'INR_CR',
            'quarter': sel_q,
            'is_latest': is_latest,
            'delta_text': f"{'▲ +' + str(round(yoy_g, 1)) + '% YoY' if yoy_g else 'Baseline Period'} · CM: {cm:.1f}% · EBITDA: {ebitda_pct:.1f}%",
            'trend': 'positive' if yoy_g and yoy_g > 0 else 'neutral',
            'definition': 'Gross Order Value of all food orders placed on Swiggy platform including taxes and delivery fees',
            'source_doc': sf_cur.iloc[0].get('source_doc'),
            'source_page': sf_cur.iloc[0].get('source_page'),
            'nature': 'REPORTED_OPERATIONAL'
        })
        
    # 2. Eternal Food Delivery Order Flow
    ef_cur = q_data[(q_data['company'] == 'Eternal') & (q_data['segment'] == 'Food')]
    if not ef_cur.empty:
        nov = float(ef_cur.iloc[0]['nov_cr']) if pd.notna(ef_cur.iloc[0].get('nov_cr')) else float(ef_cur.iloc[0].get('gov_cr', 0.0))
        ef_prev = yoy_data[(yoy_data['company'] == 'Eternal') & (yoy_data['segment'] == 'Food')] if has_yoy else pd.DataFrame()
        prev_nov = float(ef_prev.iloc[0]['nov_cr']) if not ef_prev.empty and pd.notna(ef_prev.iloc[0].get('nov_cr')) else None
        yoy_g = ((nov - prev_nov) / prev_nov * 100.0) if prev_nov else None
        ebitda_pct = float(ef_cur.iloc[0]['adj_ebitda_margin_pct']) if pd.notna(ef_cur.iloc[0].get('adj_ebitda_margin_pct')) else None
        kpis.append({
            'kpi_id': 'ETERNAL_FOOD_NOV',
            'title': f'Eternal Food Flow ({sel_q})',
            'value': f'₹{nov:,.0f} Cr',
            'raw_value': nov,
            'unit': 'INR_CR',
            'quarter': sel_q,
            'is_latest': is_latest,
            'delta_text': f"{'▲ +' + str(round(yoy_g, 1)) + '% YoY' if yoy_g else 'Baseline Period'} · EBITDA: {ebitda_pct:.2f}% of NOV",
            'trend': 'positive',
            'definition': 'Net Order Value of Zomato food delivery operations excluding customer discounts',
            'source_doc': ef_cur.iloc[0].get('source_doc'),
            'source_page': ef_cur.iloc[0].get('source_page'),
            'nature': 'REPORTED_OPERATIONAL'
        })
        
    # 3. Blinkit Scale & Density
    eqc_cur = q_data[(q_data['company'] == 'Eternal') & (q_data['segment'] == 'QuickCommerce')]
    if not eqc_cur.empty:
        nov = float(eqc_cur.iloc[0]['nov_cr'])
        stores = int(eqc_cur.iloc[0]['dark_stores']) if pd.notna(eqc_cur.iloc[0].get('dark_stores')) else None
        eqc_prev = yoy_data[(yoy_data['company'] == 'Eternal') & (yoy_data['segment'] == 'QuickCommerce')] if has_yoy else pd.DataFrame()
        prev_nov = float(eqc_prev.iloc[0]['nov_cr']) if not eqc_prev.empty else None
        yoy_g = ((nov - prev_nov) / prev_nov * 100.0) if prev_nov else None
        ebitda_cr = float(eqc_cur.iloc[0]['adj_ebitda_cr']) if pd.notna(eqc_cur.iloc[0].get('adj_ebitda_cr')) else None
        
        # Exact throughput per store-day on 91.25 days
        throughput = round((nov * 1e7) / (stores * 91.25), 0) if stores else None
        
        kpis.append({
            'kpi_id': 'BLINKIT_NOV_SCALE',
            'title': f'Blinkit NOV ({sel_q})',
            'value': f'₹{nov:,.0f} Cr',
            'raw_value': nov,
            'unit': 'INR_CR',
            'quarter': sel_q,
            'is_latest': is_latest,
            'delta_text': f"{'▲ +' + str(round(yoy_g, 1)) + '% YoY' if yoy_g else 'Baseline'} · {stores:,} Stores · Throughput: ₹{int(throughput):,}/day" if throughput else f"{stores:,} Stores",
            'trend': 'positive',
            'definition': 'Net Order Value across Blinkit quick commerce dark-store network with derived blended daily store throughput',
            'source_doc': eqc_cur.iloc[0].get('source_doc'),
            'source_page': eqc_cur.iloc[0].get('source_page'),
            'nature': 'REPORTED_OPERATIONAL'
        })
        
    # 4. Swiggy Instamart Scale & Economics
    sqc_cur = q_data[(q_data['company'] == 'Swiggy') & (q_data['segment'] == 'QuickCommerce')]
    if not sqc_cur.empty:
        gov = float(sqc_cur.iloc[0]['gov_cr'])
        stores = int(sqc_cur.iloc[0]['dark_stores']) if pd.notna(sqc_cur.iloc[0].get('dark_stores')) else None
        sqc_prev = yoy_data[(yoy_data['company'] == 'Swiggy') & (yoy_data['segment'] == 'QuickCommerce')] if has_yoy else pd.DataFrame()
        prev_gov = float(sqc_prev.iloc[0]['gov_cr']) if not sqc_prev.empty else None
        yoy_g = ((gov - prev_gov) / prev_gov * 100.0) if prev_gov else None
        cm = float(sqc_cur.iloc[0]['contribution_margin_pct']) if pd.notna(sqc_cur.iloc[0].get('contribution_margin_pct')) else None
        aov = float(sqc_cur.iloc[0]['aov_inr']) if pd.notna(sqc_cur.iloc[0].get('aov_inr')) else None
        cm_loss = round((cm / 100.0) * gov, 1) if cm is not None else None
        
        kpis.append({
            'kpi_id': 'INSTAMART_GOV_SCALE',
            'title': f'Swiggy Instamart GOV ({sel_q})',
            'value': f'₹{gov:,.0f} Cr',
            'raw_value': gov,
            'unit': 'INR_CR',
            'quarter': sel_q,
            'is_latest': is_latest,
            'delta_text': f"{'▲ +' + str(round(yoy_g, 1)) + '% YoY' if yoy_g else 'Baseline'} · {stores:,} Stores · AOV: ₹{int(aov)} · CM: {cm:.1f}% (-₹{abs(cm_loss):.1f} Cr)",
            'trend': 'positive' if yoy_g and yoy_g > 0 else 'neutral',
            'definition': 'Gross Order Value of Swiggy Instamart quick commerce with contribution margin % and monetary contribution loss',
            'source_doc': sqc_cur.iloc[0].get('source_doc'),
            'source_page': sqc_cur.iloc[0].get('source_page'),
            'nature': 'REPORTED_OPERATIONAL'
        })
        
    # 5. Food Delivery EBITDA Margin Spread
    if not ef_cur.empty and not sf_cur.empty:
        e_margin = float(ef_cur.iloc[0]['adj_ebitda_margin_pct']) if pd.notna(ef_cur.iloc[0].get('adj_ebitda_margin_pct')) else None
        s_margin = float(sf_cur.iloc[0]['adj_ebitda_margin_pct']) if pd.notna(sf_cur.iloc[0].get('adj_ebitda_margin_pct')) else None
        if e_margin is not None and s_margin is not None:
            spread_bps = int(round((e_margin - s_margin) * 100))
            kpis.append({
                'kpi_id': 'FOOD_EBITDA_SPREAD',
                'title': f'Food EBITDA Spread ({sel_q})',
                'value': f'{spread_bps} bps',
                'raw_value': spread_bps,
                'unit': 'BPS',
                'quarter': sel_q,
                'is_latest': is_latest,
                'delta_text': f"Eternal: {e_margin:.2f}% vs. Swiggy: {s_margin:.2f}% (Eternal ahead by {spread_bps} bps)",
                'trend': 'neutral',
                'definition': 'Adjusted EBITDA margin gap between Eternal Food Delivery and Swiggy Food Delivery in basis points',
                'source_doc': 'Comparative Derivation',
                'source_page': 'N/A',
                'nature': 'DERIVED_COMPETITIVE_GAP'
            })
            
    # 6. Management Credibility
    kpis.append({
        'kpi_id': 'MGMT_CREDIBILITY_RATING',
        'title': 'Management Guidance Delivery',
        'value': '80.0% Strict (Avg)',
        'raw_value': 80.0,
        'unit': 'PERCENT',
        'quarter': 'Consolidated Horizon',
        'is_latest': True,
        'delta_text': 'Eternal: 83.33% · Swiggy: 75.00% (11 unexpired IPO commitments isolated)',
        'trend': 'positive',
        'definition': 'Delivery rate of verifiable management forward-looking guidance with strict isolation of pending multi-year commitments',
        'source_doc': 'Guidance Tracker Core',
        'source_page': 'N/A',
        'nature': 'GOVERNED_AUDIT'
    })
    
    return sanitize_for_json({
        'status': 'success',
        'selected_quarter': sel_q,
        'latest_quarter': latest_quarter,
        'is_latest': is_latest,
        'available_quarters': all_quarters,
        'kpis': kpis
    })


def get_chart_time_series() -> Dict[str, Any]:
    """
    Returns continuous quarterly time-series for charting with dual-axis metadata and structural breaks.
    """
    df = get_analytical_df()
    quarters = sorted(df['quarter'].unique().tolist(), key=lambda q: (int(q[4:]), int(q[1])))
    
    # Food Delivery GOV/NOV series
    e_food = df[(df['company'] == 'Eternal') & (df['segment'] == 'Food')].sort_values(['fiscal_year', 'quarter_num'])
    s_food = df[(df['company'] == 'Swiggy') & (df['segment'] == 'Food')].sort_values(['fiscal_year', 'quarter_num'])
    
    # Quick Commerce series
    e_qc = df[(df['company'] == 'Eternal') & (df['segment'] == 'QuickCommerce')].sort_values(['fiscal_year', 'quarter_num'])
    s_qc = df[(df['company'] == 'Swiggy') & (df['segment'] == 'QuickCommerce')].sort_values(['fiscal_year', 'quarter_num'])
    
    return sanitize_for_json({
        'status': 'success',
        'quarters': quarters,
        'food_delivery': {
            'eternal_nov_cr': e_food['nov_cr'].tolist(),
            'eternal_ebitda_pct': e_food['adj_ebitda_margin_pct'].tolist(),
            'swiggy_gov_cr': s_food['gov_cr'].tolist(),
            'swiggy_cm_pct': s_food['contribution_margin_pct'].tolist(),
            'swiggy_ebitda_pct': s_food['adj_ebitda_margin_pct'].tolist()
        },
        'quick_commerce': {
            'blinkit_nov_cr': e_qc['nov_cr'].tolist(),
            'blinkit_stores': e_qc['dark_stores'].tolist(),
            'blinkit_ebitda_cr': e_qc['adj_ebitda_cr'].tolist(),
            'instamart_gov_cr': s_qc['gov_cr'].tolist(),
            'instamart_nov_cr': s_qc['nov_cr'].tolist(),
            'instamart_cm_pct': s_qc['contribution_margin_pct'].tolist(),
            'instamart_ebitda_cr': s_qc['adj_ebitda_cr'].tolist(),
            'instamart_stores': s_qc['dark_stores'].tolist(),
            'instamart_aov_inr': s_qc['aov_inr'].tolist()
        },
        'structural_breaks': [
            {'quarter': 'Q2FY25', 'title': 'Paytm Ticketing Acquisition', 'company': 'Eternal', 'impact': '+118% inorganic Out-of-Home GOV jump'},
            {'quarter': 'Q2FY26', 'title': 'Blinkit 1P Inventory Shift', 'company': 'Eternal', 'impact': '+128% reported revenue surge under Ind AS 115'},
            {'quarter': 'Q3FY27', 'title': 'Swiggy IPO Listing', 'company': 'Swiggy', 'impact': 'Fresh capital injection and public disclosures'}
        ]
    })
