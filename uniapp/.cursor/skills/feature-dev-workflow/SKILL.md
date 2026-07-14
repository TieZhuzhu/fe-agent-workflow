---
name: feature-dev-workflow
version: 1.1.1
description: uni-app 功能从零开发主工作流。串联需求理解、方案对齐、写码与验收。 用户说【新建】、按 PRD/Figma/原型开发新页面时触发；已有页增量见 incremental-feature。
---
# 功能开发主工作流

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

## 输入识别

根据用户提供的材料，选择对应子流程：

| 输入特征 | 子 Skill | 典型材料 |
|----------|----------|----------|
| **语雀 / 飞书 Markdown PRD** | [prd-markdown-ingest](../prd-markdown-ingest/SKILL.md) → [prd-feature-dev](../prd-feature-dev/SKILL.md) | 语雀「复制为 Markdown」粘贴 |
| PRD 文案、截图、接口文档 | [prd-feature-dev](../prd-feature-dev/SKILL.md) | Word/Markdown PRD、原型截图、Swagger |
| **远程 Axure / HTML 原型站 URL** | [prototype-html-feature-dev](../prototype-html-feature-dev/SKILL.md) §远程原型站 | `index.html#页面.html` 导航壳 |
| 本地静态 HTML 原型 | [prototype-html-feature-dev](../prototype-html-feature-dev/SKILL.md) §本地原型 | `.html` 文件 + PRD + 接口 |
| Figma 设计链接 | [figma-feature-dev](../figma-feature-dev/SKILL.md) | `figma.com/design/...` URL |

**多种材料同时存在**：UI 结构来源优先级 — Figma > 原型 HTML（含 page-spec-panel）> PRD 截图/文案；业务规则与接口以 PRD/接口文档为准。语雀 PRD + 原型站可并行：`prd-markdown-ingest` 与 `prototype-html-feature-dev` 各产出 digest，阶段 ② 合并。

**含 JS 交互的原型**（选券、开票、弹层、跨页）：`prototype-html-feature-dev` §F — **curl+JS 批量 ingest**，**Browser MCP 实点 P0** 写入 `e2e.md`；不可仅用 curl 默认态 HTML。

**复杂需求**：可选 [spec-research-clarify](../spec-research-clarify/SKILL.md)

**Skill 路由**（Agent 须按用户意图自动选用，勿等用户点名文件名）：

| 用户意图 | Skill |
|----------|-------|
| 从零新建页面（PRD / Figma / 原型 / 截图） | 本 Skill → 对应子 Skill |
| **已有页面加字段 / 加列 / 加按钮** | [incremental-feature](../incremental-feature/SKILL.md) |
| 接口文档到了 / 联调对字段 | [api-integration](../api-integration/SKILL.md) |
| 修 Bug / 报错排查 | [bugfix-workflow](../bugfix-workflow/SKILL.md) |
| 拆分大文件 / 重构页面 | [page-refactor](../page-refactor/SKILL.md) |
| 提交前规范审查 | [code-review](../code-review/SKILL.md) |
| 新页本地路由 | [route-permission](../route-permission/SKILL.md) |
| build / test 失败 | [ci-fix](../ci-fix/SKILL.md) |
| 用户明确要求写单测 | [unit-test-codegen](../unit-test-codegen/SKILL.md) |
| **先写 spec / 提案** | [feature-spec](../feature-spec/SKILL.md) |
| **验收 feature / 对照 spec** | [feature-verify](../feature-verify/SKILL.md) |
| **归档 feature / 合并 spec** | [feature-archive](../feature-archive/SKILL.md) |

---

## 统一流程（SDD + 四阶段）

```
⓪ feature-spec（新建且非 trivial）→ ⓪b feature-analyze（ready 门禁）
→ ① 理解 → ② 对齐 → ③ 写码 → ④ 验收 → feature-verify → feature-finish → feature-archive
```

简单增量 / 明确小改可跳过 ⓪，直接 ①～④。

### 阶段 ⓪ Feature Spec（新建默认）

**触发：** 新建页、多文件、多接口、复杂页。

1. 执行 [feature-spec](../feature-spec/SKILL.md)，产出 `docs/features/<slug>/`
2. 执行 [feature-analyze](../feature-analyze/SKILL.md)，`feature-check analyze` **PASS** 后 `proposal.md` 为 `Status: ready`
3. 阶段 ①② 可从 feature 工件读取，避免重复劳动

**跳过 ⓪：** 用户明确「直接写码」且 scope 为单页 trivial；或 [incremental-feature](../incremental-feature/SKILL.md) 场景。

