# Polyglot Codebase Debugging and Cross-Language Program Repair with LLMs and Agentic AI

**Progress Report & Research Direction**
**June 2026 | Targeting ICSE / FSE 2027**

---

## 1. What Is This Research?

### The Problem: Software Debugging Across Language Boundaries

Modern enterprise software is polyglot. A typical production system might run a Java Spring backend, a TypeScript/React frontend, Python microservices for ML, and Go services for performance-critical paths — all communicating over REST or gRPC. This is the norm, not the exception.

When a bug occurs, it rarely respects language boundaries. A malformed payload serialized by a Python service can corrupt data parsed by a Go consumer, which surfaces as a UI anomaly in TypeScript — with the Java layer somewhere in between. No existing debugging tool or AI agent can trace this chain.

> **Core Research Problem**
>
> LLM-based debugging agents have achieved ~70–80% resolution rates on Python-only benchmarks (SWE-bench Verified). However, when evaluated on realistic enterprise tasks — multi-language, multi-file, cross-boundary bugs — performance drops to 10–33%.
>
> This 40–60 percentage point gap is not an incremental engineering shortfall. It is a fundamental research problem: current agents lack the representations, tools, and architectures to reason across language boundaries.
>
> This research targets exactly that gap, with a focus on the two most commercially significant polyglot pairs: **Java + TypeScript** and **Python + Go**.

### Why Now? Why These Language Pairs?

- **Java + TypeScript** is the dominant enterprise web stack. Java backends (Spring Boot, Quarkus) fronted by TypeScript (React, Angular, Next.js) represent a massive proportion of commercial software. Bugs at the REST/JSON boundary are frequent and hard to attribute.
- **Python + Go** is the dominant ML/infrastructure stack. Python drives ML pipelines and data services; Go powers high-performance microservices and infrastructure tooling. gRPC/Protobuf is the common interface — but contract drift bugs across this boundary are entirely unaddressed in the literature.
- **Benchmark saturation on Python** — IBM's own researchers have flagged that Python SWE-bench scores (~80%) are likely contaminated. The community needs new, harder evaluation ground. Java + TS and Python + Go provide it.

---

## 2. Recent Research: What Has Been Done

### 2.1 Benchmarks: Measuring Multi-Language Capability

| Benchmark | Languages | Tasks | Key Feature | Relevance to Our Work |
|-----------|-----------|-------|-------------|------------------------|
| Multi-SWE-bench | Java, TS, JS, Go, Rust, C, C++ | 1,632 | Multi-lang issue resolution | Primary evaluation target — Java & TS subsets |
| SWE-PolyBench | Java, JS, TS, Python | 2,110 | Syntax-tree retrieval metrics | Java + TS directly — our core language pair |
| xCodeEval | 11+ languages | ~25M docs | Executable multilingual tasks | Go + Python coverage, APR track |
| SWE-bench Pro | Python, Go, TS, JS | 1,865 | Enterprise complexity, anti-contamination | Go-pair evaluation; measures real-world gap |
| Multi-SWE-bench Java (verified) | Java | 128 | Human-validated Java issues | iSWE-Agent baseline: 33.6% — our starting point |

#### SWE-PolyBench (AWS AI Labs, April 2025)

**Paper:** arXiv:2504.08703 | **Authors:** Muhammad Shihab Rashid et al., AWS AI Labs

- 2,110 repository-level, execution-based tasks across Java (165), JavaScript (1,017), TypeScript (729), and Python (199) — one of the few benchmarks to include TypeScript as a primary target.
- Introduces syntax-tree-based retrieval metrics (precision/recall on file and node identification) that go beyond simple pass/fail.
- **Key finding:** Agents performed best on Python (~24.1% pass rate) but struggled severely with TypeScript (~4.7%) — a nearly 5× performance gap. Java results were moderate. This directly motivates our work: TypeScript is the hardest existing target, and no paper has yet explained why.

> **Relevance to Our Research**
> SWE-PolyBench Java and TypeScript subsets will be our primary evaluation datasets. The 4.7% TypeScript baseline sets a low floor — there is significant room to improve, and the performance gap between Java and TypeScript is itself a research finding to explain and address.

