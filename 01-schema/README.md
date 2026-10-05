# 01 Schema

本模块只定义**跨公司 / 跨产品可复用的产品知识库公共结构**。

产品专属字段、值域、材质词表、功能标签、场景标签、性能指标等，不再写死在 Core；统一由当前 active Product Profile 定义。

当前 Profile 入口：

```text
profiles/active-profile.yaml
```

当前润通鞋垫 Profile：

```text
profiles/runtong/products/insoles/profile.yaml
```

## 一、Product / SKU 公共层

每个产品至少使用以下公共字段：

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

说明：

- `Product_Category`：产品类别，由 Product Profile 定义标准值与目录映射。
- `SKU_ID`：单个产品的稳定唯一编号。
- `Main_Image`：真实图片引用，图片不进入 GitHub。
- `Function_Tags / Scenario_Tags / Special_Features`：具体标准词由 Product Profile 定义。
- `Performance_Attributes`：字段名、值域、显示名称由 Product Profile 定义。
- `Packaging_Options`：预留 Packaging_SKU 引用，可为空。

## 二、Factory Offer 公共层

同一 SKU 可以对应多个工厂供应方案。

公共字段：

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

规则：

- 最终检索粒度固定为 `SKU + Factory Offer`。
- `Price` 必须与具体 Factory Offer 绑定。
- `Price_Term` 为可选价格口径；原始资料有则保留，没有可靠信息时保持 null。
- 新资料空白不得覆盖已有正式值。
- `Price / Price_Term / MOQ / Factory_Name` 默认不进入向量语义文本。
- Material 标准词、Size_System 标准值及别名由当前 Product Profile 定义。

## 三、Profile 与 Core 的边界

Core 负责：

- 公共数据结构；
- 数据导入 / 校验 / 维护流程；
- 结构化条件、关键词、向量和 Hybrid Search；
- Search_Request / Search_Result；
- 索引构建与更新。

Product Profile 负责：

- 产品类别；
- 材质词表；
- 标签；
- 性能字段和值域；
- 表格列别名；
- 展示字段；
- 产品业务映射知识。

Company Profile 负责：

- 公司身份与运行配置；
- 当前公司的兼容环境变量与数据路径提示。

## 四、真实数据边界

真实业务数据不进入 GitHub：

- SKU 数据
- 产品图片
- 工厂真实供应数据
- 真实价格 / MOQ
- 客户数据
- 真实包装数据

这些由外部 `Product_KB` / `Packaging_KB` 保存。

## 五、标准 product.md

正式 Product_KB 的公共模板见：

```text
01-schema/product-template.md
```

实际 `Performance_Attributes` 字段由 active Product Profile 展开。
