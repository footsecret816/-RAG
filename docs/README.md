# Docs / 系统级文档

本目录只负责解释整个系统，不作为业务规则的第二套真源。

## 当前文档

### ① Architecture / 总体架构 ✅
`01-architecture.md`

### ② Data Flow / 数据流 ✅
`02-data-flow.md`

### ③ Deployment Guide / 部署说明 ✅
`03-deployment-guide.md`

### ④ Operation Guide / 管理员操作说明 ✅
`04-operation-guide.md`

### ⑤ Changelog / 系统更新记录 ✅
`05-changelog.md`

## 真源边界

```text
01 = Schema 真源
02 = Taxonomy & Rules 真源
03 = Data Management 真源
04 = Search 真源
05 = Retrieval Tool 真源
06 = Agent 真源
07 = Tests 真源

docs = 系统说明
```

如 docs 与具体模块规则发生冲突，以对应 01～07 模块为准。
