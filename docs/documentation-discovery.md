# Discovering publisher API documentation and metadata

Checked **2026-09-19**. **Follow-up:** [discovery beyond OpenAPI](alternative-discovery.md) found live CMS/Steam catalogs and both missing PlayFab contracts in the vendor's custom JSON format. The checks below describe the initial Swagger/source-map pass. This follow-up explicitly tested conventional Swagger/OpenAPI/help URLs on known publisher hosts and followed the source-map URLs published in the website JavaScript. It also inspected PlayFab's vendor-published specifications.

**Result:** no Swagger/OpenAPI document was found at the **28 tested API-host URLs**. However, the website's **public source map** supplied readable client source, and **PlayFab's published Swagger specifications** supplied authoritative generic platform schemas. These are useful first-party references with different scopes; neither establishes that every AoE endpoint currently works.

## Bounded URL checks

| Host | URLs requested | Result |
| --- | ---: | --- |
| `api.ageofempires.com` | 10 | All redirected to the Age of Empires homepage; the final HTTP 200 HTML was not API documentation |
| `api-dr.ageofempires.com` | 2 | Swagger UI candidate redirected to the homepage; JSON candidate returned gateway HTTP 403; remaining candidate skipped |
| `aoe-api.worldsedgelink.com` | 8 | JSON HTTP 404 responses |
| `dr-activerelease1-api.worldsedgelink.com` | 8 | JSON HTTP 404 responses |

All four received checks for `/swagger/index.html` and `/swagger/v1/swagger.json`. `/openapi.json` and `/swagger.json` were checked on the website and the two World’s Edge hosts; the planned `/openapi.json` request on `api-dr` was skipped after the 403.

Additional website candidates: `/swagger/docs/v1`, `/swagger/ui/index`, `/openapi/v1.json`, `/api/openapi.json`, `/Help`, `/api-docs`. Additional World’s Edge candidates on both hosts: `/api-docs`, `/v2/api-docs`, `/v3/api-docs`, `/docs`.

The [exact request manifest](../catalog/documentation-probes.json) and [dated results](../evidence/2026-09-19/documentation-discovery.json) preserve URLs, final redirect destinations, status, content type, size, hash and classification. Requests were sequential, unauthenticated GETs, with TLS validation, a descriptive User-Agent, approximately 1.2-second spacing and bounded response reads. Further requests on `api-dr` stopped after the 403.

A negative result means **not found at those URLs**, not “no specification exists.” A 403 does not establish what is behind the path or prove a Swagger document exists. These checks did not enumerate release hosts, test protected alternatives, or query business/account operations.

There were **30 completed documentation-discovery requests**: the 28 API-host candidates above and two linked source maps. One planned candidate was skipped. Repository/specification source fetches are recorded separately. These checks are **separate from the original 47 API/service probes** and do not increase the 16 publisher route patterns with successful runtime samples.

## Public publisher source map

