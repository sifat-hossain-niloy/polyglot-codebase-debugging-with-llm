# Step 2 — Cross-Language Call Graph & Schema Integration (placeholder)

**Maps to:** §3.3 Step 2 of the [research plan](../../Polyglot_Debugging_Research_Progress_Report.md).
**Timeline (compressed for FSE 2027):** Weeks 4–6 of the 14-week schedule → **2026-07-22 to 2026-08-11**.
**Status:** 🔴 Blocked on Step 1 — do not start until Step 1's annotated bug corpus exists.

> **Scope note under time pressure:** the full research plan calls for both Java+TS and Python+Go cross-language graphs. Given the FSE 2027 deadline (2026-10-02), prioritize **Java+TS end-to-end** first. Python+Go graph is stretch — feasible if Java+TS lands cleanly in Week 4–5.

## What this step will contain (preview)

The core technical contribution: a unified symbol graph that spans Java↔TS (REST / OpenAPI mediated) and Python↔Go (gRPC / Protobuf mediated). Sub-steps will likely be:

1. **SCIP setup.** Install and run `scip-java`, `scip-typescript`, `scip-python`, and a Go indexer on representative repos. Verify symbol navigation.
2. **REST edge construction.** Parse Java JAX-RS / Spring MVC annotations and TS `fetch` / `axios` calls. Connect endpoints to consumers.
3. **gRPC / Protobuf edge construction.** Parse `.proto` files. Link to generated bindings on both sides.
4. **Tree-sitter tools for TS / Go.** Implement TS and Go equivalents of iSWE's 7 Java AST tools (`get_call_chain`, etc.).
5. **Cross-language navigation tests.** Validate the unified graph against curated bugs from Step 1.

## Inputs (when this step starts)

- `steps/01-empirical-characterization/01-github-mining/data/processed/repos.jsonl` — repos to index.
- `steps/01-empirical-characterization/02-bug-extraction/data/processed/bugs.jsonl` — bugs whose cross-language edges we expect the graph to model.

## Outputs

- Cross-language call graph artifact (SCIP-compatible export + schema-edge overlay).
- Library of TS/Go AST tools (`get_call_chain`, `get_class_info`, etc.).
- Validation report: which bug-corpus edges the graph correctly models.

## Scaffold this step when…

…Step 1's STATUS goes 🟢 across all sub-steps AND the user signals "ready to start Step 2." At that point, expand this placeholder into full sub-step structure mirroring Step 1's layout (`01-scip-setup/`, `02-rest-edges/`, `03-grpc-edges/`, `04-ts-go-ast-tools/`, `05-validation/`).
