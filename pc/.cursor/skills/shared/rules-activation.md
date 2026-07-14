# 规范预加载清单（强制）

> **任何涉及写码的 Skill 在执行前必须先完成本节对应清单。** 使用 Read 工具读取列出的 rules/skills 文件，未读取不得生成或修改代码。

## 写码前门禁（所有场景）

### Step 0：项目约定

1. 若存在 `.cursor/project-conventions.md`，**必须先 Read**（仅对齐 request 路径、布局组件等**扫描项**）
2. 若不存在 → 先执行 [project-bootstrap](../project-bootstrap/SKILL.md)，**再写码**
3. 依赖栈 major 升级后 → 用户说「重新扫描项目约定」更新 conventions
4. **权限、路由、接口对接、目录命名等规范**以 `.cursor/rules` 为准；**conventions 不得覆盖 rules**；全项目重构见 `rules-refactor`

### Step 1：输出预加载计划（复杂任务必做）

**新建页 / 跨模块组件 / 复杂页 / 多文件改动**时，**Read 任何业务代码之前**，先向用户输出：

```markdown
## 预加载计划
- 场景词：新建 | 增量 | 联调 | 优化 | vue2 | ...
- 选用 Skill：feature-dev-workflow / incremental-feature / ...
- 将 Read：
  1. shared/rules-activation.md
  2. ...
- 不 Read：代码规范示例参考.mdc（仅查阅）
```

简单任务（单文件小改、bugfix、明确增量）可**省略** Step 1 预加载计划，但仍须完成 Step 2 基线 Read。

### Step 2：通用基线 Read

| 顺序 | 文件 | 说明 |
|------|------|------|
| 1 | `.cursor/rules/前端通用代码规范.mdc` | Always Apply，仍须确认 |
| 2 | `.cursor/rules/项目结构与命名规范.mdc` | 目录与命名 |
| 2b | `.cursor/rules/TypeScript与types规范.mdc` | **Vue 3 + TS 写码必做**（types 就近原则） |
| 2c | `.cursor/rules/接口对接规范.mdc` | **联调 / services / 入参出参必做** |
| 3 | `.cursor/rules/Vue代码生成指南.mdc` | 版本判定 |
| 3b | `.cursor/rules/Vue2代码生成指南.mdc` | **vue@2.x 时**替代 Vue 3 专用表单/复杂页/状态 rules |

**写码前额外必做：**

3. 读取目标页面目录及同模块已有页面，对齐现有写法
4. 搜索 `services.ts` / `services.js` 的 request import，**以项目/conventions 为准**
5. 读取 `package.json` 判定 Vue 2 / Vue 3

---

## 禁止预加载（仅查阅）

| 文件 | 说明 |
|------|------|
| `.cursor/rules/代码规范示例参考.mdc` | 427 行示例库；**仅**在不确定写法时按需查阅，**不得**列入预加载计划 |
| `shared-component/reference.md` | 公共组件示例；实现复杂组件时按需 Read |
| `feature-dev-workflow/reference-checklist.md` | 阶段 ④ / **code-normalize ⑥ 验收** 时 Read |

---

## 按页面类型追加（阶段 ③ / vue-page-codegen 必做）

### Vue 3（默认）

| 页面类型 | 追加 Read |
|----------|-----------|
| 列表页 / 组合页 | `JavaScript通用代码生成指南.mdc`、`HTML与CSS代码生成指南.mdc`、`路由与权限规范.mdc` |
| 表单页 / 详情页 | 上表 + `表单与详情页开发指南.mdc`、`状态与异步数据规范.mdc`；含高级控件 + `高级表单控件开发指南.mdc` |
| 复杂页 | 上表 + `复杂页面开发指南.mdc`、`状态与异步数据规范.mdc` |

### Vue 2（vue@^2.x）

