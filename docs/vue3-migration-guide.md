# Vue2 → Vue3 全项目迁移 SDD 指南（vue3-migration）

> **适用：** PC 中后台 + uni-app 移动端  
> **固定 slug：** `vue3-migration`（与 `project-refactor` 互斥，不可混在同一 feature）  
> **Skill 链：** `feature-spec` → `feature-analyze` → `vue2-to-vue3-refactor` → `feature-verify` → `feature-finish` → `feature-archive`

---

## 与 project-refactor 的关系

| 场景 | slug | Skill |
|------|------|-------|
| **同版本**全项目规范对齐（Vue2 保 Vue2 / Vue3 保 Vue3） | `project-refactor` | `rules-refactor` |
| **技术栈升级** Vue2 → Vue3 | `vue3-migration` | `vue2-to-vue3-refactor` |

二者均需 SDD 工件 + inventory + verify，**不可省略**。

若项目需「先升 Vue3 再规范整理」，默认 **先 `vue3-migration` 完成并 verify**，再视情况启动新的 `project-refactor`（Vue3 保 Vue3）。

---

## 目录结构（业务项目）

```
docs/features/vue3-migration/
├── proposal.md      # 升级目标、依赖 major、回滚策略
├── spec.md          # 业务回归 + Vue3 技术验收场景
├── design.md        # 迁移映射表（Vuex→Pinia、UI 库、目录）
├── tasks.md         # 分阶段：依赖 → 基础设施 → 按模块 views/pages
├── field-map.md     # N/A（不改接口）
├── e2e.md           # P0 冒烟（升级后全链路）
└── status.yaml

docs/vue3-migration-inventory.md   # 逐模块迁移进度（与 rules-refactor inventory 同构）
```

模板：各平台 `docs/features/_template/vue3-migration/`。

---

## 标准流程

```
① 【spec】propose vue3-migration
② 【analyze】vue3-migration → ready
③ 【vue3】vue2-to-vue3-refactor — 按 tasks 执行
④ 每批：改码 → lint/build/vue-tsc → 更新 inventory + tasks
⑤ 【verify】vue3-migration — 业务场景 + Vue3 专用项全通过
⑥ 【finish】→ 【archive】
```

**禁止：** 无 `docs/features/vue3-migration/` ready 时直接全项目改 script setup。

---

## install 行为

`install.sh --with-docs` **不同步**业务仓已有 `docs/features/vue3-migration/`，同步 `_template/vue3-migration/` 模板。
