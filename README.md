# 产品知识库与智能检索系统

这是一套**平台无关**的企业产品知识库与智能检索系统。

目标是让业务员使用自然语言查询公司真实产品库，并稳定返回具体的产品与供应方案。

## 核心目标

```text
业务需求
↓
找到合适 Product SKU
↓
找到具体 Factory Offer
↓
未来可继续关联 Packaging SKU
```

当前产品检索粒度：

```text
Product SKU + Factory Offer
```

未来完整业务方案：

```text
Product SKU + Factory Offer + Packaging SKU
```

## 系统结构

1. `01-schema/`  
   定义产品数据结构和标准 product.md 模板。

2. `02-taxonomy-rules/`  
   定义标准词、自然语言映射、硬软条件和业务规则。

3. `03-data-management/`  
   负责产品资料导入、更新、校验、正式写库与 Change Set。

4. `04-search/`  
   负责 Search Object、索引同步、混合检索与排序。

5. `05-retrieval-tool/`  
   把自然语言转换成标准 Search Request，并调用 04。

6. `06-agent/`  
   业务使用入口。默认查询；明确维护请求才转 03。

7. `07-tests/`  
   验证数据链路、搜索、Retrieval Tool、Agent 与回归稳定性。

8. `docs/`  
   总体架构、数据流、部署和管理员操作说明。

## 核心数据流

```text
原始产品表格 + 图片
↓
03 Data Management
↓
Product_KB
↓
04 Search Engine
↓
05 Retrieval Tool
↓
06 Agent
↓
业务员
```

## 数据边界

真实业务数据不进入本 GitHub 仓库。

建议实际存储：

```text
Product_Data/
├─ Raw_Input/
├─ Product_KB/
│  ├─ insoles/
│  ├─ shoe-care/
│  └─ ...
└─ Packaging_KB/   # 未来预留
```

本仓库只管理：

- Schema
- Taxonomy & Rules
- 数据管理逻辑
- 搜索逻辑
- Retrieval Tool 规则
- Agent 规则
- 测试规范
- 系统文档

## Packaging_KB

包装作为独立知识对象管理。

每个包装未来拥有独立：

```text
Packaging_SKU
```

产品通过：

```text
Packaging_Options
```

引用可关联的 Packaging_SKU。

当前 V1 只保留接口，不展开 Packaging_KB 内部 Schema。

## 当前状态

**V1 架构与规则设计已完成。**

已完成 01～07 的 V1 规则设计和系统级文档。

下一阶段重点：

```text
建立真实 Product_KB
→ 实现可执行 Search / Retrieval Tool
→ 用真实脱敏案例跑 07 Tests
→ 根据测试结果迭代
```

本项目保持平台无关，避免把核心产品知识和检索逻辑绑定到单一 Agent 平台。
