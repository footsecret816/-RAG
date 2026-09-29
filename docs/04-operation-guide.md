# Operation Guide / 管理员操作说明

## 查询产品

普通业务查询：

```text
用户问题
→ 06 Agent
→ 05 Retrieval Tool
→ 04 Search
```

默认只读，不修改 Product_KB。

## 新增产品

```text
上传固定格式产品表格 + 图片
→ 03③
→ 生成候选
→ REVIEW 确认
→ ⑤校验
→ PASS
→ 写入 Product_KB
```

## 更新产品

同 SKU 已存在时：

```text
→ 03④
→ 对比新旧数据
→ 只显示真实变化
→ 人工确认
→ ⑤校验
→ PASS
→ 写入
```

规则：

- 新值为空：保留旧值
- 同 SKU + 新工厂：新增 Factory Offer
- 新表格未出现旧工厂：不删除
- 删除必须明确发起

## 图片替换

以 SKU 可靠匹配图片。

检测到已有主图时，确认后作为候选替换，再经过⑤校验后写入。

## 搜索同步

Product_KB 成功写入后，由 03⑥生成 Change Set，04②负责同步搜索层。
