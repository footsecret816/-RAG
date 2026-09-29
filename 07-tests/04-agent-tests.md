# 04 Agent Tests / Agent 测试

本文件用于验证 06-agent 是否正确调用系统，并稳定展示结果。

## 重点测试

- 普通产品问题是否默认走查询流程
- 是否正确调用 05 Retrieval Tool
- 是否编造 SKU
- 是否编造 Factory_Name
- 是否编造 Price / MOQ / Material
- 是否脱离 05 结果自行推荐其他产品
- 是否错误修改 04 的排序
- 是否隐藏 Unmet_Conditions
- 是否正确展示 Product SKU + Factory Offer
- 是否正确展示 Packaging_Options

## 查询 / 维护分流测试

普通查询：

```text
“F0228 的价格和 MOQ 是多少？”
```

预期：

```text
→ 查询
→ 不进入 03
```

明确维护：

```text
“把 F0228 富置高的价格改成 7.2”
```

预期：

```text
→ 转 03 Data Management
→ 候选变更
→ 人工确认
→ ⑤校验
→ PASS 后写入
```

仅在聊天中提到某个价格，但没有明确修改意图时，不得触发维护。
