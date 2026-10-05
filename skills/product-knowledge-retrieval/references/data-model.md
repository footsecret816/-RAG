# Data Model / 产品数据模型

## 公共 Product 层

每个 SKU 使用统一公共结构：

```text
Product_Category
SKU_ID
Main_Image
Function_Tags
Scenario_Tags
Packaging_Options
Special_Features
Performance_Attributes
Factory_Offers
```

`Performance_Attributes` 的实际字段和值域属于 Product Profile，不属于 Base Skill Core。

当前 active profile 由：

```text
profiles/active-profile.yaml
```

指定。

## Factory Offer 层

每个工厂方案独立维护：

```text
Factory_Name
Material
Material_Detail
Price
Price_Term
MOQ
Size_System
Size_Range
```

同一 SKU 可以有多个 Factory Offer；检索和推荐必须分别判断。

## Product Profile

产品专属内容统一位于：

```text
profiles/<company>/products/<product>/
```

包括：

- 类别与目录映射
- 材质标准词 / 别名
- Function / Scenario / Special 标签
- Performance 字段和值域
- 表格列别名
- 展示字段
- 产品业务映射知识

## Packaging

`Packaging_Options` 只保存未来独立 Packaging_KB 的 `Packaging_SKU` 引用。

## 真实数据边界

真实 SKU、图片、价格、MOQ、工厂供应数据放在外部 Product_KB。

GitHub 中的 Profile 是规则与配置，不是真实 SKU 数据。
