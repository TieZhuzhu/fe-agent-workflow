---
name: rules-refactor
version: 1.2.0
description: 全项目按 .cursor/rules 重构至合规，功能不变，自主闭环不中途询问。须先具备 docs/features/project-refactor/（【spec】propose project-refactor）再改码；收尾【verify】project-refactor。用户说全量重构、按 rules 重构、规范重构、project refactor 时触发。
---
# 全项目 Rules 规范重构

> **管控力度：** 严 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **唯一权威（写法）：** `.cursor/rules/*.mdc` + 本 Skill 附属 checklist。  
> **唯一权威（计划与业务回归）：** `docs/features/project-refactor/`（**强制**，见 ⓪ SDD 门禁）。  
> **合规进度：** `docs/project-refactor-inventory.md`（② 创建并持续更新）。  
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

1. **先 spec 后改码** — 无 `docs/features/project-refactor/` 或 `status` 非 ready → **禁止**大规模改码；须先走 [feature-spec](../feature-spec/SKILL.md) `【spec】propose project-refactor`
2. **功能不变** — 不改路由 path、不改接口 URL、不改产品文案与交互语义
3. **rules 优先** — 存量写法不是模板；向 rules 靠拢
4. **全量覆盖** — inventory 全部 ✅ + checklist-project 🔴=0
5. **禁止中途询问** — 自动进入下一批直至完成或用户说 **暂停/停止**
6. **双闭环验收** — 技术：`checklist-project`；业务：`【verify】project-refactor` PASS
7. **不主动 commit/push** — 除非用户明确要求

---

## 流程（自主循环，勿打断）

```
⓪ SDD 门禁 — project-refactor spec ready（缺失则 feature-spec）
① 预加载全部 rules + Read docs/features/project-refactor/
② 全项目盘点 → docs/project-refactor-inventory.md（同步 tasks.md）
③ 按 design/tasks 分批重构（P0→P3）
④ 每批：改码 → lint/build → 自审 → 更新 inventory + tasks.md
⑤ 全项目 checklist-project 🔴
⑥ 仍有阻塞 → 回到 ③
⑦ 【verify】project-refactor → 重构报告
```

---

## ⓪ SDD 门禁（强制）

### 检查

```bash
test -d docs/features/project-refactor && test -f docs/features/project-refactor/spec.md
python3 .cursor/skills/scripts/feature-check.py analyze project-refactor  # 建议
```

| 条件 | 动作 |
|------|------|
| 目录不存在 | 执行 [feature-spec](../feature-spec/SKILL.md)：`【spec】propose project-refactor`，复制 [`docs/features/_template/project-refactor/`](../../../docs/features/_template/project-refactor/) |
| 存在但 draft | 补全 proposal/spec/design/tasks/e2e，`【analyze】project-refactor` 至 ready |
| ready | 进入 ① |

### 工件分工

| 文件 | 职责 |
|------|------|
| `docs/features/project-refactor/spec.md` | **业务回归**验收场景 |
| `docs/features/project-refactor/design.md` | 模块优先级、技术约束 |
| `docs/features/project-refactor/tasks.md` | 分阶段勾选（与 implement 同步） |
| `docs/features/project-refactor/e2e.md` | P0 冒烟路径 |
| `docs/project-refactor-inventory.md` | **rules 合规**逐模块进度 |

详见内核文档 [`docs/project-refactor-guide.md`](../../../../docs/project-refactor-guide.md)（install 后在业务项目 `docs/` 可自建链接说明）。

---

## ① 规范预加载（强制）

1. Read [shared/rules-activation.md](../shared/rules-activation.md)
2. Read `.cursor/rules/` 下**全部** `.mdc`（`代码规范示例参考.mdc` 仅查阅）
3. Read **`docs/features/project-refactor/`** 全部工件
4. Read `package.json` 判定 Vue 2 / Vue 3 — 默认保持 major
5. Read [code-normalize/checklist.md](../code-normalize/checklist.md) + [checklist-project.md](./checklist-project.md)
6. Read [code-review/SKILL.md](../code-review/SKILL.md)
7. 若存在 `project-conventions.md` — 仅对齐 request/alias
8. 输出预加载计划 + rules 清单

---

## ② 全项目盘点

按 [inventory-template.md](./inventory-template.md) 扫描，写入 **`docs/project-refactor-inventory.md`**（无则创建），并同步 `design.md` §Inventory 摘要与 `tasks.md` 阶段标题。

- `src/views/**` 每个业务目录
- `src/components/**`、`src/service/**`、`src/router/**`、`src/store/**`

---

## ③–④ 分批重构与自检

（同前：P0 基础设施 → P1 列表 → P2 表单详情 → P3 组件/store）

每批结束：

1. `npm run lint-fix`（有 script 时零 error）
2. `npm run build`（有 script 时通过）
3. 更新 `inventory` + `tasks.md` 勾选
4. 对照 `e2e.md` 执行本批相关冒烟（能跑则跑）

---

## ⑤–⑦ 验收与交付

1. [checklist-project.md](./checklist-project.md) 全部 🔴 = 0
2. `tasks.md` 全部 [x] 或标注 skip
3. 执行 [feature-verify](../feature-verify/SKILL.md)：`【verify】project-refactor`
4. **verify PASS 前**不得声称「重构完成」

**汇报模板**

```markdown
## Rules 重构报告
- Feature: project-refactor | verify: PASS/FAIL
- Vue 版本：2.x / 3.x
- inventory：N/N ✅ | checklist-project 🔴=0
- build / lint：通过 / skip（原因）

### 主要变更摘要
- ...

### spec 场景回归
- 场景 1–N：pass/fail（见 verify 报告）

### 仍 🟡 建议
- ...
```

---

## 禁止

- 无 project-refactor spec 直接全项目改码
- 仅产出 inventory、无 feature 工件与 verify
- 以 conventions 为由跳过 rules
- 只做部分模块就停并问「是否继续」
- verify 未 PASS 就声称完成
- 重构时加新功能

---

## 触发话术

```
【spec】propose project-refactor。全项目按 rules 重构，Vue2 保持不变
【analyze】project-refactor
【重构】按 project-refactor tasks 执行，中途不要问我是否继续
【verify】project-refactor
```
