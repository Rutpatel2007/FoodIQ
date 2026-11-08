import sys, os, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.database import SessionLocal
from backend.app.models.metrics import MetricObservation, MetricDefinition
from backend.app.analytics.competitive_findings import get_all_competitive_findings
from backend.app.analytics.credibility_engine import calculate_management_credibility_scorecard
from backend.app.analytics.statistical_research import get_all_relationship_studies_with_fdr, get_all_research_workbench_questions
from backend.app.analytics.scenario_lab import run_monte_carlo_simulation, compute_breakeven_analysis
from backend.app.analytics.report_engine import generate_institutional_report
from backend.app.analytics.disclosure_intelligence import get_disclosure_monitoring_overview
from backend.app.analytics.extension_framework import registry

db = SessionLocal()

print("=== TRACING 8 WORKFLOWS ===")
# WF 1: Financial Research (Food Delivery)
t0 = time.time()
obs_count = db.query(MetricObservation).filter(MetricObservation.segment_id.in_(['ETERNAL_FOOD', 'SWIGGY_FOOD'])).count()
t1 = time.time()
print(f"WF1: Food Delivery observations count={obs_count} in {(t1-t0)*1000:.2f}ms")

# WF 2: Quick Commerce (Blinkit vs Instamart)
t0 = time.time()
findings = get_all_competitive_findings()
t1 = time.time()
print(f"WF2: Competitive findings generated={len(findings)} in {(t1-t0)*1000:.2f}ms")

# WF 3: Management Credibility
t0 = time.time()
scorecard_eternal = calculate_management_credibility_scorecard(company="ETERNAL")
scorecard_swiggy = calculate_management_credibility_scorecard(company="SWIGGY")
t1 = time.time()
print(f"WF3: Credibility scorecards: Eternal={scorecard_eternal.get('evaluable_completed')}/{scorecard_eternal.get('delivered_count')} ({scorecard_eternal.get('strict_delivery_rate_pct')}%), Swiggy={scorecard_swiggy.get('evaluable_completed')}/{scorecard_swiggy.get('delivered_count')} (pending={scorecard_swiggy.get('pending_count')}, {scorecard_swiggy.get('strict_delivery_rate_pct')}%) in {(t1-t0)*1000:.2f}ms")

# WF 4: Quantitative Research
t0 = time.time()
studies = get_all_relationship_studies_with_fdr()
questions = get_all_research_workbench_questions()
t1 = time.time()
print(f"WF4: Quantitative studies={len(studies)}, workbench questions={len(questions)} in {(t1-t0)*1000:.2f}ms")

# WF 5: Scenario Modelling
t0 = time.time()
be = compute_breakeven_analysis('SWIGGY', 'QUICK_COMMERCE')
mc = run_monte_carlo_simulation('SWIGGY', 'QUICK_COMMERCE', 1000)
t1 = time.time()
print(f"WF5: Instamart break-even AOV={be.get('breakeven_aov')} (mean simulated CM={mc.get('mean_contribution_margin_pct')}%) in {(t1-t0)*1000:.2f}ms")

# WF 6: Report Generation
t0 = time.time()
rep = generate_institutional_report(report_type='COMPREHENSIVE')
t1 = time.time()
print(f"WF6: Report generated ID={rep.get('report_id')} in {(t1-t0)*1000:.2f}ms")

# WF 7: Disclosure Intelligence
t0 = time.time()
filings = get_disclosure_monitoring_overview()
t1 = time.time()
print(f"WF7: Disclosure overview total filings={filings.get('total_disclosures_tracked')} in {(t1-t0)*1000:.2f}ms")

# WF 8: Extensions Framework
t0 = time.time()
comps = registry.list_companies()
mods = registry.list_modules()
t1 = time.time()
print(f"WF8: Extensible framework: {len(comps)} companies, {len(mods)} modules in {(t1-t0)*1000:.2f}ms")

db.close()
