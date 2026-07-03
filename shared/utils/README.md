# Utils

Cross-step Python helpers. Anything imported by ≥2 sub-steps lives here.

## Current contents

None yet — populate as Step 1 sub-steps need shared helpers (likely candidates: schema validators, JSONL streamers, GitHub API client with retry+backoff).

## Rules

- Pure Python, no global state.
- Each module has at least one unit test. Use `pytest`.
- Public function signatures get type hints.
- No business logic — helpers only. Sub-steps own their domain logic.

## Suggested first additions (when needed)

- `jsonl.py` — `iter_records(path)`, `write_records(path, records)`.
- `schema.py` — wrapper around `jsonschema` for validating against `shared/schemas/`.
- `github.py` — authenticated client with rate-limit backoff, used by Step 1.1 and 1.2.
- `costs.py` — token-count → USD estimation for whichever LLM is in use.
