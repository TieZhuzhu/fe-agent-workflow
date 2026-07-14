# Agent 工作流跨 Host 导出（Cursor → Claude Code / Codex）

> **源仓库：** `HiStore-mall-mobile` · `platform: uniapp` · `kernelVersion: 1.3.1`  
> **权威源：** `.cursor/skills/` + `.cursor/rules/`（Cursor 为 authoring host）  
> **相关：** [agent-kernel-sync.md](./agent-kernel-sync.md) · [agent-workflow-roadmap.md](./agent-workflow-roadmap.md)

---

## 一、结论

**可以写迁移脚本；Rules 与 MCP 已支持自动转换 + Host 适配表。**

| 层级 | 可自动化 | 导出产物 |
|------|---------|---------|
| 31 个 Skill | ✅ | `.claude/skills/` / `.agents/skills/` |
| Rules 注入语义 | ✅ | `.claude/rules/` / `.agents/rules/` + `rules-on-demand/` |
| MCP 差异 | ✅ | `shared/mcp-host-adapter.md`（按 Host 渲染） |
| Cursor alwaysApply | ✅ | Claude 全局 rule 无 frontmatter |
| Cursor globs | ✅ | Claude `alwaysApply: false` + `paths:` CSV 单行 |
| 仅查阅 rules | ✅ | `{skills}/shared/rules-on-demand/`（不 auto-load） |

**仍须人工：** 目标 Host 实际安装的 MCP 插件名、Playwright 环境、团队是否提交导出目录。

---

## 二、各 Host 目录

| Host | Skills | Rules（auto-load） | on-demand rules | MCP 适配 |
|------|--------|-------------------|-----------------|----------|
| Cursor | `.cursor/skills/` | `.cursor/rules/*.mdc` | 同文件，description 标注 | Cursor MCP |
| Claude Code | `.claude/skills/` | `.claude/rules/*.md` | `.claude/skills/shared/rules-on-demand/` | `mcp-host-adapter.md` |
| Codex | `.agents/skills/` | `.agents/rules/*.md` | 同上 | 同上 |
| Copilot | `.github/skills/` | `.agents/rules/` | `.github/skills/shared/rules-on-demand/` | 同上 |

共用：`AGENTS.md`（路由 + Rules 索引 + MCP 指针）、`CLAUDE.md`（Claude 专用）。

---

## 三、Rules 注入语义映射

| Cursor `.mdc` | Claude Code `.claude/rules/` | Codex `.agents/rules/` |
|---------------|------------------------------|------------------------|
| `alwaysApply: true` | 无 frontmatter（会话级全局） | `tier: always`，无 globs |
| `alwaysApply: false` + `globs` | `alwaysApply: false` + `paths: **/*.vue, **/*.ts` | `tier: scoped` + `globs:` |
| description 含「仅查阅」 | **不**进 rules 目录 → `rules-on-demand/` | 同左 |

清单配置：`.cursor/skills/shared/host-rules-manifest.yaml`（**本仓库为 uni-app 11 条 rules**）。

**路径重写：** 导出 rule 正文中 `.cursor/rules/X.mdc` → `{rules_dir}/X.md`；`.cursor/skills/` → 目标 skills 路径。

---

## 四、Claude 原生 Skill 路由

| 机制 | 导出产物 |
|------|---------|
| `description` + `when_to_use` | 导出时注入 `.claude/skills/*/SKILL.md` frontmatter |
| `CLAUDE.md` | SDD 链路 + 场景词表 + 硬约定 |
| `/skill-name` | 目录名即命令 |

配置源：`.cursor/skills/shared/skill-when-to-use.yaml`（31 Skill 触发词，uni-app 术语已适配）

---

## 五、MCP 适配

配置源：`.cursor/skills/shared/mcp-host-adapter.yaml`

涉及 Skill：`bugfix-workflow`、`feature-e2e-verify`、`prototype-html-feature-dev`、`figma-feature-dev`。

**移动端注意：** H5 实点优先 Browser MCP；小程序真机仍须人工验收。

---

## 六、命令

```bash
python3 .cursor/skills/scripts/export-agent-host.py plan
python3 .cursor/skills/scripts/export-agent-host.py export --host claude-code
python3 .cursor/skills/scripts/export-agent-host.py export --host codex
python3 .cursor/skills/scripts/export-agent-host.py export --host all
python3 .cursor/skills/scripts/export-agent-host.py check --host claude-code
```

依赖：`pip install pyyaml`（Rules/MCP 导出）。

---

## 七、验收

- [ ] `export-agent-host.py check --host <host>` PASS
- [ ] scoped rule 含 `paths:` CSV 单行
- [ ] `bugfix-workflow/SKILL.md` 文首有 Host MCP 横幅（导出后）
- [ ] `feature-check.py board` 可运行
- [ ] 导出 rules 含 `uniapp代码生成指南`、`路由与分包规范`（非 PC 中后台 rules）

---

## 八、团队流程

1. 改 `.cursor/rules/` 或 `.cursor/skills/` → `export-agent-host.py export --host all`
2. **不要**在 `.claude/rules/` 手改后忘记回写 `.cursor/rules/`
3. PC ↔ uni-app **内核**同步走 [agent-kernel-sync.md](./agent-kernel-sync.md)，与 host-export 独立

---

*维护：内核升版后 re-export；培训见 [agent-workflow-training.md](./agent-workflow-training.md)。*
