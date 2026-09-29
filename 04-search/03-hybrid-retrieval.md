# 03 Hybrid Retrieval / 混合检索

本文件定义 04 如何根据 Search Request 真正检索产品。

## 一、当前 V1 检索组成

```text
Metadata Filter
+
Keyword Search
```

未来可增加：

```text
Vector Semantic Search
```

但 Vector 不作为 V1 必要依赖。

---

## 二、检索顺序

建议流程：

```text
Search Request
↓
硬条件过滤
↓
Metadata 匹配
↓
Keyword 匹配
↓
Vector Semantic Search（后续）
↓
合并候选
```

---

## 三、Metadata 适用字段

适合精确筛选或数值过滤，例如：

- Product_Category
- SKU_ID
- Factory_Name
- Material
- Price
- MOQ
- Size_System
- Size_Range
- Function_Tags
- Scenario_Tags
- Special_Features
- Performance_Attributes

例如：

```text
Material = PU
MOQ <= 3000
Softness = 2-3
Scenario = 户外徒步
```

---

## 四、Keyword 适用内容

主要用于：

- Function_Tags
- Scenario_Tags
- Material_Detail
- 其他已标准化可检索文本

Keyword 不得覆盖硬条件筛选结果。

---

## 五、Vector / Semantic Search

未来主要用于：

- 模糊自然语言
- 相似产品
- 难以完全结构化的业务表达

例如：

```text
“走很久不累，但不要太软”
“有没有和这个产品定位差不多的？”
```

核心规则：

> Vector 相似度不能突破任何硬条件。

---

## 六、无完全匹配

如果没有任何记录满足全部硬条件：

```text
Exact_Match = none
```

系统不得把违反硬条件的结果伪装成完全匹配。

可以继续寻找最接近候选，但必须明确标出未满足条件。

---

## 七、核心原则

1. 硬条件先过滤。
2. Metadata 优先保证事实准确。
3. Keyword 用于补充文本匹配。
4. Vector 只做增强。
5. 所有候选仍以 Product SKU + Factory Offer 为粒度。
