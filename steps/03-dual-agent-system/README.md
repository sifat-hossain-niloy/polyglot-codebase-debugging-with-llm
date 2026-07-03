# Step 3 — Dual-Agent Debugging System (placeholder)

**Maps to:** §3.3 Step 3 of the [research plan](../../Polyglot_Debugging_Research_Progress_Report.md).
**Timeline:** Months 5–9.
**Status:** 🔴 Blocked on Step 2 — do not start until the cross-language call graph from Step 2 is available.

## What this step will contain (preview)

The agent system that consumes the cross-language graph from Step 2. Likely sub-steps:

1. **Cross-language Localization agent.** Extends iSWE's Localization agent with the Step 2 graph tools. When a Java stack trace points into a REST handler, the agent follows the call chain across the boundary into the TypeScript consumer.
2. **Schema-aware hypothesis generation.** A specialized module that, on detecting a boundary-crossing dependency, retrieves the relevant `.proto` / OpenAPI contract, identifies the server-vs-client mismatch, and generates fix hypotheses at three levels (schema, server binding, client binding).
3. **Cross-language Editing agent.** Extends iSWE's editor to apply multi-language patches atomically with compilation + linting validation on both sides.
4. **Execution feedback loop.** Run tests on both sides; route per-language failures back to the Localization agent for hypothesis revision.
5. **End-to-end harness.** Plug into Step 1's annotated bug corpus for evaluation.

## Inputs (when this step starts)

- Cross-language graph from Step 2.
- Bug corpus from Step 1.
- LLM API access (TBD on which model — set during Step 1.3 baseline work).

## Outputs

- The cross-language agent (open-sourceable).
- Resolution results on Step 1's corpus.
- Trajectory logs for analysis and ablation.

## Scaffold this step when…

…Step 2 produces a usable cross-language graph for at least one bug AND the user signals "ready to start Step 3."
