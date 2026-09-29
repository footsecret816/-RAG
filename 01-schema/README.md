# 01 Schema

本模块定义产品知识库的数据结构标准。

当前先固化 **鞋垫类产品 Schema V1**。未来新增鞋护理、足部护理、运动护具等其他品类时，在保留通用字段的基础上，分别增加对应品类的专属性能指标。

---

## 一、产品层

### 1. Product_Category / 产品分类

当前鞋垫产品固定为：

```text
Product_Category = 鞋垫
```

该字段用于未来区分不同产品大类。

---

### 2. SKU_ID / 产品编号

- 每款产品的唯一识别字段。
- 不使用固定产品名称作为唯一识别，因为同一款鞋垫可能根据市场、客户或使用场景使用不同名称。
- SKU_ID 应保持稳定，不因产品描述变化而变化。

---

### 3. Main_Image / 产品多角度组合图

- 每个 SKU 对应一张产品多角度组合图。
- 图片属于真实产品资料，不进入 Git 仓库。
- Schema 中只定义图片字段与引用规则。

---

### 4. Function_Tags / 功能标签

用于描述产品具有什么功能。鞋垫类当前标准功能标签为：

- 足弓支撑
- 缓震
- 回弹
- 抗疲劳减压
- 防滑
- 透气排湿
- 防臭

说明：

- 功能标签必须使用标准词表。
- 业务员查询时不要求使用标准词。
- 系统需要通过近义词、口语表达和语义理解，将自然语言映射到标准标签。

---

### 5. Scenario_Tags / 使用场景标签

用于描述产品适合的使用场景。

鞋垫类当前标准场景标签为：

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

当前不单独拆分“适用鞋型”，因为鞋型与使用场景高度重合，统一放入 Scenario_Tags 管理。

---

### 6. Packaging_Options / 包装方案引用（预留，可选）

包装暂不纳入当前 V1 的实际数据维护，但在产品 Schema 中预留引用窗口。

未来包装采用独立知识库管理，每个包装方案拥有独立唯一编号：

```text
Packaging_SKU
```

产品只保存可关联的包装编号，例如：

```text
Packaging_Options:
- PKG-IN-001
- PKG-IN-005
```

说明：

- Packaging_Options 当前允许为空。
- 包装本体资料不直接写入 product.md。
- 包装未来由独立 `Packaging_KB` 管理。
- Packaging_KB 内部再按产品类别区分，例如鞋垫包装、鞋护理包装等。
- 当前阶段只预留 Packaging_SKU 引用关系，不提前定义包装材质、尺寸、印刷、价格等内部 Schema。
- 包装不放入 Factory Offer 普通字段中，避免把独立包装知识塞进产品供应信息。

---

### 7. Special_Features / 特殊属性（可选）

用于记录普通功能标签之外的特殊技术或劳保属性。

例如：

- 防穿刺
- 防静电
- ESD
- 绝缘

说明：

- 该字段为可选字段。
- 普通鞋垫没有特殊属性时可留空。
- 后续如出现新的特殊技术属性，可在标准词表中继续补充。
- Special_Features 不与 Function_Tags 混用。

---

## 二、Performance_Attributes / 鞋垫性能维度

鞋垫类产品使用以下固定性能维度。

### 1. Cushioning / 缓震性

评分范围：1–5

```text
1 = 缓震最弱 / 最不缓震
2 = 缓震较弱
3 = 中等缓震
4 = 缓震较强
5 = 缓震最强 / 最明显
```

规则：

- 数值越大，缓震越强。
- 1 和 5 的方向必须固定，防止 AI 反向理解。

---

### 2. Elasticity / 回弹性

评分范围：1–5

```text
1 = 回弹最弱 / 最不弹
2 = 回弹较弱
3 = 中等回弹
4 = 回弹较强
5 = 回弹最强 / 最弹
```

规则：

- 数值越大，回弹越强。

---

### 3. Softness / 软硬度

评分范围：1–5

```text
1 = 最硬
2 = 偏硬
3 = 软硬适中
4 = 偏软
5 = 最软
```

规则：

- 数值越大，产品越软。
- 该方向必须固定，防止与“硬度”概念混淆。

---

### 4. Arch_Height / 足弓高度

固定三档：

```text
低
中
高
```

说明：

- 足弓高度与足弓支撑强度是两个不同维度。
- 高足弓不等于强支撑。

---

### 5. Arch_Support / 足弓支撑强度

固定三档：

```text
无支撑
轻度支撑
强支撑
```

说明：

- 描述足弓区域实际支撑力度。
- 与足弓高度分开记录。

---

### 6. Heel_Cup_Depth / 后跟杯深度

固定四档：

```text
平
浅
中
深
```

说明：

- 使用“后跟杯深度”而不是主观的“包裹性”作为结构指标。
- 深度越大，通常后跟包围结构越明显，但实际包裹体验仍可能受鞋垫轮廓等因素影响。

---

## 三、工厂供应层

同一款 SKU 可以对应多个工厂。

每个工厂分别维护自己的供应条件。

### Factory Offer 字段

