# 02 Field Automation Levels / 字段自动化等级规范

本文件只定义跨产品复用的自动化等级与边界。

## 四种等级

### AUTO

原始资料中有明确事实，可直接提取并做格式清洗，但不得改变事实。

典型公共字段：

- SKU_ID
- Factory_Name
- MOQ
- Price
- Price_Term
- Material_Detail
- Size_Range

### RULE

必须按 active Product Profile 的 Schema、词表和值域进行标准化。

如果无法可靠映射，不得创造新标准值，应转 REVIEW。

### REVIEW

AI 可以给出候选，但存在语义歧义、主观等级或结构判断时，必须人工确认后才能进入正式 Product_KB。

### MISSING

原始资料无足够依据时保持缺失，不得补猜。

## 产品专属自动化规则

具体某类产品哪些字段属于 RULE / REVIEW / MISSING，不写死在 Core。

当前 active Product Profile：

```text
profiles/active-profile.yaml
```

当前润通鞋垫规则：

```text
profiles/runtong/products/insoles/data-rules.md
```

## 核心原则

```text
AI 理解原文
↓
Product Profile 标准化
↓
人工处理歧义
↓
Validation PASS
↓
正式写库
```

任何自动化不得为了填满字段而编造事实。
