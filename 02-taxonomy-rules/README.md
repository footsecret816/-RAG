# 02 Taxonomy & Rules

本模块定义标签体系、自然语言映射与检索规则。

当前拆分为：

- `A-framework/`：通用规则框架，可跨产品、跨平台复用。
- `B-business-knowledge/`：按产品类别维护真实业务词库与映射知识。

## A-framework

当前包含：

1. 标签定义规则
2. 近义词与自然语言映射规则
3. 查询条件拆分规则
4. 查询优先级规则
5. 硬条件与软条件规则
6. 数据层级边界规则

## B-business-knowledge

B 必须先按 `Product_Category` 区分。

当前已建立：

```text
B-business-knowledge/
└─ insoles/
   ├─ 01-material-mapping.md
   ├─ 02-function-tags.md
   ├─ 03-scenario-tags.md
   ├─ 04-special-features.md
   ├─ 05-performance-attributes.md
   └─ 06-business-concept-mapping.md
```

鞋垫类当前核心结构：

```text
Material
+
Function
+
Scenario
+
Special Features
+
Performance
+
Business Concept Mapping
```

真实 SKU、工厂、价格、MOQ、图片等数据仍由独立 Product_KB 管理，不进入 Git。
