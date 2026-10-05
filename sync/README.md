# Offline Sync Verification

Accio 当前本地 Skill 目录不是 Git 仓库，因此 V1 不把“复制成功”当成“同步成功”。

标准：

```text
GitHub = 代码真源
↓
逐文件覆盖到 Accio 本地
↓
verify_sync.py 按 Git Blob SHA-1 校验
↓
全部 OK
↓
才认可后续测试结果
```

## 为什么使用 Git Blob SHA-1

GitHub API 返回的每个文件 SHA 就是 Git Blob SHA-1。

本地即使没有 `.git`，也可以直接根据文件字节重新计算同一个值，因此可以证明：

> 本地这个文件的字节内容与 GitHub 对应文件完全一致。

脚本同时输出本地 SHA256 供排障，但发布清单的权威比较值使用 Git Blob SHA-1。

## 使用

同步完发布清单中的所有文件后：

```bash
python sync/verify_sync.py
```

通过时：

```text
ok = true
matched = total
problems = []
```

任何：

- MISSING
- MISMATCH

都表示本地代码不能视为当前 GitHub V1 发布版本。

## 校验范围

`release_manifest.json` 只列入会影响 V1 行为或验收结果的受控文件：

- SKILL
- 01～07 核心规则
- 03 / 04 / 05 可执行代码
- 07 测试代码
- 当前平台 Adapter

真实业务数据不在校验范围：

- Product_KB
- Search_Index
- Embedding 模型
- 产品图片
- Raw_Input
