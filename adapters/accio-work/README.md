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

## 产品图片展示规则

Accio 已验证可以直接显示 Product_KB 中的图片，因此产品推荐结果应优先直接渲染图片。

优先级：

```text
① 推荐表单元格内直接显示真实图片
② 表格内无法显示时，在对应 SKU 附近直接显示缩略图
③ 前两种都失败时，才使用可点击图片引用 / 附件预览
```

在 Accio 中不要把以下形式作为默认结果：

```text
main.jpg
附件图标
仅文件名链接
需要点击后才能看到的图片预览
```

如果读取到 `Main_Image`：

- 尽量使用平台支持的图片渲染 / 附件展示能力直接显示图片本体；
- 图片必须与对应 SKU 紧邻；
- 多个 SKU 时应分别显示各自图片；
- 不要因为使用 Markdown 表格而退化成只显示文件名。

如果 Accio 某次会话无法把图片直接嵌入表格，应改用：

```text
【直接显示产品缩略图】
SKU｜关键规格｜MOQ｜价格｜星级｜推荐理由
```

而不是仅输出 `main.jpg`。

Packaging_KB 启用后，包装图片遵循同样规则。

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
