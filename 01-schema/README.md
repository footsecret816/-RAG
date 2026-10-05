# 01 Schema

本模块只定义跨公司、跨产品可复用的公共产品数据结构。

产品专属的材质、功能、场景、性能字段和值域全部来自当前 active Product Profile：

```text
profiles/active-profile.yaml
→ profiles/<company>/products/<product>/profile.yaml
```

## Product / SKU 公共层

```text
Product_Category
SKU_ID
Main_Image
Packaging_Options
Function_Tags
Scenario_Tags
Special_Features
Performance_Attributes
Factory_Offers
```

其中：

- Function_Tags / Scenario_Tags / Special_Features 的标准值由 Product Profile 定义；
- Performance_Attributes 的具体键和值域由 Product Profile 定义；
- Main_Image、真实 SKU、价格、MOQ、工厂等真实业务数据不进入 GitHub。

## Factory Offer 公共层

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

固定原则：

- 检索粒度 = Product SKU + Factory Offer；
- Price / MOQ / Material / Size 必须与具体 Factory Offer 绑定；
- Price_Term 可为空，空白不得覆盖已有正式值；
- Product Profile 更换时，Core 结构不需要修改。
