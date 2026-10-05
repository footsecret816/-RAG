# 03 Response Format / 回答格式

核心原则：

> 后台可以复杂，前台必须一眼看懂。

默认流程：

```text
Top 产品推荐表
↓
Packaging 推荐（如有真实数据）
↓
必要提醒
```

## 产品推荐表

默认每个 Product_Category 最多 Top 5，不强制凑满。

统一核心列：

```text
产品图片
SKU
关键规格
MOQ
价格
本次需求匹配度
本次推荐理由
```

“关键规格”不得写死在 Core，必须读取当前 Product Profile 的 `display_fields`，并结合本次需求选择最相关的 2～4 项。

## 图片

Main_Image 可访问时优先直接显示；不能直接渲染时才退化为图片引用。不得默认只显示文件名。

## 星级

星级只表示“本次需求匹配度”，直接使用 04 Search 输出；Agent 不得重新打分。

通常正常推荐只展示 3～5 星。1～2 星默认不展示；若无完全匹配，可单独作为接近候选并说明差异。

## 推荐理由

推荐理由必须来自：

```text
本次用户重点
×
真实 Product_KB / Search_Result 匹配点
```

默认 1～2 个核心点，不写泛化卖点，不编造市场假设。

## 多工厂

同一 SKU 多个 Factory Offer 必须分开判断。Price / MOQ / Material / Size 不得混合。

## Packaging

Packaging_KB 有真实数据时，放在对应产品品类表格下方，默认 2～3 个方案。没有真实数据时不得编造。

## 内部字段

普通业务员默认不展示 Search_Request、Hard_Conditions、Soft_Conditions、Exact_Match 等内部技术字段。

## 最终原则

- 每个品类最多 Top 5；
- 图片优先直接显示；
- 星级由 Search 决定；
- 关键规格由 Product Profile 决定；
- 推荐理由围绕本次需求；
- 默认回答保持短。
