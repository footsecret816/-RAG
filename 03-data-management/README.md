# 03 Data Management

本模块负责真实产品知识从“原始资料”进入标准 Product_KB 后的完整数据维护流程。

## 当前核心原则

```text
原始 Excel / 图片 / 供应商资料
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

## 当前文件

1. `01-local-kb-structure.md`
   - 定义本地 Product_KB 怎么建立
   - SKU 文件夹、product.md、主图的命名与目录规则
   - 原始资料与正式知识库分离

2. `02-field-automation-levels.md`
   - 定义 AUTO / RULE / REVIEW / MISSING
   - 明确每一个鞋垫字段的自动化等级
   - 禁止 AI 对无依据字段进行猜测

## 后续计划

```text
03-raw-data-ingestion.md
04-data-normalization.md
05-create-product.md
06-update-product.md
07-manage-factory-offer.md
08-data-validation.md
09-index-sync-rules.md
10-change-log.md
```

## 与其他模块关系

- `01-schema/`：规定“产品有哪些字段”
- `02-taxonomy-rules/`：规定“字段使用什么标准词和映射规则”
- `03-data-management/`：规定“真实资料如何转换、写入、修改和维护”

真实 SKU、产品图片、工厂价格、MOQ 等业务数据不进入 GitHub。
