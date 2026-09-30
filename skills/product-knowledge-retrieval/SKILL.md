---
name: product-knowledge-retrieval
description: Search, compare, and recommend internal company products from an external Product_KB. Use when users ask for suitable SKUs, product recommendations, factory offers, materials, MOQ, price, size, performance, scenarios, product images, or Packaging_SKU references. Also recognize explicit product-data maintenance requests and route them through the defined maintenance flow. Never invent product facts.
compatibility: Requires the agent runtime to have read access to the company's Product_KB folder. Product_KB is external business data and is not bundled in this skill.
metadata:
  author: runtong-wayyeah
  version: "1.0.1"
---

# Product Knowledge Retrieval Skill

这是公司的产品知识检索 Skill。

核心目标：

> 根据业务员的自然语言需求，从真实 Product_KB 中找到合适的 Product SKU + Factory Offer，并给出可核对的匹配原因。

## 什么时候使用

当用户提出以下任务时启用本 Skill：

- 推荐产品
- 查找某个 SKU
- 根据客户需求筛选产品
- 比较多个产品或多个工厂方案
- 查询材质、价格、MOQ、尺码、使用场景、性能
- 查询产品图片
- 查询 Packaging_Options / Packaging_SKU
- 明确要求新增、修改、替换或删除产品资料

普通公司介绍、客户背调、写邮件等非产品库任务不要调用本 Skill。

## 数据真源

真实产品事实只允许来自：

`Product_KB`

本 Skill 自身不保存真实 SKU、真实价格、真实 MOQ、真实工厂数据。

如果当前运行环境无法访问 Product_KB：

1. 不要猜测产品信息；
2. 提示用户连接或提供 Product_KB 路径；
3. 获得访问后再继续。

## 查询主流程

```text
用户自然语言
↓
识别 Product_Category
↓
拆分 Hard Conditions / Soft Conditions / Priority
↓
读取 Product_KB
↓
每个 Product SKU + Factory Offer 独立判断
↓
先满足硬条件
↓
再按用户优先级和软条件排序
↓
输出结果
```

详细规则见：

- `references/data-model.md`
- `references/query-rules.md`
- `references/runtime-and-maintenance.md`

## 核心检索粒度

必须按：

```text
Product SKU + Factory Offer
```

处理。

同一 SKU 有多个工厂时，不得把不同工厂的 Price、MOQ、Material、Size 混在一起。

## 硬条件规则

硬条件必须满足。

例如：

```text
PU
MOQ <= 3000
指定尺码
指定特殊属性
```

Keyword、语义相似度或“看起来很合适”都不能突破硬条件。

如果没有完全匹配：

- 明确说明没有完全符合的结果；
- 可以给最接近候选；
- 必须列出 Unmet_Conditions。

## 禁止编造

不得自行编造：

- SKU
- Factory_Name
- Material
- Material_Detail
- Price
- MOQ
- Size
- Packaging_SKU
- 产品性能数据

资料缺失就明确说缺失。

## 标准结果

优先返回：

```text
Product SKU
Main Image
Factory_Name
Material
Material_Detail
Price
MOQ
Size_System / Size_Range
Packaging_Options
Match_Reasons
Unmet_Conditions
```

根据用户问题可隐藏不相关字段，但不能改变事实。

## 产品维护

默认模式是查询。

只有用户：

1. 明确提供产品维护资料；
2. 并明确要求新增 / 修改 / 替换 / 删除；

才进入维护流程。

不要因为用户在聊天里提到一个新价格或新 MOQ 就自动更新 Product_KB。

维护流程见：

`references/runtime-and-maintenance.md`

## REVIEW 确认方式

需要人工确认的候选字段必须集中展示，并给每项分配简短编号。

默认优先让操作者直接回复：

```text
确认
```

如果只调整部分内容，则接受：

```text
P2=3
去掉S2
P=344
S=12
```

不要要求操作者重新输入 AI 已经展示过的完整场景词或长段文字。

KB 路径、价格口径等全局配置默认只确认一次。

## 平台兼容原则

本 Skill 不依赖 Accio Work、Codex、Claude、WorkBuddy、DeepSeek Harness 中任何一家。

平台只负责：

- 让 Skill 被触发；
- 让 Agent 访问 Product_KB；
- 提供文件读取 / 搜索能力。

产品 Schema、检索规则和业务逻辑保持平台无关。
