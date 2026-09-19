# API discovery beyond Swagger/OpenAPI

Checked **2026-09-19**. This pass found **two live discovery catalogs** and a **vendor-specific contract format that contains both PlayFab operations missing from the inspected Swagger files**. It did not find a self-description of the World’s Edge game backend at the tested URLs.

The evidence distinguishes three results: a metadata document successfully fetched, operations described by that document, and operations actually executed. Only the first two occurred in this pass.

## What other mechanisms can expose

| Mechanism | What it can tell us | Result or scope of this investigation |
| --- | --- | --- |
| **Framework route indexes** | Registered paths, verbs, argument types, defaults and constraints | Publisher WordPress index found: 232 patterns across 13 namespaces |
| **Vendor discovery methods** | API interfaces, versions and parameters | Steam catalog found: 27 interfaces and 63 method/version entries |
| **Custom SDK-generator contracts** | Paths, authentication, request/response models, enums, errors and feature flags | Seven PlayFab `.api.json` files inspected; all 15 emulator operations matched |
| **GraphQL introspection / SDL** | Query/mutation fields, types, arguments and descriptions | Minimal GET introspection candidate tested at `/graphql` on three API hosts; no GraphQL response |
| **OData CSDL/EDMX** | Entity sets, properties, types, relationships and operations | `/$metadata` and `/odata/$metadata` tested on three API hosts; no metadata document |
| **SOAP WSDL / REST WADL** | Operations, bindings, message schemas or HTTP resources | Root `?wsdl` and `/application.wadl` tested on three hosts; no contract |
| **Framework metadata pages** | Generated service lists and DTO descriptions, such as ServiceStack `/metadata` | `/metadata` tested on three hosts; no metadata page |
| **API catalogs and hypermedia** | Links to services, documentation and schemas | `/.well-known/api-catalog`, `/apis.json`, HTML discovery links and HTTP `Link` headers examined; no game API catalog found |
| **HTTP OPTIONS** | Resource capabilities; some frameworks return schemas | Three API-root checks; no route list or useful `Allow`/discovery metadata |
| **OpenID Connect / OAuth metadata** | Identity issuer, authorization/token endpoints and supported capabilities | Account-host OpenID discovery returned 403; no identity configuration established |
| **gRPC reflection / protobuf descriptors** | RPC names and input/output message definitions | Source search only: existing community AoE2 CadeRemote protobuf lead; no publisher AoE4 gRPC target established or reflection call sent |
| **OpenRPC / XML-RPC discovery** | JSON-RPC method schemas or XML-RPC service hints | Website RSD candidate returned 403; no JSON-RPC game target established, so no `rpc.discover` call |
| **MCP and capability registries** | Tool/resource lists and input schemas when the protocol is accessible | Publisher CMS index declares an MCP adapter and WordPress Abilities routes; protocol access not tested |
| **RAML, API Blueprint, AsyncAPI, JSON Schema, request collections and typed SDKs** | Resource/message contracts or executable request examples | Public client/repository leads examined; no additional publisher game contract in these formats located in this bounded pass |

These formats serve different purposes. JSON Schema by itself need not describe routes; AsyncAPI describes messaging interfaces; OpenID discovery describes identity services. A Postman/Bruno collection can be useful implementation evidence without being a provider-maintained contract. Swagger UI, ReDoc, RapiDoc and Scalar are documentation renderers, so another renderer is not necessarily another contract format.

