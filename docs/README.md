# Docs / 系统级文档

本目录只保存整个系统的架构、部署、操作和版本说明。

具体业务规则仍由各模块自身维护。

Docs 不作为 Schema、标签、搜索规则或 Agent 规则的第二套真源。

---

## 当前规划

### ① Architecture / 总体架构

说明：

- 01～07 模块关系
- Product_KB 的位置
- 未来 Packaging_KB 的扩展关系
- Git 仓库与真实业务数据的边界
- 平台无关架构

---

### ② Data Flow / 数据流

描述完整链路：

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

以及 Product_KB 发生变化后：

```text
Change Set
→ 04 Search Index Sync
```

---

### ③ Deployment Guide / 部署说明

未来说明：

- 本地电脑部署
- 移动硬盘数据源
- 公司服务器部署
- 不同 Agent 平台接入
- Search / Retrieval Tool 的运行方式

部署文档不能把某一个平台写成整个系统的必要依赖。

---

### ④ Operation Guide / 管理员操作说明

面向实际维护人员说明：

- 如何新增产品
- 如何更新价格 / MOQ
- 如何新增工厂供应方案
- 如何处理 REVIEW
- 如何替换产品图片
- 如何触发或检查搜索同步
- 如何进行基础故障排查

---

### ⑤ Changelog / 系统更新记录

记录：

- Schema 重大变化
- Taxonomy 规则变化
- 搜索逻辑升级
- Retrieval Tool 接口变化
- Agent 规则变化
- 重大兼容性调整

---

## 文档边界

```text
01 = Schema 真源
02 = Taxonomy & Rules 真源
03 = Data Management 真源
04 = Search 真源
05 = Retrieval Tool 真源
06 = Agent 真源
07 = Tests 真源

docs = 解释整个系统，不复制一套规则
```

---

## 当前状态

当前仅完成系统文档结构规划。

后续在各核心模块稳定后逐步补齐正式文档。