# Verification snapshot — 2026-09-19

**Publisher subset:** 27 requests, with 25 HTTP 200 responses, one HTTP 401 and one TLS/transport failure. They cover 17 distinct route patterns: 16 have an HTTP 200 sample; the mod Find route has only an authentication rejection. All authenticated game-session, PlayFab and WebSocket findings remain source-only. [Coverage guide](../../docs/publisher-services.md), [offline audit](../../catalog/verification-summary.json). This categorization uses the existing observations and does not refresh their timestamps.

**47 selected API/service probes.** HTTP/transport distribution: 200: 43, 401: 1, 404: 1, transport-error: 2. These are individual request outcomes, not provider health scores.

All probe requests used the manifest in [catalog/probes.json](../../catalog/probes.json). HTTP 200 JSON is still interpreted separately from nonempty/useful data. No benchmark/load test was performed. The `.json` reports contain timestamped response structure and selected headers; array shapes inspect only the first item.

| Probe | HTTP | Body | Application result | Evidence |
| --- | --- | --- | --- | --- |
| `we-age4-leaderboard` | 200 | json | {"code": 0, "message": "SUCCESS"} | [extended-probes.json](extended-probes.json) |
| `we-age4-match` | 200 | json | {"code": 0, "message": "SUCCESS"} | [extended-probes.json](extended-probes.json) |
| `we-age4-lobbies` | 200 | json | {"code": 0, "message": "SUCCESS"} | [extended-probes.json](extended-probes.json) |
| `we-age4-achievements` | 200 | json | {"code": 0, "message": "SUCCESS"} | [extended-probes.json](extended-probes.json) |
| `official-age4-events` | 200 | json | — | [extended-probes.json](extended-probes.json) |
| `official-mod-games` | 200 | json | — | [extended-probes.json](extended-probes.json) |
| `companion-leaderboards` | 200 | json | — | [extended-probes.json](extended-probes.json) |
| `companion-dump-list` | 200 | json | — | [extended-probes.json](extended-probes.json) |
| `aoestats-dump-list` | 200 | json | — | [extended-probes.json](extended-probes.json) |
| `guides-direct-status` | 200 | json | — | [followup-probes.json](followup-probes.json) |
| `guides-direct-builds` | 200 | json | — | [followup-probes.json](followup-probes.json) |
| `we-dr-discovery` | 200 | json | {"code": 0, "message": "SUCCESS"} | [followup-probes.json](followup-probes.json) |
| `we-dr-history` | 200 | json | {"code": 0, "message": "SUCCESS"} | [followup-probes.json](followup-probes.json) |
| `we-replays` | 200 | json | {"code": 0, "message": "SUCCESS"} | [followup-probes.json](followup-probes.json) |
| `we-dr-replays` | 200 | json | {"code": 0, "message": "SUCCESS"} | [followup-probes.json](followup-probes.json) |
| `official-age4-leaderboard` | 200 | json | — | [followup-probes.json](followup-probes.json) |
| `world-game` | 200 | json | — | [followup-probes.json](followup-probes.json) |
| `world-stats` | 200 | json | — | [followup-probes.json](followup-probes.json) |
| `steam-player-count` | 200 | json | — | [followup-probes.json](followup-probes.json) |
| `aoe2net-sunset` | 200 | html | — | [followup-probes.json](followup-probes.json) |
| `aoeivnet` | transport error | — | — | [followup-probes.json](followup-probes.json) |
| `world-profile` | 200 | json | — | [initial-probes.json](initial-probes.json) |
| `world-last-game` | 200 | json | — | [initial-probes.json](initial-probes.json) |
| `world-search` | 200 | json | — | [initial-probes.json](initial-probes.json) |
| `world-leaderboard` | 200 | json | — | [initial-probes.json](initial-probes.json) |
| `world-esports` | 200 | json | — | [initial-probes.json](initial-probes.json) |
| `we-age4-discovery` | 200 | json | {"code": 0, "message": "SUCCESS"} | [initial-probes.json](initial-probes.json) |
| `we-age2-discovery` | 200 | json | {"code": 0, "message": "SUCCESS"} | [initial-probes.json](initial-probes.json) |
| `we-age3-discovery` | 200 | json | {"code": 0, "message": "SUCCESS"} | [initial-probes.json](initial-probes.json) |
| `we-age1-discovery` | 200 | json | {"code": 0, "message": "SUCCESS"} | [initial-probes.json](initial-probes.json) |
| `we-age4-personal` | 200 | json | {"code": 0, "message": "SUCCESS"} | [initial-probes.json](initial-probes.json) |
| `we-age4-history` | 200 | json | {"code": 0, "message": "SUCCESS"} | [initial-probes.json](initial-probes.json) |
| `legacy-relic-discovery` | transport error | — | — | [initial-probes.json](initial-probes.json) |
| `data-civs` | 200 | json | — | [initial-probes.json](initial-probes.json) |
| `data-unit` | 200 | json | — | [initial-probes.json](initial-probes.json) |
| `guides-builds` | 404 | json | {"error": "not_proxied", "message": "aoe4guides.com proxies only /api/builds/{buildId} and /api/api-docs/. The full A... | [initial-probes.json](initial-probes.json) |
| `official-age4-leaderboard-sorted` | 200 | json | — | [official-probes.json](official-probes.json) |
| `official-age4-fullstats` | 200 | json | {"statusCode": 0, "errorMessage": null} | [official-probes.json](official-probes.json) |
| `official-age4-matches` | 200 | json | — | [official-probes.json](official-probes.json) |
| `official-age4-matchdetail` | 200 | json | {"statusCode": 0, "errorMessage": null} | [official-probes.json](official-probes.json) |
| `official-age4-replay` | 200 | non-json | — | [official-probes.json](official-probes.json) |
| `official-mod-find` | 401 | json | {"errorCode": 900, "errorMessage": "Access Denied - User not authenticated."} | [official-probes.json](official-probes.json) |
| `we-myth-discovery` | 200 | json | {"code": 0, "message": "SUCCESS"} | [official-probes.json](official-probes.json) |
| `aoe2-static-civ` | 200 | json | — | [official-probes.json](official-probes.json) |
| `official-age4-events-ladder` | 200 | json | — | [targeted-probes.json](targeted-probes.json) |
| `official-age4-matches-filtered` | 200 | json | — | [targeted-probes.json](targeted-probes.json) |
| `guides-build-overlay` | 200 | json | — | [targeted-probes.json](targeted-probes.json) |

## Important interpretations

- World’s Edge `result.code=0` was observed for the tested community routes and cross-game discovery requests.
- The ordinary-player esports query returned an empty `players` array; the endpoint was reachable, not shown to contain that player.
- The official unfiltered match list was empty. Adding `matchType:17` returned entries; despite requesting `recordCount:1`, the sample contained multiple rows. Do not claim pagination semantics from that parameter name alone.
- The official stats/detail results contained default or zero fields; inspect field validity before joins or aggregation.
- Official replay GET returned a gzip attachment with an `AOE4_RE` signature in a bounded decompressed prefix. Full format parsing and game playback were not tested.
- AoE4 Guides website list request returned 404 with an explicit host-routing explanation; the full API host and individual-build website proxy worked.
- Official mod Find returned 401 with an unauthenticated-user error. Mod Games discovery was public.
- Legacy Relic hostname failed TLS verification. AoEIV.net root timed out. Neither is treated as a successful API response.
- AoE2.net root returned HTML containing the provider shutdown notice, not an API payload.

## Additional evidence

- [Documentation discovery](documentation-discovery.json): 28 conventional documentation URL checks plus two source-map requests; vendor specifications fetched separately. These are not additional business-API successes.

- [Provider OpenAPI snapshot](aoe4guides-openapi.json)
- [Local installed SCAR documentation metadata](local-scar-metadata.json)
- [Direct source-fetch metadata](source-fetches.json)
- [LibreMatch full-tree and linked-spec review](librematch-review.json): source-only follow-up; no additional live service requests
- [ageLANServer routes, messages and resource review](agelanserver-review.json): source-only indexing; no additional live service requests
- [AoECenter repository and model review](aoecenter-review.json): source inspection plus one offline compressed-fixture check; no additional live service requests

The original response body hashes remain unchanged when explanatory application status fields were added from the already fetched temporary samples. No credentials or signed replay URLs are stored here. Non-personal discovery metadata is retained to make identifier mappings reviewable.
