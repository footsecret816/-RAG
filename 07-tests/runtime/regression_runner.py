from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SEARCH_RUNTIME = REPO_ROOT / "04-search" / "runtime"
sys.path.insert(0, str(SEARCH_RUNTIME))

from hybrid_search import search


def _contains_all(values: list[str], expected: list[str]) -> bool:
    actual = set(values)
    return all(item in actual for item in expected)


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    if case.get("enabled") is False:
        return {"id": case.get("id"), "status": "SKIP", "failures": []}

    request = case.get("search_request") or {}
    top_k = int(case.get("top_k") or 5)
    result = search(request, top_k=top_k, debug=bool(case.get("debug", False)))
    results = result.get("results") or []
    skus = [str(x.get("product_sku")) for x in results]

    expected = case.get("assert") or {}
    failures: list[str] = []

    if "exact_match" in expected and result.get("exact_match") != expected["exact_match"]:
        failures.append(
            f"exact_match: expected={expected['exact_match']} actual={result.get('exact_match')}"
        )

    top_sku = expected.get("top_sku")
    if top_sku and (not skus or skus[0] != top_sku):
        failures.append(f"top_sku: expected={top_sku} actual={skus[0] if skus else None}")

    top_any = expected.get("top_sku_any_of") or []
    if top_any and (not skus or skus[0] not in top_any):
        failures.append(f"top_sku not in allowed set: {top_any}; actual={skus[0] if skus else None}")

    order_prefix = expected.get("order_prefix") or []
    if order_prefix and skus[: len(order_prefix)] != order_prefix:
        failures.append(
            f"order_prefix: expected={order_prefix} actual={skus[:len(order_prefix)]}"
        )

    must_include = expected.get("must_include_skus") or []
    if not _contains_all(skus, must_include):
        failures.append(f"missing required SKUs: {sorted(set(must_include) - set(skus))}")

    must_exclude = expected.get("must_exclude_skus") or []
    present_forbidden = sorted(set(skus) & set(must_exclude))
    if present_forbidden:
        failures.append(f"forbidden SKUs present: {present_forbidden}")

    min_top_star = expected.get("min_top_star")
    if min_top_star is not None:
        actual = results[0].get("star_count") if results else None
        if actual is None or actual < min_top_star:
            failures.append(f"top star expected >= {min_top_star}; actual={actual}")

    max_top_star = expected.get("max_top_star")
    if max_top_star is not None:
        actual = results[0].get("star_count") if results else None
        if actual is None or actual > max_top_star:
            failures.append(f"top star expected <= {max_top_star}; actual={actual}")

    expected_warnings = expected.get("warnings_empty")
    if expected_warnings is True and result.get("warnings"):
        failures.append(f"warnings not empty: {result.get('warnings')}")

    return {
        "id": case.get("id"),
        "title": case.get("title"),
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "actual_top_skus": skus,
        "actual_top_stars": [x.get("star_count") for x in results],
    }


def run_suite(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases") if isinstance(data, dict) else data
    if not isinstance(cases, list):
        raise ValueError("回归文件必须包含 cases 数组")

    results = [evaluate_case(case) for case in cases]
    passed = sum(1 for x in results if x["status"] == "PASS")
    failed = sum(1 for x in results if x["status"] == "FAIL")
    skipped = sum(1 for x in results if x["status"] == "SKIP")
    return {
        "ok": failed == 0,
        "suite": str(path),
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="运行真实业务 Search_Request 回归集")
    parser.add_argument("suite")
    args = parser.parse_args()

    result = run_suite(Path(args.suite).expanduser().resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
