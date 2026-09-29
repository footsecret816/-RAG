# Accio Work Adapter

本目录只记录 Accio Work 的安装与接入方式。

核心 Skill 位于：

```text
skills/product-knowledge-retrieval/
```

不要在本目录复制另一套产品规则。

## 安装到 Accio Work

1. 下载或 Clone 本 GitHub 仓库。
2. 在 Accio Work 打开 Skills。
3. 选择 Install Local Skill / Upload。
4. 选择本地目录：

```text
skills/product-knowledge-retrieval/
```

5. 安装后启用该 Skill。
6. 在“润通业务 AI 助理”等目标 Agent 中勾选 / 分配该 Skill。
7. 用产品查询测试是否触发。

例如：

```text
/ product-knowledge-retrieval

客户要 PU 鞋垫，户外使用，MOQ 不超过 3000，
价格不是第一优先级，有什么合适的？
```

## Product_KB

Skill 本身不包含真实产品数据。

Accio Work 运行时还需要能够访问实际：

```text
Product_KB/
```

如果 Agent 无法访问 Product_KB，只能加载规则，不能真实查产品。

## 当前 V1 运行方式

当前属于 Agent-driven retrieval：

```text
Accio Agent
↓
Product Knowledge Retrieval Skill
↓
读取 Product_KB
↓
按 Skill 规则筛选 / 排序
↓
返回 Product SKU + Factory Offer
```

04 Search Engine / 05 Retrieval Tool 的真正代码化版本属于下一阶段。

## 平台边界

Accio Work 只是一个运行平台。

核心 Skill 使用标准 `SKILL.md` 结构，平台专属配置不进入 01～07。
