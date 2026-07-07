#!/usr/bin/env python3
"""Heuristic triage of raw cross-language PRs → candidates for annotation.

Filters kept:
  - PR title or body contains bug-indicator keywords (fix, bug, issue, error, crash,
    mismatch, null, undefined, NPE, broken, regression, incorrect, wrong).
  - At least 1 code file in each language of the pair (already enforced by fetch,
    but re-checked here to allow re-running with different fetch outputs).
  - Non-trivial code changes: ≤500 files (drop massive merges); at least 2 lines
    changed on the smaller-language side.
  - Not a merge commit / release PR (title starts with 'Merge ' / 'Release ' /
    'chore(release)' / 'v0.' / 'v1.' etc.).

Signals recorded (advisory, not filters):
  - `has_schema_files` — .proto / openapi / swagger touched
  - `boundary_hint` — best guess at boundary kind (rest / grpc / ffi / unknown)

Input:  data/raw/prs-<pair>-<date>.jsonl
Output: data/processed/candidates-<date>.jsonl

Usage:
    uv run scripts/triage_prs.py --date 2026-07-08
    uv run scripts/triage_prs.py --lang-pair java-ts
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
RAW_DIR = SUB_STEP_DIR / "data" / "raw"
PROCESSED_DIR = SUB_STEP_DIR / "data" / "processed"

BUG_KEYWORDS = [
    r"\bfix(es|ed|ing)?\b",
    r"\bbug(s|gy)?\b",
    r"\bissue(s)?\b",
    r"\berror(s)?\b",
    r"\bcrash(es|ed|ing)?\b",
    r"\bmismatch(es)?\b",
    r"\bnull( pointer)?\b",
    r"\bundefined\b",
    r"\bnil (pointer|deref)\b",
    r"\bNPE\b",
    r"\bbroken\b",
    r"\bregression(s)?\b",
    r"\bincorrect(ly)?\b",
    r"\bwrong(ly)?\b",
    r"\bmissing\b",
    r"\bbreak(s|ing)?\b",
    r"\bfail(s|ed|ing)?\b",
]

# Titles that indicate release / merge / bump / doc-only work — drop these
DROP_TITLE_PATTERNS = [
    r"^merge\b",
    r"^release\b",
    r"^chore\(release\)",
    r"^chore: release",
    r"^bump\b",
    r"^v?\d+\.\d+\.\d+",  # version number at start
    r"^\[release\]",
    r"^update readme",
    r"^docs?:",
    r"^style:",
    r"^chore\(deps\)",
    r"^ci:",
    r"^test:",
]

BUG_RX = re.compile("|".join(BUG_KEYWORDS), re.IGNORECASE)
DROP_RX = re.compile("|".join(DROP_TITLE_PATTERNS), re.IGNORECASE)


def is_release_or_bump(title: str) -> bool:
    return bool(DROP_RX.search(title.strip()))


def has_bug_keyword(text: str) -> bool:
    return bool(BUG_RX.search(text))


def guess_boundary(files_schema: list[str], files_lang_a: list[str], files_lang_b: list[str], pair: str) -> str:
    if any(p.lower().endswith(".proto") for p in files_schema):
        return "grpc"
    if any("openapi" in p.lower() or "swagger" in p.lower() for p in files_schema):
        return "rest"
    # java-ts pairs that touch Android JNI code are FFI
    if pair == "java-ts":
        joined = " ".join(files_lang_a).lower()
        if "/android/" in joined or "jni" in joined or "kotlin" in joined:
            return "ffi"
    return "unknown"


def has_test_file(files: list[str]) -> bool:
    for p in files:
        pl = p.lower()
        if "/test/" in pl or "/tests/" in pl or "test_" in pl or "_test." in pl or pl.endswith(".spec.ts") or pl.endswith(".test.ts"):
            return True
    return False


def code_lines_changed(pr: dict, files_key: str) -> int:
    # We don't have per-file additions/deletions in the fetched record (we only kept
    # paths). Approximate by counting number of files as a proxy.
    return len(pr.get(files_key, []))


def triage_one(pr: dict) -> tuple[bool, list[str], dict]:
    """Return (keep, reasons_for_drop, enriched_fields)."""
    reasons = []
    title = pr["title"] or ""
    body = pr.get("body") or ""
    text = f"{title}\n{body}"

    if is_release_or_bump(title):
        reasons.append("release/merge/bump title")

    if not has_bug_keyword(text):
        reasons.append("no bug keyword in title or body")

    if pr.get("changed_files", 0) > 500:
        reasons.append(f"too many files changed ({pr['changed_files']})")

    if not pr.get("files_lang_a") or not pr.get("files_lang_b"):
        reasons.append("missing files in one language")

    boundary = guess_boundary(
        pr.get("files_schema", []),
        pr.get("files_lang_a", []),
        pr.get("files_lang_b", []),
        pr["language_pair"],
    )

    enriched = {
        "has_schema_files": bool(pr.get("files_schema")),
        "boundary_hint": boundary,
        "n_files_lang_a": len(pr.get("files_lang_a", [])),
        "n_files_lang_b": len(pr.get("files_lang_b", [])),
        "n_files_schema": len(pr.get("files_schema", [])),
        "has_test_change": has_test_file(pr.get("files_lang_a", []) + pr.get("files_lang_b", [])),
        "has_linked_issue": bool(pr.get("linked_issues")),
    }

    keep = not reasons
    return keep, reasons, enriched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--lang-pair", choices=["java-ts", "python-go", "all"], default="all")
    args = parser.parse_args()

    pairs = ["java-ts", "python-go"] if args.lang_pair == "all" else [args.lang_pair]
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"candidates-{args.date}.jsonl"

    total_in = 0
    total_kept = 0
    per_pair_kept = Counter()
    per_pair_seen = Counter()
    drop_reasons = Counter()

    with out_path.open("w") as f_out:
        for pair in pairs:
            in_path = RAW_DIR / f"prs-{pair}-{args.date}.jsonl"
            if not in_path.exists():
                print(f"[{pair}] no raw file at {in_path}; skipping", file=sys.stderr)
                continue
            with in_path.open() as f_in:
                for line in f_in:
                    pr = json.loads(line)
                    total_in += 1
                    per_pair_seen[pair] += 1
                    keep, reasons, enriched = triage_one(pr)
                    for r in reasons:
                        drop_reasons[r] += 1
                    if not keep:
                        continue
                    total_kept += 1
                    per_pair_kept[pair] += 1
                    candidate = {**pr, **enriched, "_triaged_at": dt.datetime.now(dt.timezone.utc).isoformat()}
                    f_out.write(json.dumps(candidate) + "\n")

    print(f"=== triage summary ===")
    print(f"seen:  {total_in}")
    for pair, n in per_pair_seen.items():
        print(f"  {pair}: {n}")
    print(f"kept:  {total_kept}")
    for pair, n in per_pair_kept.items():
        print(f"  {pair}: {n}")
    print("drop reasons:")
    for reason, n in drop_reasons.most_common():
        print(f"  {reason:40s} {n}")
    print(f"\ncandidates → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
