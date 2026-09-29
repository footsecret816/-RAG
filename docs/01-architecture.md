# Architecture / 总体架构

本项目是一套平台无关的企业产品知识库与智能检索系统。

## 模块关系

```text
01 Schema
↓
02 Taxonomy & Rules
↓
03 Data Management
↓
Product_KB
↓
04 Search Engine
↓
05 Retrieval Tool
↓
06 Agent
↓
业务员

07 Tests
= 对 03～06 做验证与回归
```

## 各模块职责

- 01：定义产品数据结构
- 02：定义标准词、自然语言映射和业务规则
- 03：负责产品数据导入、更新、校验与 Change Set
- 04：负责搜索对象、索引、检索和排序
- 05：把自然语言转换成 Search Request，并调用 04
- 06：业务使用入口
- 07：测试与回归验证

## 数据真源

`Product_KB` 是真实产品数据真源。

GitHub 只保存：

- Schema
- Rules
- 数据管理逻辑
- Search 规则
- Tool / Agent 规则
- 测试与文档

真实 SKU、图片、价格、MOQ、工厂等不进入 Git。

## 包装扩展

未来包装独立使用：

```text
Packaging_KB
+
Packaging_SKU
```

产品通过 `Packaging_Options` 引用可关联的 Packaging_SKU。

当前 V1 只保留接口，不建设 Packaging_KB 内部 Schema。

最终业务方案未来可组合为：

```text
Product SKU + Factory Offer + Packaging SKU
```


## 平台适配层

```text
Accio Work ─┐
WorkBuddy ──┤
Codex ──────┤
Claude ─────┤
DeepSeek ───┤
            ↓
        adapters/
            ↓
统一 Search_Request / Search_Result
            ↓
        05 Retrieval Tool
```

平台专属差异只放 `adapters/`，不进入 01～07 核心模块。
