# Sub-step 1.1 — GitHub Mining

**Maps to:** §3.3 Step 1.1 + §6 item 13 of the [research plan](../../../Polyglot_Debugging_Research_Progress_Report.md).
**Goal:** Produce a list of 50–100 candidate polyglot repositories per language pair (Java+TS, Python+Go), with metadata sufficient to drive later bug extraction.

## What "candidate" means

A repo is a candidate if it meets all of:

- **Polyglot composition.** Both languages of the pair present, each as a non-trivial fraction of the codebase. For Java+TS: ≥10% Java AND ≥10% TS by GitHub's `languages` API. For Python+Go: same.
- **Activity.** ≥6 months of commit activity, ≥1 commit in the last 90 days.
- **Quality signal.** ≥500 stars OR (≥100 stars AND CI configuration files present).
- **Has tests.** Detected via standard markers (`pom.xml` with surefire, `package.json` with `test` script, `go.mod` with `_test.go` files, etc.).
- **License.** Permissive (MIT, Apache 2.0, BSD-3) so the bug dataset can be released.

## Inputs

- GitHub personal access token (set as `GITHUB_TOKEN` in env, never committed).
- Query strategy in `configs/queries.yaml` (to be written).

## Outputs

- **`data/processed/repos.jsonl`** — one JSON object per repo, conforming to [`shared/schemas/repo.schema.json`](../../../shared/schemas/repo.schema.json).
- **`output/repo-summary.md`** — human-readable summary: counts per language pair, distribution of stars / sizes / org vs personal.

## Suggested execution

This is a research script, not production code. Expected structure:

```
01-github-mining/
├── scripts/
│   ├── search_repos.py       Query GitHub Search API by topic + language
│   ├── enrich_repos.py       Pull /languages, /contents for filter checks
│   └── filter_repos.py       Apply selection criteria, write final JSONL
├── configs/
│   └── queries.yaml          Topic / keyword / star-cutoff per language pair
├── data/
│   ├── raw/                  Paginated API responses (gitignored)
│   └── processed/
│       └── repos.jsonl       Final filtered list
└── output/
    └── repo-summary.md       Stats for the paper
```

## Pitfalls to avoid

- **GitHub Search API rate limits.** 30 requests/min authenticated. Build retry+backoff.
- **Over-relying on `languages` byte counts.** Generated code (e.g., gRPC bindings) inflates one language. Spot-check.
- **Forks and mirrors.** Filter `fork: false` and check `mirror_url` is null.
- **Monorepo vs polyrepo.** Both are valid for Java+TS pair (e.g., Nx monorepos). Don't exclude one architecture without rationale.

See [CLAUDE.md](CLAUDE.md) for agent-facing instructions and [STATUS.md](STATUS.md) for state.
