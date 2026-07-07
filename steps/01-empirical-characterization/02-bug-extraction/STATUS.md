# Status: Sub-step 1.2 — Bug Extraction & Annotation

**Last updated:** 2026-06-27
**Owner:** unassigned
**State:** ⚪ Unblocked — ready to start
**Milestone:** ≥100 annotated bugs by 2026-07-21 (end of Week 3 in the FSE 2027 schedule)

## What's done

Nothing yet. 1.1 is complete; `../01-github-mining/data/processed/repos.jsonl` has 145 repos ready to mine.

## What's next

Follow [CLAUDE.md](CLAUDE.md) "Concrete first session" steps 1–7. First action: write `scripts/fetch_prs.py`.

## Open questions

- **Per-language-pair targets.** Aim for 50 Java+TS bugs AND 50 Python+Go bugs separately, or 100 total without balancing? Default: try for balance; document if one pair is naturally scarcer.
- **Public PR text in the dataset.** GitHub PR titles/bodies are public, but commit messages and linked issues can contain author emails. Review before publication.
- **LLM pre-classification.** Try a Claude prompt that suggests category + rationale, then human-confirm? Could 3–5× annotation throughput. Worth experimenting *after* annotating ~20 manually so we have ground truth to calibrate against.

## Artifacts produced

None.
