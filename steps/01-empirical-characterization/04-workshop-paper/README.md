# Sub-step 1.4 — Workshop Paper

**Maps to:** §6 item 17 of the [research plan](../../../Polyglot_Debugging_Research_Progress_Report.md) and Phase A of [ROADMAP.md](../../../ROADMAP.md).
**Goal:** A 4-page short paper synthesizing findings from sub-steps 1.1–1.3, targeting ICSE NIER 2027 or a co-located workshop.

**Working title:** *Towards Cross-Language Debugging Agents for Java+TypeScript Polyglot Systems — A Characterization and Research Agenda.*

## When this sub-step starts

In parallel with sub-steps 1.2–1.3. The outline can be written before there is data; the draft fills in as findings accumulate. Final draft requires all of:

- Repo corpus (sub-step 1.1) ✓
- ≥100 annotated bugs (sub-step 1.2) ✓
- One baseline agent run with failure-mode analysis (sub-step 1.3) ✓

## What goes in a 4-page workshop paper

NIER / workshop short papers are vision + evidence, not a full system. Section budget:

| Section | Page budget | Content |
|---------|-------------|---------|
| Introduction | 0.75 | The gap — single-language benchmarks vs polyglot reality |
| Background & motivation | 0.5 | Prior work pointers (iSWE-Agent, SWE-PolyBench, LANTERN) |
| Empirical study | 1.5 | Corpus, taxonomy, baseline numbers, failure modes |
| Research agenda | 0.75 | What this characterization implies for tool design |
| Threats to validity | 0.25 | Mining bias, annotator subjectivity, agent-version drift |
| Conclusion + future work | 0.25 | Pointer to Phase B/C |

References get ~0.5 page (NIER usually allows references not to count toward the limit, but check the venue's exact rules).

## Outputs

- **`sections/*.md`** — one file per section.
- **`figures/`** — plots and tables (PDF / PNG output, source script next to it).
- **`paper.tex` or `paper.md`** — assembled final draft (LaTeX preferred for IEEE/ACM templates).
- **`output/key-numbers.md`** — every quantitative claim with provenance ("36% of bugs are schema mismatches — source: bugs.jsonl filtered by category=schema").

## Figures we'll likely want

- **Figure 1:** Taxonomy with example bug per category. Conceptual, not a chart.
- **Figure 2:** Bug-count distribution per category, per language pair (bar chart).
- **Figure 3:** Baseline-agent resolution rate vs same agent's published single-language number. Headline result.
- **Table 1:** Failure-mode breakdown.

## Pitfalls

- **Over-claiming.** "First cross-language debugging agent" is Phase C. In Phase A: "First characterization of the gap." Watch the verbs.
- **No tool, no numbers from a tool.** Don't accidentally describe a tool we haven't built. Keep this paper purely empirical + agenda-setting.
- **Vague taxonomy.** Reviewers will hammer on annotation methodology. Inter-rater agreement should be reported even if solo (e.g., "single annotator, second annotator on 30-bug subset shows κ=X").

See [CLAUDE.md](CLAUDE.md), [outline.md](outline.md), and [STATUS.md](STATUS.md).
