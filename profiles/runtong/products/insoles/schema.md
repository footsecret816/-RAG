# Runtong Insoles Schema / 润通鞋垫产品 Schema

本文件属于：

```text
profiles/runtong/products/insoles/
```

可执行字段、值域、别名以同目录 `profile.yaml` 为真源。

## Product Category

```text
Product_Category = 鞋垫
```

## Performance Attributes

- Cushioning：1–5，数值越高缓震越强
- Elasticity：1–5，数值越高回弹越强
- Softness：1–5，1 最硬，5 最软
- Arch_Height：低 / 中 / 高
- Arch_Support：无支撑 / 轻度支撑 / 强支撑
- Heel_Cup_Depth：平 / 浅 / 中 / 深

## Product Profile 范围

本 Product Profile 还定义：

- 材质标准词与别名
- Function_Tags
- Scenario_Tags
- Special_Features
- Performance 字段和值域
- 表格列别名
- 业务展示优先字段

## 数据边界

真实 SKU、工厂、价格、MOQ、图片不进入本目录；真实数据仍由外部 Product_KB 管理。

未来替换其他公司或产品时，替换 Company / Product Profile，不修改 Core。
