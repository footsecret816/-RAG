# Claude Adapter

本目录用于 Claude 的平台适配。

## 适配原则

Claude 只作为运行或交互外壳。

核心产品能力仍来自：

```text
01 Schema
02 Taxonomy & Rules
03 Data Management
04 Search
05 Retrieval Tool
06 Agent
07 Tests
```

## 统一接口

平台侧只需要完成：

```text
用户输入
→ 转交 05 Retrieval Tool
→ 使用统一 Search_Request
→ 接收统一 Search_Result
→ 由 06 Agent 组织最终回答
```

明确维护请求则转入 03 Data Management。

## 禁止

- 在本适配层重新定义产品 Schema
- 在本适配层重新维护标签规则
- 在本适配层自行写另一套排序逻辑
- 将平台专属配置写进 01～07 核心模块

## 当前状态

预留适配目录。

具体安装、插件、Skill、MCP、API 或运行配置，等实际部署到 Claude 时再按平台能力补充。
