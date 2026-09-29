# 03 Data Management

本模块负责真实产品知识从原始资料进入标准 Product_KB 后的完整数据维护流程。

## 当前核心流程

```text
固定格式产品表格 + 产品图片
        ↓
字段提取
        ↓
标准词与规则转换
        ↓
AI 语义理解
        ↓
必要字段人工确认
        ↓
标准化 Product_KB
        ↓
检索索引更新
```

## 已确认子板块

### ① Local KB Structure / 本地知识库结构 ✅

文件：

`01-local-kb-structure.md`

负责：

- 本地 Product_KB 怎么建立
- SKU 文件夹、product.md、主图命名
- 原始资料与正式知识库分离
- 同一 SKU 多 Factory Offer 的存储方式

### ② Field Automation Levels / 字段自动化等级 ✅

文件：

`02-field-automation-levels.md`

负责：

- AUTO / RULE / REVIEW / MISSING
- 每个鞋垫字段的自动化等级
- AI 自动判断边界
- 禁止对无依据字段进行猜测

### ③ Ingestion & Normalization / 表格导入与标准化 ✅

文件：

`03-ingestion-and-normalization.md`

负责：

- 固定格式产品表格导入
- 产品图片按 SKU 自动关联
- 一行数据识别为 SKU + Factory Offer
- 同 SKU 多工厂自动合并
- Material、标签和尺码标准化
- AI 从产品特性描述中提取功能、场景和性能候选
- REVIEW / MISSING 标记
- 生成标准 product.md 草稿

### ④ Product Maintenance / 增量更新与覆盖 ✅

文件：

`04-product-maintenance.md`

负责：

- 已存在 SKU 的差异更新
- 同 SKU + 同工厂的字段覆盖
- 同 SKU + 新工厂新增 Factory Offer
- 空白字段保护：空白不覆盖旧值
- 新图片确认后替换
- 删除必须由操作者明确发起
- 所有覆盖动作先展示差异、人工确认后写入

## 后续待确认

### ⑤ Data Validation / 数据校验

负责写入 Product_KB 前的数据完整性、合法性、重复项和 REVIEW 状态检查。

### ⑥ Index Sync Rules / 索引同步规则

负责 Product_KB 变更后，Metadata、Keyword、Vector / Embedding 等检索索引如何更新。

## 与其他模块关系

- `01-schema/`：规定产品有哪些字段
- `02-taxonomy-rules/`：规定字段使用什么标准词和映射规则
- `03-data-management/`：规定真实产品资料如何进入、修改和维护

真实 SKU、产品图片、工厂价格、MOQ 等业务数据不进入 GitHub。
