# 04 Interface Schema / 统一机器接口规范

本文件定义不同 Agent 平台调用 05 Retrieval Tool 时共用的内部数据结构。

目标：

> 平台可以变，内部 Search_Request / Search_Result 不变。

---

## 一、Search_Request

推荐结构：

```json
{
  "product_category": "鞋垫",
  "hard_conditions": [],
  "soft_conditions": [],
  "priority": [],
  "semantic_query": ""
}
```

### hard_conditions

必须满足的条件，例如：

```json
[
  {"field":"Material","op":"eq","value":"PU"},
  {"field":"MOQ","op":"lte","value":3000}
]
```

### soft_conditions

用于排序的偏好，例如：

```json
[
  {"field":"Scenario_Tags","op":"contains","value":"户外徒步"},
  {"field":"Softness","op":"range","value":[1,3]}
]
```

### priority

记录用户明确优先级，例如：

```json
[
  {"field":"MOQ","level":"high"},
  {"field":"Price","level":"low"}
]
```

### semantic_query

保留无法完全结构化的原始语义。

---

## 二、Search_Result

推荐结构：

```json
{
  "exact_match": true,
  "results": [
    {
      "product_sku": "F0228",
      "factory_offer": {
        "factory_name": "富置高",
        "material": "PU",
        "material_detail": "",
        "price": 6.9,
        "moq": 3000,
        "size_system": "EU",
        "size_range": "36-46"
      },
      "product": {
        "main_image": "main.jpg",
        "function_tags": [],
        "scenario_tags": [],
        "special_features": [],
        "performance_attributes": {}
      },
      "packaging_options": [],
      "match_reasons": [],
      "unmet_conditions": []
    }
  ]
}
```

---

## 三、Change_Set

03⑥ 与 04②之间继续使用统一 Change Set。

最少包含：

```json
{
  "product_category": "鞋垫",
  "product_sku": "F0228",
  "factory_name": "富置高",
  "change_type": "update",
  "changed_fields": ["Price"]
}
```

---

## 四、兼容原则

1. 平台专属格式先转换成统一内部格式。
2. 04 / 05 不读取平台专属字段。
3. 平台变化不能要求修改 Product_KB Schema。
4. 新平台优先新增 Adapter，不改核心模块。
5. V1 可先用 JSON / 等价结构表达；后续实现代码时保持字段语义不变。
