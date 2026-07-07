# Bug Annotation Stats

**Total PRs reviewed:** 50
**Confirmed cross-language bugs:** 12 (24%)
**Skipped:** 38 (76%)

## Confirmed bugs — by language pair

| Pair | Count |
|------|------:|
| java-ts | 7 |
| python-go | 5 |

## By primary category

| Category | java-ts | python-go | Total |
|----------|--------:|----------:|------:|
| `schema` | 3 | 3 | 6 |
| `coerce` | 2 | 1 | 3 |
| `nil` | 1 | 1 | 2 |
| `serde` | 0 | 0 | 0 |
| `async` | 1 | 0 | 1 |
| `other` | 0 | 0 | 0 |

## Secondary categories

- `schema`: 3

## By boundary_kind

| Boundary | java-ts | python-go | Total |
|----------|--------:|----------:|------:|
| `rest` | 3 | 1 | 4 |
| `grpc` | 0 | 4 | 4 |
| `ffi` | 4 | 0 | 4 |

## Category × boundary_kind (cross-tab)

| Category | ffi | grpc | rest |
|----------|----------|----------|----------|
| `schema` | 1 | 2 | 3 |
| `coerce` | 2 | 1 | 0 |
| `nil` | 0 | 1 | 1 |
| `serde` | 0 | 0 | 0 |
| `async` | 1 | 0 | 0 |
| `other` | 0 | 0 | 0 |

## Confirmed bugs per repo (top 10)

| Repo | Count |
|------|------:|
| [microcks/microcks](https://github.com/microcks/microcks) | 2 |
| [NativeScript/NativeScript](https://github.com/NativeScript/NativeScript) | 2 |
| [autokitteh/autokitteh](https://github.com/autokitteh/autokitteh) | 2 |
| [FormidableLabs/react-native-app-auth](https://github.com/FormidableLabs/react-native-app-auth) | 1 |
| [Cap-go/capacitor-updater](https://github.com/Cap-go/capacitor-updater) | 1 |
| [alibaba/nacos](https://github.com/alibaba/nacos) | 1 |
| [hatchet-dev/hatchet](https://github.com/hatchet-dev/hatchet) | 1 |
| [vllm-project/aibrix](https://github.com/vllm-project/aibrix) | 1 |
| [treeverse/lakeFS](https://github.com/treeverse/lakeFS) | 1 |

## Skip reasons (top 10)

| Reason | Count |
|--------|------:|
| feature | 17 |
| not-a-bug | 11 |
| not-cross-language | 7 |
| insufficient context | 2 |
| feature+integration | 1 |

## Representative examples per category (for §3.3)

### `schema` (6 bugs)

- **microcks/microcks#1765** (java-ts, `rest`): fix: swagger import fail because body parameter is not exist
  - Java enum `ParameterLocation` and TypeScript `ParameterLocation` in the service model must agree on valid values; missing `body` value caused IllegalArgumentException when importing Swagger specs that used body parameters. Fix adds the value to both enums simultaneously — a canonical shared-enum drift.
- **FormidableLabs/react-native-app-auth#886** (java-ts, `ffi`): Expose optional native error details for auth failures
  - Auth failures on Android/iOS produced only a generic `error.message` field visible to JS, with no way to access the native cause. Fix expands the error object contract to expose `error.nativeError` — a shared-contract expansion driven by the cross-language debuggability gap.

### `coerce` (3 bugs)

- **NativeScript/NativeScript#10862** (java-ts, `ffi`): fix(android): coerce string width/height in ImageAssetOptions
  - JS side passes width/height as strings; Android's `optInt()` returned 0 for numeric strings like "300", causing oversized decode operations. Fix adds `parsePositiveInt` on Android + coerces on TS side — a coerce bug at the JS↔Android JNI boundary.
- **Cap-go/capacitor-updater#801** (java-ts, `ffi`): fix: keep channel ids numeric
  - Backend returns numeric channel IDs but iOS Swift modeled them as `String?`; JSONDecoder failed before channels reached JS. Android and TS types were also inconsistent. Fix forces numeric IDs across Android, iOS, and TS — a coerce bug on the JS↔native FFI boundary where the wire format disagreed with each side's static type.

### `nil` (2 bugs)

- **microcks/microcks#1981** (java-ts, `rest`): Fix/add explain tracing to operation service errors
  - Failed operation-selection requests returned HTTP errors silently with no trace payload; the UI's live-traces graph received null trace data and had nothing to render. Fix populates trace data on the error path and the UI now consumes it — a nil across the REST boundary that only manifests when both sides participate.
- **autokitteh/autokitteh#1530** (python-go, `grpc`): fix: event_id is optional in dispatcher response
  - Dispatcher's `event_id` field was required but should be optional — with org-connections, multiple events are generated and the field is empty. Fix marks `event_id` optional in the proto and both language bindings — nullability mismatch across gRPC.

### `async` (1 bug)

- **NativeScript/NativeScript#11215** (java-ts, `ffi`): fix(android): update view imageSource when image is set asynchronously
  - Android async image-load completes without notifying the TS-side that `imageSource` is now populated. TS observer/property never fires. Fix propagates the async update across the FFI boundary.
