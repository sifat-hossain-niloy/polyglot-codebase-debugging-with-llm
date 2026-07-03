# Publication Strategy

Chunk-by-chunk plan to convert this research into a sequence of accepted publications rather than betting everything on a single conference submission. Source: ROADMAP.md, §4 of the research plan.

## Why incremental?

- **Risk reduction.** If iSWE-Agent's full paper comes out mid-2026, we still have a workshop paper banked.
- **Feedback loop.** Workshop reviews and MSR data-paper reviews sharpen the conference submission.
- **Public artifacts.** Each phase releases a dataset or short paper that builds citation momentum.

## Phases mapped to artifacts

| Phase | Months | Active step(s) | Artifact | Venue |
|-------|--------|----------------|----------|-------|
| A | 1–3 | Step 1 | 4-page short paper + Zenodo dataset (v1) | ICSE NIER / workshop |
| B | 3–6 | Step 1 (extended) | Full empirical paper + dataset (v2) | MSR or ICSE empirical track |
| C | 6–15 | Steps 2–4 | Full system + evaluation paper | ICSE / FSE 2027 |
| D | post-C | extensions | Journal extension | TOSEM / TSE |

## Phase A — workshop paper

### Hard requirements before submission

- Mined repo corpus exists and is reproducible (`scripts/` + `data/processed/`).
- ≥100 cross-language bugs annotated, with at least one secondary annotator on a 30-bug subset for κ.
- Baseline numbers: at least one of (iSWE-Agent / MASAI / SWE-agent) executed end-to-end on ≥20 cross-language bugs from our corpus, with failure-mode breakdown.
- Short paper draft reviewed once by the user.

### Positioning

Lead with the **gap**: prior benchmarks (SWE-PolyBench, Multi-SWE-bench) test languages independently. No one has measured agent performance specifically on bugs that *require* cross-language reasoning. Our contribution is:

1. The first cross-language-bug corpus for Java+TS and Python+Go.
2. Empirical demonstration that current SOTA agents fail predictably at the boundary.
3. A taxonomy of failure modes that defines the research agenda.

### Things to avoid

- Don't promise the dual-agent system in the workshop paper. That's Phase C.
- Don't over-claim the dataset size — 100 bugs is fine for a workshop short paper. The empirical paper (Phase B) is where size grows.
- Don't run baseline agents at full scale yet — pick a representative subset to make Phase A's cost bounded.

## Phase B — empirical paper

### What grows from Phase A

- Dataset to 200–400 bugs.
- All 6 taxonomy categories populated with ≥15 examples each.
- All three baseline agents run on the full corpus.
- Statistical analysis: which taxonomy categories correlate with which agent-failure modes.

### Positioning

Phase A says "the problem exists." Phase B says "here is the structure of the problem, in detail, at scale."

### Hard requirements

- Inter-rater reliability formally reported (κ ≥ 0.7 target).
- A reproducibility package: scripts, configs, model versions, prompt versions.
- A data statement (per ICSE/MSR norms): selection criteria, exclusions, demographic/representational notes on the GitHub population.

## Phase C — conference paper

### What grows from Phases A and B

- The cross-language agent itself (Steps 2 and 3 of the plan).
- Evaluation on SWE-PolyBench + Multi-SWE-bench Java + our annotated corpus.
- Ablations isolating (a) cross-language graph and (b) schema-aware hypothesis generation.
- Human eval of patch quality on 50 bugs.

### Positioning

Two narrative options — pick when results are in:

- **Tool-first narrative:** "We built a cross-language localize-then-edit agent. It beats single-language baselines by X% on cross-boundary bugs."
- **Analysis-first narrative:** "We characterize *why* current agents fail at boundaries (Phases A/B), then show that addressing the specific failure modes (schema unawareness, missing cross-language graph) yields X% improvement."

The analysis-first narrative is stronger if the absolute resolution rate is moderate (10–25%, the §5.2 risk).

### Hard requirements

- Beats single-language baselines on cross-boundary bugs (RQ1).
- Cross-language graph improves localization precision over single-language graphs (RQ2).
- Either RQ4 (translate-to-repair for Python+Go) succeeds OR has a clean negative result with explanation.
- Tool and data both open-sourced.

## Phase D — journal extension

Triggered after Phase C is accepted. Adds:

- A third language pair or N-language case (per the 2026 "N-language Polyglot Programs" vision paper).
- Cross-session memory experiments.
- Broader human-eval cohort.

## Workshop venue shortlist (Phase A)

To check submission deadlines closer to draft time:

- **ICSE 2027 NIER** — short, vision-friendly.
- **AIware @ FSE/ICSE** — AI-for-software-engineering co-located.
- **InteNSE** — international workshop on interpretable and trustworthy NL-driven SE.
- **LLM4Code** — emerging focused workshop.
- **MSR 2026 Mining Challenge** — data-paper track, fits the dataset release.

## Risks specific to publication

- **iSWE-Agent arXiv release.** Mitigated by Phase A's cross-language scope (orthogonal).
- **Reviewer asks "where are the comparison numbers?"** — Phase A must have at least one full baseline run on cross-language bugs.
- **Dataset license / GDPR concerns.** GitHub-mined PR content is generally fine, but PII in commit messages / linked issues is a risk. Review before public release.

## Tracking

When a paper deadline is set or a draft milestone is hit, log it in [ROADMAP.md](../ROADMAP.md) under "Decision points," not here. Keep this document about *strategy*; let ROADMAP carry the dates.
