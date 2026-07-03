# Status: Sub-step 1.2 — Bug Extraction & Annotation

**Last updated:** 2026-06-23
**Owner:** unassigned
**State:** 🔴 Blocked on 01-github-mining

## What's done

Nothing yet. Cannot start until [01-github-mining](../01-github-mining/STATUS.md) produces `repos.jsonl`.

## What's next

When unblocked, follow [CLAUDE.md](CLAUDE.md) "Concrete first session" steps 1–7.

## Open questions

- **Per-language-pair targets.** Aim for 50 Java+TS bugs AND 50 Python+Go bugs separately, or 100 total without balancing? Default: try for balance; document if one pair is naturally scarcer.
- **Public PR text in the dataset.** GitHub PR titles/bodies are public, but commit messages and linked issues can contain author emails. Review before publication.
- **LLM pre-classification.** Try a Claude prompt that suggests category + rationale, then human-confirm? Could 3–5× annotation throughput. Worth experimenting *after* annotating ~20 manually so we have ground truth to calibrate against.

## Artifacts produced

None.
