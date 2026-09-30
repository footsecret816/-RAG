# 04 Ranking & Search Result / 排序与搜索结果

本文件定义候选结果如何排序，以及 04 最终向 05 返回什么。

## 一、排序优先级

固定顺序：

```text
硬条件满足
>
用户明确优先级
>
软条件匹配度
>
Keyword / Semantic 相似度
```

---

## 二、用户优先级

必须服从 02 Taxonomy & Rules。

例如：

```text
“MOQ越低越好，价格贵一点没关系”
```

应理解为：

```text
MOQ = 高优先级
Price = 低优先级
```

不能因为某个候选价格更低，就自动把它排在 MOQ 更合适的候选前面。

---

## 三、硬条件规则

任何违反硬条件的结果：

```text
→ 不进入完全匹配结果
```

例如：

```text
用户要求 MOQ <= 1000
候选 MOQ = 5000
→ 不能作为完全匹配
```

---

## 四、稳定匹配评分与星级

星级必须由本次查询条件稳定计算，不能由 Agent 临场凭感觉决定。

### 1. 只使用本次查询条件

不得把用户没有提到、规则也没有明确推导出的偏好擅自加入评分。

### 2. 条件权重

按 02 中的优先级使用固定权重：

```text
高优先级 = 3
中优先级 = 2
低优先级 = 1
```

### 3. 单项匹配值

对每个可评分条件使用：

```text
完全满足 = 1
部分满足 / 接近 = 0.5
不满足或无数据证明 = 0
```

### 4. 匹配分

```text
Match_Score
=
Σ(条件权重 × 单项匹配值)
÷
Σ(条件权重)
× 100
```

硬条件先过滤，不进入这个分数抵消。

### 5. 星级映射

```text
90–100 = ★★★★★
75–89  = ★★★★☆
60–74  = ★★★☆☆
40–59  = ★★☆☆☆
0–39   = ★☆☆☆☆
```

正常推荐区默认只展示 3～5 星候选。

如果某个候选违反硬条件：

- 不进入正常推荐排名；
- 仅在没有完全匹配、需要展示“接近候选”时出现；
- 星级最高不得超过 2 星；
- 必须明确写出未满足的硬条件。

### 6. 排序与去同质化

先按以下顺序排序：

```text
硬条件满足
>
Match_Score
>
高优先级条件满足数
>
中优先级条件满足数
>
Keyword / Semantic 相似度
```

再做去同质化选择。

去同质化可以决定“展示哪几款代表产品”，但不能把明显低匹配产品包装成高匹配产品，也不能改变其星级。

---

## 五、标准搜索结果

04 返回给 05 的结果至少应包含：

```text
Product_SKU

Factory_Offer:
- Factory_Name
- Material
- Material_Detail
- Price
- MOQ
- Size_System
- Size_Range

Product:
- Main_Image
- Function_Tags
- Scenario_Tags
- Special_Features
- Performance_Attributes

Packaging_Options:
- Packaging_SKU ...

Match_Reasons:
- ...

Unmet_Conditions:
- ...
```

---

## 六、Packaging 边界

当前 04 只返回：

```text
Packaging_Options
```

也就是当前产品允许关联的 Packaging_SKU。

未来 Packaging_KB 启用后，再把：

```text
Product SKU
+
Factory Offer
+
Packaging SKU
```

组合为最终业务方案。

当前不提前生成所有产品 × 工厂 × 包装组合。

---

## 七、无完全匹配时

如果没有完全匹配：

```text
Exact_Match = none
```

仍可返回最接近候选，但必须同时返回：

```text
Unmet_Conditions
```

不能隐瞒冲突。

---

## 八、核心原则

1. 排序不能突破硬条件。
2. 用户明确优先级高于普通软匹配。
3. 返回结果必须保留具体 Factory Offer。
4. Packaging 当前只返回引用，不展开包装本体。
5. Match_Score 与星级必须按固定规则生成，保证相同条件与相同数据下结果尽量一致。
6. 最终结果必须能被 05 稳定读取和继续处理。
