# 规范预加载清单（强制）

> **任何涉及写码的 Skill 在执行前必须先完成本节对应清单。** 使用 Read 工具读取列出的 rules/skills 文件，未读取不得生成或修改代码。

## 写码前门禁（所有场景）

### Step 0：项目约定

1. 若存在 `.cursor/project-conventions.md`，**必须先 Read**（request 路径、接口组织方式、UI 库版本等**扫描项**）
2. 若不存在 → 先执行 [project-bootstrap](../project-bootstrap/SKILL.md)，**再写码**
3. 依赖栈 major 升级后 → 用户说「重新扫描项目约定」更新 conventions
4. **路由分包、接口对接、目录命名等规范**以 `.cursor/rules` 为准；**conventions 不得覆盖 rules**

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

简单任务（单文件小改、bugfix、明确增量）可**省略** Step 1，但仍须完成 Step 2 基线 Read。

### Step 2：通用基线 Read

| 顺序 | 文件 | 说明 |
|------|------|------|
| 1 | `.cursor/rules/前端通用代码规范.mdc` | Always Apply |
| 2 | `.cursor/rules/项目结构与命名规范.mdc` | 目录与命名 |
| 3 | `.cursor/rules/uniapp代码生成指南.mdc` | uni-app 主指南 |
| 3b | `.cursor/rules/Vue2代码生成指南.mdc` | **vue@2.x 时**必做 |
| 3c | `.cursor/rules/Vue代码生成指南.mdc` | **vue@3.x 时**必做 |
| 2b | `.cursor/rules/TypeScript与types规范.mdc` | **Vue 3 + TS 写码必做** |
| 2c | `.cursor/rules/接口对接规范.mdc` | **联调 / services 必做** |

**写码前额外必做：**

1. 读取目标页面目录及同子包已有页面，对齐现有写法
2. 搜索 `service/*.js` 或页面 `services.*` 的 request import，**以 project-conventions 为准**
3. 读取 `package.json` 判定 Vue 2 / Vue 3
4. 读取 `pages.json` 确认主包/分包与子包 root

---

## 禁止预加载（仅查阅）

| 文件 | 说明 |
|------|------|
| `.cursor/rules/代码规范示例参考.mdc` | 示例库；不确定写法时按需查阅 |
| `shared-component/reference.md` | 公共组件示例 |
| `feature-dev-workflow/reference-checklist.md` | 阶段 ④ / code-normalize 验收时 Read |

---

## 按页面类型追加（vue-page-codegen 必做）

| 页面类型 | 追加 Read |
|----------|-----------|
| 列表页 | `JavaScript通用代码生成指南.mdc`、`HTML与CSS代码生成指南.mdc`、`路由与分包规范.mdc` |
| 表单页 / 详情页 | 上表 + 对应 Vue 版本指南 §表单/详情 |
| 复杂页 / 多 Tab | 上表 + `uniapp代码生成指南.mdc` §复杂页 |

---

## 按 Skill 追加

| Skill | 追加 Read |
|-------|-----------|
| `feature-spec` | `docs/constitution.md` + feature-spec SKILL + `docs/features/_template/` |
| `feature-analyze` | feature 目录 + feature-analyze SKILL |
| `feature-finish` | feature 目录 + feature-finish SKILL |
| `feature-verify` | feature 目录 + feature-verify SKILL + reference-checklist |
| `api-smoke` | api-smoke SKILL + `接口对接规范.mdc` + field-map.md |
| `feature-e2e-verify` | feature-e2e-verify SKILL + e2e.md |
| `unit-test-codegen` | unit-test-codegen SKILL + package.json scripts |
| `feature-archive` | feature 目录 + feature-archive SKILL + docs/specs/README.md |
| `feature-dev-workflow` ③ | 本文件 + 页面类型 rules + vue-page-codegen SKILL |
| `vue-page-codegen` | 本文件 + 页面类型 rules |
| `incremental-feature` | 本文件 + TypeScript规范（TS 时）+ 接口对接规范 + incremental-feature SKILL |
| `api-integration` | 本文件 + 接口对接规范 + api-integration SKILL |
| `openapi-api-integration` | 上表 + openapi-api-integration SKILL |
| `page-refactor` | 本文件 + 页面类型 rules |
| `code-normalize` | 本文件 + 页面类型 rules + code-normalize SKILL + checklist.md |
| `code-review` | 本文件 + code-review SKILL |
| `bugfix-workflow` | 至少通用基线 |
| `route-permission` | `路由与分包规范.mdc` + route-permission SKILL |
| `ci-fix` | package.json scripts + ci-fix SKILL |
| `project-bootstrap` | project-bootstrap SKILL |
| `rules-refactor` | 本文件 + **全部** rules + rules-refactor SKILL + checklist |
| `vue2-to-vue3-refactor` | 上表 + vue2-to-vue3-refactor SKILL（uni-app Vue2→3 迁移） |
| `figma-feature-dev` | 本文件 + 页面类型 + figma-feature-dev SKILL |
| `shared-component` | 本文件 + shared-component SKILL |

---

## 配置约定

| 项 | Vue 3 | Vue 2 |
|----|-------|-------|
| request | 以 conventions / 项目为准 | 同左 |
| services 导出 | `export const GetXxx = (data) => ...` | 同左 |
| 接口组织 | 默认页面级；存量集中式沿用 | 同左 |
| 路由 | `pages.json` + subPackages | 同左 |
| 导航 | `uni.navigateTo` / `uni.switchTab` | 同左 |

---

## 激活汇报（写码后交付首行）

```
规范预加载：Vue 2 | uni-app 列表页 | Skill feature-dev-workflow | 已读 rules ×6 | services 页面级（存量见 conventions） | 分包 order
```

---

## 质量红灯

- [ ] 无「规范预加载」汇报行
- [ ] 全项目 `rules-refactor` 无 `project-refactor` 或未 verify 就声称完成
- [ ] 全项目 `vue2-to-vue3-refactor` 无 `vue3-migration` spec 或未 `【verify】vue3-migration` 就声称完成
- [ ] Vue 2 项目出现 script setup / Pinia
- [ ] Vue 3 项目出现 Options API 与 setup 混用
- [ ] 非 tabBar 页放入主包 `pages`
- [ ] 为单页随意新建 subPackage
- [ ] request 路径与 conventions 不一致
- [ ] 入参兜底 / 出参过度 normalize
- [ ] 新建页无 spec 且用户未声明跳过
- [ ] 大批量改码后未跑 lint
