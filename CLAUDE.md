# Project Context for Claude

## What this repo is

Research project: **Polyglot Codebase Debugging and Cross-Language Program Repair with LLMs and Agentic AI**, targeting a workshop paper first, then ICSE/FSE 2027. Full plan: [Polyglot_Debugging_Research_Progress_Report.md](Polyglot_Debugging_Research_Progress_Report.md).

PI: Fahim (fahim@cse.du.ac.bd).

## Current focus

**Target: FSE 2027 Research Papers, deadline 2026-10-02.** 14-week compressed schedule from 2026-06-27. **Step 1 — Empirical Characterization** must complete by end of Week 3 (2026-07-21). See [ROADMAP.md](ROADMAP.md) for the week-by-week plan and decision points, and [STATUS.md](STATUS.md) for where we are right now.

Do NOT default to the earlier workshop-first plan. That path is dropped; the workshop-paper outline now lives inside the FSE paper's §3 (Empirical Study).

## How work is organized

```
steps/01-empirical-characterization/   ← active
  01-github-mining/                    ← sub-step
  02-bug-extraction/
  03-baseline-evaluation/
  04-workshop-paper/
steps/02-call-graph-schema/            ← future (placeholder)
steps/03-dual-agent-system/            ← future
steps/04-evaluation-ablations/         ← future
```

Each step and sub-step has:
- `README.md` — what the step is, inputs, outputs
- `CLAUDE.md` — instructions for the agent working on this step
- `STATUS.md` — what's done, what's next (source of truth across sessions)

## Rules for every session

1. **Start by reading the active step's `STATUS.md`.** It tells you where the previous session stopped. Don't re-derive — read.
2. **Update `STATUS.md` when you finish a sub-task** — this is how the next session picks up cleanly.
3. **Follow `docs/conventions.md`** for file naming, data formats, and where things go.
4. **Don't skip ahead.** Step 2 depends on Step 1's annotated bug corpus existing. If you think you need to skip, raise it with the user.
5. **Cite the research plan section.** When making decisions, reference the section of [Polyglot_Debugging_Research_Progress_Report.md](Polyglot_Debugging_Research_Progress_Report.md) you're acting on (e.g., "§3.3 Step 1.2").
6. **Treat unknowns as research questions, not blockers.** If something is unspecified (e.g., exact bug taxonomy granularity), record the open question in the relevant `STATUS.md` and propose a default — don't stall.

## Key references

- [Research plan](Polyglot_Debugging_Research_Progress_Report.md) — authoritative source for scope, RQs, methodology
- [ROADMAP.md](ROADMAP.md) — publication path: workshop → empirical paper → conference
- [docs/glossary.md](docs/glossary.md) — SCIP, iSWE-Agent, MASAI, etc.
- [docs/conventions.md](docs/conventions.md) — file naming, data formats, scripting language
- [docs/workflow.md](docs/workflow.md) — how to run a session in this repo

## What NOT to do

- Don't write tools (Step 2 work) before Step 1's empirical corpus is annotated.
- Don't claim novelty or results without checking [docs/glossary.md](docs/glossary.md) for prior work (xLoc, Cai et al., LANTERN, iSWE-Agent).
- Don't commit raw GitHub-mined data into the repo without checking size — use the gitignore patterns in [.gitignore](.gitignore).
- Don't run iSWE-Agent / MASAI / SWE-agent without first reading their licenses and resource requirements (see [steps/01-empirical-characterization/03-baseline-evaluation/README.md](steps/01-empirical-characterization/03-baseline-evaluation/README.md)).
