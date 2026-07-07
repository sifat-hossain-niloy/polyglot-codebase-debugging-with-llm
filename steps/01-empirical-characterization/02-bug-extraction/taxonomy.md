# Cross-Language Bug Taxonomy

Six primary categories for cross-language bugs. Every bug in `data/processed/bugs.jsonl` gets exactly one primary category, an optional secondary category, and a 1–2 sentence rationale.

Seeded from Cai et al.'s FSE 2025 taxonomy of Python–C and Java–C bugs, adapted for REST/gRPC-mediated boundaries in Java+TS and Python+Go.

---

## Rule of thumb: pick the *primary* cause, not the symptom

If a Java service sends `userId` as a `Long`, the TS client parses it as `number`, and JavaScript silently truncates the value above 2^53 → the primary cause is **type-coercion at the boundary** (`coerce`), not a null-handling difference or serialization drift. The symptom is a wrong ID; the cause is a type-precision mismatch across the JSON boundary.

If two categories genuinely overlap, put the primary in `category` and the second in `secondary_category`.

---

## `schema` — Schema / contract mismatch

**Definition:** the OpenAPI / Protobuf / JSON-schema *contract* between the two languages diverged. Either side is internally correct; the contract is what changed or was mis-implemented.

**Signals to look for:**
- The PR touches a `.proto` file, `openapi.yaml`, `swagger.json`, or JSON-schema definition alongside code in both languages.
- The bug report says "field X was renamed / removed / changed type" and the fix updates the contract + regenerates bindings.
- The Java DTO and TS interface refer to a field with a different name or type.

**Worked example (illustrative):**
> "Fix `orderStatus` field mismatch between Java DTO and TS interface. The backend enum was extended in v2.3 but the TypeScript union type was never updated, causing runtime crashes in the OrderTable component when a new status arrives from the API."
> → primary category = `schema`, boundary = `rest`, secondary_category = null.

**Boundary cases:**
- If the fix only touches the contract file (say, `.proto`) but code changes are code-generated only → still `schema`. The bug is contract drift.
- If one side has the correct contract but implements it wrong → NOT `schema`; use `coerce` or the more specific category matching the implementation bug.

---

## `coerce` — Type-coercion error at boundary

**Definition:** the two languages agree on the field name but disagree on how the value is *represented* or *converted* across the wire.

**Signals to look for:**
- Numbers: Java `Long`/`BigDecimal` → JSON → TS `number` (precision loss above 2^53).
- Booleans: Python treats `"true"` as truthy; Go strictly requires `true`.
- Enums: string vs numeric encoding differs.
- Timestamps: ISO-8601 vs epoch millis vs epoch seconds.
- Currencies / decimals: Java `BigDecimal` serialized as string but the TS parser expects a number.

**Worked example (illustrative):**
> "Fix invoice amount overflow when total exceeds 9,007,199,254,740,992. The backend uses `BigDecimal` for precise arithmetic; JSON serialization was fine but the React client stored it as `number`, silently losing precision on very-large-invoice reproductions."
> → primary category = `coerce`, boundary = `rest`.

**Boundary cases:**
- If the *schema* explicitly declares the type and one side violates it → `schema`. If the schema is silent or under-specified and the sides pick different encodings → `coerce`.

---

## `nil` — Null / nil / undefined handling difference

**Definition:** one language's null semantics don't map to the other's, producing a bug whose fix hinges on optionality/nullability at the boundary.

**Signals to look for:**
- Java `null` → JSON `null` → TS `undefined` (the fields *disappear* rather than becoming null).
- Go zero-value ambiguity: an empty string `""` may mean "not set" (Python `None`) or "explicitly empty."
- Optional fields in Protobuf 3 vs Python `Optional[...]` vs TS `field?:`.
- Null propagation across the boundary that a single-language linter can't catch.

**Worked example (illustrative):**
> "Fix `user.middleName` crash on user profile page. Backend uses `null` for users with no middle name; frontend was destructuring assuming the key existed. Added a defensive `??` in the ProfileHeader, but the real fix is a nullable field in the OpenAPI schema."
> → primary category = `nil`, secondary = `schema`, boundary = `rest`.

