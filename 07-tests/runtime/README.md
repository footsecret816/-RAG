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