#### xCodeEval (ACL 2024)

**Paper:** arXiv:2303.03004 | **Authors:** M.A.M. Khan, M.S. Bari et al. | **Venue:** ACL 2024

- The largest executable multilingual multitask benchmark: ~25 million examples, ~7,500 problems, 11+ languages, 7 tasks including program repair.
- Ships ExecEval — a unit-test execution engine supporting all languages including Go and Python, making it the only benchmark with executable Go repair evaluation.
- **Key finding:** LANTERN (2025) evaluated on xCodeEval and found a >24 percentage point Pass@10 gap between strong repair languages (Python ~89%) and weak ones (Rust ~65%, Go underserved). This is the quantitative motivation for the translate-to-repair approach.

> **Relevance to Our Research**
> xCodeEval is our evaluation platform for the Python + Go language pair. The Go program repair track gives us a baseline and the executable environment to validate patches. The Python–Go performance gap motivates RQ4 in our proposed research.

### 2.2 Agentic Issue Resolution

#### AutoCodeRover (NUS, ISSTA 2024)

**Paper:** arXiv:2404.05427 | **Authors:** Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, Abhik Roychoudhury | **Venue:** ISSTA 2024

- First agent to combine program structure analysis (AST, call graphs) with spectrum-based fault localization — rather than raw file search — to ground the LLM's search space before generating patches.
- Achieved ~16% on full SWE-bench and ~19–22% on SWE-bench-Lite at ~$0.43/issue — highly cost-efficient.
- **Architectural insight:** The key design lesson is that structured code navigation (AST-aware search) dramatically outperforms keyword/grep-based navigation. This principle transfers directly to polyglot debugging — but only if the AST tools span language boundaries.

> **Relevance to Our Research**
> AutoCodeRover establishes that AST-aware, structure-guided localization is the right approach. Our work extends this to the cross-language case: we need AST tools that can traverse a Java→TypeScript boundary at a REST API call site, which AutoCodeRover's single-language tools cannot do.

#### IBM iSWE-Agent for Java (IBM Research, December 2025)

**Source:** IBM Research Blog (Dec 8, 2025); Multi-SWE-bench submission README (Dec 1, 2025) | **Team:** Jatin Ganhotra (lead), Martin Hirzel, David Kung

- **State of the art on Java:** 33.59% resolved on Multi-SWE-bench Java (Claude 4.5 Sonnet); 31.25% with open models via inference scaling — both #1 and #2 on the leaderboard, beating Gemini 2.5 Pro (28.9%) and Claude 3.7 Sonnet (23.4%).
- **Architecture:** Two sequential agents — Localization agent + Editing agent. The Localization agent uses 7 custom Java AST tools built on tree-sitter and IBM's CodeLLM-DevKit (CLDK): `get_call_chain`, `get_class_info`, `get_file_info`, `get_function_callers`, `get_inheritance_hierarchy`, `get_method_info`, `get_symbol_info`. Bash access is restricted to prevent arbitrary exploration.
- **Editing agent:** Uses an enhanced diff/merge-conflict edit format supporting multi-file, multi-location patches. Validates via linting and compilation before finalizing — ensuring syntactically correct patches reach the verifier.
- **Open-model pipeline:** Inference scaling: same issue run multiple times; a fine-tuned Qwen-2.5-Coder-32B scorer ranks candidates; LLM-as-a-judge tournament selects the final patch.
- **Scientific motivation for Java:** IBM's Hirzel noted that Python SWE-bench is 'saturated' and frontier models are 'basically contaminated by seeing this benchmark data in training.' Java provides cleaner, less contaminated evaluation ground — a direct parallel to our polyglot motivation.

> **Relevance to Our Research**
> iSWE-Agent is the closest existing template for our work. Its separation of localization and editing agents, its read-only AST tools, its compilation-validated editing are all patterns we will adapt. The critical gap: its 7 AST tools are Java-only. When a bug crosses into TypeScript, `get_call_chain` stops at the Java boundary. Extending this architecture to cross-language is the core technical challenge we address.

### 2.3 Cross-Language Program Analysis Infrastructure

