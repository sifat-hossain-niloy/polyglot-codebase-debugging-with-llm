#!/usr/bin/env python3
"""Generate output/bug-stats.md from data/processed/bugs.jsonl and skipped.jsonl.

Used by the FSE paper's §3 (Empirical Study). Every number that appears in
the paper text should be traceable back to this output.

Usage:
    uv run scripts/bug_stats.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
BUGS = SUB_STEP_DIR / "data" / "processed" / "bugs.jsonl"
SKIPS = SUB_STEP_DIR / "data" / "processed" / "skipped.jsonl"
OUT = SUB_STEP_DIR / "output" / "bug-stats.md"


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return [json.loads(l) for l in f]


def main() -> int:
    bugs = load_jsonl(BUGS)
    skips = load_jsonl(SKIPS)
    total = len(bugs) + len(skips)

    lines: list[str] = []
    lines.append("# Bug Annotation Stats")
    lines.append("")
    lines.append(f"**Total PRs reviewed:** {total}")
    lines.append(f"**Confirmed cross-language bugs:** {len(bugs)} ({100*len(bugs)/total:.0f}%)")
    lines.append(f"**Skipped:** {len(skips)} ({100*len(skips)/total:.0f}%)")
    lines.append("")

    if not bugs:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text("\n".join(lines) + "\n(No annotations yet.)\n")
        return 0

    # By pair
    by_pair = Counter(b["language_pair"] for b in bugs)
    lines.append("## Confirmed bugs — by language pair")
    lines.append("")
    lines.append("| Pair | Count |")
    lines.append("|------|------:|")
    for pair, n in sorted(by_pair.items()):
        lines.append(f"| {pair} | {n} |")
    lines.append("")

    # By category (primary)
    lines.append("## By primary category")
    lines.append("")
    by_cat = Counter(b["category"] for b in bugs)
    by_cat_pair = Counter((b["category"], b["language_pair"]) for b in bugs)
    lines.append("| Category | java-ts | python-go | Total |")
    lines.append("|----------|--------:|----------:|------:|")
    cats = ["schema", "coerce", "nil", "serde", "async", "other"]
    for cat in cats:
        j = by_cat_pair.get((cat, "java-ts"), 0)
        p = by_cat_pair.get((cat, "python-go"), 0)
        total_cat = j + p
        lines.append(f"| `{cat}` | {j} | {p} | {total_cat} |")
    lines.append("")

    # Secondary categories
    lines.append("## Secondary categories")
    lines.append("")
    sec = Counter(b.get("secondary_category") for b in bugs if b.get("secondary_category"))
    if sec:
        for cat, n in sec.most_common():
            lines.append(f"- `{cat}`: {n}")
    else:
        lines.append("(None recorded.)")
    lines.append("")

    # By boundary_kind
    lines.append("## By boundary_kind")
    lines.append("")
    lines.append("| Boundary | java-ts | python-go | Total |")
    lines.append("|----------|--------:|----------:|------:|")
    by_bnd = Counter((b["boundary_kind"], b["language_pair"]) for b in bugs)
    boundaries = ["rest", "grpc", "ffi", "shared-file", "subprocess", "other", "unknown"]
    for bnd in boundaries:
        j = by_bnd.get((bnd, "java-ts"), 0)
        p = by_bnd.get((bnd, "python-go"), 0)
        total_bnd = j + p
        if total_bnd > 0:
            lines.append(f"| `{bnd}` | {j} | {p} | {total_bnd} |")
    lines.append("")

    # Category × boundary
    lines.append("## Category × boundary_kind (cross-tab)")
    lines.append("")
    cx = Counter((b["category"], b["boundary_kind"]) for b in bugs)
    active_boundaries = sorted({b["boundary_kind"] for b in bugs})
    header = "| Category | " + " | ".join(active_boundaries) + " |"
    lines.append(header)
    lines.append("|" + "|".join(["-" * 10] * (len(active_boundaries) + 1)) + "|")
    for cat in cats:
        row = f"| `{cat}` | " + " | ".join(str(cx.get((cat, bnd), 0)) for bnd in active_boundaries) + " |"
        lines.append(row)
    lines.append("")

    # Per-repo
    lines.append("## Confirmed bugs per repo (top 10)")
    lines.append("")
    by_repo = Counter(b["repo"] for b in bugs)
    lines.append("| Repo | Count |")
    lines.append("|------|------:|")
    for repo, n in by_repo.most_common(10):
        lines.append(f"| [{repo}](https://github.com/{repo}) | {n} |")
    lines.append("")

    # Skip reasons
    if skips:
        lines.append("## Skip reasons (top 10)")
        lines.append("")
        reasons = Counter()
        for s in skips:
            reason = s.get("reason", "")
            head = reason.split(":", 1)[0]
            reasons[head] += 1
        lines.append("| Reason | Count |")
        lines.append("|--------|------:|")
        for r, n in reasons.most_common(10):
            lines.append(f"| {r} | {n} |")
        lines.append("")

    # Featured examples per category (for the paper §3.3)
    lines.append("## Representative examples per category (for §3.3)")
    lines.append("")
    for cat in cats:
        examples = [b for b in bugs if b["category"] == cat]
        if not examples:
            continue
        lines.append(f"### `{cat}` ({len(examples)} bug{'s' if len(examples)!=1 else ''})")
        lines.append("")
        for ex in examples[:2]:  # 2 per category max in the display
            lines.append(f"- **{ex['bug_id']}** ({ex['language_pair']}, `{ex['boundary_kind']}`): {ex['title']}")
            lines.append(f"  - {ex['rationale']}")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
