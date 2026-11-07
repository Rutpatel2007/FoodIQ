# FoodIQ — Data dictionary and analytical methods

## Observation model

Every observation should store: company, quarter, fiscal year, quarter number, period end, segment, metric name, value, unit, scope, denominator/basis, source document, physical PDF page, printed page where available, extraction method, report version, value status (`reported`, `derived`, `management_estimate`, `user_seed_unverified`, `model_assumption`), and reviewer notes.

The long-form source dataset is canonical. Wide panels are convenience exports, never the only source of truth.

## Scope hierarchy

- `B2C`: Food Delivery + Quick Commerce + Out-of-Home; excludes Platform Innovations. B2C GOV and B2C Adjusted Revenue are different measures.
- `Consolidated`: full group financial statement / adjusted revenue / adjusted EBITDA perimeter, including non-B2C/platform innovation and distribution activity as reported.
- `Food`, `QuickCommerce`, `OutOfHome`, `SupplyChain`, `PlatformInnovations`: segment-level metrics.

Do not assume segment metrics add exactly to consolidated metrics: eliminations, corporate/other items and scope definitions may apply.

## Metric semantics

- GOV: Gross Order Value of completed orders for the relevant consumer-facing segment.
- NOV: Net Order Value after discounts; Swiggy publishes Quick Commerce NOV / NOV-to-GOV information. Food Delivery and Out-of-Home NOV are not published in the supplied letters.
- Adjusted Revenue: company-defined segment or consolidated adjusted revenue. Preserve source-level definitions and reconciliation; do not interchange with statutory revenue from operations.
- Adjusted EBITDA: company-defined adjusted EBITDA, excluding items listed in the source definition (including other income, exceptional items, share in net loss of associate, share-based payment expense and Ind AS 116 rental expenses, as described in the letter).
- Contribution Margin: segment-level margin with denominator normally GOV for Food/Quick Commerce/Out-of-Home. Store the exact numerator/denominator definition from the corresponding letter and segment, including variable-cost differences.
- Adjusted EBITDA margin: denominator varies; Food/QuickCommerce/OutOfHome as % GOV, Platform B2C adjusted EBITDA as % B2C GOV, SupplyChain as % revenue, PlatformInnovations as % adjusted revenue.
- AOV: source KPI average order value. Preserve units and whether GOV/order is stated or computed.
- nAOV: separate source term used in management commentary; definition is not fully pinned down in the current extraction. Do not substitute for AOV.
- MTU: monthly transacting users; can refer to platform-wide or segment-level MTU. Prefix field with platform/segment scope.
- RPO: adjusted revenue per order, as described by management. Keep separate from take rate.
- Orders/store/day: source KPI based on active darkstore-days; not total orders divided by period-end store count.

## Recommended core calculations

### Growth

`YoY % = (value_t / value_t-4 - 1) * 100` for quarterly data, only where scope/definition is comparable.

`QoQ % = (value_t / value_t-1 - 1) * 100`; annotate seasonality and quarter length / report scope.

### GOV decomposition (Food and Quick Commerce)

Where GOV is reasonably represented by order count × AOV:

`ΔGOV = (ΔOrders × prior_AOV) + (ΔAOV × current_Orders)`

Use unit conversion carefully: when orders are in millions and AOV in INR, `INR crore = orders_mn × AOV_inr / 100`.

This is an exact two-factor allocation under the stated convention; disclose that the cross-term is assigned to the AOV/price-mix component if using the alternative convention. Validate against reported GOV and rounding. Avoid using an AOV decomposition on OOH without order count/AOV evidence.

### Monetary contribution margin

`Contribution_Margin_INR_cr = GOV_cr × contribution_margin_pct / 100`.

This makes the margin trend interpretable in currency, but is not a driver decomposition. A valid driver bridge requires source-disclosed cost/revenue components with matching scope and denominator.

### Adjusted EBITDA margin

`Adjusted_EBITDA_margin_pct = adjusted_ebitda_cr / (GOV_cr or Revenue_cr or Adjusted_Revenue_cr) × 100` only when the report defines that denominator. Store denominator as data, not a code assumption.

### Quick Commerce NOV

`NOV/GOV` is reported as a rounded percentage in the KPI chart. `NOV_cr = GOV_cr × NOV/GOV` is an estimate when only the rounded ratio is available, not an exact reported NOV value. Prefer directly reported NOV values from narrative / table; never convert rounded ratio into a “reported” value.

### Margin driver bridge

Q2FY27 management attributed QComm CM change to approximately -100bps user habit investment, -40bps user/category mix, +60bps operating leverage/efficiencies. Record this in a separate management-attribution table. The components sum to approximately -80bps; the reported change is -82bps, so preserve the ~2bps unallocated/rounding residual. Do not merge with an independently calculated cost bridge.

### Guidance scorecard

Each target needs type, scope, issuance date, target time window, target threshold/range, actual observation, and explicit status. Categories: annual formal guidance, near-term guidance, scale threshold, medium-term ambition, long-term aspiration, qualitative strategy. Statuses: pending, achieved at milestone, within range, approximately met, missed, not assessable. Do not mark long-term aspirations as missed.

### Scenario analysis

Use transparent input parameters and sensitivity ranges for order growth, AOV, discounts, take rate, RPO, delivery cost/order, store utilisation, inventory ownership and working capital. Keep management targets separate from independent FoodIQ assumptions. Show base/downside/upside, break-even boundaries, and sensitivity tornado/waterfall. No single hardcoded elasticity should be used without calibration and uncertainty bounds.

## Statistical testing

- Pair Eternal quarter `t` with Swiggy quarter `t+1` using an explicit join on fiscal-quarter sequence; do not rely on ambiguous SQL `LAG()` across a filtered series.
- Report lag-0, lag-1 and lag-2 associations; Pearson and Spearman where sensible; first-difference / YoY-growth robustness; confidence intervals and sample size.
- With small `n`, label analyses exploratory and do not use “predicts” or “causes” absent stronger out-of-sample validation.