#### PyXray: Cross-Language Call Graph Construction (ICSE 2026)

**Venue:** ICSE 2026 Research Track

- Constructs cross-language call graphs between Python and native (C/C++) functions using dynamic analysis of Python object memory layouts — no test inputs required.
- Analyzed NumPy and PyTorch in minutes, significantly outperforming static methods for Python–native boundary crossing.
- **Key contribution:** Demonstrates that cross-language call graph construction is tractable for managed-to-native boundaries, and that object layout analysis is a viable signal for linking language-level abstractions across the boundary.

> **Relevance to Our Research**
> PyXray targets Python→C, not Python→Go. However, its core insight — that runtime object layout can bridge language abstractions — informs our approach for Python→Go boundary analysis via gRPC/Protobuf schema matching. PyXray is a direct methodological predecessor.

#### Towards Analyzing N-language Polyglot Programs (arXiv 2602.00303, 2026)

**Authors:** Jyoti Prakash, Abhishek Tiwari, Mikkel Baun Kjærgaard | University of Southern Denmark

- The most explicit statement of the N-language analysis open problem in the literature. Existing cross-language analyses handle exactly two languages; three or more languages introduce multi-hop dependencies, cyclic shared variables, and mutual fixed-point computation that no two-language model captures.
- Defines three communication models: different runtimes/FFI, common intermediate representation, and shared library interfaces. Identifies entry/middle/bottom language roles in a polyglot call chain.
- **Critical finding:** In a three-language system (e.g., Java backend + TypeScript frontend + native C library), a bug may propagate through two language boundaries before manifesting. The second boundary crossing is invisible to all current two-language analysis tools.

> **Relevance to Our Research**
> This paper is the strongest literature support for the novelty of our research direction. If we can cite this 2026 vision paper and show an empirical study demonstrating N-language bugs in Java+TypeScript systems (or Python+Go), that is already a publishable MSR/ICSE empirical track contribution — before any tool is built.

#### Schema/API Contract Bugs Across Language Boundaries

- **The unaddressed problem:** When a Java service and a TypeScript client communicate over REST (JSON schema) or gRPC (Protobuf), the 'bug' often lives in the contract itself — a field renamed on one side, a nullable type assumed non-null on the other, a serialization format mismatch. Neither side's code is 'wrong' in isolation.
- **Industry practice:** Contract testing (Pact-style) and gRPC schema validation tools handle static contract enforcement, but these are not integrated into LLM debugging agents. There is no agent that reads a `.proto` file, traces the generated Java and TypeScript bindings, and diagnoses a contract-drift bug.
- **Research gap status:** A search of ICSE, FSE, ASE, ISSTA proceedings confirms: zero published papers on LLM-based debugging or repair of REST/gRPC/Protobuf contract bugs across a Java+TypeScript or Python+Go boundary. This is a fully open problem.
- **Supporting evidence:** Cai et al.'s 400-bug study (FSE 2025) characterizes cross-language bugs in Python–C and Java–C systems; their taxonomy reveals that interface/contract mismatches are among the most common root causes. There is no equivalent study for REST-mediated or gRPC-mediated boundaries.

> **Why This Matters for Publication**
> Contract/schema bugs at REST and gRPC boundaries are a zero-prior-work area in the LLM debugging literature. An empirical characterization of these bugs — their prevalence, root cause taxonomy, and challenge for current agents — is a standalone ICSE/FSE empirical track contribution, independent of whether we build a full tool.

---

## 3. Proposed Research: Methodology & Direction

### 3.1 Research Vision

We propose to investigate, build, and evaluate the first LLM-based agentic debugging system designed for cross-language fault localization and repair in polyglot codebases — specifically targeting Java + TypeScript and Python + Go as the two highest-value enterprise language pairs.

The research is structured to produce publishable contributions at multiple stages: an early empirical/characterization paper suitable for a workshop or empirical track (MSR, ICSE), followed by a full systems+evaluation paper for ICSE 2027 or FSE 2027.

