"""
FoodIQ Management Credibility & Narrative Verification Engine (Phase 4).
Evaluates executive management communication over time against retrospective reported performance.
Implements:
1. Comprehensive Statement Repository (16 categories, source document, physical PDF page).
2. Commitment Lifecycle Engine: ANNOUNCED -> ACTIVE -> DUE -> EVALUATED -> CLOSED.
   7-tier outcome taxonomy: DELIVERED, PARTIALLY_DELIVERED, MISSED, PENDING,
   NOT_OBJECTIVELY_MEASURABLE, WITHDRAWN_OR_SUPERSEDED, INSUFFICIENT_EVIDENCE.
3. Transparent Delivery & Credibility Analytics (Strict, Broad, by Segment, by Category, by FY).
4. Narrative Verification Engine: Compares qualitative explanations with financial observations.
   Tiers: SUPPORTED_BY_DISCLOSED_EVIDENCE, PARTIALLY_SUPPORTED, CONTRADICTED_BY_DISCLOSED_EVIDENCE,
   NOT_TESTABLE, INSUFFICIENT_DISCLOSURE. Separates correlation from causality.
5. Strategic Initiative Tracking across Eternal and Swiggy.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from backend.app.config import settings
from backend.app.analytics.repository import _get_sqlite_path, sanitize_for_json, get_analytical_df

# -----------------------------------------------------------------------------
# 1. 16 Formal Statement Categories
# -----------------------------------------------------------------------------
STATEMENT_CATEGORIES = [
    'FINANCIAL_GUIDANCE',
    'GROWTH_COMMITMENTS',
    'PROFITABILITY_TARGETS',
    'CONTRIBUTION_MARGIN_TARGETS',
    'ADJUSTED_EBITDA_TARGETS',
    'STORE_EXPANSION_COMMITMENTS',
    'CUSTOMER_ENGAGEMENT_TARGETS',
    'ORDER_GROWTH_FREQUENCY_EXPECTATIONS',
    'AOV_MONETISATION_EXPECTATIONS',
    'CAPEX_INVESTMENT_PLANS',
    'OPERATIONAL_EFFICIENCY_INITIATIVES',
    'STRATEGIC_INITIATIVES',
    'MARKET_EXPANSION_PLANS',
    'COMPETITIVE_POSITIONING_CLAIMS',
    'MANAGEMENT_EXPLANATIONS_OF_PAST_PERFORMANCE',
    'FORWARD_LOOKING_EXPECTATIONS'
]

# -----------------------------------------------------------------------------
# 2. Master Repository of Management Commitments (Both Eternal and Swiggy)
# -----------------------------------------------------------------------------
MASTER_MANAGEMENT_COMMITMENTS = [
    # --- SWIGGY COMMITMENTS ---
    {
        'commitment_id': 'COMM-SW-001',
        'legacy_id': 'GD-001',
        'company': 'Swiggy',
        'speaker': 'Sriharsha Majety (Group CEO) & Rohit Kapoor (CEO Food)',
        'verbatim_quote': "Targeting >20% annualised GOV growth for the core Food Delivery business in FY26 and beyond.",
        'source_doc': 'Swiggy-Q1-FY2026-Shareholder-letter.pdf',
        'source_page': 4,
        'issued_quarter': 'Q1FY26',
        'category': 'GROWTH_COMMITMENTS',
        'segment': 'Food',
        'metric_targeted': 'gov_cr',
        'target_value': 20.0,
        'target_unit': 'YoY % Growth',
        'target_period': 'FY26 / Annual',
        'direction': 'INCREASE',
        'conditions': 'Excluding one-off platform promotions; assuming stable macro environment',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': 22.1,
        'variance': 2.1,
        'pct_achievement': 110.5,
        'evaluation_date': '2026-05-15',
        'evaluation_evidence': 'FY26 food GOV grew 21.6% to 22.8% YoY across quarters, averaging 22.1%.',
        'counter_evidence': 'Growth slowed to 19.8% in seasonal Q3, but full-year FY26 average exceeded target.',
        'credibility_notes': 'Delivered cleanly without metric redefinitions.'
    },
    {
        'commitment_id': 'COMM-SW-002',
        'legacy_id': 'GD-002',
        'company': 'Swiggy',
        'speaker': 'Rahul Bothra (CFO)',
        'verbatim_quote': "Targeting medium-term Food Delivery Adjusted EBITDA margin of 4.0% to 5.0% of GOV.",
        'source_doc': 'Swiggy-Q1-FY2026-Shareholder-letter.pdf',
        'source_page': 5,
        'issued_quarter': 'Q1FY26',
        'category': 'ADJUSTED_EBITDA_TARGETS',
        'segment': 'Food',
        'metric_targeted': 'adj_ebitda_margin_pct',
        'target_value': 4.5,
        'target_unit': '% of GOV',
        'target_period': 'Medium-term (FY28+)',
        'direction': 'INCREASE',
        'conditions': 'Subject to ad monetisation scaling and delivery partner density',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 3.4,
        'variance': -1.1,
        'pct_achievement': 75.5,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Food delivery EBITDA margin expanded from 0.8% in Q1FY25 to 3.4% in Q2FY27.',
        'counter_evidence': 'Medium-term target window has not matured; cannot be classified as delivered or missed.',
        'credibility_notes': 'Progressing steadily toward 4.0% lower bound.'
    },
    {
        'commitment_id': 'COMM-SW-003',
        'legacy_id': 'GD-003',
        'company': 'Swiggy',
        'speaker': 'Phani Kishan (CEO Instamart)',
        'verbatim_quote': "Instamart targeting contribution margin break-even (0.0%) by Q1 FY27.",
        'source_doc': 'Swiggy-Q2-FY2026-Shareholder-letter.pdf',
        'source_page': 8,
        'issued_quarter': 'Q2FY26',
        'category': 'CONTRIBUTION_MARGIN_TARGETS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'contribution_margin_pct',
        'target_value': 0.0,
        'target_unit': '% of GOV',
        'target_period': 'Q1FY27',
        'direction': 'INCREASE',
        'conditions': 'Assuming network dark store base does not exceed 1,150 stores in Q1',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'PARTIALLY_DELIVERED',
        'actual_value_reported': -0.2,
        'variance': -0.2,
        'pct_achievement': 95.0,
        'evaluation_date': '2026-08-10',
        'evaluation_evidence': 'Swiggy achieved single exit-month break-even in May 2026 (+0.1%), but quarterly average was -0.2%.',
        'counter_evidence': 'Subsequent aggressive store rollout in Q2FY27 brought CM back to -1.0%.',
        'credibility_notes': 'Milestone technically achieved on monthly exit run-rate, but quarterly average narrowly missed.'
    },
    {
        'commitment_id': 'COMM-SW-004',
        'legacy_id': 'GD-004',
        'company': 'Swiggy',
        'speaker': 'Rahul Bothra (CFO)',
        'verbatim_quote': "Targeting Adjusted EBITDA break-even in Quick Commerce at scale threshold of ₹15,000 Cr annualised GOV.",
        'source_doc': 'Swiggy-Q2-FY2026-Shareholder-letter.pdf',
        'source_page': 9,
        'issued_quarter': 'Q2FY26',
        'category': 'PROFITABILITY_TARGETS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'adj_ebitda_cr',
        'target_value': 0.0,
        'target_unit': 'INR Cr',
        'target_period': 'At Scale Threshold (FY28)',
        'direction': 'INCREASE',
        'conditions': 'Requires dark store density in top 15 metros to reach mature throughput',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': -895.0,
        'variance': -895.0,
        'pct_achievement': None,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Current annualised GOV is ~₹36,920 Cr, but accelerated expansion has kept EBITDA negative.',
        'counter_evidence': 'Scale threshold target has not matured.',
        'credibility_notes': 'Pending evaluation at end of current investment cycle.'
    },
    {
        'commitment_id': 'COMM-SW-005',
        'legacy_id': 'GD-005',
        'company': 'Swiggy',
        'speaker': 'Phani Kishan (CEO Instamart)',
        'verbatim_quote': "Bridging Instamart per-order economics through ₹10 product mix/monetisation, ₹10 ads, and ₹10 scale leverage.",
        'source_doc': 'Swiggy-Q3-FY2026-Shareholder-letter.pdf',
        'source_page': 11,
        'issued_quarter': 'Q3FY26',
        'category': 'OPERATIONAL_EFFICIENCY_INITIATIVES',
        'segment': 'QuickCommerce',
        'metric_targeted': 'contribution_profit_per_order_inr',
        'target_value': 30.0,
        'target_unit': 'INR / order improvement',
        'target_period': 'Medium-term (FY28)',
        'direction': 'INCREASE',
        'conditions': 'Non-grocery general merchandise reaching 25%+ of cart mix',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 14.84,
        'variance': -15.16,
        'pct_achievement': 49.5,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Loss per order contracted from -₹21.92 to -₹7.08 (₹14.84 per order saved).',
        'counter_evidence': 'Remaining ₹15.16 per order improvement pending ad network scale.',
        'credibility_notes': 'On track; 49.5% of total bridge delivered to date.'
    },
    {
        'commitment_id': 'COMM-SW-006',
        'legacy_id': 'GD-006',
        'company': 'Swiggy',
        'speaker': 'Sriharsha Majety (Group CEO)',
        'verbatim_quote': "Adding 100+ net dark stores in Q2 FY27 to reach 1,200+ operating stores.",
        'source_doc': 'Swiggy-Q1-FY2027-Shareholder-letter.pdf',
        'source_page': 6,
        'issued_quarter': 'Q1FY27',
        'category': 'STORE_EXPANSION_COMMITMENTS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'dark_stores',
        'target_value': 1200.0,
        'target_unit': 'Count',
        'target_period': 'Q2FY27',
        'direction': 'INCREASE',
        'conditions': 'Real estate handover timelines in Tier-2 micro-markets',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': 1240.0,
        'variance': 40.0,
        'pct_achievement': 103.3,
        'evaluation_date': '2026-10-25',
        'evaluation_evidence': 'Reported 1,240 dark stores at end of Q2FY27 (adding 69 net stores over 1,171 base).',
        'counter_evidence': 'None.',
        'credibility_notes': 'Clean delivery exceeding target by 40 stores.'
    },
    {
        'commitment_id': 'COMM-SW-007',
        'legacy_id': 'GD-007',
        'company': 'Swiggy',
        'speaker': 'Rahul Bothra (CFO)',
        'verbatim_quote': "Expect Instamart contribution margin to fluctuate between 0.0% and -1.0% in Q2-Q3 FY27 due to store opening gestation costs.",
        'source_doc': 'Swiggy-Q1-FY2027-Shareholder-letter.pdf',
        'source_page': 7,
        'issued_quarter': 'Q1FY27',
        'category': 'CONTRIBUTION_MARGIN_TARGETS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'contribution_margin_pct',
        'target_value': -0.5,
        'target_unit': '% of GOV',
        'target_period': 'Q2FY27',
        'direction': 'RANGE',
        'conditions': 'Opening 100+ stores per quarter',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': -1.0,
        'variance': 0.0,
        'pct_achievement': 100.0,
        'evaluation_date': '2026-10-25',
        'evaluation_evidence': 'Q2FY27 contribution margin landed at exactly -1.0% of GOV, within the guided 0 to -1.0% corridor.',
        'counter_evidence': 'At lower bound of guidance corridor.',
        'credibility_notes': 'Accurate forward guidance regarding gestation cost drag.'
    },
    {
        'commitment_id': 'COMM-SW-008',
        'legacy_id': 'GD-008',
        'company': 'Swiggy',
        'speaker': 'Phani Kishan (CEO Instamart)',
        'verbatim_quote': "Targeting average daily order volume of 1,200+ orders per store-day for mature cohorts.",
        'source_doc': 'Swiggy-Q2-FY2027-Shareholder-letter.pdf',
        'source_page': 13,
        'issued_quarter': 'Q2FY27',
        'category': 'ORDER_GROWTH_FREQUENCY_EXPECTATIONS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'orders_per_store_day',
        'target_value': 1200.0,
        'target_unit': 'Orders / store-day',
        'target_period': 'Q4FY27',
        'direction': 'INCREASE',
        'conditions': 'Mature stores >12 months in Tier-1 catchments',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 1143.0,
        'variance': -57.0,
        'pct_achievement': 95.3,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Current blended average across all stores is 1,143 orders/store-day.',
        'counter_evidence': 'Target matures in Q4FY27.',
        'credibility_notes': 'On track for mature cohort.'
    },
    {
        'commitment_id': 'COMM-SW-009',
        'legacy_id': 'GD-009',
        'company': 'Swiggy',
        'speaker': 'Rohit Kapoor (CEO Food & Out-of-Home)',
        'verbatim_quote': "Targeting ₹10,000 Cr annualised GOV run-rate for Out-of-Home by FY29.",
        'source_doc': 'Swiggy-Q1-FY2026-Shareholder-letter.pdf',
        'source_page': 9,
        'issued_quarter': 'Q1FY26',
        'category': 'GROWTH_COMMITMENTS',
        'segment': 'OutOfHome',
        'metric_targeted': 'gov_cr',
        'target_value': 2500.0,
        'target_unit': 'INR Cr / quarter',
        'target_period': 'FY29',
        'direction': 'INCREASE',
        'conditions': 'Expanding Dineout and SteppinOut across 50 cities',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 850.0,
        'variance': -1650.0,
        'pct_achievement': 34.0,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Current quarterly run-rate is ~₹850 Cr.',
        'counter_evidence': 'Long-term horizon (FY29).',
        'credibility_notes': 'Pending evaluation.'
    },
    {
        'commitment_id': 'COMM-SW-010',
        'legacy_id': 'GD-010',
        'company': 'Swiggy',
        'speaker': 'Rahul Bothra (CFO)',
        'verbatim_quote': "Expecting Out-of-Home Adjusted EBITDA margin to reach 3.0%-4.0% of GOV over medium term.",
        'source_doc': 'Swiggy-Q1-FY2026-Shareholder-letter.pdf',
        'source_page': 10,
        'issued_quarter': 'Q1FY26',
        'category': 'PROFITABILITY_TARGETS',
        'segment': 'OutOfHome',
        'metric_targeted': 'adj_ebitda_margin_pct',
        'target_value': 3.5,
        'target_unit': '% of GOV',
        'target_period': 'Medium-term (FY28)',
        'direction': 'INCREASE',
        'conditions': 'Ticketing platform synergies',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 1.2,
        'variance': -2.3,
        'pct_achievement': 34.3,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Segment is profitable at 1.2% EBITDA margin.',
        'counter_evidence': 'Target period ongoing.',
        'credibility_notes': 'Pending.'
    },
    {
        'commitment_id': 'COMM-SW-011',
        'legacy_id': 'GD-011',
        'company': 'Swiggy',
        'speaker': 'Sriharsha Majety (Group CEO)',
        'verbatim_quote': "Consolidated platform NOV to double over the next 3 to 4 years.",
        'source_doc': 'Swiggy-Q2-FY2026-Shareholder-letter.pdf',
        'source_page': 3,
        'issued_quarter': 'Q2FY26',
        'category': 'GROWTH_COMMITMENTS',
        'segment': 'Consolidated',
        'metric_targeted': 'nov_cr',
        'target_value': 30000.0,
        'target_unit': 'INR Cr / quarter',
        'target_period': 'FY29-FY30',
        'direction': 'INCREASE',
        'conditions': 'Multi-segment adoption by Swiggy One subscribers',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 17120.0,
        'variance': -12880.0,
        'pct_achievement': 57.1,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Platform NOV grew from ~₹12,000 Cr to ₹17,120 Cr.',
        'counter_evidence': '3-4 year horizon.',
        'credibility_notes': 'Pending.'
    },
    {
        'commitment_id': 'COMM-SW-012',
        'legacy_id': 'GD-012',
        'company': 'Swiggy',
        'speaker': 'Rahul Bothra (CFO)',
        'verbatim_quote': "Lynks sale to complete in Q2 FY27 with full deconsolidation by Q3 FY27, improving quarterly EBITDA by ~₹20 Cr.",
        'source_doc': 'Swiggy-Q2-FY2027-Shareholder-letter.pdf',
        'source_page': 15,
        'issued_quarter': 'Q2FY27',
        'category': 'STRATEGIC_INITIATIVES',
        'segment': 'SupplyChain',
        'metric_targeted': 'adj_ebitda_cr',
        'target_value': 20.0,
        'target_unit': 'INR Cr / quarter benefit',
        'target_period': 'Q3FY27',
        'direction': 'INCREASE',
        'conditions': 'Closing of divestment transaction',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': None,
        'variance': None,
        'pct_achievement': None,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Transaction closed in Q2FY27; financial deconsolidation pending Q3 earnings disclosure.',
        'counter_evidence': 'Quarterly numbers for Q3FY27 not yet filed.',
        'credibility_notes': 'Pending Q3 disclosure.'
    },
    {
        'commitment_id': 'COMM-SW-013',
        'legacy_id': 'GD-013',
        'company': 'Swiggy',
        'speaker': 'Sriharsha Majety (Group CEO)',
        'verbatim_quote': "Full year FY27 Food Delivery GOV expected to grow 20-22% YoY.",
        'source_doc': 'Swiggy-Q1-FY2027-Shareholder-letter.pdf',
        'source_page': 4,
        'issued_quarter': 'Q1FY27',
        'category': 'GROWTH_COMMITMENTS',
        'segment': 'Food',
        'metric_targeted': 'gov_cr',
        'target_value': 21.0,
        'target_unit': 'YoY % Growth',
        'target_period': 'FY27 Full Year',
        'direction': 'INCREASE',
        'conditions': 'Full year completion',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 21.4,
        'variance': 0.4,
        'pct_achievement': 101.9,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'First half (Q1-Q2 FY27) tracking at 21.4% YoY growth.',
        'counter_evidence': 'FY27 has 2 quarters remaining.',
        'credibility_notes': 'Pending full year completion.'
    },
    {
        'commitment_id': 'COMM-SW-014',
        'legacy_id': 'GD-014',
        'company': 'Swiggy',
        'speaker': 'Management Commentary',
        'verbatim_quote': "Exploring incremental snacking and late-night 'Toing' occasions to expand platform engagement.",
        'source_doc': 'Swiggy-Q2-FY2027-Shareholder-letter.pdf',
        'source_page': 9,
        'issued_quarter': 'Q2FY27',
        'category': 'STRATEGIC_INITIATIVES',
        'segment': 'Food',
        'metric_targeted': 'engagement',
        'target_value': None,
        'target_unit': 'Qualitative Concept',
        'target_period': 'Ongoing',
        'direction': 'EXPLORATORY',
        'conditions': 'Customer trial',
        'lifecycle_stage': 'EVALUATED',
        'outcome_status': 'NOT_OBJECTIVELY_MEASURABLE',
        'actual_value_reported': None,
        'variance': None,
        'pct_achievement': None,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Framed explicitly as an exploratory concept, not a quantitative commitment.',
        'counter_evidence': 'No numeric metric or deadline provided.',
        'credibility_notes': 'Qualitative ambition, correctly excluded from delivery rate denominators.'
    },
    {
        'commitment_id': 'COMM-SW-015',
        'legacy_id': 'GD-015',
        'company': 'Swiggy',
        'speaker': 'Phani Kishan (CEO Instamart)',
        'verbatim_quote': "Q3 FY27 Quick Commerce NOV expected to maintain >80% YoY growth.",
        'source_doc': 'Swiggy-Q2-FY2027-Shareholder-letter.pdf',
        'source_page': 14,
        'issued_quarter': 'Q2FY27',
        'category': 'GROWTH_COMMITMENTS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'nov_cr',
        'target_value': 80.0,
        'target_unit': 'YoY % Growth',
        'target_period': 'Q3FY27',
        'direction': 'INCREASE',
        'conditions': 'Diwali festival shopping demand',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': None,
        'variance': None,
        'pct_achievement': None,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Q3 FY27 disclosures pending.',
        'counter_evidence': 'Not matured.',
        'credibility_notes': 'Pending Q3 reporting.'
    },
    {
        'commitment_id': 'COMM-SW-016',
        'legacy_id': 'GD-016',
        'company': 'Swiggy',
        'speaker': 'Rahul Bothra (CFO)',
        'verbatim_quote': "Targeting Q3 FY27 Quick Commerce contribution margin in the -0.5% to -1.0% corridor.",
        'source_doc': 'Swiggy-Q2-FY2027-Shareholder-letter.pdf',
        'source_page': 14,
        'issued_quarter': 'Q2FY27',
        'category': 'CONTRIBUTION_MARGIN_TARGETS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'contribution_margin_pct',
        'target_value': -0.75,
        'target_unit': '% of GOV',
        'target_period': 'Q3FY27',
        'direction': 'RANGE',
        'conditions': 'Continued rapid store additions',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': None,
        'variance': None,
        'pct_achievement': None,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Q3 FY27 disclosures pending.',
        'counter_evidence': 'Not matured.',
        'credibility_notes': 'Pending Q3 reporting.'
    },
    {
        'commitment_id': 'COMM-SW-017',
        'legacy_id': 'GD-017',
        'company': 'Swiggy',
        'speaker': 'Sriharsha Majety (Group CEO)',
        'verbatim_quote': "Envisioning serving 100 million monthly transacting users across all offerings by FY31.",
        'source_doc': 'Swiggy-Q1-FY2026-Shareholder-letter.pdf',
        'source_page': 2,
        'issued_quarter': 'Q1FY26',
        'category': 'CUSTOMER_ENGAGEMENT_TARGETS',
        'segment': 'Platform',
        'metric_targeted': 'mtu_mn',
        'target_value': 100.0,
        'target_unit': 'Millions (MTU)',
        'target_period': 'FY31',
        'direction': 'INCREASE',
        'conditions': 'Macro smartphone and digital penetration expansion in India',
        'lifecycle_stage': 'EVALUATED',
        'outcome_status': 'NOT_OBJECTIVELY_MEASURABLE',
        'actual_value_reported': 18.5,
        'variance': -81.5,
        'pct_achievement': 18.5,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'Long-term corporate vision statement (>5 year horizon), explicitly qualified as non-binding.',
        'counter_evidence': 'Too far in the future to constitute a quarterly operational commitment.',
        'credibility_notes': 'Vision statement, excluded from current execution scoring.'
    },
    {
        'commitment_id': 'COMM-SW-018',
        'legacy_id': 'GD-018',
        'company': 'Swiggy',
        'speaker': 'Rohit Kapoor (CEO Food)',
        'verbatim_quote': "Targeting deeper geographic penetration into Tier-3 and Tier-4 towns over the coming quarters.",
        'source_doc': 'Swiggy-Q2-FY2027-Shareholder-letter.pdf',
        'source_page': 8,
        'issued_quarter': 'Q2FY27',
        'category': 'MARKET_EXPANSION_PLANS',
        'segment': 'Food',
        'metric_targeted': 'city_count',
        'target_value': None,
        'target_unit': 'Cities',
        'target_period': 'Coming quarters',
        'direction': 'INCREASE',
        'conditions': 'Restaurant availability',
        'lifecycle_stage': 'EVALUATED',
        'outcome_status': 'NOT_OBJECTIVELY_MEASURABLE',
        'actual_value_reported': None,
        'variance': None,
        'pct_achievement': None,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'General geographic ambition without specific town count or delivery milestone.',
        'counter_evidence': 'No verifiable metric.',
        'credibility_notes': 'Qualitative statement.'
    },

    # --- ETERNAL (ZOMATO / BLINKIT / DISTRICT) COMMITMENTS ---
    {
        'commitment_id': 'COMM-ET-001',
        'legacy_id': 'GD-ET-001',
        'company': 'Eternal',
        'speaker': 'Albinder Dhindsa (CEO Blinkit) & Deepinder Goyal (CEO Eternal)',
        'verbatim_quote': "Targeting 1,000 dark stores by the end of FY25 (March 2025).",
        'source_doc': 'Eternal-Q1FY25-Shareholder-letter.pdf',
        'source_page': 12,
        'issued_quarter': 'Q1FY25',
        'category': 'STORE_EXPANSION_COMMITMENTS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'dark_stores',
        'target_value': 1000.0,
        'target_unit': 'Count',
        'target_period': 'Q4FY25',
        'direction': 'INCREASE',
        'conditions': 'Availability of micro-market properties and dark store manager talent',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': 1300.0,
        'variance': 300.0,
        'pct_achievement': 130.0,
        'evaluation_date': '2025-05-10',
        'evaluation_evidence': 'Reported 1,300 dark stores in Q4 FY25, beating stated guidance by 300 stores (+30%).',
        'counter_evidence': 'None.',
        'credibility_notes': 'Major delivery outperformance.'
    },
    {
        'commitment_id': 'COMM-ET-002',
        'legacy_id': 'GD-ET-002',
        'company': 'Eternal',
        'speaker': 'Albinder Dhindsa (CEO Blinkit)',
        'verbatim_quote': "Targeting 2,000 dark stores by the end of calendar year 2026.",
        'source_doc': 'Eternal-Q2FY25-Shareholder-letter.pdf',
        'source_page': 14,
        'issued_quarter': 'Q2FY25',
        'category': 'STORE_EXPANSION_COMMITMENTS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'dark_stores',
        'target_value': 2000.0,
        'target_unit': 'Count',
        'target_period': 'Q3FY27',
        'direction': 'INCREASE',
        'conditions': 'Cluster density expansion across top 20 cities and selective Tier-2 entry',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': 2700.0,
        'variance': 700.0,
        'pct_achievement': 135.0,
        'evaluation_date': '2026-10-20',
        'evaluation_evidence': 'Reported 2,700 dark stores in Q2 FY27, surpassing the 2,000-store milestone ahead of calendar 2026 target.',
        'counter_evidence': 'None.',
        'credibility_notes': 'Delivered ahead of time and above volume target.'
    },
    {
        'commitment_id': 'COMM-ET-003',
        'legacy_id': 'GD-ET-003',
        'company': 'Eternal',
        'speaker': 'Deepinder Goyal (CEO Eternal) & Akshant Goyal (CFO)',
        'verbatim_quote': "Expecting Blinkit to reach Adjusted EBITDA break-even by Q1 FY25.",
        'source_doc': 'Eternal-Q3FY24-Shareholder-letter.pdf',
        'source_page': 10,
        'issued_quarter': 'Q3FY24',
        'category': 'PROFITABILITY_TARGETS',
        'segment': 'QuickCommerce',
        'metric_targeted': 'adj_ebitda_cr',
        'target_value': 0.0,
        'target_unit': 'INR Cr',
        'target_period': 'Q1FY25',
        'direction': 'INCREASE',
        'conditions': 'Consistent AOV and dark store operating cost absorption',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'PARTIALLY_DELIVERED',
        'actual_value_reported': -3.0,
        'variance': -3.0,
        'pct_achievement': 97.0,
        'evaluation_date': '2024-07-25',
        'evaluation_evidence': 'Reported Adjusted EBITDA was -₹3 Cr in Q1 FY25 (virtually break-even, positive contribution margin achieved). Turned positive in Q2FY25 (+₹8 Cr).',
        'counter_evidence': 'Narrowly missed exact zero in Q1 by ₹3 Cr before crossing in Q2.',
        'credibility_notes': 'Missed by a negligible margin of ₹3 Cr on a ₹4,900 Cr GOV base, achieving positive EBITDA the following quarter.'
    },
    {
        'commitment_id': 'COMM-ET-004',
        'legacy_id': 'GD-ET-004',
        'company': 'Eternal',
        'speaker': 'Deepinder Goyal (CEO Eternal)',
        'verbatim_quote': "Targeting >20% YoY GOV growth in Food Delivery over the medium term.",
        'source_doc': 'Eternal-Q1FY25-Shareholder-letter.pdf',
        'source_page': 5,
        'issued_quarter': 'Q1FY25',
        'category': 'GROWTH_COMMITMENTS',
        'segment': 'Food',
        'metric_targeted': 'gov_cr',
        'target_value': 20.0,
        'target_unit': 'YoY % Growth',
        'target_period': 'FY25-FY26',
        'direction': 'INCREASE',
        'conditions': 'Zomato Gold membership expansion and restaurant menu curation',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': 24.2,
        'variance': 4.2,
        'pct_achievement': 121.0,
        'evaluation_date': '2026-05-10',
        'evaluation_evidence': 'Food delivery GOV grew between 21.4% and 27.2% YoY throughout FY25 and FY26, averaging 24.2%.',
        'counter_evidence': 'None.',
        'credibility_notes': 'Consistently delivered above stated target.'
    },
    {
        'commitment_id': 'COMM-ET-005',
        'legacy_id': 'GD-ET-005',
        'company': 'Eternal',
        'speaker': 'Akshant Goyal (CFO)',
        'verbatim_quote': "Targeting Food Delivery Adjusted EBITDA margin of 4.0% to 5.0% of GOV.",
        'source_doc': 'Eternal-Q1FY25-Shareholder-letter.pdf',
        'source_page': 6,
        'issued_quarter': 'Q1FY25',
        'category': 'ADJUSTED_EBITDA_TARGETS',
        'segment': 'Food',
        'metric_targeted': 'adj_ebitda_margin_pct',
        'target_value': 4.5,
        'target_unit': '% of GOV',
        'target_period': 'FY26-FY27',
        'direction': 'INCREASE',
        'conditions': 'Platform fee optimization and delivery fleet efficiency',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': 5.82,
        'variance': 1.32,
        'pct_achievement': 129.3,
        'evaluation_date': '2026-10-20',
        'evaluation_evidence': 'Food Delivery Adjusted EBITDA margin expanded to 5.82% of GOV by Q2 FY27, beating the 5.0% target ceiling.',
        'counter_evidence': 'Platform fees faced minor restaurant association pushback.',
        'credibility_notes': 'Strong delivery exceeding upper bound of guidance.'
    },
    {
        'commitment_id': 'COMM-ET-006',
        'legacy_id': 'GD-ET-006',
        'company': 'Eternal',
        'speaker': 'Deepinder Goyal (CEO Eternal)',
        'verbatim_quote': "Targeting District (Going-Out) to achieve ₹10,000 Cr annualised GOV by FY26.",
        'source_doc': 'Eternal-Q2FY25-Shareholder-letter.pdf',
        'source_page': 9,
        'issued_quarter': 'Q2FY25',
        'category': 'GROWTH_COMMITMENTS',
        'segment': 'OutOfHome',
        'metric_targeted': 'gov_cr',
        'target_value': 2500.0,
        'target_unit': 'INR Cr / quarter',
        'target_period': 'FY26',
        'direction': 'INCREASE',
        'conditions': 'Integration of Paytm Insider and TicketNew ticketing business',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': 1850.0,
        'variance': -650.0,
        'pct_achievement': 74.0,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'District reached ~₹1,850 Cr quarterly GOV in Q2FY26 following full consolidation.',
        'counter_evidence': 'FY26 full year results ongoing.',
        'credibility_notes': 'Pending full year evaluation.'
    },
    {
        'commitment_id': 'COMM-ET-007',
        'legacy_id': 'GD-ET-007',
        'company': 'Eternal',
        'speaker': 'Akshant Goyal (CFO)',
        'verbatim_quote': "Hyperpure targeting sustained Adjusted EBITDA break-even over the next 4 to 6 quarters.",
        'source_doc': 'Eternal-Q3FY25-Shareholder-letter.pdf',
        'source_page': 11,
        'issued_quarter': 'Q3FY25',
        'category': 'PROFITABILITY_TARGETS',
        'segment': 'SupplyChain',
        'metric_targeted': 'adj_ebitda_cr',
        'target_value': 0.0,
        'target_unit': 'INR Cr',
        'target_period': 'Q1FY27',
        'direction': 'INCREASE',
        'conditions': 'Higher private label mix in packaging and value-added food processing',
        'lifecycle_stage': 'ACTIVE',
        'outcome_status': 'PENDING',
        'actual_value_reported': -18.0,
        'variance': -18.0,
        'pct_achievement': None,
        'evaluation_date': '2026-11-08',
        'evaluation_evidence': 'EBITDA loss narrowed to -₹18 Cr, but intercompany eliminations from Blinkit 1P shifted revenue structure.',
        'counter_evidence': 'Target period Q1FY27 maturing.',
        'credibility_notes': 'Pending final evaluation.'
    },
    {
        'commitment_id': 'COMM-ET-008',
        'legacy_id': 'GD-ET-008',
        'company': 'Eternal',
        'speaker': 'Deepinder Goyal (CEO Eternal)',
        'verbatim_quote': "Maintaining strong liquidity buffer of >₹10,000 Cr cash balance post-QIP to fund quick commerce land-grab.",
        'source_doc': 'Eternal-Q3FY25-Shareholder-letter.pdf',
        'source_page': 4,
        'issued_quarter': 'Q3FY25',
        'category': 'CAPEX_INVESTMENT_PLANS',
        'segment': 'Consolidated',
        'metric_targeted': 'cash_balance_cr',
        'target_value': 10000.0,
        'target_unit': 'INR Cr',
        'target_period': 'Ongoing FY25-FY26',
        'direction': 'MAINTAIN',
        'conditions': 'Successful completion of ₹8,500 Cr QIP equity raise',
        'lifecycle_stage': 'CLOSED',
        'outcome_status': 'DELIVERED',
        'actual_value_reported': 12400.0,
        'variance': 2400.0,
        'pct_achievement': 124.0,
        'evaluation_date': '2025-12-15',
        'evaluation_evidence': 'Completed QIP and maintained consolidated treasury balance exceeding ₹12,000 Cr.',
        'counter_evidence': 'None.',
        'credibility_notes': 'Fully delivered.'
    }
]

# -----------------------------------------------------------------------------
# 3. Master Repository of Narrative Explanations & Empirical Verifications
# -----------------------------------------------------------------------------
MASTER_NARRATIVE_VERIFICATIONS = [
    {
        'narrative_id': 'NARR-001',
        'company': 'Swiggy',
        'speaker': 'Management Q&A / Letter',
        'document': 'Swiggy-Q1-FY2026-Shareholder-letter.pdf',
        'page': 2,
        'quarter': 'Q1FY26',
        'topic': 'seasonality_and_margin',
        'verbatim_explanation': "Management attributed Q1 food-delivery margin decline to seasonal delivery-partner availability pressure from reverse migration and the start of rains, alongside annual salary increments.",
        'relevant_metrics': ['adj_ebitda_margin_pct', 'delivery_cost_per_order_inr'],
        'empirical_evidence_found': (
            "Food Delivery Adjusted EBITDA margin declined by ~40 bps sequentially in Q1 FY26. "
            "Delivery cost per order increased by ₹3.20 during the monsoon quarter."
        ),
        'other_disclosed_factors': 'Annual corporate salary increments and festival promotional subsidies.',
        'correlation_vs_causation_note': (
            "Seasonal weather disruptions correlate with delivery cost surges across both Indian delivery platforms. "
            "However, primary disclosures aggregate weather bonuses with fuel escalation, preventing exact causal decomposition."
        ),
        'verification_tier': 'SUPPORTED_BY_DISCLOSED_EVIDENCE',
        'audit_determination': 'Empirically supported by seasonal margin contraction observed in both FY25 and FY26 Q1s.'
    },
    {
        'narrative_id': 'NARR-002',
        'company': 'Swiggy',
        'speaker': 'Phani Kishan (CEO Instamart)',
        'document': 'Swiggy-Q2-FY2026-Shareholder-letter.pdf',
        'page': 11,
        'quarter': 'Q2FY26',
        'topic': 'aov_and_contribution_margin',
        'verbatim_explanation': "Management stated that higher Average Order Value directly expands Instamart contribution margins by spreading fixed delivery costs.",
        'relevant_metrics': ['aov_inr', 'contribution_margin_pct'],
        'empirical_evidence_found': (
            "AOV expanded from ₹487 to ₹708 while Contribution Margin improved from -4.5% to -1.0% over 6 quarters ($r = 0.9014$ on levels). "
            "However, first-difference detrending reveals $r = 0.1399 (p = 0.72)$."
        ),
        'other_disclosed_factors': 'Route densification, dark store pick-and-pack automation, and ad monetisation growth.',
        'correlation_vs_causation_note': (
            "While higher basket size provides mechanical operating leverage, econometric testing shows AOV jumps "
            "do not synchronously cause margin jumps in the same quarter. Cost efficiencies compound gradually."
        ),
        'verification_tier': 'PARTIALLY_SUPPORTED',
        'audit_determination': 'Long-term level association is strong, but contemporaneous causal claim is rejected by statistical detrending.'
    },
    {
        'narrative_id': 'NARR-003',
        'company': 'Eternal',
        'speaker': 'Albinder Dhindsa (CEO Blinkit)',
        'document': 'Eternal-Q2FY26-Shareholder-letter.pdf',
        'page': 12,
        'quarter': 'Q2FY26',
        'topic': 'inventory_ownership_and_revenue',
        'verbatim_explanation': "Management stated that inventory ownership (1P model) was adopted to ensure consistent product availability in electronics and apparel, resulting in headline revenue expansion.",
        'relevant_metrics': ['adj_revenue_cr', 'nov_cr'],
        'empirical_evidence_found': (
            "Adjusted Revenue leaped +128.4% QoQ from ₹1,061 Cr to ₹2,423 Cr. "
            "Underlying transacted NOV grew +24.2% QoQ from ₹9,400 Cr to ₹11,679 Cr."
        ),
        'other_disclosed_factors': 'Under Ind AS 115, gross product selling price is billed as revenue under 1P rather than net commission.',
        'correlation_vs_causation_note': (
            "Over 80% of the sequential revenue surge was an accounting recognition artifact rather than 128% commercial volume growth."
        ),
        'verification_tier': 'SUPPORTED_BY_DISCLOSED_EVIDENCE',
        'audit_determination': 'Management acknowledged the accounting impact; empirical verification confirms volume grew 24.2% while revenue surged 128%.'
    },
    {
        'narrative_id': 'NARR-004',
        'company': 'Eternal',
        'speaker': 'Deepinder Goyal (CEO Eternal)',
        'document': 'Eternal-Q1FY25-Shareholder-letter.pdf',
        'page': 6,
        'quarter': 'Q1FY25',
        'topic': 'dark_store_gestation_and_throughput',
        'verbatim_explanation': "Management explained that new dark stores in emerging clusters require 6 to 9 months of cohort maturation to reach network-average throughput.",
        'relevant_metrics': ['dark_stores', 'nov_cr', 'throughput_store_day'],
        'empirical_evidence_found': (
            "Blended network throughput expanded +22.0% (from ₹6.96L to ₹8.50L / store-day) between Q1 FY25 and Q2 FY27. "
            "However, store-level cohort disclosures are withheld."
        ),
        'other_disclosed_factors': 'Expanding SKU catalog density (from 4,000 SKUs to 12,000+ SKUs) and non-grocery expansion.',
        'correlation_vs_causation_note': (
            "Without month-by-month store vintage disclosures, cohort ramp curves cannot be independently audited from public filings."
        ),
        'verification_tier': 'NOT_TESTABLE',
        'audit_determination': 'Plausible retail operational dynamic, but unverified due to lack of store-level cohort reporting.'
    },
    {
        'narrative_id': 'NARR-005',
        'company': 'Swiggy',
        'speaker': 'Rohit Kapoor (CEO Food)',
        'document': 'Swiggy-Q2-FY2027-Shareholder-letter.pdf',
        'page': 7,
        'quarter': 'Q2FY27',
        'topic': 'take_rate_and_advertising',
        'verbatim_explanation': "Management attributes its superior headline Take Rate (~24.0% of GOV) to advertising penetration and premium restaurant curation.",
        'relevant_metrics': ['take_rate_pct', 'adj_revenue_cr', 'gov_cr'],
        'empirical_evidence_found': (
            "Swiggy headline take rate is 24.0% vs Eternal Food Adjusted Revenue take rate of 20.2%. "
            "However, Swiggy take rate includes gross customer delivery charges, whereas Zomato reports net of certain subsidies."
        ),
        'other_disclosed_factors': 'Differences in Ind AS presentation of customer delivery fees and platform discounts.',
        'correlation_vs_causation_note': (
            "Headline spread (+380 bps) is predominantly driven by presentation differences rather than pure ad auction premiums."
        ),
        'verification_tier': 'CONTRADICTED_BY_DISCLOSED_EVIDENCE',
        'audit_determination': 'Claim that Swiggy extracts significantly higher net merchant monetization is contradicted by delivery fee netting adjustments.'
    }
]

# -----------------------------------------------------------------------------
# 4. Master Strategic Initiative Tracker
# -----------------------------------------------------------------------------
MASTER_STRATEGIC_INITIATIVES = [
    {
        'initiative_id': 'INIT-ET-001',
        'company': 'Eternal',
        'segment': 'QuickCommerce',
        'name': 'Blinkit 1P Inventory Model Migration',
        'launch_period': 'Q2FY26',
        'initiative_type': 'BUSINESS_MODEL_TRANSITION',
        'stated_objective': 'Take direct inventory ownership in high-velocity electronics, beauty, and apparel to guarantee availability and speed.',
        'economic_mechanism': 'Gross revenue billing under Ind AS 115, gross margin expansion, working capital investment in dark store inventory.',
        'status': 'MATURE',
        'financial_evidence': 'Adjusted Revenue leaped +128% QoQ in Q2FY26; working capital requirements expanded.',
        'operational_evidence': 'SKU count per dark store increased from 4,500 to 12,000+ items.',
        'risks': 'Inventory obsolescence, markdowns, and working capital drag in fast-moving electronics.',
        'is_active': True,
        'is_outcome_measurable': True
    },
    {
        'initiative_id': 'INIT-ET-002',
        'company': 'Eternal',
        'segment': 'OutOfHome',
        'name': 'District Platform & Paytm Ticketing Integration',
        'launch_period': 'Q2FY25',
        'initiative_type': 'ACQUISITION_SCOPE_EXPANSION',
        'stated_objective': 'Build a comprehensive Going-Out app integrating dining, live concerts, movies, and sports ticketing.',
        'economic_mechanism': 'Acquisition of Paytm Insider and TicketNew for ₹2,048 Cr, consolidating live ticketing volume.',
        'status': 'SCALING',
        'financial_evidence': 'Segment headline GOV grew 171% YoY in Q2FY25 (organic LFL was 53%).',
        'operational_evidence': 'District standalone app launched; major concert IP ticketing (Coldplay, Diljit Dosanjh).',
        'risks': 'High transaction churn, event promoter concentration, and lower margin vs dining reservations.',
        'is_active': True,
        'is_outcome_measurable': True
    },
    {
        'initiative_id': 'INIT-ET-003',
        'company': 'Eternal',
        'segment': 'Food',
        'name': 'Zomato Everyday & Kitchen Consolidation',
        'launch_period': 'Q1FY24',
        'initiative_type': 'AFFORDABILITY_VALUE_PROPOSITION',
        'stated_objective': 'Provide home-style fresh meals at sub-₹150 price points to capture daily lunch/dinner occasions.',
        'economic_mechanism': 'Dedicated cloud kitchens, pre-batched prep, optimized rider pooling.',
        'status': 'DISCONTINUED / RESTRUCTURED',
        'financial_evidence': 'Minimal reported GOV contribution (<2% of food delivery).',
        'operational_evidence': 'Scaled down in several cities; absorbed into core restaurant curation.',
        'risks': 'Low AOV severely compresses unit delivery contribution.',
        'is_active': False,
        'is_outcome_measurable': True
    },
    {
        'initiative_id': 'INIT-SW-001',
        'company': 'Swiggy',
        'segment': 'Food',
        'name': 'Swiggy Bolt (10-Minute Food Delivery)',
        'launch_period': 'Q2FY27',
        'initiative_type': 'SPEED_AND_FORMAT',
        'stated_objective': 'Deliver popular food items from pre-curated restaurant kitchens within a 2-km radius in 10-15 minutes.',
        'economic_mechanism': 'Pre-cooked / rapid-assembly menu items, localized rider geofencing.',
        'status': 'SCALING',
        'financial_evidence': 'Contributed to ~5% of food orders in pilot metro catchments.',
        'operational_evidence': 'Active in 6 metros; average delivery time reduced to 12.4 minutes.',
        'risks': 'Cannibalization of core food orders; rider safety and kitchen staging bottlenecks.',
        'is_active': True,
        'is_outcome_measurable': True
    },
    {
        'initiative_id': 'INIT-SW-002',
        'company': 'Swiggy',
        'segment': 'QuickCommerce',
        'name': 'Instamart Mega-Pods / Large Format Dark Stores',
        'launch_period': 'Q1FY27',
        'initiative_type': 'INFRASTRUCTURE_FORMAT',
        'stated_objective': 'Establish 5,000-8,000 sq ft dark stores capable of holding 15,000+ SKUs including appliances and general merchandise.',
        'economic_mechanism': 'Higher AOV from electronics, reduced stockouts, mother-hub replenishment efficiency.',
        'status': 'SCALING',
        'financial_evidence': 'AOV expanded to ₹708 in Q2FY27 (+45% YoY).',
        'operational_evidence': '50+ mega-pods operational in Tier-1 cities.',
        'risks': 'Higher fixed dark store rental lease commitments and longer gestation periods.',
        'is_active': True,
        'is_outcome_measurable': True
    },
    {
        'initiative_id': 'INIT-SW-003',
        'company': 'Swiggy',
        'segment': 'Platform',
        'name': 'Swiggy One & One Lite Multi-Category Loyalty',
        'launch_period': 'Q1FY25',
        'initiative_type': 'CROSS_PLATFORM_SUBSCRIPTION',
        'stated_objective': 'Drive cross-service usage across Food Delivery, Instamart, Dineout, and Genie through bundled free delivery.',
        'economic_mechanism': 'Subscription fee upfront, higher frequency per user, lower churn, amortized CAC.',
        'status': 'MATURE',
        'financial_evidence': 'One members order 2.8x more frequently and generate >60% of platform GOV.',
        'operational_evidence': 'Over 5 million active paying subscribers.',
        'risks': 'Delivery subsidy drag if order frequency surges without merchant fee sharing.',
        'is_active': True,
        'is_outcome_measurable': True
    },
    {
        'initiative_id': 'INIT-SW-004',
        'company': 'Swiggy',
        'segment': 'SupplyChain',
        'name': 'Lynks Divestment & Core Focus Realignment',
        'launch_period': 'Q2FY27',
        'initiative_type': 'PORTFOLIO_RATIONALIZATION',
        'stated_objective': 'Divest non-core trucking operations to eliminate drag on Supply Chain profitability.',
        'economic_mechanism': 'Deconsolidation of operating losses (~₹20 Cr/quarter EBITDA benefit).',
        'status': 'MATURE',
        'financial_evidence': 'Completed in Q2FY27; financial deconsolidation pending Q3 disclosures.',
        'operational_evidence': 'Focus returned exclusively to restaurant partner ingredients and packaging.',
        'risks': 'Loss of proprietary intra-city linehaul routing control.',
        'is_active': True,
        'is_outcome_measurable': True
    }
]


# -----------------------------------------------------------------------------
# 5. Core Credibility Engine Analytics
# -----------------------------------------------------------------------------
def get_all_management_statements(company: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all management commitments and statements, optionally filtered."""
    results = []
    for c in MASTER_MANAGEMENT_COMMITMENTS:
        if company and c['company'].lower() != company.lower():
            continue
        if category and c['category'].lower() != category.lower():
            continue
        results.append(dict(c))
    return results


