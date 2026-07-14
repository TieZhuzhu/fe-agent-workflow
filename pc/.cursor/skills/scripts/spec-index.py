#!/usr/bin/env python3
"""Scan router + views and generate docs/specs/_index.md.

Usage:
  python3 .cursor/skills/scripts/spec-index.py
  python3 .cursor/skills/scripts/spec-index.py --check   # exit 1 if gaps exist
  python3 .cursor/skills/scripts/spec-index.py --json    # stdout JSON summary
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
SRC = REPO_ROOT / "src"
ROUTER_MODULES = SRC / "router" / "modules"
VIEWS = SRC / "views"
SPECS_DIR = REPO_ROOT / "docs" / "specs"
FEATURES_DIR = REPO_ROOT / "docs" / "features"
OUTPUT = SPECS_DIR / "_index.md"

IMPORT_RE = re.compile(
    r"path:\s*['\"]([^'\"]+)['\"].*?"
    r"component:\s*\(\)\s*=>\s*import\([^)]*@/views/([^'\"]+)['\"]",
    re.DOTALL,
)
TITLE_RE = re.compile(r"title:\s*['\"]([^'\"]+)['\"]")
REDIRECT_RE = re.compile(r"path:\s*['\"]([^'\"]+)['\"].*?redirect:\s*['\"]([^'\"]+)['\"]")

SKIP_PATH_PREFIXES = ("/login", "/403", "/404", "/error")
SKIP_PATH_EXACT = {"/", "*"}


@dataclass
class RouteEntry:
    path: str
    title: str
    view_import: str
    view_dir: str
    module: str
    page_dir: str
    spec_path: str
    spec_status: str
    feature_slug: str = ""
    note: str = ""


@dataclass
class IndexReport:
    routes: list[RouteEntry] = field(default_factory=list)
    orphan_views: list[str] = field(default_factory=list)

    @property
    def gaps(self) -> list[RouteEntry]:
        return [r for r in self.routes if r.spec_status in ("缺失", "进行中")]

    @property
    def has_gaps(self) -> bool:
        return len(self.gaps) > 0


def parse_route_blocks(content: str) -> list[str]:
    """Split router module file into route object blocks."""
    blocks: list[str] = []
    current: list[str] = []
    depth = 0
    for line in content.splitlines():
        if re.match(r"^\s*\{", line):
            if depth == 0:
                current = [line]
            else:
                if current:
                    current.append(line)
            depth += line.count("{") - line.count("}")
            continue
        if current:
            current.append(line)
            depth += line.count("{") - line.count("}")
            if depth <= 0:
                blocks.append("\n".join(current))
                current = []
                depth = 0
    return blocks


def read_router_routes() -> list[tuple[str, str, str]]:
    """Return list of (path, view_import, title)."""
    entries: list[tuple[str, str, str]] = []
    if not ROUTER_MODULES.is_dir():
        return entries

    for module_file in sorted(ROUTER_MODULES.glob("*.js")):
        content = module_file.read_text(encoding="utf-8")
        for block in parse_route_blocks(content):
            path_m = re.search(r"path:\s*['\"]([^'\"]+)['\"]", block)
            if not path_m:
                continue
            path = path_m.group(1)
            if path in SKIP_PATH_EXACT or path.startswith(SKIP_PATH_PREFIXES):
                continue
            if re.search(r"redirect:\s*['\"]", block):
                continue
            import_m = re.search(r"@/views/([^'\"]+)", block)
            if not import_m:
                continue
            view_import = import_m.group(1).removesuffix("/index.vue").removesuffix(".vue")
            title_m = TITLE_RE.search(block)
            title = title_m.group(1) if title_m else ""
            entries.append((path, view_import, title))
    return entries


def resolve_view_dir(view_import: str) -> Path | None:
    candidates = [
        VIEWS / view_import,
        VIEWS / f"{view_import}/index.vue",
        VIEWS / f"{view_import}.vue",
        VIEWS / f"{view_import}/Index.vue",
    ]
    for c in candidates:
        if c.is_dir():
            return c
        if c.is_file():
            return c.parent if c.name.endswith(".vue") else c
    return None


def path_to_spec_relpath(path: str, view_import: str) -> tuple[str, str, str]:
    """Return (module, page_dir, spec relative path under docs/specs/)."""
    parts = view_import.split("/")
    module = parts[0] if parts else "unknown"
    page_dir = parts[1] if len(parts) > 1 else parts[0]
    # align with docs/specs/<module>/<page-dir>.md convention
    spec_rel = f"{module}/{page_dir}.md"
    return module, page_dir, spec_rel


def find_active_feature(view_import: str, path: str) -> str:
    """Match page-scoped in-progress feature only (not fuzzy global refactor)."""
    if not FEATURES_DIR.is_dir():
        return ""
    view_norm = view_import.replace("\\", "/")
    path_tail = path.rsplit("/", 1)[-1]

    for entry in sorted(FEATURES_DIR.iterdir()):
        if not entry.is_dir() or entry.name in ("_template", "archive"):
            continue
        proposal = entry / "proposal.md"
        if proposal.exists():
            status = re.search(r"Status:\s*\*?\*?(\w+)\*?\*?", proposal.read_text(encoding="utf-8"), re.I)
            if status and status.group(1).lower() in ("archived", "implemented"):
                continue
        design_text = (entry / "design.md").read_text(encoding="utf-8", errors="ignore") if (entry / "design.md").exists() else ""
        if not design_text:
            continue
        # 全项目治理 feature：仅在 design 文件清单/路由表显式列出该视图时关联
        markers = (
            f"views/{view_norm}",
            f"`{view_norm}`",
            f"| `{path}` |",
            f"| {path} |",
        )
        if any(m in design_text for m in markers):
            return entry.name
        # slug 与 module-page 一致：如 product-tag-list ↔ views/product/tag-list
        slug_parts = entry.name.split("-")
        if len(slug_parts) >= 2:
            guess = "/".join(slug_parts[:2]) if len(slug_parts) == 2 else f"{slug_parts[0]}/{'-'.join(slug_parts[1:])}"
            if view_norm == guess or view_norm.endswith(guess):
                return entry.name
    return ""


def spec_status(spec_rel: str, feature_slug: str) -> str:
    spec_file = SPECS_DIR / spec_rel
    if spec_file.exists():
        return "已归档"
    if feature_slug:
        return "进行中"
    return "缺失"


def is_page_level_view(rel: str) -> bool:
    """views/<module>/<page> — exclude components and legacy duplicates."""
    parts = rel.split("/")
    if len(parts) != 2:
        return False
    legacy_dupes = {
        "product/product-detail",
        "trade/order-manage",
        "trade/order-detail",
        "trade/order-delivery",
        "setting/permission-group",
        "setting/operation-log",
    }
    return rel not in legacy_dupes


def collect_orphan_views(routed_imports: set[str]) -> list[str]:
    orphans: list[str] = []
    if not VIEWS.is_dir():
        return orphans
    for index in VIEWS.rglob("index.vue"):
        rel = index.parent.relative_to(VIEWS).as_posix()
        if not is_page_level_view(rel):
            continue
        if rel in ("login",):
            continue
        if rel not in routed_imports:
            orphans.append(rel)
    return sorted(set(orphans))


def build_report() -> IndexReport:
    report = IndexReport()
    routed_imports: set[str] = set()

    for path, view_import, title in read_router_routes():
        routed_imports.add(view_import)
        view_dir = resolve_view_dir(view_import)
        module, page_dir, spec_rel = path_to_spec_relpath(path, view_import)
        feature_slug = find_active_feature(view_import, path)
        status = spec_status(spec_rel, feature_slug)
        note = ""
        if view_dir is None:
            note = "视图目录未找到"
        report.routes.append(
            RouteEntry(
                path=path,
                title=title,
                view_import=view_import,
                view_dir=str(view_dir.relative_to(REPO_ROOT)) if view_dir else "—",
                module=module,
                page_dir=page_dir,
                spec_path=f"docs/specs/{spec_rel}",
                spec_status=status,
                feature_slug=feature_slug,
                note=note,
            )
        )

    report.orphan_views = collect_orphan_views(routed_imports)
    return report


def render_markdown(report: IndexReport) -> str:
    today = date.today().isoformat()
    total = len(report.routes)
    archived = sum(1 for r in report.routes if r.spec_status == "已归档")
    in_progress = sum(1 for r in report.routes if r.spec_status == "进行中")
    missing = sum(1 for r in report.routes if r.spec_status == "缺失")

    lines = [
        "# Spec 索引（页面 ↔ 路由 ↔ 规格）",
        "",
        f"> 由 `project-bootstrap` / `spec-index.py` 生成，日期：{today}",
        "> 权威行为 spec：`docs/specs/<module>/<page>.md`；进行中变更：`docs/features/<slug>/`",
        "",
        "## 统计",
        "",
        f"| 指标 | 数量 |",
        f"|------|------|",
        f"| 注册业务路由 | {total} |",
        f"| 已归档 spec | {archived} |",
        f"| 进行中 feature | {in_progress} |",
        f"| **缺失 spec** | **{missing}** |",
        "",
        "## 路由索引",
        "",
        "| 模块 | 路由 path | 标题 | 视图目录 | 主 spec | 状态 | 进行中 feature |",
        "|------|-----------|------|----------|---------|------|----------------|",
    ]

    for r in sorted(report.routes, key=lambda x: (x.module, x.path)):
        spec_link = r.spec_path if r.spec_status == "已归档" else "—"
        feat = r.feature_slug or "—"
        view = f"`{r.view_dir}`" if r.view_dir != "—" else "—"
        lines.append(
            f"| {r.module} | `{r.path}` | {r.title} | {view} | {spec_link} | {r.spec_status} | {feat} |"
        )

    if report.orphan_views:
        lines.extend([
            "",
            "## 有视图无路由（或 legacy 目录）",
            "",
            "> 可能是历史目录、子页面或待清理；**不自动建 spec**，人工确认。",
            "",
        ])
        for v in report.orphan_views:
            lines.append(f"- `views/{v}/`")

    if missing > 0:
        lines.extend([
            "",
            "## 缺口建议（缺失 spec）",
            "",
            "以下路由有代码、无 `docs/specs/` 主 spec，建议上线后 `【archive】` 或补录：",
            "",
        ])
        for r in report.routes:
            if r.spec_status == "缺失":
                lines.append(f"- `{r.path}` → `{r.spec_path}`（`views/{r.view_import}`）")

    lines.extend([
        "",
        "## 刷新命令",
        "",
        "```bash",
        "python3 .cursor/skills/scripts/spec-index.py",
        "python3 .cursor/skills/scripts/spec-index.py --check   # 有缺口则 exit 1",
        "```",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate docs/specs/_index.md")
    parser.add_argument("--check", action="store_true", help="exit 1 if spec gaps exist")
    parser.add_argument("--json", action="store_true", help="print JSON summary to stdout")
    parser.add_argument("--no-write", action="store_true", help="dry run, do not write file")
    args = parser.parse_args()

    report = build_report()
    md = render_markdown(report)

    if args.json:
        payload = {
            "routes": len(report.routes),
            "archived": sum(1 for r in report.routes if r.spec_status == "已归档"),
            "in_progress": sum(1 for r in report.routes if r.spec_status == "进行中"),
            "missing": sum(1 for r in report.routes if r.spec_status == "缺失"),
            "gaps": [
                {"path": r.path, "spec": r.spec_path, "view": r.view_import}
                for r in report.routes
                if r.spec_status == "缺失"
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    if not args.no_write:
        SPECS_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(md, encoding="utf-8")
        if not args.json:
            print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")
            print(f"Routes: {len(report.routes)} | Missing spec: {sum(1 for r in report.routes if r.spec_status == '缺失')}")

    if args.check and report.has_gaps:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
