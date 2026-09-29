# 数据层级边界规则

## 目标

防止产品事实和工厂供应事实混在一起。

## 产品层

描述产品本身。

包括：
- Product_Category
- SKU_ID
- Main_Image
- Function_Tags
- Scenario_Tags
- Performance_Attributes

## 工厂供应层

描述某个工厂如何供应这款产品。

包括：
- Factory_Name
- Material
- Price
- MOQ
- Size_System
- Size_Range

## 核心规则

1. 一个 SKU 可以对应多个工厂供应方案。
2. 价格不能直接挂在 SKU 层。
3. MOQ 不能直接挂在 SKU 层。
4. 材质如果因工厂不同而变化，应记录在工厂供应层。
5. 尺码如果因工厂不同而变化，应记录在工厂供应层。
6. 最终检索结果应支持返回：
   SKU + Factory_Name
