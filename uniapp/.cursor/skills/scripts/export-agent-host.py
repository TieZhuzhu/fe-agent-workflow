#!/usr/bin/env python3
"""Export HiStore Agent workflow from .cursor/skills to Claude Code / Codex / Copilot hosts."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

SKILLS_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILLS_ROOT.parents[1]
RULES_SRC = REPO_ROOT / ".cursor" / "rules"

# Default export targets (excludes github-copilot unless --host specified)
DEFAULT_EXPORT_HOSTS = ("claude-code", "codex")

HOST_PROFILES: dict[str, dict[str, str | None]] = {
    "cursor": {
        "skills_dir": ".cursor/skills",
        "rules_dir": ".cursor/rules",
        "agents_file": "AGENTS.md",
        "extra_file": None,
        "label": "Cursor",
    },
    "claude-code": {
        "skills_dir": ".claude/skills",
        "rules_dir": ".claude/rules",
        "agents_file": "AGENTS.md",
        "extra_file": "CLAUDE.md",
        "label": "Claude Code",
    },
    "codex": {
        "skills_dir": ".agents/skills",
        "rules_dir": ".agents/rules",
        "agents_file": "AGENTS.md",
        "extra_file": None,
        "label": "Codex CLI",
    },
    "github-copilot": {
        "skills_dir": ".github/skills",
        "rules_dir": ".agents/rules",
        "agents_file": "AGENTS.md",
        "extra_file": ".github/copilot-instructions.md",
        "label": "GitHub Copilot",
    },
}

CURSOR_PATH_RE = re.compile(r"\.cursor/skills/")
CURSOR_RULES_RE = re.compile(r"\.cursor/rules/")
CURSOR_AGENT_RE = re.compile(r"Cursor Agent Skill", re.IGNORECASE)
MDC_REF_RE = re.compile(r"([`\[（(]?)([\w\u4e00-\u9fff-]+)\.mdc")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
WHEN_TO_USE_IN_FM = re.compile(r"^when_to_use:", re.MULTILINE)

MCP_HEAVY_SKILLS = frozenset(
    {
        "bugfix-workflow",
        "feature-e2e-verify",
        "prototype-html-feature-dev",
        "figma-feature-dev",
        "feature-spec",
        "prd-markdown-ingest",
    }
)


def load_manifest() -> dict:
    with (SKILLS_ROOT / "manifest.json").open(encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def skill_dirs(manifest: dict) -> list[str]:
    return [s["name"] for s in manifest["skills"]]


def rules_manifest() -> dict[str, dict]:
    path = SKILLS_ROOT / "shared" / "host-rules-manifest.yaml"
    entries: dict[str, dict] = {}
    if path.is_file() and yaml:
        data = load_yaml(path)
        for item in data.get("rules", []):
            entries[item["source"]] = item
    return entries


def parse_mdc_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    block = m.group(1)
    body = text[m.end() :]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip()
    return meta, body


def infer_rule_tier(meta: dict[str, str]) -> str:
    desc = meta.get("description", "")
    if "仅查阅" in desc or "非预加载" in desc:
        return "on-demand"
    if meta.get("alwaysApply", "").lower() == "true":
        return "always"
    if meta.get("globs"):
        return "scoped"
    return "scoped"


def cursor_globs_to_paths_csv(globs: str) -> str:
    """Convert Cursor globs to Claude paths CSV (single line, unquoted)."""
    g = globs.strip()
    # Expand brace groups: **/*.{vue,ts} -> **/*.vue, **/*.ts
    brace = re.match(r"^(.+)\.\{([^}]+)\}$", g)
    if brace:
        prefix, exts = brace.group(1), brace.group(2)
        parts = [f"{prefix}.{ext.strip()}" for ext in exts.split(",")]
        return ", ".join(parts)
    return g


def slug_from_mdc(name: str) -> str:
    stem = Path(name).stem
    return re.sub(r"[^\w\u4e00-\u9fff-]+", "-", stem).strip("-") or "rule"


def rewrite_rule_body(body: str, *, skills_rel: str, rules_rel: str) -> str:
    out = CURSOR_PATH_RE.sub(f"{skills_rel}/", body)
    out = CURSOR_RULES_RE.sub(f"{rules_rel}/", out)
    out = CURSOR_AGENT_RE.sub("Agent Skill", out)

    def mdc_ref_repl(match: re.Match[str]) -> str:
        prefix, stem = match.group(1), match.group(2)
        return f"{prefix}{stem}.md"

    out = MDC_REF_RE.sub(mdc_ref_repl, out)
    return out


def claude_rule_frontmatter(tier: str, globs: str | None) -> str:
    if tier == "always":
        return ""
    if tier == "scoped" and globs:
        paths = cursor_globs_to_paths_csv(globs)
        return f"---\nalwaysApply: false\npaths: {paths}\n---\n"
    return ""


def codex_rule_frontmatter(tier: str, globs: str | None, description: str) -> str:
    lines = ["---", f"tier: {tier}"]
    if description:
        lines.append(f"description: {description}")
    if tier == "scoped" and globs:
        lines.append(f"globs: {globs}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def export_rules(host: str, *, dry_run: bool = False) -> list[str]:
    if host == "cursor":
        return []

    profile = HOST_PROFILES[host]
    rules_rel = str(profile["rules_dir"])
    skills_rel = str(profile["skills_dir"])
    rules_dst = REPO_ROOT / rules_rel
    on_demand_dst = REPO_ROOT / skills_rel / "shared" / "rules-on-demand"

    manifest_map = rules_manifest()
    actions: list[str] = []

    if not dry_run:
        if rules_dst.exists():
            shutil.rmtree(rules_dst)
        rules_dst.mkdir(parents=True, exist_ok=True)
        on_demand_dst.mkdir(parents=True, exist_ok=True)

    mdc_files = sorted(RULES_SRC.glob("*.mdc"))
    for mdc_path in mdc_files:
        text = mdc_path.read_text(encoding="utf-8")
        meta, body = parse_mdc_frontmatter(text)
        entry = manifest_map.get(mdc_path.name, {})
        tier = entry.get("tier") or infer_rule_tier(meta)
        slug = entry.get("slug") or slug_from_mdc(mdc_path.name)
        out_name = f"{slug}.md"
        globs = meta.get("globs")
        description = meta.get("description", "")

        rewritten = rewrite_rule_body(body, skills_rel=skills_rel, rules_rel=rules_rel)
        header = (
            f"> **Exported from** `.cursor/rules/{mdc_path.name}` · tier: `{tier}` · host: `{host}`\n\n"
        )

        if tier == "on-demand":
            out_path = on_demand_dst / out_name
            content = header + rewritten
        else:
            if host == "claude-code":
                fm = claude_rule_frontmatter(tier, globs)
            else:
                fm = codex_rule_frontmatter(tier, globs, description)
            out_path = rules_dst / out_name
            content = fm + header + rewritten

        if dry_run:
            actions.append(f"[dry-run] rule {mdc_path.name} -> {out_path.relative_to(REPO_ROOT)} ({tier})")
        else:
            out_path.write_text(content, encoding="utf-8")
            actions.append(f"rule {mdc_path.name} -> {out_path.relative_to(REPO_ROOT)} ({tier})")

    return actions


def resolve_mcp_host_key(host: str) -> str:
    if host == "github-copilot":
        return "codex"
    return host


def render_mcp_adapter_md(host: str) -> str:
    path = SKILLS_ROOT / "shared" / "mcp-host-adapter.yaml"
    if not path.is_file() or not yaml:
        return "# MCP Host Adapter\n\n(PyYAML not installed — skip)\n"

    data = load_yaml(path)
    host_key = resolve_mcp_host_key(host)
    lines = [
        "# MCP Host 适配表",
        "",
        f"> **Auto-generated** for host `{host}` · 源：`.cursor/skills/shared/mcp-host-adapter.yaml`",
        "",
        "Skills 内「Browser MCP / Figma MCP」均以本表为准。Cursor `plugin-browse-browser` 为 authoring 默认；Codex/Claude 须配置等价 MCP。",
        "",
    ]

    reqs = data.get("skill_browser_requirements") or {}
    aliases = data.get("browser_tool_aliases") or {}
    if reqs and host_key in ("codex", "claude-code", "github-copilot"):
        lines.extend(["## Skills 需要的 Browser 能力", ""])
        lines.append("| Skill | 需要 |")
        lines.append("|-------|------|")
        for skill, needs in reqs.items():
            lines.append(f"| `{skill}` | {', '.join(needs)} |")
        lines.append("")
        if aliases:
            lines.extend(["### 工具名对照（Read schema 时用）", ""])
            lines.append("| 能力 | Cursor | Playwright MCP | Real Browser MCP |")
            lines.append("|------|--------|----------------|------------------|")
            for cap, mapping in aliases.items():
                lines.append(
                    f"| {cap} | `{mapping.get('cursor', '-')}` | "
                    f"`{mapping.get('playwright', '-')}` | `{mapping.get('real-browser', '-')}` |"
                )
            lines.append("")

    for cap_id, cap in data.get("capabilities", {}).items():
        label = cap.get("label", cap_id)
        used = ", ".join(f"`{s}`" for s in cap.get("used_by", []))
        lines.append(f"## {label} (`{cap_id}`)")
        if used:
            lines.append(f"\n**涉及 Skill：** {used}\n")

        cfg = cap.get(host_key) or cap.get("cursor", {})
        if cap.get(host_key, {}).get("inherit"):
            inherit = cap[host_key]["inherit"]
            cfg = cap.get(inherit, cfg)

        lines.append("| 项 | 值 |")
        lines.append("|----|-----|")
        for key in (
            "server",
            "recommended",
            "config_key",
            "url",
            "discover",
            "env_note",
            "setup",
            "note",
        ):
            val = cfg.get(key)
            if val:
                if isinstance(val, list):
                    val = " / ".join(str(v) for v in val)
                elif isinstance(val, dict):
                    val = "; ".join(f"{k}: {v}" for k, v in val.items())
                lines.append(f"| {key} | {val} |")
        tools = cfg.get("tools") or []
        if tools:
            lines.append(f"| tools | `{', '.join(tools)}` |")
        fallbacks = cfg.get("fallback") or []
        if fallbacks:
            lines.append("| fallback | " + " → ".join(str(f) for f in fallbacks) + " |")

        for cfg_block in ("playwright_config", "real_browser_config"):
            block = cfg.get(cfg_block)
            if block:
                lines.extend(["", f"**{cfg_block}：**", "", "```toml", str(block).strip(), "```", ""])

        cursor_cfg = cap.get("cursor", {})
        if host_key != "cursor" and cursor_cfg.get("tools") and cap_id == "browser":
            lines.append("")
            lines.append(
                f"**与 Cursor 差异：** network 在 Playwright MCP 常为 `browser_network_requests`；"
                f"Real Browser MCP 与 Cursor 工具名基本一致（`browser_navigate/snapshot/click`）。"
            )
        elif host_key != "cursor" and cursor_cfg.get("tools") and cap_id == "figma":
            lines.append("")
            lines.append(
                f"**Cursor 独有工具（可选）：** `use_figma` 等 @ `{cursor_cfg.get('server', '?')}`"
            )
        lines.append("")

    lines.extend(
        [
            "## 通用降级原则",
            "",
            "1. **有 MCP** → `/mcp` 或 Read tool schema → 实点",
            "2. **无 MCP** → Shell Playwright 一次性脚本 / 用户粘贴证据",
            "3. **仍不可用** → 静态读码 + 人工清单；**禁止伪造 PASS**",
            "4. **禁止**因 MCP 不可用而拒绝 bugfix / spec 流程",
            "",
        ]
    )
    return "\n".join(lines)


def generate_rules_activation_host(host: str, skills_rel: str, rules_rel: str) -> str:
    on_demand = f"{skills_rel}/shared/rules-on-demand"
    return f"""# 规范预加载清单（{HOST_PROFILES[host]['label']} Host）

