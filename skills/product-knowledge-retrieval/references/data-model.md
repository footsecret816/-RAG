# Data Model / 产品数据模型

## Product 层

每个 SKU 至少按以下字段理解：

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

Performance_Attributes 当前鞋垫包括：

```text
Cushioning: 1-5
Elasticity: 1-5
Softness: 1-5
Arch_Height: 低 / 中 / 高
Arch_Support: 无支撑 / 轻度支撑 / 强支撑
Heel_Cup_Depth: 平 / 浅 / 中 / 深
```

Softness：

```text
1 = 最硬
5 = 最软
```

## Factory Offer 层

每个工厂方案独立维护：

```text
Factory_Name
Material
Material_Detail
Price
MOQ
Size_System
Size_Range
```

同一 SKU 可以有多个 Factory Offer。

检索和推荐时必须分别判断。

## Packaging

`Packaging_Options` 只保存未来独立 Packaging_KB 的 `Packaging_SKU` 引用。

当前不能根据 Packaging_SKU 猜测包装的材质、尺寸、价格或工艺。

## 真实数据边界

产品真实资料应位于外部 Product_KB，例如：

```text
Product_KB/
└─ insoles/
   └─ F0228/
      ├─ product.md
      └─ main.jpg
```

本 Skill 不把 GitHub 内的规则文档当成真实产品数据。
