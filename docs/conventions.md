# Conventions

These conventions exist so that any Claude session can pick up work without re-deriving where files go. Deviate only when a sub-step's `CLAUDE.md` explicitly overrides one of these rules.

## Directory layout inside a sub-step

```
steps/<step>/<sub-step>/
├── README.md            human-facing description
├── CLAUDE.md            agent instructions for THIS sub-step
├── STATUS.md            running state (update this as you work)
├── scripts/             executable code that produces data or results
├── configs/             config files (queries, filters, run configs)
├── data/
│   ├── raw/             gitignored — large, regenerable
│   ├── samples/         small committed samples (≤500 KB per file)
│   └── processed/       cleaned, annotated, ready for downstream
└── output/              reports, tables, figures, paper-ready artifacts
```

A sub-step may omit any of these directories if it doesn't need them. Don't invent new top-level directories without updating this file.

## Languages and tooling

- **Default language:** Python 3.11+. Use `uv` (preferred) or `pip` + `venv` for environments. One `pyproject.toml` per sub-step or one at the step root if scripts share dependencies.
- **TypeScript / Java / Go:** only when manipulating those languages' ASTs (tree-sitter bindings, `.proto` parsers). Don't write the orchestration logic in them.
- **Shell scripts:** only for thin wrappers over Python/CLI tools. Anything with logic goes in Python.

## Data formats

- **JSONL** for any append-friendly record stream (mined repos, extracted bugs, annotations). One JSON object per line, UTF-8.
- **JSON** for single-document configs and reports.
- **CSV / TSV** only when explicitly needed for paper tables.
- **Parquet** allowed for large processed datasets (>100 MB) — note format in the sub-step's README.

Every JSONL or JSON output that's part of a research artifact must conform to a schema in [`shared/schemas/`](../shared/schemas/). If a new schema is needed, add it there and reference it from the sub-step's README.

## File naming

- Kebab-case for files and directories: `github-mining.py`, not `GitHubMining.py`.
- Date-stamp data dumps: `repos-2026-06-23.jsonl`, not `repos-final-v2.jsonl`.
- Numbered prefixes (`01-`, `02-`) only at the step / sub-step boundary, where ordering matters.
- Scripts that are entry points (run from CLI) live in `scripts/` and have a `__main__` block.

## STATUS.md format

Every sub-step has a `STATUS.md`. Required sections:

```markdown
# Status: <sub-step name>

**Last updated:** YYYY-MM-DD
**Owner:** <person or "unassigned">
**State:** ⚪ not started | 🟡 in progress | 🟢 done | 🔴 blocked

## What's done
- ...

## What's next
- ...

## Open questions
- ...

## Artifacts produced
- `path/to/file.jsonl` — N records, schema vX
```

Update this when you finish a unit of work, not at the end of the session — a session may be interrupted.

## LLM prompts

Reusable prompts live in [`shared/prompts/`](../shared/prompts/) and are versioned by filename suffix: `bug-classifier-v1.md`, `bug-classifier-v2.md`. When you change a prompt, bump the version — don't overwrite. Record which version produced which output in the relevant `STATUS.md`.

## Citing the research plan

In commits, docs, and code comments, refer to the plan as `§<section>` (e.g., `§3.3 Step 1.2`). This makes it easy to grep back to the canonical motivation.

## Commit messages (when this repo becomes a git repo)

- `step-1.1: mine 50 Java+TS monorepos from GitHub`
- `step-1.2: add bug taxonomy v1 with 6 categories`
- `docs: clarify JSONL schema for repo metadata`

First token is the scope (`step-X.Y` or `docs` or `shared`). Keep subject line under 72 chars.

## What NOT to commit

- API tokens, `.env` files, anything matching `.gitignore` patterns.
- Cloned target repositories (use `data/raw/repos-cache/` which is gitignored).
- Full mined dumps over 10 MB — link from `STATUS.md` to where they live instead.
- Half-edited paper drafts in the main step directories — put paper work in `04-workshop-paper/sections/`.

## When in doubt

Read the relevant sub-step's `CLAUDE.md`. If still unclear, write the open question into `STATUS.md` and proceed with a documented default.
