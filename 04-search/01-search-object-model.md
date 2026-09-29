# 01 Search Object Model / 搜索对象模型

本文件定义 04-search 中最基础的搜索对象。

## 核心规则

1. `Product_KB` 是真实数据源；Search Record 只是为检索生成的派生数据。
2. 当前产品搜索粒度固定为：

```text
Product SKU + Factory Offer
```

3. 同一 Product SKU 如果有多个 Factory Offer，应展开成多条独立搜索记录。
4. 产品层字段继承到每条 Factory Offer 搜索记录中。
5. `Packaging_Options` 当前只保存可关联的 `Packaging_SKU` 引用，不提前展开产品 × 工厂 × 包装组合。
6. 最终业务结果可以组合为：

```text
Product SKU + Factory Offer + Packaging SKU
```

但该组合在查询结果阶段动态生成，不作为当前 Product Search Record 的永久存储粒度。

---

## Product_Offer_Record

当前 V1 的产品搜索对象：

```text
Product_Offer_Record

Identity
├─ Product_Category
├─ SKU_ID
└─ Factory_Name

Product Fields
├─ Main_Image
├─ Function_Tags
├─ Scenario_Tags
├─ Special_Features
├─ Performance_Attributes
└─ Packaging_Options

Factory Offer Fields
├─ Material
├─ Material_Detail
├─ Price
├─ MOQ
├─ Size_System
└─ Size_Range
```

例如同一 SKU：

```text
F0228 + 富置高
F0228 + 王氏
```

应形成两条独立 `Product_Offer_Record`。

---

## 包装边界

当前只保留：

```text
Packaging_Options:
- PKG-IN-001
- PKG-IN-005
```

其中每个值都是未来独立 `Packaging_KB` 中的 `Packaging_SKU`。

当前 04① 不定义 Packaging_Record 的内部字段，也不建立包装搜索索引。

---

## 数据边界

Search Record：

- 可以由 Product_KB 重新生成；
- 不作为业务事实真源；
- 不允许反向覆盖 Product_KB；
- 具体索引结构与同步方式由 04② 定义。
