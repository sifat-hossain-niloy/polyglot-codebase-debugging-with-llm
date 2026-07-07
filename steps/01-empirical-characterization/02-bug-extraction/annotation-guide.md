# Annotation Guide — Cross-Language Bug Corpus

**Purpose:** ensure a second annotator can reproduce our classifications so we can report inter-rater agreement (κ) in Phase B of the FSE paper.

**Prerequisites:** read [taxonomy.md](taxonomy.md) end-to-end before starting. This guide assumes you already know the six categories.

**Time budget:** aim for 5–15 minutes per PR. If you're at 20 minutes, mark `skip` and move on — spending an hour on one ambiguous case biases the corpus.

---

## What you're producing

One JSONL record per bug that conforms to [`shared/schemas/bug-annotation.schema.json`](../../../shared/schemas/bug-annotation.schema.json). Every kept bug gets:

- `bug_id` — `<owner>/<repo>#<pr_number>` (already set by the fetch script)
- `category` — one of `schema`, `coerce`, `nil`, `serde`, `async`, `other`
- `secondary_category` — same set, or null
- `boundary_kind` — `rest`, `grpc`, `shared-file`, `subprocess`, `ffi`, `other`, `unknown`
- `rationale` — 20+ chars, 1–2 sentences
- `is_confirmed_cross_language` — true if you're confident the bug requires *both* languages to manifest
- `annotator` — your initials or handle
- `annotated_at` — ISO timestamp

---

## Step-by-step for each candidate PR

### 1. Open the PR in a browser

Use `pr_url` from the candidate record. Skim the title, body, and linked issues.

### 2. Ask three yes/no questions

**Q1: Is this a real bug fix (not a refactor, docs, or feature)?**

Signals the answer is *no* → mark `skip`:
- Title starts with "Refactor", "Cleanup", "docs", "Add feature", "Introduce".
- Body says "no functional change" or "internal cleanup".
- Diff shows renames without behavioral changes.

**Q2: Was the bug caused by the *interaction* between the two languages?**

Signals the answer is *no* → mark `skip`:
- Files in the two languages were both touched but for independent reasons (e.g., a global rename that happens to hit both).
- The bug is entirely on one side; the "other language" change is just a follow-up (tests, docs, or renaming a mirrored variable).
- The bug would still happen if the two sides used the same language.

Signals the answer is *yes* → proceed:
- The bug report describes an interaction ("frontend crashes on this backend response").
- The fix requires *coordinated* changes on both sides.
- The stack trace or reproduction path crosses the wire (REST/gRPC/subprocess/FFI).

**Q3: Do you understand enough to categorize?**

If the diff is opaque or the description too brief → mark `skip` rather than guess.

### 3. Categorize

Use [taxonomy.md](taxonomy.md). Pick the *primary cause*, not the symptom.

Order of consideration if two categories seem to fit:
1. `schema` (contract-level) beats `coerce` (representation-level) beats `serde` (encoding-level).
2. `nil` and `async` are orthogonal to the above — use them when the bug is specifically about optionality or timing.
3. Never use `other` without a full sentence of rationale.

### 4. Set `boundary_kind`

Best guess from PR contents:
- `.proto` in the diff → `grpc`
- `openapi.yaml` / `swagger` / `axios(` / `fetch(` in the diff → `rest`
- `/android/native/` or React Native bridge code → `ffi`
- Shell / `exec` / subprocess boundary → `subprocess`
- Can't tell → `unknown`

### 5. Write the rationale (mandatory, ≥20 chars)

One or two sentences. Answer: **why this category**, and if applicable, **why not the other candidate categories**.

Bad rationale: "Type mismatch." (too short)
Good rationale: "Java DTO field renamed in v3; TS binding not regenerated → runtime crash on this route. `schema` because the fix touches the shared OpenAPI definition, not the encoding."

### 6. Save

Append the record to `data/processed/bugs.jsonl`. Use `scripts/write_annotation.py` if provided, or edit by hand carefully.

---

## Skipping — when and how

Skip freely. Skipped PRs go to `data/processed/skipped.jsonl` with a one-line reason. Skipping is fine; misclassifying poisons the dataset.

Common skip reasons:
- `not-cross-language` — coincidental dual-touch
- `not-a-bug` — refactor / feature / docs
- `insufficient-context` — can't tell from PR alone
- `too-large` — >500 files or the fix spans many unrelated changes
- `duplicate` — same underlying bug as another already-annotated PR (link both)

---

## Consistency drift

Every 25 PRs, re-read this guide and [taxonomy.md](taxonomy.md). Annotator drift is real — categories that felt clear at PR #10 often blur by PR #40.

Also every 25 PRs: skim your last 5 rationales. If they sound thin, revisit them.

---

## Second-annotator κ

For κ computation:
- Second annotator processes a subset of ≥30 already-annotated PRs, *without seeing* the first annotator's label.
- The `write_annotation.py` script has an `--annotator` flag that writes to a separate JSONL. Merge and compute κ with a small script.
- Cohen's κ ≥ 0.7 is the standard threshold for the paper.

---

## LLM-assisted annotation

If you use an LLM to pre-classify:

- Version the prompt under [`shared/prompts/`](../../../shared/prompts/) — never edit an in-use prompt in place.
- Record `prompt_version` in each annotation.
- **Human confirms every LLM label.** The LLM is a suggestion engine; the annotator is the source of truth.
- For the paper: report LLM-assist as part of the methodology, disclose the fraction of PRs where the annotator overrode the LLM.