| 页面类型 | 追加 Read |
|----------|-----------|
| 列表页 / 组合页 | `JavaScript通用代码生成指南.mdc`、`HTML与CSS代码生成指南.mdc`、`路由与权限规范.mdc`、`Vue2代码生成指南.mdc` |
| 表单页 / 详情页 | 列表页追加 + `Vue2代码生成指南.mdc` §表单；高级控件见 `高级表单控件开发指南.mdc` §Vue 2 |
| 复杂页 | 列表页追加 + `Vue2代码生成指南.mdc` §复杂页、§状态 |

**Vue 2 不 Read：** `表单与详情页开发指南.mdc`、`复杂页面开发指南.mdc`、`状态与异步数据规范.mdc`。

---

## 按 Skill 追加

| Skill | 追加 Read |
|-------|-----------|
| `feature-spec` | Read `docs/constitution.md` + [feature-spec/SKILL.md](../feature-spec/SKILL.md) + `docs/features/_template/` |
| `feature-analyze` | Read feature 目录 + [feature-analyze/SKILL.md](../feature-analyze/SKILL.md) |
| `feature-verify` | Read feature 目录 + [feature-verify/SKILL.md](../feature-verify/SKILL.md) + `reference-checklist.md` |
| `feature-finish` | Read feature 目录 + [feature-finish/SKILL.md](../feature-finish/SKILL.md) |
| `api-smoke` | [api-smoke/SKILL.md](../api-smoke/SKILL.md) + `接口对接规范.mdc` + feature `field-map.md` |
| `feature-e2e-verify` | [feature-e2e-verify/SKILL.md](../feature-e2e-verify/SKILL.md) + feature `e2e.md` |
| `unit-test-codegen` | [unit-test-codegen/SKILL.md](../unit-test-codegen/SKILL.md) + `package.json` scripts |
| `feature-archive` | Read feature 目录 + [feature-archive/SKILL.md](../feature-archive/SKILL.md) + `docs/specs/README.md` |
| `feature-dev-workflow` ③ | 本文件 + 页面类型 rules + `vue-page-codegen/SKILL.md`；**若有** `docs/features/<slug>/` 须 Read design + tasks |
| `vue-page-codegen` | 本文件 + 页面类型 rules |
| `incremental-feature` | 本文件 + `TypeScript与types规范.mdc` + **`接口对接规范.mdc`**（涉及接口时）+ `incremental-feature/SKILL.md`；加字段须同步 `types.ts` |
| `api-integration` | 本文件 + `TypeScript与types规范.mdc` + **`接口对接规范.mdc`** + `api-integration/SKILL.md` |
| `openapi-api-integration` | 上表 + **[openapi-api-integration/SKILL.md](openapi-api-integration/SKILL.md)** + `reference.md` |
| `page-refactor` | 本文件 + `TypeScript与types规范.mdc` + 原页面类型 rules |
| `code-normalize` | 本文件 + **页面类型 rules（全量）** + `TypeScript与types规范.mdc` + **`接口对接规范.mdc`** + `code-normalize/SKILL.md`；验收 Read `code-normalize/checklist.md` + `reference-checklist.md` |
| `code-review` | 本文件 + `TypeScript与types规范.mdc` + `code-review/SKILL.md` |
| `bugfix-workflow` | 至少通用基线；涉及表单/路由时再读对应 rule；**可省略**预加载计划 |
| `route-permission` | Read `路由与权限规范.mdc` + [route-permission/SKILL.md](../route-permission/SKILL.md) |
| `ci-fix` | Read `package.json` scripts；改业务代码时补通用基线；[ci-fix/SKILL.md](../ci-fix/SKILL.md) |
| `project-bootstrap` | 本 Skill；产出 `project-conventions.md`（**扫描快照，非重构标准**） |
| `rules-refactor` | 本文件 + **全部** `.cursor/rules/*.mdc` + [rules-refactor/SKILL.md](../rules-refactor/SKILL.md) + `checklist-project.md` + `code-normalize/checklist.md` → 完成后 [lint-check](../lint-check/SKILL.md) |
| `code-normalize` | 本文件 + 页面类型 rules + [code-normalize/SKILL.md](../code-normalize/SKILL.md) → 完成后 [lint-check](../lint-check/SKILL.md) |
| `vue2-to-vue3-refactor` | 上表 + [vue2-to-vue3-refactor/SKILL.md](../vue2-to-vue3-refactor/SKILL.md) + `rules-refactor` 闭环 |
| `figma-feature-dev` | 本文件 + 页面类型 + `figma-feature-dev/SKILL.md` |
| `shared-component` | 本文件 + `shared-component/SKILL.md`；复杂实现按需 `reference.md` |