> **Central Claim (Hypothesis)**
>
> A cross-language agent architecture that (1) constructs a unified call graph spanning Java and TypeScript via SCIP-based code intelligence, (2) understands REST/gRPC schema contracts as first-class debugging context, and (3) applies iSWE-style structured localization before patch generation, will significantly outperform single-language baselines on cross-boundary bugs in Java+TypeScript and Python+Go systems.

### 3.2 Research Questions

| RQ | Research Question | Methodology | Target Venue Signal |
|----|-------------------|-------------|----------------------|
| **RQ1** | Can a localize-then-edit agent architecture (based on IBM iSWE) be adapted for Java+TypeScript cross-boundary fault localization? | Implement dual-agent system with SCIP-based cross-language call graph; ablate localization strategies on SWE-PolyBench Java+TS subset | ICSE / FSE: Empirical study + new tool |
| **RQ2** | Does a unified cross-language call graph (SCIP + tree-sitter) improve fault localization precision for boundary-crossing bugs vs. single-language graphs? | Build cross-language call graph for Java↔TS (REST/gRPC schemas); compare against single-language baselines on boundary-bug test suite | FSE / ISSTA: Program analysis + empirical |
| **RQ3** | What fraction of real enterprise Java+TypeScript bugs are boundary-crossing, and what are their root cause categories? | Empirical study: mine GitHub repos for Java+TS projects; manually classify 100–200 bugs; taxonomy of cross-language failure modes | ICSE / MSR: Empirical study — high novelty |
| **RQ4** | Does LANTERN-style translate-to-repair improve fix rates for Python+Go bugs vs. same-language repair? | Replicate LANTERN for Python→Go direction; evaluate on xCodeEval Go subset and custom Python↔Go boundary bugs | FSE / TOSEM: APR + evaluation |

### 3.3 Methodology

#### Step 1 — Empirical Characterization (Months 1–3)

Before building any tool, we establish the empirical ground truth. This produces the first publishable output.

1. **Mine GitHub for polyglot repositories:** Identify Java+TypeScript repositories (Spring Boot backend + React/Angular frontend in same repo or monorepo) and Python+Go repositories (data service + infrastructure service). Filter for ≥500 stars, ≥6 months maintenance, CI with tests.
2. **Extract and classify cross-language bugs:** From closed pull requests and linked issues, identify bugs that required changes to files in both languages. Manual classification by two annotators into root cause categories: (a) schema/contract mismatch, (b) type coercion error at boundary, (c) null/nil handling difference, (d) serialization format drift, (e) async/sync impedance mismatch, (f) other.
3. **Measure current agent performance:** Run iSWE-Agent, MASAI, and SWE-agent on the boundary-crossing bugs. Record resolution rate, where agents fail (which boundary crossing they miss), and token cost. This becomes the baseline to beat.
4. **Output:** Taxonomy paper — 'An Empirical Study of Cross-Language Bugs in Java+TypeScript and Python+Go Polyglot Systems' — targeting the MSR 2026 mining challenge track or an ICSE 2027 empirical track submission.

#### Step 2 — Cross-Language Call Graph & Schema Integration (Months 4–7)

The core technical contribution. We build the infrastructure that enables cross-language localization.

5. **Unified cross-language call graph:** Use Sourcegraph SCIP indexers (scip-java + scip-typescript for Java+TS; scip-python + Go indexer for Python+Go) to build a single unified symbol graph across both languages. Add edges for REST call sites: parse OpenAPI/Swagger annotations in Java (JAX-RS, Spring MVC) and TypeScript (fetch/axios calls) to connect HTTP client to HTTP server at the schema level.
6. **gRPC/Protobuf schema parser:** For Python+Go pairs, parse `.proto` files and link to generated bindings in both languages. When a field is renamed or a type changes in the schema, the parser identifies both the Java/Python server-side and the TypeScript/Go client-side symbols that are affected — this is the 'cross-language dependency edge' that current agents cannot see.
7. **Extend iSWE's 7 AST tools to TypeScript/Go:** Implement TypeScript equivalents of `get_call_chain`, `get_class_info`, `get_method_info` etc. using tree-sitter-typescript. For Go, use tree-sitter-go. Cross-language versions of `get_call_chain` will traverse the SCIP graph across language boundaries.
8. **Dataset annotation:** Annotate the mined bug corpus with cross-language dependency edges, ground-truth fault locations, and whether the bug was a single-language or multi-language root cause.

