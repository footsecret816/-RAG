# 02 Query Normalization / 查询标准化

本文件定义如何把业务员自然语言转换成 04-search 可执行的标准 Search Request。

05② 执行 02 Taxonomy & Rules 中已经定义好的语言理解与映射规则。

---

## 一、基本流程

```text
用户自然语言
↓
识别产品类别
↓
拆分产品条件 / Factory Offer 条件
↓
识别硬条件 / 软条件
↓
识别用户优先级
↓
映射到标准字段与标准词
↓
保留无法完全结构化的 Semantic_Query
↓
输出 Search Request
```

---

## 二、示例

用户：

```text
“要 PU 的，户外用，MOQ 不能超过 3000，
价格其次，不要太软”
```

标准化：

```text
Product_Category = 鞋垫

Hard_Conditions:
- Material = PU
- MOQ <= 3000

Soft_Conditions:
- Scenario_Tags = 户外徒步
- Softness = 偏向 1-3

Priority:
- MOQ = 高
- Price = 低

Semantic_Query:
- 户外用，不要太软
```

---

## 三、核心规则

1. 标准字段必须服从 01 Schema。
2. 标准词必须服从 02 Taxonomy & Rules。
3. 用户明确说“必须、不能超过”等，优先视为硬条件。
4. “最好、尽量、希望”等优先视为软条件。
5. “越低越好、最重要”等用于 Priority。
6. 不确定表达不得强行映射成不存在的标准值。
7. 无法可靠结构化的内容保留进入 Semantic_Query。
8. 05②只负责生成检索请求，不负责查产品。