> **Auto-generated** — 与 Cursor 源 [rules-activation.md](rules-activation.md) 逻辑一致，路径已换为 `{rules_rel}/`。
> **MCP 差异：** 见 [mcp-host-adapter.md](mcp-host-adapter.md)

## 写码前门禁

### Step 0：项目约定

1. 若存在 `.cursor/project-conventions.md`，**必须先 Read**
2. 不存在 → 执行 `project-bootstrap` Skill
3. **编码规范**以 `{rules_rel}/` 为准（由 `.cursor/rules/*.mdc` 导出）

### Step 2：通用基线 Read

| 顺序 | 文件 |
|------|------|
| 1 | `{rules_rel}/frontend-general.md` |
| 2 | `{rules_rel}/项目结构与命名规范.md` 或 slug 文件 |
| 2b | `{rules_rel}/TypeScript与types规范.md` |
| 2c | `{rules_rel}/接口对接规范.md` |
| 3 | `{rules_rel}/Vue代码生成指南.md` |

> 实际文件名以 `{rules_rel}/` 目录为准（slug 化命名）。

### 禁止预加载（仅查阅）

| 文件 | 说明 |
|------|------|
| `{on_demand}/code-examples-reference.md` | 示例库；不确定写法时再 Read |

## MCP 相关 Skill

