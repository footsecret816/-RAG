---
name: product-knowledge-retrieval
description: Internal product knowledge retrieval and maintenance skill for company Product_KB. Supports product ingestion from structured tables and images, normalization into Product_KB, product search, recommendation, factory-offer comparison, and explicit maintenance requests. Never invent product facts.
compatibility: Requires access to an external Product_KB folder. Real product data is not stored in this repository.
metadata:
  author: runtong-wayyeah
  version: "1.0.0"
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

## 必须遵守的核心模块

- `01-schema/`：产品数据结构真源
- `02-taxonomy-rules/`：标准词、自然语言映射和业务规则真源
- `03-data-management/`：产品导入、维护、校验和 Change Set
- `04-search/`：搜索对象、检索和排序
- `05-retrieval-tool/`：统一 Search_Request / Search_Result
- `06-agent/`：Agent 行为与回答格式
- `07-tests/`：测试与回归

如系统级说明与具体模块冲突，以对应 01～07 模块为准。

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
