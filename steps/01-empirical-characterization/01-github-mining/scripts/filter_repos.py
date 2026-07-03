#!/usr/bin/env python3
"""Apply selection criteria to enriched candidates and write the final repos.jsonl.

Reads data/raw/enriched-<pair>-<date>.jsonl and emits
data/processed/repos.jsonl validated against shared/schemas/repo.schema.json.

Selection criteria (per ../README.md, configurable via ../configs/queries.yaml):
  - Both required languages present, each ≥ min_bytes and ≥ min_fraction.
  - ≥ min_stars.
  - Created ≥6 months ago (min_created_before).
  - Not archived, not a fork.
  - has_ci is True.
  - License is non-null and permissive (MIT, Apache-2.0, BSD-3-Clause, etc.).
  - Name and description do not contain any exclusion_terms.

Also writes a rejection log (output/rejected.jsonl) showing why each rejected
candidate was dropped — useful for tuning the filter.

Usage:
    uv run scripts/filter_repos.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
STEP_DIR = SUB_STEP_DIR.parent
REPO_ROOT = STEP_DIR.parent.parent

CONFIG_PATH = SUB_STEP_DIR / "configs" / "queries.yaml"
RAW_DIR = SUB_STEP_DIR / "data" / "raw"
PROCESSED_DIR = SUB_STEP_DIR / "data" / "processed"
OUTPUT_DIR = SUB_STEP_DIR / "output"
SCHEMA_PATH = REPO_ROOT / "shared" / "schemas" / "repo.schema.json"

PERMISSIVE_LICENSES = {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "MPL-2.0",
    "Unlicense",
    "0BSD",
}


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return [json.loads(line) for line in f]


def name_or_desc_excluded(record: dict, exclusion_terms: list[str]) -> str | None:
    blob = " ".join(
        [
            record["name"].lower(),
            (record.get("description") or "").lower(),
        ]
    )
    for term in exclusion_terms:
        if term.lower() in blob:
            return term
    return None


def check_languages(record: dict, filters: dict) -> str | None:
    langs = record.get("languages_bytes") or {}
    if not langs:
        return "no languages data"
    total = sum(langs.values())
    if total == 0:
        return "zero-byte languages"
    for required in filters["languages_required"]:
        bytes_ = langs.get(required, 0)
        if bytes_ < filters["min_bytes_per_required_language"]:
            return f"language {required}: only {bytes_} bytes < {filters['min_bytes_per_required_language']}"
        fraction = bytes_ / total
        if fraction < filters["min_fraction_per_required_language"]:
            return (
                f"language {required}: fraction {fraction:.3f} "
                f"< {filters['min_fraction_per_required_language']}"
            )
    return None


def to_repo_record(record: dict, lang_pair: str) -> dict:
    """Project an enriched record into the schema-conformant repos.jsonl format."""
    return {
        "owner": record["owner"],
        "name": record["name"],
        "url": record["url"],
        "language_pair": lang_pair,
        "languages_bytes": record["languages_bytes"],
        "stars": record["stars"],
        "forks": record["forks"],
        "default_branch": record["default_branch"],
        "license": record.get("license"),
        "has_ci": record.get("has_ci", False),
        "has_tests": record.get("has_tests_marker", False),
        "is_monorepo": True,  # by current selection: single-repo polyglot
        "is_fork": record.get("is_fork", False),
        "is_archived": record.get("is_archived", False),
        "last_commit_at": record["pushed_at"],
        "created_at": record["created_at"],
        "size_kb": record["size_kb"],
        "topics": record.get("topics", []),
        "fetched_at": record["_fetched_at"],
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Date suffix on the input enriched-<pair>-<date>.jsonl files",
    )
    parser.add_argument(
        "--include-non-permissive-license",
        action="store_true",
        help="Keep repos with non-permissive or null licenses (default: reject)",
    )
    args = parser.parse_args()

    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)

    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft202012Validator(schema)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    repos_out_path = PROCESSED_DIR / "repos.jsonl"
    rejected_out_path = OUTPUT_DIR / "rejected.jsonl"

    accepted = 0
    rejected = 0
    rejection_counts: dict[str, int] = {}
    per_pair_counts: dict[str, int] = {}

    min_created_before = dt.datetime.fromisoformat(
        cfg["defaults"]["min_created_before"]
    ).replace(tzinfo=dt.timezone.utc)
    min_stars = cfg["defaults"]["min_stars"]
    exclusion_terms = cfg["exclusion_terms"]

    with repos_out_path.open("w") as f_out, rejected_out_path.open("w") as f_rej:
        for pair in ["java-ts", "python-go"]:
            cfg_key = pair.replace("-", "_")
            filters = cfg[cfg_key]["filters"]
            in_path = RAW_DIR / f"enriched-{pair}-{args.date}.jsonl"
            records = load_records(in_path)
            log(f"[{pair}] loaded {len(records)} enriched candidates from {in_path.name}")

            for record in records:
                reasons: list[str] = []
                if record.get("enrichment_failed"):
                    reasons.append("enrichment_failed")
                if record["stars"] < min_stars:
                    reasons.append(f"stars {record['stars']} < {min_stars}")
                if record.get("is_archived"):
                    reasons.append("is_archived")
                if record.get("is_fork"):
                    reasons.append("is_fork")
                if not record.get("has_ci"):
                    reasons.append("no CI marker at root")
                # has_tests_marker is informational only — many monorepos place
                # test configs in sub-packages, not at root. CI presence is the
                # real signal that the project is tested.

                created = dt.datetime.fromisoformat(
                    record["created_at"].replace("Z", "+00:00")
                )
                if created > min_created_before:
                    reasons.append(
                        f"too young; created {created.date()} > {min_created_before.date()}"
                    )

                lic = record.get("license")
                if not args.include_non_permissive_license:
                    if lic is None:
                        reasons.append("no license")
                    elif lic not in PERMISSIVE_LICENSES:
                        reasons.append(f"non-permissive license: {lic}")

                lang_reason = check_languages(record, filters)
                if lang_reason:
                    reasons.append(lang_reason)

                excl_term = name_or_desc_excluded(record, exclusion_terms)
                if excl_term:
                    reasons.append(f"excluded term: {excl_term}")

                if reasons:
                    rejected += 1
                    for r in reasons:
                        primary = r.split(":", 1)[0]
                        rejection_counts[primary] = rejection_counts.get(primary, 0) + 1
                    f_rej.write(
                        json.dumps(
                            {
                                "full_name": record["full_name"],
                                "language_pair": pair,
                                "stars": record["stars"],
                                "reasons": reasons,
                            }
                        )
                        + "\n"
                    )
                    continue

                projected = to_repo_record(record, pair)
                errors = sorted(validator.iter_errors(projected), key=lambda e: e.path)
                if errors:
                    rejected += 1
                    rejection_counts["schema_error"] = (
                        rejection_counts.get("schema_error", 0) + 1
                    )
                    f_rej.write(
                        json.dumps(
                            {
                                "full_name": record["full_name"],
                                "language_pair": pair,
                                "reasons": [
                                    f"schema: {e.message}" for e in errors[:3]
                                ],
                            }
                        )
                        + "\n"
                    )
                    continue

                f_out.write(json.dumps(projected) + "\n")
                accepted += 1
                per_pair_counts[pair] = per_pair_counts.get(pair, 0) + 1

    log("")
    log(f"=== summary ===")
    log(f"accepted: {accepted}")
    for pair, cnt in per_pair_counts.items():
        log(f"  {pair}: {cnt}")
    log(f"rejected: {rejected}")
    for reason, cnt in sorted(rejection_counts.items(), key=lambda x: -x[1]):
        log(f"  {reason:40s}  {cnt}")
    log("")
    log(f"final corpus: {repos_out_path}")
    log(f"rejections:   {rejected_out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
