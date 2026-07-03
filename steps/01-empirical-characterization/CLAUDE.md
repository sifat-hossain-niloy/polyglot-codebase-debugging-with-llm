# Agent Instructions — Step 1 (Empirical Characterization)

## Your job in this step

Produce two publishable artifacts:

1. **A cross-language bug dataset** (Java+TS, Python+Go) released on Zenodo with DOI.
2. **A 4-page workshop paper** characterizing the gap and presenting baseline numbers.

You're NOT building the agent system here. Resist scope creep into Step 2.

## Working order

Read [STATUS.md](STATUS.md) and pick up at the active sub-step. The order is:

1. [`01-github-mining/`](01-github-mining/CLAUDE.md) — find repos. Must finish before 02.
2. [`02-bug-extraction/`](02-bug-extraction/CLAUDE.md) — extract and annotate bugs. Must finish before 03 for a meaningful baseline.
3. [`03-baseline-evaluation/`](03-baseline-evaluation/CLAUDE.md) — run agents.
4. [`04-workshop-paper/`](04-workshop-paper/CLAUDE.md) — write up. Runs in parallel with 2–3 as data accumulates.

If you're tempted to work multiple sub-steps at once, don't — separate sessions per sub-step is the design.

## Decisions that only apply to this step

- **Languages to mine.** Two language pairs: Java+TypeScript AND Python+Go. Don't drop a pair without checking with the user — both pairs are core to the plan's claim.
- **Repo selection criteria.** ≥500 stars, ≥6 months active, has CI with tests. Tighten or relax only with documented rationale in [STATUS.md](STATUS.md).
- **Bug-annotation taxonomy.** Use the 6 categories in [docs/glossary.md](../../docs/glossary.md) (schema, coerce, nil, serde, async, other). Adding a category requires updating the glossary first.
- **What counts as a "cross-language" bug.** A closed PR that modified files in *both* languages of the pair (Java AND TS, or Python AND Go) AND where the issue can be traced to interaction between the two. Pure refactors that happen to touch both languages don't count.

## Things to keep checking against the plan

- §3.3 Step 1 (this step).
- §3.2 RQ3 (the research question this step answers).
- §6 items 13–17 (the immediate next steps the plan lists — they match this step's sub-steps closely).

## Outputs that exit this step

- `01-github-mining/data/processed/repos.jsonl`
- `02-bug-extraction/data/processed/bugs.jsonl`
- `02-bug-extraction/taxonomy.md`
- `03-baseline-evaluation/output/results.jsonl`
- `04-workshop-paper/sections/*.md`
- Updated `STATUS.md` at each level

When all are produced, mark this step 🟢 in `STATUS.md` and update the global [STATUS.md](../../STATUS.md).

## Common traps

- Don't annotate bugs without first running ≥10 through the taxonomy and refining categories. Premature scaling.
- Don't run a full baseline agent sweep without first costing it. iSWE-Agent at scale is expensive.
- Don't write the paper before there are real numbers to put in it. Skeleton outline first, evidence second.
