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

明确必须满足的条件，例如：

- Material = PU
- MOQ <= 3000
- Price <= 某值
- 指定尺码
- 指定特殊功能

### Soft Conditions

偏好、倾向或体验要求，例如：

- 户外使用
- 缓震更强
- 不要太软
- 支撑强一点

### Priority

用户明确说：

- 必须
- 最重要
- 越低越好

通常优先级高。

用户说：

- 最好
- 希望
- 尽量

通常作为软偏好。

例如：

```text
“价格贵一点没事”
→ Price 优先级低
```

## 二、鞋垫标准场景

当前主要 Scenario_Tags：

- 日常
- 长距离行走
- 长时间站立 / 工作
- 劳保 / 安全鞋
- 跑步
- 篮球
- 足球
- 健身 / 训练
- 综合运动
- 户外徒步
- 登山 / 越野
- 休闲 / 皮鞋
- 紧脚鞋

## 三、标准功能

当前主要 Function_Tags：

- 足弓支撑
- 缓震
- 回弹
- 抗疲劳减压
- 防滑
- 透气排湿
- 防臭

## 四、常见自然语言映射

```text
“不要太软”
→ Softness 偏向 1-3

“支撑强一点”
→ Arch_Support 偏向 强支撑

“有弹性 / 回弹好”
→ Elasticity 偏高

“户外走路”
→ Scenario_Tags 优先考虑 户外徒步 / 长距离行走
```

无法可靠标准化的内容保留原始语义，不要强行贴标签。

## 五、排序原则

固定优先顺序：

```text
硬条件满足
>
用户明确优先级
>
软条件匹配
>
关键词 / 语义相似度
```

## 六、无完全匹配

如果没有满足全部 Hard Conditions 的结果：

```text
Exact_Match = false
```

然后给最接近候选，并明确：

```text
Unmet_Conditions
```

不得把近似结果说成完全符合。
