# 02 Search Tests / 搜索测试

本文件用于验证 04-search 的检索、过滤和排序是否正确。

## 重点测试

- Product SKU + Factory Offer 是否作为独立搜索粒度
- 同一 SKU 不同工厂是否正确区分
- Material / MOQ / Price / Size 等硬条件是否正确过滤
- Function / Scenario / Performance 是否正确匹配
- 用户优先级是否正确影响排序
- Keyword 是否不会突破硬条件
- 未来 Vector / Semantic Search 是否不会突破硬条件
- 无完全匹配时是否正确返回最接近候选
- Packaging_Options 是否只作为 Packaging_SKU 引用返回

## 必测规则

```text
硬条件
>
用户明确优先级
>
软条件匹配
>
Keyword / Semantic 相似度
```

## 典型测试

用户要求：

```text
Material = PU
MOQ <= 3000
Scenario = 户外徒步
```

MOQ 5000 的 Factory Offer 不得作为完全匹配结果。
