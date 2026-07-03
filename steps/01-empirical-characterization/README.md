# Step 1 — Empirical Characterization

**Maps to:** §3.3 Step 1 of the [research plan](../../Polyglot_Debugging_Research_Progress_Report.md).
**Timeline:** Months 1–3.
**Goal:** Establish empirical ground truth about cross-language bugs *before* any tool is built. Output of this step seeds both Phase A (workshop paper) and Phase B (empirical paper).

## Why this step is first

Every later step depends on the artifacts produced here:

- The annotated bug corpus is the only evaluation set that specifically tests boundary-crossing bugs.
- The baseline numbers from Step 1.3 define what Phase C (the conference paper) has to beat.
- The bug taxonomy from Step 1.2 informs the schema/feature design of the cross-language call graph in Step 2.

Skipping this step would leave the whole project unfalsifiable.

## Sub-steps

| # | Sub-step | Purpose | Output |
|---|----------|---------|--------|
| [01](01-github-mining/README.md) | GitHub mining | Find polyglot repos worth analyzing | Repo metadata JSONL |
| [02](02-bug-extraction/README.md) | Bug extraction & annotation | Identify and classify cross-language bugs | Annotated bug corpus JSONL |
| [03](03-baseline-evaluation/README.md) | Baseline agent eval | Measure where current SOTA agents fail | Per-bug results + failure-mode breakdown |
| [04](04-workshop-paper/README.md) | Workshop paper | Synthesize findings into a 4-page short paper | Draft + figures |

Sub-steps 1 → 2 → 3 are sequential. Sub-step 4 (paper) runs in parallel with 2–3 as evidence accumulates.

## Inputs

- Research plan (`../../Polyglot_Debugging_Research_Progress_Report.md`).
- GitHub API token (set in env, never committed — see [docs/conventions.md](../../docs/conventions.md)).
- Optional: API budget for running baseline agents (Step 1.3).

## Outputs

- **`01-github-mining/data/processed/repos.jsonl`** — list of candidate polyglot repositories with metadata.
- **`02-bug-extraction/data/processed/bugs.jsonl`** — annotated cross-language bugs.
- **`02-bug-extraction/taxonomy.md`** — finalized taxonomy with examples per category.
- **`03-baseline-evaluation/output/results.jsonl`** — per-bug agent results with failure modes.
- **`04-workshop-paper/sections/*.md`** — paper draft.

All conform to schemas in [`shared/schemas/`](../../shared/schemas/).

## How to work this step

See [CLAUDE.md](CLAUDE.md) for the agent-facing instructions. The short version: read [STATUS.md](STATUS.md), find the active sub-step, work it, update its STATUS.

## Exit criteria

Step 1 is complete when:

1. Repo corpus is mined (50–100 per language pair) and metadata is schema-conformant.
2. ≥100 cross-language bugs are annotated, with category counts reported.
3. At least one baseline agent has run end-to-end on ≥20 of those bugs.
4. The workshop paper is drafted and reviewed.

When all four are checked, update the global [STATUS.md](../../STATUS.md) and unblock Step 2.
