# Data Model / 产品数据模型

## Product 公共层

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

Performance_Attributes 的具体字段和值域由当前 Product Profile 定义。

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

同一 SKU 可有多个 Factory Offer，检索时必须分别判断。

## Profile

公司 / 产品专属信息读取：

```text
profiles/active-profile.yaml
→ Company Profile
→ Product Profile
```

真实 SKU、图片、工厂、价格、MOQ 仍只来自外部 Product_KB。
