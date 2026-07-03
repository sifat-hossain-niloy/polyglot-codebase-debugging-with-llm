# Polyglot Codebase LLM

Research codebase for **cross-language fault localization and program repair** in polyglot systems (Java↔TypeScript, Python↔Go) using LLM-based agents.

## TL;DR

Modern enterprise stacks span multiple languages. LLM debugging agents perform at ~70–80% on single-language Python benchmarks but drop to 10–33% on cross-language enterprise tasks. We're building the first system that treats the **language boundary** as a first-class object of debugging.

Full plan: [Polyglot_Debugging_Research_Progress_Report.md](Polyglot_Debugging_Research_Progress_Report.md).

## Publication strategy

We're delivering this **chunk by chunk**, not all at once:

| Stage | Output | Timing |
|------|--------|--------|
| **Phase A** | Workshop short paper (NIER / ICSE workshop) + annotated bug dataset | Months 1–3 |
| **Phase B** | Empirical/MSR paper on cross-language bug taxonomy | Months 3–6 |
| **Phase C** | Conference paper (ICSE / FSE 2027) — full agent system + evaluation | Months 6–15 |
| **Phase D** | Journal extension (TOSEM / TSE) | Post-conference |

See [ROADMAP.md](ROADMAP.md) for milestones and [STATUS.md](STATUS.md) for where we are right now.

## How to navigate this repo

```
.
├── CLAUDE.md                                  agent-facing master instructions
├── README.md                                  ← you are here
├── ROADMAP.md                                 phase-by-phase publication path
├── STATUS.md                                  global status across all steps
├── Polyglot_Debugging_Research_Progress_Report.md   research plan (authoritative)
│
├── docs/
│   ├── conventions.md                         file naming, data formats, languages
│   ├── glossary.md                            SCIP, iSWE-Agent, MASAI, LANTERN…
│   ├── publication-strategy.md                workshop → conference details
│   └── workflow.md                            how to work in this repo
│
├── steps/
│   ├── 01-empirical-characterization/         ← active
│   ├── 02-call-graph-schema/                  placeholder
│   ├── 03-dual-agent-system/                  placeholder
│   └── 04-evaluation-ablations/               placeholder
│
└── shared/
    ├── prompts/                               reusable LLM prompts
    ├── schemas/                               JSON Schemas for shared data
    └── utils/                                 cross-step utility scripts
```

## Working with Claude on this repo

This repo is designed for multi-session work. Open a Claude Code session at the repo root and Claude will:

1. Auto-load [CLAUDE.md](CLAUDE.md) for global context.
2. Check [STATUS.md](STATUS.md) to find the active step.
3. `cd` into the active sub-step, read its `CLAUDE.md`, and continue from where the last session stopped.

See [docs/workflow.md](docs/workflow.md) for the session protocol.

## Current focus (Step 1)

[Empirical Characterization](steps/01-empirical-characterization/README.md) — mine cross-language bug corpora from GitHub, build the taxonomy, run baselines. Outputs: workshop paper + annotated dataset.
