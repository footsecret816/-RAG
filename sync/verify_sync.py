from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("files") or []

    results: list[dict[str, Any]] = []
    for item in entries:
        rel = item["path"]
        expected = item["git_blob_sha1"]
        path = root / rel

        if not path.exists():
            results.append({
                "path": rel,
                "status": "MISSING",
                "expected": expected,
                "actual": None,
            })
            continue

        actual = git_blob_sha1(path)
        results.append({
            "path": rel,
            "status": "OK" if actual == expected else "MISMATCH",
            "expected": expected,
            "actual": actual,
            "sha256": sha256(path),
        })

    bad = [x for x in results if x["status"] != "OK"]
    return {
        "ok": not bad,
        "release": manifest.get("release"),
        "manifest_scope": manifest.get("scope"),
        "checked_root": str(root),
        "matched": len(results) - len(bad),
        "total": len(results),
        "problems": bad,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="离线校验本地 Skill 与 GitHub 发布清单是否逐文件一致")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="本地仓库/Skill镜像根目录",
    )
    parser.add_argument(
        "--manifest",
        default=str(Path(__file__).with_name("release_manifest.json")),
    )
    args = parser.parse_args()

    result = verify(
        Path(args.root).expanduser().resolve(),
        Path(args.manifest).expanduser().resolve(),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
