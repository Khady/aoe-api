# AoECenter: SDK, response models and supporting tools

**Origin: independent/community client tools.** They document and consume publisher services; their models and fixtures are source evidence, not new live verification. [Operator categories and direct verification](publisher-services.md).

[AoECenter](https://github.com/AoECenter) supplies implementation detail for the World’s Edge/Relic backend. Its most useful repository is `relic-sdk`, an OCaml client with typed models and captured response fixtures. It explicitly acknowledges LibreMatch’s protocol research. This complements the wiki and OpenAPI reference with concrete parsing and request-building code.

All **five public repositories** were inspected at pinned revisions on **2026-09-19**. No separate hosted AoECenter data API or new upstream endpoint was established by this review. The [coverage index](../catalog/aoecenter-coverage.json) records repositories, SDK request builders, model fields and discrepancies; the [evidence record](../evidence/2026-09-19/aoecenter-review.json) contains fetch hashes and a small offline fixture check.

## Repository map

| Repository | What the inspected source provides | Relevance |
| --- | --- | --- |
| [`relic-sdk`](https://github.com/AoECenter/relic-sdk/tree/5b82d10bcc48dea5770745bc8e12f723576ca744) | OCaml HTTP client, 14 community request builders, two game request builders, login helper, models and fixtures | Main API/protocol reference; incomplete implementation |
| [`relic-store`](https://github.com/AoECenter/relic-store/tree/284602fae6c8e5073e059b981a53cab676005375) | Lobby collector and SQLite player-identity persistence | Example of joining lobby members to profiles; executable selects AoE2 |
| [`relic-token`](https://github.com/AoECenter/relic-token/tree/c86c8efe7326250a549f2f6078e434ff963c8f35) | Local Steam/AoE2 network-capture and login-field extraction prototype | Authentication implementation research; not a public token-issuing service |
| [`relic-client`](https://github.com/AoECenter/relic-client/tree/f25fb2df7f682d4b88585b96dfa9e1d38f2cee70) | Tauri/Svelte starter application with a greeting command | No implemented game API integration found in its app source |
| [`makefiles`](https://github.com/AoECenter/makefiles/tree/2038c80a1da1a1a9b9e0a4fe051e1ae8498dca8b) | Shared OCaml build/documentation/test recipes | Build support; no game-data interface |

The GitHub metadata reported the SDK’s latest push as 2025-09-09 and the other repositories’ pushes in 2024. These are repository timestamps, not evidence that a particular service or SDK integration currently works. The SDK, store and token repositories declare MIT licenses; no license was identified for the other two in this snapshot.

## SDK request coverage

The SDK’s [game mapping](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/data/game.ml) includes `age1`, `age2`, `age3`, `age4` and their Steam app IDs, plus unrelated Relic titles. The four AoE entries use `aoe-api.worldsedgelink.com`. An enum entry establishes request construction, not tested support for every model or authenticated operation.

| OCaml API family | Requests implemented in source |
| --- | --- |
| `Api.Community.Achievement` | Available achievements; achievement attainment by profile |
| `Api.Community.Advertisement` | Lobby listing with `start` and `count` |
| `Api.Community.Clan` | Clan search; full clan information |
| `Api.Community.Community_event` | Available community events |
| `Api.Community.External` | Steam-user request proxy |
| `Api.Community.Item` | Inventory request builder, with a route discrepancy described below |
| `Api.Community.Leaderboard` | Discovery, avatar stats, leaderboard rows, recent history, personal stats |
| `Api.Community.News` | Community news |
| `Api.Game.Advertisement` | Observable-game listing |
| `Api.Game.News` | Game news |
| Platform cookie helper | POST to `/game/login/platformlogin` |

Sources: [community modules](https://github.com/AoECenter/relic-sdk/tree/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/api/community), [game modules](https://github.com/AoECenter/relic-sdk/tree/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/api/game), [login helper](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/data/platform/cookie.ml).

There are **17 request builders** including login. Fifteen of the **17 game-module `.ml` files are empty**; only advertisement and news contain implementations. The module list in the generated documentation therefore overstates implemented game-route coverage. No SDK wrapper for community `getMatchHistory` or `getReplayFiles` was found at this revision.

The [leaderboard builder](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/api/community/leaderboard.ml) defaults to `leaderboard_id=3`, `platform=PC_STEAM`, `start=1`, `count=200`. Those are client defaults, not universal AoE4 choices or verified service limits. Several requests add `format=json`. The generic client adds `callNum`; supplied cookies can add session query parameters and Cookie headers. [Client source](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/client.ml).

## Response models and compressed fields

The repository contains **13 community response-model files**, **two game response-model files**, and **14 JSON fixtures**. Supporting models cover lobby participants, stat groups, leaderboard mappings, civilizations/races, achievements, inventory, clans and news. The coverage index extracts record-field names/types from these files without copying player payloads.

Community models consume named JSON objects. The observable-game model instead expects a positional outer array containing a status integer, advertisements, members and an optional tail. Its nested models retain unidentified fields under names such as `int1` and `string1`; their semantics remain unknown. This is valuable layout evidence, not a complete interpretation of every field. [Response model](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/models/response/game/observable_advertisements.ml), [member model](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/models/stub/game/observable_advertisement_member.ml).

The compressed lobby code is particularly useful:

- `options`: decode base64, inflate zlib, remove quote characters, decode a second base64 layer, then split a colon-separated string. Both advertisements in the saved fixture produced 73 fields in the offline check. This does not establish their meaning or a fixed AoE4 layout. [Decoder](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/models/stub/community/advertisement_options.ml).
- `slotinfo`: attempts base64/zlib decoding and parsing a numeric prefix plus slot records. Its current comma-splitting implementation selects only the second comma-separated fragment. That fragment was invalid JSON for both saved fixture entries in our offline check; the parser should not be adopted as a working general decoder. [Parser](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/models/stub/community/slot_info.ml).
- Serialization is incomplete: advertisement `to_json` writes empty strings for `options` and `slotinfo`. A parse/serialize round trip would lose those fields. [Advertisement model](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/models/stub/community/advertisement.ml).

The SDK itself was not compiled or executed. The offline check used Python’s standard library to inspect the repository’s public fixture and reproduce the relevant byte transformations; only counts and validation outcomes are retained here.

## Concrete integration discrepancies

| Finding | Implication / evidence |
| --- | --- |
| Inventory builder targets `/community/achievement/getInventoryByProfileIDs` | LibreMatch places it under `/community/item/`. The SDK literal is retained as a discrepancy, not added as a confirmed alternative endpoint. [Builder](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/api/community/item.ml) |
| Steam proxy builder sends `profile_names` | LibreMatch’s example and OpenAPI use `profileNames`, while the wiki table uses `profile_names`. The SDK supplies another implementation choice, not a resolution of the mismatch. [Builder](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/api/community/external.ml) |
| Login form hard-codes `title=age2` and `appID=813780` | Selecting `Age4` for ordinary requests does not convert this helper into AoE4 login. [Cookie helper](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/data/platform/cookie.ml) |
| Observable-game request has fixed build/checksum fields and two `dataChecksum` entries | Treat it as a captured protocol example requiring current title/build validation. With no profile filter, the function makes a second request using member IDs from the first response. [Builder](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/lib/api/game/advertisement.ml) |
| Mock requester ignores the request URL and returns a fixture | Passing a fixture test does not validate the URL, parameters, authentication or selected game. Some tests select `Age4`, but no AoE4 runtime conclusion follows from that. [Mock](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/tests/unit/mock/json_file.ml), [tests](https://github.com/AoECenter/relic-sdk/blob/5b82d10bcc48dea5770745bc8e12f723576ca744/tests/unit/test_cases/api.ml) |

Additional details matter when reusing the implementation: some enum interpretations are explicitly marked as assumptions, and many model fields are decoded strictly rather than tolerating missing fields. The client logs session-bearing URLs/cookies in some paths. Review those behaviors before using an authenticated deployment. These observations come from source inspection; they are not a claim that an installed application on this machine exposed credentials.

## Collector and identity mapping

`relic-store` demonstrates a useful flow: page through community advertisements, join each match member to its avatar using `profile_id`, parse platform identities, and persist player records in SQLite. Its parser recognizes `/steam/<decimal-id>` and `/xboxlive/<uppercase-hex-id>`. Those are source-supported formats, not a complete cross-platform identity specification. [Fetch](https://github.com/AoECenter/relic-store/blob/284602fae6c8e5073e059b981a53cab676005375/lib/fetch.ml), [join/storage](https://github.com/AoECenter/relic-store/blob/284602fae6c8e5073e059b981a53cab676005375/lib/store.ml), [identity parser](https://github.com/AoECenter/relic-store/blob/284602fae6c8e5073e059b981a53cab676005375/lib/parser/platform_id.ml).

Its executable selects AoE2 and the loop sleeps four seconds after collection. That interval is a client implementation choice, not a provider polling recommendation. The store uses older SDK call/model conventions than the inspected current SDK; compatibility and database writes were not tested. It is not a published player-database download or a hosted query API.

`relic-token` launches Steam for AoE2, inspects captured traffic for login fields and handles local processes. It is an authentication-research prototype rather than evidence of a public login service. Its code was read only: no capture, credential extraction, session creation, game launch or process termination was performed. [Source](https://github.com/AoECenter/relic-token/blob/c86c8efe7326250a549f2f6078e434ff963c8f35/lib/cli.ml).

## What this adds to the atlas

AoECenter corroborates existing backend routes and adds typed model references, binary-field decoding leads, client defaults, identity parsing and a collector design. Existing endpoints gain source links; questionable route literals remain explicitly marked in the separate SDK coverage map. The live-probe count remains 47, and no new hosted-provider or AoE4 authentication claim is inferred from these repositories.
