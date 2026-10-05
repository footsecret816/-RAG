# Product Template / 标准 product.md 公共模板

本文件只定义跨产品复用的公共结构。

产品专属 `Performance_Attributes`、标签和值域必须读取 active Product Profile，不得在 Core 中写死。

```yaml
---
Product_Category: null
SKU_ID: null
Main_Image: main.jpg

Packaging_Options: []

Function_Tags: []
Scenario_Tags: []
Special_Features: []

Performance_Attributes: {}

Factory_Offers:
  - Factory_Name: null
    Material: null
    Material_Detail: null
    Price: null
    Price_Term: null
    MOQ: null
    Size_System: null
    Size_Range: null
---
```

## 规则

- `Performance_Attributes` 的实际键由 Product Profile 定义。
- 同一 SKU 可以存在多个 Factory Offer。
- Factory Offer 唯一业务组合键为 `SKU_ID + Factory_Name`。
- 可选字段没有可靠信息时使用 `null` 或空列表。
- REVIEW 未确认的建议值不得伪装成正式值。
- 新表格空白不得清空已有正式值。
- 删除必须走明确删除流程。
- 真实产品字段标准以 `01-schema/README.md` + active Product Profile 为准。
