# 功能开发规范验收清单

**按项目 Vue 版本审查。** `vue@2.x` 见 `Vue2代码生成指南.mdc`。

## Feature Spec（若有 docs/features/<slug>/）

- [ ] design.md 与实现 path / 目录 / 文件清单一致
- [ ] field-map.md 与 types / 模板 / services 一致（有接口时）
- [ ] tasks.md 相关项已勾选
- [ ] 已通过 feature-verify 或交付 verify 报告

## 规范预加载

- [ ] 已 Read rules-activation 及页面类型 rules
- [ ] 已 Read uniapp代码生成指南.mdc
- [ ] request import 与项目一致
- [ ] 交付含预加载摘要行

## 目录与分包

- [ ] 非 tabBar 页在 `subPackages/`，未入主包
- [ ] 优先复用已有子包，未随意新建子包
- [ ] `pages.json` path 与磁盘文件一致
- [ ] 接口位置符合项目惯例（页面级 / 集中式）
- [ ] 组件 PascalCase + `index.vue`

## 页面类型

- [ ] 类型判定正确（列表 / 表单 / 详情 / 弹层 / 复杂）
- [ ] 原生组件优先，uview 仅补充
- [ ] 列表：下拉刷新/分页/空态
- [ ] 表单：校验 + 防重复提交

## Vue 写法

- [ ] Vue 3：`<script setup>`；Vue 2：Options API；**无混用**
- [ ] 箭头函数导出 services
- [ ] onLoad 正确处理路由参数
- [ ] 单文件建议 ≤800 行

## 状态与接口

- [ ] loading / empty / error 三态
- [ ] 无 mock
- [ ] 入参无兜底；出参无 normalizeRows
- [ ] 展示空值 `?? '-'`

## 路由

- [ ] pages.json 已注册
- [ ] tabBar 用 switchTab；普通页用 navigateTo
- [ ] navigationBarTitleText 正确

## 样式

- [ ] scoped SCSS；rpx 为单位
- [ ] Figma 切图：内容区视觉与稿一致；未画状态栏/胶囊/Home 条
- [ ] 安全区：`env(safe-area-inset-bottom)`（固定底栏）

## 代码质量

- [ ] `@/` alias；无 console.log
- [ ] lint 零 error（有 lint 时）