执行 `bugfix-workflow` / `feature-e2e-verify` / `prototype-html-feature-dev` / `figma-feature-dev` 前：

1. Read [mcp-host-adapter.md](mcp-host-adapter.md)
2. 按本 Host 的 server/tools 或 fallback 执行；**不得**假设 Cursor `plugin-browse-browser` 可用

## 激活汇报（写码后交付首行）

```
规范预加载：Vue 3 | Host {host} | 已读 rules + mcp-host-adapter | request 见 conventions
```
"""


def rewrite_content(text: str, skills_rel: str, *, host: str = "claude-code") -> str:
    out = CURSOR_PATH_RE.sub(f"{skills_rel}/", text)
    out = CURSOR_AGENT_RE.sub("Agent Skill", out)

    # Cursor MCP server ids → host-agnostic wording in exported copy
    if host != "cursor":
        out = out.replace("plugin-browse-browser", "Browser MCP（见 mcp-host-adapter.md）")
        out = out.replace("plugin-figma-figma", "Figma MCP（见 mcp-host-adapter.md）")
        out = out.replace(
            "Cursor **Settings → MCP**",
            "目标 Host 的 MCP 设置（Claude Code 插件 / 非 Cursor Settings）",
        )
        out = out.replace(
            "完全退出并重新打开 Cursor",
            "重启 Agent Host / MCP 服务",
        )
    return out


def mcp_banner(skill_name: str, host: str) -> str:
    if skill_name not in MCP_HEAVY_SKILLS or host == "cursor":
        return ""
    return (
        f"\n> **Host MCP：** Browser/Figma 工具见 "
        f"[mcp-host-adapter.md](../shared/mcp-host-adapter.md)（host: `{host}`）。\n\n"
    )


def inject_mcp_banner_after_frontmatter(content: str, skill_name: str, host: str) -> str:
    banner = mcp_banner(skill_name, host)
    if not banner:
        return content
    m = FRONTMATTER_RE.match(content)
    if m:
        return content[: m.end()] + banner + content[m.end() :]
    return banner + content


def copy_tree(
    src: Path,
    dst: Path,
    *,
    rewrite: bool = False,
    skills_rel: str = "",
    host: str = "claude-code",
    skill_name: str = "",
    when_to_use_map: dict[str, str] | None = None,
) -> None:
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for child in src.iterdir():
            if child.name in ("__pycache__", ".DS_Store"):
                continue
            copy_tree(
                child,
                dst / child.name,
                rewrite=rewrite,
                skills_rel=skills_rel,
                host=host,
                skill_name=skill_name,
                when_to_use_map=when_to_use_map,
            )
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if rewrite and src.suffix in (".md", ".py", ".yaml", ".yml", ".json"):
            content = src.read_text(encoding="utf-8")
            if src.name == "SKILL.md" and skill_name:
                if host == "claude-code" and when_to_use_map:
                    content = inject_when_to_use(content, skill_name, when_to_use_map)
                content = inject_mcp_banner_after_frontmatter(content, skill_name, host)
            dst.write_text(rewrite_content(content, skills_rel, host=host), encoding="utf-8")
        else:
            shutil.copy2(src, dst)


def rules_index_table(host: str, rules_rel: str) -> str:
    rules_dst = REPO_ROOT / rules_rel
    if not rules_dst.is_dir():
        return "_Rules not exported yet._"
    rows = []
    for p in sorted(rules_dst.glob("*.md")):
        rows.append(f"| `{p.name}` | auto-load |")
    on_demand = REPO_ROOT / HOST_PROFILES[host]["skills_dir"] / "shared" / "rules-on-demand"
    for p in sorted(on_demand.glob("*.md")) if on_demand.is_dir() else []:
        rows.append(f"| `{p.name}` | on-demand Read |")
    return "\n".join(rows) if rows else "_empty_"


def generate_agents_md(manifest: dict, host: str, skills_rel: str, rules_rel: str) -> str:
    platform = manifest.get("platform", "pc")
    kernel = manifest.get("kernelVersion", "?")
    bundle = manifest.get("bundleVersion", "?")
    label = HOST_PROFILES[host]["label"]

    routing_rows = []
    for entry in manifest["skills"]:
        desc = entry.get("description", "").split("。")[0].split(".")[0]
        routing_rows.append(f"| `{entry['name']}` | {desc} |")
    routing_table = "\n".join(routing_rows)

    mcp_note = ""
    if host == "codex":
        mcp_note = (
            f"> **Codex：** 无原生 Skills 发现。按意图 Read `{skills_rel}/<skill>/SKILL.md`。"
            f"MCP 见 `{skills_rel}/shared/mcp-host-adapter.md`。"
        )
    elif host == "claude-code":
        mcp_note = (
            f"> **Claude Code：** Skills `{skills_rel}/`；Rules `{rules_rel}/`（由 .mdc 导出）。"
            f"MCP 见 `{skills_rel}/shared/mcp-host-adapter.md`。"
        )
    elif host == "github-copilot":
        mcp_note = f"> **Copilot：** Skills `{skills_rel}/`；Rules `{rules_rel}/`。"

    rules_table = rules_index_table(host, rules_rel)

    return f"""# HiStore Agent Workflow ({label})

