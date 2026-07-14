---
name: feature-verify
version: 1.0.1
description: L1 验收：对照 spec/tasks/field-map 与代码，执行 lint+build。 可选衔接 api-smoke（L2）、feature-e2e-verify（L3）。 用户说【verify】、验收 feature 时触发。
---
# Feature Verify

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 对应 OpenSpec `/opsx:verify`、Spec-Kit `/speckit.analyze` + converge。验证**是否做对**，不只验证**写法是否规范**。

## 触发场景

- `【verify】product-tag-list`
- feature 实现完成，合并 / 交付前
- `feature-dev-workflow` 阶段 ④ 之后（或替代仅跑 reference-checklist）

**不触发：** 纯 code-review（无 feature 目录时用 `code-review`）。

---

## 流程

```
① 定位 feature → ② 对照 spec → ③ 对照 design/field-map → ④ 勾 tasks → ⑤ 规范验收 → ⑥ 命令验证 → ⑥b 增强验收（可选）→ ⑦ 报告
```

### ① 定位 feature

- 用户指定 slug → `docs/features/<slug>/`
- 未指定 → 从 git diff / 最近改动推断 module-page slug

若目录不存在 → 降级为 `code-review` + `reference-checklist`，并提示「无 feature spec，建议下次走 feature-spec」。

### ② 对照 spec.md

逐条检查 **验收场景**：

| 场景 | 实现位置 | 结果 |
|------|----------|------|
| Given/When/Then | 文件:行或组件 | pass / fail / skip |

- fail → 修代码或更新 spec（须说明理由）
- 未实现 FR → 标记 blocker

### ③ 对照 design.md + field-map.md

- [ ] 路由 path 与 `views/` 目录一致
- [ ] design 文件清单中的文件存在
- [ ] field-map 列与 `types.ts`、模板 `prop`、services 入参一致
- [ ] 接口 URL / 函数名与 design 一致

### ④ 勾选 tasks.md

Read `tasks.md`，逐项核对：

- 已完成 → 改为 `- [x]`
- 未完成 → 列出 blocker
- **全部 [x] 或已标注 skip 理由** 才可 pass

### ⑤ 规范验收

执行 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md) 与本次改动相关的项。

可选：[code-review](../code-review/SKILL.md) 快速扫一遍。

### ⑥ 命令验证

**优先执行 CLI（团队门禁）：**

```bash
python3 .cursor/skills/scripts/feature-check.py verify <slug>
# 仅静态、不跑 build：加 --no-build
```

将 CLI 输出的 Blockers 写入报告。CLI FAIL 则 Verdict 不得为 PASS。

Read `package.json`，CLI 未覆盖时再按实际 scripts 执行：

```bash
npm run lint-fix   # 或项目等价 lint script，须 0 errors
pnpm test          # 若有
pnpm build         # 若有
```

lint / test / build 失败 → [lint-check](../lint-check/SKILL.md) / [ci-fix](../ci-fix/SKILL.md) 或修到通过。

### ⑥b 增强验收（可选）

| 维度 | Skill | 无环境时 |
|------|-------|----------|
| 接口实况 L2 | [api-smoke](../api-smoke/SKILL.md)（curl） | skip + 标注 |
| UI 冒烟 L3 | [feature-e2e-verify](../feature-e2e-verify/SKILL.md)（MCP 须用户侧重载；Shell nvm 不等价） | skip + 人工清单 |
| 单测 | [unit-test-codegen](../unit-test-codegen/SKILL.md) | skip（无 test script） |

用户 `【api-smoke】` / `【verify-e2e】` 时走对应 Skill。普通 `【verify】` 完成 L1 即可 PASS，但报告**须填写** L2/L3 为 pass/fail/skip。

### ⑦ 验证报告

```markdown
## Feature Verify: <slug>

| 维度 | 结果 |
|------|------|
| Spec 场景 | x/y pass |
| design 一致 | pass/fail |
| field-map | pass/fail/N/A |
| tasks.md | x/y 完成 |
| reference-checklist | pass/fail |
| lint | pass/fail/skip |
| test:unit | pass/fail/skip |
| build | pass/fail/skip |
| api-smoke (L2) | pass/fail/skip |
| e2e (L3) | pass/fail/skip |

### Blockers
- ...

### 建议
- 通过后：【archive】<slug>
```

**Verdict：** `PASS` | `FAIL`（有 blocker 不可 archive）

PASS 后建议执行 [feature-finish](../feature-finish/SKILL.md)；上线合码后 `【archive】`。

---

## 与 code-review 的区别

| | feature-verify | code-review |
|---|----------------|-------------|
| 对照物 | spec / design / field-map | rules |
| 任务清单 | tasks.md 勾完 | 无 |
| 命令 | test / build | 无 |

两者可串联：verify → archive 前 review 可选。

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 跑 feature-check verify、对照 tasks 勾选
- 🚫 未跑 lint/build 即报 PASS

## 交付检查

**交付首行：** `Feature Verify: <slug> | PASS/FAIL | spec x/y | tasks x/y | build ✅/❌`

**门禁**

- [ ] `feature-check verify <slug>` 结果写入汇报
- [ ] tasks 未完成项列出
