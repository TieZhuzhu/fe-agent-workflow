# Agent 工作流跨 Host 导出（Cursor → Claude Code / Codex）

> **源仓库：** `HiStore-store-pc` · `platform: pc` · `kernelVersion: 1.3.1`  
> **权威源：** `.cursor/skills/` + `.cursor/rules/`（Cursor 为 authoring host）  
> **相关：** [agent-kernel-sync.md](./agent-kernel-sync.md) · [agent-workflow-comparison.md](./agent-workflow-comparison.md)

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

清单配置：`.cursor/skills/shared/host-rules-manifest.yaml`（tier 覆盖 frontmatter 推断）。

**路径重写：** 导出 rule 正文中 `.cursor/rules/X.mdc` → `{rules_dir}/X.md`；`.cursor/skills/` → 目标 skills 路径。

---

## 四、Claude 原生 Skill 路由（非 Cursor 对齐）

Claude Code **没有**单独的 `skill-routing` 模块；路由由以下组成：

| 机制 | 导出产物 |
|------|---------|
| `description` + `when_to_use` | 导出时注入 `.claude/skills/*/SKILL.md` frontmatter |
| `CLAUDE.md` | SDD 链路 + 场景词表 + 硬约定 |
| `/skill-name` | 目录名即命令（如 `/feature-spec`） |

配置源：`.cursor/skills/shared/skill-when-to-use.yaml`（31 Skill 触发词）

**不写入 Cursor 源** — 仅 Claude 导出副本带 `when_to_use`，`.cursor/skills/` authoring 不变。

---

## 五、MCP 适配

配置源：`.cursor/skills/shared/mcp-host-adapter.yaml`

导出时按 Host 渲染为 `{skills}/shared/mcp-host-adapter.md`，包含：

| 能力 | Cursor | Claude Code | Codex |
|------|--------|-------------|-------|
| Browser | `plugin-browse-browser` | Real Browser / Playwright MCP | **Playwright MCP** / **Real Browser MCP** |
| Figma | `plugin-figma-figma` | Figma 插件 | **Figma MCP Server**（`mcp.figma.com`） |
| Shell | Agent Shell | 同 | 主力 |

**MCP 相关 Skill** 导出时自动：

1. 文首插入 `Host MCP` 横幅 → 指向 `mcp-host-adapter.md`
2. 替换 `plugin-browse-browser` / `Cursor Settings → MCP` 等 Cursor 专有用语

涉及 Skill：`bugfix-workflow`、`feature-e2e-verify`、`prototype-html-feature-dev`、`figma-feature-dev`、`feature-spec`、`prd-markdown-ingest`。

**Codex Browser 选型：**

| 方案 | 适用 | 与 Skills 对齐 |
|------|------|----------------|
| **Playwright MCP** | 通用自动化、官方插件 | `browser_navigate/snapshot/click`；network → `browser_network_requests` |
| **Real Browser MCP** | 中后台已登录 Chrome | 工具名与 Cursor Skills **几乎一致**（含 `browser_network`） |

示例配置：`.codex/config.toml.example`

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

## 七、生成物

| 路径 | 说明 |
|------|------|
| `.claude/skills/` | 31 Skill + shared + scripts |
| `.claude/rules/` | 13 条 auto-load rules |
| `.claude/skills/shared/rules-on-demand/` | 示例参考（仅显式 Read） |
| `.claude/skills/shared/mcp-host-adapter.md` | Host MCP 映射 |
| `.claude/skills/shared/rules-activation-host.md` | 预加载清单（Host 路径版） |
| `CLAUDE.md` | Claude 入口（claude-code 专用） |
| `AGENTS.md` | 跨 Host 基线（Codex 主读此文件） |

无 `.agent-export/` — 该目录仅为历史导出快照，**不必生成**；`check` 直接校验 skills/rules/CLAUDE.md。

---

## 八、验收

- [ ] `export-agent-host.py check --host <host>` PASS
- [ ] `.claude/rules/frontend-general.md` 无 frontmatter（全局）
- [ ] scoped rule 含 `paths:` CSV 单行
- [ ] `bugfix-workflow/SKILL.md` 文首有 Host MCP 横幅
- [ ] `.claude/skills/feature-spec/SKILL.md` 含 `when_to_use:`
- [ ] `CLAUDE.md` 含 SDD 链路与场景词表
- [ ] Claude Code 新 session：【spec】/【verify】/ 增量 三条话术
- [ ] `feature-check.py board` 可运行

---

## 九、团队流程

1. 改 `.cursor/rules/` 或 `.cursor/skills/` → `export-agent-host.py export --host all`
2. **不要**在 `.claude/rules/` 手改后忘记回写 `.cursor/rules/`
3. 新增 MCP 能力：先改 `mcp-host-adapter.yaml`，再 export
4. uni-app 仍走 [agent-kernel-sync.md](./agent-kernel-sync.md)，不走 host-export

---

*维护：内核升版后 re-export；培训见 [agent-workflow-training.md](./agent-workflow-training.md)。*
