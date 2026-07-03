# Status: Sub-step 1.1 — GitHub Mining

**Last updated:** 2026-06-27
**Owner:** Sifat
**State:** 🟢 Done — pipeline complete, corpus produced

## Outcome

**145 polyglot repos accepted, both pairs over the 50-repo target.**

| Pair | Accepted | Median stars | Range |
|------|---------:|-------------:|------:|
| java-ts | 61 | 3,567 | 591 – 40,156 |
| python-go | 84 | 4,505 | 527 – 83,633 |

Full corpus: [`data/processed/repos.jsonl`](data/processed/repos.jsonl). Schema-validated against [`shared/schemas/repo.schema.json`](../../../shared/schemas/repo.schema.json). Human-readable summary: [`output/repo-summary.md`](output/repo-summary.md). Per-rejection log: [`output/rejected.jsonl`](output/rejected.jsonl) (2,227 candidates rejected with reasons — useful for tuning filters in future re-mining).

## What was built

- [pyproject.toml](../pyproject.toml) at step level: requests, pyyaml, jsonschema, python-dotenv, tenacity (Python 3.11+).
- [configs/queries.yaml](configs/queries.yaml) — 12 java-ts queries, 13 python-go queries, including one broad query per pair (`language:Java stars:>=1500`, `language:Go stars:>=2000`) that depends on enrichment-stage language filtering.
- Pipeline scripts under `scripts/`:
  - `search_repos.py` (paginated Search API with backoff)
  - `enrich_repos.py` (/languages + root contents, resumable, `--date` arg)
  - `filter_repos.py` (criteria + schema validation, `--include-non-permissive-license` flag)
  - `summarize.py` (generates the report)
- [scripts/README.md](scripts/README.md) documents the full pipeline.

## Decisions made during execution (logged for the paper)

1. **Test-marker check made informational.** Many monorepos (e.g., `pulumi/pulumi`) put test configs in sub-packages, not at root. CI presence is the real test signal, and we now treat root-level test markers as soft info, not a hard reject. Without this change, ~33 valid candidates were rejected by a heuristic gap.
2. **Python+Go language fraction relaxed from 5% → 2%.** Python+Go monorepos are inherently asymmetric: typically Go-dominant (server/infra) with a Python SDK or CLI. 5% would reject pulumi (10% Py — actually passes), milvus (21% Py), harbor (5.5% Py), and similar real polyglots. 2% captures the asymmetric reality without admitting noise.
3. **One broad query per pair added.** Topic-specific queries returned only 50–130 candidates total. Adding `language:Java stars:>=1500` and `language:Go stars:>=2000` brought the candidate pool to ~2,300, allowing the enrichment step to find polyglots that don't carry the right topic tags.

## Findings to feed into the workshop paper

- **Top java-ts polyglots are real enterprise applications**, not React Native bridges. Examples: `appsmithorg/appsmith`, `keycloak/keycloak`, `alibaba/nacos`, `conductor-oss/conductor`, `kestra-io/kestra`, `thingsboard/thingsboard`, `jhipster/generator-jhipster`, `pinpoint-apm/pinpoint`, `codecentric/spring-boot-admin`.
- **A small fraction of java-ts repos are still React Native libraries** (NativeScript, capacitor, etc.). These should be tagged in Step 1.2 — their cross-language bugs are *FFI-mediated* (Android JNI), not *REST-mediated*, which is a different category from our primary research target. Worth noting in the paper as a distinct sub-population.
- **Python+Go space is dominated by Go-primary projects with Python as SDK/tooling.** True symmetric python-go is rare (`infiniflow/ragflow` is the rare counter-example at 34% Py + 39% Go). This asymmetry will likely show up in the bug taxonomy — most cross-language bugs at this boundary will be Go-API-vs-Python-SDK contract drift, not symmetric request/response mismatches.

## Open items for Step 1.2 to handle

- **Triage tag for React Native vs REST/gRPC boundary.** Add a `boundary_kind` annotation field (already in [`shared/schemas/bug-annotation.schema.json`](../../../shared/schemas/bug-annotation.schema.json) — values: `rest | grpc | shared-file | subprocess | ffi | other | unknown`) and decide upfront how to weight FFI-bridge repos in the corpus.
- **Sampling strategy.** 145 repos × ~5 PRs/repo = ~725 candidate PRs to scan. The plan budget (5–15 min per bug annotation) implies we can realistically annotate ~100 PRs. Decision needed: stratified sample by stars / by pair, or random sample within categories.

## Artifacts produced

- `configs/queries.yaml` — committed, paper artifact.
- `data/raw/search-{java-ts,python-go}-2026-06-26.jsonl` — 977 + 1,395 records (gitignored, regenerable).
- `data/raw/enriched-{java-ts,python-go}-2026-06-26.jsonl` — same (gitignored).
- `data/processed/repos.jsonl` — **145 records, committed, schema-validated paper artifact.**
- `output/repo-summary.md` — committed paper artifact.
- `output/rejected.jsonl` — 2,227 records with reasons, committed.
- `output/search-full-2026-06-26.log`, `output/enrich-full-2026-06-26.log` — execution logs.

## Cost so far

~2,400 GitHub API calls. Free tier (5000/hr authenticated). No paid services.

## Next session (Step 1.2)

Start [`02-bug-extraction/`](../02-bug-extraction/CLAUDE.md). The input is `01-github-mining/data/processed/repos.jsonl`. First task: write `fetch_prs.py` per the sub-step's CLAUDE.md.
