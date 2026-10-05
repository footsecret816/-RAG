# 04 Category Display Fields / 品类展示字段

统一展示框架保持不变：

```text
图片｜SKU｜关键规格｜MOQ｜价格｜⭐本次匹配度｜本次推荐理由
```

Base Skill 不写死某个产品类别的“关键规格”。

具体优先展示字段从当前 Product Profile 的：

```yaml
display_fields:
```

读取，并根据本次用户需求选择最相关的 2～4 项。

规则：

- 只展示真实 Product_KB / Search_Result 中存在的值；
- 不为填满表格编造规格；
- 更换 Product Profile 后，本文件无需修改。
