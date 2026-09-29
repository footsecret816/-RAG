# 02 Index Build & Change Sync / 索引建立与变更同步

本文件定义 Product_KB 如何转换为可搜索索引，以及 Product_KB 发生变化后如何同步更新搜索层。

## 一、首次建立索引

基本流程：

```text
Product_KB
↓
读取 product.md
↓
按照 04① 生成 Product_Offer_Record
↓
建立 Search Index
```

当前 V1 优先支持：

- Metadata Index
- Keyword Index

Vector / Embedding 后续作为增强能力加入，不作为 V1 正常运行的前提。

---

## 二、接收 03⑥ Change Set

03-data-management 负责告诉 04：

> 哪个 SKU / Factory Offer 发生了什么变化。

04②负责决定：

> 搜索索引应该如何同步。

---

## 三、基本同步规则

### new_sku

```text
→ 为该 SKU 的所有 Factory Offer 新建 Product_Offer_Record
```

### new_factory_offer

```text
→ 新增一条 Product_Offer_Record
```

### update

```text
→ 找到对应 Product SKU + Factory Offer
→ 只更新变化字段
```

### image_update

```text
→ 更新该 SKU 相关 Product_Offer_Record 的 Main_Image 引用
```

### delete_factory_offer

```text
→ 删除对应 Product_Offer_Record
```

### delete_sku

```text
→ 删除该 SKU 的全部 Product_Offer_Record
```

---

## 四、更新范围原则

不同字段变化只更新必要部分。

例如：

```text
Price / MOQ 变化
→ 更新 Metadata

Function / Scenario / Material 变化
→ 更新 Metadata + Keyword

未来语义文本变化
→ 再决定是否重新生成 Embedding
```

V1 不要求因为任何普通字段变化都重建全部索引。

---

## 五、核心原则

1. Product_KB 是数据真源。
2. Search Index 可以从 Product_KB 重建。
3. Change Set 只描述变化，不负责搜索同步。
4. 增量更新优先，避免每次全量重建。
5. Vector / Embedding 是后续增强，不作为当前依赖。
