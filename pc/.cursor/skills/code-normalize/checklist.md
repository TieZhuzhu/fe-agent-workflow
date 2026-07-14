# code-normalize 全量规范审计清单

> **用途：** `code-normalize` ② 审计 与 ⑥ 验收 的权威清单。与 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md) 对齐，并补充「优化任务」特有项。
>
> **原则：** 凡本清单 **阻塞项** 未通过，不得声称「已按规范优化」。非阻塞项列入「建议优化」并在交付中说明。

---

## 如何使用

1. 判定页面类型（列表 / 表单 / 详情 / 组合 / 复杂）
2. 按 **§通用** + 对应 **§页面类型** 逐项审计目标目录
3. 改码后 **同一清单** 复验；全部阻塞项打勾方可交付

**阻塞 / 建议：**

| 标记 | 含义 |
|------|------|
| 🔴 | 阻塞 — 必须在本轮修复 |
| 🟡 | 建议 — 可记 TODO，用户未要求大范围重构时可暂不修 |
| ⚪ | 仅记录 — 与业务/产品相关，优化任务不改 |

---

## §通用（所有页面）

### 规范预加载 🔴

- [ ] 已 Read `shared/rules-activation.md` 通用基线
- [ ] 已 Read 页面类型对应 rules（见 rules-activation §按页面类型追加）
- [ ] 已 Read `TypeScript与types规范.mdc`
- [ ] 已 Read `接口对接规范.mdc`（联调 / 入参 / 出参）
- [ ] 已 Read 目标页 + 同模块参照页
- [ ] `request` import 与同模块 `services` 一致
- [ ] 交付含「规范预加载」汇报行

### 目录与命名 🔴

- [ ] `views/<module>/<page-dir>/`，kebab-case
- [ ] 接口 `services.ts`（或同模块既有约定路径）；类型 `types.ts`
- [ ] `constants.js` / `utils.js` 分离；constants 内无工具函数 🔴
- [ ] 组件 PascalCase + `index.vue`；`components/index.ts` 导出（若有子组件）
- [ ] 英文命名，无拼音 key / 变量名
- [ ] `@/` alias，无深层相对路径

### types.ts（Vue 3 TS）🔴

- [ ] Query / Item / Form / DTO 在 `types.ts`
- [ ] hook / component / utils **不**重复定义页面级 interface
- [ ] `constants.ts` / `utils.ts` 无 type/interface
- [ ] `utils.ts` 无 lodash-es 可替代的自定义数据处理函数 🔴
- [ ] 无裸 `any[]` / `row: any`（或 `// TODO:` 标注）
- [ ] 未新建混放 options + 工具函数的文件；遗留文件已拆 constants + utils
- [ ] 入参无兜底；出参无过度 normalize（见 `接口对接规范.mdc`）🔴

### Vue 写法 🔴

- [ ] `<script setup lang="ts">`（Vue 3）
- [ ] 交互 `const handleXxx = () => {}`；composable `export const useXxx = () => {}`
- [ ] services 导出 `export const GetXxx = (data) => ...` 箭头函数
- [ ] 文字按钮 `type="primary" link`（Vue 3）
- [ ] 弹窗 `v-model`；表格插槽 `#default="{ row }"`
- [ ] 未混用 Vue 2 写法（Options API、`:visible.sync` 等）

### 样式 🔴 / 🟡

- [ ] scoped SCSS；深度选择 `:deep()` 🔴
- [ ] 列表/表单页按需引入 `tablePage.scss` / `formPage.scss` 🟡（同模块已引入则对齐）

### 代码质量 🔴

- [ ] 无 `console.log`、dead code、注释掉的废弃代码
- [ ] 无未使用 `import` / 变量；`npm run lint-fix` 零 error 🔴
- [ ] 无 `@ts-ignore`（除非有注释说明且用户知晓）
- [ ] 静态不变数据不在 reactive/ref 中
- [ ] 单文件 >800 行且职责混杂 → 交付中建议 `page-refactor` 🟡

### 状态与接口 🔴 / 🟡

- [ ] loading 态有处理 🔴
- [ ] empty / error 三态符合 `状态与异步数据规范` 🟡（缺失则补或 TODO）
- [ ] 无 mock 硬编码数据 🔴
- [ ] 提交类操作有 `submitting` 防重复 🟡
- [ ] 展示空值 `|| '-'` 一层兜底 🟡

### 路由与权限 🟡

- [ ] `routes.ts` 已注册；`meta.title` + 权限字段（或 TODO）
- [ ] 按钮权限与项目既有方式一致

### 组件层级 🔴

- [ ] 单页组件在 `views/.../components/`
- [ ] 同模块多页复用在 `views/<module>/components/`
- [ ] 跨模块复用才在顶层 `components/`（误放须指出或迁移 🟡）
- [ ] 纯逻辑在 `hooks/` / `utils/`，非空壳 `.vue`

### 功能行为 ⚪

- [ ] 筛选/列表/表单/弹窗与优化前行为一致（**优化任务不改产品逻辑**）

---

## §列表页 / 组合页

追加 Read：`JavaScript通用`、`HTML与CSS`、`路由与权限规范`

- [ ] HiTable + `el-table-column`（`.cursor/components/HiTable/`）🔴
- [ ] 筛选区 inline form + handleSearch / handleClear 🔴
- [ ] **标准列表**：query、loadList、handlers 在 `index.vue`；**禁止**整页 `useXxxManage` 上帝 hook 🔴
- [ ] 组合页弹窗在 `components/EditDialog`；复杂表单才抽 `useXxxForm` 🟡

---

## §表单页 / 详情页

追加 Read：`表单与详情页开发指南`、`状态与异步数据规范`；高级控件 + `高级表单控件开发指南`

- [ ] 逻辑在 `hooks/useXxxForm` / `useXxxDetail` 🔴
- [ ] 表单校验、提交、重置符合表单指南 🔴
- [ ] 详情只读分组清晰 🟡
- [ ] 高级控件（上传、富文本等）符合高级表单指南 🟡

---

## §复杂页

追加 Read：`复杂页面开发指南`、`状态与异步数据规范`

- [ ] 每区块独立子组件 + hook + loading 🔴
- [ ] index 仅编排，无大块业务 script 🔴
- [ ] Tab/双栏/工作台结构符合复杂页指南 🟡

---

## §Vue 2（vue@^2.x 时）

不 Read Vue 3 专用表单/复杂页/状态 rules；以 `Vue2代码生成指南.mdc` + reference-checklist §Vue 2 为准。

- [ ] Options API；`services.js`；HiTable-vue2 语法 🔴
- [ ] 未引入 `<script setup>` / Pinia / 页面 `services.ts` 🔴

---

## 交付自检（rules-activation §质量红灯）

改码后必须过 [rules-activation §质量红灯](../shared/rules-activation.md) 全部项，否则视为流程失败。

---

## 审计输出模板

```markdown
## 规范审计（code-normalize）
- 页面：views/xxx/yyy
- 类型：列表页
- 阻塞违规：N 项
- 建议项：M 项

### 阻塞项
1. [文件:行] 问题 — 修复方式

### 建议项
1. ...

### 不改项（行为/产品）
- ...
```
