from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from hybrid_search import search


def _load_request(args) -> dict:
    if args.request_json:
        return json.loads(args.request_json)
    if args.request_file:
        return json.loads(Path(args.request_file).read_text(encoding="utf-8"))
    raw = sys.stdin.read().strip()
    if not raw:
        raise ValueError("请通过 --request-json、--request-file 或 stdin 提供 Search_Request JSON")
    return json.loads(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description="润通产品混合检索统一入口")
    parser.add_argument("--request-json")
    parser.add_argument("--request-file")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    try:
        request = _load_request(args)
        result = search(request, top_k=args.top_k, debug=args.debug)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {"ok": False, "error": str(exc)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
