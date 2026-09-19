# Publisher services: origin and verification

**Publisher/developer-operated** is the useful label here. It describes the service's origin, without implying an advertised public API, an official specification, third-party support, or verified behavior. Platform vendors and independent/community projects are separate categories.

For example, World’s Edge's `/community/…` routes belong to the **publisher backend**. LibreMatch is a **community source documenting that backend**. AoE4 World is an **independent API provider**. ageLANServer is an **independent emulator** of parts of publisher/vendor protocols. These are four different roles.

## What has actually been tested

The saved **2026-09-19** evidence contains **27 requests to publisher HTTP hosts**: **25 HTTP 200 responses**, **one HTTP 401**, and **one TLS/transport failure**. Repeated requests across filters, game titles and host aliases reduce that to **17 distinct route patterns attempted: 16 with an HTTP 200 sample and one with only an authentication rejection**.

There were **47 recorded requests across all providers**. The other 20 are outside this publisher-host audit; the 47 must not be described as 47 verified publisher APIs. Neither count includes source-document fetches as game API tests.

| Publisher API area | Cataloged patterns in this group | HTTP 200 sample | Error-only sample | No direct probe |
| --- | ---: | ---: | ---: | ---: |
| World’s Edge `/community/…` | 16 | 8 | 0 | 8 |
| World’s Edge `/game/…`, principally LibreMatch references | 88 | 0 | 0 | 88 |
| AgeOfEmpires.com website APIs | 42 | 8 | 1 | 33 |
| AgeOfEmpires.com account API | 1 | 0 | 0 | 1 |

These denominators describe the **current catalog groups**, not the full APIs. The ageLANServer-only additions remain separate: 41 upstream candidates (23 World’s Edge, 15 PlayFab, one website-family and two CDN paths), all without a direct probe. Its five local management/file helpers are not publisher API candidates. The emulator's 88 AoE4 game-router operations overlap other references; do not add every index count together.

**No authenticated game session, PlayFab title operation, WebSocket stream, BattleServer relay or local replay gRPC was runtime-tested.** The publisher ecosystem is partly mapped, not broadly runtime-validated. No percentage of the complete API can be established because the full endpoint set is unknown.

Counts are reproducible from the saved files using the [offline audit script](../scripts/audit_verification.py):

```bash
python3 scripts/audit_verification.py --check
```

The [machine-readable audit](../catalog/verification-summary.json) links every publisher attempt to its timestamp, host, method, path, title parameter, outcome and original evidence file. The provenance audit did **not** issue new API requests or refresh the original check dates. Subsequent [documentation discovery](documentation-discovery.md) made 30 documentation/source-map requests, and [alternative discovery](alternative-discovery.md) made 35 metadata requests. Vendor specifications were fetched separately. The CMS and Steam index responses are labeled `metadata-observed` and excluded from the original business-API audit above; their listed operations were not executed.

## The routes with direct evidence

All World’s Edge rows below had a successful AoE4 sample with `result.code=0`. Cross-title discovery and alternate-host samples are additional observations of the same route patterns. The legacy Relic hostname's TLS failure belongs to the discovery route and does not disprove the successful World’s Edge samples.

