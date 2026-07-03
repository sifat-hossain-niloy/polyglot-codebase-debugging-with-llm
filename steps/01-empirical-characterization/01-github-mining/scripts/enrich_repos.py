#!/usr/bin/env python3
"""Enrich raw search results with /languages byte breakdown and root-contents signals.

For each repo in data/raw/search-<pair>-<date>.jsonl, fetches:
  - GET /repos/{owner}/{name}/languages       → byte distribution
  - GET /repos/{owner}/{name}/contents/       → root-level files for CI / test detection

Writes data/raw/enriched-<pair>-<date>.jsonl with added fields:
  languages_bytes, has_ci, has_tests_marker, root_files, enrichment_failed.

Resumable: if the output file exists, skips repos already enriched.

Usage:
    uv run scripts/enrich_repos.py --lang-pair java-ts
    uv run scripts/enrich_repos.py            # all pairs
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import find_dotenv, load_dotenv
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

GITHUB_API = "https://api.github.com"

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
RAW_DIR = SUB_STEP_DIR / "data" / "raw"

# Root-level markers we look for
CI_MARKERS = {
    ".github",           # then we check workflows/ via separate call
    ".circleci",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    ".travis.yml",
    "azure-pipelines.yml",
    ".drone.yml",
    "bitbucket-pipelines.yml",
}
TEST_MARKERS = {
    # Python
    "pytest.ini",
    "tox.ini",
    "setup.cfg",
    # Java
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    # JS/TS
    "package.json",       # heuristic: most have a test script
    "jest.config.js",
    "jest.config.ts",
    "vitest.config.ts",
    "vitest.config.js",
    # Go (presence of go.mod is necessary but not sufficient; _test.go files
    # would need recursive walk — leave to filter step)
    "go.mod",
}


class RateLimited(Exception):
    def __init__(self, sleep_for: int):
        super().__init__(f"rate limited; need to sleep {sleep_for}s")
        self.sleep_for = sleep_for


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def build_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "polyglot-codebase-llm-research/0.1",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


@retry(
    retry=retry_if_exception_type(RateLimited),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=2, min=2, max=120),
    reraise=True,
)
def _get(url: str, headers: dict) -> requests.Response:
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code == 403 and "rate limit" in resp.text.lower():
        reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
        sleep_for = max(1, reset - int(time.time()) + 2)
        log(f"  rate-limited; sleeping {sleep_for}s")
        time.sleep(sleep_for)
        raise RateLimited(sleep_for)
    return resp


def fetch_languages(full_name: str, headers: dict) -> dict[str, int] | None:
    resp = _get(f"{GITHUB_API}/repos/{full_name}/languages", headers)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def fetch_root_contents(full_name: str, headers: dict) -> list[dict] | None:
    resp = _get(f"{GITHUB_API}/repos/{full_name}/contents/", headers)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    payload = resp.json()
    if not isinstance(payload, list):
        return None  # repo with no root contents (rare)
    return payload


def analyze_root(contents: list[dict]) -> tuple[bool, bool, list[str]]:
    """Returns (has_ci, has_tests_marker, list_of_root_filenames)."""
    names = [item["name"] for item in contents]
    has_ci = any(name in CI_MARKERS for name in names)
    has_tests_marker = any(name in TEST_MARKERS for name in names)
    return has_ci, has_tests_marker, names


def load_enriched_keys(out_path: Path) -> set[str]:
    if not out_path.exists():
        return set()
    keys = set()
    with out_path.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
                keys.add(rec["full_name"])
            except Exception:
                continue
    return keys


def enrich_pair(lang_pair: str, headers: dict, date_suffix: str) -> Path:
    in_path = RAW_DIR / f"search-{lang_pair}-{date_suffix}.jsonl"
    out_path = RAW_DIR / f"enriched-{lang_pair}-{date_suffix}.jsonl"

    if not in_path.exists():
        log(f"[{lang_pair}] no search file found at {in_path}; run search_repos.py first")
        return out_path

    already_done = load_enriched_keys(out_path)
    if already_done:
        log(f"[{lang_pair}] resuming; {len(already_done)} repos already enriched")

    with in_path.open() as f:
        repos = [json.loads(line) for line in f]
    log(f"[{lang_pair}] enriching {len(repos)} repos ({len(already_done)} cached)")

    # Open in append mode so resumability works.
    with out_path.open("a") as f_out:
        for idx, repo in enumerate(repos, start=1):
            full_name = repo["full_name"]
            if full_name in already_done:
                continue
            try:
                langs = fetch_languages(full_name, headers)
                time.sleep(0.4)  # ≤ ~150/min, well under the 5000/hr ceiling
                root = fetch_root_contents(full_name, headers)
                time.sleep(0.4)
                if langs is None or root is None:
                    enriched = {
                        **repo,
                        "languages_bytes": {},
                        "has_ci": False,
                        "has_tests_marker": False,
                        "root_files": [],
                        "enrichment_failed": True,
                        "_enrichment_error": "404 on languages or contents",
                    }
                else:
                    has_ci, has_tests, names = analyze_root(root)
                    enriched = {
                        **repo,
                        "languages_bytes": langs,
                        "has_ci": has_ci,
                        "has_tests_marker": has_tests,
                        "root_files": names,
                        "enrichment_failed": False,
                    }
            except (RetryError, requests.HTTPError) as e:
                log(f"  [{idx}/{len(repos)}] {full_name}: enrichment failed: {e}")
                enriched = {
                    **repo,
                    "languages_bytes": {},
                    "has_ci": False,
                    "has_tests_marker": False,
                    "root_files": [],
                    "enrichment_failed": True,
                    "_enrichment_error": str(e),
                }

            enriched["_enriched_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            f_out.write(json.dumps(enriched) + "\n")
            f_out.flush()  # so resume works even after Ctrl-C

            if idx % 10 == 0 or idx == len(repos):
                log(f"  [{idx}/{len(repos)}] {full_name}")

    log(f"[{lang_pair}] wrote → {out_path}")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lang-pair",
        choices=["java-ts", "python-go", "all"],
        default="all",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Date suffix on the input search-<pair>-<date>.jsonl files (default: today)",
    )
    args = parser.parse_args()

    env_file = find_dotenv(usecwd=True)
    if env_file:
        load_dotenv(env_file)
    headers = build_headers()
    if "Authorization" not in headers:
        log("auth: no GITHUB_TOKEN — enrichment will hit rate limits fast")

    pairs = ["java-ts", "python-go"] if args.lang_pair == "all" else [args.lang_pair]
    for pair in pairs:
        enrich_pair(pair, headers, args.date)

    log("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
