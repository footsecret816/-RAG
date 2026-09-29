# 04 Search Engine / 检索引擎

本模块负责把标准 Product_KB 转换成可搜索的数据，并执行实际产品检索。

当前核心检索粒度固定为：

```text
SKU + Factory Offer
```

也就是说，同一 SKU 的不同工厂供应方案必须能够被独立筛选、排序和返回。

---

## 当前规划子板块

### ① Search Object Model / 搜索对象模型 ✅

文件：

`01-search-object-model.md`

负责定义 Product_KB 如何转换成可检索对象。

已确认：

- Product_KB 是真实数据源，Search Record 是派生数据。
- 产品搜索粒度为 `Product SKU + Factory Offer`。
- 同一 SKU 多工厂展开成多条 Product_Offer_Record。
- 产品层字段继承到每条 Factory Offer 搜索记录。
- Packaging_Options 只保存 Packaging_SKU 引用，不提前展开组合。
- 最终业务结果可动态组合为 `Product SKU + Factory Offer + Packaging SKU`。

---

### ② Index Build & Change Sync / 索引建立与变更同步 ✅

文件：

`02-index-build-and-sync.md`

负责：

- Product_KB 首次建立搜索索引
- 接收 03⑥ Change Set
- 对 Product_Offer_Record 做增量同步
- 当前优先支持 Metadata + Keyword
- Vector / Embedding 作为后续增强

---

### ③ Hybrid Retrieval / 混合检索 ✅

文件：

`03-hybrid-retrieval.md`

负责：

- 硬条件过滤
- Metadata 检索
- Keyword 检索
- Vector / Semantic Search 后续增强
- 无完全匹配时返回最接近候选但明确冲突

---

### ④ Ranking & Search Result / 排序与检索结果 ✅

文件：

`04-ranking-and-search-result.md`

负责：

- 按硬条件、用户优先级、软条件和语义相似度排序
- 输出标准 Product SKU + Factory Offer 结果
- 返回 Match_Reasons 与 Unmet_Conditions
- 返回 Packaging_Options 引用，为未来 Packaging SKU 组合留接口

---

## 与其他模块关系

```text
03 Data Management
        ↓
Change Set
        ↓
04 Search Engine
        ↓
05 Retrieval Tool
```

- 03：负责数据本身
- 04：负责数据怎么被搜索
- 05：负责把业务需求转换成可执行检索请求并调用 04

---

## 当前状态

当前仅完成模块职责与结构校正。

①②③④ 已完成 V1 规则设计。后续进入 05-retrieval-tool，并在 07-tests 中逐步验证。