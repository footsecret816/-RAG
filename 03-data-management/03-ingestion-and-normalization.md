# 03 Ingestion & Normalization / 表格导入与标准化

本模块定义固定格式产品表格 + 产品图片进入标准 Product_KB 的通用 V1 流程。

## 输入

V1 支持：

- .xlsx / .xlsm / .csv 固定格式产品表格
- 与 SKU 对应的清晰产品图片

产品专属字段、材质、标签、性能值域不在本文件写死，统一读取 active Product Profile。

## 基本粒度

```text
一行数据 = 一个 SKU + 一个 Factory Offer
```

同一 SKU 不同 Factory_Name 必须合并到同一个 Product，并保留独立 Factory Offer。

## 标准流程

```text
产品表格 + 图片
↓
识别 SKU / Factory Offer
↓
提取明确事实字段
↓
按 Product Profile 标准化材质 / 尺码 / 标签 / 性能
↓
生成候选
↓
AUTO / RULE / REVIEW / MISSING
↓
人工确认 REVIEW
↓
Validation PASS
↓
写入 Product_KB
```

## 固定事实字段

以下字段优先直接提取，只做格式清洗：

- SKU_ID
- Factory_Name
- MOQ
- Price
- Price_Term
- Material_Detail
- Size_Range

空白不得覆盖旧值。

## Product Profile 负责

```text
profiles/active-profile.yaml
→ 当前 Product Profile
```

其中定义：

- Product_Category
- Material 标准词与别名
- Size_System
- Function_Tags
- Scenario_Tags
- Special_Features
- Performance_Attributes
- automation_levels

无法可靠映射时进入 REVIEW，不得自行创建标准值。

## 图片

优先按 SKU_ID 关联。无法唯一匹配时进入 REVIEW。

## 边界

V1 不处理任意 PDF / Word / 网页抓取。新 SKU 走首次导入；已存在 SKU 必须进入 Product Maintenance 差异更新流程。
