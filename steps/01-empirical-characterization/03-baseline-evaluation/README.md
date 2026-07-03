# Sub-step 1.3 — Baseline Agent Evaluation

**Maps to:** §3.3 Step 1.3 + §6 item 15 of the [research plan](../../../Polyglot_Debugging_Research_Progress_Report.md).
**Goal:** Run current SOTA LLM debugging agents on our annotated cross-language bugs. Establish the baseline that Phase C must beat, and the failure-mode breakdown that motivates the workshop paper.

## Which agents

In priority order:

1. **iSWE-Agent (IBM).** Closest architectural match to what we're building. Java-only AST tools — so we know it will fail or degrade on cross-language bugs. That failure mode IS the result.
2. **MASAI.** Multi-agent SWE solver. Different architecture; tests whether failure is architectural or just tool-coverage.
3. **SWE-agent (Princeton).** Earlier baseline; structured-terminal style. Useful as a "even older approach" comparison.

For the workshop paper, **one agent is enough** if it gives us a clean failure-mode story. For the empirical paper (Phase B), we want all three.

## Inputs

- `../02-bug-extraction/data/processed/bugs.jsonl` — annotated bug corpus.
- Selected baseline agent(s) — clone separately, do NOT vendor into this repo.
- Local clones of the source repos (each agent typically needs a working copy of the buggy code).
- Compute budget — confirm with user before any full sweep.

## Outputs

- **`output/results.jsonl`** — one record per (agent, bug) attempt with resolution status, patch diff, token cost, wall time.
- **`output/failure-modes.md`** — qualitative breakdown: where did the agents fail?
   - localization failure (couldn't find the bug),
   - patch generation failure (located but produced wrong fix),
   - test-execution failure (couldn't even run the tests),
   - boundary-blind failure (specifically failed because the bug crossed languages).
- **`configs/runs/<agent>-<date>.yaml`** — exact config used for each run (for reproducibility).

## Cost discipline

Running iSWE-Agent / MASAI on real bugs is expensive. Before any sweep:

- **Cost-per-bug estimate.** Token usage × model price × expected retries. Multiply by 1.5 for safety.
- **Smoke test first.** Run on 2–3 bugs to validate the harness end-to-end before scaling.
- **Cap per-bug spend.** Set a hard timeout / token cap so a runaway loop doesn't blow the budget.

User must approve the full sweep cost before it runs.

## Pitfalls

- **Test-passing ≠ correct.** An agent's patch might pass the tests but be wrong (over-broad, deletes the test, etc.). For ≥30% of "resolved" bugs, do human spot-checks for the failure-modes write-up.
- **Repo-state mismatch.** Agents need a specific commit (parent of the fix). Be careful with checkouts.
- **Flaky tests.** Some repos have flaky CI. Run each bug 2–3× and report median + variance.

See [CLAUDE.md](CLAUDE.md) for the run protocol and [STATUS.md](STATUS.md).