> **Auto-generated** by `export-agent-host.py` — re-export from `.cursor/skills/` after changes.
> **platform:** `{platform}` · **kernelVersion:** `{kernel}` · **bundleVersion:** `{bundle}` · **host:** `{host}`

{mcp_note}

## SDD 全链路

```
【spec】→ 【analyze】→ 【新建】→ 【verify】→ 【finish】→ 【archive】
```

## Skill 路由

| 意图 | Skill |
|------|-------|
| 新建 / PRD / Figma / 原型 | `feature-dev-workflow` |
| 增量 / 加列 / 加字段 | `incremental-feature` |
| spec / analyze / verify / finish / archive | 对应 `feature-*` |
| bug / 报错 / 点击无反应 | `bugfix-workflow` |
| lint / 单测 / CI | `lint-check` / `unit-test-codegen` / `ci-fix` |

完整索引：`{skills_rel}/README.md`

| Skill | 摘要 |
|-------|------|
{routing_table}

## Rules 注入（{label}）

| 文件 | 加载方式 |
|------|----------|
{rules_table}

- **写码前清单：** `{skills_rel}/shared/rules-activation-host.md`
- **Authoring 源（勿 fork）：** `.cursor/rules/*.mdc`
- **on-demand 示例：** `{skills_rel}/shared/rules-on-demand/`

