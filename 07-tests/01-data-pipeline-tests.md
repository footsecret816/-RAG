# 01 Data Pipeline Tests / 数据链路测试

本文件用于验证 03-data-management 是否正确处理真实产品资料。

## 重点测试

- SKU_ID 是否正确提取
- 同一 SKU 多 Factory Offer 是否正确合并
- Material 是否正确标准化
- Material_Detail 是否保留真实信息
- REVIEW 是否被错误自动确认
- MISSING 是否被错误补猜
- 空白字段是否错误覆盖旧值
- 新 Factory_Name 是否正确新增 Factory Offer
- 新图片是否正确关联 SKU
- ③④产生的候选数据是否先经过⑤校验再正式写入

## 必测异常

- 新表格 MOQ 为空，但旧 MOQ 有值
- 新表格未出现旧工厂
- 同 SKU + 同 Factory_Name 重复
- 图片与 SKU 无法可靠匹配
- 非标准 Material / Tag
- REVIEW 尚未人工确认

## 通过标准

测试结果必须符合 01 Schema、02 Rules、03 Data Management 的既定规则。
