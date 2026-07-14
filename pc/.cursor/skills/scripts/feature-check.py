#!/usr/bin/env python3
"""Feature SDD gate — static checks + optional lint/build.

Usage:
  python3 .cursor/skills/scripts/feature-check.py list
  python3 .cursor/skills/scripts/feature-check.py board
  python3 .cursor/skills/scripts/feature-check.py spec <slug>
  python3 .cursor/skills/scripts/feature-check.py analyze <slug>
  python3 .cursor/skills/scripts/feature-check.py verify <slug> [--no-build] [--no-lint]
  python3 .cursor/skills/scripts/feature-check.py archive-ready <slug>
  python3 .cursor/skills/scripts/feature-check.py sync-status <slug> [--set STATUS]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_ROOT = SCRIPT_DIR.parent
REPO_ROOT = SKILLS_ROOT.parent.parent
FEATURES_DIR = REPO_ROOT / "docs" / "features"
ARCHIVE_DIR = FEATURES_DIR / "archive"

REQUIRED_FILES = ("proposal.md", "spec.md", "design.md", "tasks.md", "field-map.md")
READY_STATUSES = {"ready", "implemented"}
BLOCKER_MARKERS = ("[待确认]", "TBD", "???")
NON_BLOCKER_TAG = "[待确认-低]"

# 团队确认的 blocker 级待确认（阻断 proposal ready）
BLOCKER_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("路由 path 未定义", re.compile(r"path\s*未定义|路由\s*未定义|path:\s*`?/?\.\.\.|path\s*:\s*[`']/?[`']", re.I)),
    ("主接口 URL 未知", re.compile(r"接口\s*URL\s*未知|主列表.*未知|提交接口.*未知|接口\s*待后端|接口\s*未就绪.*无\s*URL", re.I)),
    ("业务模块未定义", re.compile(r"模块\s*未定义|所属模块\s*未知|module\s*未定义", re.I)),
    ("权限模型无决策", re.compile(r"权限模型.*不一致.*无决策|权限.*\[待确认\](?!-低)", re.I)),
    ("页面冲突未解决", re.compile(r"重复\s*path|重复功能|与现有页面冲突.*\[待确认\]", re.I)),
)

FILE_PATH_RE = re.compile(
    r"`((?:src/)?(?:views|components|store|config|router)/[^`\s]+)`|"
    r"((?:src/)?(?:views|components|store|config|router)/[\w./-]+\.(?:vue|js|ts|scss))"
)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""
    critical: bool = True


@dataclass
class Report:
    command: str
    slug: str
    results: list[CheckResult] = field(default_factory=list)

    def add(self, name: str, passed: bool, detail: str = "", *, critical: bool = True) -> None:
        self.results.append(CheckResult(name, passed, detail, critical))

    @property
    def critical_failures(self) -> list[CheckResult]:
        return [r for r in self.results if r.critical and not r.passed]

    @property
    def passed(self) -> bool:
        return len(self.critical_failures) == 0

    def print_report(self) -> None:
        print(f"\n## Feature Check: {self.slug} ({self.command})")
        print("| 检查项 | 结果 | 说明 |")
        print("|--------|------|------|")
        for r in self.results:
            status = "pass" if r.passed else ("FAIL" if r.critical else "warn")
            detail = r.detail.replace("|", "\\|")
            print(f"| {r.name} | {status} | {detail} |")
        verdict = "PASS" if self.passed else "FAIL"
        print(f"\n**Verdict: {verdict}**")
        if self.critical_failures:
            print("\n### Blockers")
            for r in self.critical_failures:
                print(f"- {r.name}: {r.detail}")


def feature_dir(slug: str) -> Path:
    direct = FEATURES_DIR / slug
    if direct.is_dir():
        return direct
    archived = sorted(ARCHIVE_DIR.glob(f"*-{slug}"))
    if archived:
        return archived[-1]
    sys.exit(f"Feature not found: {slug} (looked in docs/features/ and archive/)")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def list_features() -> list[tuple[str, str, Path]]:
    items: list[tuple[str, str, Path]] = []
    if not FEATURES_DIR.is_dir():
        return items
    for entry in sorted(FEATURES_DIR.iterdir()):
        if not entry.is_dir() or entry.name in ("_template", "archive"):
            continue
        status = parse_proposal_status(read_text(entry / "proposal.md"))
        items.append((entry.name, status, entry))
    if ARCHIVE_DIR.is_dir():
        for entry in sorted(ARCHIVE_DIR.iterdir()):
            if not entry.is_dir():
                continue
            name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", entry.name)
            status = parse_proposal_status(read_text(entry / "proposal.md")) or "archived"
            items.append((name, status, entry))
    return items


def parse_proposal_status(content: str) -> str:
    m = re.search(r"Status:\s*\*?\*?(\w+)\*?\*?", content, re.I)
    return m.group(1).lower() if m else "unknown"


def count_blockers(content: str) -> list[str]:
    hits: list[str] = []
    for line_no, line in enumerate(content.splitlines(), 1):
        if NON_BLOCKER_TAG in line:
            continue
        if not any(marker in line for marker in BLOCKER_MARKERS):
            continue
        for label, pattern in BLOCKER_PATTERNS:
            if pattern.search(line):
                hits.append(f"L{line_no} {label}: {line.strip()[:80]}")
                break
        else:
            if "[待确认]" in line:
                hits.append(f"L{line_no} [待确认]: {line.strip()[:80]}")
    return hits


def extract_design_paths(design_content: str) -> list[str]:
    paths: set[str] = set()
    for m in FILE_PATH_RE.finditer(design_content):
        p = m.group(1) or m.group(2)
        if not p:
            continue
        p = p.lstrip("`")
        if "<" in p or ">" in p or "*" in p:
            continue
        if any(x in p for x in ("mock/", "manageDetailMock", "mockOrders", "systemNoticeMock")):
            continue
        paths.add(p)
    return sorted(paths)


def parse_tasks(tasks_content: str) -> tuple[int, int, list[str]]:
    unchecked: list[str] = []
    done = 0
    total = 0
    in_backlog = False
    for line in tasks_content.splitlines():
        if re.match(r"^##\s+.*(backlog|后续阶段|Out of Scope)", line, re.I):
            in_backlog = True
            continue
        if re.match(r"^##\s+", line) and not re.match(r"^##\s+.*(backlog|后续阶段|Out of Scope)", line, re.I):
            in_backlog = False
        if in_backlog:
            continue
        if re.match(r"^-\s+\[[ xX]\]", line):
            total += 1
            if re.match(r"^-\s+\[[xX]\]", line):
                done += 1
            else:
                unchecked.append(line.strip())
    return done, total, unchecked


def is_project_wide(design_content: str) -> bool:
    return "全项目治理" in design_content or "非单页新建" in design_content


def field_map_ok(content: str) -> bool:
    text = content.strip()
    if not text:
        return False
    if re.search(r"N/A|无联调|不新增接口", text, re.I):
        return True
    return "|" in text and ("字段" in text or "Query" in text or "prop" in text)


def npm_script(name: str) -> str | None:
    pkg = REPO_ROOT / "package.json"
    if not pkg.exists():
        return None
    import json

    data = json.loads(pkg.read_text(encoding="utf-8"))
    scripts = data.get("scripts", {})
    if name in scripts:
        return name
    aliases = {
        "lint": ("lint-fix", "lint"),
        "build": ("build", "build:test"),
    }
    for candidate in aliases.get(name, (name,)):
        if candidate in scripts:
            return candidate
    return None


def run_npm(script: str) -> tuple[bool, str]:
    cmd = ["npm", "run", script]
    try:
        proc = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=600,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        tail = "\n".join(output.splitlines()[-20:])
        return proc.returncode == 0, tail
    except subprocess.TimeoutExpired:
        return False, "timeout after 600s"
    except FileNotFoundError:
        return False, "npm not found"


def check_spec(slug: str) -> Report:
    report = Report("spec", slug)
    fdir = feature_dir(slug)

    for fname in REQUIRED_FILES:
        path = fdir / fname
        report.add(f"artifact:{fname}", path.exists() and path.stat().st_size > 0, str(path.relative_to(REPO_ROOT)))

    proposal = read_text(fdir / "proposal.md")
    status = parse_proposal_status(proposal)
    report.add("proposal:Status", status in READY_STATUSES, f"Status={status}")

    combined = "\n".join(read_text(fdir / f) for f in REQUIRED_FILES if (fdir / f).exists())
    blockers = count_blockers(combined)
    report.add("clarify:blockers", len(blockers) == 0, f"{len(blockers)} blocker(s)", critical=len(blockers) > 0)
    for b in blockers[:5]:
        report.add("clarify:detail", False, b, critical=True)

    spec = read_text(fdir / "spec.md")
    has_scenario = bool(re.search(r"Given|When|Then|验收场景", spec, re.I))
    report.add("spec:scenarios", has_scenario, "≥1 acceptance scenario")

    design = read_text(fdir / "design.md")
    if is_project_wide(design):
        report.add("design:page-type", True, "全项目治理（页面类型非 blocker）", critical=False)
    else:
        has_type = bool(re.search(r"列表页|表单页|详情页|复杂页|页面类型", design))
        report.add("design:page-type", has_type, "页面类型已描述", critical=False)

    fmap = read_text(fdir / "field-map.md")
    report.add("field-map", field_map_ok(fmap), "N/A or mapping table")

    return report


def check_verify(slug: str, *, run_lint: bool, run_build: bool) -> Report:
    report = check_spec(slug)
    report.command = "verify"
    fdir = feature_dir(slug)
    design = read_text(fdir / "design.md")
    tasks = read_text(fdir / "tasks.md")

    done, total, unchecked = parse_tasks(tasks)
    report.add(
        "tasks:complete",
        len(unchecked) == 0,
        f"{done}/{total} done; {len(unchecked)} open",
    )
    for item in unchecked[:8]:
        report.add("tasks:open", False, item, critical=False)

    paths = extract_design_paths(design)
    missing: list[str] = []
    for rel in paths:
        full = REPO_ROOT / rel
        if not full.exists():
            alt = REPO_ROOT / "src" / rel.removeprefix("src/")
            if not alt.exists():
                missing.append(rel)
    project_wide = is_project_wide(design)
    if paths and not project_wide:
        report.add(
            "design:files",
            len(missing) == 0,
            f"{len(paths) - len(missing)}/{len(paths)} exist",
        )
        for m in missing[:10]:
            report.add("design:missing", False, m)
    elif paths and project_wide:
        report.add(
            "design:files",
            True,
            f"{len(paths) - len(missing)}/{len(paths)} exist（全项目治理，缺失仅 warn）",
            critical=False,
        )
        for m in missing[:5]:
            report.add("design:missing", False, m, critical=False)

    if run_lint:
        lint_script = npm_script("lint")
        if lint_script:
            ok, tail = run_npm(lint_script)
            report.add(f"lint:{lint_script}", ok, tail[-200:] if tail else "")
        else:
            report.add("lint", True, "no lint script — skip", critical=False)

    if run_build:
        build_script = npm_script("build")
        if build_script:
            ok, tail = run_npm(build_script)
            report.add(f"build:{build_script}", ok, tail[-200:] if tail else "")
        else:
            report.add("build", False, "no build script in package.json")

    return report


def check_archive_ready(slug: str) -> Report:
    report = check_verify(slug, run_lint=False, run_build=False)
    report.command = "archive-ready"
    fdir = feature_dir(slug)
    if fdir.parent.name == "archive":
        report.add("archive:location", False, "already archived")
    proposal = read_text(fdir / "proposal.md")
    status = parse_proposal_status(proposal)
    report.add("archive:status", status in {"implemented", "ready"}, f"Status={status}")
    return report


def read_status_yaml(fdir: Path) -> dict[str, str]:
    path = fdir / "status.yaml"
    data: dict[str, str] = {}
    if not path.exists():
        return data
    current_section = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":") and ": " not in line:
            current_section = line[:-1]
            continue
        if ": " in line:
            key, val = line.split(": ", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            full_key = f"{current_section}.{key}" if current_section else key
            data[full_key] = val
    return data


def infer_workflow_status(fdir: Path) -> str:
    yaml_status = read_status_yaml(fdir).get("status", "")
    if yaml_status:
        return yaml_status
    proposal = parse_proposal_status(read_text(fdir / "proposal.md"))
    if proposal == "archived" or fdir.parent.name == "archive":
        return "archived"
    if proposal == "implemented":
        return "done"
    if proposal == "ready":
        _, total, unchecked = parse_tasks(read_text(fdir / "tasks.md"))
        if total and unchecked:
            return "implementing"
        return "ready"
    return "draft"


def sync_status_yaml(slug: str, *, set_status: str | None = None) -> Path:
    fdir = feature_dir(slug)
    path = fdir / "status.yaml"
    existing = read_status_yaml(fdir)
    today = date.today().isoformat()
    status = set_status or existing.get("status") or infer_workflow_status(fdir)
    proposal = parse_proposal_status(read_text(fdir / "proposal.md"))
    if proposal == "ready" and status == "draft":
        status = "ready"
    done, total, unchecked = parse_tasks(read_text(fdir / "tasks.md"))
    if status == "ready" and total and unchecked:
        status = "implementing"
    if total and not unchecked and status in ("implementing", "ready"):
        status = "verifying"

    created = existing.get("created", today)
    owner = existing.get("owner", "")
    l1 = existing.get("verify.l1", "pending")
    l2 = existing.get("verify.l2", "skip")
    l3 = existing.get("verify.l3", "skip")
    pr = existing.get("links.pr", "")
    ticket = existing.get("links.ticket", "")

    content = f"""# Feature 状态 — 由 feature-check sync-status 维护
