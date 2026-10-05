# Product Template / 标准 product.md 模板

本文件定义单个 SKU 在正式 Product_KB 中的标准 V1 输出结构。

目标：

- 让 03-data-management 每次生成的 product.md 结构一致；
- 让 04-search 后续可以稳定读取；
- 避免不同 AI、不同平台自行发明字段或排版。

正式字段必须服从 `01-schema/README.md`，标准词必须服从 `02-taxonomy-rules/`。

---

## V1 推荐结构

```yaml
---
Product_Category: null
SKU_ID: null
Main_Image: main.jpg

Packaging_Options: []

Function_Tags: []
Scenario_Tags: []
Special_Features: []

Performance_Attributes:
  Cushioning: null
  Elasticity: null
  Softness: null
  Arch_Height: null
  Arch_Support: null
  Heel_Cup_Depth: null

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

---

## 字段规则

### 产品层

以下字段属于 SKU 本身：

- Product_Category
- SKU_ID
- Main_Image
- Packaging_Options
- Function_Tags
- Scenario_Tags
- Special_Features
- Performance_Attributes

`Packaging_Options` 当前 V1 可保持空数组：

```yaml
Packaging_Options: []
```

未来 Packaging_KB 启用后，再填写 Packaging_ID。

### Factory Offer 层

`Factory_Offers` 是一对多列表。

同一 SKU 可以存在多个工厂：

```yaml
Factory_Offers:
  - Factory_Name: 工厂A
    Material: PU
    Material_Detail: 事实性详细材质说明
    Price: 6.9
    Price_Term: 散装含税含运费
    MOQ: 3000
    Size_System: EU
    Size_Range: 36-46

  - Factory_Name: 工厂B
    Material: PU
    Material_Detail: 另一实际材质方案
    Price: 6.3
    Price_Term: 含税不含运费
    MOQ: 5000
    Size_System: EU
    Size_Range: 36-46
```

具体 Factory Offer 的识别键：

```text
SKU_ID + Factory_Name
```

---

## 空值规则

正式 Product_KB 不允许为了“填满字段”而猜测。

可选字段没有可靠信息时：

```yaml
字段: null
```

或空列表：

```yaml
字段: []
```

但：

- REVIEW 尚未人工确认的建议值，不得伪装成正式值；
- 新表格空白不得用于清空已有正式值；
- 删除必须走 03④ 的明确删除流程。

---

## 模板边界

本模板只定义正式 product.md 的结构。

它不定义：

- 原始 Excel 格式
- 标签映射规则
- 数据自动化等级
- 更新逻辑
- 搜索索引结构
- Packaging_KB 内部 Schema

这些分别由 02、03、04 及未来包装模块管理。
