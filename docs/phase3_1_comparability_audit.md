# FoodIQ Phase 3.1: Independent Comparability Governance Audit

## 1. Executive Summary & Framework

The **FoodIQ Formal Comparability Engine** provides an auditable, programmatic classification system for cross-company peer metrics. 

The engine categorizes comparisons into 4 strict epistemic tiers:
1. **LEVEL 1: DIRECTLY COMPARABLE** (Identical accounting definitions, reporting scope, and units. Direct subtraction and ratio calculation permitted).
2. **LEVEL 2: COMPARABLE WITH ADJUSTMENT** (Valid only after applying a documented mathematical normalization).
3. **LEVEL 3: DIRECTIONALLY COMPARABLE** (Trends, trajectories, and growth rates can be benchmarked; absolute levels differ due to corporate overhead allocations or gross vs. net presentation).
4. **LEVEL 4: INCOMPARABLE** (Fundamentally different accounting standards or commercial models. **Direct subtraction and peer rankings are strictly blocked at the computational layer**).

---

## 2. Audit of the Master Comparability Rulebook (10 Rules)

The audit team verified each rule in `MASTER_COMPARABILITY_REGISTRY` against corporate disclosures and accounting standards:

| Rule ID | Segment | Metric Name | Level | Direct Subtraction Permitted? | Adjustment Required? | Accounting Standard / Basis | Audit Verdict |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **RULE-COMP-001** | QuickCommerce | `dark_stores` | **L1** | Yes | No | Physical active store count at quarter end | **PASSED** |
| **RULE-COMP-002** | QuickCommerce | `nov_cr` | **L1** | Yes | No | Net Order Value post-vouchers (Ind AS 115) | **PASSED** |
| **RULE-COMP-003** | QuickCommerce | `adj_revenue_cr` (Pre-Q2FY26) | **L2** | Yes | Yes | 3P Marketplace Commission Model | **PASSED** |
| **RULE-COMP-004** | QuickCommerce | `adj_revenue_cr` (Post-Q1FY26) | **L4** | **STRICTLY BLOCKED** | No | 1P Gross (Blinkit) vs 3P Net (Swiggy) | **PASSED (BLOCKED)** |
| **RULE-COMP-005** | Food | `gov_cr` | **L1** | Yes | No | Gross checkout billings incl taxes/delivery | **PASSED** |
| **RULE-COMP-006** | Food | `cross_gov_nov` | **L4** | **STRICTLY BLOCKED** | No | Gross checkout vs Net transacted flow | **PASSED (BLOCKED)** |
| **RULE-COMP-007** | Food | `adj_ebitda_margin_pct` | **L3** | No (Directional) | No | Segment EBITDA on GOV (overhead variation) | **PASSED** |
| **RULE-COMP-008** | Food | `mtu_mn` | **L2** | Yes | Yes | 3-month average monthly unique users | **PASSED** |
| **RULE-COMP-009** | OutOfHome | `adj_revenue_cr` | **L2** | Yes | Yes | Dining directory vs Ticketing acquisition | **PASSED** |
| **RULE-COMP-010** | SupplyChain | `adj_revenue_cr` | **L2** | Yes | Yes | Hyperpure eliminations vs Lynks divestment | **PASSED** |

---

## 3. Strict Verification of Level 4 Computational Blocking

### 3.1 RULE-COMP-004: Post-Q1FY26 Quick Commerce Adjusted Revenue
- **Accounting Conflict:** In Q2 FY26, Blinkit shifted to 1P inventory ownership (Ind AS 115 principal gross billing), while Swiggy Instamart remained a 3P marketplace agent.
- **Audit Verification of Code Enforcement:**
  In `backend/app/analytics/competitive_attribution.py`:
  ```python
  if comp_level == 'LEVEL_4':
      gap_abs = None
      gap_pct = None
      gap_dir = "INCOMPARABLE_ACCOUNTING_BREAK"
      leader = "BLOCKED"
      is_blocked = True
  ```
- **Test Result:** Verified across all quarters from Q2 FY26 to Q2 FY27. When querying the peer gap for Quick Commerce Adjusted Revenue, `gap_absolute` is `None`, and `leader` is `'BLOCKED'`.
- **Integrity Guarantee:** Prohibits naive financial models from claiming "Blinkit is 6x larger than Swiggy in revenue."

### 3.2 RULE-COMP-006: Cross-GOV vs NOV Subtraction
- **Accounting Conflict:** Gross Order Value includes customer vouchers, delivery fees, and taxes. Net Order Value is net of customer discounts.
- **Audit Verification:** Cross-subtraction yields promotional voucher spend and taxes, not an operational market share gap. The engine rejects cross-metric comparisons at the router and computation layer.

---

## 4. Directional Benchmarking Governance (Level 3)

### RULE-COMP-007: Food Adjusted EBITDA Margins
- **Reporting Discrepancy:** Eternal leaves certain corporate executive overhead unallocated across business segments, whereas Swiggy's segment allocations reflect different platform cost apportionments.
- **Audit Enforcement:** The platform permits directional trajectory benchmarking (e.g., Swiggy expanded food margins +260 bps vs Eternal's +187 bps) but flags absolute margin spreads (e.g. 242 bps) as subject to corporate overhead allocation conventions.
