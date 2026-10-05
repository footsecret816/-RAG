from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DM_RUNTIME = REPO_ROOT / "03-data-management" / "runtime"
SEARCH_RUNTIME = REPO_ROOT / "04-search" / "runtime"

for path in (REPO_ROOT, DM_RUNTIME, SEARCH_RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from profiles.profile_loader import (
    default_product_category,
    load_active_profile,
    load_company_profile,
    load_default_product_profile,
)
from common import (
    PERFORMANCE_KEYS,
    category_dir,
    normalize_material,
    normalize_size_system,
)


class ProfileModularizationTests(unittest.TestCase):
    def test_active_runtong_profile_preserves_current_business_values(self):
        active = load_active_profile()
        company = load_company_profile()
        product = load_default_product_profile()

        self.assertEqual(active["company_profile"], "runtong")
        self.assertEqual(active["default_product_profile"], "insoles")
        self.assertEqual(company["id"], "runtong")
        self.assertEqual(product["id"], "insoles")

        self.assertEqual(default_product_category(), "鞋垫")
        self.assertEqual(category_dir("鞋垫"), "insoles")
        self.assertEqual(normalize_material("PU Foam"), "PU")
        self.assertEqual(normalize_size_system("欧码"), "EU")

        self.assertEqual(
            PERFORMANCE_KEYS,
            (
                "Cushioning",
                "Elasticity",
                "Softness",
                "Arch_Height",
                "Arch_Support",
                "Heel_Cup_Depth",
            ),
        )

    def test_business_literals_are_not_embedded_in_core_runtime_files(self):
        core_files = [
            REPO_ROOT / "03-data-management" / "runtime" / "common.py",
            REPO_ROOT / "03-data-management" / "runtime" / "ingest_table.py",
            REPO_ROOT / "03-data-management" / "runtime" / "validate_candidate.py",
            REPO_ROOT / "04-search" / "runtime" / "config.py",
            REPO_ROOT / "04-search" / "runtime" / "product_loader.py",
        ]

        forbidden_literals = (
            "RUNTONG_PRODUCT_DATA",
            "RUNTONG_EMBEDDING_MODEL_PATH",
            "足弓支撑",
            "缓震",
            "长距离行走",
            '"Cushioning": "缓震"',
        )

        for path in core_files:
            text = path.read_text(encoding="utf-8")
            for literal in forbidden_literals:
                self.assertNotIn(
                    literal,
                    text,
                    msg=f"{path.relative_to(REPO_ROOT)} 仍硬编码业务值：{literal}",
                )


if __name__ == "__main__":
    unittest.main()
