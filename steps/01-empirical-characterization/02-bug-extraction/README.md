# Sub-step 1.2 — Bug Extraction & Annotation

**Maps to:** §3.3 Step 1.2 + §6 item 14 of the [research plan](../../../Polyglot_Debugging_Research_Progress_Report.md).
**Goal:** From the mined repos, extract closed PRs that fixed cross-language bugs, then annotate them with our 6-category taxonomy.

## What "cross-language bug" means here

A closed PR that:

1. Modified files in *both* languages of the pair (e.g., both `*.java` and `*.ts`).
2. Was linked to an issue or had a description indicating the bug was caused by interaction between the languages — not a coincidental dual-touch.
3. Was merged (a real fix landed, so we have ground-truth changes).

PRs that touch both languages incidentally (e.g., a renaming refactor) DO NOT count. Annotator judgment matters.

## Inputs

- `01-github-mining/data/processed/repos.jsonl` — the repo list.
- GitHub API access (PR + diff + linked-issue endpoints).
- Annotation taxonomy from [docs/glossary.md](../../../docs/glossary.md).

## Outputs

- **`data/processed/bugs.jsonl`** — annotated cross-language bugs, conforming to [`shared/schemas/bug-annotation.schema.json`](../../../shared/schemas/bug-annotation.schema.json).
- **`taxonomy.md`** — finalized taxonomy with ≥3 worked examples per category.
- **`annotation-guide.md`** — instructions for a second annotator (used in Phase B for κ reporting).
- **`output/bug-stats.md`** — counts per category, per language pair, per repo.

## Process

1. **Candidate extraction.** For each repo, page through closed PRs. Filter to those touching both languages. Save raw candidates.
2. **Manual triage.** Annotator reads PR title + body + issue + diff to confirm it's a true cross-language bug.
3. **Categorization.** Assign one of the 6 categories from the glossary. Free-text rationale (1–2 sentences) is required for every annotation.
4. **Schema-conformant write-out.** Each kept bug becomes one record in `bugs.jsonl`.

## Pitfalls

- **Linked-issue ambiguity.** Many PRs don't link issues. Use commit-message scraping (`Fixes #...`, `Closes #...`) as a secondary signal.
- **Bot PRs.** Dependabot, Renovate, etc. Filter them. They touch many languages but they're not bugs.
- **Cherry-picks and backports.** Same bug appears multiple times. Deduplicate by issue or by the primary commit SHA.
- **Annotator drift.** As you annotate more, your category interpretation drifts. Re-read your annotation-guide every 25 bugs.

## Phase boundary

This sub-step produces:
- 50–100 bugs annotated → enough for Phase A (workshop paper).
- 200–400 bugs annotated → required for Phase B (empirical paper).

Stop at the Phase A threshold, write up findings, then return here to expand for Phase B.

See [CLAUDE.md](CLAUDE.md) and [STATUS.md](STATUS.md).
