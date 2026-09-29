# 03 Response Format / 回答格式

本文件定义 Agent 如何把 05 返回的结果展示给业务员。

## 一、产品推荐结果

建议至少展示：

```text
SKU
产品图片
Factory_Name
Material
Size
MOQ
Price
匹配原因
```

有 Packaging_Options 时可一并展示 Packaging_SKU 引用。

---

## 二、示例

```text
推荐 1

SKU：F0228
工厂：富置高
材质：PU
MOQ：3000
价格：6.9
尺码：EU 36-46

匹配原因：
- 户外徒步
- 缓震
- MOQ 符合要求

Packaging_Options：
- PKG-IN-005
```

---

## 三、非完全匹配

如果 05 返回：

```text
Exact_Match = false
```

Agent 必须明确展示未满足条件。

例如：

```text
未完全满足：
用户要求 MOQ <= 1000
当前最接近候选 MOQ = 1500
```

不得隐藏冲突。

---

## 四、回答原则

1. 事实字段以 05 返回结果为准。
2. 不自行更改 SKU、Factory、Price、MOQ。
3. 不重新排序内部候选。
4. 根据用户问题适当精简展示字段。
5. 产品查询回答尽量直接，不重复解释系统内部流程。
