# Data Flow / 数据流

## 一、产品首次入库

```text
固定格式产品表格 + 图片
↓
03③ Ingestion & Normalization
↓
候选 product.md
↓
人工确认 REVIEW
↓
03⑤ Data Validation
↓
PASS
↓
正式写入 Product_KB
↓
03⑥ Change Set
↓
04② Search Index Sync
```

## 二、已有产品更新

```text
新表格 / 新图片
↓
03④ Product Maintenance
↓
差异比对
↓
人工确认变更意图
↓
03⑤ Data Validation
↓
PASS
↓
写入 Product_KB
↓
Change Set
↓
04② 同步搜索层
```

空白新值不覆盖旧值，删除必须是明确操作。

## 三、业务查询

```text
业务员自然语言
↓
06 Agent
↓
05 Query Normalization
↓
Search Request
↓
04 Search Engine
↓
Product SKU + Factory Offer
↓
05 标准化结果
↓
06 展示给业务员
```

未来 Packaging_KB 启用后，再动态组合 Packaging_SKU。
