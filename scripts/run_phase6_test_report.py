import json
import time
from datetime import datetime, timezone
import pytest

class TestResultCollector:
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
    collector = TestResultCollector()
    start_time = time.time()
    exit_code = pytest.main([
        "-v",
        "backend/tests/test_phase6_workstation_integration.py"
    ], plugins=[collector])
    total_time = round(time.time() - start_time, 4)

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": "PHASE_6_INSTITUTIONAL_WORKSTATION",
        "total_tests": len(collector.results),
        "passed": sum(1 for r in collector.results if r["outcome"] == "passed"),
        "failed": sum(1 for r in collector.results if r["outcome"] == "failed"),
        "duration_seconds": total_time,
        "exit_code": int(exit_code),
        "verdict": "PASS" if exit_code == 0 else "FAIL",
        "tests": collector.results
    }

    with open("reports/phase6_e2e_test_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Phase 6 test results generated: {summary['passed']}/{summary['total_tests']} passed.")

if __name__ == "__main__":
    main()
