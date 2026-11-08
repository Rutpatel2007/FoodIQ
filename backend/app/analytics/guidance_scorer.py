"""
FoodIQ Management Guidance Credibility & Delivery Scorer.
Tracks forward corporate disclosures against retrospective actuals, calculating
empirical delivery rates, outcome variances, and credibility tiers.

Phase 2.1 Financial Audit Enforcement:
1. Strict 5-category outcome taxonomy:
   - DELIVERED
   - MISSED
   - PARTIALLY_DELIVERED
   - PENDING
   - NOT_OBJECTIVELY_MEASURABLE
2. Two delivery-rate sensitivities:
   - Strict: Delivered / Evaluable
   - Broad: (Delivered + 0.5 * Partially Delivered) / Evaluable
3. Clear isolation of Pending commitments (unmatured milestones cannot be counted as delivered or missed).
"""

import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.config import settings
from backend.app.analytics.repository import _get_sqlite_path

# Standardized Phase 2.1 Guidance Taxonomy Mapping
GUIDANCE_TAXONOMY_MAP = {
    'GD-001': {'category': 'DELIVERED', 'reason': 'FY26 quarterly GOV growth sustained at 21.6%-22.8%, exceeding 20% guidance.'},
    'GD-002': {'category': 'PENDING', 'reason': 'Medium-term target (FY28+) for 4.0-5.0% Adjusted EBITDA margin.'},
    'GD-003': {'category': 'PARTIALLY_DELIVERED', 'reason': 'Break-even reached in single exit month (May 2024), but quarterly average remained negative (-0.1%).'},
    'GD-004': {'category': 'PENDING', 'reason': 'Scale threshold EBITDA break-even target for Quick Commerce.'},
    'GD-005': {'category': 'PENDING', 'reason': 'Contribution per order bridge at future scale.'},
    'GD-006': {'category': 'DELIVERED', 'reason': 'Q2 net dark store addition guidance met with reported store count expansion.'},
    'GD-007': {'category': 'PENDING', 'reason': 'Q2-Q3 target horizon ongoing.'},
    'GD-008': {'category': 'PENDING', 'reason': 'Daily order volume threshold for dark store maturity.'},
    'GD-009': {'category': 'PENDING', 'reason': 'Long-term Out-of-Home run-rate target (FY29).'},
    'GD-010': {'category': 'PENDING', 'reason': 'Medium-term Out-of-Home margin target.'},
    'GD-011': {'category': 'PENDING', 'reason': 'Medium-term consolidated NOV target.'},
    'GD-012': {'category': 'PENDING', 'reason': 'Regulatory ownership transition ongoing over stated multi-quarter window.'},
    'GD-013': {'category': 'PENDING', 'reason': 'Full-year FY27 annual GOV guidance pending completion of FY27.'},
    'GD-014': {'category': 'NOT_OBJECTIVELY_MEASURABLE', 'reason': 'Management discussion of incremental toing opportunities; framed as strategic exploration, not numeric commitment.'},
    'GD-015': {'category': 'PENDING', 'reason': 'Q3 Quick Commerce NOV growth pending release of Q3 disclosures.'},
    'GD-016': {'category': 'PENDING', 'reason': 'Q3 Quick Commerce margin pending release of Q3 disclosures.'},
    'GD-017': {'category': 'NOT_OBJECTIVELY_MEASURABLE', 'reason': 'FY31 aspirational vision statement; explicitly stated in disclosure as non-binding aspiration.'},
    'GD-018': {'category': 'NOT_OBJECTIVELY_MEASURABLE', 'reason': 'Qualitative geographic expansion ambition without specific city count or date commitment.'}
}


