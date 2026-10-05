# Query Rules / 查询与推荐规则

## 一、条件分类

把用户需求拆成：

```text
Hard_Conditions
Soft_Conditions
Priority
Semantic_Query
```

### Hard Conditions

用户明确不能违反的条件，例如：

- 指定材质
- MOQ / Price 数值上限或下限
- 指定尺码
- 指定特殊属性

### Soft Conditions

用户希望满足但允许权衡的场景、功能、性能或体验要求。

### Priority

用户明确说“最重要、越低越好、越高越好”等时，用 priority 表示；相对方向使用 `goal=min/max`。

## 二、产品专属词表与自然语言映射

Base Skill 不写死任何具体产品的标准场景、功能、性能字段或同义词。

必须读取当前 active Product Profile：

```text
profiles/active-profile.yaml
```

并使用对应产品目录中的：

- `profile.yaml`
- 业务概念映射文档
- 数据处理规则

当前润通鞋垫映射位于：

```text
profiles/runtong/products/insoles/
```

无法可靠标准化的内容保留到 Semantic_Query，不强行贴标签。

## 三、排序原则

固定优先顺序：

```text
硬条件满足
>
用户明确优先级 / 结构化匹配
>
关键词 / 语义相似度辅助排序
```

关键词与向量权重属于 Runtime Tuning；在没有真实业务回归数据时不要随意调整。

## 四、无完全匹配

如果没有满足全部 Hard Conditions 的结果：

```text
Exact_Match = false
```

可以提供接近候选，但必须保留 `Unmet_Conditions`，不得把近似结果说成完全符合。