#### Step 3 — Dual-Agent Debugging System (Months 5–9)

Building on iSWE's architecture, we implement a cross-language localize-then-edit agent.

9. **Cross-Language Localization Agent:** Adapts iSWE's Localization agent with cross-language call graph tools. When a bug report references a Java stack trace, the agent can now follow call chains across the REST or gRPC boundary into TypeScript/Go, identifying that the root cause may be in the client-side type mapping or schema definition.
10. **Schema-Aware Hypothesis Generation:** If the Localization agent identifies a boundary-crossing dependency, a specialized Schema Reasoning module retrieves the relevant `.proto` or OpenAPI contract, identifies the mismatch between server-side and client-side interpretations, and generates fix hypotheses at the schema level, the server-side binding, and the client-side binding — potentially generating a three-file patch.
11. **Cross-Language Editing Agent:** Extends iSWE's Editing agent to handle multi-language patches. A Java patch and a TypeScript patch must be applied atomically, and both must pass compilation/linting validation in their respective runtimes before the patch is submitted.
12. **Execution Feedback Loop:** Run the full test suite across both languages after patching. Report per-language test failures back to the Localization agent for hypothesis revision. If only Java tests fail, the root cause is likely server-side; if only TypeScript fails, client-side; if both fail, a schema-level issue is likely.

#### Step 4 — Evaluation & Ablations (Months 9–12)

Rigorous evaluation is what makes this ICSE/FSE-worthy.

