# Bug Annotation Stats

**Total PRs reviewed:** 100
**Confirmed cross-language bugs:** 19 (19%)
**Skipped:** 81 (81%)

## Confirmed bugs — by language pair

| Pair | Count |
|------|------:|
| java-ts | 10 |
| python-go | 9 |

## By primary category

| Category | java-ts | python-go | Total |
|----------|--------:|----------:|------:|
| `schema` | 3 | 4 | 7 |
| `coerce` | 2 | 2 | 4 |
| `nil` | 3 | 1 | 4 |
| `serde` | 0 | 1 | 1 |
| `async` | 2 | 1 | 3 |
| `other` | 0 | 0 | 0 |

## Secondary categories

- `schema`: 4

## By boundary_kind

| Boundary | java-ts | python-go | Total |
|----------|--------:|----------:|------:|
| `rest` | 3 | 2 | 5 |
| `grpc` | 0 | 4 | 4 |
| `ffi` | 6 | 2 | 8 |
| `other` | 1 | 1 | 2 |

## Category × boundary_kind (cross-tab)

| Category | ffi | grpc | other | rest |
|----------|----------|----------|----------|----------|
| `schema` | 1 | 2 | 0 | 4 |
| `coerce` | 3 | 1 | 0 | 0 |
| `nil` | 2 | 1 | 0 | 1 |
| `serde` | 0 | 0 | 1 | 0 |
| `async` | 2 | 0 | 1 | 0 |
| `other` | 0 | 0 | 0 | 0 |

## Confirmed bugs per repo (top 10)

| Repo | Count |
|------|------:|
| [microcks/microcks](https://github.com/microcks/microcks) | 2 |
| [NativeScript/NativeScript](https://github.com/NativeScript/NativeScript) | 2 |
| [autokitteh/autokitteh](https://github.com/autokitteh/autokitteh) | 2 |
| [go-python/gopy](https://github.com/go-python/gopy) | 2 |
| [FormidableLabs/react-native-app-auth](https://github.com/FormidableLabs/react-native-app-auth) | 1 |
| [Cap-go/capacitor-updater](https://github.com/Cap-go/capacitor-updater) | 1 |
| [alibaba/nacos](https://github.com/alibaba/nacos) | 1 |
| [hatchet-dev/hatchet](https://github.com/hatchet-dev/hatchet) | 1 |
| [vllm-project/aibrix](https://github.com/vllm-project/aibrix) | 1 |
| [treeverse/lakeFS](https://github.com/treeverse/lakeFS) | 1 |

## Skip reasons (top 10)

| Reason | Count |
|--------|------:|
| feature | 31 |
| not-cross-language | 25 |
| not-a-bug | 21 |
| insufficient context | 3 |
| feature+integration | 1 |

## Representative examples per category (for §3.3)

### `schema` (7 bugs)

- **microcks/microcks#1765** (java-ts, `rest`): fix: swagger import fail because body parameter is not exist
  - Java enum `ParameterLocation` and TypeScript `ParameterLocation` in the service model must agree on valid values; missing `body` value caused IllegalArgumentException when importing Swagger specs that used body parameters. Fix adds the value to both enums simultaneously — a canonical shared-enum drift.
- **FormidableLabs/react-native-app-auth#886** (java-ts, `ffi`): Expose optional native error details for auth failures
  - Auth failures on Android/iOS produced only a generic `error.message` field visible to JS, with no way to access the native cause. Fix expands the error object contract to expose `error.nativeError` — a shared-contract expansion driven by the cross-language debuggability gap.

### `coerce` (4 bugs)

- **NativeScript/NativeScript#10862** (java-ts, `ffi`): fix(android): coerce string width/height in ImageAssetOptions
  - JS side passes width/height as strings; Android's `optInt()` returned 0 for numeric strings like "300", causing oversized decode operations. Fix adds `parsePositiveInt` on Android + coerces on TS side — a coerce bug at the JS↔Android JNI boundary.
- **Cap-go/capacitor-updater#801** (java-ts, `ffi`): fix: keep channel ids numeric
  - Backend returns numeric channel IDs but iOS Swift modeled them as `String?`; JSONDecoder failed before channels reached JS. Android and TS types were also inconsistent. Fix forces numeric IDs across Android, iOS, and TS — a coerce bug on the JS↔native FFI boundary where the wire format disagreed with each side's static type.

### `nil` (4 bugs)

- **microcks/microcks#1981** (java-ts, `rest`): Fix/add explain tracing to operation service errors
  - Failed operation-selection requests returned HTTP errors silently with no trace payload; the UI's live-traces graph received null trace data and had nothing to render. Fix populates trace data on the error path and the UI now consumes it — a nil across the REST boundary that only manifests when both sides participate.
- **autokitteh/autokitteh#1530** (python-go, `grpc`): fix: event_id is optional in dispatcher response
  - Dispatcher's `event_id` field was required but should be optional — with org-connections, multiple events are generated and the field is empty. Fix marks `event_id` optional in the proto and both language bindings — nullability mismatch across gRPC.

### `serde` (1 bug)

- **infiniflow/ragflow#16468** (python-go, `other`): Fix: ValueError: too many values to unpack in list_tenant_added_models for model IDs containing '@' (#16467)
  - The shared composite model-key format `model_name@instance_name@provider_name` was parsed independently by Python (`.split('@')`) and Go with the same brittle assumption; LM-Studio model names containing `@` broke both parsers with `too many values to unpack`. Fix hardens the parser on both sides to use right-anchored parsing. Serialization-format brittleness in a format shared across the polyglot boundary.

### `async` (3 bugs)

- **NativeScript/NativeScript#11215** (java-ts, `ffi`): fix(android): update view imageSource when image is set asynchronously
  - Android async image-load completes without notifying the TS-side that `imageSource` is now populated. TS observer/property never fires. Fix propagates the async update across the FFI boundary.
- **DataLinkDC/dinky#4160** (java-ts, `other`): [Bug-4149] Bug fix for web socket session do not closed correctly and page stuck caused by it
  - Frontend WebSocket close condition was wrong and backend never set max-idle-timeout on sessions; sessions accumulated on server side while frontend thought they were closed, eventually stalling the page. Fix on both sides. Async/lifecycle mismatch across the WS boundary.
