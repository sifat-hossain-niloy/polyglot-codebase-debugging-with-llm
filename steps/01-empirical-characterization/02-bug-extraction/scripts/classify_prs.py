#!/usr/bin/env python3
"""LLM-assisted classification of candidate PRs against the 6-category taxonomy.

Uses the Anthropic API (Claude models) to propose a category + rationale per PR.
Output must be treated as *advisory* — a human annotator confirms the label
before it enters the final `bugs.jsonl`.

The script:
  1. Reads data/processed/candidates-<date>.jsonl.
  2. For each candidate not already in data/processed/bugs.jsonl:
     - Fetches the PR diff (patches) from GitHub if not cached.
     - Builds a structured prompt with title/body/files/linked-issue/diff-summary.
     - Calls the Claude API forcing a JSON response conforming to bug-annotation.schema.json.
     - Appends the annotation record.
  3. Prints a summary.

Prerequisites:
  - ANTHROPIC_API_KEY in .env
  - GITHUB_TOKEN in .env (for optional diff fetches)
  - `uv add anthropic` (add to pyproject.toml if not present)

Usage:
    uv run scripts/classify_prs.py --date 2026-07-08 --limit 20
    uv run scripts/classify_prs.py --model claude-sonnet-4-6

Cost estimate (rough): ~$0.05–0.20 per PR at Sonnet prices depending on diff size.
For 100 PRs, budget ~$5–20.

**Note (2026-07-08):** this script is a scaffold. Requires ANTHROPIC_API_KEY to
run. If the key isn't available, the current session falls back to in-conversation
annotation of a smaller batch — see the STATUS.md for the manual annotations
produced so far.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
PROCESSED_DIR = SUB_STEP_DIR / "data" / "processed"
PROMPTS_DIR = SUB_STEP_DIR.parent.parent.parent / "shared" / "prompts"

DEFAULT_PROMPT_VERSION = "bug-classifier-v1"
DEFAULT_MODEL = "claude-sonnet-4-6"


SYSTEM_PROMPT = """You are a software engineering research assistant classifying cross-language bugs.

You will read a pull request that fixed a bug spanning two languages (Java+TypeScript or Python+Go). Your job is to:

1. Decide whether the bug is truly cross-language (the bug requires interaction between the two languages to manifest), or a coincidental dual-language touch.
2. If it IS cross-language, classify it into ONE of these 6 categories:
   - `schema`: schema / contract mismatch (OpenAPI, Protobuf, JSON-schema divergence)
   - `coerce`: type-coercion error at the boundary (numbers losing precision, enum encoding differences)
   - `nil`: null / nil / undefined handling difference across the boundary
   - `serde`: serialization format drift (timestamp format, casing, encoding)
   - `async`: async / sync / concurrency impedance mismatch
   - `other`: genuinely cross-language but none of the above (rationale mandatory)
3. Guess the boundary_kind: `rest`, `grpc`, `shared-file`, `subprocess`, `ffi`, `other`, or `unknown`.
4. Write a 1–2 sentence rationale explaining your choice.

Rules:
- Pick the *primary cause*, not the symptom.
- Order of precedence when two categories seem to fit: `schema` > `coerce` > `serde`. `nil` and `async` are orthogonal.
- If unsure whether the bug is truly cross-language, set `is_confirmed_cross_language: false` and explain why.
- Never invent a new category. If unsure, use `other` and explain.

Output MUST be a single JSON object matching this shape:

{
  "is_confirmed_cross_language": true | false,
  "category": "schema" | "coerce" | "nil" | "serde" | "async" | "other" | null,
  "secondary_category": "schema" | "coerce" | "nil" | "serde" | "async" | "other" | null,
  "boundary_kind": "rest" | "grpc" | "shared-file" | "subprocess" | "ffi" | "other" | "unknown",
  "rationale": "..."
}

