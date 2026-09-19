# AgeOfEmpires.com: official website interfaces

**Operator: publisher website.** Of 42 cataloged route patterns, 8 have HTTP 200 samples, one has only a 401 rejection and 33 have no direct probe. Frontend declarations establish source usage, not complete runtime correctness. [Coverage and evidence labels](../publisher-services.md).

**API origin:** `https://api.ageofempires.com`  
**Primary evidence:** the [current official stats page](https://www.ageofempires.com/stats/ageiv) and its [published JavaScript bundle](https://www.ageofempires.com/wp-content/themes/ageOfEmpires/public/js/main.b0837c.js), fetched on 2026-09-19. The bundle’s URL and hash are recorded in the [source-fetch metadata](../../evidence/2026-09-19/source-fetches.json).

These are publisher-operated website interfaces, with several unauthenticated reads confirmed below. A public website client is not the same as a supported third-party API program. The inspected pages did not provide a general OpenAPI spec, compatibility promise, or numeric rate limit. A [bounded documentation-URL check](../documentation-discovery.md) subsequently found no specification at the tested paths, but the publicly linked source map exposed readable frontend source.

## AoE4 leaderboards and seasons

| Method | Path | Request / observed behavior |
| --- | --- | --- |
| POST | `/api/ageiv/Leaderboard` | JSON filters; unranked leaderboard request succeeded without auth |
| GET | `/api/ageiv/EventList` | Optional `isConsole` used by the website; returns season/event records |
| POST | `/api/ageiv/EventLeaderboard` | JSON filters; `matchType` is a seasonal **leaderboard ID from EventList**, not its event ID |

The current website request shape for ordinary leaderboards is:

```json
{
  "region": 7,
  "versus": "players",
  "matchType": "unranked",
  "teamSize": "1v1",
  "searchPlayer": "",
  "page": 1,
  "count": 1,
  "sortColumn": "rank",
  "sortDirection": "ASC",
  "isConsole": false
}
```

The website uses 100 rows; the sample deliberately uses one. **Specify sorting.** The initial probe modeled on an older wrapper omitted sort fields and returned a bottom-ranked row; the current frontend sends them explicitly. Do not assume an omitted sort returns rank 1.

`versus` values in source include `players` and `ai`; `matchType` includes `custom`, `unranked`, `aieasy`, `aimedium`, `aihard`, `aiexpert`. Team-size strings include `1v1`–`4v4`. The older published [Go wrapper](https://github.com/theflyingcodr/aoe4-client/blob/2a65b081a6209057593df2935541c895aa45d9c9/official/leaderboards.go) maps region 0–7 to Europe, Middle East, Asia, North America, South America, Oceania, Africa, Global. Only the global-player sample was tested here.

Response fields observed: `count`, `lastUpdated`, `items`, `isEvent`, `compressedItems`, and additional envelope metadata. Entries include `rlUserId`, `userName`, `elo`, `eloRating`, `eloHighest`, rank, wins/losses, win rate and streak. Do not infer semantics for every legacy/redundant field: the sampled envelope’s region did not simply echo the request region.

`EventList` returned objects with `eventId`, `leaderboardId`, `eventName`, `startDate`, `endDate`. For the snapshot’s “Year A - Fall - Ranked Solo Crossplay 14”, `eventId` was 160 and `leaderboardId` was 164. Use the latter as EventLeaderboard’s `matchType` string. These are dated examples, not fixed season constants. Controller filtering is present in current frontend code. [Live results](../../evidence/2026-09-19/README.md).

## Full stats, match lists and detail

The website builds these routes from `/api/GameStats/` + game name + operation. AoE4 uses `AgeIV`.

| Method | Path | Source-backed request fields | What this check established |
| --- | --- | --- | --- |
| POST | `/api/GameStats/AgeIV/GetFullStats` | `profileId`, `game`, `matchType`; frontend also carries `gamertag`, `player`, `gameId`, `gameType` | Returned `mpStatList`, `careerStats`, `user`, `mpMatches`, `statusCode:0` |
| POST | `/api/GameStats/AgeIV/GetMatchList` | `profileId`, `game`, `matchType`, `page`, `recordCount`, `sortColumn`, `sortDirection`; other profile selectors in frontend | Unfiltered sample returned HTTP 200 with an empty `matchList`; adding `matchType:17` returned entries; requested `recordCount:1` did not restrict the sample to one entry |
| POST | `/api/GameStats/AgeIV/GetMatchDetail` | `matchId`, `profileId`, `game`; frontend can carry match/context fields | Returned `matchSummary`, `playerList`, `statusCode:0` for a known public match |
| GET | `/api/GameStats/AgeIV/GetMatchReplay/` | `matchId`, `profileId` query parameters | Returned a gzip attachment with an AoE4 replay signature |

Example of the tested match-detail request:

```bash
curl --fail-with-body 'https://api.ageofempires.com/api/GameStats/AgeIV/GetMatchDetail' \
  -H 'Content-Type: application/json' \
  -H 'User-Agent: my-aoe-tool/0.1 (your project/contact URL)' \
  --data '{"profileId":4635035,"game":"age4","matchId":250457718}'
```

**Interpretation limits:** zero values in `careerStats` do not prove zero lifetime activity. The tested full-stats result contained aggregate multiplayer totals while career fields and embedded matches were empty/zero. A successful request does not establish all fields are populated for AoE4 or every identity/platform.

In the match-detail response, some participants had `profileId:0` while their usable identifier appeared as a string in `userId`. `matchLength` was `40.75`, corresponding to the other API’s `2445` seconds for the same match; this strongly supports minutes for that sample. The date was a formatted string without an explicit timezone. Preserve the raw value and avoid silently treating every official-website date as ISO UTC.

Replay availability is perspective-dependent. File integrity and availability do not prove that the replay will play on the user’s installed build. [Replay reference](../aoe4/replays-and-local-apis.md), [official replay instructions](https://support.ageofempires.com/hc/en-us/articles/34920298779540-Downloading-Replay-Files-through-the-Age-of-Empires-Stats-page).

## Mod catalog and publishing family

The current frontend declares a separate `/api/v4/mods` family. This research used only discovery and a small read-only catalog request.

| Method / route evidence | Path | Access / verification |
| --- | --- | --- |
| GET tested | `/api/v4/mods/Games` | Anonymous success; game IDs 1, 2, 3, 4, 1001 in this snapshot |
| POST source + tested | `/api/v4/mods/Find` | Anonymous request returned **401**, `errorCode:900`, “User not authenticated” |
| GET in publisher source | `/Detail/{modId}`, `/Download/{modId}`, `/Tags`, `/Related/{modId}` | Methods and path construction established; runtime untested |
| POST in publisher source | `/Featured`, `/Reviews` | Catalog/review queries; runtime untested |
| GET in publisher source, state-changing | `/Subscribe/{modId}`, `/UnSubscribe/{modId}` | Subscription actions; not executed |
| POST in publisher source, state-changing | `/Rate`, `/Report`, `/Publish`, `/Delete`, `/Notifications` | Publication uses multipart form data; not executed |
| PUT in publisher source | `/CheckAndPublishFile` | Binary upload chunks; not executed |
| Other frontend declarations | `/Types`, `/My`, `/Installed`, `/Like` | Current method/access not established here; historical community methods noted below |
| Moderation paths | `/GetFlagged`, `/GetFlaggedDetail`, `/Moderate` | Restricted-looking frontend family; neither permissions nor request bodies investigated |

Do not describe the entire mod API as anonymous because `/Games` works. Do not reuse example Authorization tokens from third-party protocol documentation. The [LibreMatch Find page](https://github.com/LibreMatch/wiki/blob/fdb932e9eb6cff5f7dd8d1d46c7fbcc8202d0419/src/aoe/api/v4/mods/find.md) includes historical captured authentication; this atlas deliberately reproduces only the field names and no credential values.

Read-only Find body tested:

```json
{"q":"","filter":0,"sort":"lastUpdate","order":"desc","start":0,"count":1,"game":4,"modid":0}
```

The same response’s `isLoggedOn:false` makes the access requirement explicit. Read/publish access is an integration task requiring the service’s supported account flow, not something a fresh unauthenticated probe can establish.

LibreMatch’s historical reference also records POST for `Installed` and `My`; the catalog now links those method declarations separately from current frontend path evidence. Its broader v1/v2/v4 website section includes many short placeholder pages, so a listed operation is not automatically a complete current request. See the [source coverage map](../librematch.md).

## Cross-game website routes found

The same official bundle declares these leaderboard paths:

- AoE1 DE: `/api/v2/agede/Leaderboard`
- AoE2 DE: `/api/v2/ageii/Leaderboard`
- AoE2 native Mac family: `/api/gamestats/ageiimac/Leaderboard`
- AoE3 DE: `/api/ageiii/Leaderboard`
- Mythology: `/api/agemyth/Leaderboard`

It also constructs `GameStats` routes using game names and explicitly declares `/api/GameStats/AgeII/GetCampaignStats` and `/api/GameStats/AgeII/GetMatchReplay`. These cross-game operations were **source-observed, not tested** in this edition. Parameters need not be identical to AoE4.

Other declared website interfaces include `/webapi/Languages?gameId=aoe` and WordPress-specific AJAX paths. They are ancillary site plumbing, not a general game-control API. ageLANServer additionally identifies `api-dr.ageofempires.com` for newer AoE4 game clients; this is a host lead, not a verified replacement for the website origin used above.

## Error and caching notes

Read `statusCode`/`errorMessage`, nested match metadata, and HTTP status. An empty successful match list is not equivalent to a demonstrated populated history. Sample requests reflected `Access-Control-Allow-Origin: https://example.org` when that Origin was sent; browser cookie/preflight behavior was not fully tested. No numerical request limit or freshness SLA was established. Cache sensible read results and avoid assuming the official frontend’s refresh policy is identical to the raw backend’s.

The [ageLANServer source review](../agelanserver.md#functional-handlers-fixtures-and-stubs) also identifies game-client POST `/textmoderation` and two CDN status paths. Their local handlers and proxy fallback were inspected only; they are not extra verified website API responses.

## Readable publisher source and account/poll APIs

The [documentation-discovery guide](../documentation-discovery.md) records a public source map with 192 embedded modules. It adds `/poll/list/4`, `/poll/list/archive/4`, `/poll/{pollId}`, vote submission at `/poll/`, the language-config declaration, and `https://auth.ageofempires.com/home/checklogin`. These are source-derived and were not executed. Account status belongs to the separately cataloged publisher account host.

The source map resolves methods for 14 existing mod patterns, including credentialed GET subscription/unsubscription actions, multipart POST publication, and binary PUT upload chunks. The [detailed method table](../documentation-discovery.md#existing-mod-routes-become-more-concrete) and catalog link these findings to source modules and positions. No state-changing operation was tested.
