import os
import sys
import json
import subprocess
import time

def run_tests_and_record():
    start = time.time()
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "backend/tests/", "-v"],
        capture_output=True,
        text=True
    )
    duration = time.time() - start
    print("Pytest stdout tail:")
    print("\n".join(res.stdout.splitlines()[-25:]))
    
    test_lines = [l for l in res.stdout.splitlines() if "::" in l and ("PASSED" in l or "FAILED" in l)]
    tests_detail = []
    for tl in test_lines:
        parts = tl.split()
        if len(parts) >= 2:
            tests_detail.append({
                "test_name": parts[0],
                "status": parts[1]
            })
            
    passed = len([t for t in tests_detail if "PASSED" in t['status']])
    failed = len([t for t in tests_detail if "FAILED" in t['status']])
    
    data = {
        "test_suite": "FoodIQ Backend Test Suite (Phases 1, 2, 2.1, 3, 3.1)",
        "timestamp": "2026-11-08T12:23:00Z",
        "exit_code": res.returncode,
        "duration_seconds": round(duration, 2),
        "total_collected": len(tests_detail),
        "total_passed": passed,
        "total_failed": failed,
        "all_tests_passed": res.returncode == 0 and failed == 0,
        "test_cases": tests_detail
    }
    with open("reports/phase3_1_test_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {passed} passed tests to reports/phase3_1_test_results.json")

if __name__ == '__main__':
    run_tests_and_record()