### Cursor → {label} 语义映射

| Cursor `.mdc` | {label} |
|---------------|---------|
| `alwaysApply: true` | Rules 无 `paths` frontmatter（全局） |
| `alwaysApply: false` + `globs` | `alwaysApply: false` + `paths:` CSV 单行 |
| 仅查阅 | `{skills_rel}/shared/rules-on-demand/`（不 auto-load） |

## MCP 适配

Read **`{skills_rel}/shared/mcp-host-adapter.md`** 后再执行：

- `bugfix-workflow` / `feature-e2e-verify` → Browser 类 MCP 或 Playwright/人工降级
- `figma-feature-dev` → Figma MCP 或截图降级
- `prototype-html-feature-dev` → curl + Browser MCP P0（无 MCP 则 panel+JS+待确认）

## CLI

```bash
python3 {skills_rel}/scripts/feature-check.py board
python3 {skills_rel}/scripts/skills-version.py check
```

## 文档

- `docs/agent-host-export.md` · `docs/agent-kernel-sync.md` · `docs/constitution.md`
"""


def load_skill_when_to_use() -> dict[str, str]:
    path = SKILLS_ROOT / "shared" / "skill-when-to-use.yaml"
    if not path.is_file() or not yaml:
        return {}
    data = load_yaml(path)
    out: dict[str, str] = {}
    for name, entry in (data.get("skills") or {}).items():
        if isinstance(entry, dict) and entry.get("when_to_use"):
            out[name] = str(entry["when_to_use"]).strip()
    return out


def inject_when_to_use(content: str, skill_name: str, when_map: dict[str, str]) -> str:
    """Inject Claude-native when_to_use into exported SKILL.md frontmatter."""
    trigger = when_map.get(skill_name)
    if not trigger:
        return content
    m = FRONTMATTER_RE.match(content)
    if not m or WHEN_TO_USE_IN_FM.search(m.group(1)):
        return content
    block = m.group(1).rstrip("\n")
    folded = "\n".join(f"  {line}" if line else "  " for line in trigger.splitlines())
    block = f"{block}\nwhen_to_use: |\n{folded}\n"
    return f"---\n{block}\n---\n{content[m.end() :]}"


def claude_routing_table() -> str:
    """Concise scene-word → skill table for CLAUDE.md."""
    rows = [
        ("【spec】、propose、先写方案", "`feature-spec`"),
        ("【analyze】、ready 前评审", "`feature-analyze`"),
        ("【新建】、PRD/Figma/原型", "`feature-dev-workflow`"),
        ("【verify】、验收", "`feature-verify`"),
        ("【finish】、PR 收尾", "`feature-finish`"),
        ("【archive】、归档", "`feature-archive`"),
        ("【verify-e2e】、UI 冒烟", "`feature-e2e-verify`"),
        ("增量、加列、加字段", "`incremental-feature`"),
        ("联调、Swagger、OpenAPI", "`openapi-api-integration` / `api-integration`"),
        ("bug、报错、点击无反应", "`bugfix-workflow`"),
        ("lint / 单测 / CI", "`lint-check` / `unit-test-codegen` / `ci-fix`"),
        ("bootstrap、扫描约定", "`project-bootstrap`"),
    ]
    return "\n".join(f"| {intent} | {skill} |" for intent, skill in rows)


def generate_claude_md(manifest: dict, skills_rel: str, rules_rel: str) -> str:
    kernel = manifest.get("kernelVersion", "?")
    bundle = manifest.get("bundleVersion", "?")
    routing = claude_routing_table()
    return f"""# HiStore Agent — Claude Code

