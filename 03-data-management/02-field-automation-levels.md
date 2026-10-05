# 02 Field Automation Levels / 字段自动化等级规范

Core 只定义四种处理等级：

- AUTO：原始资料有明确事实，可直接提取并做格式清洗；
- RULE：必须按当前 Product Profile 的词表 / Schema 标准化；
- REVIEW：存在语义歧义或主观判断，必须人工确认；
- MISSING：无足够依据，不得补猜。

具体某个产品字段属于哪一级，不写死在 Core。

每次导入前读取：

```text
profiles/active-profile.yaml
→ 当前 Product Profile
→ automation_levels
```

固定原则：

```text
AI 理解原文
↓
Product Profile 标准化
↓
人工确认 REVIEW
↓
Validation PASS
↓
正式写入 Product_KB
```

无依据不得推断；空白不得覆盖旧值。
