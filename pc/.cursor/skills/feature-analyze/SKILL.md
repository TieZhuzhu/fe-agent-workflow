---
name: feature-analyze
version: 1.0.1
description: 对照 spec/design/tasks/field-map/e2e 做 implement 前一致性分析；CRITICAL>0 禁止标记 ready。 用户说【analyze】、spec 评审、ready 前触发。CLI：feature-check analyze。
---
# Feature Analyze（规划门禁）

> **管控力度：** 严 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 对应 Spec-Kit `/speckit.analyze`。在 **implement 前** 发现 artifact 矛盾，避免写码后返工。

## 触发场景

- `【analyze】<slug>`
- `feature-spec` 标记 `Status: ready` **之前**
- `feature-dev-workflow` 阶段 ② 结束、阶段 ③ 开始前

**不触发：** 无 `docs/features/<slug>/`；纯 incremental / bugfix。

---

## 流程

```
① 定位 feature → ② 交叉矩阵检查 → ③ CLI 校验 → ④ 报告 → ⑤ 修复或 ready
```

### ① 定位

`docs/features/<slug>/`，Read：proposal、spec、design、tasks、field-map、e2e.md（若有）、status.yaml（若有）

### ② 交叉矩阵（Agent 须逐项核对）

| 对照 | 检查 | 严重级 |
|------|------|--------|
| spec ↔ design | 每个 FR / 用户故事在 design 文件清单或接口表有落点 | CRITICAL |
| design ↔ tasks | design 列出的文件/模块在 tasks 有可勾选项 | CRITICAL |
| design ↔ field-map | design 接口表每条 URL 在 field-map 有映射（或 N/A 说明） | CRITICAL |
| design path ↔ 目录 | path 与 `views/<module>/<page-dir>/` 规划一致（全项目治理可豁免） | CRITICAL |
| spec ↔ e2e | P0 新建页：主流程场景在 e2e.md 有步骤 | WARNING |
| tasks ↔ TDD | `testStrategy: strict` 时 logic 项须标 `[test]` | WARNING |
| clarify | blocker 级 `[待确认]` = 0 | CRITICAL |

### ③ CLI（团队门禁）

```bash
python3 .cursor/skills/scripts/feature-check.py analyze <slug>
```

**Verdict：**

- `CRITICAL = 0` → 可进入 `Status: ready` + implement
- `CRITICAL > 0` → **禁止** ready；修复 artifact 后重跑 analyze

### ④ 报告模板

```markdown
## Feature Analyze: <slug>

| 检查项 | 结果 | 说明 |
|--------|------|------|
| spec ↔ design | pass/fail | |
| design ↔ tasks | pass/fail | |
| design ↔ field-map | pass/fail | |
| path ↔ 目录 | pass/fail/N/A | |
| clarify blockers | pass/fail | |
| spec ↔ e2e | pass/warn/skip | |

**CRITICAL:** 0 | **WARNING:** n
**Verdict:** PASS / FAIL
```

### ⑤ 下一步

- **PASS** → 更新 `status.yaml` 为 `ready`（`feature-check sync-status <slug>`）→ 告知可 `【新建】`
- **FAIL** → 列出修复项，回到 feature-spec / 补 tasks / field-map

---

## 与 feature-spec / feature-verify 的关系

| 阶段 | Skill |
|------|-------|
| propose 填完工件 | **feature-analyze**（本 Skill） |
| ready 后写码 | feature-dev-workflow |
| 写码后 | feature-verify（实现对照，非规划对照） |

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 只读分析，输出 CRITICAL/WARNING 清单
- 🚫 CRITICAL>0 时声称可开始写码

## 交付检查

**交付首行：** `Feature Analyze: <slug> | PASS/FAIL | CRITICAL n | WARNING n`

**门禁**

- [ ] 运行 `feature-check analyze <slug>` 并汇报结果
