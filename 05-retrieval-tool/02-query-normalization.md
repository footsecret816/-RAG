# 02 Query Normalization / 查询标准化

本文件定义如何把业务员自然语言转换成 04-search 可执行的标准 Search_Request。

核心原则：

> 能可靠结构化的业务含义先结构化；向量负责补充模糊语义，不替代明确条件。

---

## 一、基本流程

```text
用户自然语言
↓
识别产品类别
↓
识别明确硬条件
↓
识别可映射的功能 / 场景 / 性能软条件
↓
识别相对优化目标（越低越好 / 越高越好）
↓
识别优先级
↓
保留仍有价值的模糊语义
↓
输出 Search_Request
```

---

## 二、不要把所有自然语言都丢给向量

例如用户说：

```text
每天站8小时，想脚底没那么累，MOQ最多3000。
```

应优先结构化为：

```json
{
  "product_category": "鞋垫",
  "hard_conditions": [
    {"field":"MOQ","op":"lte","value":3000}
  ],
  "soft_conditions": [
    {"field":"Scenario_Tags","op":"contains","value":"长时间站立"},
    {"field":"Function_Tags","op":"contains","value":"缓震"},
    {"field":"Function_Tags","op":"contains","value":"抗疲劳减压"}
  ],
  "priority": [],
  "semantic_query": "每天站8小时，想脚底没那么累"
}
```

说明：

- MOQ 是精确硬条件；
- “站8小时”可可靠映射到“长时间站立”；
- “脚底没那么累”可映射为缓震 / 抗疲劳减压倾向；
- 原始模糊表达仍可保留给向量，用于补充召回和同分排序。

这样星级由真实结构化条件计算，向量不直接决定星级。

---

## 三、Priority 增加 goal

`priority` 不再只表示“这个字段有多重要”，还可以表示相对优化方向。

标准结构：

```json
[
  {"field":"MOQ","level":"high","goal":"min"},
  {"field":"Price","level":"low","goal":"min"},
  {"field":"Elasticity","level":"medium","goal":"max"}
]
```

### level

```text
high   = 高优先级
medium = 中优先级
low    = 低优先级
```

### goal

当前 V1 支持：

```text
min = 越低越好
max = 越高越好
```

例如：

```text
“MOQ越低越好”
→ {"field":"MOQ","level":"high","goal":"min"}

“价格贵一点没关系”
→ {"field":"Price","level":"low","goal":"min"}

“回弹越高越好”
→ {"field":"Elasticity","level":"high","goal":"max"}
```

如果用户只强调“这个条件很重要”，但没有明确越高 / 越低方向，可以只写 level，不写 goal。

---

## 四、硬条件 / 软条件 / 相对偏好必须分清

### 硬条件

用户明确不能违反：

```text
必须
不能超过
至少
只能
不要某材质
```

例如：

```json
{"field":"MOQ","op":"lte","value":3000}
```

### 软条件

用户希望满足的具体属性：

```text
希望缓震
最好适合长时间站立
不要太软
最好有足弓支撑
```

例如：

```json
{"field":"Softness","op":"range","value":[1,3]}
```

### 相对偏好

没有具体阈值，只表达候选之间谁更优：

```text
MOQ越低越好
价格越便宜越好
回弹越高越好
```

使用：

```text
priority + goal
```

不要为了表达“越低越好”凭空造一个阈值。

---

## 五、Semantic_Query

Semantic_Query 用于保留：

- 模糊场景描述
- 感受型表达
- 无法完全映射的业务语言
- 相似产品描述

但以下内容不应只依赖 Semantic_Query：

- 价格
- MOQ
- 明确材质
- 明确尺码
- 已经有标准字段可表达的硬条件

允许同一句模糊表达：

```text
既映射成软条件
+
又保留原始语义给向量
```

因为：

- 软条件负责匹配分 / 星级；
- 向量负责召回和辅助排序。

---

## 六、示例：户外 + MOQ + 不要太软

用户：

```text
要 PU 的，户外用，MOQ 不能超过 3000，
价格其次，不要太软。
```

标准化：

```json
{
  "product_category": "鞋垫",
  "hard_conditions": [
    {"field":"Material","op":"eq","value":"PU"},
    {"field":"MOQ","op":"lte","value":3000}
  ],
  "soft_conditions": [
    {"field":"Scenario_Tags","op":"contains","value":"户外徒步"},
    {"field":"Softness","op":"range","value":[1,3]}
  ],
  "priority": [
    {"field":"Price","level":"low","goal":"min"}
  ],
  "semantic_query": "户外使用，不要太软"
}
```

---

## 七、示例：测试产品，MOQ 优先，价格次要

用户：

```text
客户先测试产品，MOQ越低越好，价格贵一点没关系。
```

标准化：

```json
{
  "product_category": "鞋垫",
  "hard_conditions": [],
  "soft_conditions": [],
  "priority": [
    {"field":"MOQ","level":"high","goal":"min"},
    {"field":"Price","level":"low","goal":"min"}
  ],
  "semantic_query": "客户先测试产品"
}
```

此时即使没有 soft_conditions，MOQ / Price 仍会参与实际排序。

---

## 八、核心规则

1. 标准字段必须服从 01 Schema。
2. 标准词必须服从 02 Taxonomy & Rules。
3. 能可靠结构化的条件不能全部留给向量。
4. 用户明确“必须、不能超过”等，优先视为硬条件。
5. “最好、希望、不要太软”等视为软条件。
6. “越低越好 / 越高越好”使用 priority.goal。
7. 不得为了相对偏好凭空造数值阈值。
8. Semantic_Query 负责补充语义，不直接决定星级。
9. 不确定表达不得强行映射成不存在的标准值。
10. 05 只负责生成 / 校验检索请求，不负责自行选择产品。
