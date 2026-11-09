# FoodIQ v1.1 — Testing, Verification & QA Manual
**Document Reference:** DOC-V11-11  
**Classification:** Quality Assurance & Continuous Integration  

---

## 1. Test Suite Architecture

The FoodIQ test suite contains 145 comprehensive pytest cases organized into 19 modules across `backend/tests/`:

- `test_metrics.py`: Mathematical validation of metrics and reconciliations.
- `test_analytics.py`: Margin bridges, unit economics, and throughput formulas.
- `test_econometrics.py`: Studies REL-001–012, FDR correction, and OLS regressions.
- `test_credibility.py`: Management credibility scorecards and commitment tracking.
- `test_comparability.py`: Enforcement of 4-tier comparability rules.
- `test_lineage.py`: Coordinate grounding and PDF bounding box extraction.
- `test_scenarios.py`: Monte Carlo simulations and AOV elasticity curves.
- `test_security.py`: Parameterized queries, path traversal, and bounds checking.

---

## 2. Test Execution Command

To execute the complete regression test suite:
```bash
pytest backend/tests/ -v
```

**Verified Test Performance:**
- Total Tests: 145
- Total Test Functions: 158
- Pass Rate: 100% (0 failures, 0 errors)
- Execution Duration: 185.56s
