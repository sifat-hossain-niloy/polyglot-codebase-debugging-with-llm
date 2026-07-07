# Publication Strategy

**Primary target: FSE 2027 Research Papers track. Deadline: 2026-10-02.**

This document replaces the earlier phased workshop→empirical→conference plan. We are compressing to a single FSE submission, with a graceful-degrade to an empirical-only paper if the tool work slips.

## Why a single-shot strategy?

- The FSE 2027 deadline gives us 14 weeks from 2026-06-27. That's enough for one strong submission, not three sequential ones.
- Sequential workshop/empirical papers would consume writing time we need for the FSE draft.
- FSE is the same tier as ICSE — a single accepted paper here is worth more than three intermediate workshop papers.

## What we're submitting

**Working title:** *Cross-Language Localize-then-Edit: An Agentic Debugging System for Java+TypeScript and Python+Go Polyglot Codebases*

**Track:** Research Papers (full, up to 22 pages including references).

**Structure (approximate page budget):**

| Section | Pages | Content |
|---------|-------|---------|
| Introduction | 1.5 | The gap, our contribution, RQs |
| Background & Related Work | 2 | Multi-lang benchmarks, iSWE-Agent, PyXray, LANTERN, N-language vision paper |
| Empirical Study | 4 | Corpus (Step 1.1), taxonomy (Step 1.2), baseline failure modes (Step 1.3) |
| Cross-Language Call Graph | 3 | SCIP + tree-sitter + REST/gRPC schema edges (Step 2) |
| Dual-Agent System | 3 | Cross-language localizer + cross-language editor + execution feedback (Step 3) |
| Evaluation | 4 | RQs 1–4 with ablations on SWE-PolyBench + our corpus (Step 4) |
| Human Evaluation | 1 | 50 patches × 10 engineers → correctness/plausibility/completeness |
| Threats to Validity | 0.5 | Mining bias, annotator subjectivity, agent version drift |
| Discussion + Conclusion | 1 | Findings + future work |
| References | ~2 | 40–60 refs |

## Hard requirements to submit

**By 2026-09-29 (draft-complete day):**

- ≥100 annotated cross-language bugs, corpus schema-validated.
- Cross-language call graph proof of concept working on ≥5 curated bug traces.
- Dual-agent system runs end-to-end on the corpus; per-bug results captured.
- Ablations demonstrating RQ1 and RQ2 (cross-language graph on/off; schema-awareness on/off).
- At least one language-pair result strong enough to lead with — Java+TS is our primary target; Python+Go can be a secondary case study if it's weaker.
- Human evaluation on 50 bugs completed. If we can't recruit 10 engineers, minimum viable is 3 evaluators × 30 bugs.
- Reproducibility package: scripts, configs, model versions, prompt versions.

**By 2026-10-01:**

- Full-paper draft finalized.
- arXiv preprint uploaded.
- Data + code links live (private or public — decide close to submission).
- Anonymization pass done (if FSE 2027 requires double-blind — check when CfP publishes).

## Graceful-degrade: empirical-only paper

If by 2026-09-15 the tool doesn't produce publishable-quality patches, we pivot the submission to:

**Backup title:** *An Empirical Characterization of Cross-Language Debugging Failure in Java+TypeScript and Python+Go Polyglot Systems*

**Structure:**
- Introduction: gap between single-lang and multi-lang benchmarks.
- Corpus: 145 mined repos + 100+ annotated bugs (Step 1.1–1.2).
- Taxonomy: 6-category classification with prevalence per language pair.
- Baseline analysis: iSWE-Agent (and possibly MASAI, SWE-agent) run on the corpus; failure-mode breakdown.
- Research agenda: what a cross-language agent needs, grounded in observed failure modes.

This paper is:
- Fully doable in 14 weeks even with tool setbacks.
- Independently valuable regardless of what happens with Steps 2–4.
- Still an FSE Research Papers-track submission (it makes an empirical contribution + a research agenda).

**Implication for how we work weeks 1–3:** Step 1 must be paper-quality on its own. Not a stepping stone to the tool — a standalone contribution.

## What survives from the earlier plan

- All research questions (RQ1–RQ4) exactly as written in `Polyglot_Debugging_Research_Progress_Report.md` §3.2.
- Central hypothesis unchanged.
- Selection criteria for repos and bugs unchanged.
- Bug taxonomy unchanged.
- Quality gates: schema validation, second-annotator κ, human patch evaluation.

## What was in the earlier plan and is now dropped

- Workshop paper submission as a separate deliverable. The outline in `steps/01-empirical-characterization/04-workshop-paper/outline.md` is now the skeleton for the FSE paper's §3 (Empirical Study).
- MSR intermediate paper. Dataset still gets a Zenodo DOI at FSE submission time.
- Sequential Phase A / Phase B / Phase C separation. Everything runs in parallel with a single deadline.

## Post-decision plan

- **If FSE accepts:** camera-ready, then extend to TOSEM/TSE journal with additional languages + cross-session memory.
- **If FSE rejects:** revise per reviews and re-submit to ICSE 2027 (usually next major deadline). The rejection reviews sharpen the paper.
- **If we invoked the backup narrative and FSE accepts it:** tool work (Steps 2–4) becomes a follow-up ICSE 2028 submission with the empirical paper's results as anchor.

## Venue-tracking checklist (do these in Week 1)

- [ ] Confirm FSE 2027 Research Papers CfP text (page limit, double-blind rules, artifact-badge process).
- [ ] Confirm submission system (HotCRP link).
- [ ] Confirm exact deadline timezone (usually AoE — anywhere on earth).
- [ ] Check if there is a Registered Reports track we should route through instead.
- [ ] Note the artifact-evaluation deadline (usually ~4 weeks after paper deadline) — plan reproducibility package accordingly.