Return null for category if is_confirmed_cross_language is false.
"""


def build_user_prompt(pr: dict) -> str:
    parts = [
        f"Repo: {pr['repo']}",
        f"Language pair: {pr['language_pair']}",
        f"PR #{pr['pr_number']}: {pr['title']}",
        f"URL: {pr['pr_url']}",
        "",
        "PR body:",
        (pr.get("body") or "(empty)")[:4000],
        "",
        f"Files changed in lang A ({pr['language_pair'].split('-')[0]}): {pr.get('n_files_lang_a', 0)}",
    ]
    for p in pr.get("files_lang_a", [])[:20]:
        parts.append(f"  - {p}")
    parts.append(f"Files changed in lang B ({pr['language_pair'].split('-')[1]}): {pr.get('n_files_lang_b', 0)}")
    for p in pr.get("files_lang_b", [])[:20]:
        parts.append(f"  - {p}")
    if pr.get("files_schema"):
        parts.append("Schema files touched:")
        for p in pr["files_schema"]:
            parts.append(f"  - {p}")
    if pr.get("linked_issues"):
        parts.append("Linked issues:")
        for iss in pr["linked_issues"]:
            parts.append(f"  #{iss['number']}: {iss['title']}")
            body = (iss.get("body") or "")[:1500]
            if body:
                parts.append(f"    {body}")
    parts.append("")
    parts.append("Classify this bug. Return JSON only.")
    return "\n".join(parts)


def classify_with_claude(client, pr: dict, model: str) -> dict | None:
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_user_prompt(pr)}],
        )
        text = resp.content[0].text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip("` \n")
        return json.loads(text)
    except Exception as e:
        print(f"  API error on {pr['repo']}#{pr['pr_number']}: {e}", file=sys.stderr)
        return None


def already_annotated(bugs_path: Path) -> set[str]:
    if not bugs_path.exists():
        return set()
    seen = set()
    with bugs_path.open() as f:
        for line in f:
            try:
                seen.add(json.loads(line)["bug_id"])
            except Exception:
                continue
    return seen


def to_annotation(pr: dict, classification: dict, prompt_version: str, annotator: str) -> dict:
    return {
        "bug_id": f"{pr['repo']}#{pr['pr_number']}",
        "repo": pr["repo"],
        "language_pair": pr["language_pair"],
        "pr_url": pr["pr_url"],
        "pr_number": pr["pr_number"],
        "merged_at": pr["merged_at"],
        "title": pr["title"],
        "body": (pr.get("body") or "")[:5000],
        "linked_issues": [
            {"number": i["number"], "url": i["url"], "title": i["title"], "body": i.get("body")}
            for i in pr.get("linked_issues", [])
        ],
        "category": classification.get("category"),
        "secondary_category": classification.get("secondary_category"),
        "rationale": classification.get("rationale", ""),
        "files_changed": {
            "primary_language": pr.get("files_lang_a", []),
            "secondary_language": pr.get("files_lang_b", []),
            "schema_files": pr.get("files_schema", []),
            "other": pr.get("files_other", []),
        },
        "boundary_kind": classification.get("boundary_kind", "unknown"),
        "is_confirmed_cross_language": classification.get("is_confirmed_cross_language", False),
        "annotator": annotator,
        "second_annotator": None,
        "annotator_disagreement": None,
        "annotated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "prompt_version": prompt_version,
        "schema_version": "1.0",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--limit", type=int, default=None, help="Only classify this many PRs (for cost control)")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--annotator", default="llm-auto")
    parser.add_argument("--prompt-version", default=DEFAULT_PROMPT_VERSION)
    args = parser.parse_args()

    load_dotenv(find_dotenv(usecwd=True))
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set. Add it to .env then re-run.", file=sys.stderr)
        return 2
    try:
        import anthropic
    except ImportError:
        print("anthropic package not installed. Run: uv add anthropic", file=sys.stderr)
        return 2

    client = anthropic.Anthropic(api_key=api_key)

    in_path = PROCESSED_DIR / f"candidates-{args.date}.jsonl"
    if not in_path.exists():
        print(f"missing {in_path} — run triage_prs.py first", file=sys.stderr)
        return 2
    with in_path.open() as f:
        candidates = [json.loads(l) for l in f]

    bugs_path = PROCESSED_DIR / "bugs.jsonl"
    already = already_annotated(bugs_path)

    todo = [c for c in candidates if f"{c['repo']}#{c['pr_number']}" not in already]
    if args.limit:
        todo = todo[: args.limit]
    print(f"classifying {len(todo)} candidates (skipping {len(candidates) - len(todo)} already done)")

    with bugs_path.open("a") as f_out:
        for idx, pr in enumerate(todo, start=1):
            classification = classify_with_claude(client, pr, args.model)
            if not classification:
                continue
            annotation = to_annotation(pr, classification, args.prompt_version, args.annotator)
            f_out.write(json.dumps(annotation) + "\n")
            f_out.flush()
            if idx % 5 == 0 or idx == len(todo):
                print(f"  [{idx}/{len(todo)}] {pr['repo']}#{pr['pr_number']} → {classification.get('category')} ({classification.get('boundary_kind')})")

    print(f"done → {bugs_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
