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

默认自动寻找：

```text
<工作目录>/RUNTONG products/Product_Data/
```

推荐显式设置：

```text
RUNTONG_PRODUCT_DATA=D:\ACCIO\RUNTONG products\Product_Data
```

如模型已提前下载，可设置：

```text
RUNTONG_EMBEDDING_MODEL_PATH=D:\ACCIO\RUNTONG products\Product_Data\_models\multilingual-e5-small
```

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
python 04-search/runtime/search.py --request-json "{\"product_category\":\"鞋垫\",\"hard_conditions\":[{\"field\":\"MOQ\",\"op\":\"lte\",\"value\":3000}],\"soft_conditions\":[{\"field\":\"Softness\",\"op\":\"range\",\"value\":[1,3]}],\"priority\":[{\"field\":\"MOQ\",\"level\":\"high\"}],\"semantic_query\":\"每天站8小时，想脚底没那么累\"}"
```

也可以把 JSON 从 stdin 输入。

## V1 边界

- 当前检索粒度：产品货号 + 工厂报价。
- 结构化条件优先，向量不能突破硬条件。
- 向量相似度只负责候选召回/辅助排序，不直接等于星级。
- 同一索引禁止混用不同 Embedding 模型。
- 更换向量模型必须整库重建。
- 任何向量错误都不应修改 Product_KB。
