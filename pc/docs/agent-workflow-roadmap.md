# Agent 工作流演进路线图

> 基于 2026-07-09 团队决策。与 [agent-workflow-training.md](./agent-workflow-training.md) 配套（**Bundle 1.3.1**）。

**推荐 SDD 链路：** `【spec】→ 【analyze】→ 【新建】→ 【verify】→ 【finish】→ 【archive】`

**话术与路由权威：** [.cursor/skills/README.md](../.cursor/skills/README.md) §黄金路径 · §SDD 完整路径

---

## 已确认决策（P0）

| 项 | 决策 |
|----|------|
| CLI 位置 | `.cursor/skills/scripts/feature-check.py` |
| verify 默认 | 跑 `lint-fix` + `build`（`--no-build` / `--no-lint` 可跳过） |
| CI 接入 | **不接入**（本地 + Agent 使用） |
| 示例 slug | `project-refactor` |
| Clarify blocker | path、主接口 URL、模块、权限冲突、页面冲突 |
| Clarify 非 blocker | 页面类型、文案、样式、非核心字段 |
| TDD | **暂缓 strict**（`testStrategy: pending`，见 constitution §11） |

### feature-check 用法

```bash
# 列出 feature
python3 .cursor/skills/scripts/feature-check.py list

# 规格门禁（implement 前）
python3 .cursor/skills/scripts/feature-check.py spec <slug>

# 验收门禁（默认 lint-fix + build）
python3 .cursor/skills/scripts/feature-check.py verify <slug>

# 仅静态，不跑 build（快）
python3 .cursor/skills/scripts/feature-check.py verify <slug> --no-build

# 归档前
python3 .cursor/skills/scripts/feature-check.py archive-ready <slug>
```

---

## P0 实施状态

| ID | 内容 | 状态 |
|----|------|------|
| P0-1 | `feature-check.py` CLI | ✅ 已落地 |
| P0-2 | Delta Spec 合并规范（archive 默认） | ✅ 已落地 |
| P0-3 | Clarify 分级 + clarify-log 模板 | ✅ 已落地 |
| P0-4 | TDD strict（暂缓 pending，constitution + conventions） | ✅ 已落地 |

---

## P1 优先级（团队排序）

| 优先级 | ID | 内容 | 状态 |
|--------|-----|------|------|
| **1** | P1-5 | bootstrap spec 索引（onboard 扫 views → docs/specs/_index.md） | ✅ 已落地 |
| **2** | P1-3 | bugfix-workflow 四阶段调试清单 | ✅ 已落地 |
| **3** | P1-4 | feature-finish Skill（PR 收尾清单） | ✅ 已落地 |
| **4** | P1-2 | feature-analyze Skill（implement 前 artifact 一致性） | ✅ 已落地 |
| **5** | P1-1 | status.yaml + feature-check board | ✅ 已落地 |

### CLI 命令总览

```bash
python3 .cursor/skills/scripts/feature-check.py board
python3 .cursor/skills/scripts/feature-check.py analyze <slug>
python3 .cursor/skills/scripts/feature-check.py sync-status <slug> [--set STATUS]
python3 .cursor/skills/scripts/spec-index.py
```

### P1-5 bootstrap spec 索引（✅ 已落地）

**产出：** `docs/specs/_index.md`

```bash
python3 .cursor/skills/scripts/spec-index.py
python3 .cursor/skills/scripts/spec-index.py --check
python3 .cursor/skills/scripts/spec-index.py --json
```

**触发：** `扫描项目约定` / `【onboard】刷新 spec 索引`

### P1-3 bugfix 四阶段（✅）

`bugfix-workflow` v1.3.0 — Phase 1 复现 → 2 假设 → 3 验证 → 4 修复

### P1-4 feature-finish（✅）

`【finish】<slug>` — verify PASS 后 PR 描述 + 自检 + archive 提示

### P1-2 feature-analyze（✅）

`【analyze】<slug>` — `feature-check analyze <slug>`；CRITICAL>0 禁止 ready

### P1-1 status.yaml + board（✅）

- 模板：`docs/features/_template/status.yaml`
- `feature-check board` / `sync-status <slug>`

---

## 与 OpenSpec / Spec-Kit / Superpowers 吸收对照

| 借鉴 | 落地项 |
|------|--------|
| OpenSpec verify/archive | P0-1 CLI、P0-2 Delta |
| Spec-Kit analyze/clarify | P0-3、P1-2 |
| Superpowers TDD / debugging / finish | P0-4、P1-3、P1-4 |

**对比文档：** [agent-workflow-comparison.md](./agent-workflow-comparison.md)

---

*更新：2026-07-10*
