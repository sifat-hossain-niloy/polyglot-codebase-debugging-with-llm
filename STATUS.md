# Global Status

**Last updated:** 2026-06-27
**Target:** FSE 2027 Research Papers track. **Deadline: 2026-10-02 (14 weeks from today).**
**Active step:** [Step 1 — Empirical Characterization](steps/01-empirical-characterization/STATUS.md)
**Active sub-step:** [02-bug-extraction](steps/01-empirical-characterization/02-bug-extraction/STATUS.md)

> **Plan change (2026-06-27):** switched from a chunk-by-chunk workshop→conference plan to a single FSE 2027 submission. The workshop-paper deliverable is dropped; its outline folds into the FSE paper's §3 (Empirical Study). See [ROADMAP.md](ROADMAP.md) for the 14-week schedule and [docs/publication-strategy.md](docs/publication-strategy.md) for the graceful-degrade to an empirical-only paper if Steps 2–4 slip.

## At a glance

| Step | Status | Output | Notes |
|------|--------|--------|-------|
| 01 — Empirical Characterization | 🟡 1.1 done; 1.2 batches 1+2 done (19/100 bugs) | FSE paper §3 evidence | 145 repos ✓, 19 bugs ✓ |
| 02 — Call Graph & Schema | ⚪ Not started | Cross-language SCIP graph + schema parser | Blocked on Step 1 dataset |
| 03 — Dual-Agent System | ⚪ Not started | Cross-language localize-then-edit agent | Blocked on Step 2 |
| 04 — Evaluation & Ablations | ⚪ Not started | Ablation results + human eval | Blocked on Step 3 |

Legend: 🟢 done · 🟡 in progress · 🔴 blocked · ⚪ not started

## What was done in the last session (2026-07-08)

- **Sub-step 1.2 batch 1 complete:** wrote the full pipeline (`fetch_prs.py`, `triage_prs.py`, `classify_prs.py`, `bug_stats.py`) plus `taxonomy.md`, `annotation-guide.md`, and versioned prompt `bug-classifier-v1.md`.
- Fetched 1,206 raw cross-language PRs from the 145 mined repos; triage kept 668 candidates.
- Manually classified 50 top-signal candidates in-conversation: **12 confirmed cross-language bugs (24% acceptance), 38 skipped.**
- Bug distribution already shows meaningful pattern: `schema` bugs cluster at REST + gRPC boundaries, `coerce` bugs cluster at FFI boundary. `serde` and `other` categories still empty — more sampling needed.

## Next session should

1. Read [steps/01-empirical-characterization/02-bug-extraction/STATUS.md](steps/01-empirical-characterization/02-bug-extraction/STATUS.md).
2. **Continue sub-step 1.2** — batch 2 of manual annotations. Pick the next 50 candidates that weren't in batch 1 (`data/processed/candidates-2026-07-08.jsonl` has 668 total; batch 1 covered the top 50 by score). Aim for another 10–15 confirmed bugs.
3. **Or scale via API:** if user provides `ANTHROPIC_API_KEY`, run `classify_prs.py --limit 500` for LLM-assisted bulk classification; human confirms every headline claim.
4. Same `GITHUB_TOKEN` and `uv` env from earlier sub-steps carry over.

## Open questions (global)

- **GitHub token rotation.** The token was shared in chat during 1.1; once 1.2 finishes API work, rotate at https://github.com/settings/tokens.
- **Second annotator for κ.** Plan says two annotators per §3.3 Step 1.2. Solo for now; need to recruit a second before any inter-rater agreement is reported in the paper.
- **Sampling strategy for Step 1.2.** 145 repos × ~5 PRs each ≈ 725 candidate PRs. Annotation budget realistically supports ~100. Suggest stratified sampling by pair + star range.
- **Compute budget for baseline agents (Step 1.3):** running iSWE-Agent or MASAI at scale is expensive. Cost estimate required before Step 1.3.
- **Public release plan:** Zenodo DOI for dataset, GitHub for code. Confirm before any data is published.

## Memory note for Claude

When resuming a session: don't re-summarize the plan or re-derive what the next step is. Read this file, the active sub-step's `STATUS.md`, and act.