slug: {slug}
status: {status}

owner: "{owner}"
created: {created}
updated: {today}

blockers: []

verify:
  l1: {l1}
  l2: {l2}
  l3: {l3}

links:
  pr: "{pr}"
  ticket: "{ticket}"
"""
    path.write_text(content, encoding="utf-8")
    return path


def extract_fr_ids(spec_content: str) -> list[str]:
    return re.findall(r"FR-\d+", spec_content, re.I)


def extract_task_file_refs(tasks_content: str) -> list[str]:
    refs: set[str] = set()
    for m in re.finditer(r"`((?:src/)?(?:views|components)/[^`]+)`", tasks_content):
        refs.add(m.group(1))
    for m in re.finditer(r"(views/[\w./-]+)", tasks_content):
        if "." in m.group(1) or "/" in m.group(1):
            refs.add(m.group(1))
    return sorted(refs)


def check_analyze(slug: str) -> Report:
    report = Report("analyze", slug)
    fdir = feature_dir(slug)
    spec = read_text(fdir / "spec.md")
    design = read_text(fdir / "design.md")
    tasks = read_text(fdir / "tasks.md")
    fmap = read_text(fdir / "field-map.md")
    e2e = read_text(fdir / "e2e.md")

    # spec ↔ design
    frs = extract_fr_ids(spec)
    has_user_story = bool(re.search(r"用户故事|作为.*希望", spec))
    design_has_scope = bool(re.search(r"文件清单|接口|path|页面类型", design))
    spec_design_ok = (not frs or design_has_scope) and (has_user_story or re.search(r"Given|When|Then", spec, re.I))
    report.add("spec↔design", spec_design_ok, f"FR={len(frs)} design_scope={design_has_scope}")

    # design ↔ tasks
    design_paths = extract_design_paths(design)
    task_refs = extract_task_file_refs(tasks)
    _, total, _ = parse_tasks(tasks)
    tasks_ok = total >= 3 and (bool(design_paths) or bool(task_refs) or is_project_wide(design))
    report.add("design↔tasks", tasks_ok, f"tasks={total} design_files={len(design_paths)}")

    # design ↔ field-map
    has_api_in_design = bool(re.search(r"接口|services|Get|Post|url", design, re.I))
    fmap_ok = field_map_ok(fmap) or not has_api_in_design or is_project_wide(design)
    report.add("design↔field-map", fmap_ok, "N/A or mapped" if fmap_ok else "missing mapping")

    # path ↔ 目录
    if is_project_wide(design):
        report.add("path↔目录", True, "全项目治理 N/A", critical=False)
    else:
        path_ok = bool(re.search(r"path|views/", design))
        report.add("path↔目录", path_ok, "path and views planned")

    # clarify
    blockers = count_blockers("\n".join(read_text(fdir / f) for f in REQUIRED_FILES if (fdir / f).exists()))
    report.add("clarify:blockers", len(blockers) == 0, f"{len(blockers)} blocker(s)")

    # spec ↔ e2e
    if re.search(r"Given|When|Then", spec, re.I) and not e2e.strip():
        report.add("spec↔e2e", False, "e2e.md 缺失", critical=False)
    elif e2e.strip():
        report.add("spec↔e2e", bool(re.search(r"步骤|P0|Given", e2e, re.I)), "e2e steps present", critical=False)
    else:
        report.add("spec↔e2e", True, "skip", critical=False)

    critical = len(report.critical_failures)
    warnings = len([r for r in report.results if not r.critical and not r.passed])
    report.add("summary:CRITICAL", critical == 0, f"{critical}", critical=critical > 0)
    report.add("summary:WARNING", warnings == 0, f"{warnings}", critical=False)
    return report


def cmd_board(_: argparse.Namespace) -> int:
    print("| slug | workflow | proposal | tasks | L1 | path |")
    print("|------|----------|----------|-------|-----|------|")
    for slug, proposal_status, fdir in list_features():
        if fdir.parent.name == "archive":
            continue
        wf = infer_workflow_status(fdir)
        yaml_data = read_status_yaml(fdir)
        l1 = yaml_data.get("verify.l1", "—")
        done, total, unchecked = parse_tasks(read_text(fdir / "tasks.md"))
        tasks_col = f"{done}/{total}" if total else "—"
        print(f"| {slug} | {wf} | {proposal_status} | {tasks_col} | {l1} | {fdir.relative_to(REPO_ROOT)} |")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    rows = list_features()
    print("| slug | Status | path |")
    print("|------|--------|------|")
    for slug, status, path in rows:
        print(f"| {slug} | {status} | {path.relative_to(REPO_ROOT)} |")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Feature SDD gate checks")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list")
    sub.add_parser("board")

    p_spec = sub.add_parser("spec")
    p_spec.add_argument("slug")

    p_analyze = sub.add_parser("analyze")
    p_analyze.add_argument("slug")

    p_verify = sub.add_parser("verify")
    p_verify.add_argument("slug")
    p_verify.add_argument("--no-build", action="store_true", help="skip npm run build")
    p_verify.add_argument("--no-lint", action="store_true", help="skip npm run lint-fix")

    p_arch = sub.add_parser("archive-ready")
    p_arch.add_argument("slug")

    p_sync = sub.add_parser("sync-status")
    p_sync.add_argument("slug")
    p_sync.add_argument("--set", dest="set_status", help="workflow status to set")

    args = parser.parse_args()

    if args.command == "list":
        return cmd_list(args)
    if args.command == "board":
        return cmd_board(args)

    slug: str = getattr(args, "slug", "")
    if args.command == "sync-status":
        path = sync_status_yaml(slug, set_status=args.set_status)
        print(f"Synced {path.relative_to(REPO_ROOT)}")
        return 0
    if args.command == "spec":
        report = check_spec(slug)
    elif args.command == "analyze":
        report = check_analyze(slug)
    elif args.command == "verify":
        report = check_verify(slug, run_lint=not args.no_lint, run_build=not args.no_build)
    else:
        report = check_archive_ready(slug)

    report.print_report()
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
