# 产品知识库与智能检索系统

这是一套**平台无关、Profile 可替换**的企业产品知识库与智能检索系统。

目标：让业务员用自然语言查询公司真实 Product_KB，并稳定返回具体 Product SKU + Factory Offer。

## 三层结构

```text
Base Skill / Core
↓
Company + Product Profiles
↓
真实 Product_KB + Search_Index
```

当前仓库默认启用润通 Profile，但润通/鞋垫专属信息应集中在 `profiles/runtong/`，Core 不应依赖这些具体业务词。

## 系统结构

1. `01-schema/`：公共数据结构
2. `02-taxonomy-rules/`：通用标签 / 查询规则框架
3. `03-data-management/`：导入、更新、校验、正式写库、Change Set
4. `04-search/`：结构化 + Keyword + Vector 混合检索与排序
5. `05-retrieval-tool/`：Search_Request / Search_Result 接口
6. `06-agent/`：业务使用与展示规则
7. `07-tests/`：单元测试与真实业务回归
8. `profiles/`：可替换的公司与产品模块
9. `skills/`：可安装 Skill
10. `adapters/`：Accio 等平台适配
11. `docs/`：架构与部署说明

## 当前 active profile

```text
profiles/active-profile.yaml
→ company_profile: runtong
→ default_product_profile: insoles
```

润通公司运行配置：

```text
profiles/runtong/company.yaml
```

润通鞋垫产品规则：

```text
profiles/runtong/products/insoles/
```

## 核心数据流

```text
原始产品表格 + 图片
↓
03 Data Management
↓
Product_KB
↓
04 Search Engine
  = structured + keyword + vector
↓
05 Retrieval Tool
↓
06 Agent
↓
业务员
```

## 数据边界

真实业务数据不进入 GitHub。

建议运行目录：

```text
Product_Data/
├─ Raw_Input/
├─ Product_KB/
├─ Packaging_KB/
├─ Search_Index/
└─ _models/
```

GitHub 保存的是：

- Base Skill / Core
- Company / Product Profiles
- Schema 与规则
- 数据管理逻辑
- 检索逻辑
- Agent 规则
- 测试与同步规范

## Profile 替换原则

未来换公司或产品时，目标是：

```text
Core 不改
↓
替换 Company Profile
↓
替换 Product Profile
↓
导入新的 Product_KB
↓
build_index
```

当前阶段不做复杂 Onboarding 自动化，先保证润通效果不变并完成模块边界。

## 检索粒度

```text
Product SKU + Factory Offer
```

未来 Packaging_KB 启用后可扩展为：

```text
Product SKU + Factory Offer + Packaging SKU
```

## 跨平台接口

```text
Search_Request
Search_Result
Change_Set
```

平台专属差异只放入 `adapters/`。
