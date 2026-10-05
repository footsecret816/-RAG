from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DM_RUNTIME = REPO_ROOT / "03-data-management" / "runtime"
sys.path.insert(0, str(DM_RUNTIME))

from ingest_table import build_candidate
from maintenance import _merge_candidate
from validate_candidate import validate_candidate


class DataManagementTests(unittest.TestCase):
    def test_ingest_groups_same_sku_multiple_factories(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = [
                {
                    "SKU": "T001",
                    "工厂": "工厂A",
                    "材质": "PU Foam",
                    "价格": "6.9",
                    "MOQ": "3000双",
                    "尺码体系": "EU",
                    "尺码": "36-46",
                },
                {
                    "SKU": "T001",
                    "工厂": "工厂B",
                    "材质": "PU",
                    "价格": "6.3",
                    "MOQ": "5000",
                    "尺码体系": "EU",
                    "尺码": "36-46",
                },
            ]
            candidate = build_candidate(
                source=root / "test.xlsx",
                rows=rows,
                default_category="鞋垫",
                image_dir=None,
            )
            self.assertEqual(len(candidate["products"]), 1)
            product = candidate["products"][0]
            self.assertEqual(product["SKU_ID"], "T001")
            self.assertEqual(len(product["Factory_Offers"]), 2)
            self.assertEqual(product["Factory_Offers"][0]["Material"], "PU")
            self.assertEqual(product["Factory_Offers"][0]["MOQ"], 3000)

    def test_pending_review_blocks_validation(self):
        candidate = {
            "products": [{
                "Product_Category": "鞋垫",
                "SKU_ID": "T001",
                "Function_Tags": [],
                "Scenario_Tags": [],
                "Special_Features": [],
                "Performance_Attributes": {},
                "Factory_Offers": [{
                    "Factory_Name": "工厂A",
                    "Material": "PU",
                    "Price": 6.9,
                    "MOQ": 3000,
                    "Size_System": "EU",
                    "Size_Range": "36-46",
                }],
                "Review_Items": [{
                    "id": "T001-SEMANTIC",
                    "status": "pending",
                }],
            }],
            "issues": [],
        }
        result = validate_candidate(candidate)
        self.assertFalse(result["ok"])
        self.assertTrue(any("REVIEW 未完成" in x for x in result["errors"]))

    def test_blank_factory_fields_do_not_overwrite(self):
        old = {
            "Product_Category": "鞋垫",
            "SKU_ID": "T001",
            "Main_Image": "main.jpg",
            "Packaging_Options": [],
            "Function_Tags": ["缓震"],
            "Scenario_Tags": ["日常"],
            "Special_Features": [],
            "Performance_Attributes": {
                "Cushioning": 3,
                "Elasticity": 3,
                "Softness": 3,
                "Arch_Height": None,
                "Arch_Support": None,
                "Heel_Cup_Depth": None,
            },
            "Factory_Offers": [{
                "Factory_Name": "工厂A",
                "Material": "PU",
                "Material_Detail": "PU泡棉",
                "Price": 6.9,
                "MOQ": 3000,
                "Size_System": "EU",
                "Size_Range": "36-46",
            }],
        }
        candidate = {
            "Product_Category": "鞋垫",
            "SKU_ID": "T001",
            "Function_Tags": [],
            "Scenario_Tags": [],
            "Special_Features": [],
            "Performance_Attributes": {},
            "Factory_Offers": [{
                "Factory_Name": "工厂A",
                "Material": None,
                "Material_Detail": None,
                "Price": 7.2,
                "MOQ": None,
                "Size_System": None,
                "Size_Range": None,
            }],
        }
        merged, changes = _merge_candidate(old, candidate)
        offer = merged["Factory_Offers"][0]
        self.assertEqual(offer["MOQ"], 3000)
        self.assertEqual(offer["Material"], "PU")
        self.assertEqual(offer["Price"], 7.2)
        changed = [
            c for c in changes
            if c.get("factory_name") == "工厂A" and c.get("change_type") == "update"
        ]
        self.assertEqual(changed[0]["changed_fields"], ["Price"])

    def test_price_term_is_controlled_optional_field(self):
        rows = [{
            "SKU": "T002",
            "工厂": "工厂A",
            "材质": "PU",
            "价格": "6.9",
            "价格口径": "散装含税含运费",
            "MOQ": "3000",
            "尺码体系": "EU",
            "尺码": "36-46",
        }]
        candidate = build_candidate(
            source=Path("test.xlsx"),
            rows=rows,
            default_category="鞋垫",
            image_dir=None,
        )
        offer = candidate["products"][0]["Factory_Offers"][0]
        self.assertEqual(offer["Price_Term"], "散装含税含运费")

        old = {
            "Product_Category": "鞋垫",
            "SKU_ID": "T002",
            "Main_Image": "main.jpg",
            "Packaging_Options": [],
            "Function_Tags": [],
            "Scenario_Tags": [],
            "Special_Features": [],
            "Performance_Attributes": {},
            "Factory_Offers": [{
                "Factory_Name": "工厂A",
                "Material": "PU",
                "Material_Detail": "PU泡棉",
                "Price": 6.9,
                "Price_Term": "散装含税含运费",
                "MOQ": 3000,
                "Size_System": "EU",
                "Size_Range": "36-46",
            }],
        }

        blank_candidate = {
            "Product_Category": "鞋垫",
            "SKU_ID": "T002",
            "Performance_Attributes": {},
            "Factory_Offers": [{
                "Factory_Name": "工厂A",
                "Price_Term": None,
            }],
        }
        merged, changes = _merge_candidate(old, blank_candidate)
        self.assertEqual(merged["Factory_Offers"][0]["Price_Term"], "散装含税含运费")
        term_changes = [
            c for c in changes
            if c.get("factory_name") == "工厂A" and c.get("change_type") == "update"
        ]
        self.assertEqual(term_changes, [])

        updated_candidate = {
            "Product_Category": "鞋垫",
            "SKU_ID": "T002",
            "Performance_Attributes": {},
            "Factory_Offers": [{
                "Factory_Name": "工厂A",
                "Price_Term": "含税不含运费",
            }],
        }
        merged2, changes2 = _merge_candidate(old, updated_candidate)
        self.assertEqual(merged2["Factory_Offers"][0]["Price_Term"], "含税不含运费")
        updated = [
            c for c in changes2
            if c.get("factory_name") == "工厂A" and c.get("change_type") == "update"
        ]
        self.assertEqual(updated[0]["changed_fields"], ["Price_Term"])

    def test_new_factory_is_incremental(self):
        old = {
            "Product_Category": "鞋垫",
            "SKU_ID": "T001",
            "Main_Image": "main.jpg",
            "Packaging_Options": [],
            "Function_Tags": [],
            "Scenario_Tags": [],
            "Special_Features": [],
            "Performance_Attributes": {},
            "Factory_Offers": [{
                "Factory_Name": "工厂A",
                "Material": "PU",
                "Price": 6.9,
                "MOQ": 3000,
            }],
        }
        candidate = {
            "Product_Category": "鞋垫",
            "SKU_ID": "T001",
            "Factory_Offers": [{
                "Factory_Name": "工厂B",
                "Material": "PU",
                "Price": 6.3,
                "MOQ": 5000,
                "Size_System": "EU",
                "Size_Range": "36-46",
            }],
            "Performance_Attributes": {},
        }
        merged, changes = _merge_candidate(old, candidate)
        self.assertEqual(len(merged["Factory_Offers"]), 2)
        self.assertTrue(any(c["change_type"] == "new_factory_offer" for c in changes))


if __name__ == "__main__":
    unittest.main()
