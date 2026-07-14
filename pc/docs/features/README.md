# Feature Spec（SDD 轻量层）

每个**新建页 / 多文件功能**在编码前建立独立目录，作为跨会话、可评审的规格工件。

## 目录结构

```
docs/features/<feature-slug>/
├── proposal.md    # 为什么做、范围、不做什么
├── spec.md        # 需求与验收场景
├── design.md      # 技术方案：path、文件清单、接口、布局
├── tasks.md       # 可勾选实现任务
├── field-map.md   # 接口字段 ↔ UI（有联调时必填）
└── e2e.md         # P0 浏览器冒烟（可选；建议 P0 新建页填写）
```

`<feature-slug>`：kebab-case，如 `product-tag-list`。

## 生命周期

```
feature-spec（propose）→ feature-dev-workflow（apply）→ feature-verify（L1）
  → api-smoke（L2，可选）→ feature-e2e-verify（L3，可选）→ feature-archive
```

| 阶段 | 话术 | Skill |
|------|------|-------|
| 提案 | `【spec】propose product-tag-list` | `feature-spec` |
| 实现 | `【新建】…` | `feature-dev-workflow` |
| 静态验收 | `【verify】product-tag-list` | `feature-verify` |
| 接口探针 | `【api-smoke】product-tag-list` | `api-smoke` |
| UI 冒烟 | `【verify-e2e】product-tag-list` | `feature-e2e-verify` |
| 归档 | `【archive】product-tag-list` | `feature-archive` |

验收分层说明见 [docs/testing/README.md](../testing/README.md)。

## 何时可省略

| 场景 | 省略 feature 目录 |
|------|-------------------|
| 单文件加列 / 加筛选项 | 是 |
| 修 bug | 是 |
| **单页**规范优化（`code-normalize`） | 是 |
| **全项目**规范重构（`rules-refactor`） | **否 — 必须用 `project-refactor`** |
| e2e.md | trivial 增量可省略 |

## 全项目重构（固定 slug）

**Slug：** `project-refactor`（不可改名）

```
【spec】propose project-refactor → 【analyze】project-refactor → 【重构】… → 【verify】project-refactor
```

| 工件 | 职责 |
|------|------|
| `docs/features/project-refactor/` | 计划、业务回归 spec、分阶段 tasks |
| `docs/project-refactor-inventory.md` | rules 合规逐模块进度 |

模板：[`_template/project-refactor/`](./_template/project-refactor/) · 说明：`docs/project-refactor-guide.md`

## Vue2 → Vue3 全项目迁移（固定 slug）

**Slug：** `vue3-migration`（与 `project-refactor` **互斥**）

```
【spec】propose vue3-migration → 【analyze】 → 【vue3】… → 【verify】vue3-migration
```

| 工件 | 职责 |
|------|------|
| `docs/features/vue3-migration/` | 升级计划、依赖、业务回归 |
| `docs/vue3-migration-inventory.md` | 逐模块迁移进度 |

模板：[`_template/vue3-migration/`](./_template/vue3-migration/) · 说明：`docs/vue3-migration-guide.md`

## 模板

复制 [`_template/`](./_template/) 下文件到新目录后填写；全项目重构复制 [`_template/project-refactor/`](./_template/project-refactor/)。
