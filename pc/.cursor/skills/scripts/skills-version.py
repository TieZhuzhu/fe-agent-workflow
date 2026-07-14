#!/usr/bin/env python3
"""Skills version manager — manifest.json is the source of truth."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SKILLS_ROOT / "manifest.json"

CATEGORIES = (
    "workflow",
    "ingest",
    "codegen",
    "integration",
    "quality",
    "maintenance",
    "infra",
)


def load_manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def save_manifest(data: dict) -> None:
    data["updatedAt"] = date.today().isoformat()
    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def skill_path(name: str) -> Path:
    return SKILLS_ROOT / name / "SKILL.md"


def read_frontmatter_version(content: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return None
    vm = re.search(r"^version:\s*([^\n]+)", m.group(1), re.MULTILINE)
    return vm.group(1).strip() if vm else None


def set_frontmatter_version(content: str, version: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        raise ValueError("SKILL.md missing YAML frontmatter")
    block = m.group(1).strip("\n")
    rest = content[m.end() :]

    if re.search(r"^version:", block, re.MULTILINE):
        block = re.sub(r"^version:.*$", f"version: {version}", block, count=1, flags=re.MULTILINE)
    else:
        block = re.sub(r"^(name: .+)$", rf"\1\nversion: {version}", block, count=1, flags=re.MULTILINE)

    return f"---\n{block}\n---{rest}"


def bump_version(current: str, level: str) -> str:
    parts = current.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"Invalid semver: {current}")
    major, minor, patch = (int(p) for p in parts)
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"Unknown level: {level}")


def cmd_sync(_: argparse.Namespace) -> int:
    data = load_manifest()
    errors: list[str] = []
    for entry in data["skills"]:
        name = entry["name"]
        version = entry["version"]
        path = skill_path(name)
        if not path.exists():
            errors.append(f"missing SKILL.md: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        path.write_text(set_frontmatter_version(text, version), encoding="utf-8")
        print(f"synced {name} -> {version}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"OK: synced {len(data['skills'])} skills")
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    data = load_manifest()
    manifest_names = {s["name"] for s in data["skills"]}
    errors: list[str] = []

    for entry in data["skills"]:
        name = entry["name"]
        expected = entry["version"]
        if not entry.get("description", "").strip():
            errors.append(f"{name}: missing description in manifest.json")
        path = skill_path(name)
        if not path.exists():
            errors.append(f"{name}: SKILL.md not found")
            continue
        actual = read_frontmatter_version(path.read_text(encoding="utf-8"))
        if actual != expected:
            errors.append(f"{name}: manifest={expected} skill={actual}")

    for d in SKILLS_ROOT.iterdir():
        if not d.is_dir() or d.name in ("shared", "scripts"):
            continue
        if (d / "SKILL.md").exists() and d.name not in manifest_names:
            errors.append(f"{d.name}: SKILL.md exists but not in manifest.json")

    if errors:
        print("CHECK FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK: {len(data['skills'])} skills match manifest.json")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    data = load_manifest()
    skills = data["skills"]
    if args.category:
        skills = [s for s in skills if s.get("category") == args.category]

    print(f"bundleVersion: {data.get('bundleVersion', '?')}  updatedAt: {data.get('updatedAt', '?')}")
    print(f"{'NAME':<32} {'VER':<8} {'CAT':<14} {'STATUS':<12} DESCRIPTION")
    print("-" * 100)
    for s in sorted(skills, key=lambda x: (x.get("category", ""), x["name"])):
        desc = s.get("description", "")
        print(f"{s['name']:<32} {s['version']:<8} {s.get('category', ''):<14} {s.get('status', 'stable'):<12} {desc}")
    return 0


def cmd_bump(args: argparse.Namespace) -> int:
    data = load_manifest()
    entry = next((s for s in data["skills"] if s["name"] == args.name), None)
    if not entry:
        print(f"ERROR: skill not in manifest: {args.name}", file=sys.stderr)
        return 1

    old = entry["version"]
    new = bump_version(old, args.level)
    entry["version"] = new

    if args.level in ("minor", "major"):
        bundle = data.get("bundleVersion", "1.0.0")
        try:
            data["bundleVersion"] = bump_version(bundle, "minor" if args.level == "minor" else "major")
        except ValueError:
            pass

    save_manifest(data)

    path = skill_path(args.name)
    if path.exists():
        text = path.read_text(encoding="utf-8")
        path.write_text(set_frontmatter_version(text, new), encoding="utf-8")

    print(f"bumped {args.name}: {old} -> {new}")
    if args.note:
        print(f"  note: {args.note}")
        print("  -> append to CHANGELOG.md")
    print(f"  bundleVersion: {data.get('bundleVersion')}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="HiStore Cursor Skills version manager")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("sync", help="Write manifest versions into all SKILL.md frontmatter")
    sub.add_parser("check", help="Verify manifest matches SKILL.md frontmatter")

    p_list = sub.add_parser("list", help="List skills from manifest")
    p_list.add_argument("--category", choices=CATEGORIES, help="Filter by category")

    p_bump = sub.add_parser("bump", help="Bump skill version in manifest (+ sync one file)")
    p_bump.add_argument("name", help="Skill name (directory name)")
    p_bump.add_argument("level", choices=["major", "minor", "patch"])
    p_bump.add_argument("note", nargs="?", default="", help="Changelog note reminder")

    args = parser.parse_args()
    handlers = {
        "sync": cmd_sync,
        "check": cmd_check,
        "list": cmd_list,
        "bump": cmd_bump,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
