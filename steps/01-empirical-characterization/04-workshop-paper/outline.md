# Paper Outline — Workshop Short Paper

**Working title:** *Towards Cross-Language Debugging Agents for Java+TypeScript Polyglot Systems — A Characterization and Research Agenda*

**Target venue:** ICSE 2027 NIER (preferred) or co-located workshop (AIware, InteNSE, LLM4Code).

**Format:** 4 pages + references (verify exact rules per venue at draft-finalization time).

---

## 1. Introduction (~0.75 page)

**Opening:** Modern enterprise software is polyglot. A typical production system runs a Java backend, a TypeScript frontend, Python microservices, and Go infrastructure — all communicating over REST or gRPC.

**Gap:** LLM debugging agents achieve ~70–80% on Python-only SWE-bench but drop to 10–33% on multi-language benchmarks. No prior work has measured agent performance specifically on bugs that *require* cross-language reasoning.

**Contribution (3 bullets):**
- The first annotated corpus of cross-language bugs in Java+TS and Python+Go systems.
- An empirical taxonomy of failure modes when current SOTA agents are run on these bugs.
- A research agenda for cross-language agent architectures grounded in the empirical findings.

**Roadmap of the paper.**

---

## 2. Background & Motivation (~0.5 page)

**Existing benchmarks treat languages independently.** Brief tour:
- Multi-SWE-bench, SWE-PolyBench, xCodeEval, SWE-bench Pro.
- All score per-language. None isolate boundary-crossing bugs.

**Existing agents are single-language.** iSWE-Agent's 7 AST tools, AutoCodeRover's spectrum-based localization, MASAI's multi-agent design — all assume the bug lives in one language.

**The gap is structural, not incremental.** Cite the 2026 "N-language Polyglot Programs" vision paper as theoretical framing.

---

## 3. Empirical Study (~1.5 pages — the heart of the paper)

### 3.1 Corpus

- Mining methodology (one paragraph + reference to release).
- Repo count per language pair, selection criteria, total bugs annotated.
- One-line statement on annotation reliability.

### 3.2 Taxonomy

- 6 categories with one-sentence definition each.
- **Figure 1:** Bug-count distribution per category, per language pair.
- One representative example per category — short, anonymized if needed.

### 3.3 Baseline Agent Performance

- Which agent was run, on what subset, with what LLM and config.
- Headline number: resolution rate on cross-language subset vs. that agent's published single-language number.
- **Figure 2:** Bar chart of these numbers.

### 3.4 Failure Modes

- **Table 1:** Per failure-mode counts (localization, cross-language-blind, patch-quality, test-execution, other).
- 2–3 case studies of cross-language-blind failures — these are the paper's headline finding.
- Brief discussion: where existing AST tools stop, and why.

---

## 4. Research Agenda (~0.75 page)

Translate the failure modes into design requirements:

- **Unified cross-language call graph.** A localization tool must follow call chains across REST and gRPC boundaries.
- **Schema-aware reasoning.** Contracts (`.proto`, OpenAPI) are first-class debugging context, not just metadata.
- **Multi-language patch validation.** Patches must compile and pass tests on both sides of the boundary atomically.
- **Failure-aware routing.** When localization confidence is low at a boundary, generate hypotheses that span both languages.

Each bullet maps to a planned contribution in the full system (Phase C).

---

## 5. Threats to Validity (~0.25 page)

- **Mining bias.** ≥500-star, English-language repos over-represent certain ecosystems.
- **Annotator subjectivity.** Categories overlap on boundary cases; describe how we resolved them.
- **Single-annotator κ.** Note if a secondary annotator was unavailable for the workshop draft; commit to it for Phase B.
- **Agent / model version drift.** The baseline numbers are tied to specific commits + LLM versions.
- **Selection of one agent.** A second agent (Phase B) is needed to claim findings generalize.

---

## 6. Conclusion & Future Work (~0.25 page)

- One-sentence summary of the gap and our contribution.
- Pointer to (a) the dataset release and (b) the planned tool work for the full paper.

---

## References

Target: 20–30 references including:
- Multi-SWE-bench, SWE-PolyBench, xCodeEval, SWE-bench Pro
- iSWE-Agent (IBM blog + README), AutoCodeRover, MASAI, SWE-agent
- LANTERN
- PyXray, N-language Polyglot Programs vision paper
- Cai et al. cross-language bug study (FSE 2025)
- SCIP / Sourcegraph code intelligence references
- Pact / contract-testing reference

---

## Notes for the writer

- This is an **outline**, not the paper. Don't paste section bodies here. Write them in `sections/*.md` as data accumulates.
- If a section's planned content disappears (e.g., we never get a baseline run done in time), shrink the outline and re-allocate pages — don't write filler.
- The headline contribution is the **gap + failure-mode breakdown**. Everything else supports those two paragraphs.
