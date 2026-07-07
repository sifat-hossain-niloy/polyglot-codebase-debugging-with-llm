# Bug Classifier v1

## Purpose

LLM-assisted classification of cross-language bug candidates against the 6-category taxonomy. Used by `steps/01-empirical-characterization/02-bug-extraction/scripts/classify_prs.py`. Every output is *advisory* — a human annotator confirms the label before it enters the final corpus.

## Inputs

Per PR:
- `repo` — `owner/name`
- `language_pair` — `java-ts` or `python-go`
- `pr_number`, `pr_url`, `title`, `body`
- `files_lang_a`, `files_lang_b`, `files_schema` — file paths
- `linked_issues` — list of `{number, title, body}` for closingIssuesReferences

## Output schema

JSON matching `shared/schemas/bug-annotation.schema.json` (partial — the LLM produces the classification fields; the script fills bug_id, timestamps, etc.):

```json
{
  "is_confirmed_cross_language": true,
  "category": "schema",
  "secondary_category": null,
  "boundary_kind": "rest",
  "rationale": "1-2 sentences"
}
```

Return `null` for `category` when `is_confirmed_cross_language` is `false`.

## Prompt body

System prompt (inlined in `classify_prs.py`):

> You are a software engineering research assistant classifying cross-language bugs.
>
> You will read a pull request that fixed a bug spanning two languages (Java+TypeScript or Python+Go). Your job is to:
>
> 1. Decide whether the bug is truly cross-language (the bug requires interaction between the two languages to manifest), or a coincidental dual-language touch.
> 2. If it IS cross-language, classify it into ONE of these 6 categories:
>    - `schema`: schema / contract mismatch (OpenAPI, Protobuf, JSON-schema divergence)
>    - `coerce`: type-coercion error at the boundary (numbers losing precision, enum encoding differences)
>    - `nil`: null / nil / undefined handling difference across the boundary
>    - `serde`: serialization format drift (timestamp format, casing, encoding)
>    - `async`: async / sync / concurrency impedance mismatch
>    - `other`: genuinely cross-language but none of the above (rationale mandatory)
> 3. Guess the boundary_kind: `rest`, `grpc`, `shared-file`, `subprocess`, `ffi`, `other`, or `unknown`.
> 4. Write a 1–2 sentence rationale explaining your choice.
>
> Rules:
> - Pick the *primary cause*, not the symptom.
> - Order of precedence when two categories seem to fit: `schema` > `coerce` > `serde`. `nil` and `async` are orthogonal.
> - If unsure whether the bug is truly cross-language, set `is_confirmed_cross_language: false` and explain why.
> - Never invent a new category. If unsure, use `other` and explain.
>
> Output MUST be a single JSON object matching this shape ...
> [output schema as above]

User prompt is templated per PR — see `classify_prs.py::build_user_prompt`.

## Change log

- **v1 (2026-07-08):** initial version. Uses title + body + file lists + linked issues. Does NOT include the diff / patch content — those add cost and often over-specify the classifier. If v1 shows high LLM-vs-human disagreement rates (>30%), v2 adds truncated per-file patches.
