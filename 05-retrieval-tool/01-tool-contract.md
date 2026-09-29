# 01 Tool Contract / 工具接口

本文件定义 05 Retrieval Tool 的统一输入输出接口。

目标：

- 不绑定具体 Agent 平台；
- 让 Accio、OpenAI 或其他平台都调用同一套检索能力；
- 输入自然语言或结构化条件；
- 输出稳定、可继续处理的产品检索结果。

---

## 一、输入

05 可以接收：

- 用户自然语言需求
- 可选结构化条件
- 必要业务上下文

例如：

```text
“要 PU 的，户外用，MOQ 不超过 3000，
价格其次，不要太软”
```

---

## 二、标准 Search Request

经过 05② 标准化后，应形成统一 Search Request。

建议至少包含：

```text
Product_Category

Hard_Conditions
Soft_Conditions
Priority
Semantic_Query
```

其中：

- Hard_Conditions：必须满足
- Soft_Conditions：用于排序
- Priority：用户明确优先级
- Semantic_Query：无法完全结构化的原始语义

---

## 三、标准输出

05 最终返回给 06 Agent 的结果至少包含：

```text
Product_SKU
Factory_Offer
Packaging_Options
Match_Reasons
Unmet_Conditions
Exact_Match
```

Factory_Offer 至少保留：

- Factory_Name
- Material
- Material_Detail
- Price
- MOQ
- Size_System
- Size_Range

---

## 四、边界

05：

- 不修改 Product_KB
- 不修改 04 的排序结果
- 不编造 SKU、工厂、价格、MOQ、材质
- 不绕过 04 自行推荐产品
- Packaging 当前只返回 Packaging_SKU 引用

最终业务方案未来可以组合：

```text
Product SKU + Factory Offer + Packaging SKU
```

但当前包装知识库尚未启用。
