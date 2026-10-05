# 04-search/runtime

这是 04 检索引擎的 V1 可执行实现。

## 当前固定模型

```text
intfloat/multilingual-e5-small
384维
CPU运行
```

GitHub 只保存代码和模型规定，不保存模型权重、真实产品数据或真实向量索引。

## 运行目录

运行路径由当前 Company Profile 提供兼容提示。

推荐显式设置通用变量：

```text
PRODUCT_DATA_ROOT=<Product_Data绝对路径>
```

当前润通 Profile 继续兼容：

```text
RUNTONG_PRODUCT_DATA
```

如模型已提前下载，推荐设置：

```text
EMBEDDING_MODEL_PATH=<multilingual-e5-small目录>
```

当前润通 Profile 同时兼容原有 `RUNTONG_EMBEDDING_MODEL_PATH`。

未设置本地模型路径时，会使用模型 ID 下载到：

```text
Product_Data/_models/hf_cache/
```

## 安装

```bash
python -m pip install -r 04-search/runtime/requirements.txt
```

网络慢时，推荐提前准备 wheel 和模型文件，再离线安装/加载。

## 首次建库

```bash
python 04-search/runtime/build_index.py
```

生成：

```text
Product_Data/Search_Index/
├─ records/records.jsonl
├─ keywords/keywords.json
├─ vectors/embeddings.npy
├─ vectors/vectors.faiss
└─ index_meta/index_meta.json
```

## 产品资料更新后同步

```bash
python 04-search/runtime/update_index.py
```

V1 会读取整个 Product_KB 做差异判断，但只对新增或语义发生变化的检索记录重新生成向量。

价格、MOQ、图片等不影响语义的变化会复用旧向量。

## 验证

```bash
python 04-search/runtime/validate_index.py
```

## 查询

```bash
python 04-search/runtime/search.py --request-json "<按 active Product Profile 生成的 Search_Request JSON>"
```

也可以把 JSON 从 stdin 输入。

## V1 边界

- 当前检索粒度：产品货号 + 工厂报价。
- 结构化条件优先，向量不能突破硬条件。
- 向量相似度只负责候选召回/辅助排序，不直接等于星级。
- 同一索引禁止混用不同 Embedding 模型。
- 更换向量模型必须整库重建。
- 任何向量错误都不应修改 Product_KB。
