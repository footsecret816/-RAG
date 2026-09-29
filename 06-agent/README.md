# 06 Agent / 业务使用层

本模块定义业务员如何通过 Agent 使用产品检索系统。

Agent 是交互层，不是产品知识真源，也不是独立的推荐算法。

核心原则：

> 产品事实来自 Product_KB，产品检索来自 05 Retrieval Tool，Agent 负责调用工具和组织回答。

---

## 已确认子板块

### ① Agent Policy / Agent 职责 ✅

文件：

`01-agent-policy.md`

Agent 主要负责：

- 理解用户当前任务
- 判断是否需要调用产品检索工具
- 收集必要但缺失的查询条件
- 把用户需求传递给 05 Retrieval Tool
- 将工具结果整理成业务员容易使用的回答

Agent 不负责：

- 自行维护 Product_KB
- 自行生成产品事实
- 绕过 05 / 04 独立选择 SKU
- 修改搜索结果中的真实价格、MOQ、工厂、材质等事实

---

### ② Tool Calling Rules / 工具调用规则 ✅

文件：

`02-tool-calling-rules.md`

定义：

- 什么情况下必须调用产品检索工具
- 哪些用户需求需要补问
- 什么上下文应传给 05
- 如何处理无完全匹配
- 如何处理多个候选结果

Agent 应优先依赖结构化检索结果，而不是凭模型自身知识推荐公司内部产品。

---

### ③ Response Format / 最终回答格式 ✅

文件：

`03-response-format.md`

最终回答应尽量稳定展示：

- SKU
- 产品图片
- Factory_Name
- Material
- Size
- MOQ
- Price
- 匹配原因
- 未满足条件
- 必要说明

实际显示字段可以根据用户问题适当裁剪，但不得隐藏关键冲突。

---

## 平台无关原则

本模块核心规则不绑定具体平台。

未来如不同平台需要不同配置，可使用独立适配层，例如：

```text
adapters/
├─ accio/
├─ openai/
└─ other-platform/
```

平台适配只处理接口和配置差异，不复制一套新的产品业务规则。

---

## 与其他模块关系

```text
业务员
  ↓
06 Agent
  ↓
05 Retrieval Tool
  ↓
04 Search Engine
  ↓
Product_KB
```

Agent 不应脱离 05 返回结果重新判断“哪个 SKU 更合适”。

默认业务场景是只读产品查询；只有用户明确提供维护资料并明确要求新增、修改、替换或删除时，才转入 03 Data Management。

---

## 当前状态

①②③ 已完成 V1 规则设计。后续在 07-tests 中验证查询、维护分流和最终回答稳定性。