# 02 Taxonomy & Rules

本模块保留跨产品复用的查询与标签规则框架。

通用规则位于：

```text
02-taxonomy-rules/A-framework/
```

公司 / 产品专属内容不再属于 Core 真源，统一读取：

```text
profiles/active-profile.yaml
→ 当前 Company Profile
→ 当前 Product Profile
```

当前润通鞋垫标准词、性能字段、自然语言映射等以：

```text
profiles/runtong/products/insoles/profile.yaml
```

为可执行真源。

旧的 B-business-knowledge 内容仅作为历史说明，不得覆盖 active Product Profile。
