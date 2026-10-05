# 04 Category Display Fields / 品类展示字段

本文件只定义跨产品复用的展示框架。

统一框架：

```text
图片｜SKU｜关键规格｜MOQ｜价格｜⭐本次匹配度｜本次推荐理由
```

不同 Product_Category 的“关键规格”不得写死在 Core。

Agent 必须从当前 active Product Profile 的：

```yaml
display_fields:
```

读取该品类优先展示字段，并根据本次用户需求选择最相关的 2～4 项。

当前 Profile 入口：

```text
profiles/active-profile.yaml
```

核心原则：

1. 统一的是展示结构，不是所有品类使用同样字段。
2. 只显示真实 Product_KB / Search_Result 中存在的值。
3. 不得为了填满表格编造规格。
4. Product Profile 更换后，本文件无需修改。
