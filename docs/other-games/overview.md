# Beyond AoE4

This edition verifies selected discovery routes across the series and records concrete provider documentation. It is a starting index, not the same depth of validation as the AoE4 chapters.

## Shared publisher services

| Game | Verified discovery request | Other source-backed interfaces |
| --- | --- | --- |
| AoE: Definitive Edition | Common World’s Edge host, `title=age1`; 4 ladder entries | Official `/api/v2/agede/Leaderboard`; mod game ID 1 |
| AoE II: Definitive Edition | Common host, `title=age2`; 17 ladder entries | Official `/api/v2/ageii/Leaderboard`; `GameStats/AgeII` paths; mod game ID 2 |
| AoE III: Definitive Edition | Common host, `title=age3`; 7 ladder entries | Official `/api/ageiii/Leaderboard`; mod game ID 3 |
| AoE IV | Common/newer hosts, `title=age4`; detailed coverage elsewhere | Website `ageiv`/`GameStats/AgeIV`; mod game ID 4 |
| Age of Mythology: Retold | `athens-live-api.worldsedgelink.com`, `title=athens`; 9 ladder entries | Official `/api/agemyth/Leaderboard`; mod game ID 1001 |

Counts are from dated discovery metadata and may include inactive/special/internal ladders. They do not establish complete history support or data freshness. Cross-game website leaderboard paths were found in the official frontend but only AoE4 website stats were exercised. [World’s Edge reference](../shared/worlds-edge.md), [official frontend reference](../shared/official-website.md), [evidence](../../evidence/2026-09-19/README.md).

## AoE2 Companion: HTTP, WebSockets and exports