| Method | Publisher route | What was observed / important limit |
| --- | --- | --- |
| GET | `/community/achievement/getAvailableAchievements` | Achievement definitions; not proof of achievement grant/sync behavior. [Evidence](../evidence/2026-09-19/extended-probes.json) |
| GET | `/community/advertisement/findAdvertisements` | Lobby response; not a test of hosting, joining or live gameplay. [Evidence](../evidence/2026-09-19/extended-probes.json) |
| GET | `/community/leaderboard/getAvailableLeaderboards` | Leaderboard, match-type and civilization metadata; successful discovery also recorded for AoE1/2/3 and Mythology. [Evidence](../evidence/2026-09-19/initial-probes.json) |
| GET | `/community/leaderboard/getLeaderBoard2` | Leaderboard/stat-group response; one selected ladder/page, not every ladder. [Evidence](../evidence/2026-09-19/extended-probes.json) |
| GET | `/community/leaderboard/getMatchHistory` | Lookup of a known public match by ID. [Evidence](../evidence/2026-09-19/extended-probes.json) |
| GET | `/community/leaderboard/getPersonalStat` | Personal statistics for one profile; not complete cross-platform identity coverage. [Evidence](../evidence/2026-09-19/initial-probes.json) |
| GET | `/community/leaderboard/getRecentMatchHistory` | Recent match history for one profile; retention and full pagination not established. [Evidence](../evidence/2026-09-19/initial-probes.json) |
| GET | `/community/leaderboard/getReplayFiles` | Replay-file metadata including expiring URLs; not a guarantee of availability for every match. [Evidence](../evidence/2026-09-19/followup-probes.json) |
| POST | `/api/GameStats/AgeIV/GetFullStats` | HTTP 200 and application status 0; some career/embedded-match fields were zero or empty. [Evidence](../evidence/2026-09-19/official-probes.json) |
| POST | `/api/GameStats/AgeIV/GetMatchDetail` | HTTP 200 and application status 0; identifier fields had inconsistencies requiring care. [Evidence](../evidence/2026-09-19/official-probes.json) |
| POST | `/api/GameStats/AgeIV/GetMatchList` | Unfiltered sample empty; filtered sample populated; requested recordCount did not establish page-size semantics. [Evidence](../evidence/2026-09-19/targeted-probes.json) |
| GET | `/api/GameStats/AgeIV/GetMatchReplay/` | Gzip attachment with an AoE4 replay signature; full parsing and game playback untested. [Evidence](../evidence/2026-09-19/official-probes.json) |
| POST | `/api/ageiv/EventLeaderboard` | Seasonal leaderboard response with a discovered leaderboard ID. [Evidence](../evidence/2026-09-19/targeted-probes.json) |
| GET | `/api/ageiv/EventList` | Season/event discovery; event IDs and leaderboard IDs differ. [Evidence](../evidence/2026-09-19/extended-probes.json) |
| POST | `/api/ageiv/Leaderboard` | Leaderboard response; sorting fields changed which row was returned. [Evidence](../evidence/2026-09-19/official-probes.json) |
| POST | `/api/v4/mods/Find` | HTTP 401 with unauthenticated-user error: access rejection established, successful mod search unverified. [Evidence](../evidence/2026-09-19/official-probes.json) |
| GET | `/api/v4/mods/Games` | Anonymous game-list discovery only. [Evidence](../evidence/2026-09-19/extended-probes.json) |

A timestamped response is stronger evidence of deployment than a route in an old repository, but it still does not prove a complete contract. The evidence retains request parameters/bodies in the manifest, HTTP/application status, selected headers, response shapes and hashes. It is not a complete response corpus or a full schema-conformance suite. Some successful responses were empty/default-valued, and only selected combinations were checked.

## Read three properties independently

| Property | Question it answers | Examples |
| --- | --- | --- |
| **Operator/origin** | Who supplies this service or interface? | Publisher/developer, platform vendor, independent/community, unresolved |
| **Evidence origin** | Where did this route/schema claim come from? | Provider frontend/specification, independent client, community protocol research, emulator, direct response |
| **Runtime verification** | What did we actually observe, and when? | HTTP 200 sample, authentication rejection, transport failure, no probe |

A publisher endpoint documented only by a community project remains **publisher-operated, community-described, untested**. A community API with maintainer documentation and a successful response remains **independent, provider-documented, sample-tested**. The word “provider” in a source record means the provider of that particular service/tool; it does not automatically mean Microsoft or a game developer.

The labels deliberately make no inference from a recent commit to live compatibility. A copied fixture, passing mock test or complete-looking function signature can be stale or wrong. Multiple clients repeating the same literal are corroborating references, not multiple live verifications. An emulator may reproduce enough behavior for local play while deliberately replacing real data with constants or errors.

## Operator index

`catalog/services.json` records `operator.category`, a descriptive label, attribution basis and supporting source IDs for every service/tool. Categories indicate the evidenced role; exact legal ownership and subcontractor responsibilities were not audited. A commercial third party is not automatically a publisher/developer service, and a claimed game partnership needs its own supporting evidence.

