from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from config import MODEL_ID, get_config


REQUIRED_IMPORTS = {
    "numpy": "numpy",
    "yaml": "PyYAML",
    "faiss": "faiss-cpu",
    "sentence_transformers": "sentence-transformers",
}


def dependency_status() -> dict[str, bool]:
    return {
        package: importlib.util.find_spec(module) is not None
        for module, package in REQUIRED_IMPORTS.items()
    }


def install_requirements(wheel_dir: str | None = None) -> None:
    requirements = Path(__file__).with_name("requirements.txt")
    cmd = [sys.executable, "-m", "pip", "install"]
    if wheel_dir:
        cmd += ["--no-index", "--find-links", wheel_dir]
    cmd += ["-r", str(requirements)]
    subprocess.run(cmd, check=True)


def download_model() -> str:
    cfg = get_config()
    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise RuntimeError(
            "缺少 huggingface_hub。先安装 requirements.txt 后再下载模型。"
        ) from exc

    cfg.local_model_dir.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=str(cfg.local_model_dir),
    )
    return str(cfg.local_model_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="检查/准备产品检索运行环境")
    parser.add_argument("--install", action="store_true", help="安装 requirements.txt")
    parser.add_argument("--wheel-dir", help="从本地 wheel 目录离线安装")
    parser.add_argument("--download-model", action="store_true", help="下载 V1 Embedding 模型到 Product_Data/_models")
    args = parser.parse_args()

    before = dependency_status()
    if args.install:
        install_requirements(args.wheel_dir)

    model_path = None
    if args.download_model:
        model_path = download_model()

    after = dependency_status()
    cfg = get_config()

    result = {
        "ok": all(after.values()),
        "dependencies_before": before,
        "dependencies_after": after,
        "model_id": MODEL_ID,
        "model_source": cfg.model_source,
        "downloaded_model_path": model_path,
        "product_data_root": str(cfg.product_data_root),
        "search_index_dir": str(cfg.search_index_dir),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
