#!/usr/bin/env python3
"""Sync manifest.json descriptions from skill-metadata.yaml and bump patch versions."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

SKILLS_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = SKILLS_ROOT / "manifest.json"
META = SKILLS_ROOT / "shared" / "skill-metadata.yaml"


def bump_patch(v: str) -> str:
    parts = v.split(".")
    return f"{parts[0]}.{parts[1]}.{int(parts[2]) + 1}"


def short_desc(full: str, max_len: int = 120) -> str:
    s = " ".join(full.split())
    if len(s) <= max_len:
        return s
    cut = s[: max_len - 3].rsplit("。", 1)[0]
    return cut + "…" if cut else s[: max_len - 3] + "…"


def main() -> int:
    with META.open(encoding="utf-8") as f:
        meta = yaml.safe_load(f)
    with MANIFEST.open(encoding="utf-8") as f:
        data = json.load(f)

    data["bundleVersion"] = "1.3.0"
    data["updatedAt"] = date.today().isoformat()

    for entry in data["skills"]:
        name = entry["name"]
        if name not in meta:
            print(f"WARN: {name} not in skill-metadata.yaml", file=sys.stderr)
            continue
        entry["version"] = bump_patch(entry["version"])
        entry["description"] = short_desc(meta[name]["description"])

    with MANIFEST.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"manifest -> bundle {data['bundleVersion']}, {len(data['skills'])} skills patch-bumped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