def score_management_guidance(db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Evaluates management forward guidance commitments using the audited 5-tier taxonomy.
    """
    path = _get_sqlite_path(db_path)
    conn = sqlite3.connect(path)
    
    query = """
    SELECT 
        id, company, issued_quarter, metric, guidance_text, 
        target_quarter, target_value, actual_value, met, outcome_status,
        source_doc, source_page
    FROM guidance_log
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return {'total_commitments': 0, 'evaluable_commitments': 0, 'records': []}
        
    records = []
    delivered_count = 0
    missed_count = 0
    partially_delivered_count = 0
    pending_count = 0
    unmeasurable_count = 0
    
    for _, row in df.iterrows():
        gid = str(row['id'])
        tax_info = GUIDANCE_TAXONOMY_MAP.get(gid, {
            'category': 'PENDING' if pd.isna(row['met']) else ('DELIVERED' if row['met'] == 1 else 'MISSED'),
            'reason': row['outcome_status'] or ''
        })
        category = tax_info['category']
        
        if category == 'DELIVERED':
            delivered_count += 1
            met_val = 1
        elif category == 'MISSED':
            missed_count += 1
            met_val = 0
        elif category == 'PARTIALLY_DELIVERED':
            partially_delivered_count += 1
            met_val = 0.5
        elif category == 'PENDING':
            pending_count += 1
            met_val = None
        else:  # NOT_OBJECTIVELY_MEASURABLE
            unmeasurable_count += 1
            met_val = None
            
        target_val = row['target_value']
        actual_val = row['actual_value']
        variance_pct = round(((actual_val - target_val) / abs(target_val)) * 100.0, 1) if (
            pd.notna(target_val) and pd.notna(actual_val) and target_val != 0
        ) else None
        
        records.append({
            'id': gid,
            'company': row['company'],
            'issued_quarter': row['issued_quarter'],
            'metric': row['metric'],
            'guidance_text': row['guidance_text'],
            'target_quarter': row['target_quarter'],
            'target_value': target_val,
            'actual_value': actual_val,
            'variance_pct': variance_pct,
            'met': met_val,
            'standardized_status': category,
            'audit_rationale': tax_info['reason'],
            'outcome_status_raw': row['outcome_status'],
            'source_doc': row['source_doc'],
            'source_page': int(row['source_page']) if pd.notna(row['source_page']) else None
        })
        
    total_commitments = len(records)
    evaluable = delivered_count + missed_count + partially_delivered_count
    
    # Strict delivery rate = Delivered / Evaluable
    strict_delivery_rate_pct = round((delivered_count / evaluable) * 100.0, 1) if evaluable > 0 else None
    
    # Broad delivery rate = (Delivered + 0.5 * Partially Delivered) / Evaluable
    broad_delivery_rate_pct = round(((delivered_count + 0.5 * partially_delivered_count) / evaluable) * 100.0, 1) if evaluable > 0 else None
    
    if strict_delivery_rate_pct is not None and strict_delivery_rate_pct >= 80.0:
        credibility_tier = "High"
        credibility_notes = (
            f"Management shows strong execution on matured commitments ({delivered_count} of {evaluable} evaluable milestones delivered). "
            f"12 commitments remain pending future quarters; 3 items are directional aspirations rather than measurable forecasts."
        )
    elif strict_delivery_rate_pct is not None and strict_delivery_rate_pct >= 50.0:
        credibility_tier = "Moderate"
        credibility_notes = "Management delivers on core directional targets, though operational timelines experience modest slippage."
    else:
        credibility_tier = "Low"
        credibility_notes = "Significant variance between stated operational aspirations and reported corporate disclosures."

    return {
        'total_commitments': total_commitments,
        'evaluable_commitments': evaluable,
        'delivered_count': delivered_count,
        'missed_count': missed_count,
        'partially_delivered_count': partially_delivered_count,
        'pending_count': pending_count,
        'not_objectively_measurable_count': unmeasurable_count,
        'strict_delivery_rate_pct': strict_delivery_rate_pct,
        'broad_delivery_rate_pct': broad_delivery_rate_pct,
        'credibility_tier': credibility_tier,
        'credibility_notes': credibility_notes,
        'commitments': records
    }
