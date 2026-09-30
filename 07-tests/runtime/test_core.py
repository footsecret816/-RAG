from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME = REPO_ROOT / "04-search" / "runtime"
sys.path.insert(0, str(RUNTIME))

from product_loader import load_product_file
from ranking import condition_match, score_soft_conditions


PRODUCT_MD = """---
Product_Category: 鞋垫
SKU_ID: TEST001
Main_Image: main.jpg
Packaging_Options: []
Function_Tags: [缓震, 回弹]
Scenario_Tags: [长时间站立]
Special_Features: []
Performance_Attributes:
  Cushioning: 4
  Elasticity: 4
  Softness: 3
  Arch_Height: medium
  Arch_Support: light
  Heel_Cup_Depth: medium
Factory_Offers:
  - Factory_Name: 工厂A
    Material: PU
    Material_Detail: 高回弹PU + Gel
    Price: 6.9
    MOQ: 3000
    Size_System: EU
    Size_Range: 36-46
---
"""


class ProductLoaderTests(unittest.TestCase):
    def test_product_record_generation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            product_dir = root / "Product_KB" / "insoles" / "TEST001"
            product_dir.mkdir(parents=True)
            path = product_dir / "product.md"
            path.write_text(PRODUCT_MD, encoding="utf-8")
            (product_dir / "main.jpg").write_bytes(b"")

            records = load_product_file(path, root)
            self.assertEqual(len(records), 1)
            record = records[0]

            self.assertEqual(record["product_sku"], "TEST001")
            self.assertEqual(record["factory_offer"]["material"], "PU")
            self.assertIn("缓震", record["keywords"])
            self.assertIn("长时间站立", record["semantic_text"])

            # 精确商务字段不能混入语义文本。
            self.assertNotIn("工厂A", record["semantic_text"])
            self.assertNotIn("3000", record["semantic_text"])
            self.assertNotIn("6.9", record["semantic_text"])


class RankingTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            "product_sku": "TEST001",
            "product_category": "鞋垫",
            "factory_offer": {
                "factory_name": "工厂A",
                "material": "PU",
                "material_detail": "高回弹PU + Gel",
                "price": 6.9,
                "moq": 3000,
                "size_system": "EU",
                "size_range": "36-46",
            },
            "product": {
                "function_tags": ["缓震", "回弹"],
                "scenario_tags": ["长时间站立"],
                "special_features": [],
                "performance_attributes": {
                    "Cushioning": 4,
                    "Elasticity": 4,
                    "Softness": 3,
                },
            },
        }

    def test_hard_condition(self):
        self.assertTrue(
            condition_match(
                self.record,
                {"field": "MOQ", "op": "lte", "value": 3000},
            )
        )
        self.assertFalse(
            condition_match(
                self.record,
                {"field": "MOQ", "op": "lte", "value": 1000},
            )
        )

    def test_tag_condition(self):
        self.assertTrue(
            condition_match(
                self.record,
                {"field": "Scenario_Tags", "op": "contains", "value": "长时间站立"},
            )
        )

    def test_soft_score(self):
        request = {
            "soft_conditions": [
                {"field": "Softness", "op": "range", "value": [2, 3]},
                {"field": "Scenario_Tags", "op": "contains", "value": "长时间站立"},
            ],
            "priority": [
                {"field": "Scenario_Tags", "level": "high"},
                {"field": "Softness", "level": "medium"},
            ],
        }
        score, high_full, medium_full = score_soft_conditions(self.record, request)
        self.assertEqual(score, 100.0)
        self.assertEqual(high_full, 1)
        self.assertEqual(medium_full, 1)


if __name__ == "__main__":
    unittest.main()
