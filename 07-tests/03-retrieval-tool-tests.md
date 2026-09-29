# 03 Retrieval Tool Tests / 检索工具测试

本文件用于验证 05-retrieval-tool 是否能正确把自然语言转换成 Search Request，并正确调用 04。

## 重点测试

- 产品类别识别
- 产品条件与 Factory Offer 条件拆分
- 硬条件 / 软条件识别
- 用户优先级识别
- 标准词映射
- 无法结构化内容是否保留到 Semantic_Query
- 05 是否保持 04 的排序结果
- 05 是否完整保留 Match_Reasons / Unmet_Conditions

## 典型测试

输入：

```text
“要 PU 的，户外用，MOQ 不能超过 3000，
价格其次，不要太软”
```

预期至少识别：

```text
Product_Category = 鞋垫

Hard:
- Material = PU
- MOQ <= 3000

Soft:
- Scenario = 户外徒步
- Softness = 偏向 1-3

Priority:
- MOQ = 高
- Price = 低
```

05 不负责自己重新挑选 SKU。
