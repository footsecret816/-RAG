# 04 Product Maintenance / 增量更新与覆盖

本文件定义产品已经进入 Product_KB 后，如何使用同一套固定格式产品表格和 SKU 图片进行后续更新。

④不重新建立一套维护入口。

V1 继续使用：

1. 固定格式产品表格
2. 以 SKU_ID 命名或可稳定关联的产品图片

核心目标：

> 新资料与旧知识库自动比对，只处理真正发生变化的内容；任何覆盖动作在写入前必须由操作者确认。

---

## 一、适用范围

④只处理 Product_KB 中已经存在的 SKU。

如果 SKU_ID 不存在：

```text
→ 不走④
→ 转交③ Ingestion & Normalization 做首次入库
```

如果 SKU_ID 已存在：

```text
→ 读取现有 product.md
→ 与新表格 / 新图片做差异比对
→ 按本文件规则处理
```

---

## 二、核心更新原则

最高优先级规则：

```text
有新值才比较；
有冲突才更新；
新值为空则保留旧值；
覆盖前必须确认。
```

也就是说：

### 1. 新值有内容，且与旧值相同

```text
→ 无变化
→ 不处理
```

### 2. 新值有内容，且与旧值不同

```text
→ 检测为变更
→ 展示旧值 → 新值
→ 等待操作者确认
→ 确认后覆盖
```

### 3. 新值为空

```text
→ 保留旧值
→ 不覆盖
→ 不删除
```

空白绝不等于删除。

---

## 三、同 SKU + 同 Factory_Name

如果新表格中的：

```text
SKU_ID 相同
+
Factory_Name 相同
```

则视为对现有 Factory Offer 的更新。

例如旧数据：

```text
SKU_ID: F0228
Factory_Name: 富置高
Material: PU
Price: 6.9
MOQ: 3000
```

新表格：

```text
SKU_ID: F0228
Factory_Name: 富置高
Material: PU
Price: 7.2
MOQ: 3000
```

系统应输出差异：

```text
F0228 / 富置高

Price:
6.9 → 7.2

其余字段：
无变化
```

操作者确认后，只覆盖 Price。

不得重建 SKU，也不得重建整个 Factory Offer。

---

## 四、空白字段保护

例如旧数据：

```text
MOQ = 3000
Price = 6.9
Material = PU
```

新表格：

```text
MOQ = 空白
Price = 7.2
Material = PU
```

正确处理：

```text
MOQ:
新值为空
→ 保留旧值 3000

Price:
6.9 → 7.2
→ 待确认覆盖

Material:
PU → PU
→ 无变化
```

最终确认后：

```text
MOQ = 3000
Price = 7.2
Material = PU
```

禁止：

```text
新表格空白
→ 自动清空旧值
```

---

## 五、同 SKU + 新 Factory_Name

如果 SKU 已存在，但新表格出现该 SKU 以前没有的 Factory_Name：

```text
→ 识别为新增 Factory Offer
```

例如原来：

```text
F0228
└─ 富置高
```

新表格出现：

```text
F0228 | 王氏 | PU | 6.3 | MOQ 5000
```

系统应提示：

```text
检测到新增 Factory Offer：

SKU_ID: F0228
Factory_Name: 王氏
Material: PU
Price: 6.3
MOQ: 5000
```

操作者确认后，新增到原来的 F0228 下：

```text
F0228
├─ 富置高
└─ 王氏
```

不得新建第二个 F0228 SKU。

---

## 六、新表格未出现旧工厂，不代表删除

例如 Product_KB 中已有：

```text
F0228
├─ 富置高
└─ 王氏
```

本次新表格只包含：

```text
F0228 | 富置高 | ...
```

正确处理：

```text
王氏未出现在本次表格
→ 保留王氏原有 Factory Offer
```

禁止自动理解为：

```text
“新表格没写王氏”
→ 删除王氏
```

删除 Factory Offer 必须是明确操作。

---

## 七、产品层字段更新

对于同一个 SKU 的产品层字段，例如：

- Function_Tags
- Scenario_Tags
- Special_Features
- Performance_Attributes

同样使用“新值非空才比较”的规则。

例如：

```text
旧值：
Scenario_Tags = 日常

新值：
Scenario_Tags = 日常 + 长距离行走
```

系统应展示：

```text
Scenario_Tags:
日常
→
日常 + 长距离行走
```

操作者确认后更新。

如果新表格该字段为空：

```text
→ 保留旧值
```

---

## 八、REVIEW 字段更新

如果新资料对 REVIEW 字段提供了更明确的信息，例如：

```text
旧值：
Softness = REVIEW

新资料明确描述：
非常柔软
```

系统仍应按照 ② Field Automation Levels 处理：

```text
→ 生成新的建议值
→ 继续标记 REVIEW
→ 人工确认后写入正式值
```

④不能绕过②的自动化等级规则。

---

## 九、产品图片更新

产品图片继续通过 SKU_ID 关联。

例如现有：

```text
Product_KB/insoles/F0228/main.jpg
```

新上传：

```text
F0228.jpg
```

系统检测到 F0228 已存在时：

```text
→ 识别为候选替换图片
→ 提示操作者确认
→ 确认后覆盖 main.jpg
```

如果无法可靠确认图片属于该 SKU：

```text
→ REVIEW
→ 不自动覆盖
```

---

## 十、明确删除必须独立操作

V1 中，删除不能通过“留空”表达。

以下情况都不得自动删除：

- 新表格某字段为空
- 新表格没有出现某个旧 Factory Offer
- 新表格没有附带旧图片

如确实需要删除：

```text
→ 必须由操作者明确发起删除动作
→ 展示将删除的对象
→ 人工确认
→ 再执行删除
```

删除与普通更新必须严格区分。

---

## 十一、更新前差异预览

任何会改变 Product_KB 的操作，都必须先输出差异预览。

建议格式：

```text
SKU: F0228

变更 1
Factory: 富置高
Price: 6.9 → 7.2

变更 2
Factory: 富置高
MOQ: 3000 → 2500

新增
Factory: 王氏

图片
F0228/main.jpg → 检测到新图片，待确认替换
```

操作者确认后再写入。

---

## 十二、无变化时不写入

如果新表格和现有 Product_KB 完全一致：

```text
→ 返回“未检测到变化”
→ 不修改 product.md
→ 不触发无意义的后续索引更新
```

---

## 十三、处理流程

```text
固定格式新表格 / 新图片
        ↓
识别 SKU_ID
        ↓
SKU 是否已存在？
   ├─ 否 → 转③首次入库
   └─ 是
        ↓
读取现有 product.md
        ↓
按 SKU + Factory_Name 比对
        ↓
空白字段保护
        ↓
识别：
- 无变化
- 字段变更
- 新 Factory Offer
- 新图片
        ↓
生成差异预览
        ↓
操作者确认
        ↓
写入 Product_KB
        ↓
交给⑥判断需要更新哪些检索索引
```

---

## 十四、核心原则

```text
同 SKU + 同工厂
→ 差异更新

同 SKU + 新工厂
→ 新增 Factory Offer

同 SKU + 新图片
→ 确认后替换

新值为空
→ 保留旧值

未明确删除
→ 永不自动删除

所有实际覆盖
→ 先比对、再确认、后写入
```

④的目标不是复杂的版本管理系统，而是让固定格式产品表格可以长期、低风险地维护现有 Product_KB。
