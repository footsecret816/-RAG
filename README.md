# Product Knowledge Retrieval / 产品知识检索 Skill

这是一个平台无关的企业内部产品知识检索与维护 Skill。

目标：

```text
业务员自然语言
↓
Search_Request
↓
结构化条件 + Keyword + Vector
↓
Product SKU + Factory Offer
↓
紧凑推荐结果
```

## 架构

```text
Base Skill / Core
+
profiles/
+
外部 Product_KB
+
Search_Index
```

### Core

负责：

- 数据导入与维护
- Search_Request / Search_Result
- 结构化条件
- Keyword
- Vector
- Hybrid Ranking
- FAISS
- 索引更新
- Agent 展示框架
- Tests

### Profiles

```text
profiles/active-profile.yaml
→ Company Profile
→ Product Profile
```

公司名、产品材质、标签、性能字段、查询映射、展示字段等企业 / 产品专属信息放在 Profile，不写死在 Core。

当前仓库默认启用润通鞋垫 Profile。

未来换公司或产品时，目标是：

```text
Core 不改
↓
替换 Company / Product Profile
↓
导入新的 Product_KB
↓
build_index
```

## 真实数据

真实 SKU、图片、工厂、价格、MOQ、客户资料和 Search_Index 不进入 GitHub。

建议运行目录：

```text
Product_Data/
├─ Raw_Input/
├─ Product_KB/
├─ Packaging_KB/
├─ Search_Index/
└─ _models/
```

## 主要模块

- `01-schema/`：通用数据结构
- `02-taxonomy-rules/`：通用规则框架
- `03-data-management/`：导入、校验、维护
- `04-search/`：Hybrid Search
- `05-retrieval-tool/`：查询接口
- `06-agent/`：回答规则
- `07-tests/`：测试 / 回归
- `profiles/`：当前公司和产品专属配置
- `skills/`：Skill 包
- `adapters/`：平台适配
- `sync/`：离线一致性校验

当前检索粒度固定为：

```text
Product SKU + Factory Offer
```
