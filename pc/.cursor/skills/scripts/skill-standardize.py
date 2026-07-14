#!/usr/bin/env python3
"""Standardize SKILL.md per shared/skill-conventions.md (Agent Skills best practices)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

SKILLS_ROOT = Path(__file__).resolve().parents[1]
META_PATH = SKILLS_ROOT / "shared" / "skill-metadata.yaml"

HEADER_MARKER = "**管控力度：**"
BOUNDARIES_MARKER = "## 操作边界"
DELIVERY_MARKER = "## 交付检查"


def load_meta() -> dict:
    with META_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_frontmatter(content: str) -> tuple[str, str, str]:
    m = re.match(r"^(---\n.*?\n---)(.*)$", content, re.DOTALL)
    if not m:
        raise ValueError("Missing frontmatter")
    block = m.group(1)
    body = m.group(2)
    inner = re.match(r"^---\n(.*?)\n---$", block, re.DOTALL)
    return block, inner.group(1) if inner else "", body


def set_description(inner: str, description: str) -> str:
    desc = description.strip().replace("\n", " ")
    if re.search(r"^description:", inner, re.MULTILINE):
        inner = re.sub(
            r"^description:.*?(?=\n[a-z_]+:|\Z)",
            f"description: {desc}",
            inner,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
    else:
        inner = re.sub(r"^(name: .+)$", rf"\1\ndescription: {desc}", inner, count=1, flags=re.MULTILINE)
    return inner


def build_header(risk: str) -> str:
    return (
        f"> **管控力度：** {risk} | "
        f"**规范：** [skill-conventions](../shared/skill-conventions.md) | "
        f"**边界：** [baseline](../shared/skill-boundaries-baseline.md) | "
        f"**工具：** [toolbox](../shared/project-toolbox.md)\n"
    )


def inject_header(body: str, risk: str) -> str:
    if HEADER_MARKER in body:
        body = re.sub(
            r"> \*\*管控力度：\*\*[^\n]+\n",
            build_header(risk),
            body,
            count=1,
        )
        return body

    # After first # title line
    m = re.match(r"(\n?#\s+[^\n]+\n)", body)
    if m:
        pos = m.end()
        return body[:pos] + "\n" + build_header(risk) + body[pos:]

    return build_header(risk) + "\n" + body


def build_boundaries_section(extra: str) -> str:
    extra = extra.strip()
    return (
        f"{BOUNDARIES_MARKER}\n\n"
        f"基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)\n\n"
        f"{extra}\n"
    )


def build_delivery_section(items: str) -> str:
    items = items.strip()
    # Support metadata as plain checklist or structured blocks
    if "**汇报" in items or "**门禁" in items:
        body = items
    else:
        lines = [ln.strip() for ln in items.splitlines() if ln.strip()]
        checks = "\n".join(f"- [ ] {ln.lstrip('- [ ] ')}" for ln in lines)
        body = f"**门禁**\n\n{checks}"
    return f"{DELIVERY_MARKER}\n\n{body}\n"


def upsert_section(body: str, marker: str, section: str) -> str:
    if marker in body:
        pattern = rf"{re.escape(marker)}\n.*?(?=\n## |\Z)"
        return re.sub(pattern, section.rstrip() + "\n", body, count=1, flags=re.DOTALL)
    # Insert before ## 禁止 or at end
    forbid = re.search(r"\n## 禁止", body)
    if forbid:
        return body[: forbid.start()] + "\n" + section + body[forbid.start() :]
    return body.rstrip() + "\n\n" + section


def standardize_skill(name: str, meta: dict, dry_run: bool = False) -> list[str]:
    changes: list[str] = []
    skill_md = SKILLS_ROOT / name / "SKILL.md"
    if not skill_md.exists():
        return [f"SKIP {name}: no SKILL.md"]

    content = skill_md.read_text(encoding="utf-8")
    original = content

    block, inner, body = parse_frontmatter(content)
    inner = set_description(inner, meta["description"])
    new_block = f"---\n{inner}\n---"

    body = inject_header(body, meta["risk"])
    body = upsert_section(body, BOUNDARIES_MARKER, build_boundaries_section(meta["boundaries"]))
    body = upsert_section(body, DELIVERY_MARKER, build_delivery_section(meta["delivery"]))

    content = new_block + body
    if not content.endswith("\n"):
        content += "\n"

    if content != original:
        changes.append(name)
        if not dry_run:
            skill_md.write_text(content, encoding="utf-8")

    return changes


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Standardize all SKILL.md files")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skill", help="Single skill name")
    args = parser.parse_args()

    meta_all = load_meta()
    names = [args.skill] if args.skill else list(meta_all.keys())

    updated: list[str] = []
    for name in names:
        if name not in meta_all:
            print(f"Unknown skill: {name}", file=sys.stderr)
            return 1
        updated.extend(standardize_skill(name, meta_all[name], dry_run=args.dry_run))

    action = "would update" if args.dry_run else "updated"
    print(f"{action} {len(updated)} skills:")
    for n in updated:
        print(f"  - {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
