# Status: Step 1 — Empirical Characterization

**Last updated:** 2026-06-27
**State:** 🟡 In progress (sub-step 1.1 complete; 1.2 ready to start)
**Active sub-step:** [02-bug-extraction/](02-bug-extraction/STATUS.md)
**Deadline:** Step 1 fully done by 2026-07-21 (end of Week 3 in the FSE 2027 schedule)

> **Plan change 2026-06-27:** we now target FSE 2027 full paper by 2026-10-02, not the earlier workshop→conference chunked path. Step 1 remains the same in content but is compressed into 3 weeks. See [../../ROADMAP.md](../../ROADMAP.md).

## Sub-step states

| Sub-step | State | Last updated | Owner |
|----------|-------|--------------|-------|
| [01-github-mining](01-github-mining/STATUS.md) | 🟢 done | 2026-06-27 | Sifat |
| [02-bug-extraction](02-bug-extraction/STATUS.md) | 🟡 batches 1+2 done (19/100 bugs) | 2026-07-08 | Sifat |
| [03-baseline-evaluation](03-baseline-evaluation/STATUS.md) | 🔴 blocked on 02 hitting 20+ bugs | 2026-06-23 | unassigned |
| [04-workshop-paper](04-workshop-paper/STATUS.md) | ⚪ can start writing methodology + corpus paragraphs | 2026-06-23 | unassigned |

## What's done at the step level

- Sub-step scaffolding written (READMEs, CLAUDE.md, STATUS).
- Bug taxonomy seeded in [docs/glossary.md](../../docs/glossary.md) with 6 categories.
- **Sub-step 1.1 done:** 145 polyglot repos accepted (61 java-ts, 84 python-go). See [01-github-mining/STATUS.md](01-github-mining/STATUS.md) for findings + decisions logged for the paper.

## What's next

Start [02-bug-extraction](02-bug-extraction/CLAUDE.md). Input is [`01-github-mining/data/processed/repos.jsonl`](01-github-mining/data/processed/repos.jsonl). First task per its CLAUDE.md: write `fetch_prs.py` to page closed merged PRs per repo.

## Open questions (step-wide)

- **Second annotator for κ.** Plan says two annotators per §3.3 Step 1.2. Solo for now; need to recruit a second before any inter-rater agreement is reported in the paper.
- **Sampling strategy for Step 1.2.** 145 repos × ~5 PRs each ≈ 725 candidate PRs. Annotation budget realistically supports ~100. Decision needed: stratified by pair / by stars, or simple random sample. Suggest stratified to ensure both pairs and a star range are represented.
- **Compute budget for Step 1.3.** TBD — depends on which baseline agent we use. Cost-estimate before running anything at scale.
- **React Native sub-population.** Several accepted java-ts repos are RN libraries (Android JNI bridge, not REST). Their cross-language bugs are FFI-mediated, which is a different category from our primary REST/gRPC target. Either tag separately in Step 1.2 or exclude.

## Artifacts produced so far

- `01-github-mining/configs/queries.yaml` — query strategy.
- `01-github-mining/data/processed/repos.jsonl` — 145 schema-validated repos.
- `01-github-mining/output/repo-summary.md` — paper-ready table.
- `01-github-mining/output/rejected.jsonl` — 2,227 rejections with reasons.
