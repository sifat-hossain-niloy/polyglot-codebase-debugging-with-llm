#!/usr/bin/env python3
"""Query GitHub Search API for candidate polyglot repos.

Reads ../configs/queries.yaml. For each query, pages through results and
writes one JSON object per repo to ../data/raw/search-<lang-pair>-<date>.jsonl.
Dedupes by full_name within a language pair.

Usage:
    uv run scripts/search_repos.py --dry-run
    uv run scripts/search_repos.py --lang-pair java-ts
    uv run scripts/search_repos.py            # full sweep, both pairs

Maps to §3.3 Step 1.1 of the research plan.
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
import yaml
from dotenv import find_dotenv, load_dotenv
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

GITHUB_API = "https://api.github.com"
SEARCH_ENDPOINT = f"{GITHUB_API}/search/repositories"

SCRIPT_DIR = Path(__file__).resolve().parent
SUB_STEP_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SUB_STEP_DIR / "configs" / "queries.yaml"
RAW_DIR = SUB_STEP_DIR / "data" / "raw"


class RateLimited(Exception):
    """Raised when GitHub responds with 403 + rate-limit headers."""

    def __init__(self, sleep_for: int):
        super().__init__(f"rate limited; need to sleep {sleep_for}s")
        self.sleep_for = sleep_for


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def build_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "polyglot-codebase-llm-research/0.1",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        log("auth: using GITHUB_TOKEN (5000 req/hr, 30 search req/min)")
    else:
        log("auth: no GITHUB_TOKEN found — falling back to 60 req/hr unauth")
    return headers


@retry(
    retry=retry_if_exception_type(RateLimited),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=2, min=2, max=120),
    reraise=True,
)
def _do_search(query: str, page: int, headers: dict) -> dict:
    resp = requests.get(
        SEARCH_ENDPOINT,
        params={
            "q": query,
            "per_page": 100,
            "page": page,
            "sort": "stars",
            "order": "desc",
        },
        headers=headers,
        timeout=30,
    )
    if resp.status_code == 403 and "rate limit" in resp.text.lower():
        reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
        sleep_for = max(1, reset - int(time.time()) + 2)
        log(f"  rate-limited; will sleep {sleep_for}s and retry")
        time.sleep(sleep_for)
        raise RateLimited(sleep_for)
    resp.raise_for_status()
    return resp.json()


def project_item(item: dict, query: str) -> dict:
    """Project the GitHub Search response into the fields we keep."""
    return {
        "owner": item["owner"]["login"],
        "name": item["name"],
        "full_name": item["full_name"],
        "url": item["html_url"],
        "stars": item["stargazers_count"],
        "forks": item["forks_count"],
        "primary_language": item.get("language"),
        "size_kb": item["size"],
        "is_fork": item["fork"],
        "is_archived": item["archived"],
        "default_branch": item["default_branch"],
        "created_at": item["created_at"],
        "pushed_at": item["pushed_at"],
        "updated_at": item["updated_at"],
        "license": (item.get("license") or {}).get("spdx_id"),
        "topics": item.get("topics", []) or [],
        "description": item.get("description"),
        "_search_query": query,
        "_fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def search_pair(
    lang_pair: str,
    queries: list[str],
    *,
    dry_run: bool,
    headers: dict,
) -> Path:
    today = dt.date.today().isoformat()
    out_path = RAW_DIR / f"search-{lang_pair}-{today}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seen: set[str] = set()
    total_written = 0
    max_pages = 1 if dry_run else 10  # GitHub caps at 1000 results = 10 pages of 100

    with out_path.open("w") as f:
        for q_idx, query in enumerate(queries, start=1):
            log(f"[{lang_pair}] ({q_idx}/{len(queries)}) {query}")
            for page in range(1, max_pages + 1):
                try:
                    payload = _do_search(query, page, headers)
                except (RetryError, requests.HTTPError) as e:
                    log(f"  page {page}: request failed: {e}")
                    break
                items = payload.get("items", [])
                new_this_page = 0
                for item in items:
                    key = item["full_name"]
                    if key in seen:
                        continue
                    seen.add(key)
                    f.write(json.dumps(project_item(item, query)) + "\n")
                    total_written += 1
                    new_this_page += 1
                log(
                    f"  page {page}: {len(items)} returned, "
                    f"{new_this_page} new (total unique {total_written})"
                )
                if len(items) < 100:
                    break
                # Polite delay between pages (Search API is 30 req/min)
                time.sleep(2.5)
            # Polite delay between queries
            time.sleep(2.5)

    log(f"[{lang_pair}] wrote {total_written} unique repos → {out_path}")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch only the first page per query (cheap sanity check)",
    )
    parser.add_argument(
        "--lang-pair",
        choices=["java-ts", "python-go", "all"],
        default="all",
    )
    args = parser.parse_args()

    env_file = find_dotenv(usecwd=True)
    if env_file:
        load_dotenv(env_file)
        log(f"env: loaded {env_file}")
    else:
        log("env: no .env file found (will rely on shell env)")

    headers = build_headers()
    cfg = load_config()

    pairs = ["java-ts", "python-go"] if args.lang_pair == "all" else [args.lang_pair]
    for pair in pairs:
        cfg_key = pair.replace("-", "_")
        queries = cfg[cfg_key]["search_queries"]
        search_pair(pair, queries, dry_run=args.dry_run, headers=headers)

    log("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
