# 01 Local KB Structure / 本地知识库结构规范

本文件定义真实产品知识库在本地磁盘、移动硬盘或公司局域网中的目录与文件命名规范。

GitHub 仓库只保存规则、代码、模板和文档；真实产品数据不进入 Git。

---

## 一、总体目录

建议将“原始资料”和“标准化后的 Product_KB”分开。

```text
Product_Data/
├─ Raw_Input/
│  └─ 原始 Excel、图片、供应商资料等
│
├─ Product_KB/
│  ├─ insoles/
   │  ├─ F0228/
   │  │  ├─ product.md
   │  │  └─ main.jpg
   │  ├─ F1005/
   │  │  ├─ product.md
   │  │  └─ main.jpg
   │  └─ ...
   │
│  ├─ shoe-care/
│  └─ sports-support/
│
└─ Packaging_KB/              # 预留，V1 暂不启用
   ├─ insoles/
   ├─ shoe-care/
   └─ other-categories/
```

说明：

- `Raw_Input/` 是原始资料入口，不作为正式检索知识库。
- `Product_KB/` 只存已经标准化后的产品知识。
- `Packaging_KB/` 是未来独立包装知识库的预留目录，当前 V1 不要求建立或维护真实内容。
- 包装方案未来使用独立 `Packaging_ID`，产品只保存包装编号引用。
- Packaging_KB 内部按产品类别区分，例如鞋垫包装、鞋护理包装等。
- Product_KB 与未来 Packaging_KB 均可位于本地硬盘、移动硬盘或未来的公司服务器。
- Obsidian 仅可作为查看和编辑这些 Markdown 文件的工具，不是系统依赖。

---

## 二、产品分类目录

Product_KB 第一层按 `Product_Category` 划分。

当前鞋垫统一使用：

```text
Product_KB/insoles/
```

未来新增其他品类时，分别建立独立目录。

---

## 三、SKU 文件夹

每个 SKU 必须使用独立文件夹。

规则：

- 文件夹名直接使用 `SKU_ID`。
- 一个 SKU 只能有一个主文件夹。
- 同一个 SKU 即使有多个工厂，也不能重复建立多个 SKU 文件夹。
- 多工厂供应信息统一写入同一个 SKU 的 `product.md` 中。

正确：

```text
insoles/
└─ F0228/
   ├─ product.md
   └─ main.jpg
```

错误：

```text
insoles/
├─ F0228-富置高/
└─ F0228-其他工厂/
```

---

## 四、product.md

每个 SKU 的标准产品数据统一写入：

```text
product.md
```

字段和结构必须遵守：

- `01-schema/product-template.md` 定义的标准 product.md 模板
- `01-schema/` 定义的数据结构
- `02-taxonomy-rules/` 定义的标准词与映射规则

不得自行增加近义标签、临时字段或重复字段。

同一 SKU 的多个 Factory Offer 必须作为多个供应方案写在同一个 `product.md` 内。

---

## 五、产品图片

当前每个 SKU 使用一张主产品多角度组合图。

统一命名：

```text
main.jpg
```

如源文件必须保留 PNG，可使用：

```text
main.png
```

原则：

- 图片文件与对应 SKU 放在同一文件夹。
- `Main_Image` 指向该文件。
- 不把真实产品图片上传到 GitHub。
- 后续如需要支持多张图片，再单独扩展图片结构，不在 V1 提前复杂化。

---

## 六、原始资料与标准知识分离

业务人员现有的 Excel、供应商表格、图片和文字描述先进入 `Raw_Input/`。

处理链路：

```text
原始 Excel / 图片 / 供应商资料
        ↓
Raw_Input
        ↓
字段提取
        ↓
标准词映射
        ↓
AI 语义理解
        ↓
人工确认必要字段
        ↓
生成标准 product.md
        ↓
写入 Product_KB
```

禁止直接把未经清洗的原始 Excel 当成正式 Product_KB。

---

## 七、包装知识库预留边界

当前 03-data-management V1 只处理 Product_KB，不处理包装资料导入、清洗和更新。

未来启用包装模块时：

```text
Product_KB
   │
   │ Packaging_ID / Packaging_Options
   ↓
Packaging_KB
```

Packaging_KB 使用独立编号与独立目录，不把包装本体资料直接塞进产品 product.md。

---

## 八、核心原则

1. 一个 SKU 一个文件夹。
2. 一个 SKU 一个 `product.md`。
3. 一个 SKU 可以包含多个 Factory Offer。
4. 真实产品数据只放本地 Product_KB，不进 Git。
5. 原始资料与标准化产品知识分开存储。
6. 所有正式字段服从 01 Schema。
7. 所有标准标签和自然语言映射服从 02 Taxonomy。
8. 包装当前只保留 Packaging_ID 引用窗口，V1 不进入产品数据管理流程。
