# Shared

Cross-step infrastructure: schemas, reusable prompts, utility scripts.

## Layout

```
shared/
├── schemas/         JSON Schemas for data artifacts (repos, bugs, runs)
├── prompts/         versioned LLM prompts reused across sub-steps
└── utils/           cross-step Python helpers (CLI tools, parsers)
```

## Rules

- **Schemas are versioned in the filename.** `repo.schema.json` is v1; the next version is `repo.schema.v2.json` and we don't overwrite v1.
- **Prompts are versioned in the filename.** `bug-classifier-v1.md`, `bug-classifier-v2.md`. Whichever version produced an output is recorded in that sub-step's STATUS.
- **Utils have unit tests.** If you add code here, add tests. This is the one place we don't accept "research script" hygiene — too many sub-steps depend on it.

## When to add here

- A data shape is used by ≥2 sub-steps → schema.
- A prompt is used by ≥2 sub-steps OR produces published-paper outputs → prompts/.
- A function is needed by ≥2 sub-steps → utils/.

Single-sub-step prompts and schemas live next to the sub-step that uses them, not here.
