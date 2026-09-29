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
- Packaging_Options（预留）
- Special_Features
- Performance_Attributes

## 工厂供应层

描述某个工厂如何供应这款产品。

包括：
- Factory_Name
- Material
- Material_Detail
- Price
- MOQ
- Size_System
- Size_Range

## 核心规则

1. 一个 SKU 可以对应多个工厂供应方案。
2. 价格不能直接挂在 SKU 层。
3. MOQ 不能直接挂在 SKU 层。
4. 材质如果因工厂不同而变化，应记录在工厂供应层。
5. Material 用于标准化检索；Material_Detail 用于保留实际详细材质事实，两者都绑定具体 Factory Offer。
6. Material 虽然属于工厂供应层，但可以作为一级重要检索条件直接查询。
7. Packaging_Options 当前只是产品层对未来 Packaging_KB 的编号引用窗口，不在本模块展开包装本体规则。
8. 尺码如果因工厂不同而变化，应记录在工厂供应层。
9. 最终检索结果应支持返回：
   SKU + Factory_Name
