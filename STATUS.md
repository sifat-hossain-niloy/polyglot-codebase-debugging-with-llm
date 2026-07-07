# Global Status

**Last updated:** 2026-06-27
**Target:** FSE 2027 Research Papers track. **Deadline: 2026-10-02 (14 weeks from today).**
**Active step:** [Step 1 — Empirical Characterization](steps/01-empirical-characterization/STATUS.md)
**Active sub-step:** [02-bug-extraction](steps/01-empirical-characterization/02-bug-extraction/STATUS.md)

> **Plan change (2026-06-27):** switched from a chunk-by-chunk workshop→conference plan to a single FSE 2027 submission. The workshop-paper deliverable is dropped; its outline folds into the FSE paper's §3 (Empirical Study). See [ROADMAP.md](ROADMAP.md) for the 14-week schedule and [docs/publication-strategy.md](docs/publication-strategy.md) for the graceful-degrade to an empirical-only paper if Steps 2–4 slip.

## At a glance

| Step | Status | Output | Notes |
|------|--------|--------|-------|
| 01 — Empirical Characterization | 🟡 1.1 done; 1.2 next | Workshop paper + bug dataset | 145 polyglot repos mined ✓ |
| 02 — Call Graph & Schema | ⚪ Not started | Cross-language SCIP graph + schema parser | Blocked on Step 1 dataset |
| 03 — Dual-Agent System | ⚪ Not started | Cross-language localize-then-edit agent | Blocked on Step 2 |
| 04 — Evaluation & Ablations | ⚪ Not started | Ablation results + human eval | Blocked on Step 3 |

Legend: 🟢 done · 🟡 in progress · 🔴 blocked · ⚪ not started

## What was done in the last session (2026-06-27)

- Built the GitHub mining pipeline (sub-step 1.1): 4 Python scripts (search/enrich/filter/summarize), 25 search queries across both pairs, JSON-Schema-validated output.
- **Produced the repo corpus:** 145 polyglot repositories (61 Java+TS, 84 Python+Go) committed to [steps/01-empirical-characterization/01-github-mining/data/processed/repos.jsonl](steps/01-empirical-characterization/01-github-mining/data/processed/repos.jsonl). Both pairs cleared the 50-repo target.
- Documented two filter calibrations as findings for the paper: (a) test-marker check made informational (CI presence is the real test signal), (b) python-go language-fraction lowered from 5%→2% because python-go monorepos are inherently Go-dominant.
- Noted a sub-population (React Native libraries in java-ts) whose cross-language bugs are FFI-mediated rather than REST-mediated — Step 1.2 should tag these separately.

## Next session should

1. Read [steps/01-empirical-characterization/STATUS.md](steps/01-empirical-characterization/STATUS.md) and [steps/01-empirical-characterization/02-bug-extraction/CLAUDE.md](steps/01-empirical-characterization/02-bug-extraction/CLAUDE.md).
2. Start sub-step 1.2 — Bug Extraction. First task: write `fetch_prs.py` that pages closed merged PRs per repo via GitHub GraphQL.
3. The same `GITHUB_TOKEN` and same `uv` env from sub-step 1.1 carry over.

## Open questions (global)

- **GitHub token rotation.** The token was shared in chat during 1.1; once 1.2 finishes API work, rotate at https://github.com/settings/tokens.
- **Second annotator for κ.** Plan says two annotators per §3.3 Step 1.2. Solo for now; need to recruit a second before any inter-rater agreement is reported in the paper.
- **Sampling strategy for Step 1.2.** 145 repos × ~5 PRs each ≈ 725 candidate PRs. Annotation budget realistically supports ~100. Suggest stratified sampling by pair + star range.
- **Compute budget for baseline agents (Step 1.3):** running iSWE-Agent or MASAI at scale is expensive. Cost estimate required before Step 1.3.
- **Public release plan:** Zenodo DOI for dataset, GitHub for code. Confirm before any data is published.

## Memory note for Claude

When resuming a session: don't re-summarize the plan or re-derive what the next step is. Read this file, the active sub-step's `STATUS.md`, and act.
