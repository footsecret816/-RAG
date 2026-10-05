---
name: product-knowledge-retrieval
description: Internal product knowledge retrieval and maintenance skill for company Product_KB. Supports product ingestion, normalization, hybrid retrieval, factory-offer comparison, and explicit maintenance requests. Never invent product facts.
compatibility: Requires access to an external Product_KB folder and a Python runtime for executable hybrid retrieval.
metadata:
  author: runtong-wayyeah
  version: "1.3.0-rc1"
---

# Product Knowledge Retrieval Skill

本仓库整体作为“产品知识检索 Skill”使用。

## 核心目标

支持两类任务：

1. 产品资料入库与维护；
2. 业务员自然语言查询、筛选和推荐产品。

真实产品数据放在外部 `Product_KB`。

GitHub 只保存：

- 通用 Core；
- 可替换 Company / Product Profiles；
- 数据结构；
- 通用标签和查询规则；
- 03 数据导入 / 维护可执行代码；
- 04 混合检索可执行代码；
- 05 查询接口与校验代码；
- Agent 展示规则；
- 测试与离线同步校验规范。

---

## Profile 边界

当前 active profile：

```text
profiles/active-profile.yaml
→ company_profile: runtong
→ default_product_profile: insoles
```

公司 / 产品专属信息必须来自 `profiles/`；Core 不得把润通、鞋垫材质、标签、性能字段等写死在运行代码中。

更换公司或产品时，目标是替换 Profile + Product_KB，不修改 Core。

---

## 当前 V1 可执行检索架构

```text
业务员自然语言
↓
05 查询标准化
↓
Search_Request JSON
↓
04-search/runtime/search.py
↓
结构化条件检索
+
关键词检索
+
multilingual-e5-small 向量检索
↓
融合排序
↓
Search_Result JSON
↓
06 Agent 展示
```

V1 固定向量模型：

```text
intfloat/multilingual-e5-small
384维
CPU运行
```

聊天大模型可以更换。

同一套产品向量索引不得混用其他 Embedding 模型。

---

## 首次运行

先确认当前环境可以访问：

```text
Product_Data/
├─ Product_KB/
└─ Search_Index/
```

推荐设置通用环境变量：

```text
PRODUCT_DATA_ROOT=<Product_Data绝对路径>
```

当前润通 Profile 继续兼容原有 `RUNTONG_PRODUCT_DATA`，因此现有 Accio 环境无需立即改动。

### 第一步：检查运行环境

执行：

```bash
python 04-search/runtime/bootstrap.py
```

如果缺依赖，获得用户授权后执行：

```bash
python 04-search/runtime/bootstrap.py --install
```

网络慢时优先使用本地 wheel。

### 第二步：准备 Embedding 模型

推荐把模型提前放在：

```text
Product_Data/_models/multilingual-e5-small/
```

如果本地没有模型且允许下载：

```bash
python 04-search/runtime/bootstrap.py --download-model
```

### 第三步：首次建立索引

当 Product_KB 已有正式产品资料，但 Search_Index 尚未建立时：

```bash
python 04-search/runtime/build_index.py
```

完成后执行：

```bash
python 04-search/runtime/validate_index.py
```

索引验证通过后才进入正常业务查询。

---

## 日常查询流程

收到产品查询时：

1. 按 02 的规则识别产品品类；
2. 拆分硬条件、软条件、优先级和剩余模糊语义；
3. 按 05 生成标准 Search_Request JSON；
4. 调用：

```bash
python 04-search/runtime/search.py --request-json "<Search_Request JSON>"
```

7. 读取 Search_Result；
8. 按 06 的展示规则回答。

Agent 不得绕过检索结果重新凭感觉挑产品。

查询标准化特别规则：

- 能可靠映射到 active Product Profile 的场景 / 功能 / 性能，先结构化，同时可保留原始模糊语义给向量；
- “MOQ越低越好”使用 `{"field":"MOQ","level":"high","goal":"min"}`；
- “价格贵一点没关系”可使用 `{"field":"Price","level":"low","goal":"min"}`；
- priority.goal 即使没有 soft_conditions，也会进入本次匹配分和排序。

