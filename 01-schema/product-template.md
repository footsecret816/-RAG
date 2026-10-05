# Product Template / 标准 product.md 公共模板

产品专属 Performance_Attributes 键、标签和值域由当前 Product Profile 定义。

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

规则：

- 同一 SKU 可有多个 Factory Offer；
- 组合键为 SKU_ID + Factory_Name；
- 缺失事实保持 null / []；
- REVIEW 未确认不得写成正式事实；
- 新表空白不得清空已有值；
- 删除必须走明确删除流程。
