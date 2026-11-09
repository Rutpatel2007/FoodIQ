import sys
sys.path.insert(0, '.')
import backend.app.analytics.credibility_engine as ce

for co in ['ALL', 'Eternal', 'Swiggy']:
    res = ce.calculate_management_credibility_scorecard(company_filter=co)
    print(f"=== {co} ===")
    print(f"  Total: {res['total_commitments']}, Evaluable: {res['evaluable_completed']}")
    print(f"  Delivered: {res['delivered_count']}, Partial: {res['partially_delivered_count']}, Missed: {res['missed_count']}")
    print(f"  Pending: {res['pending_count']}, Not Measurable: {res['not_objectively_measurable_count']}")
    print(f"  Strict Delivery Rate: {res['strict_delivery_rate_pct']}%, Broad Delivery Rate: {res['broad_delivery_rate_pct']}%")
    print(f"  Credibility Tier: {res['credibility_tier']}")
