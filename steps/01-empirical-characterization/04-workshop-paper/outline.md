# FSE Paper §3 Empirical Study — Outline

> **Scope change 2026-06-27:** originally a standalone workshop paper outline. Now the outline for §3 of the FSE 2027 Research Paper.

**Full paper working title:** *Cross-Language Localize-then-Edit: An Agentic Debugging System for Java+TypeScript and Python+Go Polyglot Codebases.*

**Target venue:** FSE 2027 Research Papers track.
**Deadline:** 2026-10-02.
**Section budget:** ~4 pages of ~22 total.

---

## §3.1 Corpus Construction (~0.75 page)

- Repo-mining methodology in one paragraph. Refer to reproducibility package for full detail.
- **Figure or table:** repo counts + median stars + license distribution per language pair.
- One line on the two filter calibrations logged during 1.1 (test-marker informational; python-go language fraction 2%) — these are *methodology decisions*, worth reporting for transparency.

## §3.2 Bug Extraction & Annotation (~0.5 page)

- PR filtering pipeline (both-language touch + bug-keyword heuristics).
- Manual annotation protocol.
- Inter-rater agreement statement — solo for first draft, κ on 30-bug subset once second annotator is available.
- Total bugs annotated per language pair.

## §3.3 Bug Taxonomy (~1 page)

- 6 categories with one-sentence definitions:
  - `schema` — schema/contract mismatch
  - `coerce` — type-coercion error at boundary
  - `nil` — null/nil/undefined handling difference
  - `serde` — serialization format drift
  - `async` — async/sync impedance mismatch
  - `other` — with mandatory rationale
- **Figure 1:** stacked-bar count per category × language pair.
- One representative example bug per category — 3–4 lines of prose each, anonymized if double-blind.

## §3.4 Baseline Agent Performance (~1 page)

- Which agent(s) were run, on what subset, with what LLM.
- Headline number: resolution rate on cross-language subset vs the agent's published single-language number.
- **Figure 2:** bar chart showing this gap.
- Cost per bug + wall time — reviewers will ask.

## §3.5 Failure-Mode Analysis (~0.75 page — THE HEADLINE)

- **Table 1:** counts per failure mode (localization / cross-language-blind / patch-quality / test-execution / other).
- 2–3 case-study bugs demonstrating "cross-language-blind" — where the agent finds files in one language but never crosses the REST/gRPC boundary. **These are the paper's smoking gun.**
- Brief prose: what specifically stops current single-language AST tools at the boundary.
- Transitions to §4 (our cross-language call graph) — "this failure mode motivates the graph structure we present next."

---

## References anchored in this section

- Multi-SWE-bench, SWE-PolyBench, xCodeEval, SWE-bench Pro
- iSWE-Agent (IBM blog + Multi-SWE-bench README), MASAI, SWE-agent
- Cai et al. FSE 2025 cross-language bug study
- PyXray ICSE 2026, N-language Polyglot Programs vision paper (2026)

---

## Non-obvious writing notes

- **Frame the corpus-imbalance as a finding, not a limitation.** Python+Go monorepos are rare — this is itself worth reporting.
- **The React Native sub-population** (Android JNI bridge, not REST) should either be excluded from the primary corpus or reported as a separate category. Decide when 1.2 is halfway done, based on how many RN bugs we're seeing.
- **Don't lead with the tool.** §3 is empirical only. The tool starts in §4.
- **Every number appears in `output/key-numbers.md`.** No exceptions.

---

## What this outline is NOT

- Not the full FSE paper — this is §3 only. §1, §2, §8, §9 are written by the Week-12 sprint. §4–§7 are owned by Steps 2–4.
- Not the workshop paper it was originally drafted as. That deliverable is dropped per [ROADMAP.md](../../../ROADMAP.md).
