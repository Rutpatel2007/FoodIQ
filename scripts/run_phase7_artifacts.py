"""
Generates Phase 7 test and validation artifacts:
1. reports/phase7_test_results.json
2. reports/phase7_report_validation.json
3. reports/phase7_citation_audit.csv
"""

import os
import sys
sys.path.insert(0, ".")
import json
import csv
import time
from datetime import datetime, timezone
import pytest

from backend.app.analytics.report_engine import (
    generate_institutional_report,
    REPORT_TYPES
)

class Phase7TestCollector:
    def __init__(self):
        self.results = []

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.results.append({
                "nodeid": report.nodeid,
                "name": report.location[2],
                "outcome": report.outcome,
                "duration": round(report.duration, 4)
            })

def main():
    collector = Phase7TestCollector()
    start_time = time.time()
    exit_code = pytest.main([
        "-v",
        "backend/tests/test_phase7_reporting_engine.py"
    ], plugins=[collector])
    total_time = round(time.time() - start_time, 4)

    test_summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": "PHASE_7_REPORTING_ENGINE",
        "total_tests": len(collector.results),
        "passed": sum(1 for r in collector.results if r["outcome"] == "passed"),
        "failed": sum(1 for r in collector.results if r["outcome"] == "failed"),
        "duration_seconds": total_time,
        "exit_code": int(exit_code),
        "verdict": "PASS" if exit_code == 0 else "FAIL",
        "tests": collector.results
    }

    with open("reports/phase7_test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_summary, f, indent=2)

    # Generate a reference Comprehensive Report to validate
    comp_rep = generate_institutional_report(
        report_type="COMPREHENSIVE",
        period_cutoff="Q2FY27",
        author="Principal Research Auditor"
    )

    validation_summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "report_id": comp_rep["report_id"],
        "report_type": comp_rep["report_type"],
        "title": comp_rep["title"],
        "total_sections": comp_rep["total_sections"],
        "verification_status": comp_rep["verification_status"],
        "verification_scorecard": comp_rep["verification_scorecard"],
        "citation_verification": comp_rep["citation_verification"]
    }

    with open("reports/phase7_report_validation.json", "w", encoding="utf-8") as f:
        json.dump(validation_summary, f, indent=2)

    # Citation audit CSV
    cit_audit = comp_rep["citation_verification"]["audit_records"]
    with open("reports/phase7_citation_audit.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company", "Source Document", "Page Reference", "Metric / Quote", "Resolution Status"])
        for r in cit_audit:
            writer.writerow([r["company"], r["source_doc"], r["page"], r["metric"], r["resolution_status"]])

    print("Phase 7 test results, report validation, and citation audit CSV generated.")

if __name__ == "__main__":
    main()