**Boundary cases:**
- If both sides handle null but do it inconsistently and the fix touches the schema too → primary `nil`, secondary `schema`.

---

## `serde` — Serialization format drift

**Definition:** the wire format itself changed — encoding, field ordering, escaping, framing — but the schema fields are the same.

**Signals to look for:**
- Timestamp format changed (ISO-8601 without timezone → with timezone).
- Base64 vs raw bytes for binary fields.
- Case convention: `camelCase` on one side, `snake_case` on the other (usually via Jackson/GSON annotations vs default JS).
- Character encoding: UTF-8 vs UTF-16 mishandling in `.proto` string fields.
- Trailing newline / whitespace differences that a strict parser rejects.

**Worked example (illustrative):**
> "Fix workflow start timestamps arriving 5 hours off. Backend upgraded Jackson to a version that emits ISO-8601 with timezone by default; the older Angular client was assuming local time. Rolled back Jackson default and added explicit timezone in the API response."
> → primary category = `serde`, boundary = `rest`.

**Boundary cases:**
- If a *field* was added/removed → `schema`. If the *encoding* of an existing field changed → `serde`.

---

## `async` — Async / sync impedance mismatch

**Definition:** timing, ordering, or concurrency semantics across the boundary produce a bug.

**Signals to look for:**
- TS promise unawaited where Java expected a synchronous response.
- Streaming vs unary gRPC calls treated differently on the two sides.
- Race between a Java REST call and its response handler in a TS event loop.
- Retries / idempotency: Go client retries a call that the Python server processed as duplicated.
- Websocket / SSE message ordering that violates a contract-level assumption.

**Worked example (illustrative):**
> "Fix duplicate charge on payment webhook retries. Go webhook publisher retries with 2s backoff when the Python receiver takes >1s; the receiver was not idempotent. Added an idempotency key in the payload and a dedupe check on the Python side."
> → primary category = `async`, secondary = `nil` (if the key can be missing), boundary = `rest`.

**Boundary cases:**
- Pure single-side threading bugs are NOT cross-language. This category requires the timing mismatch to be between the two sides.

---

## `other` — Doesn't fit above

**Definition:** the bug is genuinely cross-language but doesn't match any of the five categories above. Rationale is *mandatory* — no bare `other` labels.

**Signals:**
- New failure modes we didn't anticipate. Writing them here informs the paper's future-work section.

**Examples that would go here:**
- Character-set incompatibilities that aren't strictly `serde` (e.g., collation mismatch in a shared DB layer).
- Build-time cross-language issues (say, a Java build target that assumes a specific TS output structure).
- Cross-language dependency-version drift (a shared library exists in both languages and the versions diverged).

If we accumulate ≥5 bugs in `other` that share a pattern, promote them to a new named category (and update this file).

---

## Not-a-cross-language-bug (dropped in triage / annotation)

For completeness — reasons we *reject* a candidate:

- **Coincidental dual-touch.** A rename refactor that touches both languages but has no cross-language cause.
- **Docs-only.** A README update that mentions a field name in both `.java` and `.ts` code blocks.
- **Test-only.** Adding tests for existing behavior on both sides.
- **Merge / release / bump PRs.** No new bug, just tooling.
- **Config / build-only.** No code change that affects the running system.

These get skipped in annotation, not classified as `other`.

---

## Sub-boundary tags (`boundary_kind`)

Independent of category — every annotated bug also gets a boundary_kind:

- `rest` — REST/HTTP JSON boundary
- `grpc` — gRPC/Protobuf boundary
- `shared-file` — JSON/config file read by both sides (rare)
- `subprocess` — one side shells out to the other
- `ffi` — direct in-process interop (e.g., Java JNI to native code, React Native bridge)
- `other` — something else, with rationale
- `unknown` — couldn't determine from the PR

The React Native sub-population from Step 1.1 will mostly be `ffi`. Reporting it separately in the paper matters — it's a different failure surface than REST/gRPC.

---

## When to update this file

- If a boundary case pattern appears in ≥3 annotated bugs → add a "Boundary case" line here so future annotators handle it consistently.
- If a new category is proposed → add here first, THEN start using it in annotations. Never invent a category on the fly inside `bugs.jsonl`.
- Track substantive changes to this file in commits — the taxonomy version is a paper artifact.
