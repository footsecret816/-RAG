# 06 Data Change Handoff / 数据变更交接

本文件定义 Product_KB 成功写入后，03-data-management 如何把“发生了什么变化”交给 04-search。

⑥不负责真正更新搜索索引，也不决定是否重新生成 Embedding。

这些属于 04-search。

---

## 一、职责边界

⑥只负责生成标准化的变更信息。

例如：

```text
SKU_ID: F0228
change_type: update

changed_fields:
- Price
- MOQ
```

然后交给 04-search。

⑥不负责：

- Metadata Index 如何更新
- Keyword Index 如何更新
- Vector Index 如何更新
- 是否重新生成 Embedding
- 搜索排序如何变化

这些规则全部由 04-search 定义。

---

## 二、触发条件

只有在以下条件都满足后才生成 Change Handoff：

```text
③ 或 ④ 处理完成
+
⑤ Validation = PASS
+
Product_KB 已成功写入
```

如果没有实际变化：

```text
→ 不生成无意义的变更事件
```

---

## 三、变更类型

V1 至少支持以下 change_type：

### new_sku

新增 SKU。

```text
change_type = new_sku
```

### update

已有字段发生变化。

```text
change_type = update
```

### new_factory_offer

同一 SKU 新增工厂供应方案。

```text
change_type = new_factory_offer
```

### delete_factory_offer

操作者明确删除某个 Factory Offer。

```text
change_type = delete_factory_offer
```

### image_update

产品主图发生替换。

```text
change_type = image_update
```

### delete_sku

操作者明确删除整个 SKU。

```text
change_type = delete_sku
```

---

## 四、标准 Change Set

建议最少输出：

```text
Change_Set

SKU_ID:
change_type:
Factory_Name:
changed_fields:
```

其中 Factory_Name 仅在涉及具体 Factory Offer 时填写。

---

## 五、示例：价格与 MOQ 更新

```text
Change_Set

SKU_ID: F0228
change_type: update
Factory_Name: 富置高

changed_fields:
- Price
- MOQ
```

⑥只说明“Price 和 MOQ 变了”。

至于搜索系统应该更新什么，由 04-search 判断。

---

## 六、示例：新增工厂

```text
Change_Set

SKU_ID: F0228
change_type: new_factory_offer
Factory_Name: 王氏

changed_fields:
- Factory_Name
- Material
- Price
- MOQ
- Size_System
- Size_Range
```

---

## 七、示例：产品层标签变化

```text
Change_Set

SKU_ID: F0228
change_type: update

changed_fields:
- Function_Tags
- Scenario_Tags
```

⑥不判断这些字段是否需要重新生成 Embedding。

只把变更事实交给 04-search。

---

## 八、示例：图片替换

```text
Change_Set

SKU_ID: F0228
change_type: image_update

changed_fields:
- Main_Image
```

---

## 九、与 04-search 的边界

03-data-management 到⑥为止，只回答：

> 哪个 SKU 发生了什么变化？

04-search 再回答：

> 这个变化需要更新哪些检索能力？

整体边界：

```text
03 Data Management
= 管数据本身

04 Search
= 管数据如何被搜索
```

---

## 十、核心原则

```text
数据先通过⑤校验
→ 成功写入 Product_KB
→ ⑥生成标准 Change Set
→ 交给 04-search
```

⑥是 03 和 04 之间的交接层，不是搜索索引执行层。
