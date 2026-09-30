# 04 Category Display Fields / 品类展示字段

本文件定义不同 Product_Category 在业务推荐表中应优先展示哪些“关键规格”。

统一框架：

```text
图片｜SKU｜关键规格｜MOQ｜价格｜⭐本次匹配度｜本次推荐理由
```

不同品类只替换“关键规格”。

---

## 鞋垫 / Insoles

优先从以下字段中选择最相关的 2～4 项：

- Material
- Cushioning
- Elasticity
- Softness
- Arch_Support
- Arch_Height
- Heel_Cup_Depth
- Size_Range
- Special_Features

示例：

```text
PU / 回弹4 / 缓震3 / 轻支撑
```

---

## 鞋刷 / Shoe Brush

未来 Schema 建立后优先：

- Brush_Material / 刷毛材质
- Handle_Material / 手柄材质
- Size
- Intended_Use / 适用清洁对象

示例：

```text
猪鬃 / 木柄 / 17cm / 光面皮
```

---

## 鞋油 / 清洁剂 / Shoe Care Liquid

未来 Schema 建立后优先：

- Volume
- Applicable_Material
- Core_Function
- Formula_Type

示例：

```text
180ml / 皮革 / 清洁+护理
```

---

## 足部护理 / Foot Care

未来 Schema 建立后优先：

- Material
- Size
- Applicable_Area
- Core_Function

示例：

```text
SEBS / 均码 / 前掌 / 减压
```

---

## 运动护具 / Sports Support

未来 Schema 建立后优先：

- Material
- Size
- Support_Level
- Applicable_Sport

示例：

```text
弹力织物 / M-L / 中等支撑 / 健身
```

---

## 其他产品类别

如果尚未建立专属展示字段：

1. 优先显示最能区分产品的真实规格；
2. 总数控制在 2～4 个；
3. 不要把所有字段塞进表格；
4. 后续为该 Product_Category 建立专属字段模板。

---

## 核心原则

> 统一的是“怎么展示”，不是“所有品类显示同样的字段”。

每个产品类别都应让业务员一眼看到最有决策价值的规格。
