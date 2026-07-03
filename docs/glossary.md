# Glossary

Terms and tools referenced throughout this project. Definitions are scoped to *how we use them*, not their full general meaning. If you find yourself uncertain about a term while working on a sub-step, look here first.

## Benchmarks

**SWE-bench / SWE-bench Verified.** Original Python-only benchmark of GitHub issues + patches. "Verified" subset is human-validated. Saturated; per IBM (Dec 2025) likely contaminated.

**Multi-SWE-bench.** Java + TS + JS + Go + Rust + C + C++ extension. 1,632 tasks. Has a human-verified Java subset of 128 tasks where iSWE-Agent currently leads at 33.59%.

**SWE-PolyBench (AWS, arXiv:2504.08703).** 2,110 tasks across Java (165), JS (1,017), TS (729), Python (199). Introduces AST-based retrieval precision/recall metrics. **Our primary eval set for Java+TS.** Best published TS pass rate is ~4.7%.

**SWE-bench Pro.** Enterprise complexity + anti-contamination. Includes Python, Go, TS, JS. 1,865 tasks.

**xCodeEval (ACL 2024, arXiv:2303.03004).** ~25M examples, 11+ languages, ships ExecEval test runner. Only benchmark with executable Go program repair. **Our primary eval set for Python+Go.**

## Agents and systems

**iSWE-Agent (IBM Research, Dec 2025).** Two-agent localize-then-edit system. Uses 7 Java-only AST tools from IBM's CodeLLM-DevKit (CLDK): `get_call_chain`, `get_class_info`, `get_file_info`, `get_function_callers`, `get_inheritance_hierarchy`, `get_method_info`, `get_symbol_info`. **The architectural template we're extending to cross-language.**

**MASAI.** Multi-agent SWE-bench solver. Differentiates from iSWE by using more sub-agents (planner, retriever, editor, etc.). Will be a baseline.

**SWE-agent.** Princeton's earlier agent — single-agent with a structured terminal interface (ACI). Earlier baseline.

**AutoCodeRover (NUS, ISSTA 2024, arXiv:2404.05427).** First to combine AST + spectrum-based fault localization with LLM. ~$0.43/issue. Established that *structured navigation beats grep-based search* — a principle we transfer to polyglot.

**LANTERN (2025).** Translate-to-repair: translate a bug to a language the LLM repairs better, fix it there, translate back. Showed >24pp Pass@10 gap between Python (~89%) and weaker repair languages on xCodeEval. **Inspires RQ4 (Python↔Go direction).**

## Code-analysis infrastructure

**SCIP (Sourcegraph Code Intelligence Protocol).** Language-agnostic symbol-graph format. Indexers exist for Java (`scip-java`), TypeScript (`scip-typescript`), Python (`scip-python`), Go (community-maintained). **Foundation of our cross-language call graph.**

**tree-sitter.** Incremental parser generator producing concrete syntax trees. We use `tree-sitter-typescript`, `tree-sitter-go` to build the TS/Go equivalents of iSWE's Java AST tools.

**CLDK (CodeLLM-DevKit).** IBM's Python library wrapping tree-sitter + Java analyzers. Provides the 7 AST tools iSWE-Agent uses. Java-only.

**PyXray (ICSE 2026).** Builds Python→C cross-language call graphs from runtime object layouts. Methodological predecessor for our gRPC/Protobuf-mediated graphs.

## Boundary technologies

**REST / OpenAPI / Swagger.** HTTP-based contract. Schema is JSON-Schema-flavored. Java side uses JAX-RS / Spring annotations (`@GetMapping`, etc.); TS side uses `fetch` / `axios`. Schema is not type-safe at the wire.

**gRPC / Protobuf.** Binary RPC contract defined in `.proto` files. Code generators produce typed bindings in both languages. Contract drift = `.proto` changes without re-generating bindings.

**Pact.** Industry-standard contract testing for REST. Static; not integrated into LLM agents — gap we discuss in §2.3 of the plan.

## Bug-taxonomy categories (§3.3 Step 1.2)

When annotating bugs, every cross-language bug gets one primary category:

| Code | Category | Example |
|------|----------|---------|
| `schema` | Schema / contract mismatch | TS expects `userId: string`, Java sends `userId: number` |
| `coerce` | Type-coercion error at boundary | Java `BigDecimal` → JSON → TS `number` losing precision |
| `nil` | Null / nil / undefined handling | Go zero-value vs Python `None` ambiguity |
| `serde` | Serialization format drift | Java `LocalDateTime` ISO format vs JS Date constructor |
| `async` | Async / sync impedance | TS Promise unawaited where Java expected synchronous |
| `other` | Doesn't fit above | Note rationale in annotation |

Document any new category you propose in `steps/01-empirical-characterization/02-bug-extraction/taxonomy.md` before using it.

## Publication venues

**ICSE / FSE.** Top SE conferences. Target full-paper venues for Phase C.

**ISSTA.** Testing/analysis-focused. Strong fit for the program-analysis contribution if we lead with the call graph.

**MSR (Mining Software Repositories).** Strong fit for Phase B empirical paper.

**TOSEM / TSE.** Journals; Phase D extension target.

**NIER (New Ideas and Emerging Results).** ICSE short-paper track. Phase A target.

## Adding to this glossary

If you encounter a term that took >2 minutes to look up, add it here. Keep entries 1–3 sentences. Don't paste paper abstracts.
