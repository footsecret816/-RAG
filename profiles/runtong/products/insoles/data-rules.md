# Data Rules / 润通鞋垫数据处理规则

本文件属于润通鞋垫 Product Profile。

## 字段自动化等级

| 字段 | 等级 | 处理原则 |
|---|---|---|
| Product_Category | RULE | 使用当前 Product Profile 标准类别 |
| SKU_ID | AUTO | 直接提取 |
| Main_Image | AUTO | 按 SKU 关联，冲突时 REVIEW |
| Factory_Name | AUTO | 原始资料明确时直接提取 |
| MOQ | AUTO | 格式清洗后保存数值 |
| Price | AUTO | 提取实际价格数值 |
| Price_Term | AUTO | 有则原样保留；空白不覆盖旧值 |
| Material | RULE | 映射到 profile.yaml 批准材质 |
| Material_Detail | AUTO | 保留事实性详细材质 |
| Size_Range | AUTO | 保留实际范围 |
| Size_System | RULE | 映射到 profile.yaml 标准值 |
| Function_Tags | RULE / REVIEW | 只能使用批准标签；歧义时 REVIEW |
| Scenario_Tags | RULE / REVIEW | 明确场景可 RULE；语义推断必须 REVIEW |
| Special_Features | RULE | 只有原始资料明确出现才写入 |
| Cushioning | REVIEW | 1–5 主观等级，需确认 |
| Elasticity | REVIEW | 1–5 主观等级，需确认 |
| Softness | REVIEW | 1–5 主观等级，需确认 |
| Arch_Support | RULE / REVIEW | 明确描述可规则化；模糊时 REVIEW |
| Arch_Height | MISSING / REVIEW | 有结构依据时再判断 |
| Heel_Cup_Depth | MISSING / REVIEW | 有结构依据时再判断 |

## 原则

- AI 负责理解原文；
- Profile 负责标准词与值域；
- 人工只处理歧义和缺失；
- 不得因为材质“通常具有某功能”而补造功能；
- 空白不得覆盖旧值；
- REVIEW 未确认不得写入正式 Product_KB。