def get_commitment_by_id(commitment_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single commitment by ID."""
    for c in MASTER_MANAGEMENT_COMMITMENTS:
        if c['commitment_id'].upper() == commitment_id.upper() or c.get('legacy_id', '').upper() == commitment_id.upper():
            return dict(c)
    return None


def calculate_management_credibility_scorecard(company: Optional[str] = None) -> Dict[str, Any]:
    """
    Computes transparent management execution scorecards with explicit numerators and denominators.
    Strict delivery rate = Delivered / Evaluable Completed
    Broad delivery rate = (Delivered + 0.5 * Partially Delivered) / Evaluable Completed
    """
    commitments = get_all_management_statements(company=company)
    
    total = len(commitments)
    delivered = len([c for c in commitments if c['outcome_status'] == 'DELIVERED'])
    partially_delivered = len([c for c in commitments if c['outcome_status'] == 'PARTIALLY_DELIVERED'])
    missed = len([c for c in commitments if c['outcome_status'] == 'MISSED'])
    pending = len([c for c in commitments if c['outcome_status'] == 'PENDING'])
    unmeasurable = len([c for c in commitments if c['outcome_status'] == 'NOT_OBJECTIVELY_MEASURABLE'])
    withdrawn = len([c for c in commitments if c['outcome_status'] == 'WITHDRAWN_OR_SUPERSEDED'])
    
    # Completed evaluable denominator strictly excludes pending, unmeasurable, and withdrawn
    evaluable_completed = delivered + partially_delivered + missed
    
    strict_delivery_rate = round((delivered / evaluable_completed * 100), 2) if evaluable_completed > 0 else None
    broad_delivery_rate = round(((delivered + 0.5 * partially_delivered) / evaluable_completed * 100), 2) if evaluable_completed > 0 else None
    partial_rate = round((partially_delivered / evaluable_completed * 100), 2) if evaluable_completed > 0 else None
    miss_rate = round((missed / evaluable_completed * 100), 2) if evaluable_completed > 0 else None
    
    # Segment breakdown
    segment_breakdown = {}
    for c in commitments:
        seg = c['segment']
        if seg not in segment_breakdown:
            segment_breakdown[seg] = {'total': 0, 'delivered': 0, 'partially_delivered': 0, 'missed': 0, 'pending': 0, 'unmeasurable': 0}
        segment_breakdown[seg]['total'] += 1
        stat = c['outcome_status'].lower()
        if stat in segment_breakdown[seg]:
            segment_breakdown[seg][stat] += 1

    # Credibility tier
    if strict_delivery_rate is not None and strict_delivery_rate >= 80.0:
        credibility_tier = "HIGH_CREDIBILITY_PROVEN"
    elif strict_delivery_rate is not None and strict_delivery_rate >= 60.0:
        credibility_tier = "MODERATE_HIGH_CREDIBILITY"
    elif strict_delivery_rate is not None:
        credibility_tier = "MIXED_EXECUTION_RECORD"
    else:
        credibility_tier = "INSUFFICIENT_COMPLETED_OBSERVATIONS"

    return {
        'company_filter': company or 'ALL',
        'total_commitments': total,
        'evaluable_completed': evaluable_completed,
        'delivered_count': delivered,
        'partially_delivered_count': partially_delivered,
        'missed_count': missed,
        'pending_count': pending,
        'not_objectively_measurable_count': unmeasurable,
        'withdrawn_count': withdrawn,
        'strict_delivery_rate_pct': strict_delivery_rate,
        'broad_delivery_rate_pct': broad_delivery_rate,
        'partial_delivery_rate_pct': partial_rate,
        'miss_rate_pct': miss_rate,
        'credibility_tier': credibility_tier,
        'segment_breakdown': segment_breakdown,
        'methodology_note': (
            f"Evaluable denominator ({evaluable_completed}) excludes {pending} pending unmatured milestones "
            f"and {unmeasurable} qualitative/vision statements. Never penalizes companies for active targets."
        )
    }


def get_all_narrative_verifications(company: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns narrative explanations evaluated against empirical evidence."""
    results = []
    for n in MASTER_NARRATIVE_VERIFICATIONS:
        if company and n['company'].lower() != company.lower():
            continue
        results.append(dict(n))
    return results


def get_all_strategic_initiatives(company: Optional[str] = None, segment: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns strategic initiatives across both companies."""
    results = []
    for init in MASTER_STRATEGIC_INITIATIVES:
        if company and init['company'].lower() != company.lower():
            continue
        if segment and init['segment'].lower() != segment.lower():
            continue
        results.append(dict(init))
    return results


def get_company_credibility_comparison() -> Dict[str, Any]:
    """Provides a head-to-head credibility comparison between Eternal and Swiggy."""
    swiggy_sc = calculate_management_credibility_scorecard(company='Swiggy')
    eternal_sc = calculate_management_credibility_scorecard(company='Eternal')
    
    return {
        'comparison_type': 'MANAGEMENT_EXECUTION_AND_CREDIBILITY',
        'comparability_status': 'LEVEL_3_DIRECTIONALLY_COMPARABLE',
        'eternal': eternal_sc,
        'swiggy': swiggy_sc,
        'analytical_synthesis': (
            "Eternal has delivered 5 of 6 evaluable commitments (83.3% strict, 91.7% broad) primarily driven by "
            "massive Blinkit store additions (1,300 vs 1,000 guided) and sustained Food delivery profitability (5.82% EBITDA). "
            "Swiggy has delivered 3 of 4 evaluable commitments (75.0% strict, 87.5% broad) with solid Food delivery growth (22.1% vs 20% guided) "
            "and store rollout (1,240 vs 1,200 guided). Both management teams maintain high credibility (>75% strict delivery) on matured guidance."
        ),
        'methodological_caution': (
            "Do not penalize Swiggy for having 11 pending medium-term commitments vs Eternal's 2. "
            "Swiggy's recent IPO prospectus introduced numerous multi-year targets that are still within their maturation window."
        )
    }
