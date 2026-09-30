# 02 Field Automation Levels / 字段自动化等级规范

本文件定义从原始 Excel、供应商资料和业务描述生成标准 Product_KB 时，各字段允许采用的自动化方式。

目标：

- 明确哪些字段可以自动入库。
- 明确哪些字段必须经过固定规则标准化。
- 防止 AI 对缺失信息进行猜测。
- 将人工工作集中到真正有歧义的字段。

---

## 一、四种处理等级

### AUTO

原始资料中存在明确事实，可以直接提取。

例如：

- SKU_ID
- Factory_Name
- MOQ
- Price

允许做格式清洗，但不得改变原始事实。

---

### RULE

必须根据固定 Schema、词表或转换规则处理。

AI 可以负责理解原始文字，但最终输出必须落到已经批准的标准值。

例如：

```text
Memory Foam
慢回弹海绵
慢回弹泡棉
→ Material = 记忆棉
```

如果无法可靠映射，不得自行创造新标准词，应转为 REVIEW。

---

### REVIEW

AI 可以给出建议结果，但存在主观判断、等级判断或语义歧义，必须人工确认后才能成为正式数据。

例如：

```text
“缓震比较明显”
→ Cushioning 建议 4
→ REVIEW
```

---

### MISSING

原始资料没有提供足够依据。

系统不得补猜。

例如：

原始描述没有后跟杯信息：

```text
Heel_Cup_Depth = 待补充
状态 = MISSING
```

---

## 二、鞋垫字段当前处理等级

| 字段 | 当前等级 | 处理原则 |
|---|---|---|
| Product_Category | RULE | 根据导入产品类别确定 |
| SKU_ID | AUTO | 直接提取货号/产品编号 |
| Main_Image | AUTO | 根据 SKU 对应图片建立引用 |
| Factory_Name | AUTO | 原表明确工厂名称时直接提取 |
| MOQ | AUTO | 去掉“双”等单位后保存数值 |
| Price | AUTO | 提取实际价格数值；原始备注不得误当价格 |
| Material | RULE | 必须映射到 02-B 材质标准词 |
| Material_Detail | AUTO | 保留原始详细材质信息，可做格式整理 |
| Size_Range | AUTO | 保留实际尺码范围 |
| Size_System | RULE | 根据明确格式转换，如 EU、US、UK、Alpha |
| Function_Tags | RULE | AI理解原文后，只能映射到批准的标准标签；模糊时转 REVIEW |
| Scenario_Tags | RULE / REVIEW | 原文明确场景时 RULE；未明确写场景但可从产品语义中合理提炼时生成标准场景候选并标记 REVIEW；完全无依据时 MISSING |
| Special_Features | RULE | 只有原始资料明确出现时才能写入 |
| Cushioning | REVIEW | 当前 1–5 评分存在主观性 |
| Elasticity | REVIEW | 当前 1–5 评分存在主观性 |
| Softness | REVIEW | 当前 1–5 评分存在主观性 |
| Arch_Support | RULE / REVIEW | 明确描述可规则化；模糊描述需确认 |
| Arch_Height | MISSING / REVIEW | 原资料通常缺失；有结构依据时再判断 |
| Heel_Cup_Depth | MISSING / REVIEW | 原资料通常缺失；有结构依据时再判断 |

---

## 三、明确事实优先

只要原始资料能够直接支持，就优先自动处理。

例如原文：

```text
货号：F0228
鞋垫材质：PU
起订量：3000双
价格：6.9
工厂：富置高
```

可以直接生成：

```text
SKU_ID = F0228
Material = PU
MOQ = 3000
Price = 6.9
Factory_Name = 富置高
```

其中 Material 仍需通过标准材质词表校验。

---

## 四、自然语言功能与场景

例如原文：

```text
透气，缓震但是有韧性，柔软，
没有支撑片，但是足弓有一点点软垫支撑
```

可以自动提取候选：

```text
Function_Tags:
- 透气排湿
- 缓震
- 回弹
- 足弓支撑

Arch_Support:
- 轻度支撑
```

规则：

- Function_Tags 与 Scenario_Tags 都必须映射到 02-B 中已经存在的标准词。
- Function_Tags：原文没有表达的功能，不得因为“这种材料通常具有某功能”而自动补上。
- Scenario_Tags：允许 AI 根据整段产品语义（特性、材质、结构描述等）提炼适用场景，但只能从已批准的 Scenario_Tags 中选择。
- 若场景不是原文明确事实，而是基于语义判断得到，必须标记为 REVIEW，待操作者确认后才能写入正式 Product_KB。
- 只有完全缺乏语义依据时，Scenario_Tags 才标记为 MISSING。

---

## 五、性能评分不得拍脑袋

当前：

- Cushioning
- Elasticity
- Softness

使用 1–5 等级。

在没有建立更加成熟的评分转换规则前，AI只能生成“建议值”，不能直接作为正式值入库。

例如：

```text
“非常柔软”
→ Softness 建议 4–5
→ REVIEW
```

未来当公司形成稳定的评分基准、样品对照或关键词转换标准后，可以将部分 REVIEW 字段升级为 RULE。

---

## 六、无依据不得推断

以下行为禁止：

```text
PU 材质
→ 自动推断缓震 = 4        ×

运动鞋垫
→ 自动推断足弓支撑 = 强   ×

图片看起来后跟较深
→ 未经明确规则直接写“深” ×
```

应优先写：

```text
待人工确认
```

或：

```text
MISSING
```

---

## 七、建议的处理状态

数据清洗工具可以对每个字段生成状态：

```text
✅ AUTO / RULE 通过，可自动入库
⚠ REVIEW，需要人工确认
— MISSING，原始资料没有依据
```

最终只将已确认的数据写入正式 Product_KB。

---

## 八、核心原则

```text
AI负责理解原文
        ↓
规则负责标准化
        ↓
人工只处理歧义和缺失
```

任何自动化都必须服从：

- 01 Schema
- 02 Taxonomy & Rules

不得为了填满字段而编造数据。
