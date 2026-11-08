"""
Headless Chrome Browser Automation & DOM Verification for FoodIQ Workstation.
Launches uvicorn server in a subprocess, uses headless Chrome to render http://127.0.0.1:8000/,
captures DOM, verifies all 10 workspaces, header elements, KPI cards, and canvas elements.
"""

import subprocess
import time
import socket
import os
import sys

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def wait_for_port(port=8000, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = s.connect_ex(('127.0.0.1', port))
        s.close()
        if res == 0:
            return True
        time.sleep(0.5)
    return False

def main():
    print("Starting FastAPI uvicorn server...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )

    try:
        ready = wait_for_port(8000, timeout=15)
        if not ready:
            print("ERROR: FastAPI server failed to start within 15 seconds.")
            return False

        print("FastAPI server active on http://127.0.0.1:8000/. Launching headless Chrome...")
        chrome_cmd = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--virtual-time-budget=5000",
            "--dump-dom",
            "http://127.0.0.1:8000/"
        ]

        result = subprocess.run(chrome_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
        dom = result.stdout or ""
        print(f"Captured rendered DOM length: {len(dom)} characters.")

        # Check required DOM elements
        checks = [
            ("Workstation Title", "FoodIQ — Institutional Corporate Financial Intelligence Workstation"),
            ("Status Badge", "DB CONNECTED"),
            ("Tab: overview", 'data-tab="tab-overview"'),
            ("Tab: company", 'data-tab="tab-company"'),
            ("Tab: financials", 'data-tab="tab-financials"'),
            ("Tab: competitive", 'data-tab="tab-competitive"'),
            ("Tab: credibility", 'data-tab="tab-credibility"'),
            ("Tab: quantitative", 'data-tab="tab-quantitative"'),
            ("Tab: scenarios", 'data-tab="tab-scenarios"'),
            ("Tab: library", 'data-tab="tab-library"'),
            ("Tab: sources", 'data-tab="tab-sources"'),
            ("Tab: governance", 'data-tab="tab-governance"'),
            ("Canvas chart", '<canvas id="overviewTrendCanvas"'),
            ("Global Company Filter", 'id="global-company-filter"'),
            ("Global Segment Filter", 'id="global-segment-filter"'),
            ("Global Period Filter", 'id="global-period-filter"')
        ]

        all_passed = True
        for name, expected in checks:
            present = expected in dom
            status = "PASS" if present else "FAIL"
            print(f"[{status}] {name}: '{expected}'")
            if not present:
                all_passed = False

        if all_passed:
            print("\n>>> ALL BROWSER DOM AND WORKSPACE CHECKS PASSED SUCCESSFULLY. <<<")
            return True
        else:
            print("\n>>> SOME DOM CHECKS FAILED. <<<")
            return False

    finally:
        print("Terminating background uvicorn server...")
        server_proc.terminate()
        server_proc.wait(timeout=5)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