---

## 配置约定（全文统一）

> **权威来源：** 本表与 `前端通用代码规范.mdc` §配置约定 保持一致；request 实际路径以 `project-conventions.md` 为准。

| 项 | Vue 3（默认） | Vue 2 |
|----|---------------|-------|
| request | 以 conventions / 项目 services 为准 | 同左 |
| services 导出 | `export const GetXxx = (data) => ...` | 同左（`.js`） |
| services 位置 | 页面 `./services.ts`；组件 `components/<Name>/services.ts`；全局 **`src/services.ts`** | 同左（`.js`） |
| 函数写法 | **箭头函数**（含 composable、utils、services） | services 箭头；methods Options API |
| 文字按钮 | `type="primary" link` | `type="text"` |
| 接口文件 | `services.ts` | `services.js` |
| 公共组件目录 | `components/<Name>/index.vue` | 同左 |

---

## 激活汇报（写码后交付首行）

```
规范预加载：Vue 3 | 列表页 | Skill incremental-feature | 已读 rules ×5 | request @/config/request
```

须与 Step 1「预加载计划」一致（简单任务省略计划时，汇报中标注「预加载计划：省略」）。

---

## 质量红灯（交付自检）

出现任一项视为流程失败，须修正后再交付：

- [ ] 无「规范预加载」汇报行
- [ ] 预加载计划与实际 Read 不一致
- [ ] Vue 2 项目出现 `<script setup>` / Pinia / 页面 `services.ts`
- [ ] request 路径与 conventions / 项目现有 services 不一致
- [ ] **标准列表页**整页 logic 下沉为上帝 hook（`index.vue` 仅解构）
- [ ] **生成代码使用 `function` / `export function`**（应全箭头函数，见 JS 指南）
- [ ] 同模块多页组件误放顶层 `components/`
- [ ] 纯逻辑封装成空壳 `.vue` 而非 `hooks/`
- [ ] **页面 Query/Item/Form 类型未在 `types.ts`**（仍在 hook / constants / utils / index.vue 内定义）
- [ ] **`constants.ts` / `utils.ts` 含 interface/type 定义**（应迁 `types.ts`）
- [ ] 未新建混放 options 与工具函数的文件
- [ ] **入参兜底 / 出参过度 normalize**（见 `接口对接规范.mdc`）
- [ ] 规范优化/重构后仍大量 `any[]` / `row: any` 且无 TODO
- [ ] 用户要求「全项目按 rules 重构」却未走 `rules-refactor`、**无 `docs/features/project-refactor/` 就改码**、中途询问「是否继续」、或仅以 conventions 为标准
- [ ] 用户要求「升 Vue3」却**无 `docs/features/vue3-migration/`** 或未 `【verify】vue3-migration` 就声称完成
- [ ] **新建页无 feature spec 且用户未声明跳过**（见 `feature-spec`）
- [ ] **新建 feature 交付无 verify 报告**
- [ ] **大批量改码 / 重构后未跑 lint**（有 lint script 时须零 error；见 `lint-check`）
- [ ] **改动文件存在未使用 import / 变量**（须删除，禁止 eslint-disable 糊弄）
