# 04 Interface Schema / 统一机器接口规范

本文件定义不同智能体平台调用 05 Retrieval Tool 时共用的内部数据结构。

目标：

> 平台可以变，内部 Search_Request / Search_Result 不变。

---

## 一、Search_Request

V1 结构：

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

必须满足的条件：

```json
[
  {"field":"Material","op":"eq","value":"PU"},
  {"field":"MOQ","op":"lte","value":3000}
]
```

支持的基础操作符：

```text
eq
neq
contains
lte
gte
lt
gt
range
in
```

---

### soft_conditions

用于本次需求匹配分的具体偏好：

```json
[
  {"field":"Scenario_Tags","op":"contains","value":"长时间站立"},
  {"field":"Softness","op":"range","value":[1,3]}
]
```

---

### priority

记录用户明确优先级以及可选的相对优化方向：

```json
[
  {"field":"MOQ","level":"high","goal":"min"},
  {"field":"Price","level":"low","goal":"min"},
  {"field":"Elasticity","level":"medium","goal":"max"}
]
```

`level`：

```text
high
medium
low
```

`goal` 当前 V1：

```text
min = 越低越好
max = 越高越好
```

如果只有优先级、没有明确优化方向，可以省略 goal。

重要：

> priority.goal 即使没有对应 soft_condition，也必须参与排序。

---

### semantic_query

保留模糊自然语言，用于语义向量召回和辅助排序。

例如：

```text
每天站8小时，想脚底没那么累
```

如果其中部分含义已经可靠映射成 soft_conditions，仍可保留原始模糊表达给向量。

但价格、MOQ 等精确条件不能只写在 semantic_query 里。

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
      "match_score": 86.0,
      "star_count": 4,
      "match_reasons": [],
      "unmet_conditions": []
    }
  ]
}
```

说明：

- `match_score`：本次结构化需求匹配分；
- `star_count`：由 match_score 稳定映射；
- 向量相似度不直接作为 star_count；
- 相对偏好（goal=min/max）会进入 match_score。

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
5. 同一字段的 goal 含义跨平台保持一致。
6. V1 使用 JSON / 等价结构表达，字段语义不得自行扩写。