> **platform:** `{manifest.get("platform", "pc")}` · **kernel:** `{kernel}` · **bundle:** `{bundle}`  
> Auto-generated · re-export: `python3 .cursor/skills/scripts/export-agent-host.py export --host claude-code`

## 如何使用本仓库的 Skills

本项目是 **Claude Skills 驱动的 SDD 工作流**。Claude 通过每个 Skill 的 `description` + `when_to_use` 自动选用；也可用 **`/skill-name`**（如 `/feature-spec`）显式加载。

**硬约定：**

1. 用户首句含场景词（见下表）→ **先加载对应 Skill，再动手**
2. 新建页须走 SDD 全链路，**禁止无 spec 直接写码**（用户明确跳过除外）
3. 写码前 Read `{skills_rel}/shared/rules-activation-host.md`
4. 编码规范：`{rules_rel}/` · MCP：`{skills_rel}/shared/mcp-host-adapter.md`

## SDD 全链路（新建页）

```
【spec】→ 【analyze】→ 【新建】→ 【verify】→ 【finish】→ 【archive】
```

## 场景词 → Skill

| 用户意图 | Skill |
|----------|-------|
{routing}

完整 31 Skill 索引：`{skills_rel}/README.md`

## 常用 CLI

```bash
python3 {skills_rel}/scripts/feature-check.py board
python3 {skills_rel}/scripts/feature-check.py analyze <slug>
python3 {skills_rel}/scripts/feature-check.py verify <slug>
python3 {skills_rel}/scripts/skills-version.py check
```

## 文档

- `docs/constitution.md` · `docs/features/_template/` · `docs/agent-workflow-training.md`

Authoring 源（改 Skill/Rules 后 re-export）：`.cursor/skills/` + `.cursor/rules/`
"""


def generate_copilot_instructions(manifest: dict, skills_rel: str, rules_rel: str) -> str:
    return f"""# Copilot Instructions

