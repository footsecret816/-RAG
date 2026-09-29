# Adapters / 平台适配层

本目录只处理不同智能体平台的接入差异。

核心原则：

```text
01～07
= 平台无关核心能力

adapters/
= 平台接入与配置差异
```

任何平台适配都不得复制或改写一套新的 Schema、Taxonomy、Search 或 Retrieval 业务规则。

统一内部接口以：

- `Search_Request`
- `Search_Result`
- `Change_Set`

为准。

当前预留：

- Accio Work
- WorkBuddy
- Codex
- DeepSeek Harness
- Claude
- Generic

各平台目录当前只定义接入边界；具体安装文件、命令或配置格式应根据平台实际能力单独补充。
