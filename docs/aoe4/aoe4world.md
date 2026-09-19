# AoE4 World: player, match and statistics API

**Operator: independent/community project.** AoE4 World is a separate API provider, not the game publisher. Provider documentation and selected live samples are recorded separately. [Operator and evidence definitions](../publisher-services.md).

**Base:** `https://aoe4world.com/api/v0`  
**Provider documentation:** [aoe4world.com/api](https://aoe4world.com/api)  
**Operator:** independent community project; [provider FAQ](https://aoe4world.com/faq).  
**Access:** public reads need no key. The docs describe an optional `api_key` on some player-game routes for private games. This does not establish access to arbitrary private histories. No private key was used in this research.

The documentation lives at `/api`; `/api/v0` is the versioned request prefix. Do not treat the prefix alone as a health or discovery endpoint.

## Route reference

All methods below are GET. Parameters are optional unless marked **required**. This table follows the provider page; the final row is independently source-observed and live-tested.

| Path under `/api/v0` | Query parameters | Purpose / caveat |
| --- | --- | --- |
| `/players/{profile_id}` | None documented | Profile, linked public identity fields and mode statistics |
| `/players/{profile_id}/games` | `page`, `limit`, `leaderboard`, `opponent_profile_id`, `since`, `include_alts`, `api_key` | Paginated games for a player; `leaderboard` accepts ladder keys and game-kind keys |
| `/players/{profile_id}/games/{game_id}` | `include_alts`, `api_key` | One game in a profile context |
| `/players/{profile_id}/games/last` | `include_alts`, `include_stats` | Provider recommends this efficiently cached route for checking a player’s latest game |
| `/players/search` | **`query`**, `page`; `exact=true` appears in the official example | Query length at least 3; names are not unique identity keys |
| `/players/autocomplete` | **`query`**, **`leaderboard`**, `limit` (documented default 10) | Leaderboard-scoped search; query length at least 3 |
| `/leaderboards/{leaderboard}` | `page`, `query`, `country`, `profile_id` / `profile_ids`, `time` | IDs are comma-separated, up to 50; `country` uses values such as `de`, `us`, `cn` |
| `/games` | `page` (documented maximum 20), `per_page` (default 50), `profile_ids`, `leaderboard`, `since`, `updated_since`, `order` | Recent global feed; this route’s `leaderboard` means **game kind** |
| `/esports/leaderboards/{leaderboard}` | `page`, `query`, `country`, `show_inactive`, `profile_id` / `profile_ids` | Tournament Elo; provider currently documents leaderboard `1` |
| `/games/{game_id}` | No parameters verified | Used by the supplied replay launcher; returned JSON for match `250457718` in this check; absent from the main route list |

Sources: [provider reference](https://aoe4world.com/api), [pinned launcher implementation](https://github.com/EKYavsil/AoE4-Replay-Launcher/blob/7543f21d75a9cb76e5fae9c2ba104cd5a2b819e3/src/aoe4replay/aoe4world.py), [live evidence](../../evidence/2026-09-19/README.md).

### Ladder keys versus game kinds

`rm_solo` and `rm_team` identify ranked rating ladders. `rm_1v1`, `rm_2v2`, `rm_3v3`, `rm_4v4` describe game sizes. Quick-match keys include `qm_1v1` through `qm_4v4`.

For example, the tested 4v4 ranked match had:

```json
{
  "kind": "rm_4v4",
  "leaderboard": "rm_team",
  "mmr_leaderboard": "rm_4v4"
}
```

The global `/games` reference explicitly excludes `rm_solo` and `rm_team` as filter values. The player-games endpoint accepts both forms. Autocomplete and ladder URLs should use `rm_solo` instead of the older `rm_1v1` ladder alias. Console game-kind examples include `rm_1v1_console` and `qm_1v1_console`–`qm_4v4_console`; validate the relevant route before extrapolating new FFA, seasonal or console variants. [Provider reference](https://aoe4world.com/api).

### Response structures actually observed

| Response | Observed structure |
| --- | --- |
| Profile | `name`, `profile_id`, nullable `steam_id`, `site_url`, `avatars`, `country`, `social`, `modes` |
| Per-mode profile stats | Rating/rank fields, wins/losses/game counts, streak, `last_game_at`, `win_rate`; some modes include `rating_history` and `previous_seasons` |
| Search | `players`, `total_count`, `page`, `per_page`, `count`, `offset`, `next_page`, `filters` |
| Leaderboard | Ladder metadata and `players`; pagination as above; filter key is `filter` singular in this sample |
| Game | `game_id`, start/update times, `duration`, map fields, `state`, `kind`, ladder/MMR identifiers, `season`, `server`, patch fields, averages, `ongoing`, `just_finished`, `teams` |
| Game participant | In this snapshot, `teams` is an array of arrays of participant objects; fields include `profile_id`, `civilization`, result, rating/MMR deltas and `input_type` |
| Civilizations statistics | Filter metadata plus `data[]`, with civilization, rates, counts and duration aggregates |

These are sampled shapes, not required-field schemas. A historical or unranked entry can contain null ratings or missing modes. The search sample’s exact match for `beasty` was not evidence that it identified a particular professional player; confirm IDs and linked accounts.

`rating` and `mmr` are distinct fields; preserve both. A participant’s current `modes` statistics need not equal the match’s rating snapshot. Likewise, `patch` and `patch_id` are separate identifiers. In the tested match they were `11308` and `358` respectively. [Observed response shapes](../../evidence/2026-09-19/followup-probes.json).

## Aggregate statistics

| GET path under `/api/v0/stats` | Coverage |
| --- | --- |
| `/rm_solo/civilizations` | Solo ranked civ win/pick rates |
| `/rm_solo/matchups` | Solo ranked civilization pairings |
| `/rm_solo/maps` | Solo ranked map statistics |
| `/rm_solo/maps/{map_id}` | Civilization statistics on one map |
| `/qm_1v1/civilizations`, `/qm_1v1/matchups` | Quick-match 1v1 equivalents |
| `/qm_1v1/maps`, `/qm_1v1/maps/{map_id}` | Quick-match map equivalents |
| `/{mode}/civilizations` | Provider describes ranked and quick-match 2v2/3v3/4v4, e.g. `rm_2v2` and `qm_2v2` |
| `/{mode}/maps`, `/{mode}/maps/{map_id}` | Team maps described in the provider’s team section; individual combinations untested |
| `/qm_2v2/teams` | Documented civilization-pair statistics for 2v2 |

Shared filters include `patch` and `rating`; ranked modes also document `rank_level`. `maps?include_civs=true` requests more expensive analysis; the provider recommends using it only when needed. Use URL encoding for values containing comparison operators, such as `rating=>1200` or `rank_level=≥diamond`.

**Documentation drift:** the page still shows `10257` as a patch default and has a team-maps heading containing an `rm_solo` route. Those are not reliable current defaults. The tested unfiltered civ-stat response reported `patch: "10604,10884,11214,11308"`. Treat that as response metadata from this check, not a permanent patch list. Pin a supported patch filter when comparing periods and retain the returned filters with your analysis. The meaning of every aggregate denominator, including mirror-match treatment, was not independently established. [Provider reference](https://aoe4world.com/api), [stats probe](../../evidence/2026-09-19/followup-probes.json).

## Efficient polling and pagination

For a player overlay, fetch `/players/{id}/games/last`, compare the `game_id`, and fetch extra detail only on a change. `ongoing` is a reported match state, not a stream of unit positions or commands. No public AoE4 World WebSocket/webhook contract was found in the consulted documentation.

For a scoped global feed, the provider documents these paired cursors:

- `order=started_at` with `since`: track newly started games within a recent window.
- `order=updated_at` with `updated_since`: track changes to already known games; overlap the previous checkpoint slightly, then deduplicate by game ID.

Use response pagination rather than assuming a fixed number of rows. Do not repeatedly walk the maximum 20 pages. Corrections and delayed processing mean “already seen once” is not equivalent to “final.” [Provider usage notes](https://aoe4world.com/api).

```bash
curl --fail-with-body --get 'https://aoe4world.com/api/v0/players/4635035/games' \
  -H 'User-Agent: my-aoe-tool/0.1 (your project/contact URL)' \
  --data-urlencode 'limit=1' \
  --data-urlencode 'leaderboard=rm_team'
```

### Bulk exports

[The provider’s dump index](https://aoe4world.com/dumps) lists compressed historical match datasets and leaderboard exports. The inspected page includes `.json.gz` match files and `.csv.gz` leaderboard files. Download links are signed and expire; save the dataset with provenance instead of embedding a signed link permanently. Only the index was inspected here; no bulk files were downloaded or row-level completeness tested.

### Access, caching and errors

The provider asks clients to identify themselves in `User-Agent`, cache responses, use incremental parameters and avoid bulk API crawling. No numerical general rate limit is published on the inspected API page. Handle 429 and `Retry-After`; a guessed requests-per-second budget is not a service guarantee.

The tested routes returned `Access-Control-Allow-Origin: *` and ETags. Their `Cache-Control` included `private, must-revalidate`; do not infer a shared-cache TTL from the provider’s internal caching recommendation. Conditional requests or an application cache must follow the response and your authorization context. Keep private-game keys out of published URLs and logs, and private responses out of shared caches.

The esports endpoint returned a valid empty result for the selected ordinary player. That verifies the response envelope, not population of the tournament ladder. Full match-summary analysis is distinct from ordinary game metadata; no summary endpoint is promoted to a supported public route merely because a website page displays build orders or economy charts.
