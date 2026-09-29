# 03 Ingestion & Normalization / 表格导入与标准化

本文件定义鞋垫类产品从原始表格和产品图片进入标准 Product_KB 的 V1 流程。

V1 输入范围固定为：

1. 固定格式产品表格
2. 与 SKU 对应的产品清晰图片

不在 V1 中处理 PDF、Word、网页抓取或其他非结构化来源。

---

## 一、原始输入标准

### 1. 产品表格

原始产品表格通常包含以下信息：

- 货号 / SKU
- 尺码
- 主材质
- 详细材质
- 产品特性描述
- MOQ
- Price
- Factory_Name

实际列名可以不同，但必须能稳定映射到 01 Schema 中的标准字段。

### 2. 产品图片

建议图片文件名直接包含 SKU_ID。

单图示例：

```text
F0228.jpg
F1005.jpg
```

如后续需要多图，可使用：

```text
F0228-main.jpg
F0228-01.jpg
F0228-02.jpg
```

V1 默认仍以一张主产品图为主。

---

## 二、一行数据的基本含义

V1 默认：

```text
一行数据 = 一个 SKU + 一个 Factory Offer
```

例如：

```text
F0228 | 富置高 | PU | 6.9 | MOQ 3000
```

代表：

```text
SKU_ID = F0228
Factory_Name = 富置高
Material = PU
Price = 6.9
MOQ = 3000
```

---

## 三、同一 SKU 多工厂合并

如果多行具有相同 SKU_ID，但 Factory_Name 不同，不建立多个 SKU。

例如：

```text
F0228 | 富置高 | PU | 6.9 | MOQ 3000
F0228 | 王氏   | PU | 6.3 | MOQ 5000
```

应合并为：

```text
F0228
├─ Factory Offer 1
│  ├─ Factory_Name: 富置高
│  ├─ Material: PU
│  ├─ Price: 6.9
│  └─ MOQ: 3000
│
└─ Factory Offer 2
   ├─ Factory_Name: 王氏
   ├─ Material: PU
   ├─ Price: 6.3
   └─ MOQ: 5000
```

最终仍只生成一个：

```text
Product_KB/insoles/F0228/product.md
```

---

## 四、标准处理流程

完整流程：

```text
产品表格 + 产品图片
        ↓
识别 SKU_ID
        ↓
识别 Factory Offer
        ↓
提取明确事实字段
        ↓
Material / Size / 标签标准化
        ↓
AI 解析产品特性描述
        ↓
生成 Function / Scenario / Performance 候选
        ↓
按照 02-field-automation-levels 标记
AUTO / RULE / REVIEW / MISSING
        ↓
同 SKU 多工厂合并
        ↓
关联 SKU 图片
        ↓
生成符合 01 product-template.md 的 product.md 候选草稿
        ↓
人工确认 REVIEW
        ↓
交给⑤ Data Validation
        ↓
Validation = PASS
        ↓
写入正式 Product_KB
```

---

## 五、明确事实字段处理

下列字段优先直接从表格提取：

- SKU_ID
- Factory_Name
- MOQ
- Price
- Material_Detail
- Size_Range

只允许做格式清洗，不得改变原始事实。

例如：

```text
MOQ = 3000双
→ MOQ = 3000

价格 = ￥6.9
→ Price = 6.9
```

---

## 六、标准词转换

以下字段必须服从 02 Taxonomy & Rules：

- Material
- Function_Tags
- Scenario_Tags
- Special_Features
- Size_System

例如：

```text
Memory Foam
慢回弹海绵
慢回弹泡棉
→ Material = 记忆棉
```

如果无法可靠映射：

```text
→ REVIEW
```

不得自行创建新的标准词。

---

## 七、产品特性描述解析

产品表格中的“特性”或类似描述，是 AI 语义理解的主要输入。

例如：

```text
透气，缓震但是有韧性，柔软，
没有支撑片，但是足弓有一点点软垫支撑
```

可以生成候选：

```text
Function_Tags:
- 透气排湿
- 缓震
- 回弹
- 足弓支撑

Arch_Support:
- 轻度支撑

Softness:
- 建议偏软
- REVIEW
```

规则：

1. 只能提取原文能够支持的内容。
2. 不得因为某种材质“通常具有某功能”就自动补标签。
3. Function_Tags 和 Scenario_Tags 必须映射到 02-B 已批准标准词。
4. Performance 评分必须遵守 02-field-automation-levels。

---

## 八、Performance 处理

当前以下字段默认不能直接自动入正式库：

- Cushioning
- Elasticity
- Softness

AI 可以根据原文给出建议值或范围，但默认状态为 REVIEW。

例如：

```text
“非常柔软”
→ Softness 建议 4–5
→ REVIEW
```

对于：

- Arch_Support
- Arch_Height
- Heel_Cup_Depth

若原始资料明确，可按规则处理；
若没有足够依据，则标记 REVIEW 或 MISSING。

---

## 九、Special_Features 处理

Special_Features 只有原始资料明确出现时才能写入。

例如：

```text
防穿刺
防静电
ESD
绝缘
```

禁止从普通劳保鞋垫、工作鞋垫或材质本身推断特殊属性。

---

## 十、图片关联规则

优先通过 SKU_ID 自动关联图片。

例如：

```text
F0228.xlsx 中的 SKU = F0228
+
F0228.jpg
↓
Product_KB/insoles/F0228/main.jpg
```

如果图片文件无法可靠匹配 SKU：

```text
→ REVIEW
```

不得把不确定图片自动绑定到正式产品。

---

## 十一、输出结果

③ 模块输出的是“待校验的标准产品候选草稿”，本模块本身不直接绕过⑤写入正式 Product_KB。

最少应包含：

```text
SKU 产品层
├─ Product_Category
├─ SKU_ID
├─ Main_Image
├─ Function_Tags
├─ Scenario_Tags
├─ Special_Features
└─ Performance_Attributes

Factory Offer
├─ Factory_Name
├─ Material
├─ Material_Detail
├─ Price
├─ MOQ
├─ Size_System
└─ Size_Range
```

字段结构服从：

- 01 Schema
- 02 Taxonomy & Rules
- 03② Field Automation Levels

---

## 十二、V1 边界

V1 专门服务于公司目前最常见的数据形态：

```text
固定格式产品表格
+
产品清晰图片
```

暂不扩展：

- PDF 自动解析
- Word 自动解析
- 网页抓取
- 邮件资料自动归档
- 任意非结构化文档识别

后续只有真实业务需要时再扩展。

---

## 十三、与④产品维护的边界

③只负责新 SKU 的首次标准化入库。

处理前必须检查 SKU_ID：

```text
SKU 不存在
→ 按③执行首次入库

SKU 已存在
→ 不在③直接覆盖
→ 转交④ Product Maintenance 做差异比对与确认更新
```

这样可以避免首次导入与增量更新互相覆盖。

---

## 核心原则

```text
先提取事实
→ 再标准化
→ 再做 AI 语义理解
→ 再标记 REVIEW / MISSING
→ 生成候选 product.md
→ 交⑤校验
→ PASS 后写入正式 Product_KB
```

系统目标不是“自动填满所有字段”，而是稳定地把现有产品表格转换为可检索、可维护、可追溯的标准产品知识。
