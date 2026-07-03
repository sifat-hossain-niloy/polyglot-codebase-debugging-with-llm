# Step 4 — Evaluation & Ablations (placeholder)

**Maps to:** §3.3 Step 4 of the [research plan](../../Polyglot_Debugging_Research_Progress_Report.md).
**Timeline:** Months 9–12.
**Status:** 🔴 Blocked on Step 3 — do not start until the dual-agent system from Step 3 runs end-to-end.

## What this step will contain (preview)

The rigorous evaluation that makes the Phase C paper ICSE/FSE-worthy. Likely sub-steps:

1. **Primary benchmark — SWE-PolyBench.** Java + TS subsets. Resolution rate, token cost, time-to-resolution vs. baselines.
2. **Secondary benchmark — Multi-SWE-bench Java.** Compare against iSWE-Agent's 33.59% baseline directly.
3. **Custom benchmark — our cross-language corpus.** This is the only benchmark that specifically tests boundary-crossing bugs — the core novelty.
4. **Ablation (RQ1).** Single-language localization vs. cross-language localization. Isolate the contribution of the unified graph.
5. **Ablation (RQ2).** Schema-aware hypothesis generation on/off. Specifically for schema/contract bugs.
6. **RQ4 — LANTERN-style translate-to-repair for Python→Go.** Replicate the LANTERN approach in the Python+Go direction and measure.
7. **Human evaluation.** 10 professional engineers evaluate patch correctness, plausibility, completeness on 50 cross-language bugs. Addresses the test-passing ≠ correct concern.

## Inputs (when this step starts)

- Step 3's agent system, runnable on a corpus.
- All three baseline agents from Step 1.3 already runnable.
- The Step 1 corpus + SWE-PolyBench + Multi-SWE-bench Java.

## Outputs

- Full results tables and figures for the Phase C paper.
- Ablation analysis.
- Human-eval results with inter-rater agreement.
- Open data + open code release artifacts.

## Scaffold this step when…

…Step 3 has working end-to-end results AND we're entering the Phase C writeup window.
