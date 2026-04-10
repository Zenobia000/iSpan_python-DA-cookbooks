"""
自動評分引擎（多模組版）
========================
1. 跑 pytest，收集每個 test 的 pass/fail
2. 按模組分組計分
3. 產生 Markdown 報告
4. 輸出到 GitHub Actions Job Summary / PR comment

用法：
  python grader/run_grader.py                  # 含解答（學生 fork 端）
  python grader/run_grader.py --no-solutions   # 不含解答（老師 PR 端）
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# 各模組的分數設定
# ============================================================
MODULES = {
    "M1 NumPy": {
        "test_file": "test_m1",
        "solution_module": "solutions.m1_solutions",
        "scores": {
            "test_green_mean": 10,
            "test_green_double": 10,
            "test_green_filter": 10,
            "test_yellow_expensive_count": 15,
            "test_yellow_top3_stock_indices": 15,
            "test_yellow_restock_cost": 15,
            "test_red_double11_prices": 20,
            "test_red_no_forloop": 5,
        },
    },
    "M2 Pandas 清理": {
        "test_file": "test_m2",
        "solution_module": "solutions.m2_solutions",
        "scores": {
            "test_green_read_csv": 10,
            "test_green_shape": 10,
            "test_green_dtypes": 10,
            "test_yellow_clean_columns": 15,
            "test_yellow_clean_amount": 15,
            "test_yellow_drop_duplicates": 15,
            "test_red_clean_orders_returns_df": 4,
            "test_red_clean_orders_columns": 4,
            "test_red_clean_orders_amount_is_numeric": 4,
            "test_red_clean_orders_date_is_datetime": 5,
            "test_red_clean_orders_no_nulls": 4,
            "test_red_clean_orders_no_duplicates": 4,
        },
    },
    "M3 Pandas 進階": {
        "test_file": "test_m3",
        "solution_module": "solutions.m3_solutions",
        "scores": {
            "test_green_load_and_merge": 10,
            "test_green_row_count": 10,
            "test_green_column_list": 10,
            "test_yellow_top_category": 15,
            "test_yellow_gold_vip_stats": 15,
            "test_yellow_region_avg_amount": 15,
            "test_red_rfm_top5_shape": 9,
            "test_red_rfm_top5_columns": 8,
            "test_red_rfm_top5_sorted_by_m": 8,
        },
    },
    "M4 時間序列": {
        "test_file": "test_m4",
        "solution_module": "solutions.m4_solutions",
        "scores": {
            "test_green_avg_by_month": 10,
            "test_green_top3_dates": 10,
            "test_green_date_range": 10,
            "test_yellow_monthly_revenue": 15,
            "test_yellow_rolling_avg": 15,
            "test_yellow_category_median": 15,
            "test_red_monthly_report_columns": 9,
            "test_red_monthly_report_values": 8,
            "test_red_monthly_report_growth": 8,
        },
    },
    "M5 視覺化": {
        "test_file": "test_m5",
        "solution_module": "solutions.m5_solutions",
        "scores": {
            "test_green_bar_category": 10,
            "test_green_hist_amount": 10,
            "test_green_set_labels": 10,
            "test_yellow_line_region_trend": 15,
            "test_yellow_box_vip": 15,
            "test_yellow_scatter_price_amount": 15,
            "test_red_category_dashboard_is_figure": 13,
            "test_red_category_dashboard_has_4_subplots": 12,
        },
    },
    "M6 Plotly Capstone": {
        "test_file": "test_m6",
        "solution_module": "solutions.m6_solutions",
        "scores": {
            "test_green_plotly_bar": 10,
            "test_green_plotly_line": 10,
            "test_green_plotly_pie": 10,
            "test_yellow_clean_and_merge": 15,
            "test_yellow_kpi_summary": 15,
            "test_yellow_plotly_scatter": 15,
            "test_red_dashboard_is_figure": 13,
            "test_red_dashboard_has_traces": 12,
        },
    },
}

# 全部 test name → 分數的平面 map（向後相容）
ALL_SCORES = {}
for mod in MODULES.values():
    ALL_SCORES.update(mod["scores"])


def run_pytest() -> dict:
    """執行 pytest，回傳 {test_name: {"passed": bool, "message": str, "nodeid": str}}"""
    result_file = ROOT / ".pytest_results.json"
    cmd = [
        sys.executable, "-m", "pytest",
        str(ROOT / "tests"),
        "--tb=short",
        "--json-report",
        f"--json-report-file={result_file}",
        "-v",
    ]

    subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)

    if not result_file.exists():
        return _run_pytest_fallback()

    with open(result_file) as f:
        data = json.load(f)

    results = {}
    for test in data.get("tests", []):
        nodeid = test["nodeid"]
        name = nodeid.split("::")[-1]
        passed = test["outcome"] == "passed"
        msg = ""
        if not passed:
            call = test.get("call", {})
            msg = call.get("longrepr", call.get("crash", {}).get("message", ""))
        results[name] = {"passed": passed, "message": msg, "nodeid": nodeid}

    result_file.unlink(missing_ok=True)
    return results


def _run_pytest_fallback() -> dict:
    """如果 pytest-json-report 沒裝，用純文字解析"""
    cmd = [
        sys.executable, "-m", "pytest",
        str(ROOT / "tests"), "--tb=line", "-v",
    ]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    output = proc.stdout + proc.stderr

    results = {}
    for name in ALL_SCORES:
        if f"::{name} PASSED" in output:
            results[name] = {"passed": True, "message": ""}
        elif f"::{name}" in output:
            msg = next(
                (line for line in output.splitlines()
                 if name in line and "FAILED" in line), "")
            results[name] = {"passed": False, "message": msg}
        else:
            results[name] = {"passed": False, "message": "測試未執行（可能 import 失敗）"}
    return results


def generate_report(results: dict, show_solutions: bool = True) -> tuple[str, int, int]:
    """產生完整多模組報告，回傳 (report_md, total_earned, total_possible)"""
    sys.path.insert(0, str(ROOT))

    grand_earned = 0
    grand_total = 0
    sections = []

    for mod_name, mod_cfg in MODULES.items():
        scores = mod_cfg["scores"]
        mod_total = sum(scores.values())
        mod_earned = sum(
            pts for name, pts in scores.items()
            if results.get(name, {}).get("passed", False)
        )
        grand_earned += mod_earned
        grand_total += mod_total

        pct = mod_earned / mod_total * 100 if mod_total > 0 else 0

        lines = [
            f"## {mod_name}（{mod_earned}/{mod_total} — {pct:.0f}%）\n",
            "| 題目 | 分數 | 狀態 |",
            "|:-----|:----:|:----:|",
        ]
        for name, pts in scores.items():
            info = results.get(name, {"passed": False, "message": ""})
            status = "✅" if info["passed"] else "❌"
            got = pts if info["passed"] else 0
            lines.append(f"| `{name}` | {got}/{pts} | {status} |")
        lines.append("")

        # 錯誤提示
        failed = {k: v for k, v in results.items()
                  if k in scores and not v.get("passed", False)}
        if failed:
            lines.append("<details><summary>❌ 錯誤提示（點擊展開）</summary>\n")
            for name, info in failed.items():
                msg = info.get("message", "") or "請檢查函式是否有 return 值"
                if len(msg) > 300:
                    msg = msg[:300] + "..."
                lines.append(f"**`{name}`**\n```\n{msg}\n```\n")
            lines.append("</details>\n")

        # 解答
        if show_solutions:
            try:
                sol_mod = importlib.import_module(mod_cfg["solution_module"])
                passed_map = {n: results.get(n, {}).get("passed", False)
                              for n in scores}
                lines.append(sol_mod.format_report(passed_map))
            except ImportError:
                lines.append("> ⚠️ 解答模組未找到\n")

        sections.append("\n".join(lines))

    # 總報告
    grand_pct = grand_earned / grand_total * 100 if grand_total > 0 else 0
    if grand_pct >= 90:
        grade = "A"
    elif grand_pct >= 80:
        grade = "B"
    elif grand_pct >= 70:
        grade = "C"
    elif grand_pct >= 60:
        grade = "D"
    else:
        grade = "F"

    header = [
        "# 📊 作業批改結果\n",
        f"**總分：{grand_earned} / {grand_total}（{grand_pct:.0f}%）— 等級 {grade}**\n",
        "---\n",
    ]

    if not show_solutions:
        header.append("> 💡 完整解答請到你自己 fork 的 repo → **Actions** 頁籤查看。\n\n")

    report = "\n".join(header) + "\n" + "\n---\n\n".join(sections)
    return report, grand_earned, grand_total


def write_outputs(report: str, earned: int, total: int):
    """輸出報告到各個目標"""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write(report)

    report_path = ROOT / "grading_report.md"
    report_path.write_text(report, encoding="utf-8")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        pct = earned / total * 100 if total > 0 else 0
        with open(github_output, "a") as f:
            f.write(f"score={earned}\n")
            f.write(f"total={total}\n")
            f.write(f"percent={pct:.0f}\n")

    if not summary_path:
        print(report)


def main():
    parser = argparse.ArgumentParser(description="自動評分引擎（多模組版）")
    parser.add_argument(
        "--no-solutions", action="store_true",
        help="不在報告中顯示解答（用於老師 repo 的 PR comment）",
    )
    args = parser.parse_args()

    print("🔍 開始批改作業...\n")

    results = run_pytest()
    show_solutions = not args.no_solutions
    report, earned, total = generate_report(results, show_solutions=show_solutions)

    print(f"📊 總分：{earned}/{total}\n")
    write_outputs(report, earned, total)

    return 0


if __name__ == "__main__":
    sys.exit(main())
