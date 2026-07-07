# Roadmap

**Primary target: FSE 2027 Research Papers track. Submission deadline: 2026-10-02.**

Today's date: 2026-06-27. **14 weeks to submission.**

The previous phased workshop→conference plan (workshop paper first, then empirical, then full paper) is superseded. We compress everything into a single FSE 2027 submission and treat the workshop-paper outline as an internal milestone that folds into the FSE paper's Empirical Study section.

---

## Compressed 14-week schedule

| Window | Dates | Work | Exit criteria |
|--------|-------|------|---------------|
| **Weeks 1–3** | Jul 1 – Jul 21 | Finish [Step 1](steps/01-empirical-characterization/README.md): bug extraction + annotation + first baseline agent run | ≥100 annotated cross-language bugs; at least one baseline agent run on ≥20 bugs with failure-mode breakdown |
| **Weeks 4–6** | Jul 22 – Aug 11 | [Step 2](steps/02-call-graph-schema/README.md): unified cross-language call graph (SCIP + tree-sitter) + REST/gRPC schema parser | Cross-language `get_call_chain` traverses a Java→TS boundary on ≥5 curated bug traces |
| **Weeks 7–9** | Aug 12 – Sep 1 | [Step 3](steps/03-dual-agent-system/README.md): dual-agent system (cross-language localizer + cross-language editor) | End-to-end run on the corpus; per-bug results captured |
| **Weeks 10–11** | Sep 2 – Sep 15 | [Step 4](steps/04-evaluation-ablations/README.md): full evaluation on SWE-PolyBench + our corpus, ablations, human eval on 50 patches | RQ1–RQ4 answered with tables + figures |
| **Weeks 12–13** | Sep 16 – Sep 29 | Paper writing sprint | Full-paper draft complete, internal review done |
| **Week 14** | Sep 30 – Oct 2 | Polish, arXiv preprint, submit | Submitted |

---

## Backup narrative (graceful degrade)

If Steps 2–3 aren't strong enough by 2026-09-15, submit an **empirical + baseline-analysis paper** instead:

- Step 1 evidence only: corpus, taxonomy, prevalence, baseline-agent failure modes.
- Positioned as: "first empirical characterization of cross-language debugging failure at REST/gRPC boundaries."
- No new tool, but the taxonomy + failure-mode analysis is standalone-publishable.
- Same FSE deadline; different narrative.

This is not a fallback plan we'd like to invoke — it's a truthful commitment: **Step 1 must be paper-quality on its own** so it survives if Steps 2–3 slip. That constrains how we prioritize weeks 1–3.

---

## Post-FSE (if accepted or rejected)

- **If accepted:** camera-ready + journal extension (TOSEM / TSE) with additional languages and cross-session memory experiments.
- **If rejected:** revise per reviews, re-submit to ICSE 2027 (usually 6–8 months later) with additional evaluation added.
- **If we hit the empirical-only backup narrative:** the tool work (Steps 2–3) becomes a follow-up ICSE 2028 submission.

---

## Decision points (add as they arise)

- **2026-07-14 (end of Week 2):** Have we hit 50+ annotated bugs? If <30, tighten annotation pace or narrow scope to Java+TS only.
- **2026-08-04 (end of Week 5):** Cross-language SCIP navigation working on real bugs? If not, pivot Step 2 to schema-parser-only (weaker but still novel).
- **2026-09-01 (end of Week 9):** Is the agent producing patches? If it can only localize, submit the localization-only story + failure analysis.
- **2026-09-15 (end of Week 11):** Are the evaluation numbers strong enough to lead with the tool? If not, invoke the backup narrative — reframe as empirical + baseline paper.

---

## How this changes the day-to-day

- **Weekly `STATUS.md` refresh** — every Friday, update at the step level so slippage is visible.
- **No exploratory tangents** — every experiment must be justified by an RQ or a paper section.
- **Parallel paper drafting from Week 1** — the writing doesn't wait for weeks 12–13. Empirical Study section fills in as 1.2 lands; Background section is already writable.
- **Cost-approval gate for baseline agents (§ Step 1.3)** — request user approval on total budget by end of Week 2.

---

## What's dropped from the previous plan

- Workshop paper as a standalone submission. Its outline (`steps/01-empirical-characterization/04-workshop-paper/outline.md`) is reused as the skeleton for the FSE paper's §3 Empirical Study.
- MSR mining-track intermediate paper. Dataset still gets a Zenodo DOI on FSE submission, but it isn't a separate paper artifact.
- Phase B / Phase D as intermediate publication milestones. Journal extension only becomes real after FSE 2027 decision.

## What survives from the previous plan

- All research questions (RQ1–RQ4).
- All step outputs and artifacts (bug corpus, taxonomy, call graph, dual-agent system, evaluations).
- All quality gates (schema validation, second-annotator κ, human evaluation of patches).
- The multi-session repo structure — even more important under time pressure.
