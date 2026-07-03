# Roadmap

Chunk-by-chunk delivery plan. Each phase produces an independently publishable output so that we accumulate publication credit incrementally rather than betting everything on a single 12-month conference submission.

---

## Phase A — Workshop Paper + Dataset (Months 1–3)

**Source of work:** [Step 1 — Empirical Characterization](steps/01-empirical-characterization/README.md). Maps to §3.3 Step 1 and §6 of the [research plan](Polyglot_Debugging_Research_Progress_Report.md).

**Target venue:** ICSE 2027 NIER (New Ideas and Emerging Results), or co-located workshop (e.g., InteNSE, AIware, LLM4Code).

**Paper title (working):** *Towards Cross-Language Debugging Agents for Java+TypeScript Polyglot Systems — A Characterization and Research Agenda.*

**Deliverables:**
- 4-page short paper.
- Annotated dataset of 100–200 cross-language bugs from Java+TypeScript and Python+Go repositories, released on Zenodo with DOI.
- Baseline numbers: iSWE-Agent, MASAI, or SWE-agent run on a TypeScript subset, with failure-mode breakdown.

**Exit criteria:**
- 50–100 candidate repos mined per language pair.
- ≥100 bugs annotated with inter-rater agreement reported (Cohen's κ).
- One baseline agent runs end-to-end on ≥20 cross-language bugs.
- Short paper drafted and reviewed internally.

---

## Phase B — Empirical Paper (Months 3–6, partially overlaps with A)

**Source of work:** Extends Phase A's dataset and analysis. Maps to §3.2 RQ3.

**Target venue:** MSR 2027 (Mining Challenge or Data Showcase), or ICSE 2027 empirical track.

**Paper title (working):** *An Empirical Study of Cross-Language Bugs in Java+TypeScript and Python+Go Polyglot Systems.*

**Deliverables:**
- Expanded dataset (200–400 bugs).
- Full taxonomy with prevalence numbers per category.
- Comparison: iSWE-Agent vs. MASAI vs. SWE-agent on the cross-language subset.
- Discussion: which boundary-crossing failure modes most defeat current agents.

**Exit criteria:**
- All 6 taxonomy categories (§3.3 Step 1.2) populated with ≥15 examples each.
- Statistical analysis: do certain bug categories correlate with specific agent-failure modes?
- Full paper submitted.

---

## Phase C — Conference Paper (Months 6–15)

**Source of work:** [Step 2](steps/02-call-graph-schema/), [Step 3](steps/03-dual-agent-system/), [Step 4](steps/04-evaluation-ablations/). Maps to §3.3 Steps 2–4 and §3.2 RQ1, RQ2, RQ4.

**Target venue:** ICSE 2027 or FSE 2027 (full research paper).

**Paper title (working):** *Cross-Language Localize-then-Edit: An Agentic Debugging System for Java+TypeScript and Python+Go Polyglot Codebases.*

**Deliverables:**
- Unified cross-language call graph (SCIP + tree-sitter + REST/gRPC schema edges).
- Dual-agent system (cross-language localizer + cross-language editor).
- Evaluation on SWE-PolyBench (Java+TS subsets), Multi-SWE-bench Java (vs. iSWE-Agent baseline), and our Phase A/B dataset.
- Ablations isolating contribution of (a) cross-language graph and (b) schema-aware hypothesis generation.
- Human evaluation of patch quality on 50 bugs.

**Exit criteria:**
- Beats single-language baselines on cross-boundary bugs (RQ1).
- Cross-language graph improves localization precision (RQ2).
- LANTERN-style translate-to-repair shows measurable improvement for Python+Go (RQ4).
- Submission with code + data release on arXiv.

---

## Phase D — Journal Extension (Post-conference)

**Target venue:** TOSEM or TSE.

**Additions over conference paper:**
- Additional language pairs (e.g., add Rust↔Python or extend to a third language for N-language analysis).
- Cross-session memory experiments (does agent memory across bugs in the same repo help?).
- Broader evaluation: more repos, more bugs, more agents compared.

---

## Decision points

These trigger re-planning:

- **If IBM releases iSWE-Agent's arXiv paper before Phase A submission:** still submit; differentiate on cross-language extension (per §5.2 of the plan).
- **If <50 boundary-crossing bugs exist in mined repos:** pivot Phase A to focus on contract/schema bugs (which are zero-prior-work per §2.3) and broaden the repo pool.
- **If SCIP cross-language navigation fails for REST boundaries:** schema parser becomes the primary contribution in Phase C; cite this as a finding in Phase A.

Add new decision points to this file as they arise — keep this living.

---

## How phases compose into sessions

Each Claude session works on **exactly one sub-step at a time** (e.g., `steps/01-empirical-characterization/01-github-mining/`). The sub-step's `STATUS.md` is the resume point. Phases A–D are publication milestones, not session boundaries.
