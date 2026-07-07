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
- **Batch 1 classified manually:** 50 top-scored candidates → 12 confirmed (24%).
- **Batch 2 classified manually:** 50 candidates from the boundary_hint=unknown pool → 7 confirmed (14%). Lower yield expected — this pool has no explicit schema/rest/grpc/ffi signals.
- **`data/processed/bugs.jsonl`** — **19 schema-validated annotations (10 java-ts + 9 python-go).**
- **`data/processed/skipped.jsonl`** — 81 skips with reasons.
- **`output/bug-stats.md`** — paper-ready summary. Cumulative patterns after 100 PRs reviewed:
  - `schema` × REST = 4 bugs (dominant pattern for contract-drift class)
  - `schema` × gRPC = 2 bugs (proto-contract drift)
  - `coerce` × FFI = 3 bugs (dominant for type-coercion class)
  - `nil`: 4 bugs across REST, gRPC, and FFI — nullability is the most boundary-agnostic failure mode
  - `serde` × other = 1 bug (shared string-format parsing)
  - `async` bugs at FFI (2) and other (1) — none at REST/gRPC yet
  - Boundary count: FFI 8, REST 5, gRPC 4, other 2
  - Skip reasons: 31 features / 25 not-cross-language / 21 not-a-bug / 3 insufficient / 1 feature+integration

## What's next

**Progress: 19/100 bugs after 2 batches (2 sessions). Extrapolating at ~17% yield → we need ~5 more batches to hit 100 confirmed bugs.**

Batch 3 next: sample 50 more candidates that weren't in batches 1 or 2. Repos not yet sampled: ~90+ (candidates.jsonl has repos from 400+ that neither batch touched). Expected yield: 10–15% (further into the tail; the low-signal pool is where genuine cross-lang bugs are increasingly rare).

Alternative paths still available (as before):
- **API-driven bulk classification.** Add `ANTHROPIC_API_KEY` to `.env`, run `classify_prs.py --limit 568`. LLM proposes labels → human verifies. ~$5–20.
- **Fetch diffs for higher-confidence classification.** Current pass uses title/body/files only. `--fetch-diff` would resolve the "insufficient context" skips.

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
- `data/processed/batch-1-selection.jsonl`, `data/processed/batch-2-selection.jsonl` — sampled batches
- `data/processed/bugs.jsonl` — **19 annotated cross-language bugs** ✓ schema-validated
- `data/processed/skipped.jsonl` — 81 skips
- `output/bug-stats.md` — paper-ready summary

## Open questions

- **Per-language-pair targets.** Aim for 50 Java+TS bugs AND 50 Python+Go bugs separately, or 100 total without balancing? Default: try for balance; document if one pair is naturally scarcer.
- **Public PR text in the dataset.** GitHub PR titles/bodies are public, but commit messages and linked issues can contain author emails. Review before publication.
- **LLM pre-classification.** Try a Claude prompt that suggests category + rationale, then human-confirm? Could 3–5× annotation throughput. Worth experimenting *after* annotating ~20 manually so we have ground truth to calibrate against.

## Artifacts produced

None.
