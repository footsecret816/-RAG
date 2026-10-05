# 07 Tests / 测试与回归验证

本模块负责验证整套产品知识与智能检索系统是否稳定、准确、可回归。

测试范围不只包含搜索结果，也覆盖：

```text
数据进入
→ 数据维护
→ 搜索
→ Retrieval Tool
→ Agent 最终回答
```

---

## 已确认子板块

### ① Data Pipeline Tests / 数据链路测试 ✅

文件：

`01-data-pipeline-tests.md`

验证 03-data-management。

例如：

- SKU 是否正确提取
- 同 SKU 多工厂是否正确合并
- Material 是否正确标准化
- 空白字段是否错误覆盖旧值
- 新工厂是否正确新增 Factory Offer
- REVIEW 是否被错误自动确认
- 图片是否关联正确 SKU

---

### ② Search Tests / 搜索测试 ✅

文件：

`02-search-tests.md`

验证 04-search。

重点包括：

- MOQ / Price / Material 等硬条件
- Function / Scenario / Performance 条件
- 同 SKU 不同 Factory Offer 是否正确区分
- 软条件排序是否合理
- 无完全匹配时是否正确降级
- Vector / Semantic 相似度不得突破硬条件

---

### ③ Retrieval Tool Tests / 检索工具测试 ✅

文件：

`03-retrieval-tool-tests.md`

验证 05-retrieval-tool。

重点测试：

```text
自然语言
→ Search Request
```

是否正确。

例如：

```text
“MOQ越低越好，贵一点没关系”
```

必须正确识别：

```text
MOQ = 高优先级
Price = 低优先级
```

---

### ④ Agent Tests / Agent 测试 ✅

文件：

`04-agent-tests.md`

验证 06-agent 最终回答。

重点检查：

- 是否编造 SKU
- 是否编造工厂
- 是否编造价格 / MOQ / 材质
- 是否推荐 05 未返回的内部产品
- 是否把不满足的硬条件误写成满足
- 是否正确展示产品图片和匹配理由

---

### ⑤ Regression Suite / 回归测试集 ✅

文件：

`05-regression-suite.md`

建立固定真实业务问题集，例如：

```text
Q001
Q002
Q003
...
```

每次修改以下内容后重新执行：

- Schema
- Taxonomy
- 数据导入规则
- Search
- Ranking
- Embedding / Vector
- Retrieval Tool
- Agent 配置
- 平台适配

目标是判断系统修改后到底变好还是变坏，而不是只凭感觉验收。

---

## 测试原则

测试数据应尽量来自真实业务场景，但真实客户、价格、工厂等敏感数据不进入公开 Git 仓库。

公开仓库可以保存脱敏测试样例和测试规范。

---

## 当前状态

V1 已增加可执行测试层：

```text
07-tests/runtime/test_core.py
07-tests/runtime/test_data_management.py
07-tests/runtime/test_profile_modularization.py
07-tests/runtime/regression_runner.py
```

其中真实业务 20～30 条回归题不进入公开 GitHub，建议存放：

```text
Product_Data/_tests/regression_cases.json
```

GitHub 只保存模板和执行器。

V1 最终验收标准：

1. 基础单元测试全部通过；
2. 真实 Product_KB 建库 / 校验通过；
3. 新增、修改、新工厂、删除等维护流程真实测试通过；
4. 20～30 条固定业务回归题达到既定预期；
5. Profile 模块化测试通过，Core runtime 不再硬编码当前公司 / 产品业务值；
6. 本地受控文件通过 sync/verify_sync.py 一致性校验。