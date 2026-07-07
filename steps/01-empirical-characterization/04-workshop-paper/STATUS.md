# Status: Sub-step 1.4 — FSE Paper §3 Empirical-Study Skeleton

**Last updated:** 2026-06-27
**Owner:** unassigned
**State:** ⚪ Not started (scope changed 2026-06-27; outline exists)
**Deadline:** 2026-10-02 (full FSE paper submission)

## What's done

- Outline rewritten for FSE §3 scope: [outline.md](outline.md).
- README and CLAUDE.md updated to reflect that this sub-step now owns §3 of the FSE paper (not a standalone workshop paper).

## What's next

1. Confirm the FSE 2027 CfP: page limit, double-blind rules, artifact-badge deadlines. Record here.
2. Create `sections/` directory. Draft `sections/03-empirical-study.md` skeleton with headers from outline.
3. Write the corpus/methodology paragraph now — 1.1 numbers are already available in `../01-github-mining/output/repo-summary.md`.
4. As 1.2 lands annotations, add taxonomy prevalence and example bugs.
5. As 1.3 lands baseline runs, add the failure-mode analysis.

## Open questions

- **Double-blind or not.** Depends on FSE 2027 CfP. Affects whether we anonymize repo names in the draft.
- **Page-budget check.** Is ~4 pages really enough for §3? Might need to negotiate with §5/§6 later. Not a decision for today.
- **RN sub-population.** Report separately as a "boundary_kind = ffi" category, or exclude from primary corpus? Decide once 1.2 has annotated ~20 RN-repo PRs.

## Artifacts produced

- `outline.md` — the §3 section structure.