---

## 产品维护后的索引同步

只有用户明确要求新增、修改、替换或删除产品资料时，才进入 03 Data Management。

完成：

```text
正式数据写入 Product_KB
+
Validation = PASS
```

后，执行：

```bash
python 04-search/runtime/update_index.py
```

该脚本会：

- 重新读取 Product_KB；
- 复用没有语义变化的旧向量；
- 只重新生成新增或语义变化的向量；
- 删除失效检索记录；
- 重建轻量 FAISS 索引；
- 重新做完整性验证。

普通查询不得修改 Product_KB。

---

## 本地版本一致性

Accio 等无 `.git` 的本地 Skill 镜像，必须在测试前执行：

```bash
python sync/verify_sync.py
```

只有发布清单中的受控文件全部匹配 GitHub Blob SHA，测试结果才视为当前 GitHub 版本的有效结果。

---

## REVIEW 确认交互

产品入库时，所有需要人工确认的 REVIEW 字段应集中一次展示，并使用短编号。

推荐：

```text
性能
P1 缓震：3
P2 回弹：4
P3 软硬：4

场景
S1 日常
S2 长距离行走
```

支持：

```text
确认
P2=3
去掉S2
P=344
S=12
```

KB 路径、价格口径等全局配置只在首次设置或发生变化时确认。

---

## 必须遵守的核心模块

- `01-schema/`：跨产品公共数据结构
- `02-taxonomy-rules/`：通用查询 / 标签规则框架
- `profiles/`：当前公司与产品专属规则真源
- `03-data-management/`：产品导入、维护、校验和 Change Set
- `04-search/`：检索规则和可执行检索引擎
- `05-retrieval-tool/`：统一 Search_Request / Search_Result
- `06-agent/`：Agent 行为与回答格式
- `07-tests/`：测试与回归

如上层说明与具体模块冲突，以对应 01～07 模块为准。

---

## 产品检索粒度

固定为：

```text
Product SKU + Factory Offer
```

同一 SKU 的不同工厂方案必须独立判断。

不得混用不同工厂的：

- Price
- MOQ
- Material
- Size

---

## 硬条件

硬条件不能被：

- 关键词命中；
- 向量相似度；
- Agent 主观判断；

突破。

如果没有完全匹配：

- 明确返回无完全匹配；
- 可以提供接近候选；
- 必须保留未满足条件。

---

## 业务员结果展示

默认：

```text
后台检索
→ 排序
→ 去同质化
→ 每个 Product_Category 最多 Top 5
→ 紧凑产品表
→ Packaging 推荐 2～3 个（如已有真实数据）
```

产品表核心列：

```text
图片｜SKU｜品类关键规格｜MOQ｜价格｜⭐本次需求匹配度｜本次推荐理由
```

要求：

- Main_Image 可访问时优先直接显示产品图片；
- 星级只表示本次需求匹配度；
- Agent 不得自行修改 04 返回的星级；
- Top 5 是上限，不强制凑满；
- 大量相似候选需要去同质化；
- Packaging 不占产品 Top 5；
- Packaging_KB 没有真实数据时不得编造；
- 默认回答保持简短。

---

## 数据真实性

不得自行编造：

- SKU
- Factory_Name
- Material
- Material_Detail
- Price
- MOQ
- Size
- Packaging_SKU
- Performance_Attributes

缺失就明确标记缺失。

---

## 平台兼容

本 Skill 不绑定任何一家智能体平台。

任意平台只要能够：

- 运行 Python；
- 访问 Product_KB；
- 加载 V1 Embedding 模型；
- 持久保存 Search_Index；
- 把 JSON 检索结果交给上层 Agent；

即可复用同一套核心系统。

平台专属差异只放在：

`adapters/`
