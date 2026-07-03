#!/usr/bin/env python3
"""Generate output/repo-summary.md from data/processed/repos.jsonl.

The summary is what the workshop paper cites: counts per language pair,
star distribution, license distribution, monorepo flag, top repos.

Usage:
    uv run scripts/summarize.py
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
PROCESSED = SUB_STEP_DIR / "data" / "processed" / "repos.jsonl"
OUTPUT = SUB_STEP_DIR / "output" / "repo-summary.md"


def fmt_int(n: int) -> str:
    return f"{n:,}"


def main() -> int:
    if not PROCESSED.exists():
        print(f"missing {PROCESSED}; run filter_repos.py first", file=sys.stderr)
        return 1
    with PROCESSED.open() as f:
        repos = [json.loads(line) for line in f]
    if not repos:
        print("repos.jsonl is empty", file=sys.stderr)
        return 1

    by_pair: dict[str, list[dict]] = {}
    for r in repos:
        by_pair.setdefault(r["language_pair"], []).append(r)

    lines: list[str] = []
    lines.append("# Repo Mining Summary")
    lines.append("")
    lines.append(f"**Total repos accepted:** {len(repos)}")
    lines.append("")
    lines.append("## By language pair")
    lines.append("")
    lines.append("| Pair | Count | Median stars | Min stars | Max stars |")
    lines.append("|------|------:|-------------:|----------:|----------:|")
    for pair, group in sorted(by_pair.items()):
        stars = [r["stars"] for r in group]
        lines.append(
            f"| {pair} | {len(group)} | "
            f"{fmt_int(int(statistics.median(stars)))} | "
            f"{fmt_int(min(stars))} | {fmt_int(max(stars))} |"
        )
    lines.append("")

    lines.append("## License distribution")
    lines.append("")
    lic_counts = Counter(r.get("license") or "(none)" for r in repos)
    lines.append("| License | Count |")
    lines.append("|---------|------:|")
    for lic, cnt in lic_counts.most_common():
        lines.append(f"| {lic} | {cnt} |")
    lines.append("")

    lines.append("## CI / test markers")
    lines.append("")
    has_ci = sum(1 for r in repos if r.get("has_ci"))
    has_tests = sum(1 for r in repos if r.get("has_tests"))
    lines.append(f"- Repos with CI markers: **{has_ci} / {len(repos)}**")
    lines.append(f"- Repos with test markers: **{has_tests} / {len(repos)}**")
    lines.append("")

    for pair, group in sorted(by_pair.items()):
        lines.append(f"## Top repos — {pair}")
        lines.append("")
        l1, l2 = (
            ("Java", "TypeScript") if pair == "java-ts" else ("Python", "Go")
        )
        lines.append(f"| Stars | Repo | {l1}% | {l2}% | License |")
        lines.append("|------:|------|------:|------:|---------|")
        for r in sorted(group, key=lambda x: -x["stars"])[:20]:
            langs = r["languages_bytes"]
            total = sum(langs.values()) or 1
            p1 = 100 * langs.get(l1, 0) / total
            p2 = 100 * langs.get(l2, 0) / total
            lines.append(
                f"| {fmt_int(r['stars'])} | [{r['owner']}/{r['name']}]({r['url']}) "
                f"| {p1:.1f} | {p2:.1f} | {r.get('license') or 'NONE'} |"
            )
        lines.append("")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines))
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