- **Primary benchmark:** SWE-PolyBench Java + TypeScript subsets. Resolution rate, token cost, time-to-resolution.
- **Secondary benchmark:** Multi-SWE-bench Java subset (compare against iSWE-Agent's 33.59% baseline).
- **Custom benchmark:** Our annotated cross-language bug corpus (Step 1). This is the only evaluation that specifically tests boundary-crossing bugs — the core novelty.
- **Ablation design (RQ1):** Single-language localization (no SCIP cross-language graph) vs. cross-language localization. If cross-language graph does not improve performance on single-language bugs but does improve on boundary bugs, this isolates the contribution.
- **Ablation design (RQ2):** Schema-aware hypothesis generation on/off. For schema/contract bugs specifically, does schema context improve resolution rate vs. code-only context?
- **Human evaluation:** 10 professional software engineers evaluate patch correctness, plausibility, and completeness on 50 cross-language bugs. This addresses the known limitation that test-passing patches are not always correct patches.

---

## 4. Publication Strategy

### 4.1 Target Venues

| Venue | Track / Type | Target Contribution |
|-------|--------------|----------------------|
| **ICSE 2027** | Full Research Paper | Full system paper: cross-language localize-then-edit agent, evaluation on SWE-PolyBench + custom benchmark |
| **FSE 2027** | Full Research Paper | Alternative/co-submission target: empirical study of cross-language bugs + tool evaluation |
| **MSR 2026/2027** | Mining Challenge / Data Paper | Bug taxonomy dataset paper — annotated corpus of Java+TS and Python+Go cross-language bugs with dependency edges |
| **ICSE / FSE Workshop 2026** | Short / Position Paper | Early vision paper: characterization of the polyglot debugging gap; research agenda for Java+TS and Python+Go agents |
| **TOSEM / TSE** | Journal Extension | Extended journal version with additional languages, broader evaluation, and cross-session memory results |

### 4.2 Publication Timeline

| Phase | Timeline | Activities | Output |
|-------|----------|------------|--------|
| **Phase 1** — Literature & Characterization | Months 1–3 | Survey cross-language bug literature (xLoc, Cai et al., MultiQL); mine Java+TS and Python+Go GitHub repos; build taxonomy of cross-language bug types; establish baseline on SWE-PolyBench | Bug taxonomy paper / workshop short paper (ICSE workshop or MSR) |
| **Phase 2** — Tool Development | Months 4–8 | Build cross-language SCIP-based call graph; implement dual-agent localizer-editor (iSWE-inspired, adapted for TS); integrate gRPC/REST schema parser; set up evaluation harness | Working prototype; dataset of annotated cross-language bugs |
| **Phase 3** — Evaluation & Ablations | Months 9–12 | Run ablation studies on SWE-PolyBench (Java+TS) and Multi-SWE-bench; cross-session memory experiments; schema/contract bug evaluation; human evaluation of patch quality | Full evaluation results; comparison vs. iSWE-Agent, MASAI baselines |
| **Phase 4** — Writeup & Submission | Months 13–15 | Write ICSE/FSE full paper; open-source tool and dataset; workshop paper → extend to journal (TOSEM/TSE) | ICSE 2027 or FSE 2027 submission; arXiv preprint |

---

## 5. What Makes This ICSE/FSE-Worthy

### 5.1 Novelty Argument

- **No published paper targets Java↔TypeScript or Python↔Go boundary-crossing bugs** in the LLM debugging/repair literature. Multi-SWE-bench, SWE-PolyBench, and xCodeEval test languages independently — this research is the first to treat the boundary as the primary object of study.
- **gRPC/REST contract bugs have zero prior LLM-agent coverage.** Pact-style contract testing exists industrially, but no agent integrates schema context into its localization and repair loop.
- **The empirical characterization (RQ3) is independently publishable** and currently missing from the literature. Cai et al.'s cross-language bug taxonomy covers C-mediated boundaries; there is no equivalent study for REST/gRPC-mediated boundaries.
- **The 'N-language Polyglot Programs' vision paper (2026) explicitly calls for exactly this work** and provides the theoretical framing. We are responding to that call with the first empirical and systems contribution.

### 5.2 Risk & Mitigation

| Risk | Likelihood | Mitigation |
|------|-----------|-------------|
| Few Java+TS repos have true cross-language bugs | Medium — monorepos are common but boundary bugs may be a small fraction | RQ3's empirical study answers this; even if proportion is low, contract bugs may be high-impact |
| IBM publishes iSWE-Agent arXiv paper before us | High — they said 'soon' in Dec 2025 | We cite them and differentiate: our work is cross-language extension, not Java-only; orthogonal contribution |
| SCIP cross-language navigation is insufficient for REST boundaries | Medium — REST is not a type-safe FFI | Schema parser (OpenAPI/Protobuf) provides the semantic bridge; we measure how much this helps vs. type-safe boundaries |
| Low absolute resolution rates make results hard to claim | Medium — cross-language bugs are harder; expect 10–25% | Frame as: 'improvement over single-language baseline on boundary bugs' rather than absolute rate; RQ1-style relative claims |

---

## 6. Immediate Next Steps

The following tasks can begin immediately, before any tool development, and each produces a standalone research output:

13. **GitHub mining setup (Week 1–2):** Write a script to query the GitHub API for Java+TypeScript monorepos (>500 stars, >6 months active) and Python+Go repos with microservice structure. Target: 50–100 repos per language pair for the empirical study.
14. **Bug annotation protocol (Week 2–3):** Define the annotation taxonomy for cross-language bugs based on Cai et al.'s existing taxonomy for C-mediated boundaries, extended to REST and gRPC boundaries. Produce an annotation guide for inter-rater reliability testing.
15. **Baseline agent evaluation (Week 3–6):** Run iSWE-Agent (or MSWE-agent as a proxy) on the SWE-PolyBench Java and TypeScript subsets. Document where failures occur — are TypeScript failures due to localization failure, patch generation failure, or test generation failure? This analysis is a section of the workshop paper.
16. **SCIP exploration (Week 4–6):** Set up scip-java and scip-typescript on 3–5 Java+TypeScript monorepos. Verify that cross-language symbol navigation works (can we go from a Java REST endpoint definition to the TypeScript fetch call that consumes it?). Document gaps — this is foundational for tool design.
17. **Workshop paper outline (Week 6–8):** Draft a 4-page short paper: 'Towards Cross-Language Debugging Agents for Java+TypeScript Polyglot Systems — A Characterization and Research Agenda.' Target: ICSE 2027 NIER (New Ideas and Emerging Results) track or a co-located workshop.

---

*Prepared June 2026 | Research Progress Report | Targeting ICSE / FSE 2027*
