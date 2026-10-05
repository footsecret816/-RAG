# 02 Query Normalization / 查询标准化

目标：把业务员自然语言转换成 04-search 可执行的 Search_Request。

核心原则：

> 能可靠结构化的业务含义先结构化；向量负责补充模糊语义，不替代明确条件。

## 标准流程

```text
用户自然语言
↓
识别 Product_Category
↓
识别 Hard Conditions
↓
识别 Soft Conditions
↓
识别 Priority / goal=min|max
↓
保留仍有价值的 Semantic_Query
↓
Search_Request
```

## Profile 边界

Base Skill 不写死任何具体产品的材质、功能、场景、性能字段或自然语言映射。

查询前必须读取：

```text
profiles/active-profile.yaml
→ 当前 Product Profile
```

并使用其中的 schema / tags / performance_attributes / query_mappings。

## 条件分类

- Hard Conditions：明确不能违反的条件，如价格、MOQ、材质、尺码、特殊属性阈值。
- Soft Conditions：用户希望满足但允许权衡的属性。
- Priority：明确“越低越好 / 越高越好”时使用 `goal=min/max`，不要凭空造阈值。
- Semantic_Query：保留模糊体验、场景描述和无法完全结构化的表达。

同一句话可以同时进入结构化条件和 Semantic_Query。

## 固定规则

1. 硬条件不能被关键词或向量突破。
2. 标准字段和值必须来自当前 Product Profile。
3. `semantic_query` 不直接决定星级。
4. 不确定表达不得强行映射。
5. 05 只生成 / 校验 Search_Request，不自行选择产品。
