# Research method and coverage

Research date: **2026-09-19**. The workspace started empty. The result is a documentation collection and a small opt-in verification tool, not a deployed integration or a claim to have discovered every API.

## How services were found

1. Inspect the user-supplied AoE4 Replay Launcher and its three upstream services.
2. Follow provider documentation, GitHub organizations, client source and hosted API specifications.
3. Inspect the public JavaScript delivered by the official Age of Empires website for current route declarations and request shapes.
4. Use community protocol documentation as attributed implementation evidence, particularly where publishers do not provide a public contract.
5. Validate selected small read requests and inspect response structure, application status, response headers and content type.
6. Verify installed AoE4 SCAR documentation read-only to distinguish network APIs from local scripting interfaces.

Context7 was checked for an indexed AoE4 World reference but returned unrelated products; it was not used as evidence. Search-engine results were discovery leads. The resulting API claims cite provider-owned documentation/source, direct responses, or identified client/protocol implementations rather than generic API directories.

A follow-up reviewed the full LibreMatch repository tree and indexed its 172 endpoint-reference pages, including placeholders and broken navigation links. Its linked OpenAPI and AoE2 replay protobuf sources were inspected separately. These additions are source-only and did not increase the live-probe count. [Coverage and limitations](librematch.md), [fetch metadata](../evidence/2026-09-19/librematch-review.json).

The AoECenter follow-up inspected all five public repositories, indexing 17 SDK request builders and 48 model files. An offline check examined compressed fields in one saved public fixture; no SDK, collector, authentication helper or live-service request was run. [Findings](aoecenter.md), [coverage index](../catalog/aoecenter-coverage.json), [fetch and fixture evidence](../evidence/2026-09-19/aoecenter-review.json).

## Evidence levels

| Level | What it means | What it does not mean |
| --- | --- | --- |
| Provider-documented | Maintainer publishes a route/spec/example | Every current parameter combination was tested |
| Provider-client observed | Official/current website code declares or calls a route | A third-party compatibility/support guarantee |
| Implementation-documented | A named community client or protocol researcher describes it | Publisher endorsement or universal title support |
| Live response observed | The saved probe records a concrete request and response | The full provider API is healthy, complete, current or anonymous |
| Source-only / local-only | Code or installed references establish an interface | A running hosted service exists or was tested |
| Unresolved / legacy / retired | A specific uncertainty, error or provider retirement notice | A timeout alone proves shutdown |

In `catalog/endpoints.json`, `method:null` means a path declaration was found but no HTTP method is asserted. `verification.status:response-observed` can include an empty list. Read the linked probe and chapter before treating an endpoint as useful for a particular data requirement.

For a source declaring both GET and POST, `method` records the first listed method and `documented_methods` preserves both. `method:gRPC` identifies a protobuf RPC rather than an HTTP JSON route. The LibreMatch page index matches route casing only for cross-references; this does not assert server case-insensitivity.

## What was verified

The [verification report](../evidence/2026-09-19/README.md) lists all 47 endpoint probes. These were sequential, bounded, identified by a descriptive User-Agent and performed with TLS verification. Selected read-only POSTs match website data queries; no publisher state-changing POST was sent.

Evidence JSON includes request URLs/bodies through the manifest, timestamps, HTTP status, application result fields where available, byte counts, hashes, selected headers and sampled response shapes. Shapes inspect the first array item and have a depth bound; they are not exhaustive JSON Schemas. Non-personal discovery metadata is retained in full for leaderboard/race mapping. A single replay response was checked for its gzip/AoE4 signature without saving the recording.

Temporary response samples were used to inspect field meaning. The repository does not include complete player histories, profile lists, signed replay URLs, login tokens or downloaded game binaries. The replay route example identifies a public match, not a durable storage link.

## Validation limits

- Request success and useful data are separate. Some successful responses contained empty lists, zero/default values or only discovery metadata.
- No load testing, rate-limit saturation, bulk match crawl, private-account query, authenticated session creation, WebSocket subscription, or dataset bulk download was performed.
- CORS observations describe headers returned to one Origin. They are not a complete browser preflight/credential test.
- Numbers such as ladder counts, civilization enums and patch IDs are dated snapshots, not constants for new software.
- Static-data publication timestamps do not prove correspondence with the user’s installed patch.
- Parser source was read, not compiled or tested on all versions. The successful replay download was not played in the game.
- No claim of complete cross-platform coverage is inferred from a Steam-based example.
- Community reports of numerical limits were kept distinct from provider-published limits. The Guides quotas come from its live specification; a general World’s Edge or AoE4 World numerical quota was not established.
- An inspected source branch and a deployed API may differ; AoE4 Guides demonstrated this issue directly.

## Refreshing the research

Run `python3 scripts/probe.py --only <ids>` first to preview selected requests. Add `--live --output evidence/<new-name>.json` for a deliberate check. Existing evidence files cannot be overwritten by the tool. A 429 stops the run; the script does not automatically retry or rotate hosts.

Refresh provider specs and official frontend route declarations when request behavior changes. Record the new source revision/date and explain the discrepancy rather than silently rewriting an old observation as if it were never seen. Source/documentation changes should be accompanied by link/JSON validation, not automatic full-service crawling.

## Follow-up research

Concrete remaining gaps, ordered by likely usefulness:

1. Establish AoE4 World’s supported access path and data contract for detailed match summaries if an application needs build-order/economy timelines; avoid extrapolating from HTML pages.
2. Validate more AoE4 FFA, console/controller, event and team statistics combinations with known matching records; separate missing coverage from empty filters.
3. Test replay-parser compatibility with representative full-replay and summary versions in a local fixture set.
4. Establish the supported authentication flow for official mod catalog/account operations if needed; this pass recorded the anonymous 401 rather than guessing credentials.
5. Verify AoE2 Companion WebSocket message schemas and reconnect/subscription behavior for an actual overlay use case.
6. Expand AoE1, AoE2, AoE3 and Mythology from discovery to per-title joins, result enums, retention and record formats.
7. Investigate other community sites only where provider-owned API docs or explicit integration support exists; website functionality alone does not constitute a public API contract.
8. Clarify the maintenance/hosting status of legacy services, static AoE2 datasets and wrappers, plus Online/Mobile coverage.
9. Establish dataset and asset reuse terms for any intended redistribution or commercial product, using the relevant provider’s own terms.

None of these gaps prevents using the documented and tested public reads. They mark the boundary between this reference and a production integration built for a specific product.

## ageLANServer source-index methodology

The [ageLANServer review](agelanserver.md) follows literal route registrations and enclosing title conditions in a pinned source archive. Computed CDN paths, wrapped management handlers and local static-file routing were resolved separately; fallthroughs, TODOs and implicit HEAD behavior were excluded. No source was compiled or executed.

The source index counts method/path operations; the main atlas groups path patterns. Existing paths receive implementation references carrying exact source casing, method and emulator title set, without overwriting earlier live evidence or documented methods. Newly cataloged patterns belong to the local emulator service and remain `not-probed`; they do not establish new working publisher APIs. Tagged structs retain explicit Go tags but omit untagged/embedded/custom-codec expansion. Resource metadata contains hashes and top-level shapes, not full game-data snapshots.
