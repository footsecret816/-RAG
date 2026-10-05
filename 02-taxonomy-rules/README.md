# 02 Taxonomy & Rules

本模块只保留**通用规则框架**。

- `A-framework/`：跨公司、跨产品复用的标签、近义词、查询条件、优先级、硬软条件和层级边界规则。
- 企业/产品专属的材质、功能、场景、性能、业务概念映射，不再写死在 Core；统一放到 `profiles/<company>/products/<product>/`。

当前启用 Profile：

```text
profiles/active-profile.yaml
→ company_profile: runtong
→ default_product_profile: insoles
```

当前润通鞋垫业务知识位于：

```text
profiles/runtong/products/insoles/
```

真实 SKU、工厂、价格、MOQ、图片等数据仍由外部 Product_KB 管理，不进入 Git。

`B-business-knowledge/` 仅保留兼容入口，避免旧引用失效；可执行与正式业务知识以 active profile 为准。
