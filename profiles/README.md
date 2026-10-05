# Profiles / 企业与产品模块

本目录只保存**可替换的企业与产品 Profile**。

核心原则：

- Core 代码不应写死“润通”“鞋垫”“PU”“足弓支撑”等企业/产品专属事实；
- 当前默认启用 `runtong` + `insoles`；
- 未来换公司或换产品时，应优先替换本目录 Profile，而不是修改核心检索代码；
- 真实 SKU、价格、MOQ、图片、工厂资料仍放在外部 Product_KB，不进入 GitHub。

当前结构：

```text
profiles/
├─ active-profile.yaml
├─ profile_loader.py
└─ runtong/
   ├─ company.yaml
   └─ products/
      └─ insoles/
         ├─ profile.yaml
         ├─ schema.md
         ├─ data-rules.md
         └─ 业务词表 / 映射说明
```

当前阶段只做“润通运行效果保持不变 + 专属信息模块化”，不提前实现复杂企业 Onboarding。
