# Age of Empires API atlas

A research reference for building Age of Empires tools, starting with **Age of Empires IV**. Researched and checked on **2026-09-19**. It covers hosted HTTP APIs, downloadable datasets, replay interfaces, platform APIs, and local modding libraries.

This is an independent catalog, not an official SDK. A service operated by Microsoft/World’s Edge can still expose an undocumented interface without a public compatibility guarantee. The endpoint inventory records that distinction and links observations to dated evidence.

This edition catalogs **30 services, datasets and tools**, **274 route/path patterns and RPCs**, and **55 sources**, with **47 recorded API/service probes**. Some entries are source-only, authenticated game operations, local libraries or retired-service references; these counts do not imply 274 working public endpoints.

The separate [documentation-discovery pass](docs/documentation-discovery.md) made **30 documentation/source-map requests**. It found readable publisher frontend source and vendor PlayFab schemas; these do not count as successful business-API probes.

## Publisher APIs and proof of operation

[Publisher services: origin and verification](docs/publisher-services.md) distinguishes **publisher/developer-operated**, **platform-vendor**, **independent/community**, and **unresolved** interfaces. An undocumented publisher endpoint can be described by community tools; operator attribution and documentation origin are separate.

The saved publisher checks cover **17 distinct route patterns: 16 with HTTP 200 samples and one with only a 401 rejection**. These came from **27 requests**, including alternate titles/hosts, repeated filters and one TLS failure. **No authenticated game-client, PlayFab, WebSocket or relay operation was runtime-tested.** Source review dates do not refresh the recorded 2026-09-19 request evidence. [Exact coverage and limits](docs/publisher-services.md#what-has-actually-been-tested), [machine-readable audit](catalog/verification-summary.json).

**Existing shared-backend reference:** [LibreMatch’s wiki](https://librematch.github.io/wiki/) already contains extensive protocol documentation. Our [LibreMatch coverage guide](docs/librematch.md) maps its 172 endpoint pages and linked OpenAPI specification to this atlas. Use it alongside the dated AoE4 checks and independent-provider research here.

[AoECenter’s SDK and tools](docs/aoecenter.md) add typed response models, compressed-field decoding code, fixtures and a collector example. The review distinguishes implemented requests from empty modules and records title-specific assumptions and source discrepancies.

[ageLANServer’s protocol implementation](docs/agelanserver.md) adds per-game route registrations, session WebSocket messages, PlayFab routes and positional serializers. Its emulator shortcuts and local-only routes are explicitly marked.

## Start here

| What you want | Best starting point | Why |
| --- | --- | --- |
| AoE4 player profiles, match history, ratings | [AoE4 World](docs/aoe4/aoe4world.md) | Documented, normalized JSON; public reads without a key |
| Raw leaderboards, profile resolution, lobbies | [World’s Edge community API](docs/shared/worlds-edge.md) | Upstream service; discovery endpoints and title-specific identifiers |
| AoE4 replay download URLs | [Replay interfaces](docs/aoe4/replays-and-local-apis.md) | `getReplayFiles` supplies expiring URLs; official website has a second retrieval route |
| Units, buildings, technologies, abilities, icons | [AoE4 World Data](docs/aoe4/static-data.md) | Static JSON and an openly inspectable data pipeline |
| Build orders and overlay instructions | [AoE4 Guides](docs/aoe4/build-orders.md) | Public REST API with OpenAPI schemas |
| Official website stats, ranked seasons, mods | [AgeOfEmpires.com interfaces](docs/shared/official-website.md) | Current website JavaScript reveals more than the older wrappers |
| Large-scale statistical research | [AoE4 World dumps](https://aoe4world.com/dumps), [other-game datasets](docs/other-games/overview.md) | Published exports avoid repeatedly crawling live APIs |
| In-game rules, units, objectives and events | [SCAR / Content Editor](docs/aoe4/replays-and-local-apis.md#scar-and-the-content-editor) | Local game scripting, with installed API documentation |
| Steam achievements, identity, player counts | [Platform and esports APIs](docs/shared/platforms-and-esports.md) | Complements game services; does not replace cross-platform match data |
| AoE1, AoE2, AoE3, Mythology and legacy games | [Other games](docs/other-games/overview.md) | Shared backend plus separate community services and tools |
| Game-client sessions, lobby notifications and title-specific routes | [ageLANServer](docs/agelanserver.md), [AoE4 route table](docs/aoe4/agelan-routes.md) | Pinned emulator source; distinguish implemented behavior from publisher API guarantees |
| AoE2 replay state streaming and viewer control | [CadeRemote gRPC](docs/other-games/aoe2-replay-grpc.md) | Local interface documented by LibreMatch; protobuf declarations inspected; runtime untested |

## Most useful findings

- **Publisher metadata is available beyond endpoint lists.** A public website source map reveals six additional route patterns and resolves fourteen mod methods. PlayFab publishes vendor Swagger schemas matching thirteen emulator routes, with meaningful authentication differences. [Discovery results and negative URL checks](docs/documentation-discovery.md).

- **AoE4 World is several resources:** normalized match/statistics API, static game data, bulk dumps, a replay parser, and an esports Elo endpoint. They have different schemas and access patterns.
- **AoE4 Guides has a host split.** Its website returns an explicit `not_proxied` error for `/api/builds`. Use the Cloud Run host listed in its Swagger specification for lists and favorites; individual builds are also proxied by the website. [Details and successful requests](docs/aoe4/build-orders.md).
- **Backend migration matters.** `aoe-api.worldsedgelink.com` and `dr-activerelease1-api.worldsedgelink.com` both answered tested AoE4 reads. The legacy `aoe-api.reliclink.com` request failed TLS hostname verification. Do not fix this by disabling TLS checks. [Host evidence](docs/shared/worlds-edge.md#hosts-and-game-titles).
- **HTTP 200 is insufficient.** World’s Edge has its own `result.code`; other endpoints can return an empty dataset, a game-level error, or HTML. The probe results preserve these distinctions.
- **There is no universal identifier.** Steam IDs, profile IDs, match IDs, stat-group IDs, leaderboard IDs, seasonal event IDs, game-kind strings, and civilization slugs need explicit mapping. [Identifier guide](docs/shared/identifiers.md).
- **AoE2.net is retired.** Its homepage explicitly announces that the website and API were sunset. Current alternatives include AoE2 Companion’s HTTP API, WebSocket streams and dumps, and aoestats’ weekly Parquet exports. [Other-game coverage](docs/other-games/overview.md).

## Documentation and machine-readable files

- [Publisher documentation discovery](docs/documentation-discovery.md), [source-map index](catalog/publisher-source-map.json), and [PlayFab vendor-schema comparison](catalog/playfab-spec-coverage.json)
- [Publisher services, operator categories and measured verification](docs/publisher-services.md)
- [Offline verification audit](catalog/verification-summary.json) and [reproducible audit script](scripts/audit_verification.py)
- [Research method, coverage and limitations](docs/research-method.md)
- [Source register and pinned revisions](docs/sources.md)
- [LibreMatch coverage map](docs/librematch.md) and [page-by-page index](catalog/librematch-coverage.json)
- [AoECenter implementation guide](docs/aoecenter.md) and [request/model index](catalog/aoecenter-coverage.json)
- [ageLANServer implementation guide](docs/agelanserver.md), [AoE4 route table](docs/aoe4/agelan-routes.md), and [route/event/resource index](catalog/agelanserver-coverage.json)
- [Endpoint inventory](catalog/endpoints.json): methods, paths, parameters, evidence and scope; **not** a generated promise of a complete OpenAPI contract
- [Service inventory](catalog/services.json): explicit operator attribution, access models and coverage
- [Selected request manifest](catalog/probes.json)
- [Dated verification report](evidence/2026-09-19/README.md), with response shapes, HTTP/application status and selected headers
- [AoE4 Guides provider OpenAPI snapshot](evidence/2026-09-19/aoe4guides-openapi.json)
- [Copyable HTTP requests](examples/requests.http)

The catalog includes documented but untested routes as well as successful probes. A successful sample says nothing about every player, every parameter combination, every platform, or future availability. See each entry’s verification information.

## Try a small request

```bash
curl --fail-with-body --get \
  'https://aoe4world.com/api/v0/players/4635035/games/last' \
  -H 'User-Agent: my-aoe-tool/0.1 (replace with your project/contact URL)'
```

For repeatable verification, the included Python script uses only the standard library and defaults to a dry run:

```bash
python3 scripts/probe.py --only world-profile,data-unit,guides-direct-status

# Explicitly sends three requests and writes a new evidence file:
python3 scripts/probe.py --only world-profile,data-unit,guides-direct-status \
  --live --output evidence/my-check.json
```

It sends requests sequentially, verifies TLS, uses a descriptive User-Agent, bounds response size, and stops on HTTP 429. Prefer a few selected probes over rerunning the entire manifest. Historical failing requests remain in the manifest so their observations are reproducible.

## Scope of this edition

AoE4 receives the detailed treatment. AoE1/2/3/Mythology have a discovery and integration index, with selected live checks. Legacy games, tournament platforms and local tooling are included where a concrete provider document or implementation could be found. Authenticated game-session interfaces are identified from source but were not logged into or exercised. No exhaustive crawl, private-account access, mod publication, or game configuration change was needed.
