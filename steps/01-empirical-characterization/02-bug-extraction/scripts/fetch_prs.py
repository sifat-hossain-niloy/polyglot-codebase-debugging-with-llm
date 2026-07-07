#!/usr/bin/env python3
"""Fetch merged closed PRs per repo via GitHub GraphQL and filter to those
that touch files in both languages of the pair.

Input:  ../01-github-mining/data/processed/repos.jsonl
Output: data/raw/prs-<pair>-<date>.jsonl

Each output record is one PR that meets:
  - state = MERGED
  - author is not a bot (login doesn't end in [bot])
  - files touched include at least one file per language of the pair

Resumable: skips repos whose PRs are already in the output file for today.

Usage:
    uv run scripts/fetch_prs.py                          # both pairs
    uv run scripts/fetch_prs.py --lang-pair java-ts
    uv run scripts/fetch_prs.py --max-pages 2            # limit paging per repo
    uv run scripts/fetch_prs.py --limit-repos 5          # smoke-test on 5 repos

Maps to §3.3 Step 1.2 of the research plan.
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
import yaml  # noqa: F401  (loaded for consistency with other scripts)
from dotenv import find_dotenv, load_dotenv
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

GITHUB_GRAPHQL = "https://api.github.com/graphql"

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
STEP_DIR = SUB_STEP_DIR.parent
REPO_ROOT = STEP_DIR.parent.parent

REPOS_INPUT = STEP_DIR / "01-github-mining" / "data" / "processed" / "repos.jsonl"
RAW_DIR = SUB_STEP_DIR / "data" / "raw"

# Extensions that indicate a file "belongs to" a language
LANG_EXTS: dict[str, set[str]] = {
    "java": {".java"},
    "typescript": {".ts", ".tsx"},
    "python": {".py"},
    "go": {".go"},
}

# Pairs → (lang_a, lang_b) for filtering
PAIR_LANGS = {
    "java-ts": ("java", "typescript"),
    "python-go": ("python", "go"),
}

# GraphQL query: recent merged PRs with files + linked issues
QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: MERGED,
      first: 50,
      after: $cursor,
      orderBy: {field: UPDATED_AT, direction: DESC}
    ) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        title
        body
        mergedAt
        url
        author { login __typename }
        additions
        deletions
        changedFiles
        files(first: 100) {
          nodes { path additions deletions }
        }
        closingIssuesReferences(first: 3) {
          nodes { number title body url }
        }
      }
    }
  }
  rateLimit { cost remaining resetAt }
}
"""


class RateLimited(Exception):
    def __init__(self, sleep_for: int):
        super().__init__(f"rate limited; sleeping {sleep_for}s")
        self.sleep_for = sleep_for


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def build_headers() -> dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        log("ERROR: no GITHUB_TOKEN set")
        sys.exit(2)
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "polyglot-codebase-llm-research/0.1",
    }


@retry(
    retry=retry_if_exception_type(RateLimited),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=2, min=2, max=180),
    reraise=True,
)
def graphql(headers: dict, query: str, variables: dict) -> dict:
    resp = requests.post(
        GITHUB_GRAPHQL,
        headers=headers,
        json={"query": query, "variables": variables},
        timeout=60,
    )
    if resp.status_code == 502 or resp.status_code == 503:
        log(f"  {resp.status_code} from GitHub — retrying")
        raise RateLimited(5)
    if resp.status_code == 403:
        reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
        sleep_for = max(1, reset - int(time.time()) + 2)
        log(f"  rate limited; sleep {sleep_for}s")
        time.sleep(sleep_for)
        raise RateLimited(sleep_for)
    resp.raise_for_status()
    payload = resp.json()
    if "errors" in payload:
        # rate-limit-like errors in the GraphQL body
        err_msg = str(payload["errors"])
        if "rate limit" in err_msg.lower() or "abuse" in err_msg.lower():
            log(f"  GraphQL rate/abuse error; sleep 60s")
            time.sleep(60)
            raise RateLimited(60)
        log(f"  GraphQL errors: {err_msg[:200]}")
        return payload
    return payload


def file_language(path: str) -> str | None:
    lower = path.lower()
    for lang, exts in LANG_EXTS.items():
        for ext in exts:
            if lower.endswith(ext):
                return lang
    return None


def classify_files(files: list[dict], lang_a: str, lang_b: str) -> dict[str, list[str]]:
    buckets = {"lang_a": [], "lang_b": [], "schema": [], "other": []}
    for f in files:
        path = f["path"]
        lang = file_language(path)
        pl = path.lower()
        if pl.endswith(".proto") or pl.endswith(".openapi.yaml") or pl.endswith("openapi.yml") or "swagger" in pl:
            buckets["schema"].append(path)
        elif lang == lang_a:
            buckets["lang_a"].append(path)
        elif lang == lang_b:
            buckets["lang_b"].append(path)
        else:
            buckets["other"].append(path)
    return buckets


def is_bot(author: dict | None) -> bool:
    if not author:
        return True
    login = (author.get("login") or "").lower()
    typ = author.get("__typename", "")
    if typ == "Bot":
        return True
    if login.endswith("[bot]"):
        return True
    if login in {"dependabot-preview", "renovate-bot", "greenkeeper", "snyk-bot", "github-actions"}:
        return True
    return False


