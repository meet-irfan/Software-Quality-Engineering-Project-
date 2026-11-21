"""Run the whole suite 3 times and build the Task 5 table.

Usage:   python run_three_times.py            (extra pytest options are passed through,
         python run_three_times.py --browser-name firefox     e.g. a different browser)

Output:  reports/report_run1.html ... report_run3.html, reports/run_summary.csv/.md
"""
import csv
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
RUNS = 3


def run_once(number: int) -> dict:
    REPORTS.mkdir(exist_ok=True)
    xml_file = REPORTS / f"run{number}.xml"
    html_file = REPORTS / f"report_run{number}.html"
    started = datetime.now()

    subprocess.run(
        [
            sys.executable, "-m", "pytest",
            f"--junitxml={xml_file}",
            f"--html={html_file}",
            "--self-contained-html",
            *sys.argv[1:],
        ],
        cwd=ROOT,
    )

    root = ET.parse(xml_file).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    total = int(suite.get("tests"))
    failed = int(suite.get("failures")) + int(suite.get("errors"))
    skipped = int(suite.get("skipped"))
    seconds = float(suite.get("time"))
    return {
        "run": number,
        "date_time": started.strftime("%d-%m-%Y %H:%M"),
        "total": total,
        "passed": total - failed - skipped,
        "failed": failed,
        "skipped": skipped,
        "duration": f"{int(seconds // 60)}m {seconds % 60:.0f}s",
    }


def main() -> None:
    rows = [run_once(n) for n in range(1, RUNS + 1)]

    with (REPORTS / "run_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "| Run | Date / time | Total | Passed | Failed | Skipped | Duration |",
        "|-----|-------------|-------|--------|--------|---------|----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['run']} | {r['date_time']} | {r['total']} | {r['passed']} | "
            f"{r['failed']} | {r['skipped']} | {r['duration']} |"
        )
    table = "\n".join(lines)
    (REPORTS / "run_summary.md").write_text(table + "\n", encoding="utf-8")
    print("\n" + table)


if __name__ == "__main__":
    main()
