# Scripts — Sub-step 1.1

Pipeline:

```
search_repos.py   →   enrich_repos.py   →   filter_repos.py   →   summarize.py
   (Search API)        (/languages +          (selection           (output/
                        root contents)         criteria,            repo-summary.md)
                                               schema check)
```

## Prerequisites

- Python env via `uv` at the step level. Run once from `steps/01-empirical-characterization/`:
  ```
  uv sync
  ```
- `GITHUB_TOKEN` in `.env` at the repo root.

## Running the full pipeline

From `steps/01-empirical-characterization/`:

```bash
# 1. Search GitHub for candidate repos. Cheap dry-run first:
uv run 01-github-mining/scripts/search_repos.py --dry-run

# 2. Full search (10 pages × queries × pairs, ~5–10 min):
uv run 01-github-mining/scripts/search_repos.py

# 3. Enrich with /languages + root file detection (resumable):
uv run 01-github-mining/scripts/enrich_repos.py

# 4. Apply selection criteria, write final corpus:
uv run 01-github-mining/scripts/filter_repos.py

# 5. Generate the human-readable summary the paper cites:
uv run 01-github-mining/scripts/summarize.py
```

## Single-pair mode

For iterating on one pair without retouching the other:

```bash
uv run 01-github-mining/scripts/search_repos.py --lang-pair java-ts
uv run 01-github-mining/scripts/enrich_repos.py --lang-pair java-ts
```

## Resumability

- `search_repos.py` overwrites — running it again retraces all queries.
- `enrich_repos.py` is resumable — already-enriched repos are skipped. To force re-enrich, delete `data/raw/enriched-*.jsonl`.
- `filter_repos.py` is idempotent — overwrites `data/processed/repos.jsonl`.

## Tuning the filter

If too many repos are rejected:

- Loosen language fraction: edit `configs/queries.yaml` → `<pair>.filters.min_fraction_per_required_language`.
- Allow non-permissive licenses: `uv run filter_repos.py --include-non-permissive-license`.
- Bypass age check: edit `configs/queries.yaml` → `defaults.min_created_before`.

Check `output/rejected.jsonl` first — the per-reason histogram tells you what's worth changing.

## Files written

| Path | Schema | Tracked? |
|------|--------|----------|
| `data/raw/search-<pair>-<date>.jsonl` | ad-hoc | gitignored |
| `data/raw/enriched-<pair>-<date>.jsonl` | ad-hoc | gitignored |
| `data/processed/repos.jsonl` | `shared/schemas/repo.schema.json` | **tracked** (small, paper artifact) |
| `output/rejected.jsonl` | ad-hoc | tracked (small) |
| `output/repo-summary.md` | n/a | tracked |
| `output/search-full-*.log` | n/a | tracked |
