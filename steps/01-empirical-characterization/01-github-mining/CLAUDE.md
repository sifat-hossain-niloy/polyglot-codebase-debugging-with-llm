# Agent Instructions — Sub-step 1.1 (GitHub Mining)

## Concrete first session

Read [STATUS.md](STATUS.md). If the state is ⚪ not started, do this in order:

1. **Draft the query strategy** as `configs/queries.yaml`. Capture:
   - GitHub search queries per language pair (using topics, language filters, keywords like `spring-boot react`, `grpc python go`).
   - Star cutoffs and activity filters.
   - List of exclusion terms (tutorial, example, demo, template).

2. **Write `scripts/search_repos.py`** (Python). It should:
   - Read the YAML config.
   - Hit GitHub Search API with backoff for rate limits.
   - Page through results and write raw responses to `data/raw/search-<lang-pair>-<date>.jsonl`.
   - **Take a `--dry-run` flag** that fetches only the first page so you can sanity-check before burning rate limits.
   - Authenticate via `GITHUB_TOKEN` env var. Fail clearly if missing.

3. **Write `scripts/enrich_repos.py`.** For each repo from step 2:
   - Fetch `/repos/{owner}/{name}/languages` for byte distribution.
   - Fetch `/repos/{owner}/{name}/contents/` to check for CI files (`.github/workflows/`, `.circleci/`, `Jenkinsfile`), test markers, and licensing.
   - Append enriched record to `data/raw/enriched-<date>.jsonl`.

4. **Write `scripts/filter_repos.py`.** Apply the selection criteria from [README.md](README.md) and emit `data/processed/repos.jsonl` conforming to [`shared/schemas/repo.schema.json`](../../../shared/schemas/repo.schema.json).

5. **Generate `output/repo-summary.md`.** Stats per language pair: count, median stars, license distribution, monorepo-vs-polyrepo split.

6. **Update [STATUS.md](STATUS.md).** Mark 🟢 done. Record: how many repos per pair, where the artifacts are, any unexpected findings.

## Pre-script checks

Before writing any code:

- Confirm the user has provided / will provide a `GITHUB_TOKEN`. Don't run search at scale without one (60 unauthenticated requests/hour will get you nowhere).
- Estimate API call budget. With proper filtering, expect ~3,000–5,000 calls. Well inside daily limits but plan for retries.
- Decide: is this incremental? If we want to re-run monthly, partition raw dumps by date so reruns don't overwrite.

## Validation before you stop

- `data/processed/repos.jsonl` validates against [`shared/schemas/repo.schema.json`](../../../shared/schemas/repo.schema.json). Use a JSON Schema validator (Python's `jsonschema` package).
- Spot-check 5 repos manually: visit them on GitHub, confirm they really are polyglot and active.
- `output/repo-summary.md` has the counts the paper will cite.

## Definition of done

🟢 means:
- `data/processed/repos.jsonl` exists and has ≥50 repos per language pair (or a documented reason in STATUS for why fewer).
- The file validates against the schema.
- `output/repo-summary.md` has the per-pair stats.
- `STATUS.md` lists the next sub-step (02) as unblocked.

## Don't

- Don't clone the repos here. That's Step 1.2 (bug extraction needs the PRs, not the full repo).
- Don't store API tokens or full unfiltered dumps in git. The `.gitignore` covers it but verify.
- Don't filter too aggressively in this sub-step — it's easier to over-collect and filter later than to re-mine.