| Service or interface | Operator category | Attribution / boundary |
| --- | --- | --- |
| [AgeOfEmpires.com account service](shared/official-website.md) | Publisher/developer | Account-status call established in publisher frontend source; runtime untested |
| [AgeOfEmpires.com CMS](alternative-discovery.md#publisher-website-an-actual-route-catalog) | Publisher/developer | Live WordPress route index on the publisher website; content operations untested |
| [AgeOfEmpires.com website APIs](shared/official-website.md) | Publisher/developer | Age of Empires publisher website |
| [SCAR / Content Editor](aoe4/replays-and-local-apis.md) | Publisher/developer | AoE4 game and Content Editor |
| [World’s Edge / Relic game services](shared/worlds-edge.md) | Publisher/developer | Age of Empires / World’s Edge / Relic backend family |
| [PlayFab game-client services](shared/platforms-and-esports.md) | Platform vendor | Microsoft PlayFab |
| [Steam Web API](shared/platforms-and-esports.md) | Platform vendor | Valve / Steam |
| [AOEMods.Essence](aoe4/replays-and-local-apis.md) | Independent/community | AOEMods.Essence project/provider |
| [AndyTheNerd AoE2 API](other-games/overview.md) | Independent/community | AndyTheNerd AoE2 API project/provider |
| [AoE2 Companion](other-games/overview.md) | Independent/community | AoE2 Companion project/provider |
| [AoE2 Tech Tree](other-games/overview.md) | Independent/community | AoE2 Tech Tree project/provider |
| [AoE2.net](other-games/overview.md) | Independent/community | AoE2.net project/provider |
| [AoE4 Guides](aoe4/build-orders.md) | Independent/community | AoE4 Guides project/provider |
| [AoE4 World](aoe4/aoe4world.md) | Independent/community | AoE4 World project/provider |
| [AoE4 World Data](aoe4/static-data.md) | Independent/community | AoE4 World Data project/provider |
| [AoE4 World datasets](aoe4/aoe4world.md) | Independent/community | AoE4 World datasets project/provider |
| [AoE4 World summary parser](aoe4/replays-and-local-apis.md) | Independent/community | AoE4 World summary parser project/provider |
| [AoECenter Relic SDK](aoecenter.md) | Independent/community | AoECenter Relic SDK project/provider |
| [AoECenter Relic Store](aoecenter.md) | Independent/community | AoECenter Relic Store project/provider |
| [AoECenter Relic Token](aoecenter.md) | Independent/community | AoECenter Relic Token project/provider |
| [AoEIV.net](other-games/overview.md) | Independent/community | AoEIV.net project/provider |
| [AoM.gg](other-games/overview.md) | Independent/community | AoM.gg project/provider |
| [Liquipedia LPDB](shared/platforms-and-esports.md) | Independent/community | Liquipedia LPDB project/provider |
| [Voobly](shared/platforms-and-esports.md) | Independent/community | Voobly project/provider |
| [aalises classic AoE2 API](other-games/overview.md) | Independent/community | aalises classic AoE2 API project/provider |
| [ageLANServer protocol implementation](agelanserver.md) | Independent/community | ageLANServer protocol implementation project/provider |
| [amrtgaber AoE2 Data API](other-games/overview.md) | Independent/community | amrtgaber AoE2 Data API project/provider |
| [aoc-mgz](other-games/overview.md) | Independent/community | aoc-mgz project/provider |
| [aoestats](other-games/overview.md) | Independent/community | aoestats project/provider |
| [openage](other-games/overview.md) | Independent/community | openage project/provider |
| [AoE2 DE CadeRemote replay interface](other-games/aoe2-replay-grpc.md) | Unresolved | AoE2 game-client / CaptureAge-related replay interface |

The local AoE2 `CadeRemote` interface is kept unresolved for precise operator/partner attribution: its current evidence is community protocol/protobuf research, not a maintainer statement establishing the implementation boundary. Its apparent game-client role and runtime verification are separate questions. SCAR, by contrast, has publisher documentation and installed API-reference evidence, but no scripting-runtime test in this research.

PlayFab is a platform/vendor service. The association of particular PlayFab titles with AoE4/Mythology in this atlas comes from community implementation source, and their deployment behavior has not been tested. Generic platform documentation would not by itself verify the game's particular configuration. [Vendor Swagger evidence](documentation-discovery.md#playfabs-vendor-published-swagger) supplies generic contract references for 13 emulator paths; the [custom JSON format](alternative-discovery.md#playfab-custom-json-closes-the-two-contract-gaps) covers all 15. Runtime status is unchanged.

## Machine-readable interpretation

- Each endpoint's `service` resolves to an operator record. Existing `verification.status` values remain intact; no source-only item was promoted to a live-verified item.
- `evidence_basis` exposes the kinds of sources attached to the endpoint. Direct request evidence is marked separately from provider or independent source code.
- `last_recorded_probe_at`, where present, dates the selected saved sample. The audit preserves all publisher attempts, including alternate hosts and failures.
- `upstream_candidate` links 41 independent-emulator entries to the publisher/vendor family they may reproduce. It does **not** relabel the emulator as publisher-operated or confirm the corresponding deployed route.
- A GET registration or source declaration does not prove anonymous access. A 401 proves rejection of the submitted request, not a functioning authenticated endpoint.

## Most useful verification work still missing

1. Test the remaining documented publisher public reads with small, well-understood inputs; record application errors and empty results as such.
2. Trace the AoE4 login/session lifecycle in multiple implementations, identifying build/platform requirements and which claims still need authorized runtime tests.
3. Validate authenticated response layouts and WebSocket notifications against the relevant game build, rather than inferring correctness from emulator serializers.
4. Trace replay/cloud storage, mod account flows and publisher frontend consumers to concrete requests and schemas.
5. Apply recursive GitHub domain-usage searches to publisher/backend hosts, recording new candidates separately from tested routes.

The immediate benefit of this classification is that research leads stay visible without being presented as proven integrations.
