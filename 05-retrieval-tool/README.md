# 05 Retrieval Tool / 产品检索工具

本模块负责把业务员自然语言转换成标准检索请求，并调用 04 的可执行混合检索引擎。

它是上层 Agent 与底层搜索之间的统一接口。

本模块保持平台无关。

---

## 当前 V1 实际链路

```text
业务员自然语言
↓
05 查询标准化
↓
Search_Request JSON
↓
04-search/runtime/search.py
↓
结构化条件 + 关键词 + 向量混合检索
↓
Search_Result JSON
↓
06 Agent 展示
```

04 已有真正可运行的 Python 检索代码。

05 的职责不是重新搜索产品，而是把自然语言稳定转换为统一 Search_Request，并把 Search_Result 交给 06。

---

## ① Tool Contract / 工具接口

文件：

`01-tool-contract.md`

输入可以包括：

- 自然语言产品需求
- 已结构化检索条件
- 必要业务上下文

输出至少包含：

- SKU_ID
- Factory_Name
- Main_Image
- Material
- Price
- MOQ
- Size
- 本次匹配度
- 匹配原因
- 未满足条件

最终结果粒度：

```text
SKU + Factory Offer
```

---

## ② Query Normalization / 查询标准化

文件：

`02-query-normalization.md`

负责根据 02 Taxonomy & Rules，把业务员自然语言转换成标准 Search_Request。

例如：

```text
“记忆棉、跑步用、不要太软，
MOQ越低越好，贵一点没关系”
```

转换为：

```json
{
  "product_category": "鞋垫",
  "hard_conditions": [
    {"field":"Material","op":"eq","value":"记忆棉"}
  ],
  "soft_conditions": [
    {"field":"Scenario_Tags","op":"contains","value":"跑步"},
    {"field":"Softness","op":"range","value":[1,3]}
  ],
  "priority": [
    {"field":"MOQ","level":"high"},
    {"field":"Price","level":"low"}
  ],
  "semantic_query": ""
}
```

02 负责规则。

05 负责执行标准化。

---

## ③ Retrieval Orchestration / 检索调度

标准化完成后，调用：

```bash
python 04-search/runtime/search.py --request-json "<Search_Request JSON>"
```

核心原则：

- 05 不绕过 04 自己重新选择产品；
- 05 不修改 Product_KB；
- 05 不自行创造 SKU、工厂、价格或属性；
- 05 不自行修改 04 返回的 Match_Score / 星级；
- 没有完全匹配时，保留 04 返回的 unmet_conditions。

---

## ④ Interface Schema / 统一机器接口

文件：

`04-interface-schema.md`

统一：

- Search_Request
- Search_Result
- Change_Set

不同平台只需要适配到该内部接口。

---

## 与 04 的边界

```text
05
= 理解用户需求并标准化

04
= 真正执行产品检索、筛选、向量召回、排序
```

05 不再直接读取全部 Product_KB 做临场人工式判断。

---

## 与 06 的边界

```text
04 / 05 返回机器结果
↓
06 负责展示
```

06 可以：

- 选择表格字段；
- 直接显示图片；
- 把匹配原因压缩成业务员易读文字。

06 不可以：

- 改 SKU；
- 改价格 / MOQ；
- 改工厂；
- 改匹配星级；
- 把未满足条件说成已经满足。

---

## 当前状态

当前 V1：

```text
查询标准化规则：已定义
统一接口：已定义
04 可执行混合检索：已代码化
05 → 04 调用方式：已确定
```

下一步主要工作是实际 Product_KB 建库、测试和回归调优。
