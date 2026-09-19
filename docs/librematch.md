# LibreMatch: existing reference and coverage map

[LibreMatch’s wiki](https://github.com/librematch/wiki) is a substantial existing reference for the shared Age of Empires backend. Use its [rendered documentation](https://librematch.github.io/wiki/) for browsing and its [pinned source](https://github.com/librematch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419) for reproducibility. The complete repository tree was checked on 2026-09-19, at the same revision used by the initial atlas.

The initial atlas used its community endpoint pages but underrepresented the rest of the project. This follow-up indexes **172 endpoint-reference pages** and follows the linked OpenAPI and replay-protocol projects. It also corrects the atlas’s news route to `/community/news/getNews`.

## What is covered upstream

| Wiki area | Coverage found | How to use it |
| --- | --- | --- |
| [`src/rlink/community`](https://github.com/librematch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community) | 16 endpoint pages | Public-read starting point: stats, replays, lobbies, achievements, clans, inventory, events, news, Steam proxy |
| [`src/rlink/game`](https://github.com/librematch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/game) | 88 endpoint pages | Mostly session-bound game-client operations; many examples are AoE2-specific; includes explicit incomplete templates |
| [`src/aoe`](https://github.com/librematch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/aoe) | 68 endpoint pages, 56 of which have only headings or short placeholder text | Historical website route leads; combine with current frontend source and live evidence |
| [`src/grpc`](https://github.com/librematch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/grpc) | AoE2 replay-viewing RPCs, protocol messages, binary delta format, rendering metadata | A separate local replay interface, with five RPCs confirmed in the linked `.proto` source |
| [`src/librematch/design`](https://github.com/librematch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/librematch/design) | Collector, storage, API, matchmaking and subscription designs | Architecture proposals; their presence does not establish deployed public services |

The [machine-readable coverage map](../catalog/librematch-coverage.json) gives every endpoint page’s pinned URL, declared method/path where present, documentation gaps, matching atlas entry, and source-only status. Counts exclude section README files. Placeholder classification is explicit in the file; it is not a judgment that the referenced operation does not exist.

## The linked OpenAPI is especially useful

The wiki links to [`librematch-rlink_client/openapi.yaml`](https://github.com/librematch/librematch-rlink_client/blob/a1227c74a6990db9d9bc0e33c83a502773084178/openapi.yaml). The inspected revision declares OpenAPI **3.0.3**, API-info version **24.11.01**, **102 paths**, and **105 HTTP operations**. Three paths declare both GET and POST.

It describes parameter names, types, request locations, and query-based `connect_id`/`sessionID` security schemes. This is useful for client generation and request inspection. However, it has **no named response schemas**: many responses use an unconstrained JSON schema. Generated clients therefore do not automatically provide strongly typed match/player models. The specification also lacks the wiki’s newer community `getMatchHistory` and `getReplayFiles` paths. [Pinned specification](https://github.com/librematch/librematch-rlink_client/blob/a1227c74a6990db9d9bc0e33c83a502773084178/openapi.yaml).

The spec and wiki are community protocol research, not a publisher-maintained compatibility contract. Keep observed title/build differences in the atlas; do not overwrite successful AoE4 observations with an older AoE2 example. No generated client or Steam-auth helper was installed or executed in this follow-up.

## Additional backend coverage

The endpoint catalog now indexes all 88 game-route pages, linking their individual source pages and recording methods and parameter names where available. Important families include:

| Family | Examples / purpose |
| --- | --- |
| Account and login | Profile lookup, platform-ID resolution, session creation/read/logout |
| Advertisement and observation | Available/observable lobbies, individual lobby lookup, spectator session lifecycle |
| Automatch | Map-pool discovery and matchmaking polling/state |
| Cloud and party | File URL lookup, temporary credentials, replay-upload finalization, match reporting |
| Leaderboard | Party stats, stat groups, single-player history, profile-name queries |
| Challenge, achievement, events, items | Progression, inventory, definitions, prices and event metadata |
| Clan, invitations, relationships, chat | Social/account operations, including mutations |

These additional operations are **source-only**. The presence of a route name does not establish anonymous access, AoE4 support, or current functionality. The wiki generally labels `/game` as authenticated, but identifies some exceptions; authentication is recorded per source where available. The follow-up made no game-service requests and did not exercise writes.

The missing community endpoint was [`/community/external/proxysteamuserrequest`](https://github.com/librematch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community/external/proxysteamuserrequest.md). It describes Steam-profile enrichment through the game service. Its example uses `profileNames`, while its table says `profile_names`; the OpenAPI uses `profileNames`. Preserve that discrepancy until a specific request is verified. The wiki’s claim that arbitrary Steam paths can be proxied was not independently tested.

The [root reference](https://github.com/librematch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/README.md) also records the replay link `https://aoe.ms/replay/?gameId=...&profileId=...`. Its example is AoE2-oriented; do not assume it is an AoE4 replacement for the verified replay routes. The [website overview](https://github.com/librematch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/aoe/README.md) supplies another useful lead: `https://cdn.ageofempires.com/aoe/rl-server-status.json`. Neither lead was live-tested here.

## Gaps and contradictions worth retaining

- **Navigation can overstate coverage.** The community index has two links to nonexistent files; the game index has 18. For example, its community `getStatGroupsByProfileIDs` page is missing, while an actual page exists under `/game/Leaderboard/`. The coverage map records these broken links without inventing endpoints from them.
- **Some pages are templates.** The game `getChallengeProgressByProfileID` and `getPersonalStat` pages explicitly lack request, parameter and response content. They remain indexed as leads, with the missing detail flagged.
- **The website section is uneven.** The AoE4 `getmatchdetail` page is a short label, while current official JavaScript and our live check establish `/api/GameStats/AgeIV/GetMatchDetail`. A wiki filename is insufficient to reconstruct a current request URL.
- **Case and names vary.** Source casing is preserved; case-insensitive matching is used only to cross-reference catalog entries, not as a claim that servers accept arbitrary casing. Historical `/mods/PublishFile` is not automatically equivalent to the current frontend’s `/mods/CheckAndPublishFile`.
- **Usage numbers are community reports.** The wiki reports different limits for community, game and replay services. They are not publisher quotas verified by this atlas. Its recommendation to prefer community reads and avoid game writes is recorded in the [usage notes](https://github.com/librematch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/usage.md).
- **Design documents are not deployment evidence.** The proposed LibreMatch Pub/Sub API does not prove a public WebSocket endpoint exists. The AoE2 Companion stream in this atlas has separate provider examples.

## How this atlas complements LibreMatch

LibreMatch supplies the shared protocol reference and much broader game-client route coverage. This atlas adds dated AoE4 checks, host-migration observations, current website request shapes, identifier mappings, and independent providers such as AoE4 World, Guides, static datasets and other-game services. Keep detailed upstream pages linked instead of maintaining a second copy of their captured payloads.

[AoECenter’s SDK](aoecenter.md) explicitly credits LibreMatch and adds typed response models and saved fixtures where the OpenAPI often leaves responses unconstrained. Its implementation is partial and contains discrepancies, which the separate coverage map preserves rather than treating the SDK as an authoritative replacement specification.

The wiki declares GFDL-1.3 licensing, and the linked client and Delta Play Replay repositories declare AGPL-3.0-or-later. This workspace retains an attributed factual index and fetch metadata, not a wholesale copy of the wiki, its captured sessions, or the generated client. See the upstream repositories for their license texts.
