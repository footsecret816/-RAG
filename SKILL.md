---
name: product-knowledge-retrieval
description: Internal product knowledge retrieval and maintenance skill for company Product_KB. Supports product ingestion from structured tables and images, normalization into Product_KB, product search, recommendation, factory-offer comparison, and explicit maintenance requests. Never invent product facts.
compatibility: Requires access to an external Product_KB folder. Real product data is not stored in this repository.
metadata:
  author: runtong-wayyeah
  version: "1.0.3"
---

# Product Knowledge Retrieval Skill

本仓库整体作为“产品知识检索 Skill”使用。

## 核心目标

支持两类任务：

1. 产品资料入库与维护；
2. 业务员自然语言查询、筛选和推荐产品。

真实产品数据存放在外部 `Product_KB`，本仓库只保存规则、结构、检索逻辑、Agent 规则和测试规范。

## 首次使用

如果当前还没有 Product_KB：

1. 让用户指定 Product_KB 存放目录；
2. 接收固定格式产品表格 + 对应产品图片；
3. 按 01～03 的规则提取、标准化、校验；
4. 生成标准 `product.md`；
5. 写入 Product_KB；
6. 完成一批产品后，再进入检索测试。

## 查询流程

```text
业务员自然语言
↓
06 Agent
↓
05 Retrieval Tool
↓
04 Search
↓
Product_KB
↓
返回 Product SKU + Factory Offer
```

## 维护流程

只有用户明确要求新增、修改、替换或删除产品资料时，才进入 03 Data Management。

不得因为用户在聊天中提到新价格、新 MOQ 或其他信息就自动改库。

## REVIEW 确认交互

产品入库时，所有需要人工确认的 REVIEW 字段应集中一次展示，并使用短编号，避免要求操作者重复输入长文字。

推荐格式：

```text
性能
P1 缓震：3
P2 回弹：4
P3 软硬：4

场景
S1 日常
S2 长距离行走
```

支持最短回复：

```text
确认
P2=3
去掉S2
P=344
S=12
```

“确认”表示接受当前全部 REVIEW 候选。

KB 路径、价格口径等全局配置只在首次设置或发生变化时确认，不得每个 SKU 重复询问。

## 必须遵守的核心模块

- `01-schema/`：产品数据结构真源
- `02-taxonomy-rules/`：标准词、自然语言映射和业务规则真源
- `03-data-management/`：产品导入、维护、校验和 Change Set
- `04-search/`：搜索对象、检索和排序
- `05-retrieval-tool/`：统一 Search_Request / Search_Result
- `06-agent/`：Agent 行为与回答格式
- `07-tests/`：测试与回归

如系统级说明与具体模块冲突，以对应 01～07 模块为准。

## 业务员结果展示

默认展示方式：

```text
后台全部候选
→ 硬条件过滤
→ 本次需求排序
→ 去同质化
→ Top 5
→ 紧凑表格
→ Packaging 推荐 2～3 个
```

产品推荐表默认：

```text
图片｜SKU｜品类关键规格｜MOQ｜价格｜⭐本次需求匹配度｜本次推荐理由
```

要求：

- Main_Image 可访问时直接展示产品图片；
- 星级只表示“本次需求匹配度”，不是产品质量评分；
- 推荐理由必须基于用户本次提问；
- 不默认展示全部命中 SKU；
- 大量相似候选需要去同质化；
- 不同 Product_Category 动态选择关键规格；
- Packaging 推荐放在产品表下方，默认 2～3 个；
- Packaging 推荐必须展示对应 Packaging 图片；
- Packaging_KB 没有真实数据时不得编造。

具体展示规则：

- `06-agent/03-response-format.md`
- `06-agent/04-category-display-fields.md`

## 产品检索粒度

必须按：

```text
Product SKU + Factory Offer
```

同一 SKU 的不同工厂供应方案必须独立判断，不得混用价格、MOQ、材质和尺码。

## 包装

未来包装独立使用：

```text
Packaging_KB
Packaging_SKU
```

当前产品仅通过 `Packaging_Options` 保留 Packaging_SKU 引用。

未来 Packaging_KB 启用后，推荐结果中应在产品表格下方展示 2～3 个匹配包装方案，包括：

- Packaging 图片
- Packaging_SKU
- 包装方式
- 基于本次客户需求的推荐理由

## 数据真实性

不得自行编造：

- SKU
- Factory_Name
- Material
- Material_Detail
- Price
- MOQ
- Size
- Packaging_SKU
- Performance_Attributes

缺失就明确标记缺失。

## 平台兼容

本 Skill 不绑定 Accio Work、WorkBuddy、Codex、Claude 或 DeepSeek Harness。

平台专属差异只放在：

`adapters/`

核心规则保持平台无关。
