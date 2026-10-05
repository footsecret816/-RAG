# Business Concept Mapping / 业务概念映射

本文件负责把业务员的自然语言、市场术语、客户需求和业务表达，映射到标准字段。

## 基本原则

- 业务员不需要记住标准标签。
- 标准标签用于系统内部保持一致。
- 自然语言可以映射到材质、功能、场景、性能或工厂供应条件。
- 不确定的表达不要强行等于单一标签，应保留为组合需求或进入语义检索。

## 示例

### “记忆棉鞋垫”

映射：

`Material = 记忆棉`

### “plantar fasciitis 的鞋垫”

不要简单等于某一个单一标签。

优先关联：
- Function_Tags：足弓支撑、抗疲劳减压
- Arch_Support：轻度或强支撑候选
- Heel_Cup_Depth：中 / 深优先
- Cushioning：不宜过低

最终由检索排序决定具体 SKU。

### “跑步用，不要太软，要有回弹”

映射：
- Scenario_Tags = 跑步
- Softness = 偏向 1–3
- Elasticity = 偏高
- Cushioning = 适中倾向

### “工作鞋垫 / 劳保鞋垫 / 站一天”

映射：
- Scenario_Tags = 长时间站立 / 工作 或 劳保 / 安全鞋
- Function_Tags 可优先关注：抗疲劳减压、缓震

如用户明确要求防穿刺、防静电、ESD，则进一步匹配 Special_Features。

### “亚马逊测品，MOQ越低越好，贵一点没事”

这不是产品标签。

映射到工厂供应层：
- MOQ = 高优先级
- Price = 低优先级

### “不要太软”

映射：
- Softness 偏向 1–3

### “支撑强一点”

映射：
- Function_Tags = 足弓支撑
- Arch_Support = 强支撑倾向

后续根据真实业务问法持续扩充。

> 当前润通鞋垫业务映射属于 Product Profile 内容；未来换公司/产品时替换该模块，不修改 Core。
