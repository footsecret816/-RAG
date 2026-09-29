# 03 Retrieval Orchestration / 检索调度

本文件定义 05 如何调用 04-search，并把搜索结果整理成统一输出。

---

## 一、基本流程

```text
自然语言需求
↓
05② Query Normalization
↓
Search Request
↓
调用 04-search
↓
读取搜索结果
↓
标准化返回给 06 Agent
```

---

## 二、有完全匹配

如果 04 返回完全匹配：

```text
Exact_Match = true
```

05 按 04 的排序顺序返回结果，不重新改排序。

---

## 三、无完全匹配

如果：

```text
Exact_Match = none
```

05 可以继续接收 04 返回的最接近候选，但必须同时保留：

```text
Unmet_Conditions
```

不得把未满足硬条件的候选包装成完全匹配。

---

## 四、返回格式

建议统一输出：

```text
Result

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

Exact_Match:
- true / false
```

---

## 五、核心边界

05：

- 负责调用和组织结果
- 不自行增加候选
- 不重新判断哪个 SKU 更优
- 不修改 04 的硬条件结论
- 不隐藏未满足条件
- 不产生公司内部不存在的产品事实

06 Agent 只需要读取 05 的标准结果并组织最终回答。
