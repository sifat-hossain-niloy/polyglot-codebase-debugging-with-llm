# Status: Sub-step 1.2 — Bug Extraction & Annotation

**Last updated:** 2026-07-08
**Owner:** Sifat (LLM-assisted for MVP; second human annotator TBD for κ)
**State:** 🟡 In progress — pipeline scripts written, fetch running
**Milestone:** ≥100 annotated bugs by 2026-07-21 (end of Week 3 in the FSE 2027 schedule)

## What's done

- Directory structure created: `scripts/`, `data/{raw,processed}`, `output/`.
- **Pipeline scripts written and validated:**
  - `scripts/fetch_prs.py` — GraphQL paging over merged PRs, filters to those touching both languages
  - `scripts/triage_prs.py` — heuristic filter (bug keywords, release/bump/docs blocklist, boundary-hint guessing)
  - `scripts/classify_prs.py` — LLM-assisted classification scaffold (needs `ANTHROPIC_API_KEY` for API-driven scale)
  - `scripts/bug_stats.py` — generates the paper-ready bug-stats.md
- **`taxonomy.md`** — 6 primary categories + boundary sub-tags, with worked examples and boundary-case rules.
- **`annotation-guide.md`** — protocol a second annotator can follow (for κ in Phase B).
- **`shared/prompts/bug-classifier-v1.md`** — versioned LLM classification prompt.
- **Fetch complete:** 1,206 raw cross-language PRs (579 java-ts + 627 python-go) from 145 repos.
- **Triage complete:** 668 candidates (330 java-ts + 338 python-go) after keyword + files filter. Rejection reasons dominated by "no bug keyword" (docs/refactors/features) and a small tail of massive-diff PRs.
- **Batch 1 classified manually:** 50 top-scored candidates read in-conversation → **12 confirmed cross-language bugs (24%), 38 skipped.**
- **`data/processed/bugs.jsonl`** — 12 schema-validated annotations (7 java-ts + 5 python-go).
- **`data/processed/skipped.jsonl`** — 38 skips with reasons.
- **`output/bug-stats.md`** — paper-ready summary. Notable patterns already visible:
  - `schema` bugs cluster at REST + gRPC (5/6 total)
  - `coerce` bugs cluster at FFI (2/3 total)
  - `serde` and `other` categories still empty — need more sampling
  - Skip reasons: 17 features / 11 not-a-bug / 7 not-cross-language / 2 insufficient-context

## What's next

**To reach the 100-bug Phase-A target, we need ~4 more batches like this one.** Options in priority order:

1. **Batch 2 in a follow-up session (recommended immediate next step).** Sample the next 50 candidates that didn't make batch 1's top-signal cut — likely a lower-yield mix (~15% confirmed), so plan for 50-per-batch × 3 more batches to hit 100 confirmed bugs. Total effort: 3 focused Claude sessions.
2. **API-driven bulk classification.** Add `ANTHROPIC_API_KEY` to `.env`, then `uv add anthropic` and run `classify_prs.py --limit 500`. LLM proposes labels → human review confirms. ~$5–20 API cost for the full 668. Faster but requires human verification loop on paper claims.
3. **Fetch diffs for higher-confidence classification.** Current pass uses title/body/files only; some skips flagged as "insufficient context" would resolve with the actual diff. Add a `--fetch-diff` mode to fetch_prs.py.

## Open questions

- **ANTHROPIC_API_KEY.** Decision from user: enable API-driven classify_prs.py for scale, or continue manual in-conversation batches?
- **RN sub-population handling.** 4 of 7 java-ts bugs are FFI (React Native / Capacitor Android bridges). Paper decision: include as a distinct category, or filter out?
- **Second annotator.** Needed for κ before Phase B. Recruiting is a decision for the user.
- **Diff-level review.** Should we fetch full diffs before the paper submission, to strengthen "insufficient context" skips into confirmed classifications?

## Artifacts produced

- `scripts/fetch_prs.py`, `scripts/triage_prs.py`, `scripts/classify_prs.py`, `scripts/bug_stats.py`
- `taxonomy.md`, `annotation-guide.md`
- `data/raw/prs-<pair>-2026-07-08.jsonl` — 1,206 raw PRs (gitignored)
- `data/processed/candidates-2026-07-08.jsonl` — 668 triaged candidates (gitignored)
- `data/processed/batch-1-selection.jsonl` — 50-PR stratified sample
- `data/processed/bugs.jsonl` — **12 annotated cross-language bugs** ✓ schema-validated
- `data/processed/skipped.jsonl` — 38 skips
- `output/bug-stats.md` — paper-ready summary

## Open questions

- **Per-language-pair targets.** Aim for 50 Java+TS bugs AND 50 Python+Go bugs separately, or 100 total without balancing? Default: try for balance; document if one pair is naturally scarcer.
- **Public PR text in the dataset.** GitHub PR titles/bodies are public, but commit messages and linked issues can contain author emails. Review before publication.
- **LLM pre-classification.** Try a Claude prompt that suggests category + rationale, then human-confirm? Could 3–5× annotation throughput. Worth experimenting *after* annotating ~20 manually so we have ground truth to calibrate against.

## Artifacts produced

None.
