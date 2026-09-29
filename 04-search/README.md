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

### ② Index Build & Change Sync / 索引建立与变更同步

负责：

- Product_KB 首次建立搜索索引
- 接收 03⑥ Data Change Handoff 生成的 Change Set
- 根据实际变化更新相关搜索记录
- 决定哪些变化需要同步 Metadata、Keyword 或未来 Vector / Embedding

03 只负责告诉本模块“什么数据发生了变化”。

具体索引更新逻辑由 04 负责。

---

### ③ Hybrid Retrieval / 混合检索

当前方向：

```text
Metadata 精确筛选
+
Keyword 关键词检索
+
可选 Vector 语义检索
```

V1 不要求依赖 Vector 才能运行。

优先保证：

- MOQ
- Price
- Material
- Size
- Factory
- Function
- Scenario
- Performance

等结构化条件可以稳定搜索。

Vector / Embedding 后续用于补强模糊表达、相似产品和语义检索能力。

---

### ④ Ranking & Search Result / 排序与检索结果

负责执行 02 Taxonomy & Rules 已定义的：

- 硬条件
- 软条件
- 优先级
- 排序偏好

核心规则：

- 硬条件不能被语义相似度突破。
- 没有完全满足全部硬条件时，必须明确标记“无完全匹配”。
- 最终结果必须保留具体 Factory Offer，不能只返回 SKU。

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

①已确认。后续按②③④继续细化和测试。