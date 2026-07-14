#!/usr/bin/env python3
"""Scan pages.json and generate docs/specs/_index.md (uni-app).

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
PAGES_JSON = REPO_ROOT / "pages.json"
SPECS_DIR = REPO_ROOT / "docs" / "specs"
FEATURES_DIR = REPO_ROOT / "docs" / "features"
OUTPUT = SPECS_DIR / "_index.md"

SKIP_PATH_EXACT = {
    "pages/login/login",
}
SKIP_PATH_SUFFIXES = ("/webview",)


@dataclass
class RouteEntry:
    path: str
    title: str
    view_file: str
    module: str
    page_dir: str
    spec_path: str
    spec_status: str
    feature_slug: str = ""
    note: str = ""


@dataclass
class IndexReport:
    routes: list[RouteEntry] = field(default_factory=list)
    orphan_pages: list[str] = field(default_factory=list)

    @property
    def gaps(self) -> list[RouteEntry]:
        return [r for r in self.routes if r.spec_status in ("缺失", "进行中")]

    @property
    def has_gaps(self) -> bool:
        return len(self.gaps) > 0


def load_pages_json() -> dict:
    if not PAGES_JSON.exists():
        return {}
    text = PAGES_JSON.read_text(encoding="utf-8")
    lines: list[str] = []
    skip_conditional = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("//") and "#ifdef" in stripped:
            skip_conditional = True
            continue
        if skip_conditional:
            if "#endif" in stripped:
                skip_conditional = False
            continue
        cleaned = re.sub(r"//.*$", "", line)
        if cleaned.strip():
            lines.append(cleaned)
    content = "\n".join(lines)
    content = re.sub(r",(\s*[}\]])", r"\1", content)
    return json.loads(content)


def extract_title(page_obj: dict) -> str:
    style = page_obj.get("style") or {}
    return style.get("navigationBarTitleText") or ""


def path_to_module_page(full_path: str) -> tuple[str, str, str]:
    """Return (module, page_dir, spec relative path under docs/specs/)."""
    parts = full_path.split("/")
    if full_path.startswith("subPackages/") and len(parts) >= 3:
        module = parts[1]
        page_dir = parts[2] if len(parts) == 3 else parts[-1].removesuffix(".vue")
    elif full_path.startswith("pages/") and len(parts) >= 3:
        module = parts[1]
        page_dir = parts[2]
    else:
        module = parts[1] if len(parts) > 1 else "unknown"
        page_dir = parts[-1]
    spec_rel = f"{module}/{page_dir}.md"
    return module, page_dir, spec_rel


def resolve_view_file(full_path: str) -> Path | None:
    candidates = [
        REPO_ROOT / f"{full_path}.vue",
        REPO_ROOT / full_path / "index.vue",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def read_pages_routes() -> list[tuple[str, str]]:
    """Return list of (full_path, title)."""
    data = load_pages_json()
    entries: list[tuple[str, str]] = []

    for page in data.get("pages", []):
        path = page.get("path", "")
        if not path:
            continue
        if path in SKIP_PATH_EXACT or any(path.endswith(s) for s in SKIP_PATH_SUFFIXES):
            continue
        entries.append((path, extract_title(page)))

    for sub in data.get("subPackages", []):
        root = sub.get("root", "").rstrip("/")
        for page in sub.get("pages", []):
            rel = page.get("path", "")
            if not rel or not root:
                continue
            full = f"{root}/{rel}".replace("//", "/")
            if full in SKIP_PATH_EXACT:
                continue
            entries.append((full, extract_title(page)))

    return entries


def find_active_feature(full_path: str) -> str:
    if not FEATURES_DIR.is_dir():
        return ""
    view_norm = full_path.replace("\\", "/")

    for entry in sorted(FEATURES_DIR.iterdir()):
        if not entry.is_dir() or entry.name in ("_template", "archive"):
            continue
        proposal = entry / "proposal.md"
        if proposal.exists():
            status = re.search(
                r"Status:\s*\*?\*?(\w+)\*?\*?",
                proposal.read_text(encoding="utf-8"),
                re.I,
            )
            if status and status.group(1).lower() in ("archived", "implemented"):
                continue
        design_text = (
            (entry / "design.md").read_text(encoding="utf-8", errors="ignore")
            if (entry / "design.md").exists()
            else ""
        )
        if not design_text:
            continue
        markers = (
            view_norm,
            f"`{view_norm}`",
            f"`{view_norm}.vue`",
            f"| `{full_path}` |",
            f"| {full_path} |",
        )
        if any(m in design_text for m in markers):
            return entry.name
        slug_parts = entry.name.split("-")
        if len(slug_parts) >= 2:
            guess = "/".join(slug_parts[:2]) if len(slug_parts) == 2 else f"{slug_parts[0]}/{'-'.join(slug_parts[1:])}"
            if view_norm.endswith(guess) or guess in view_norm:
                return entry.name
    return ""


def spec_status(spec_rel: str, feature_slug: str) -> str:
    spec_file = SPECS_DIR / spec_rel
    if spec_file.exists():
        return "已归档"
    if feature_slug:
        return "进行中"
    return "缺失"


def collect_orphan_pages(routed_paths: set[str]) -> list[str]:
    orphans: list[str] = []
    for base in (REPO_ROOT / "pages", REPO_ROOT / "subPackages"):
        if not base.is_dir():
            continue
        for vue in base.rglob("*.vue"):
            rel = vue.relative_to(REPO_ROOT).as_posix().removesuffix(".vue")
            if rel in SKIP_PATH_EXACT:
                continue
            if "/components/" in rel:
                continue
            if rel not in routed_paths:
                orphans.append(rel)
    return sorted(set(orphans))


def build_report() -> IndexReport:
    report = IndexReport()
    routed_paths: set[str] = set()

    for full_path, title in read_pages_routes():
        routed_paths.add(full_path)
        view_file = resolve_view_file(full_path)
        module, page_dir, spec_rel = path_to_module_page(full_path)
        feature_slug = find_active_feature(full_path)
        status = spec_status(spec_rel, feature_slug)
        note = ""
        if view_file is None:
            note = "页面文件未找到"
        report.routes.append(
            RouteEntry(
                path=full_path,
                title=title,
                view_file=str(view_file.relative_to(REPO_ROOT)) if view_file else "—",
                module=module,
                page_dir=page_dir,
                spec_path=f"docs/specs/{spec_rel}",
                spec_status=status,
                feature_slug=feature_slug,
                note=note,
            )
        )

    report.orphan_pages = collect_orphan_pages(routed_paths)
    return report


def render_markdown(report: IndexReport) -> str:
    today = date.today().isoformat()
    total = len(report.routes)
    archived = sum(1 for r in report.routes if r.spec_status == "已归档")
    in_progress = sum(1 for r in report.routes if r.spec_status == "进行中")
    missing = sum(1 for r in report.routes if r.spec_status == "缺失")

    lines = [
        "# Spec 索引（页面 ↔ pages.json ↔ 规格）",
        "",
        f"> 由 `project-bootstrap` / `spec-index.py` 生成，日期：{today}",
        "> 权威行为 spec：`docs/specs/<module>/<page>.md`；进行中变更：`docs/features/<slug>/`",
        "",
        "## 统计",
        "",
        "| 指标 | 数量 |",
        "|------|------|",
        f"| 注册页面 path | {total} |",
        f"| 已归档 spec | {archived} |",
        f"| 进行中 feature | {in_progress} |",
        f"| **缺失 spec** | **{missing}** |",
        "",
        "## 页面索引",
        "",
        "| 模块 | pages.json path | 标题 | 页面文件 | 主 spec | 状态 | 进行中 feature |",
        "|------|-----------------|------|----------|---------|------|----------------|",
    ]

    for r in sorted(report.routes, key=lambda x: (x.module, x.path)):
        spec_link = r.spec_path if r.spec_status == "已归档" else "—"
        feat = r.feature_slug or "—"
        view = f"`{r.view_file}`" if r.view_file != "—" else "—"
        lines.append(
            f"| {r.module} | `{r.path}` | {r.title} | {view} | {spec_link} | {r.spec_status} | {feat} |"
        )

    if report.orphan_pages:
        lines.extend([
            "",
            "## 有文件无 pages.json 注册",
            "",
            "> 可能是历史目录、子组件或待清理；**不自动建 spec**，人工确认。",
            "",
        ])
        for v in report.orphan_pages[:30]:
            lines.append(f"- `{v}.vue`")
        if len(report.orphan_pages) > 30:
            lines.append(f"- … 另有 {len(report.orphan_pages) - 30} 项")

    if missing > 0:
        lines.extend([
            "",
            "## 缺口建议（缺失 spec）",
            "",
            "以下页面有代码、无 `docs/specs/` 主 spec，建议上线后 `【archive】` 或补录：",
            "",
        ])
        for r in report.routes:
            if r.spec_status == "缺失":
                lines.append(f"- `{r.path}` → `{r.spec_path}`（`{r.view_file}`）")

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
    parser = argparse.ArgumentParser(description="Generate docs/specs/_index.md (uni-app)")
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
                {"path": r.path, "spec": r.spec_path, "view": r.view_file}
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
            print(f"Pages: {len(report.routes)} | Missing spec: {sum(1 for r in report.routes if r.spec_status == '缺失')}")

    if args.check and report.has_gaps:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
