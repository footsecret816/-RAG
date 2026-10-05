---
name: product-knowledge-retrieval
description: Search, compare, and recommend internal company products from an external Product_KB using a structured + keyword + vector hybrid retrieval flow. Also supports explicit product-data maintenance requests. Never invent product facts.
compatibility: Requires access to Product_KB. For executable V1 retrieval, the full repository runtime under 04-search/runtime must be available to the agent environment.
metadata:
  author: runtong-wayyeah
  version: "1.2.0"
---

# Product Knowledge Retrieval Skill

这是公司的产品知识检索 Skill。

核心目标：

> 根据业务员自然语言需求，从真实 Product_KB 中找到合适的 Product SKU + Factory Offer，并给出可核对的匹配结果。

---

## 什么时候使用

用于：

- 推荐产品
- 查找 SKU
- 根据客户需求筛选产品
- 比较多个产品或工厂方案
- 查询材质、价格、MOQ、尺码、场景、性能
- 查询产品图片
- 查询 Packaging_Options / Packaging_SKU
- 明确的产品资料新增、修改、替换、删除

普通公司介绍、客户背调、写邮件等任务不要调用本 Skill。

---

## 数据真源

真实产品事实只允许来自：

`Product_KB`

Skill 不保存真实 SKU、价格、MOQ 或工厂数据。

无法访问 Product_KB 时：

1. 不猜测；
2. 提示连接或提供 Product_KB；
3. 获得访问后再继续。

---

## Profile 边界

查询或维护前先读取：

```text
profiles/active-profile.yaml
→ 当前 Company Profile
→ 当前 Product Profile
```

公司名、产品材质、功能、场景、性能字段、自然语言映射、展示字段不得写死在 Base Skill；这些信息只来自 Profile。

当前运行行为由 active Profile 决定；更换公司或产品时只替换 Profile 与 Product_KB，不修改 Core。

---

## V1 检索方式

完整仓库运行时存在时，默认使用：

```text
自然语言
↓
Search_Request
↓
04-search/runtime/search.py
↓
结构化条件 + 关键词 + 向量混合检索
↓
Search_Result
```

V1 Embedding 模型：

```text
intfloat/multilingual-e5-small
384维
```

聊天大模型可以变化，但当前索引必须统一使用同一 Embedding 模型。

---

## 查询规则

先按通用规则 + 当前 Product Profile 拆分：

```text
Product_Category
Hard Conditions
Soft Conditions
Priority（可带 goal=min/max）
Semantic Query
```

标准化时：

- 能可靠映射的场景 / 功能 / 性能先进入 soft_conditions；
- “越低越好 / 越高越好”写成 priority.goal=min/max；
- 模糊表达可以同时保留到 semantic_query 供向量辅助召回；
- semantic_query 不直接决定星级。

然后调用 04。

硬条件不能被关键词或语义相似度突破。

同一 SKU 多工厂必须按：

```text
Product SKU + Factory Offer
```

独立判断。

---

## 产品导入 / 维护

完整仓库运行时，数据维护统一走：

```text
03-data-management/runtime/
```

固定表格先生成 staging candidate；REVIEW 未确认时禁止写入正式 Product_KB。

正式提交必须：

```bash
python 03-data-management/runtime/maintenance.py candidate.json --commit --confirm --update-index
```

删除使用 `delete_product.py`，不得用空白值隐式删除。

---

## 索引初始化与更新

完整仓库运行时：

首次初始化：

```bash
python 04-search/runtime/bootstrap.py
python 04-search/runtime/build_index.py
python 04-search/runtime/validate_index.py
```

正式 Product_KB 发生明确维护变化后：

```bash
python 04-search/runtime/update_index.py
```

普通查询不得修改 Product_KB。

如果本地 Skill 不是 Git 仓库，在测试前执行：

```bash
python sync/verify_sync.py
```

只有受控文件全部一致，才把本地测试视为当前 GitHub 版本测试。

---

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

---

## 结果展示

默认每个 Product_Category 最多展示 5 款。

核心列：

```text
产品图片
SKU
品类关键规格
MOQ
Price
⭐本次需求匹配度
本次推荐理由
```

要求：

- Main_Image 可访问时优先直接显示；
- 星级必须直接使用 04 的结果；
- Agent 不得自行改星；
- Top 5 是上限，不强制凑满；
- Packaging_KB 未启用时不得编造包装；
- 默认回答保持简短。

详细规则以通用 Core + 当前 active Profile 为准。

---

## 平台兼容

本 Skill 不绑定任何指定智能体平台。

平台专属差异只放在：

`adapters/`

核心产品数据结构、检索规则、向量模型规定和排序逻辑保持平台无关。
