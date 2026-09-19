# World’s Edge / Relic community API

The World’s Edge backend exposes JSON services used by community tools. Its public-read routes are distinct from authenticated game-session routes. The most useful community paths are under `/community/leaderboard`, with additional lobby, achievement and other families.

This reference combines successful AoE4 requests, the supplied [replay launcher](https://github.com/EKYavsil/AoE4-Replay-Launcher/blob/7543f21d75a9cb76e5fae9c2ba104cd5a2b819e3/src/aoe4replay/aoe4world.py), and the [LibreMatch protocol reference](https://github.com/LibreMatch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community). LibreMatch is a community reverse-engineering source, not Microsoft’s official API contract; some of its examples describe AoE2 specifically.

The [full LibreMatch coverage guide](../librematch.md) also indexes 88 game-route pages and its linked 102-path OpenAPI specification. These extend well beyond the public reads summarized below.

[AoECenter’s implementation guide](../aoecenter.md) adds OCaml request builders, typed response layouts and compressed-field examples. It also records discrepancies where SDK literals or assumptions differ from LibreMatch or the verified AoE4 requests.

## Hosts and game titles

| Host | Title parameter | Evidence / status |
| --- | --- | --- |
| `https://aoe-api.worldsedgelink.com` | `age4` | Discovery, personal stats, recent matches, match lookup, replay metadata, one leaderboard page, lobbies and achievement definitions returned JSON with `result.code=0` |
| Same common host | `age1`, `age2`, `age3` | Each discovery request returned `result.code=0`; other operations were not inferred from this check |
| `https://dr-activerelease1-api.worldsedgelink.com` | `age4` | Discovery, recent history and replay metadata also succeeded; ageLANServer identifies this host family with newer AoE4 clients |
| `https://aoe-api.reliclink.com` | `age4` in the tested request | TLS certificate hostname mismatch; legacy references should not be copied blindly |
| `https://athens-live-api.worldsedgelink.com` | `athens` | Mythology: Retold discovery succeeded; source also used by AoM.gg’s published collector |
| `aoeliverelease{N}-api.worldsedgelink.com` | AoE4 family | Historical client hosts listed by ageLANServer; not tested |
| `pb-live-release{N}-api.worldsedgelink.com` | AoE2 family | Client-release hosts reported by ageLANServer; not enumerated or tested |
| `andromeda-live-release{N}-api.worldsedgelink.com` | Mythology family | Constructed in the pinned ageLANServer source; exact current deployment/title combination unverified |
| `arthurlive-api.worldsedgelink.com` | AoE2 macOS reference | Defined in ageLANServer source; not tested |

Sources: [probe report](../../evidence/2026-09-19/README.md), [ageLANServer QA](https://github.com/luskaner/ageLANServer/wiki/Questions-and-Answers-%28QA%29), [AoM.gg collector](https://github.com/erin-fitzpatric/aom-lambda/blob/ee51b41da4a60fcfe066ca5894e7e09849d3e6a5/extract-leaderboard/app.mjs).

The [pinned hostname constructor](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/common/domain.go) corrects the earlier Mythology pattern: the release number precedes `-api`. The [ageLANServer guide](../agelanserver.md) records the source-only title/method matrix, WebSocket protocol and local implementation limits.

Keep the base URL configurable. A release-numbered hostname is not an invitation to scan possible hostnames. The tested common and newer AoE4 hosts both responded; no assumption that one is permanently superior or that every route is interchangeable is justified.

## Authentication and result envelope

The successful community requests here used no API key, cookies, Steam ticket or Authorization header. They used a descriptive User-Agent and normal HTTPS certificate verification.

```json
{"result":{"code":0,"message":"SUCCESS"}}
```

Check both HTTP status and `result.code`. A missing/nonzero code must not be interpreted as an empty successful dataset. The launcher treats code `2` as replay `NOT_FOUND`; this is implementation evidence, not a live error-code test. Keep HTTP 429, 401/403, network errors and valid-but-empty results separate.

## Endpoint reference

All listed community routes use GET. `title` is required in the examples. **Live** means the specific AoE4 request in the manifest succeeded; it does not verify every optional parameter.

| Path | Parameters beyond `title` | Result / status |
| --- | --- | --- |
| `/community/leaderboard/getAvailableLeaderboards` | None | `leaderboards`, `matchTypes`, `races`, `factions`, `leaderboardRegions`; **live** |
| `/community/leaderboard/getLeaderBoard2` | `leaderboard_id`, `start`, `count`, `sortBy`; `platform` appears in community docs | `statGroups`, `leaderboardStats`; **live**, count 1 |
| `/community/leaderboard/getPersonalStat` | `profile_ids` JSON array; alternatively `profile_names` or `aliases` in implementations/docs | Cross-ladder player statistics; **live** with one profile ID |
| `/community/leaderboard/getRecentMatchHistory` | `profile_ids`; docs also describe `profile_names`, `aliases`, `matchtype_id` | `matchHistoryStats`, `profiles`; **live** |
| `/community/leaderboard/getMatchHistory` | `matchIDs` JSON array | **Lookup by match IDs**, not an assumed arbitrary history-pagination route; **live** |
| `/community/leaderboard/getReplayFiles` | `matchIDs` JSON array | `expiryUnix`, `replayFiles`; **live**; [replay handling](../aoe4/replays-and-local-apis.md) |
| `/community/advertisement/findAdvertisements` | None in the tested request; AoECenter SDK sends `start`, `count` | Lobby/advertisement response; **live**; pagination arguments are source-only; not full in-game telemetry |
| `/community/achievement/getAvailableAchievements` | None | Achievement definitions; **live** |
| `/community/achievement/getAchievements` | `profileids` JSON array, without underscore | Player achievements; community-documented, untested for AoE4 |
| `/community/leaderboard/getAvatarStatForProfile` | LibreMatch describes `profile_names`; AoECenter uses `profile_ids`, `format=json` | Additional avatar/profile stats; source-only argument variants, untested |
| `/community/clan/find`, `/community/clan/getClanInfoFull` | See source | Clan route family; untested and title applicability unestablished |
| `/community/communityevent/getAvailableCommunityEvents` | See source | Community-event metadata; untested |
| `/community/item/getInventoryByProfileIDs` | See source | Inventory metadata; untested; no universal public-access claim |
| `/community/news/getNews` | None beyond `title` in the wiki example | News entries and localization metadata; source-only |
| `/community/external/proxysteamuserrequest` | `request`, profile selector; OpenAPI uses `profileNames` / `profile_ids` | Steam-profile proxy; source-only; wiki table disagrees with its example about `profile_names` versus `profileNames` |

Source route pages: [leaderboards](https://github.com/LibreMatch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community/leaderboard), [lobbies](https://github.com/LibreMatch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community/advertisement/findadvertisements.md), [achievements and other families](https://github.com/LibreMatch/wiki/tree/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community).

### Array encoding and identifier resolution

These endpoints use JSON text **inside query parameters**, not repeated query keys and not AoE4 World’s comma-separated format:

```bash
curl --fail-with-body --get \
  'https://aoe-api.worldsedgelink.com/community/leaderboard/getPersonalStat' \
  -H 'User-Agent: my-aoe-tool/0.1 (your project/contact URL)' \
  --data-urlencode 'title=age4' \
  --data-urlencode 'profile_ids=[4635035]'
```

A Steam identity lookup can use `profile_names=["/steam/<SteamID64>"]` where supported. Store SteamID64 as a string, and retain `(title, profile_id)` as the game-profile key. The display alias can change and collide. Choose one identity filter per request until the service’s combined-filter behavior is established. Do not assume Xbox/PlayStation accounts have Steam IDs. [Personal-stat reference](https://github.com/LibreMatch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community/leaderboard/getpersonalstat.md).

### Leaderboard discovery and joins

Read discovery metadata before choosing numeric ladder IDs. The snapshot contained 111 AoE4 leaderboard entries, 17 AoE2 entries, 7 AoE3 entries and 4 AoE1 entries. These include internal, special and historical-looking names; they are **not counts of currently active player-facing queues**.

AoE4 examples from the discovered data:

| ID | Backend name |
| --- | --- |
| 0 | `Custom` |
| 17 | `Slot1_1v1Unranked` |
| 18 | `Slot1_2v2Unranked` |
| 19 | `Slot1_3v3Unranked` |
| 20 | `Slot1_4v4Unranked` |
| 533 | `Slot1_FFA8Unranked` |
| 534 | `Slot1_FFA8Unranked_Conroller` — spelling as returned |

Each board’s `leaderboardmap[]` relates ladder IDs to `matchtype_id`, `statgroup_type` and `civilization_id`. One ladder can map to multiple match types. Do not equate these numeric namespaces. Likewise, the raw `isranked` flag is not a safe direct translation to AoE4’s player-facing “Ranked Seasons”: quick-match ladder 17 returned `isranked=1`.

For leaderboard/personal-stat responses, join `leaderboardStats[].statgroup_id` to `statGroups[].id`, then inspect `members[]` for the profile. A stat group is not inherently a profile ID. Preserve the member list rather than assuming all games/modes have one member. [Source](https://github.com/LibreMatch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community/leaderboard/getleaderboard2.md), [discovery snapshots](../../evidence/2026-09-19/initial-probes.json).

`start=1` is the documented first leaderboard position; `sortBy=1` sorts by rating and `0` by wins in community documentation. The reference examples use up to 200 rows, but the AoE4 maximum was not stress-tested. Use small pages and do not extrapolate this limit to match or replay batching.

### Match history shape and ordering

Observed recent-history fields include:

- `matchHistoryStats[]`: `id`, creator, map/internal options, `matchtype_id`, description, `startgametime`, `completiontime`, `matchhistoryreportresults`, `matchhistorymember`, replay metadata when available.
- `profiles[]`: player details joined by `profile_id`.
- Report rows: player ID, `teamid`, `civilization_id`, `resulttype`, XP and `counters`.

The test returned 97 matches for one profile, spanning older and newer games. Its first row was **not** the most recently started match. Select/sort by timestamps; do not infer chronological ordering from the endpoint name. This is one observed history window, not a promised retention period or a complete account archive.

`counters` can be a JSON-encoded string. `options` and `slotinfo` can contain encoded binary/compressed structures; preserve them separately if needed rather than guessing a universal schema. Match-history result codes require a title-specific mapping. Do not infer win/loss from ordinary HTTP conventions.

AoECenter supplies decoding code and fixtures for some compressed lobby fields, including nested base64/zlib `options`. Its `slotinfo` parser has a concrete splitting problem in the inspected revision, and serializers omit compressed fields. Use these as [format research leads](../aoecenter.md#response-models-and-compressed-fields), not proof of a general AoE4 decoder.

The by-ID lookup returned `matchHistory`, while recent history returned `matchHistoryStats`. Normalize these explicitly. Unix times in the raw responses use seconds; website APIs and AoE4 World use different date representations. [Match lookup source](https://github.com/LibreMatch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/rlink/community/leaderboard/getmatchhistory.md), [response shapes](../../evidence/2026-09-19/extended-probes.json).

## Operational limits

No provider-owned numeric rate-limit contract was found. LibreMatch reports approximate community and replay limits, but those are not verified operating budgets; this catalog does not recommend driving at them. Stop/back off on 429, respect `Retry-After`, cache metadata and batch only where supported.

Discovery responses carried `Cache-Control: public, max-age=600`; sampled player/history/replay responses used `max-age=5`. No `Access-Control-Allow-Origin` was present on the tested World’s Edge responses to an `Origin` header. This supports using a server-side integration; it is not a full browser preflight test.

## Authenticated and local-server surfaces

Published AoE4 tooling also refers to `/game/login/platformlogin` and `/game/cloud/getTempCredentials`: platform tickets establish a game session and temporary storage access. These were **source-inspected only**; no account sign-in, ticket extraction or session reuse was performed. Their request formats/build fields are not promoted to a stable public API. [Implementation evidence](https://github.com/ccsimplyspolit/AOE4-Analytics/blob/2766f54c2575d1f9222650a01ea5591d7d2a5a22/electron/services/relicAuthService.ts).

[ageLANServer’s detailed implementation review](../agelanserver.md) indexes 129 route operations across its routers, including 88 in the AoE4 game router and a session WebSocket. It supplies title-specific methods and serializers, while some handlers deliberately return empty/error data or acknowledgements. Its route registration does not prove live publisher access or functionality.

LibreMatch provides broader source-only coverage of account lookup, observable games, spectator sessions, matchmaking, challenges, inventory, social functions and match reporting. The [endpoint catalog](../../catalog/endpoints.json) now includes all 88 `/game` route pages, including explicit incomplete templates. The linked [OpenAPI](https://github.com/librematch/librematch-rlink_client/blob/a1227c74a6990db9d9bc0e33c83a502773084178/openapi.yaml) models query-based session credentials, but generally leaves response bodies as unconstrained JSON. Neither source is a substitute for AoE4-specific runtime validation.
