# 全项目重构 SDD 指南（project-refactor）

> **适用：** PC 中后台 + uni-app 移动端  
> **固定 slug：** `project-refactor`  
> **Skill 链：** `feature-spec` → `feature-analyze`（建议）→ `rules-refactor` → `feature-verify` → `feature-finish` → `feature-archive`

---

## 为何全量重构必须走 spec

| 产物 | 职责 |
|------|------|
| `docs/features/project-refactor/` | **计划 + 范围 + 业务回归验收**（防失控） |
| `docs/project-refactor-inventory.md` 或 design §inventory | **逐模块 rules 合规进度** |
| `.cursor/rules` + checklist-project | **写法标准** |

单页 `code-normalize` 可省略 feature spec；**全项目 `rules-refactor` 不可省略**。

**Vue2→Vue3 升级**使用独立 slug **`vue3-migration`**，见 [vue3-migration-guide.md](./vue3-migration-guide.md)（与 `project-refactor` 互斥）。

---

## 目录结构（业务项目）

```
docs/features/project-refactor/
├── proposal.md      # 背景、In/Out Scope、分阶段策略
├── spec.md          # 业务回归验收场景（Given/When/Then）
├── design.md        # 模块优先级、技术约束、inventory 引用
├── tasks.md         # 分阶段勾选（与 inventory 同步）
├── field-map.md     # N/A（不改接口契约）
├── e2e.md           # P0 冒烟路径（强烈建议）
└── status.yaml      # planning → implementing → verifying → done
```

模板：各平台 `docs/features/_template/project-refactor/`。

---

## 标准流程

```
① 【spec】propose project-refactor（或 rules-refactor 检测到缺失则先补 spec）
② 【analyze】project-refactor（CRITICAL=0 → ready）
③ project-bootstrap（若无 conventions）
④ 【重构】rules-refactor — 按 tasks 分阶段改码，更新 inventory
⑤ 每阶段：lint/build + 更新 tasks.md
⑥ 【verify】project-refactor — spec 场景 + tasks 全 [x] + checklist-project 🔴=0
⑦ 【finish】project-refactor → 【archive】移入 docs/features/archive/
```

**禁止：** 无 `docs/features/project-refactor/` 且 status 非 ready 时直接大规模改码。

---

## 与 docs/specs/ 的区别

- `project-refactor`：**本次重构**的计划与回归验收，归档后移入 `docs/features/archive/`
- `docs/specs/<module>/<page>.md`：各页面**现状行为**主 spec，按功能上线逐步补齐，**不是**重构前置条件

---

## install 行为

`tools/install.sh --with-docs` **不同步**业务仓已有的 `docs/features/project-refactor/`（保留项目本地计划），但会同步 `_template/project-refactor/` 模板。