def load_already_fetched(out_path: Path) -> set[str]:
    if not out_path.exists():
        return set()
    seen = set()
    with out_path.open() as f:
        for line in f:
            try:
                seen.add(json.loads(line)["repo"])
            except Exception:
                continue
    return seen


def fetch_repo(headers: dict, owner: str, name: str, lang_a: str, lang_b: str, max_pages: int) -> tuple[list[dict], int]:
    """Return (matching_prs, total_prs_seen). matching = touch both languages, non-bot."""
    matches: list[dict] = []
    total_seen = 0
    cursor = None
    for _ in range(max_pages):
        payload = graphql(headers, QUERY, {"owner": owner, "name": name, "cursor": cursor})
        if not payload.get("data") or not payload["data"].get("repository"):
            log(f"  {owner}/{name}: no repository data; stopping")
            break
        prs = payload["data"]["repository"]["pullRequests"]
        for pr in prs["nodes"]:
            total_seen += 1
            if is_bot(pr.get("author")):
                continue
            files_conn = pr.get("files") or {}
            files = files_conn.get("nodes") or []
            buckets = classify_files(files, lang_a, lang_b)
            if buckets["lang_a"] and buckets["lang_b"]:
                matches.append(
                    {
                        "number": pr["number"],
                        "title": pr["title"],
                        "body": pr.get("body") or "",
                        "merged_at": pr["mergedAt"],
                        "url": pr["url"],
                        "author": (pr.get("author") or {}).get("login"),
                        "additions": pr.get("additions", 0),
                        "deletions": pr.get("deletions", 0),
                        "changed_files": pr.get("changedFiles", 0),
                        "files_lang_a": buckets["lang_a"],
                        "files_lang_b": buckets["lang_b"],
                        "files_schema": buckets["schema"],
                        "files_other": buckets["other"],
                        "linked_issues": [
                            {"number": i["number"], "title": i["title"], "body": (i.get("body") or "")[:2000], "url": i["url"]}
                            for i in (pr.get("closingIssuesReferences") or {}).get("nodes", [])
                        ],
                    }
                )
        # Track rate-limit cost
        rl = payload.get("data", {}).get("rateLimit") or {}
        page_info = prs["pageInfo"]
        log(
            f"  {owner}/{name} page: {len(prs['nodes'])} PRs, "
            f"kept {len(matches)}, remaining points={rl.get('remaining')}"
        )
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]
        time.sleep(0.3)
    return matches, total_seen


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang-pair", choices=["java-ts", "python-go", "all"], default="all")
    parser.add_argument("--max-pages", type=int, default=4, help="Max GraphQL pages per repo (50 PRs each; default 4 = 200 recent merged PRs)")
    parser.add_argument("--limit-repos", type=int, default=None, help="Only process this many repos (smoke test)")
    args = parser.parse_args()

    env_file = find_dotenv(usecwd=True)
    if env_file:
        load_dotenv(env_file)
    headers = build_headers()

    if not REPOS_INPUT.exists():
        log(f"ERROR: {REPOS_INPUT} does not exist. Run sub-step 1.1 first.")
        return 2
    with REPOS_INPUT.open() as f:
        repos = [json.loads(line) for line in f]
    log(f"loaded {len(repos)} repos from {REPOS_INPUT.name}")

    pairs = ["java-ts", "python-go"] if args.lang_pair == "all" else [args.lang_pair]

    today = dt.date.today().isoformat()

    for pair in pairs:
        pair_repos = [r for r in repos if r["language_pair"] == pair]
        if args.limit_repos:
            pair_repos = pair_repos[: args.limit_repos]
        lang_a, lang_b = PAIR_LANGS[pair]
        out_path = RAW_DIR / f"prs-{pair}-{today}.jsonl"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        already = load_already_fetched(out_path)
        if already:
            log(f"[{pair}] resuming; {len(already)} repos already fetched")

        with out_path.open("a") as f_out:
            for idx, repo in enumerate(pair_repos, start=1):
                full = f"{repo['owner']}/{repo['name']}"
                if full in already:
                    continue
                log(f"[{pair}] ({idx}/{len(pair_repos)}) {full}")
                try:
                    matches, seen = fetch_repo(headers, repo["owner"], repo["name"], lang_a, lang_b, args.max_pages)
                except (RetryError, requests.HTTPError) as e:
                    log(f"  ERROR on {full}: {e}")
                    matches, seen = [], 0
                for m in matches:
                    rec = {
                        "repo": full,
                        "language_pair": pair,
                        "pr_number": m["number"],
                        "pr_url": m["url"],
                        "title": m["title"],
                        "body": m["body"],
                        "merged_at": m["merged_at"],
                        "author": m["author"],
                        "additions": m["additions"],
                        "deletions": m["deletions"],
                        "changed_files": m["changed_files"],
                        "files_lang_a": m["files_lang_a"],
                        "files_lang_b": m["files_lang_b"],
                        "files_schema": m["files_schema"],
                        "files_other": m["files_other"],
                        "linked_issues": m["linked_issues"],
                        "_fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                        "_prs_seen_on_repo": seen,
                    }
                    f_out.write(json.dumps(rec) + "\n")
                f_out.flush()
                log(f"  → wrote {len(matches)} cross-lang PRs (of {seen} seen)")
                time.sleep(0.3)

        log(f"[{pair}] done → {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
