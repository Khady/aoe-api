# ageLANServer: game-client protocol reference

**Operator: independent/community emulator.** Source-inspected routes are not live publisher verification; its publisher/vendor counterparts are marked as upstream candidates. [Operator categories and direct verification](publisher-services.md).

[ageLANServer](https://github.com/luskaner/ageLANServer) contributes substantially more than hostname clues. It implements a local replacement for parts of the online services used by Age of Empires I/II/III: Definitive Edition, IV, and Mythology: Retold. Its route registrations, session notifications and serializers help explain the protocol behind the game client.

**Reviewed 2026-09-19 at [revision `eb7ec5e`](https://github.com/luskaner/ageLANServer/tree/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454).** The repository metadata reports a push on 2026-09-10 and an AGPL-3.0 source license. This review inspected source and indexed declarations; it did not install or run the server, launcher or game.

The crucial distinction: **an emulator route is evidence about an implementation, not confirmation of a working public publisher endpoint.** Several handlers deliberately return empty data, errors or fixed acknowledgements. The README explicitly excludes publisher matchmaking, working leaderboards and clan operations. [Project capabilities and limitations](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/README.md).

## What this adds

| Indexed material | Coverage |
| --- | --- |
| Method/path operations across routers | 129, including 5 explicitly local management/file operations |
| Game router | 107 operations across all five titles; includes `/wss/` and the local `/cloudfiles/` helper |
| AoE4 game router | 88 operations: 87 `/game/…` routes plus `/wss/` |
| PlayFab-facing API | 15 operations overall: 9 for AoE4, 13 for Mythology |
| WebSocket notifications | 14 distinct action names across titles |
| Handler source types | 43 named structs containing explicit `schema` or `json` field tags |
| Bundled response data | 46 JSON files across titles, including 9 AoE4 files |
| Atlas integration | 46 additional path patterns; implementation references attached to 75 existing patterns |

The complete [route/type/event/resource index](../catalog/agelanserver-coverage.json) records title conditions, methods, exact casing, source lines, handlers and atlas IDs. The [AoE4 route reference](aoe4/agelan-routes.md) lists all 88 AoE4 game-router operations with direct implementation links. [Fetch hashes and review evidence](../evidence/2026-09-19/agelanserver-review.json) pin the source used.

Counts exclude commented TODOs, proxy catch-all paths and implicit HTTP HEAD handling. GET and POST on the same path count separately in this source index, while the main atlas groups path patterns. Source title codes are `age1`, `age2`, `age3`, `age4`, `athens`. The game-router counts are respectively 61, 79, 88, 88 and 87; AoE2/AoE3 totals include the artificial cloud-file helper. [Game constants](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/common/game/game.go), [game router](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/game.go).

## Relationship to the other references

| Source | Particularly useful for |
| --- | --- |
| [LibreMatch](librematch.md) | Community protocol documentation, parameter descriptions, captured layouts and linked OpenAPI |
| [AoECenter](aoecenter.md) | Client request builders, typed models and decoding examples |
| ageLANServer | Explicit title/method branches, session push protocol, local behavior and positional serializers |
| [Live atlas probes](../evidence/2026-09-19/README.md) | Evidence that particular anonymous reads returned particular data on the check date |

The emulator can fill a documentation gap without resolving the publisher API's current authentication, retention, rate limits or production behavior. Conversely, omission from the emulator does not show that the publisher lacks a feature. Its `/game/…` router does not replace the separately tested `/community/…` reference.

## Differences that matter for AoE4 integrations

These are the explicit registrations in the [pinned game router](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/game.go). “Absent” means absent from that emulator router.

| Exact path | AoE4 | AoE2 DE | AoE3 DE | Mythology: Retold |
| --- | --- | --- | --- | --- |
| `/game/automatch/getAutomatchMap` | GET | Absent | Absent | Absent |
| `/game/automatch2/getAutomatchMap` | Absent | GET | GET | GET |
| `/game/Leaderboard/getRecentMatchHistory` | GET | GET | POST | GET |
| `/game/Challenge/getChallengeProgress` | GET | GET | POST | GET |
| `/game/advertisement/findAdvertisements` | GET | GET | POST | GET |
| `/game/advertisement/findObservableAdvertisements` | GET | GET | POST | GET |
| `/game/advertisement/getLanAdvertisements` | Absent | GET | POST | Absent |
| `/game/chat/getChatChannels` | GET | GET | POST | GET |
| `/game/chat/sendWhispers` | POST | Absent | Absent | POST |
| `/game/chat/sendWhisper` | Absent | Absent | POST | Absent |
| `/game/relationship/getRelationships` | GET | GET | POST | GET |
| `/game/cloud/getFileURL` | GET | GET | POST | Absent |
| `/game/Leaderboard/getRecentMatchSinglePlayerHistory` | GET | Absent | Absent | Absent |
| `/game/challenge/updateProgressBatched` | POST | Absent | Absent | POST |
| `/game/party/createOrReportSinglePlayer` | POST | Absent | Absent | POST |

Preserve path capitalization: `/Leaderboard` and `/leaderboard`, `/Achievement` and `/achievement`, and `/Challenge` and `/challenge` are separate registrations. The index retains `reportUser`, while the older LibreMatch-derived catalog has `reportuser`; that join is explicitly a case-folded cross-reference, not a verified alias.

## Session HTTP behavior and response encoding

[TitleMiddleware](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/titleMiddleware.go) selects the configured game object for a request. Appending `title=age4` to an arbitrary URL is not established as a universal way to switch the local server's game context.

[SessionMiddleware](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/sessionMiddleware.go) normally reads `sessionID` with `r.FormValue`, checks the emulator's session store and refreshes expiry. Its explicit HTTP exceptions are `/game/msstore/getStoreTokens`, `/game/login/platformlogin`, `/game/news/getNews`, `/game/Challenge/getChallenges`, `/game/item/getItemBundleItemsJson`, `/wss/`, and the `/cloudfiles/` prefix. The WebSocket still requires a valid session in its first message. These exceptions describe this emulator; they do not establish anonymous access on publisher servers.

The [binding helper](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/http.go) reads GET query parameters, JSON bodies when the content type contains `application/json`, and form bodies otherwise. `Json[T]` decodes JSON text embedded inside form/query values. Unknown form/query keys are ignored. Handler JSON support does not mean `sessionID` inside a JSON body will satisfy the separate `r.FormValue` middleware check.

Many game responses are positional arrays (`i.A` is `[]any`), unlike the named objects returned by the community API. Do not reuse a community JSON model for these game routes. Important serializers include:

| Source | Why inspect it |
| --- | --- |
| [Login](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/login/platformlogin.go) | Creates a local session and assembles profile, relay and static login data; title and client-library version affect layout |
| [User models](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/models/user.go) | Profile/extra-profile encoding and `clientLibVersion` differences; local identity is not proof of publisher ID equivalence |
| [Advertisements](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/models/advertisement.go) | Lobby array positions differ by title; AoE4 uses numeric `0` for one platform-lobby placeholder where AoE2/Mythology use string `"0"` |
| [Battle server models](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/models/battleServer.go) | Relay host/port advertisement and observer-related connection information |
| [Session queue](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/models/session.go) | Notification buffering and polling behavior |

The 43 tagged structs in the index are **source-type clues**, not complete request schemas. Embedded structs, untagged exported fields, middleware arguments and custom codecs need separate reading. Some misleadingly named `…Request` types are actually used to construct responses.

## WebSocket session notifications

The [WebSocket implementation](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/wss/wss.go) registers **GET `/wss/`** for HTTP upgrade. It is a game-session notification channel, distinct from AoE4 World HTTP APIs and AoE2 Companion's streams.

After upgrade, the implementation expects an initial JSON message within one minute:

```json
{"operation": 0, "sessionToken": "<existing-local-session-id>"}
```

The token is looked up in the emulator's game-session store. Operation `0` also supports rebinding an existing connection to a recognized session. Ping handling sends a Pong and refreshes the read deadline and session expiry. No publisher WebSocket connection or subscription was tested.

`SendOrStoreMessage` constructs the envelope:

```text
[0, actionName, recipientLocalUserId, payloadArray]
```

If sending fails or no connection is available, it queues the message for the session. The 14 action names found at call sites are:

| Family | Actions found in source |
| --- | --- |
| Friend/presence | `FriendAcceptMessage`, `FriendClearMessage`, `PresenceMessage` |
| Invitations | `ExtendInvitationMessage`, `CancelInvitationMessage`, `ReplyInvitationMessage` |
| Match/lobby | `MatchStartMessage`, `MatchReceivedChatMessage`, `PlatformSessionUpdateMessage` |
| Chat | `PersonalChatMessage`, `ChannelJoinMessage`, `ChannelLeaveMessage`, `ChannelChatMessage` |
| Stats | `AvatarStatsUpdatedMessage` |

These span multiple games: the channel join/leave/text routes are AoE3-only, and `updatePlatformLobbyID` is registered for AoE1/AoE3. Do not assume every action applies to AoE4. Each event has a call-site source link in the [event index](../catalog/agelanserver-coverage.json); payloads can depend on client-library version.

**Polling companion:** POST `/game/login/readSession` reads `ack` and calls the session queue, whose local wait timer is 19 seconds. Its body is unusual: a decimal message ID, a comma, then JSON for an outer array containing the messages. An illustrative one-message body is:

```text
7,[[[0,"PresenceMessage",42,[]]]]
```

The example uses invented IDs and an empty placeholder payload. The whole body is not a single standard JSON value: split the numeric prefix before JSON decoding. A handler parse error emits `0,[[]]`. These are local source semantics, not a guarantee of publisher queue retention, delivery or acknowledgement rules. [readSession handler](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/login/readSession.go), [queue implementation](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/models/session.go).

## PlayFab-facing routes

The [host definitions](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/common/domain.go) associate `ed603.playfabapi.com` with AoE4 and `c15f9.playfabapi.com` with Mythology. The [PlayFab router](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/playfabapi.go) adds a concrete endpoint list to those earlier hostname leads.

All 15 API operations below use **POST** in the emulator:

| Route | AoE4 | Mythology | Reviewed implementation detail |
| --- | --- | --- | --- |
| `/Client/GetPlayerCombinedInfo` | Yes | Yes | Constructs profile/inventory-shaped local response |
| `/Client/GetTime` | Yes | Yes | Time response |
| `/Client/LoginWithCustomID` | Yes | No | Numeric custom ID mapped to a local user/session |
| `/Client/GetUserData` | Yes | No | Returns `RLinkProfileID` from the local user ID |
| `/Client/GetTitleData` | No | Yes | Includes local static-data configuration |
| `/Client/GetUserReadOnlyData` | No | Yes | Local user-data response |
| `/Client/LoginWithSteam` | No | Yes | Local login implementation |
| `/Client/UpdateUserTitleDisplayName` | Yes | Yes | Display-name handler |
| `/Event/WriteTelemetryEvents` | Yes | Yes | Acknowledges with empty `AssignedEventIds` |
| `/Inventory/GetInventoryItems` | No | Yes | Local inventory response |
| `/MultiplayerServer/GetCognitiveServicesToken` | Yes | Yes | Explicit unavailable response |
| `/MultiplayerServer/ListPartyQosServers` | Yes | Yes | Explicit unavailable response |
| `/Party/RequestParty` | Yes | Yes | Explicit unavailable response |
| `/Catalog/GetItems` | No | Yes | Local catalog handler |
| `/CloudScript/ExecuteFunction` | No | Yes | Local implementation; not arbitrary code execution support |

The [local middleware](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/playfabapiMiddleware.go) checks `X-Sessionticket` for AoE4 and `X-Entitytoken` for Mythology, except its declared login, QoS, telemetry and static-path exceptions. This establishes neither a supported third-party authentication flow nor publisher access rights. Local `LoginWithCustomID` behavior should not be copied as a claim about the live title's authentication policy.

The [response helper](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/playfab/Client/shared/response.go) wraps successful results in `code`, `status`, `data`; errors add `errorCode`, `error`, `errorMessage`. Its unavailable helper puts **503 in the JSON `code` field**, but calls a JSON writer that does not set HTTP status 503. Distinguish HTTP status from application status here too.

Mythology additionally gets **GET `/static/`**, a local file-serving subtree for bundled PlayFab data. It is not a sixteenth publisher PlayFab API method. All PlayFab findings here remain source-only.

### Vendor contract comparison added after the emulator review

A [comparison with PlayFab's published Swagger](documentation-discovery.md#corroboration-and-discrepancies) matches 13 of these 15 API operations. The vendor defines client session-ticket authentication as `X-Authorization`; the emulator headers above are local implementation choices. Telemetry authentication and QoS behavior also differ. Consult the vendor schemas for the generic contract and retain the emulator as game-client/protocol evidence; no AoE title runtime behavior was validated.

## Functional handlers, fixtures and stubs

Concrete examples explain why endpoint counts do not measure full API functionality:

| Handler | Behavior in the inspected implementation |
| --- | --- |
| [Lobby finder](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/advertisement/findAdvertisements.go) | Filters local advertisements using request criteria and game/lobby state; examine version/checksum/mod/relay/tag constraints before interpreting an empty result |
| [Observable lobby finder](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/advertisement/findObservableAdvertisements.go) | Uses local ongoing-match and observer conditions |
| [Recent match history](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/leaderboard/getRecentMatchHistory.go) | Always `[0,[]]` |
| [Leaderboard](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/leaderboard/getLeaderBoard.go) | Always `[0,[],[],[]]` |
| [Finalize replay upload](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/party/finalizeReplayUpload.go) | Always `[0]`; the handler performs no upload finalization |
| [Temporary cloud credentials](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/cloud/getTempCredentials.go) | Local cloud-file credentials; an explicit TODO leaves AoE4 replay handling unresolved |
| [Player report](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/playerreport/reportUser.go) | Fixed `[2,0]`; not a publisher moderation integration |
| [Automatch maps](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/game/automatch2/getAutomatchMap.go) | Reads bundled map definitions; does not demonstrate working matchmaking |
| [Text moderation](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/apiAgeOfEmpires/textmoderation/textmoderation.go) | Local `/textmoderation` handler returns Allow for username sanitization; no inference about publisher policy |
| [CDN status](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/cdnAgeOfEmpires/aoe/serverStatus/serverStatus.go) | Explicitly returns HTTP 404 |

The source recognizes `api.ageofempires.com`, AoE4's `api-dr.ageofempires.com` and `cdn.ageofempires.com`. It registers POST `/textmoderation`, and GET `/aoe/rl-server-status.json` or `/aoe/athens-server-status.json` depending on title. A [proxy fallback](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/proxy.go) can forward other paths when its upstream can be resolved. A fallback does not identify additional concrete endpoints, and the explicit local handlers should not be mistaken for upstream observations.

Five operations are clearly local helpers: GET `/test`, GET `/cacert.pem`, POST `/shutdown` (Windows only), GET `/cloudfiles/` (AoE2/AoE3), and GET `/static/` (Mythology). Their presence in the index does not mean those paths exist on Microsoft servers. [Management router](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/routes/router/general.go).

## Bundled data and transport boundaries

The [AoE4 response directory](https://github.com/luskaner/ageLANServer/tree/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/resources/responses/age4) contains `achievements.json`, `leaderboards.json`, `automatchMaps.json`, `challenges.json`, `presenceData.json`, `itemDefinitions.json`, `itemBundleItems.json`, `itemLocations.json`, and `levelRewardsTable.json`. Additional [login configuration](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/resources/config/age4/login.json) helps populate positional login responses.

These fixtures are useful schema/enum clues for items, progression, maps and service metadata. They are not an independently verified export of today's live data, player entitlements, unit balance or economy statistics. Keep [AoE4 World Data](aoe4/static-data.md) as the separate reference for unit/building/technology data. The resource index records file hashes and top-level shapes without copying entire fixture contents.

The HTTP/session service coordinates lobbies, peers, invitations and relay discovery. The README describes a separate BattleServer relay executable and configuration, including use of the AoE2 DE relay for AoE4/Mythology. That distinction matters: implementing these HTTP routes does not by itself implement the game's match simulation or provide an API for arbitrary live unit state. [Setup and relay architecture](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/README.md), [relay models](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/server/internal/models/battleServer.go).

## Hostname corrections and remaining gaps

The [pinned hostname constructor](https://github.com/luskaner/ageLANServer/blob/eb7ec5ed5fe2ad0a39a843819a0fb928390d4454/common/domain.go) gives these families:

| Game | Source-defined host pattern |
| --- | --- |
| AoE4 | `dr-activerelease{N}-api.worldsedgelink.com` |
| AoE2 DE | `pb-live-release{N}-api.worldsedgelink.com` |
| Mythology: Retold | `andromeda-live-release{N}-api.worldsedgelink.com` |
| AoE2 macOS-specific reference | `arthurlive-api.worldsedgelink.com` |

The Mythology form corrects this atlas's earlier `andromeda-live-release-api{N}` transcription. The source includes DNS-based release enumeration, but no enumeration was run for this review. These are construction rules and references, not confirmation of a current active release number. Previously tested common/AoE4/Athens hosts retain their original evidence in the [backend guide](shared/worlds-edge.md#hosts-and-game-titles).

The remaining integration work is concrete: confirm an intended publisher endpoint and title, establish its authorized session flow if needed, validate actual payload layouts against the relevant client build, and distinguish local-emulator shortcuts from real service behavior. This review adds no new live game-service probes; the atlas still has 47 recorded live requests.