---

## 统一流程（四阶段）

```
① 理解需求 → ② 方案对齐 → ③ 生成代码 → ④ 规范验收
```

### 阶段 ① 理解需求

0. 若存在 `docs/features/<slug>/`，**优先 Read** proposal + spec + design，本阶段可输出摘要即可
1. 若无 `.cursor/project-conventions.md`，先执行 [project-bootstrap](../project-bootstrap/SKILL.md)
2. 按子 Skill 提取：页面类型、布局、字段、交互、接口、状态
3. 读取 `package.json` 判定 Vue 2 / Vue 3，**禁止混用**
4. **判定页面类型**（关键）：

| 类型 | 特征 | 参考 |
|------|------|------|
| 列表页 | 下拉刷新 + 分页列表 | uniapp代码生成指南 §列表 |
| 表单页 | 多字段录入 + 提交 | uniapp代码生成指南 §表单 |
| 详情页 | 只读信息展示 | uniapp代码生成指南 §详情 |
| 组合页 | 列表 + 底部栏/弹层 | uniapp指南 |
| 复杂页 | 多 Tab / 多区块 | 先输出拆分清单 |

5. 搜索同子包已有页面，对齐写法
7. 信息冲突：**PRD/接口文案 > 设计稿/截图 > 推断**

输出简要 **需求摘要**（页面类型、模块路径、核心字段、接口列表、待确认项）。

### 阶段 ② 方案对齐

若 ⓪ 已产出 feature 目录：**以 `design.md` + `tasks.md` 为准**，补充缺失项即可。

信息不足时先提问，**不要猜测**以下关键项：

- 页面所属子包与 `pages.json` path
- 是否 tabBar 页（决定主包/分包）
- 接口 URL / 入参 / 出参字段（无文档则明确标注 TODO）
- 页面类型（列表 / 表单 / 详情 / 组合 / **复杂页**）
- 弹窗/抽屉是独立路由还是页面内组件
- 新页面 path；须注册 `pages.json`（交付 TODO 即可）

**进入阶段 ③ 前**须：

1. 输出 rules-activation §预加载计划
2. **新建页：** design.md + tasks.md 已存在（或用户显式跳过 ⓪）

**标准页（分包，默认）：**

```
subPackages/<module>/<page-dir>/
├── index.vue
├── services.js / services.ts
├── types.ts            # Vue3 TS 按需
├── constants.js        # 按需
└── components/         # 按需
```

**tabBar 页（主包）：**

```
pages/<module>/<page>.vue
```

**路由注册：** 阶段 ③ 后执行 [route-permission](../route-permission/SKILL.md)，注册 `pages.json`。

### 阶段 ③ 生成代码

**执行**阶段 ② 已输出的预加载计划：Read [rules-activation](../shared/rules-activation.md) 列出的全部文件 + [vue-page-codegen](../vue-page-codegen/SKILL.md)。

实现过程中**同步勾选** `docs/features/<slug>/tasks.md`（若有）。

关键约束见 vue-page-codegen；`vue@2.x` 时 **不 Read** Vue 3 专用 rules（见 rules-activation §Vue 2）。

### 阶段 ④ 规范验收

1. 执行 [reference-checklist.md](reference-checklist.md) 全部检查项
2. **新建 feature：** 执行 [feature-verify](../feature-verify/SKILL.md)，PASS 后再交付
3. 用户要求上线归档 → [feature-archive](../feature-archive/SKILL.md)

---

## 子 Skill 调用

| 阶段 | PRD / 语雀 Markdown | Figma | 原型 HTML（本地 / 远程站） |
|------|---------------------|-------|---------------------------|
| ① | prd-markdown-ingest（语雀）→ prd-feature-dev §需求提取 | figma-feature-dev §设计解析 | prototype-html-feature-dev §远程站 / §本地 |
| ② | 共用本文件 §方案对齐 | 共用 | 共用 |
| ③ | vue-page-codegen | vue-page-codegen | vue-page-codegen |
| ④ | reference-checklist | reference-checklist | reference-checklist |

---

## 交付说明

完成后简要汇报：

1. 新增/修改的文件列表
2. Feature spec 路径（若有）：`docs/features/<slug>/`
3. `pages.json` 注册 path、`navigationBarTitleText`
4. 对接的接口与字段映射（或 `field-map.md` 链接）
5. 页面类型与拆分说明（复杂页需说明各子组件职责）
6. feature-verify 结果（PASS/FAIL）
7. 待用户确认或后端未就绪的 TODO
