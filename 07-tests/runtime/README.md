# Runtime Tests

这一目录用于验证可执行检索代码。

## 基础测试

不需要下载 Embedding 模型即可运行：

```bash
python 07-tests/runtime/test_core.py
```

覆盖：

- product.md 解析
- 一条 SKU + Factory Offer 生成一条检索记录
- 语义文本不混入价格 / MOQ / 工厂名
- MOQ 硬条件
- 标签条件
- 软条件权重与匹配分

## 真正向量测试

首次在真实 Product_KB 上部署时，再运行：

```bash
python 04-search/runtime/build_index.py
python 04-search/runtime/validate_index.py
```

后续还需要基于真实 SKU 建立 20～30 条固定业务查询回归集。


## 数据管理测试

```bash
python 07-tests/runtime/test_data_management.py
```

覆盖：

- 同 SKU 多工厂合并
- Material / MOQ 等确定性清洗
- pending REVIEW 阻止写库
- 空白字段不覆盖旧值
- 新工厂增量追加

## 真实业务回归

复制模板：

```text
07-tests/runtime/regression_cases.example.json
```

到私有业务数据目录，例如：

```text
Product_Data/_tests/regression_cases.json
```

填入真实 SKU 的预期结果后执行：

```bash
python 07-tests/runtime/regression_runner.py "<Product_Data/_tests/regression_cases.json>"
```

公开 GitHub 不保存真实 SKU、工厂价格或客户信息。
