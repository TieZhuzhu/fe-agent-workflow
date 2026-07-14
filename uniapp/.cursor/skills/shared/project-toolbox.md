# 项目工具箱（Agent 优先使用 — uni-app）

> 原则七、十：**能用脚本/命令跑的，不让 Agent 手写。**  
> 以 `package.json`、`pages.json` 与 `.cursor/project-conventions.md` 为准。

---

## SDD / Feature 门禁

| 命令 | 用途 | 何时用 |
|------|------|--------|
| `python3 .cursor/skills/scripts/feature-check.py spec <slug>` | 规格完整性 | implement 前 |
| `python3 .cursor/skills/scripts/feature-check.py analyze <slug>` | artifact 一致性 | ready 前 |
| `python3 .cursor/skills/scripts/feature-check.py verify <slug>` | lint + build 验收 | 交付前 |
| `python3 .cursor/skills/scripts/feature-check.py archive-ready <slug>` | 归档门禁 | archive 前 |
| `python3 .cursor/skills/scripts/feature-check.py board` | Feature 看板 | 查看进行中 |
| `python3 .cursor/skills/scripts/feature-check.py sync-status <slug>` | 更新 status.yaml | 阶段切换 |
| `python3 .cursor/skills/scripts/spec-index.py` | 刷新 spec 索引 | bootstrap / archive 后 |
| `python3 .cursor/skills/scripts/skills-version.py check` | Skill 版本校验 | 改 Skill 后 |
| `python3 .cursor/skills/scripts/skill-standardize.py --skill <name>` | 标准化单个 Skill | skill-creator 发布后 |
| `python3 .cursor/skills/scripts/export-agent-host.py plan` | 跨 Host 导出预览 | 迁 Claude Code / Codex |

---

## 构建与质量

| 命令 | 用途 | 何时用 |
|------|------|--------|
| `npm run lint` / `lint-fix` | ESLint（若有 script） | 改码后、verify |
| `npm run build:h5` / `build:mp-weixin` | 平台构建（若有 script） | verify、ci-fix |
| HBuilderX 运行到浏览器/模拟器 | 本地 dev | e2e、bugfix 实点 |

> 若 `package.json` 无 scripts，`feature-check verify` 自动 skip lint/build（非 FAIL）。

---

## 话术 → 工具（勿手写等价流程）

| 用户说 | 跑命令 / Skill |
|--------|----------------|
| 【verify】 | `feature-check verify` |
| 【analyze】 | `feature-check analyze` |
| 扫描项目约定 | bootstrap + `spec-index.py` |
| 【lint】 | `npm run lint`（若有）或 `lint-check` Skill |
| 新建 skill | `skill-creator` Skill |

---

## 手写 vs 工具

| 用工具 | 手写 |
|--------|------|
| 验收门禁、spec 索引、版本 check | 业务页面模板、表单逻辑 |
| lint、build（若有 script） | 接口字段绑定、交互 handler |
| pages.json path 对照 | 复杂页 hooks 拆分 |
