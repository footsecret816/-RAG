# Runtime & Maintenance / 运行与维护规则

## 一、首次运行

本 Skill 不内置真实 Product_KB。

运行时需要 Agent 能访问公司 Product_KB。

如果 Product_KB 路径没有出现在当前工作区或上下文中：

- 先查找当前可访问的工作区；
- 找不到时询问用户 Product_KB 在哪里；
- 不要虚构路径。

## 二、查询模式

普通业务员提问默认只读。

例如：

```text
“推荐几个户外鞋垫”
“F0228 哪个工厂 MOQ 最低？”
“要 PU，MOQ 不超过 3000”
```

都只查询，不修改任何产品文件。

## 三、维护模式

只有以下两项同时成立才进入维护：

1. 用户提供或指定了真实产品资料；
2. 用户明确要求新增、修改、替换或删除。

例如：

```text
“把 F0228 富置高的价格改成 7.2”
“导入这份新产品表”
“把 F0228 的主图替换成这张”
```

## 四、维护流程

```text
原始资料
↓
提取 / 标准化
↓
生成候选变更
↓
显示 Diff
↓
人工确认
↓
数据校验
↓
PASS
↓
正式写入 Product_KB
```

重要规则：

- 新值为空，不覆盖旧值；
- 新资料没出现旧工厂，不代表删除旧工厂；
- 同 SKU + 新 Factory_Name = 新增 Factory Offer；
- 删除必须明确发起；
- 未确认的 REVIEW 字段不能写成确定事实。

## 五、REVIEW 最短确认交互

所有 REVIEW 字段应尽量集中在一次确认中，不要逐项追问。

推荐展示：

```text
需要确认：

性能
P1 缓震：3
P2 回弹：4
P3 软硬：4

场景
S1 日常
S2 长距离行走
```

### 默认确认

如果操作者认可全部候选，只需回复：

```text
确认
```

表示接受本轮全部 REVIEW 候选。

### 局部修改

允许使用短指令：

```text
P2=3
去掉S2
S1,S2
P=344
S=12
```

解释：

- `P2=3`：只修改回弹评分；
- `去掉S2`：删除第 2 个场景候选；
- `S1,S2` 或 `S=12`：确认场景 1、2；
- `P=344`：按 P1/P2/P3 顺序确认 3/4/4。

如果短指令存在歧义，才允许补问，不要为了形式完整而要求重新输入全部内容。

### 全局配置

以下属于运行环境或数据口径配置，不应每个 SKU 重复确认：

- Product_KB 路径
- 价格字段口径
- 默认币种
- 其他明确的全局导入设置

首次确认后沿用，只有用户主动修改或检测到冲突时再询问。

### 交互原则

> 不要求操作者重复输入 AI 已经展示出来的文字；优先使用“确认 / 编号=值 / 删除编号 / 选择编号”的最短交互方式。

## 六、平台边界

平台可能提供不同的文件搜索、文件读写或工具能力。

本 Skill 只要求结果符合统一业务规则，不绑定具体工具名称。

如果平台当前只有读权限：

- 正常执行产品查询；
- 遇到维护请求时只生成候选变更和 Diff，不声称已经写入。


---

## 七、V1 可执行维护命令

完整仓库运行环境中，03 的确定性数据维护已代码化。

固定表格导入：

```bash
python 03-data-management/runtime/ingest_table.py "<产品表.xlsx>"
```

REVIEW 确认后先校验：

```bash
python 03-data-management/runtime/validate_candidate.py candidate.json
python 03-data-management/runtime/maintenance.py candidate.json
```

第二条只生成 Diff，不写库。

只有用户明确确认本次变更后才执行：

```bash
python 03-data-management/runtime/maintenance.py candidate.json --commit --confirm --update-index
```

删除必须显式使用：

```bash
python 03-data-management/runtime/delete_product.py ...
```

禁止把空白单元格解释为删除。

## 八、本地镜像一致性

如果运行平台上的 Skill 目录不是 Git 仓库，正式测试前必须执行：

```bash
python sync/verify_sync.py
```

只有 release_manifest 中受控文件全部匹配 GitHub Blob SHA，才视为当前发布版本。
