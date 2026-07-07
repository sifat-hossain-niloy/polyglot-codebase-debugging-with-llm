# Agent Instructions — Sub-step 1.3 (Baseline Agent Evaluation)

> **Deadline pressure (FSE 2027, 2026-10-02):** this sub-step must complete by 2026-07-21 (end of Week 3) so the FSE paper's §3 has a baseline number to lead with. That's ~2 weeks after 1.2 kicks off.

## Prerequisite

`../02-bug-extraction/data/processed/bugs.jsonl` must exist with at least 20 annotated bugs. If it doesn't, go finish 1.2 first.

## Decision required from user before running

**Which agent first, and what budget?**

Default plan (require user confirmation by end of Week 2, 2026-07-14):
- Start with **iSWE-Agent** (Java + cross-language story is cleanest).
- Smoke test on 3 bugs → confirm harness works.
- Scale to 20 bugs — enough for the FSE paper's §3.5 failure-mode analysis.
- Estimate: per-bug cost should be confirmed against the agent's published numbers before scaling.

Ask the user explicitly. Don't burn API budget unauthorized.

## Concrete first session

1. **Set up the agent harness.**
   - Clone the chosen agent into a sibling directory (NOT this repo). Note its commit SHA in `STATUS.md`.
   - Install per their instructions.
   - Verify it can resolve at least one of their published test cases (sanity check).

2. **Adapt the bug format.** Most agents expect SWE-bench-style input: repo, base commit, problem statement, gold patch. Write `scripts/to_swe_format.py` that converts our `bugs.jsonl` to the agent's input format.

3. **Smoke test.** Run on 2–3 bugs. Verify the harness produces results in the expected shape. Resolve any plumbing issues now, not at scale.

4. **Cost estimate.** Multiply observed token usage × model price × expected number of bugs. Report to user. Get explicit go-ahead.

5. **Full sweep.** Run on ≥20 bugs. Capture per-bug: status (resolved / failed / timed-out), patch diff, token cost, wall time. Write to `output/results.jsonl`.

6. **Qualitative failure-mode analysis.** For each failed bug, read the agent's trajectory log. Classify failure into one of:
   - `localization` — agent couldn't find the relevant files / functions.
   - `cross-language-blind` — agent found files in one language but missed the boundary partner. **This is the key result for our workshop paper.**
   - `patch-quality` — agent located correctly but produced an incorrect or incomplete patch.
   - `test-execution` — environment / tooling failure.
   - `other` — describe.

7. **Write `output/failure-modes.md`.** Counts + 3–5 narrative examples per failure mode. Highlight cross-language-blind cases — these are the paper's headline finding.

8. **Update [STATUS.md](STATUS.md).**

## Reproducibility checklist

For every run, save in `configs/runs/<agent>-<date>.yaml`:

- Agent name + commit SHA.
- Underlying LLM (e.g., `claude-sonnet-4-6`, `gpt-4o-2024-08-06`).
- Random seed if applicable.
- Token / time caps.
- Inputs (bug-corpus version, repo commits).
- Output paths.

Reviewers WILL ask for this. Treat it as load-bearing.

## Validation before you stop

- `output/results.jsonl` schema-validates and has one record per (agent, bug, run).
- For each "resolved" bug, sanity-check that the agent's patch isn't a no-op or test deletion.
- `output/failure-modes.md` counts add up to the total number of attempts.

## Definition of done (Phase A threshold)

🟢 means:
- At least one agent has end-to-end results on ≥20 cross-language bugs.
- Failure modes are categorized and documented.
- Cross-language-blind failures (if any) have specific PR/bug references the paper can cite.
- Costs are reported.

## Don't

- Don't run agents on bugs the agent's training data has seen. Cross-reference against known SWE-bench / Multi-SWE-bench sets if our corpus accidentally overlaps.
- Don't store the cloned agent code inside this repo (use a sibling dir + record SHA).
- Don't conclude "iSWE-Agent fails because cross-language" without reading trajectories. Failures may be banal (env setup) — separate the signal.
