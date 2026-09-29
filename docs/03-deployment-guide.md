# Deployment Guide / 部署说明

当前架构不绑定具体 AI 或 Agent 平台。

## 基本组成

实际运行环境需要能够访问：

```text
本仓库规则 / 程序
+
Product_KB
+
Search / Retrieval Tool
+
Agent 平台
```

## Product_KB 存储

可根据实际环境放在：

- 本地硬盘
- 移动硬盘
- 公司局域网服务器

真实业务数据不要求进入 GitHub。

## Agent 平台

Accio、OpenAI 或其他平台只作为接入层。

平台变化时：

- 01～05 核心数据与检索逻辑尽量保持不变
- 06 可增加平台适配配置
- 不应把某个平台写成系统必要依赖

## V1 实施原则

优先实现：

```text
标准 Product_KB
+
Metadata Search
+
Keyword Search
+
Retrieval Tool
```

Vector / Embedding 可后续增加。
