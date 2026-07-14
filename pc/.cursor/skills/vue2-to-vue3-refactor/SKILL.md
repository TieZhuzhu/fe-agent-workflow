---
name: vue2-to-vue3-refactor
version: 1.2.0
description: 将 Vue2 项目迁移至 Vue3（Composition API、Pinia、Element Plus），功能不变。须先 docs/features/vue3-migration/ ready，收尾【verify】vue3-migration。用户说 Vue2 升 Vue3、迁移 Vue3、upgrade vue3 时触发。
---
# Vue2 → Vue3 全项目升级重构

> **管控力度：** 严 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **前置：** 用户**明确**要求升 Vue3。若仅「按规范整理、不升栈」→ `rules-refactor` + `project-refactor`（保持 Vue2）。  
> **计划与回归：** `docs/features/vue3-migration/`（**强制**，固定 slug）。  
> **进度：** `docs/vue3-migration-inventory.md`。  
> **权威写法：** `.cursor/rules`（Vue3：`Vue代码生成指南.mdc` 等）。

---

## ⓪ SDD 门禁（强制）

| 条件 | 动作 |
|------|------|
| 无 `docs/features/vue3-migration/` | `【spec】propose vue3-migration`，复制 `docs/features/_template/vue3-migration/` |
| draft | 补全工件，`【analyze】vue3-migration` → ready |
| ready | 进入迁移流程 |

详见 [`docs/vue3-migration-guide.md`](../../../docs/vue3-migration-guide.md)。

**与 `project-refactor` 互斥：** 本 Skill 负责 **Vue major 升级**；同版本规范整理用 `project-refactor`，不可混在同一 feature。

---

## 升级范围（典型）

| 项 | Vue2 存量 | Vue3 目标 |
|----|-----------|-----------|
| SFC | Options API | `<script setup lang="ts">` |
| 状态 | Vuex | Pinia（或项目约定） |
| UI | element-ui | element-plus |
| 列表 | HiTable-vue2 | `.cursor/components/HiTable/` |
| 接口 | services.js | services.ts + types.ts |

**功能、路由 path、接口 URL 不变。**

---

## 流程

```
⓪ vue3-migration spec ready
① 预加载 rules + Read docs/features/vue3-migration/
② 盘点 → docs/vue3-migration-inventory.md（同步 tasks.md）
③ 依赖升级（package.json；major 风险可在 spec 阶段确认一次）
④ 基础设施：request、HiTable、router、Pinia
⑤ 按模块迁移 views（P1 列表 → P2 表单详情 → P3 复杂页）
⑥ 每批 lint/build/vue-tsc + 更新 inventory + tasks
⑦ 【verify】vue3-migration PASS
```

**除依赖 major 在 spec 阶段外，不向用户逐步确认。**

---

## Vue3 专用验收（追加 🔴）

- [ ] 无 Options API 残留
- [ ] 页面级 `types.ts`
- [ ] composable / utils / services 全箭头函数
- [ ] Element Plus 已替换 element-ui
- [ ] Pinia 符合约定
- [ ] `【verify】vue3-migration` PASS

详见 [code-normalize/checklist.md](../code-normalize/checklist.md) §Vue 3。

---

## 与 rules-refactor 关系

| 场景 | slug | Skill |
|------|------|-------|
| Vue2 整理规范，不升栈 | `project-refactor` | `rules-refactor` |
| Vue2 → Vue3 | `vue3-migration` | **本 Skill** |
| 单页 Vue3 对齐 | — | `code-normalize` |

---

## 禁止

- 无 vue3-migration spec 直接全项目迁移
- verify 未 PASS 声称完成
- 同文件 Vue2/Vue3 混用
- 改业务行为 / 接口契约

---

## 触发话术

```
【spec】propose vue3-migration。全项目 Vue2 升 Vue3，功能不变
【analyze】vue3-migration
【vue3】按 vue3-migration tasks 执行，中途别问我
【verify】vue3-migration
```

## 交付检查

- [ ] inventory 全部 ✅
- [ ] lint/build/vue-tsc 通过
- [ ] verify PASS
