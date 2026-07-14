# 功能开发规范验收清单

**默认按 Vue 3 审查。** `vue@2.x` 项目按 `Vue2代码生成指南.mdc` + 下文 §Vue 2 兼容 完整核对。

## Feature Spec（新建页，若有 docs/features/<slug>/）

- [ ] design.md 与实现 path / 目录 / 文件清单一致
- [ ] field-map.md 与 types / 模板 prop / services 一致（有接口时）
- [ ] tasks.md 相关项已勾选
- [ ] 已通过 [feature-verify](../feature-verify/SKILL.md) 或交付 verify 报告

## 规范预加载

- [ ] 已 Read `shared/rules-activation.md` 及页面类型对应 rules
- [ ] 已 Read `TypeScript与types规范.mdc`（Vue 3 TS）
- [ ] 已 Read `接口对接规范.mdc`（联调 / 入参 / 出参）
- [ ] `request` import 路径与项目已有 services 一致
- [ ] 交付说明含预加载摘要行

## 目录与命名

- [ ] 页面在 `views/<module>/<page-dir>/`，**path `/<module>/<page-dir>` 与目录一一对应**
- [ ] 模块路由 `views/<module>/routes.ts`
- [ ] 接口 `services.ts`；类型 `types.ts`
- [ ] 组件 PascalCase + `index.vue`；`components/index.ts` 导出

## types.ts（Vue 3 TS，阻塞）

- [ ] `ProductQuery` / `XxxItem` / `XxxForm` 等在页面 `types.ts`
- [ ] hook、component、utils **不**重复定义页面级 interface
- [ ] `constants.ts` / `utils.ts` 无 type/interface 定义
- [ ] 列表/ facets 使用具名类型，非裸 `any[]`

## 页面类型

- [ ] 类型判定正确（列表 / 表单 / 详情 / 组合 / 复杂页）
- [ ] 列表：HiTable + filter（`.cursor/components/HiTable/`）
- [ ] 表单/详情：逻辑在 `hooks/useXxxForm` 或 `useXxxDetail`（见表单与详情页指南）
- [ ] 复杂页：每区块子组件 + 独立 hook + 独立 loading

## Vue 3 写法

- [ ] `<script setup lang="ts">`
- [ ] **全箭头函数**：`const handleXxx = () => {}`；`export const useXxx = () => {}`；utils/services 同理
- [ ] **标准列表页**主逻辑在 `index.vue`；禁止整页上帝 hook
- [ ] 弹窗 `v-model`；插槽 `#default="{ row }"`
- [ ] `tablePage.scss` / `formPage.scss` 按需引入
- [ ] 单文件建议 ≤800 行；职责可拆时已拆分

## 状态与接口

- [ ] loading / empty / error 三态（见状态与异步数据规范）
- [ ] 无 mock；字段来自接口文档
- [ ] 提交 `submitting` 防重复
- [ ] 入参无 `||` 兜底；出参无 `normalizeRows` 猜字段（见 `接口对接规范.mdc`）
- [ ] 展示空值模板层 `?? '-'`（不用 `||` 当 0 为合法值）

## 路由与权限

- [ ] 已按 [route-permission](../route-permission/SKILL.md) 注册本地 `routes.ts`；**path 与 `views/<module>/<page-dir>/` 对应**
- [ ] `meta.title`；详情子页 `activeMenu`（若需要）
- [ ] 交付「待后端配置菜单」path；**未**添加 meta 权限码 / 按钮 `v-permission`

## 代码质量

- [ ] `@/` alias；scoped SCSS；`:deep()`
- [ ] 无 console.log；英文命名

## 功能完整性

- [ ] 主流程可跑通或 TODO 明确
- [ ] 筛选/列表/表单/弹窗与需求一致

## Vue 2 兼容（仅 vue@2.x）

> 完整规范见 `Vue2代码生成指南.mdc`（替代 Vue 3 专用表单/复杂页/状态 rules）。

### 目录与文件

- [ ] 页面在 `views/<module>/<page-dir>/`，**path 与目录一一对应**
- [ ] 模块路由 `views/<module>/routes.js`
- [ ] 接口 `services.js`；常量 `constants.js`
- [ ] 组件 PascalCase + `index.vue`；`components/index.js` 导出
- [ ] **未**使用 `services.ts` / `hooks/` / Pinia（除非项目本身混用）

### 写法

- [ ] Options API：`export default { data, methods, ... }`
- [ ] 方法 `handleXxx`；新 services：`export const GetXxx = (data) => ...`
- [ ] 列表：`HiTable-vue2/` 语法，`slot-scope`、`slot="toolbar"`
- [ ] 文字按钮 `type="text"`；弹窗 `:visible.sync`
- [ ] 样式 `~styles/tablePage.scss` / `formPage.scss`；深度 `::v-deep`
- [ ] 未混用 `<script setup>`、Element Plus、`#default` 插槽

### 页面类型

- [ ] 列表：HiTable + filter
- [ ] 表单/详情：逻辑在 `methods` 或 `mixins/`，非 hooks
- [ ] 复杂页：子组件 + 各区块独立 `loading` in `data`
- [ ] 状态：页面 `data`；跨模块用 Vuex，非 Pinia

### 状态与接口

- [ ] loading / empty / error 三态
- [ ] 无 mock；JSDoc 或注释标注字段
- [ ] 提交 `submitting` 防重复
- [ ] 入参/出参见 `接口对接规范.mdc`；展示空值 `?? '-'`

### 路由与权限

- [ ] `routes.js` 已注册；`meta.title`；交付待后端菜单 path
- [ ] **未**添加前端页面/按钮权限码
