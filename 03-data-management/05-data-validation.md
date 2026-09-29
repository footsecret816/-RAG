# 05 Data Validation / 数据校验

本文件定义数据在正式写入 Product_KB 前的最后校验规则。

⑤只负责“验收结果”，不重新解析原始表格、不重新判断标签、不主动修改数据。

核心问题：

> 这份由③或④处理后的数据，现在是否可以安全写入 Product_KB？

---

## 一、职责边界

⑤负责检查，不负责修改。

不得在⑤中执行：

- 重新解析 Excel
- 重新生成 Function_Tags
- 重新判断 Scenario_Tags
- 重新映射 Material
- 自动修改 Price / MOQ
- 自动新增 Factory Offer
- 自动替换图片
- 自动确认 REVIEW 字段

如发现问题：

```text
→ 返回问题
→ 标记阻塞原因
→ 交回③或④处理
```

---

## 二、结构检查

检查③或④生成的候选数据在写入后是否会符合 01 Schema 与 `01-schema/product-template.md`。

至少包括：

- Product_Category 是否存在
- 候选 product.md 是否符合标准模板结构
- SKU_ID 是否存在
- SKU 文件夹是否与 SKU_ID 一致
- product.md 是否存在
- Factory Offer 是否挂在正确 SKU 下
- 一个 SKU 是否被错误拆成多个 SKU 文件夹

---

## 三、标准值检查

检查标准字段是否符合 02 Taxonomy & Rules。

至少包括：

- Material 是否属于标准材质词
- Material_Detail 如有内容，是否保持为来源可支持的事实性描述
- Function_Tags 是否全部为批准标签
- Scenario_Tags 是否全部为批准标签
- Special_Features 是否全部为批准值
- Size_System 是否为允许格式
- Cushioning 是否在 1–5
- Elasticity 是否在 1–5
- Softness 是否在 1–5
- Arch_Height 是否为 低 / 中 / 高
- Arch_Support 是否为 无支撑 / 轻度支撑 / 强支撑
- Heel_Cup_Depth 是否为 平 / 浅 / 中 / 深

不得让临时词、近义词或未批准值直接进入正式 Product_KB。

---

## 四、状态检查

检查②定义的自动化状态是否已经处理完成。

### AUTO / RULE

规则通过后可以入库。

### REVIEW

如仍处于 REVIEW：

```text
→ 不作为正式值直接入库
→ 要求人工确认
```

### MISSING

MISSING 不等于错误。

如果该字段不是当前必填字段：

```text
→ 可以保留缺失状态
```

如果未来某字段被定义为必填：

```text
→ MISSING 阻止入库
```

---

## 五、重复与关系检查

重点检查：

- 是否重复建立相同 SKU
- 同一 SKU 下是否重复建立相同 Factory_Name
- 同一 Factory Offer 是否出现冲突性重复记录
- 新 Factory_Name 是否被错误当成新 SKU
- 图片是否绑定到正确 SKU

判断基准：

```text
SKU_ID
+
Factory_Name
```

用于识别具体 Factory Offer。

---

## 六、空白覆盖保护检查

⑤必须再次确认④的核心安全规则没有被破坏：

```text
新值为空
≠ 删除旧值
≠ 清空旧值
```

检查：

- 旧 MOQ 是否因新表格空白被错误清空
- 旧 Price 是否因新表格空白被错误清空
- 旧 Material 是否因新表格空白被错误清空
- 旧 Factory Offer 是否因新表格未出现而被错误删除
- 旧图片是否因本次未上传图片而被错误删除

---

## 七、图片检查

检查：

- Main_Image 是否能明确对应 SKU_ID
- 图片文件是否存在
- 图片是否被错误关联到其他 SKU
- 新图片替换是否已经经过④的确认流程

无法可靠确认图片归属时：

```text
→ 阻止自动绑定
→ 返回 REVIEW
```

---

## 八、校验结果

⑤最终只输出两类结果：

### PASS

```text
Validation = PASS
→ 可以写入 Product_KB
```

### FAIL / REVIEW REQUIRED

```text
Validation = FAIL

问题：
- Material 非标准词
- Softness 仍为 REVIEW
- SKU + Factory_Name 重复
...
```

不通过时不得直接写入正式 Product_KB。

---

## 九、与其他子模块关系

```text
③ 首次导入
或
④ 增量更新
        ↓
⑤ Data Validation
        ↓
PASS
        ↓
正式写入 Product_KB
        ↓
⑥ Data Change Handoff
```

⑤只做校验，不承担③④的数据处理职责，也不承担⑥或04-search的索引职责。
