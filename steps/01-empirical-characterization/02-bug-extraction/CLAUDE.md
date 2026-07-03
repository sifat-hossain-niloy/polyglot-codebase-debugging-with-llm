# Agent Instructions — Sub-step 1.2 (Bug Extraction & Annotation)

## Prerequisite

`../01-github-mining/data/processed/repos.jsonl` must exist. If it doesn't, go finish 1.1 first.

## Concrete first session

1. **Write `scripts/fetch_prs.py`.** For each repo in `repos.jsonl`:
   - Page `closed && merged` PRs via GitHub REST or GraphQL (GraphQL preferred — fewer calls per page).
   - For each PR, fetch: title, body, labels, linked issues (via `closingIssuesReferences` in GraphQL), file changes with language detection, list of commits.
   - Filter: PR touches files in both languages of the pair. Drop bot authors.
   - Write to `data/raw/prs-<repo>-<date>.jsonl`.

2. **Write `scripts/triage_prs.py`.** A semi-automated filter:
   - Heuristic pre-filter: keep PRs where ≥2 files are in each language AND PR title/body contains bug-indicating keywords (`fix`, `bug`, `issue`, error, crash, mismatch, null, undefined).
   - Output `data/processed/candidates.jsonl` for human review.

3. **Write `taxonomy.md`.** Start from the 6 categories in [docs/glossary.md](../../../docs/glossary.md). Expand each with:
   - Definition (1 sentence).
   - 2–3 worked examples once you have annotations.
   - Boundary cases ("counts as X, not Y because...").

4. **Write `annotation-guide.md`.** Step-by-step protocol a second annotator would follow. Cover:
   - How to read a PR.
   - How to decide if it's truly cross-language vs. coincidental dual-touch.
   - How to pick a category when two seem to apply (pick the primary cause).
   - When to skip a PR ("can't determine root cause without running the code").

5. **Annotate.** Read each candidate, decide keep/skip, assign category, write rationale. Write to `data/processed/bugs.jsonl` conforming to [`shared/schemas/bug-annotation.schema.json`](../../../shared/schemas/bug-annotation.schema.json).

6. **Generate `output/bug-stats.md`.** Counts per category, per language pair, per repo. Note: imbalanced counts ARE a finding for the paper, not a problem to hide.

7. **Update [STATUS.md](STATUS.md).** Record annotation progress, current category counts, next batch to annotate.

## Annotation budget

Annotating one bug takes 5–15 minutes if you do it carefully. Plan for:
- 5–10 hours per batch of 50.
- Break in batches of 25 to re-read the guide.

When using Claude to assist annotation, treat its category suggestion as advisory — always read the actual PR diff yourself before committing the label. The taxonomy is *yours*.

## LLM-assisted annotation (optional)

If you spawn an agent or use a structured-output prompt to *pre-classify* candidates, version the prompt under [`shared/prompts/`](../../../shared/prompts/) (e.g., `bug-classifier-v1.md`) and record the prompt version in each annotation record. Don't accept LLM labels uncritically — they're a hypothesis, you confirm.

## Validation before you stop

- `bugs.jsonl` validates against schema.
- Each record has: PR URL, repo, language pair, category, rationale, files changed (per language), linked issue.
- `taxonomy.md` has examples in every populated category.
- `output/bug-stats.md` matches the actual JSONL counts (don't let stats and data drift).

## Definition of done (Phase A threshold)

🟢 means:
- ≥100 bugs annotated total (50 per language pair is a strong target).
- All 6 categories have ≥3 examples each, or category is documented as "empty in current corpus."
- Taxonomy and annotation-guide are stable enough that a second annotator could follow them.
- `STATUS.md` updated; sub-step 03 unblocked.

## Don't

- Don't add taxonomy categories on the fly. Discuss in [docs/glossary.md](../../../docs/glossary.md) first, then update here.
- Don't include PRs you can't confidently classify. Skipping is fine; misclassifying poisons the dataset.
- Don't release `bugs.jsonl` publicly without a license/PII review.
