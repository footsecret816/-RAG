# Accio Work Adapter

本目录只记录 Accio Work 的安装与接入方式。

核心规则和运行代码仍然在仓库主体中，不在这里复制另一套产品逻辑。

---

## 当前 V1 运行方式

Accio Work 当前不需要使用平台 Knowledge Base。

实际链路：

```text
Accio Agent
↓
Product Knowledge Retrieval Skill
↓
Python Runtime
↓
Product_KB
+
结构化索引
+
关键词索引
+
FAISS 向量索引
↓
返回 Search_Result JSON
↓
Accio 当前聊天大模型组织最终回答
```

向量模型固定为：

```text
intfloat/multilingual-e5-small
384维
CPU运行
```

---

## 已验证的 Accio 能力

当前已验证：

- bash 可调用 Python / Node
- Python 3.12 可用
- pip 可安装第三方库
- HuggingFace 可访问
- 工作目录文件可持久保存
- FAISS 可建立、保存、重载、删除和新增向量
- bash stdout 可返回给 Agent
- Product_Data 可放在 Accio 工作目录内长期访问

因此可以使用：

```text
Skill + Python + 本地 Embedding 模型 + 本地 FAISS
```

不依赖 Accio Knowledge Base。

---

## 推荐目录

示例：

```text
D:\ACCIO\
├─ <Skill仓库>
└─ RUNTONG products\
   └─ Product_Data\
      ├─ Product_KB\
      ├─ Packaging_KB\
      ├─ Raw_Input\
      ├─ Search_Index\
      └─ _models\
```

推荐设置：

```text
RUNTONG_PRODUCT_DATA=D:\ACCIO\RUNTONG products\Product_Data
```

---

## 首次初始化

### 1. 检查环境

```bash
python 04-search/runtime/bootstrap.py
```

### 2. 安装依赖

网络正常时：

```bash
python 04-search/runtime/bootstrap.py --install
```

如果网络慢，优先使用本地 wheel：

```bash
python 04-search/runtime/bootstrap.py --install --wheel-dir "<本地wheel目录>"
```

### 3. 下载 / 准备向量模型

推荐提前把模型放到：

```text
Product_Data/_models/multilingual-e5-small/
```

也可以执行：

```bash
python 04-search/runtime/bootstrap.py --download-model
```

由于 Accio 环境下载大文件可能较慢，正式部署优先预置模型文件。

### 4. 首次建立检索索引

```bash
python 04-search/runtime/build_index.py
```

### 5. 验证

```bash
python 04-search/runtime/validate_index.py
```

---

## 日常产品查询

Agent 先按照 02 + 05 规则，把业务员自然语言转换成标准 Search_Request JSON。

然后执行：

```bash
python 04-search/runtime/search.py --request-json "<Search_Request JSON>"
```

Python 返回标准 Search_Result JSON。

Agent：

- 不重新挑选产品；
- 不修改 Search_Result 星级；
- 只负责展示图片、关键规格、推荐理由和必要说明。

---

## 产品资料导入与更新

V1 不再依赖 Agent 直接手工改 product.md。

固定格式 Excel / CSV 先执行：

```bash
python 03-data-management/runtime/ingest_table.py "<产品表.xlsx>"
```

REVIEW 确认并校验后先看差异：

```bash
python 03-data-management/runtime/maintenance.py candidate.json
```

用户明确确认后再提交并同步索引：

```bash
python 03-data-management/runtime/maintenance.py candidate.json --commit --confirm --update-index
```

删除 SKU / Factory Offer 必须使用 `delete_product.py` 显式执行。

该脚本会：

- 重新读取 Product_KB；
- 对比现有检索记录；
- 复用未发生语义变化的旧向量；
- 只对新增或语义变化记录重新向量化；
- 删除已不存在的旧记录；
- 重建轻量 FAISS 索引；
- 重新验证索引完整性。

---

## Product_KB

Skill 本身不包含真实产品数据。

如果 Agent 无法访问 Product_KB：

- 不允许猜测；
- 不允许使用仓库中的示例冒充真实产品；
- 先解决工作目录权限或 Product_Data 路径。

---

## 图片展示

Accio 已验证可以直接显示 Product_KB 中图片。

优先级：

```text
① 推荐表内直接显示真实图片
② 表格不支持时，在对应 SKU 附近直接显示缩略图
③ 前两种失败时，才使用可点击图片引用
```

不要默认只输出：

```text
main.jpg
附件图标
仅文件名链接
```

Packaging_KB 启用后，包装图片同样处理。

---

## 权限注意

Accio 中 bash 默认可能需要授权。

首次部署时应确认：

- Python 命令允许执行；
- Skill 工作区已包含 Product_Data；
- 不依赖本机特殊的 bypassSandbox 配置。

---

## 平台边界

Accio Work 只是当前一个运行平台。

核心 V1：

```text
Product_KB
+
GitHub规则
+
multilingual-e5-small
+
Python混合检索代码
```

保持平台无关。

未来接入其他智能体平台时，只要该平台能够：

- 运行 Python；
- 读取 Product_KB；
- 加载同一向量模型；
- 保存本地索引；
- 把 JSON 结果交回上层 Agent；

即可复用同一套核心系统。


---

## Accio 本地目录与 GitHub 一致性

Accio 当前本地 Skill 目录可能没有 `.git`，因此不要以“文件已复制”作为同步成功标准。

每次覆盖 GitHub 发布文件后必须运行：

```bash
python sync/verify_sync.py
```

要求：

```text
ok = true
matched = total
problems = []
```

只有校验通过后，才运行：

```bash
python 07-tests/runtime/test_core.py
python 07-tests/runtime/test_data_management.py
```

以及真实业务回归集。

`Product_KB`、`Search_Index`、Embedding 模型、真实图片不属于 GitHub 镜像校验对象。