See [AGENTS.md](../../AGENTS.md). Skills: `{skills_rel}/`. Rules: `{rules_rel}/`.
MCP: `{skills_rel}/shared/mcp-host-adapter.md`. kernel {manifest.get("kernelVersion", "?")}.
"""


def export_host(host: str, *, dry_run: bool = False) -> dict:
    if host not in HOST_PROFILES:
        raise ValueError(f"Unknown host: {host}")

    manifest = load_manifest()
    profile = HOST_PROFILES[host]
    skills_rel = str(profile["skills_dir"])
    rules_rel = str(profile["rules_dir"])
    skills_dst = REPO_ROOT / skills_rel
    agents_path = REPO_ROOT / str(profile["agents_file"])

    def log(msg: str) -> None:
        print(msg)

    if dry_run:
        log(f"[dry-run] would export skills -> {skills_dst}")
        log(f"[dry-run] would export rules -> {REPO_ROOT / rules_rel}")
        for line in export_rules(host, dry_run=True):
            log(line)
        return {"host": host, "dry_run": True}

    if host != "cursor":
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        skills_dst.mkdir(parents=True, exist_ok=True)

        when_map = load_skill_when_to_use() if host == "claude-code" else None

        for name in skill_dirs(manifest):
            src = SKILLS_ROOT / name
            if src.is_dir():
                copy_tree(
                    src,
                    skills_dst / name,
                    rewrite=True,
                    skills_rel=skills_rel,
                    host=host,
                    skill_name=name,
                    when_to_use_map=when_map,
                )
                log(f"copied skill: {name}")

        copy_tree(SKILLS_ROOT / "shared", skills_dst / "shared", rewrite=True, skills_rel=skills_rel, host=host)
        log("copied shared/")

        copy_tree(SKILLS_ROOT / "scripts", skills_dst / "scripts", rewrite=False)
        log("copied scripts/")

        for extra in ("README.md", "CHANGELOG.md", "manifest.json"):
            src = SKILLS_ROOT / extra
            if src.exists():
                if extra.endswith(".md"):
                    content = rewrite_content(src.read_text(encoding="utf-8"), skills_rel, host=host)
                    (skills_dst / extra).write_text(content, encoding="utf-8")
                else:
                    shutil.copy2(src, skills_dst / extra)
                log(f"copied {extra}")

        # Host-specific generated shared files
        mcp_md = render_mcp_adapter_md(host)
        (skills_dst / "shared" / "mcp-host-adapter.md").write_text(mcp_md, encoding="utf-8")
        log("wrote shared/mcp-host-adapter.md")

        activation = generate_rules_activation_host(host, skills_rel, rules_rel)
        (skills_dst / "shared" / "rules-activation-host.md").write_text(activation, encoding="utf-8")
        log("wrote shared/rules-activation-host.md")

        shutil.copy2(SKILLS_ROOT / "shared" / "mcp-host-adapter.yaml", skills_dst / "shared" / "mcp-host-adapter.yaml")
        shutil.copy2(SKILLS_ROOT / "shared" / "host-rules-manifest.yaml", skills_dst / "shared" / "host-rules-manifest.yaml")
        if (SKILLS_ROOT / "shared" / "skill-when-to-use.yaml").is_file():
            shutil.copy2(SKILLS_ROOT / "shared" / "skill-when-to-use.yaml", skills_dst / "shared" / "skill-when-to-use.yaml")
        if host == "claude-code" and when_map:
            log(f"injected when_to_use into {len(when_map)} skills")

    for line in export_rules(host, dry_run=False):
        log(line)

    agents_content = generate_agents_md(manifest, host, skills_rel, rules_rel)
    agents_path.write_text(agents_content, encoding="utf-8")
    log(f"wrote {agents_path.relative_to(REPO_ROOT)}")

    extra = profile.get("extra_file")
    if extra:
        extra_path = REPO_ROOT / extra
        if host == "claude-code":
            extra_path.write_text(generate_claude_md(manifest, skills_rel, rules_rel), encoding="utf-8")
        elif host == "github-copilot":
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text(generate_copilot_instructions(manifest, skills_rel, rules_rel), encoding="utf-8")
        log(f"wrote {extra_path.relative_to(REPO_ROOT)}")

    return {"host": host, "skillsDir": skills_rel, "rulesDir": rules_rel}


def cmd_plan(_: argparse.Namespace) -> int:
    manifest = load_manifest()
    print("Export plan (source: .cursor/skills/ + .cursor/rules/)")
    print(f"  platform={manifest.get('platform')} kernel={manifest.get('kernelVersion')} bundle={manifest.get('bundleVersion')}")
    print(f"  skills={len(manifest['skills'])} rules={len(list(RULES_SRC.glob('*.mdc')))}")
    print()
    for host, profile in HOST_PROFILES.items():
        if host == "cursor":
            continue
        print(f"  [{host}]")
        print(f"    skills -> {profile['skills_dir']}/")
        print(f"    rules  -> {profile['rules_dir']}/ (+ rules-on-demand in skills/shared/)")
        print(f"    agents -> {profile['agents_file']}")
        if profile.get("extra_file"):
            print(f"    extra  -> {profile['extra_file']} (Claude-native SDD + routing)")
        if host == "claude-code":
            print(f"    when_to_use -> inject from shared/skill-when-to-use.yaml")
        print(f"    mcp    -> {profile['skills_dir']}/shared/mcp-host-adapter.md")
    print()
    print("Run: python3 export-agent-host.py export --host all  # claude-code + codex")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    if args.host == "all":
        hosts = list(DEFAULT_EXPORT_HOSTS)
    else:
        hosts = [args.host]

    for host in hosts:
        print(f"\n=== export {host} ===")
        export_host(host, dry_run=args.dry_run)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    expected = {s["name"] for s in manifest["skills"]}
    host = args.host
    profile = HOST_PROFILES.get(host)
    if not profile:
        print(f"Unknown host: {host}", file=sys.stderr)
        return 1

    skills_dst = REPO_ROOT / str(profile["skills_dir"])
    rules_dst = REPO_ROOT / str(profile["rules_dir"])
    errors: list[str] = []

    if host == "cursor":
        skills_dst = SKILLS_ROOT
    else:
        if not rules_dst.is_dir():
            errors.append(f"missing rules dir: {rules_dst.relative_to(REPO_ROOT)}")
        elif not any(rules_dst.glob("*.md")):
            errors.append(f"no rules in {rules_dst.relative_to(REPO_ROOT)}")
        for req in ("shared/mcp-host-adapter.md", "shared/rules-activation-host.md"):
            if not (skills_dst / req).is_file():
                errors.append(f"missing {req}")

    if not skills_dst.is_dir():
        errors.append(f"missing skills dir: {skills_dst.relative_to(REPO_ROOT)}")

    agents_path = REPO_ROOT / str(profile["agents_file"])
    if not agents_path.is_file():
        errors.append(f"missing {profile['agents_file']}")

    for name in expected:
        if not (skills_dst / name / "SKILL.md").is_file():
            errors.append(f"missing {name}/SKILL.md")

    for req in ("shared/skill-conventions.md", "scripts/feature-check.py", "scripts/skills-version.py"):
        if not (skills_dst / req).is_file():
            errors.append(f"missing {req}")

    if host == "claude-code":
        claude_md = REPO_ROOT / "CLAUDE.md"
        if not claude_md.is_file():
            errors.append("missing CLAUDE.md")
        sample = skills_dst / "feature-spec" / "SKILL.md"
        if sample.is_file() and "when_to_use:" not in sample.read_text(encoding="utf-8"):
            errors.append("feature-spec/SKILL.md missing when_to_use (re-export claude-code)")

    if errors:
        print("CHECK FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: {host} export check passed ({len(expected)} skills, rules OK)")
    return 0


def main() -> int:
    if yaml is None:
        print("WARNING: PyYAML not installed; rules/MCP export needs: pip install pyyaml", file=sys.stderr)

    parser = argparse.ArgumentParser(description="Export HiStore Agent workflow to other hosts")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("plan", help="Show export plan")

    p_export = sub.add_parser("export", help="Export skills, rules, AGENTS.md")
    p_export.add_argument("--host", choices=[*HOST_PROFILES.keys(), "all"], default="claude-code")
    p_export.add_argument("--dry-run", action="store_true")

    p_check = sub.add_parser("check", help="Verify exported artifacts")
    p_check.add_argument("--host", choices=list(HOST_PROFILES.keys()), default="claude-code")

    args = parser.parse_args()
    if args.cmd == "plan":
        return cmd_plan(args)
    if args.cmd == "export":
        return cmd_export(args)
    if args.cmd == "check":
        return cmd_check(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
