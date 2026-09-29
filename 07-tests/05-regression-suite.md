# 05 Regression Suite / 回归测试集

本文件定义系统长期稳定性测试方式。

## 目标

建立固定真实业务问题集。

每次系统发生重要修改后，重复执行同一批测试，判断系统是否被改坏。

## 测试编号

建议使用：

```text
Q001
Q002
Q003
...
```

每个测试至少保存：

```text
Test_ID
User_Query
Expected_Search_Request
Expected_Result
Expected_Factory_Offer
Expected_Unmet_Conditions
Notes
```

## 需要触发回归测试的变化

- Schema 修改
- Taxonomy / Rules 修改
- 03 数据导入或维护规则修改
- 04 Search 修改
- Ranking 修改
- Vector / Embedding 修改
- 05 Retrieval Tool 修改
- 06 Agent 修改
- 更换 Agent 平台或模型

## 数据安全

公开 GitHub 仓库只保存：

- 脱敏测试案例
- 测试结构
- 测试规则

真实客户名、真实敏感价格、工厂敏感信息等不进入公开测试集。