Primary references: [GraphQL introspection](https://spec.graphql.org/September2025/#sec-Introspection), [Microsoft OData metadata](https://learn.microsoft.com/en-us/odata/webapi-8/fundamentals/metadata-routing), [WSDL](https://www.w3.org/TR/wsdl20-primer/), [WADL](https://www.w3.org/submissions/wadl/), [ServiceStack metadata](https://docs.servicestack.net/metadata-page), [API catalog standard](https://www.rfc-editor.org/rfc/rfc9727.html), [service-description link relations](https://www.rfc-editor.org/rfc/rfc8631.html), [OpenID discovery](https://openid.net/specs/openid-connect-discovery-1_0.html), [gRPC reflection](https://grpc.io/docs/guides/reflection/), [OpenRPC](https://spec.open-rpc.org/#service-discovery-method), [AsyncAPI](https://www.asyncapi.com/docs/reference/specification/v3.1.0), [API Blueprint](https://apiblueprint.org/).

## Publisher website: an actual route catalog

**GET [`https://www.ageofempires.com/wp-json/`](https://www.ageofempires.com/wp-json/)** returned a WordPress REST index containing **232 registered path patterns and 13 namespaces**. The index supplies method lists and argument metadata, including types, required flags, enums, defaults and constraints. This is a live publisher-served self-description, not a reconstruction from a community client. [WordPress discovery documentation](https://developer.wordpress.org/rest-api/using-the-rest-api/discovery/).

The [saved metadata index](../catalog/publisher-cms-metadata.json) retains all path/method declarations and selected content-query argument schemas. Examples:

| GET path | Likely use based on its registration; content not fetched |
| --- | --- |
| `/wp-json/wp/v2/games` | Website game pages |
| `/wp-json/wp/v2/civilizations` | Website civilization content |
| `/wp-json/wp/v2/game_modes` | Game-mode content |
| `/wp-json/wp/v2/learn_to_play` | Learning content |
| `/wp-json/wp/v2/events` | Website events |
| `/wp-json/wp/v2/game` | Game taxonomy/filter terms, distinct from the `games` collection |

For example, the `games` GET declaration defines `page` as an integer with minimum/default 1, `per_page` as an integer with default 10 and maximum 100, and `context` with `view`, `embed`, and `edit` values. These are advertised argument constraints; this pass did not test each value or establish permission to use `edit`.

The index also advertises `POST`, `PUT`, `PATCH` and `DELETE` on various resources. **Route registration is not proof of anonymous read/write permission.** None of those actions was executed. The 232 entries include generic CMS and plugin administration, so they are not counted as 232 new AoE game APIs. The main catalog adds only the index and six selected GET content families under a separate `publisher-cms` service.

### MCP and Abilities leads

The index declares `/wp-json/mcp/mcp-adapter-default-server` with GET/POST/DELETE, plus `/wp-json/wp-abilities/v1/abilities` and related capability routes. The WordPress project's [MCP adapter](https://github.com/WordPress/mcp-adapter) is designed to expose WordPress capabilities to MCP clients.

This is **metadata evidence only**: no MCP initialization, `tools/list`, resource request or tool execution occurred. The index does not reveal the publisher's accessible tool set or establish anonymous access. This lead belongs to the website CMS, not the multiplayer backend.

## PlayFab: custom JSON closes the two contract gaps

The same pinned [PlayFab vendor repository](https://github.com/PlayFab/API_Specs/tree/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Legacy/PlayFab) contains a custom `.api.json` format under `Legacy/PlayFab`. Its `calls` array describes method, URL, authentication and named input/output models; `datatypes` describes properties, enums and optional flags. Some calls also identify allowed entity-token types and feature flags.

Across Client, Events, Multiplayer, Economy, CloudScript, Authentication and Data, the seven inspected files contain **400 call entries and 1,096 named datatype entries**. There are **55 paths absent from the corresponding Swagger files**, while Swagger has one path absent from these custom files (`/PubSub/Negotiate`). Neither format is a complete superset of the other. These are generic platform counts, not demonstrated AoE integrations. [Comparison and model references](../catalog/playfab-custom-contracts.json).

The key result is that **all 15 ageLANServer PlayFab operations now have vendor contract matches**, up from 13 in the Swagger-only comparison:

| Previously unmatched operation | Custom vendor contract details |
| --- | --- |
| POST `/MultiplayerServer/GetCognitiveServicesToken` | `EntityToken` auth; `Beta` flag; request names `CognitiveServicesType`, `Region`, optional `CustomTags`; result describes token, expiry and service endpoint |
| POST `/Party/RequestParty` | `EntityToken` auth; `Beta` flag; request names `PartyId`, `PreferredRegions`, optional build/version/session fields; response describes the allocated party/server |

Both are present in the vendor's [Multiplayer custom contract](https://github.com/PlayFab/API_Specs/blob/55bf2ff4b08c436ba961e4686ad2ab3929ec15f6/Legacy/PlayFab/Multiplayer.api.json). The structured index retains model references, properties, enum values and allowed entity-token categories without copying authentication examples.

**Correction to the earlier discovery result:** indexed GitHub searches missed these operation names even though this pinned repository revision contains them. Direct inspection of the repository tree and custom format resolved the gaps. The earlier [Swagger comparison](../catalog/playfab-spec-coverage.json) remains accurate for its seven Swagger files and now links this follow-up.

`Legacy` is the vendor's directory name, and the two calls carry `Beta` flags. Publication does not establish current title enablement, permission or availability. No PlayFab title request was sent. The other generic-only operations remain vendor leads rather than added AoE endpoints.

## Steam: a live API discovery operation

**GET [`/ISteamWebAPIUtil/GetSupportedAPIList/v1/`](https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1/)** returned **27 interfaces and 63 method/version entries** without a key. Entries include method name, version, HTTP method and parameter name/type/optionality. Valve explicitly documents this as its method-discovery interface; a key is needed to include restricted methods. [Vendor reference](https://partner.steamgames.com/doc/webapi/ISteamWebAPIUtil).

The [saved catalog](../catalog/steam-discovery.json) includes `GetNumberOfCurrentPlayers`, `GetGlobalAchievementPercentagesForApp` and `GetGlobalStatsForGame`, among others. It is platform metadata: no new AoE4 player-count, achievement or statistics request was made. A method's existence does not establish which game-defined stats AoE4 publishes. Method versions count separately, and the anonymous catalog is not Steam's complete API surface.

## Exact negative checks and limits

**35 completed requests**: 32 GETs and three OPTIONS, plus one planned request skipped after a 403. Seven pinned PlayFab file fetches are recorded separately. These are additional to the previous 30 documentation/source-map requests and remain separate from the original 47 API/service probes.

| Host | Completed | Outcome |
| --- | ---: | --- |
| `api.ageofempires.com` | 10 | Nine GETs redirected to the homepage; OPTIONS returned 301 |
| `aoe-api.worldsedgelink.com` | 10 | Eight JSON 404s; root `?wsdl` and OPTIONS returned HTTP 200 with empty bodies |
| `dr-activerelease1-api.worldsedgelink.com` | 10 | Same result pattern as the common host |
| `www.ageofempires.com` | 3 | `robots.txt`: 404; `/wp-json/`: valid index; `xmlrpc.php?rsd`: 403, then remaining catalog candidate skipped |
| `auth.ageofempires.com` | 1 | OpenID discovery: gateway 403; no further request |
| `api.steampowered.com` | 1 | Valid vendor discovery catalog |

The three API hosts received GETs for `/.well-known/api-catalog`, `/apis.json`, `/application.wadl`, `/?wsdl`, `/$metadata`, `/odata/$metadata`, `/metadata`, `/robots.txt`, and `/graphql` with the minimal query `{__schema{queryType{name}}}`, plus OPTIONS on `/`. No SOAP service path or GraphQL deployment was already known; these were candidates, not claims of protocol support. GraphQL checks were GET-only and did not cover alternate paths or POST-only handlers.

A 200 with no body is not WSDL. A homepage redirect is not documentation. Generic OPTIONS/CORS behavior is not an endpoint inventory or proof of per-operation permissions. No service-description links were identified in the saved response headers or inspected HTML discovery elements. The 403 responses were not bypassed; `api-dr.ageofempires.com` remained excluded after its earlier 403.

Public source review searched the 192 previously fetched publisher frontend modules for additional protocol/schema hints. It found none of the recorded search terms. A bounded search of previously saved community sources produced the already known AoE2 protobuf references, not a new publisher AoE4 reflection target. Search results do not prove absence; third-party conceptual schemas are not evidence that a publisher deploys the corresponding protocol.

The [request manifest](../catalog/alternative-discovery-requests.json) and [dated evidence](../evidence/2026-09-19/alternative-discovery.json) preserve request methods, URLs, redirects, selected headers, status, byte counts, hashes, search scope and source-fetch metadata. The live catalogs have `metadata-observed` status; their listed content/game operations remain untested.
