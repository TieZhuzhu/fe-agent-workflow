---
name: rules-refactor
version: 1.2.0
description: 全项目按 .cursor/rules 规范重构（Vue2 保 Vue2 / Vue3 保 Vue3），功能不变，自主执行至全部合规。须先具备 docs/features/project-refactor/ 再改码；收尾【verify】project-refactor。用户说「全量重构」「按 rules 重构项目」「规范重构」「project refactor」时触发。单页优化用 code-normalize。
---
# 全项目 Rules 规范重构

> **唯一权威（写法）：** `.cursor/rules/*.mdc` + 本 Skill 附属 checklist。  
> **唯一权威（计划与业务回归）：** `docs/features/project-refactor/`（**强制**）。  
> **合规进度：** `docs/project-refactor-inventory.md`。  
> **非权威：** `project-conventions.md` 仅为 bootstrap 扫描快照。  
> **目标：** 业务行为不变，全部业务代码符合 rules；中途不向用户确认是否继续下一模块。

---

## 与现有 Skill 边界

| Skill | 范围 | spec 要求 |
|-------|------|-----------|
| **rules-refactor（本 Skill）** | 整个项目 | **必须** `docs/features/project-refactor/` ready |
| `code-normalize` | 单页 / 单模块 | **省略** feature spec |
| `feature-spec` | 产出 project-refactor 工件 | slug 固定 `project-refactor` |
| `feature-verify` | 收尾验收 | `【verify】project-refactor` |
| `vue2-to-vue3-refactor` | Vue2→Vue3 | **须 `vue3-migration` spec**（与 project-refactor 互斥） |

**用户说「继续重构」「全量按规范改」→ 本 Skill，不是 code-normalize。**

---

## 铁律（违反即流程失败）

1. **先 spec 后改码** — 无 `docs/features/project-refactor/` 或 `status` 非 ready → **禁止**大规模改码
2. **功能不变** — 不改 pages.json path、不改接口 URL、不改产品文案
3. **rules 优先** — 向 rules 靠拢
4. **全量覆盖** — inventory 全部 ✅ + checklist-project 🔴=0
5. **禁止中途询问** — 自动下一批直至完成或用户 **暂停/停止**
6. **双闭环验收** — 技术 checklist + `【verify】project-refactor` PASS
7. **不主动 commit/push** — 除非用户明确要求

---

## 流程（自主循环，勿打断）

```
⓪ SDD 门禁 — project-refactor spec ready
① 预加载 rules + Read docs/features/project-refactor/
② 盘点 → docs/project-refactor-inventory.md（同步 tasks.md）
③ 按 design/tasks 分批重构
④ 每批：改码 → lint/build → 自审 → 更新 inventory + tasks
⑤ checklist-project 🔴
⑥ 阻塞 → 回到 ③
⑦ 【verify】project-refactor → 重构报告
```

---

## ⓪ SDD 门禁（强制）

| 条件 | 动作 |
|------|------|
| 目录不存在 | `【spec】propose project-refactor`，复制 `docs/features/_template/project-refactor/` |
| draft | 补全工件，`【analyze】project-refactor` 至 ready |
| ready | 进入 ① |

### 工件分工

| 文件 | 职责 |
|------|------|
| `spec.md` | **业务回归**场景（登录、tab、下单、购物车…） |
| `design.md` | 分包策略、自定义 tabBar 等架构决策 |
| `tasks.md` | 分阶段勾选 |
| `e2e.md` | H5 / 微信小程序 P0 冒烟 |
| `docs/project-refactor-inventory.md` | **rules 合规**进度 |

---

## ① 规范预加载（强制）

1. Read [shared/rules-activation.md](../shared/rules-activation.md)
2. Read `.cursor/rules/` 下**全部** `.mdc`
3. Read **`docs/features/project-refactor/`** 全部工件
4. Read `package.json` 判定 Vue 2 / Vue 3
5. Read [code-normalize/checklist.md](../code-normalize/checklist.md) + [checklist-project.md](./checklist-project.md)
6. Read [code-review/SKILL.md](../code-review/SKILL.md)
7. `project-conventions.md` — 仅对齐 request/alias
8. 输出预加载计划

---

## ② 全项目盘点

按 [inventory-template.md](./inventory-template.md) 写入 **`docs/project-refactor-inventory.md`**，同步 `tasks.md`。

- `pages/**`、`subPackages/**`
- `components/**`、`service/**`、`pages.json`、`store/**`

---

## ③ 分批重构优先级

| 优先级 | 内容 | rules 要点 |
|--------|------|------------|
| P0 | request、pages.json / 导航基线 | 基础设施 |
| P1 | 全部列表页 | 分页、services、目录规范 |
| P2 | 表单 / 详情 | 接口直绑 |
| P3 | 全局组件、store | 结构规范 |
| P4 | 🟡 建议项 | 全部 🔴 通过后 |

---

## ④ 每批自检

1. `npm run lint-fix`（有 script 时零 error）
2. `npm run build`（有 script 时通过；HBuilderX 工程 skip 须写入 verify 报告）
3. code-review 维度自审
4. 更新 inventory + `tasks.md`
5. 对照 `e2e.md` 本批冒烟

---

## ⑤–⑦ 验收与交付

- [checklist-project.md](./checklist-project.md) 🔴 = 0
- `tasks.md` 全部 [x]
- `【verify】project-refactor` PASS
- 然后输出重构报告

---

## 禁止

- 无 project-refactor spec 直接改码
- 仅 inventory、无 verify
- verify 未 PASS 声称完成
- 重构时加新功能

---

## 触发话术

```
【spec】propose project-refactor。全项目 uni-app 按 rules 重构，Vue2 保持不变
【analyze】project-refactor
【重构】按 project-refactor tasks 执行，中途不要问我是否继续
【verify】project-refactor
```