The [website JavaScript](https://www.ageofempires.com/wp-content/themes/ageOfEmpires/public/js/main.b0837c.js) names a source map in its `sourceMappingURL` comment. That [map](https://www.ageofempires.com/wp-content/themes/ageOfEmpires/public/js/main.b0837c.js.map) returned HTTP 200 and contains **192 source modules with embedded contents**. This gives readable source filenames, configuration and request-building code rather than only minified route strings.

The [module and route index](../catalog/publisher-source-map.json) records module names, hashes, source positions and reviewed call sites without copying the full source bundle or commented authentication examples. No Swagger/OpenAPI configuration was identified in these 192 modules. The separate `975.8075d2.js.map` also responded, but its 6,431,882-byte advertised size exceeded the two-megabyte read bound; that map was not fully parsed.

### Additional endpoint families

These six patterns were added as **publisher-client source evidence, runtime untested**:

| Method | Host and path | Client evidence |
| --- | --- | --- |
| GET | `api.ageofempires.com/poll/list/4` | `MapVoting.js`: list used by the AoE4 poll component |
| GET | `api.ageofempires.com/poll/list/archive/4` | `VoteResults.js`: archived poll listing |
| GET | `api.ageofempires.com/poll/{pollId}` | Both components fetch a selected poll's details |
| POST | `api.ageofempires.com/poll/` | Vote submission; fields include `gameId`, `pollId`, `answers`; not executed |
| Unestablished | `api.ageofempires.com/webapi/Languages?gameId=aoe` | Configuration declaration; no call site/method established in this map |
| GET | `auth.ageofempires.com/home/checklogin` | Credentialed account-status request used by three components; not executed |

The poll components send browser credentials. Their code expects poll dates, questions and options, and constructs answer records with selected option information. This is an observed client model, not an exhaustive server schema or proof of public access. The hard-coded `/4` routes are kept literal; arbitrary game IDs are not assumed supported.

`config.js` also declares **`api-flight.ageofempires.com`**, but no use of that constant was found in the 192 modules. It remains a host lead; its purpose and deployment were not established and the host was not probed.

### Existing mod routes become more concrete

The readable modules resolve methods for **14 existing mod route patterns**, including:

| Method | Path | Detail established in client source |
| --- | --- | --- |
| GET | `/api/v4/mods/Detail/{modId}`, `/Download/{modId}`, `/Related/{modId}` | ID appended to the configured path |
| GET | `/api/v4/mods/Tags` | Metadata request through `jsGet` |
| POST | `/api/v4/mods/Featured`, `/Reviews` | JSON requests through `jsPost` |
| GET | `/api/v4/mods/Subscribe/{modId}`, `/UnSubscribe/{modId}` | **State-changing client actions despite using GET** |
| POST | `/api/v4/mods/Rate`, `/Report`, `/Delete`, `/Notifications` | State-changing JSON requests |
| POST | `/api/v4/mods/Publish` | Multipart form fields and optional file/image data |
| PUT | `/api/v4/mods/CheckAndPublishFile` | Binary upload chunks; query construction uses `modId`, `blockid`, `comp` |

All shortened paths in the table use the `/api/v4/mods` prefix. The `jsGet` helper uses `XMLHttpRequest.withCredentials`; `jsPost` uses `fetch` with `credentials: "include"`. The relevant modules are `ModsList.js`, `ModsSingle.js`, `ModCreate.js` and the two HTTP helpers. [Source index and line positions](../catalog/publisher-source-map.json), [publisher map](https://www.ageofempires.com/wp-content/themes/ageOfEmpires/public/js/main.b0837c.js.map).

The catalog now records methods, ID placeholders, selected form/query fields and state-changing effects. No subscription, vote, rating, publication, deletion or upload was sent. Source may contain dead branches or mistakes; it remains weaker evidence of server behavior than a checked response.

## PlayFab's vendor-published Swagger

[PlayFab/API_Specs](https://github.com/PlayFab/API_Specs) publishes JSON specifications used for SDK generation. The [pinned source tree](https://github.com/PlayFab/API_Specs/tree/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab) contains **20 Swagger files**. This is a vendor-maintained reference, unlike the community-produced LibreMatch specification.

Seven relevant files were fetched and inspected:

| Specification | Paths | Schema definitions |
| --- | ---: | ---: |
| [Client](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab/Client.swagger.json) | 174 | 419 |
| [Events](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab/Events.swagger.json) | 12 | 34 |
| [Multiplayer](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab/Multiplayer.swagger.json) | 88 | 250 |
| [Economy](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab/Economy.swagger.json) | 46 | 156 |
| [CloudScript](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab/CloudScript.swagger.json) | 15 | 50 |
| [Authentication](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab/Authentication.swagger.json) | 4 | 14 |
| [Data](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Swagger/PlayFab/Data.swagger.json) | 7 | 22 |

These are Swagger **2.0** specifications, with version **260814** in the inspected files. They expose request/response schemas, required fields, security schemes and operation references. Their **346 paths and 945 schema definitions are generic platform coverage**, not 346 demonstrated AoE integrations. Full schema documents remain at their pinned vendor URLs; the atlas stores their hashes and a focused [AoE-source-to-vendor comparison](../catalog/playfab-spec-coverage.json).

### Corroboration and discrepancies

**13 of 15** PlayFab operations found in ageLANServer match paths/methods in the seven inspected specifications. The two unmatched operations are `/MultiplayerServer/GetCognitiveServicesToken` and `/Party/RequestParty`. GitHub code searches also returned no hits, but a [subsequent direct inspection](alternative-discovery.md#playfab-custom-json-closes-the-two-contract-gaps) found both in `Legacy/PlayFab/Multiplayer.api.json` at the same revision. They remain absent from these seven Swagger files; vendor-contract coverage across both formats is now 15/15.

The specifications make a significant distinction from emulator behavior:

| Topic | Vendor specification | Emulator source |
| --- | --- | --- |
| Client session-ticket authentication | `X-Authorization` | Local AoE4 middleware reads `X-Sessionticket`; Mythology middleware reads `X-Entitytoken` |
| `/Event/WriteTelemetryEvents` | Entity-token security (`X-EntityToken`) | Local middleware exempts this path and the handler returns an empty acknowledgement |
| `/MultiplayerServer/ListPartyQosServers` | Documented operation with no authentication headers | Local handler returns an unavailable response |

These differences are why emulator middleware must not be adopted as the vendor contract. The vendor spec is stronger evidence of generic API semantics, but **AoE title configuration, permissions and runtime behavior remain untested**. A matched path does not establish that the title enables every feature or permits a particular login/account operation. The specification's `None` security scheme explicitly means no authentication headers, not a header named `None` to send.

The Authentication and Data documents provide further platform-level token and entity/file-storage interfaces. Their existence does not establish that AoE replays use those file APIs. No PlayFab login, entity request or title API call was made.

## How these findings affect the atlas

- Publisher endpoints remain publisher-attributed even when documented through a client implementation.
- The six new source-derived paths and fourteen resolved mod methods remain `not-probed`.
- Thirteen emulator entries now have a **vendor contract reference** as well as emulator evidence. Their runtime status remains unchanged.
- Documentation fetches, source-map retrieval and specification inspection have separate evidence from functional API probes.
- The existing [publisher verification guide](publisher-services.md) continues to report actual runtime observations, including failures and empty/default responses.

A future pass can follow additional documentation links or metadata discovered in provider clients. This bounded check does not justify claiming that no private, versioned or differently located publisher specification exists.
