# Prompts

Reusable LLM prompts used across sub-steps.

## Versioning

- Filename carries the version: `bug-classifier-v1.md`, `bug-classifier-v2.md`.
- Never overwrite a published version. Bump the suffix.
- Record the prompt version in the output record (e.g., bug annotations carry a `prompt_version` field).

## Format

Each prompt is a markdown file with these sections:

```markdown
# <Prompt Name> vN

## Purpose
What this prompt is used for, what sub-step uses it.

## Inputs
What variables are substituted in, with examples.

## Output schema
Reference to the JSON Schema the output should conform to, or a description.

## Prompt body
The actual prompt text. Use {{variable}} for substitutions.

## Change log
- vN: what changed from v(N-1)
```

## When to add a prompt here

- It's used in ≥2 sub-steps, OR
- Its output appears in published-paper artifacts.

Single-use, exploratory prompts can live next to the script that uses them.
