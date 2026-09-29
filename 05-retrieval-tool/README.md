# 05 Retrieval Tool / 产品检索工具

本模块负责把业务员的自然语言需求转换成标准检索请求，并调用 04 Search Engine。

它是 Agent 与底层搜索之间的统一接口。

本模块必须保持平台无关。

---

## 当前规划子板块

### ① Tool Contract / 工具接口

定义统一输入与输出。

输入可以包括：

- 自然语言产品需求
- 已经结构化的检索条件
- 必要业务上下文

输出至少应包含：

- SKU_ID
- Factory_Name
- Main_Image
- Material
- Price
- MOQ
- Size
- 关键匹配理由
- 未满足条件或风险提示

最终结果粒度：

```text
SKU + Factory Offer
```

---

### ② Query Normalization / 查询标准化

负责根据 02 Taxonomy & Rules，把业务员自然语言转换成标准 Search Request。

例如：

```text
“记忆棉、跑步用、不要太软，
客户想先测品，MOQ越低越好，贵一点没事”
```

转换为类似：

```text
Product_Category = 鞋垫

Material = 记忆棉
Scenario = 跑步
Softness = 偏向 1–3

Priority:
MOQ = 高
Price = 低
```

02 负责定义规则。

05 负责执行这些规则。

---

### ③ Retrieval Orchestration / 检索调度

负责：

```text
Search Request
        ↓
调用 04
        ↓
读取完全匹配 / 最接近结果
        ↓
组织标准化返回
```

核心原则：

- 05 不绕过 04 自己重新选择产品。
- 05 不修改 Product_KB。
- 05 不自行创造不存在的 SKU、工厂、价格或属性。
- 如果没有完全满足硬条件的结果，必须明确返回无完全匹配，再提供最接近候选。

---

## 未来扩展

未来 Packaging_KB 启用后，可以在不改变当前产品检索核心接口的前提下，扩展包装检索或产品与 Packaging_ID 的关联查询。

当前 V1 不实现包装检索。

---

## 与其他模块关系

```text
02 Taxonomy & Rules
        ↓
05 Query Normalization
        ↓
04 Search Engine
        ↓
05 Standard Result
        ↓
06 Agent
```

---

## 当前状态

当前仅完成模块职责与结构校正。

后续按①②③逐步细化。