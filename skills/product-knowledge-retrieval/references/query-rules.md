# Query Rules / 查询与推荐规则

## 一、条件分类

统一拆成：

```text
Hard_Conditions
Soft_Conditions
Priority
Semantic_Query
```

Hard Conditions 是不能违反的条件；Soft Conditions 是允许权衡的偏好；Priority 表示用户明确的优先方向；无法可靠结构化的内容保留到 Semantic_Query。

## 二、产品专属映射

Base Skill 不写死具体产品的功能、场景、材质、性能字段或自然语言映射。

每次查询先读取：

```text
profiles/active-profile.yaml
→ 当前 Product Profile
```

产品专属标准词、性能字段、展示字段和自然语言映射，以当前 Product Profile 为准。

## 三、排序原则

固定保持：

```text
硬条件满足
>
结构化匹配 / 用户明确优先级
>
关键词 / 向量辅助排序
```

Hybrid 权重属于后期 Runtime Tuning，不在 Profile 模块化阶段调整。

## 四、无完全匹配

没有满足全部 Hard Conditions 时：

```text
Exact_Match = false
```

可以返回最接近候选，但必须明确 Unmet_Conditions。
