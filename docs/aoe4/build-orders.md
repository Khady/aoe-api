# AoE4 Guides: build-order API

**Operator: independent/community project.** Its provider-published API specification is not a game-publisher specification. [Operator and evidence definitions](../publisher-services.md).

This API serves community-authored build orders and their overlay representation. It does not serve match history or compute a build order from a replay.

- [Provider Swagger UI](https://aoe4guides.com/api/api-docs/)
- [Provider source](https://github.com/jensbuehl/aoe4-guides-api)
- [Dated OpenAPI snapshot](../../evidence/2026-09-19/aoe4guides-openapi.json), advertised version **1.16.0**

## Base URL: important correction

The live Swagger `servers` entry is:

```text
https://aoe4-guides-api-7h2vti5ckq-ey.a.run.app
```

Use it directly for the full API. A live request to `https://aoe4guides.com/api/builds?civ=ENG` returned HTTP 404 with `error: "not_proxied"`; the response explains that the website proxies **only** `/api/builds/{buildId}` and `/api/api-docs/`. The equivalent `/builds?civ=ENG` request on the Cloud Run host returned 10 build objects.

Some repository examples still advertise the website list URL. Prefer the current live Swagger and observed response over those examples. [Evidence](../../evidence/2026-09-19/initial-probes.json), [successful direct-host checks](../../evidence/2026-09-19/followup-probes.json).

## Endpoints

All methods are GET; the live specification describes them as public, read-only and requiring no API key.

| Path on the direct API host | Parameters | Response / use |
| --- | --- | --- |
| `/` | None | Welcome/API information |
| `/status` | None | Status object; returned HTTP 200 JSON in this check |
| `/builds` | `civ`, `author`, `orderBy`, `overlay` | List, at most 10 results; **no pagination** in the published contract |
| `/builds/{buildId}` | `overlay` | One build; `buildId` is an opaque string |
| `/favorites/{userId}` | `civ`, `author`, `orderBy`, `overlay` | A user’s public favorites list; user ID is the Guides identity, not a Relic profile ID |

`orderBy` values: `score`, `timeCreated`, `views`, `likes`; the schema says sorting is descending. `overlay` defaults to false. `author` filters by author ID; do not confuse it with the displayed author name.

The civilization enum is `ANY`, `ENG`, `FRE`, `RUS`, `MAL`, `DEL`, `HRE`, `ABB`, `OTT`, `CHI`, `MON`, `BYZ`, `JAP`, `AYY`, `JDA`, `ZXL`, `DRA`, `HOL`, `KTE`, `GOH`, `SEN`, `MAC`, `TUG`, `JIN`. `ANY` is a filter value, not an extra playable civilization. Treat this as a dated enum snapshot. [Live specification](https://aoe4guides.com/api/api-docs/).

```bash
curl --fail-with-body --get \
  'https://aoe4-guides-api-7h2vti5ckq-ey.a.run.app/builds' \
  -H 'User-Agent: my-aoe-tool/0.1 (your project/contact URL)' \
  --data-urlencode 'civ=ENG' \
  --data-urlencode 'orderBy=score' \
  --data-urlencode 'overlay=true'
```

## Schema notes

The observed full list is a JSON array, not a `{data: ...}` envelope. Sample build fields include `id`, `title`, `description`, `author`, `authorUid`, `civ`, `season`, `strategy`, `steps`, `video`, vote/view counters and score fields. `steps` can contain age and age-up groups with nested steps.

Resource and worker counts in the sample step objects were strings, sometimes empty strings. `timeCreated` and `timeUpdated` were objects containing `_seconds` and `_nanoseconds`, not ISO date strings. Render missing/blank values deliberately rather than coercing them to zero. Use the separate overlay schemas for `overlay=true`; that is a transformation, not a guarantee of the full schema. The tested website-proxied overlay returned `name`, `civilization`, `author`, `source`, and `build_order[]`, with numeric resource counts and `-1` sentinels in some unavailable count fields.

The live OpenAPI snapshot is the best local source for complete property definitions. The inspected GitHub `develop` branch and deployed spec can differ; do not assume a branch checkout exactly describes the deployed release.

## Rate limits, caching and attribution

The live provider specification publishes:

| Route class | Per-IP limit | Cache guidance |
| --- | --- | --- |
| Lists, including builds/favorites | 30 requests/minute and 300/hour | Responses may be cached for 60 seconds |
| Individual `/builds/{buildId}` | 120/minute and 1,200/hour | Responses may be cached for 5 minutes |

A list probe returned `Cache-Control: public, max-age=60`, `RateLimit`/`RateLimit-Policy` headers and `Access-Control-Allow-Origin: *`. HTTP 429 signals exceeded limits. These are documented limits, not stress-tested thresholds. The provider expects attribution and a link to AoE4 Guides and offers contact for higher-volume use. Source code is MIT-licensed; do not infer that every community-authored description or game asset has identical licensing. [Provider documentation](https://aoe4guides.com/api/api-docs/).

## Related client library

[Orda](https://github.com/gzordrai/orda) is a Rust wrapper exposing status, builds, individual build and favorites operations. It is a wrapper around this service, not a separate data provider. Verify its configured base URL against the current host split before adopting it; the library itself was not installed or tested here.