```text
Factory_Name / 工厂名称
├─ Material / 主材质
├─ Material_Detail / 详细材质
├─ Price / 价格
├─ MOQ / 起订量
├─ Size_System / 尺码体系
└─ Size_Range / 尺码范围
```

### Factory_Name / 工厂名称

- 直接使用公司内部熟悉的工厂名称作为唯一识别。
- 当前不额外增加 Factory_ID。

### Material / 材质

- 记录该工厂生产这款 SKU 时实际使用的材质方案。
- Material 是鞋垫检索中的一级重要字段，业务员可以直接按材质查询产品。
- 例如：记忆棉、PU、EVA、Gel、PORON、乳胶等。
- 材质的标准词、英文名、行业叫法和近义词映射由 `02-taxonomy-rules/B-business-knowledge/insoles/` 管理。
- Material 仍属于具体工厂供应方案，不提升到 SKU 产品层，因为同一 SKU 不同工厂可能使用不同材质。

### Material_Detail / 详细材质

- 保留原始资料中能够明确确认的详细材质、层次或组合信息。
- 例如面布、泡棉、Gel、支撑片等实际组成说明。
- Material_Detail 允许使用事实性自然语言，不要求压缩成单一标准词。
- Material 与 Material_Detail 分工：
  - `Material` 用于标准化检索；
  - `Material_Detail` 用于保留真实产品细节。
- 同一 SKU 不同工厂如实际用料不同，应分别记录在各自 Factory Offer 下。

### Price / 价格

- 默认币种：人民币。
- 一般一个工厂对应一个当前有效价格。
- 价格必须与具体工厂绑定，不作为 SKU 的统一价格。

### MOQ / 起订量

- 记录该工厂针对该 SKU 的实际起订量。
- MOQ 属于工厂供应条件，不属于产品本体。

### Size_System / 尺码体系

用于记录该工厂可提供的尺码体系，例如：

- EU
- US
- UK
- 其他实际使用体系

### Size_Range / 尺码范围

记录该工厂针对该 SKU 可生产的实际尺码范围。

---

## 四、核心数据关系

知识库采用两层结构：

```text
SKU 产品层
├─ Product_Category
├─ SKU_ID
├─ Main_Image
├─ Function_Tags
├─ Scenario_Tags
├─ Packaging_Options（预留，可为空）
├─ Special_Features
└─ Performance_Attributes
      ↓
      一款 SKU 可以对应多个工厂供应方案
      ↓
Factory Offer 工厂供应层
├─ Factory_Name
├─ Material
├─ Material_Detail
├─ Price
├─ MOQ
├─ Size_System
└─ Size_Range
```

最终业务检索结果的粒度不是单纯 SKU，而是：

```text
SKU + Factory_Name
```

例如同一款产品：

```text
SKU-001
├─ A工厂：MOQ 800，价格较高
└─ B工厂：MOQ 5000，价格较低
```

当业务员提出“客户首单量小，MOQ 越低越好，价格贵一点没关系”时，系统应返回：

```text
SKU-001 + A工厂
```

而不是只返回 SKU-001。

---

## 五、自然语言与标准标签的关系

标准标签主要服务于系统内部的数据一致性。

业务员不需要按照标准词表提问。

例如：

```text
“不要太软”
→ Softness 偏向 1–3

“支撑强一点”
→ Arch_Support = 强支撑

“跑步用，要有回弹，但不能像踩沙滩一样软”
→ Elasticity 较高
→ Softness 中等或偏硬
→ Cushioning 适中
```

自然语言映射、近义词、口语表达与业务规则将在 `02-taxonomy-rules/` 中单独定义。

---

## 六、标准 product.md 模板

正式 SKU 文件应遵守：

`01-schema/product-template.md`

该模板是 Product_KB 中单个 SKU 的标准输出结构，供 03-data-management 生成和维护 product.md 时使用。

---

## 七、数据边界

本 Schema 只定义数据结构，不存放真实产品信息。

以下真实业务数据不进入 Git：

- 实际 SKU 数据
- 产品图片
- 实际包装方案数据与包装图片
- 工厂真实供应数据
- 真实价格
- MOQ
- 具体材质组合
- 实际尺码范围

真实产品数据由独立的 Product_KB 存储。

未来包装数据由独立的 Packaging_KB 存储，并通过 Packaging_SKU 与产品建立引用关系。当前 V1 仅保留该扩展窗口，不启用包装数据维护流程。

---

## 当前版本

**鞋垫类产品 Schema V1**

当前已确认：

- 产品分类字段
- SKU 唯一识别
- 产品图片字段
- 功能标签
- 使用场景标签
- Packaging_Options 包装方案引用窗口（可选，V1 暂不启用）
- Special_Features 特殊属性（可选）
- 6 项鞋垫专属性能维度
- SKU 与多个工厂供应方案的一对多关系
- 工厂层价格、MOQ、Material、Material_Detail、尺码独立维护
- Material 材质作为一级重要检索字段，但仍绑定具体 Factory Offer
- 最终检索粒度为 SKU + Factory Offer
