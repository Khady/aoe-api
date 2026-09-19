# Platform, esports and adjacent APIs

These services complement game data. They should not be conflated with an AoE-specific match backend.

## Steam Web API

AoE4’s Steam app ID is **1466860**, also used in the inspected [AoE4 tooling](https://github.com/ccsimplyspolit/AOE4-Analytics/blob/2766f54c2575d1f9222650a01ea5591d7d2a5a22/electron/services/relicAuthService.ts). Xbox/PlayStation player activity is not included in a Steam-only count.

| GET interface on `https://api.steampowered.com` | Inputs | Access / usefulness |
| --- | --- | --- |
| `/ISteamUserStats/GetNumberOfCurrentPlayers/v1/` | `appid` | No key in the successful AoE4 probe; concurrent Steam player count, not a match list |
| `/ISteamUserStats/GetSchemaForGame/v2/` | `appid`, `key`, optional language | Definitions of game achievements/stats, when provided by the game |
| `/ISteamUserStats/GetPlayerAchievements/v1/` | `appid`, `steamid`, `key`, optional language | Player achievements, subject to availability/privacy |
| `/ISteamUserStats/GetUserStatsForGame/v2/` | `appid`, `steamid`, `key` | Published Steam user stats, not arbitrary engine state |
| `/ISteamUser/GetPlayerSummaries/v2/` | `steamids`, `key` | Steam profile enrichment |
| `/ISteamUser/ResolveVanityURL/v1/` | `vanityurl`, `key` | Resolve a Steam vanity name to SteamID64 |

Sources: Valve’s [ISteamUserStats reference](https://partner.steamgames.com/doc/webapi/ISteamUserStats) and [ISteamUser reference](https://partner.steamgames.com/doc/webapi/ISteamUser). Only the player-count request was run; none of the key-authenticated operations were tested. The existence of a generic method does not guarantee AoE4 populates every possible stat.

Steam web API keys, Steam identity login, and an encrypted game app ticket are different credentials/flows. A web API key is not interchangeable with a World’s Edge game-session ticket.

## PlayFab and platform-specific game services

The [ageLANServer host source](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/common/domain.go) identifies `ed603.playfabapi.com` for AoE4 and `c15f9.playfabapi.com` for Mythology. Its [PlayFab router](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/playfabapi.go) registers **15 POST operations: 9 for AoE4 and 13 for Mythology**. The [complete route table and implementation limits](../agelanserver.md#playfab-facing-routes) distinguish local sessions and fixtures from publisher service behavior.

AoE4 registrations include custom-ID login, player combined info, user data, time, display-name updates, telemetry, QoS, cognitive-service tokens and party requests. Several are explicit unavailable/empty handlers. The local middleware uses `X-Sessionticket` for AoE4 and `X-Entitytoken` for Mythology, with declared exceptions; these do not establish publisher authentication or anonymous-access rules.

No PlayFab login, title configuration query or authenticated Xbox/PlayStation operation was attempted. These remain game-client implementation leads rather than verified public community statistics APIs. For cross-platform AoE statistics, start with the documented community API or verified backend reads in this atlas.

## Liquipedia and tournament data

AoE4 World offers a documented public [esports Elo route](../aoe4/aoe4world.md). For broader tournament/player metadata, Liquipedia publishes LPDB examples under `https://api.liquipedia.net/api/v3/{table}`, using an API key in an `Authorization: Apikey …` header and a `wiki` parameter. Its provider-owned [advanced API example](https://liquipedia.net/commons/Support/Bot/Advanced_Usage) describes tables such as players and tournaments and directs developers to obtain access.

This is curated esports data, not ladder/MMR history or replay telemetry. Exact Age of Empires table coverage, entitlements, rate limits and match schemas were not tested. The [API usage-guideline page](https://liquipedia.net/commons/Liquipedia:API_Usage_Guidelines) was blocked during this check; this document does not assert an unverified numeric policy.

Tournament organizers can also publish APIs through general platforms. These are separate integrations with their own access rules and event coverage; a tournament appearing on a website is insufficient evidence that all its underlying data is available through an anonymous API.

## Voobly and legacy multiplayer

[Voobly’s external API documentation](https://www.voobly.com/pages/view/147/External-API-Documentation) is a concrete lead for legacy multiplayer statistics. It belongs to Voobly’s ecosystem, not AoE4’s current matchmaking. Documentation could be located, but follow-up access was blocked and no API calls were tested. Its current credential, route and quota details remain a follow-up item rather than runnable examples here.

## Wrappers are not additional upstream providers

- [AoECenter/relic-sdk](https://github.com/AoECenter/relic-sdk): partial OCaml client with typed models and saved fixtures; [detailed source review](../aoecenter.md) includes its collector/token tools and concrete integration limits.
- [prelate-rs](https://github.com/willfindlay/prelate-rs): Rust AoE4 World client; repository calls it work in progress.
- [theflyingcodr/aoe4-client](https://github.com/theflyingcodr/aoe4-client): Go client containing historical official leaderboard request models.
- [Orda](https://github.com/gzordrai/orda): Rust AoE4 Guides client.
- [aoe4world-mcp](https://github.com/enisn/aoe4world-mcp): factual static-data MCP interface.
- [AoE4 World overlay](https://github.com/aoe4world/overlay): first-party community-project consumer useful for following real API usage.
- [ageLANServer](https://github.com/luskaner/ageLANServer): local online-service implementation and protocol reference.

None of these packages was installed or run for this research. Verify release activity, route/base-URL drift, license and client behavior before selecting one. Their service dependencies remain the relevant source of availability and limits.