**HTTP base:** `https://data.aoe2companion.com`  
**WebSocket base:** `wss://socket.aoe2companion.com`  
**Provider examples:** [denniske/aoe2companion-api](https://github.com/denniske/aoe2companion-api), a Bruno request collection  
**Provider usage notes:** [application API page source](https://github.com/denniske/aoe2companion/blob/89c8b2e6242c6bb436aa49544da3a72d1bc112a5/src/app/%28main%29/more/api.tsx)

| Interface | Evidence / use |
| --- | --- |
| `GET /api/leaderboards` | Live JSON success; 13 entries in the sample; provider-specific ladder identifiers |
| `GET /api/profiles/{profileId}` | Provider client/examples; optional `extend=stats`, `language`, `page` in the Bruno example |
| `GET /api/profiles` | Provider examples for name search or profile IDs; inspect the collection for exact current filters |
| `GET /api/matches`, `/api/matches/{matchId}` | Provider client and examples; not exercised here |
| `GET /api/matches/{matchId}/analysis` | Client-source path; availability/permissions untested |
| `GET /api/dump/list` | Live success; provider-published dump listing |
| `wss://socket.aoe2companion.com/listen?handler=ongoing-matches&profile_ids=196240` | Exact provider WebSocket example; stream was not opened here |
| Other WebSocket examples | Lobbies; ongoing matches; match started/updated/finished; filters by profile/match IDs or verification |

Source for HTTP routes: [client implementation](https://github.com/denniske/aoe2companion/blob/89c8b2e6242c6bb436aa49544da3a72d1bc112a5/src/api/helper/api.ts). The [pinned Bruno collection](https://github.com/denniske/aoe2companion-api/tree/7861ccb8c986dbbf57052e66c9427a2fea0917d5) is the strongest place to start for a new integration.

The provider asks for a project URL in User-Agent, responsible use and bulk dumps instead of API crawling. It specifically recommends WebSockets for overlays. The notes link daily leaderboard/profile CSV and Parquet files and date-partitioned match Parquet exports at `dump.cdn.aoe2companion.com`. No bulk exports were downloaded and no numeric quota was established. An HTTP 403 at the data host’s root did **not** imply its API was unavailable: the two specific API probes succeeded.

## aoestats: AoE2 statistics and weekly Parquet dumps

[Provider API/data documentation](https://aoestats.io/api-info/) publishes `GET https://aoestats.io/api/db_dumps`, which succeeded in this check. It lists weekly exports with `matches.parquet` and `players.parquet` files, partitioned by date range.

The published data model includes match IDs, maps, timestamps, Elo, game types, patch, and replay-enhancement flags. Replay-enhanced player rows can contain age-up timings, openings and replay-derived summaries. The provider warns that cleaning is still needed; fields derived from replays are not guaranteed for every match. Only index availability was verified, not dataset completeness. This is a better evidenced bulk-research path than assuming every aoestats website chart is a supported REST endpoint. [Documentation](https://aoestats.io/api-info/).

## Static AoE2 data

| Source | Type and status |
| --- | --- |
| [SiegeEngineers/aoe2techtree](https://github.com/SiegeEngineers/aoe2techtree) | Static data and tech-tree website source; includes a Return of Rome contribution. Prefer versioned source files for reproducible lookup |
| [AndyTheNerd/age-of-empires-II-api](https://github.com/AndyTheNerd/age-of-empires-II-api) | Hosted static-data API at `https://aoe2api.teamrespawntv.com`; single-civ request succeeded |
| [aalises/age-of-empires-II-api](https://github.com/aalises/age-of-empires-II-api) | Classic Age of Kings/Conquerors-oriented API source; widely linked old Heroku URLs are not evidence of current hosting |
| [amrtgaber/aoe2-data-api](https://github.com/amrtgaber/aoe2-data-api) | Open-source NestJS/Swagger static-data service and data-generation approach; hosted availability not tested |

The AndyTheNerd provider documents these GET routes:

```text
/civilizations       /civilization/{id-or-name}
/units               /unit/{id-or-name}
/structures          /structure/{id-or-name}
/technologies        /technology/{id-or-name}
```

`/civilization/britons` returned JSON. Its README’s civilization-number range is 1–33: **do not infer full current-DE/DLC coverage** from successful hosting. Match the dataset’s edition/patch to your use case. This family exposes game definitions rather than online player results. [Provider README](https://github.com/AndyTheNerd/age-of-empires-II-api/blob/master/README.md).

## Replay and scenario libraries

[Python `mgz` / aoc-mgz](https://github.com/happyleavesaoc/aoc-mgz) parses and summarizes AoE2 recordings. Its README distinguishes parser/model/summary support across Age of Kings, Conquerors, UserPatch, HD and DE versions. Treat the support matrix and file format version as dependencies; “supports DE” does not guarantee every patch. This is a local library, not a hosted player-history API.

[LibreMatch’s CadeRemote gRPC reference](aoe2-replay-grpc.md) adds a separate replay-viewing interface: five RPCs for version information, pause, fog of war, perspective and a stream of state deltas/events/recorded commands. The linked protobuf declarations were checked; no local game connection was attempted. The Delta Play Replay project builds on that protocol, and its future-format goals should not be read as established AoE4 support.

[openage](https://github.com/SFTtech/openage) is an independent engine project with a [nyan/modding API](https://blog.openage.dev/d14-openage-modding-api-finale.html). Its API belongs to that engine, not the installed Microsoft game client. It is relevant for engine/data research but does not provide a back door into the live DE simulation.

## Mythology: Retold

AoM.gg’s [published collector](https://github.com/erin-fitzpatric/aom-lambda/blob/ee51b41da4a60fcfe066ca5894e7e09849d3e6a5/extract-leaderboard/app.mjs) supplies a concrete upstream example: Athens host with `title=athens`. The [website repository](https://github.com/erin-fitzpatric/next-aom-gg) describes its own database, replay uploads and signed downloads. Those website features alone do not establish a supported public AoM.gg API.

[Aomstats](https://aomstats.io/) is a further statistics lead. A public integration contract was not established in this pass. Newer `andromeda` backend hosts are documented by [ageLANServer](https://github.com/luskaner/ageLANServer/wiki/Questions-and-Answers-%28QA%29); their exact active release and compatibility with Athens discovery remain untested.

## Legacy, retired and unresolved services

| Name | What can be said confidently |
| --- | --- |
| [AoE2.net](https://aoe2.net/) | Provider homepage explicitly says the website and API were sunset. Do not build a new integration around old `/api/player/...` examples |
| `aoeiv.net` | Historically used by AoE4 wrappers; the root request timed out during this check. This is an observation, not proof of permanent retirement |
| `aoe-api.reliclink.com` | Legacy hostname failed TLS verification; World’s Edge host worked |
| [Voobly](https://www.voobly.com/pages/view/147/External-API-Documentation) | Legacy-platform API documentation exists; current request/access details not validated |
| AoE2 Insights | Rich website and replay analysis, but this research did not establish a supported general public API contract |
| AoE3-specific community sites | No additional independently verified public contract established here beyond the shared backend and website route |
| Age of Empires Online / Mobile | No verified relevant public integration contract established in this pass; absence from the catalog is not proof of absence |

No claim is made that this is every existing API. The [research backlog](../research-method.md#follow-up-research) records the meaningful remaining gaps, especially edition-specific schemas, authenticated services, and community sites without provider-owned API documentation.

## Per-title game-client protocol implementation

[ageLANServer](../agelanserver.md) registers different HTTP methods and paths for AoE1/2/3/4 and Mythology, and adds PlayFab-facing routes for AoE4/Mythology. Its [coverage index](../../catalog/agelanserver-coverage.json) records every route’s title conditions. The source also constructs `andromeda-live-release{N}-api.worldsedgelink.com` and references the AoE2 macOS host `arthurlive-api.worldsedgelink.com`; neither was enumerated or probed in this follow-up. Local emulator behavior is not a publisher API guarantee.
