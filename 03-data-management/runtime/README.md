# 03-data-management/runtime

这是 03 数据管理的 V1 可执行层。

目标不是让程序“猜产品”，而是把可确定的数据操作程序化，把语义判断继续交给当前平台 LLM + 人工确认。

## V1 执行链路

```text
固定格式 Excel/CSV + SKU 图片
↓
ingest_table.py
↓
staging candidate.json
↓
Agent 按 02 规则提出 Function / Scenario / Performance REVIEW
↓
人工确认
↓
patch_candidate.py
↓
validate_candidate.py
↓
maintenance.py 生成差异预览
↓
操作者明确确认
↓
写入 Product_KB + Change Set
↓
可选 update_index.py
```

## 1. 表格导入

```bash
python 03-data-management/runtime/ingest_table.py "<产品表.xlsx>"
```

可选：

```bash
--sheet "Sheet1"
--category "鞋垫"
--image-dir "<图片目录>"
--output "<candidate.json>"
```

支持：

- .xlsx
- .xlsm
- .csv

脚本自动完成：

- 列名映射
- SKU / Factory 提取
- MOQ / Price 数值清洗
- Material 标准化
- Size_System 标准化
- 同 SKU 多工厂合并
- SKU 图片初步关联

脚本不会凭材质猜测场景、功能或性能。

## 2. REVIEW

如果原表存在产品描述，候选会产生：

```text
<SKU>-SEMANTIC
status = pending
```

Agent 按 02-taxonomy-rules 生成候选，向操作者集中确认。

确认后使用结构化 patch 写回 staging candidate。

示例 patch：

```json
{
  "products": {
    "F0228": {
      "fields": {
        "Function_Tags": ["缓震", "回弹", "透气排湿"],
        "Scenario_Tags": ["日常", "长距离行走"]
      },
      "Performance_Attributes": {
        "Cushioning": 4,
        "Elasticity": 4,
        "Softness": 4
      },
      "Review_Status": {
        "F0228-SEMANTIC": "confirmed"
      }
    }
  }
}
```

执行：

```bash
python 03-data-management/runtime/patch_candidate.py candidate.json patch.json
```

## 3. 校验

```bash
python 03-data-management/runtime/validate_candidate.py candidate.json
```

只要还有 pending REVIEW，禁止正式写库。

## 4. 差异预览

```bash
python 03-data-management/runtime/maintenance.py candidate.json
```

只输出：

- new_sku
- update
- new_factory_offer
- image_update

不会写 Product_KB。

空白字段不会覆盖旧值；新表没出现的旧工厂不会被删除。

## 5. 正式提交

只有操作者明确确认后：

```bash
python 03-data-management/runtime/maintenance.py candidate.json --commit --confirm
```

如同时同步 04：

```bash
python 03-data-management/runtime/maintenance.py candidate.json --commit --confirm --update-index
```

提交前自动备份旧 product.md / 主图到：

```text
Product_Data/_Staging/backups/<timestamp>/
```

并生成标准 Change Set。

## 6. 显式删除

删除不能通过空白表格触发。

删除 Factory Offer：

```bash
python 03-data-management/runtime/delete_product.py --sku F0228 --factory "某工厂" --confirm --update-index
```

删除整个 SKU：

```bash
python 03-data-management/runtime/delete_product.py --sku F0228 --confirm --update-index
```

删除前同样自动备份。

## V1 边界

程序负责：

- 确定性字段提取
- 标准值校验
- 合并
- 差异
- 空白保护
- 备份
- 写入
- Change Set
- 索引同步调用

平台 LLM 负责：

- 理解产品描述
- 生成 REVIEW 候选
- 根据 02 规则映射自然语言

人工负责：

- 确认 REVIEW
- 确认实际覆盖 / 删除意图

这不是“未代码化”，而是故意把主观判断留在 LLM / 人工层，把数据写入安全边界固定在代码里。
