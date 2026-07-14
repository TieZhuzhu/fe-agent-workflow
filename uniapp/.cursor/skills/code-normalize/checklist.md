# code-normalize 全量规范审计清单

> `code-normalize` 审计与验收权威清单。阻塞项未通过不得声称「已按规范优化」。

## §通用（所有页面）

### 规范预加载 🔴

- [ ] 已 Read rules-activation 通用基线 + uniapp代码生成指南
- [ ] 已 Read 页面类型 rules + 接口对接规范
- [ ] request import 与同模块一致
- [ ] 交付含「规范预加载」汇报行

### 目录与分包 🔴

- [ ] 非 tabBar 页在 subPackages，未入主包
- [ ] 子包按功能模块，优先复用已有子包
- [ ] pages.json path 与文件一致
- [ ] constants / utils 分离
- [ ] 组件 PascalCase + index.vue
- [ ] `@/` alias

### types（Vue 3 TS）🔴

- [ ] 页面类型在 types.ts
- [ ] hook/utils 不重复定义页面级 interface
- [ ] 入参无兜底；出参无过度 normalize

### Vue 写法 🔴

- [ ] Vue 3：script setup；Vue 2：Options API；无混用
- [ ] services 箭头函数导出
- [ ] 原生组件优先，无 Element/PC 组件库

### 样式 🔴

- [ ] scoped SCSS；rpx 单位
- [ ] 深度选择器正确（:deep / ::v-deep）

### 代码质量 🔴

- [ ] 无 console.log、dead code
- [ ] 无未使用 import；lint 零 error
- [ ] 单文件 >800 行建议拆分 🟡

### 状态与接口 🔴

- [ ] loading / empty / error 三态
- [ ] onLoad 参数处理正确
- [ ] 无 mock

## §列表页

- [ ] 下拉刷新或分页加载
- [ ] 空态展示

## §表单页

- [ ] 提交防重复
- [ ] 校验提示 uni.showToast

## §路由 🔴

- [ ] pages.json 已正确注册
- [ ] 跳转 API 正确（switchTab vs navigateTo）
