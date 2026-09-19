# Identifier and schema map

Preserve the source namespace instead of using a generic integer called `id` throughout an application.

| Identifier | Example / format | Meaning and integration rule |
| --- | --- | --- |
| Backend title | `age4`, `age2`, `age3`, `age1`, `athens` | Send with World’s Edge requests; title/host combinations matter |
| Game profile ID | `4635035` | Used by AoE4 World and the sampled AoE4 backend; qualify by game/title |
| SteamID64 | Decimal string, typically 17 digits | Platform identity; keep as string to avoid JavaScript integer precision loss |
| Backend platform name | `/steam/<SteamID64>` | World’s Edge profile-name lookup format; not a display alias |
| Xbox backend platform name | `/xboxlive/<identifier>` | AoECenter’s collector recognizes uppercase hexadecimal suffixes; source-only parsing convention, not a complete Xbox identity specification |
| Stat-group ID | `statGroups[].id` | Join key for leaderboard rows; does not equal `profile_id` by definition |
| Match ID | `250457718` | AoE4 World `game_id`, raw backend `id`/`matchhistory_id`, official website `matchId` |
| AoE4 World ladder | `rm_solo`, `rm_team`, `qm_1v1` | Rating grouping |
| AoE4 World game kind | `rm_4v4` | Match format; can share a ladder with other sizes |
| Backend leaderboard ID | `17` in sampled AoE4 metadata | Discover with `getAvailableLeaderboards`; title-specific |
| Backend match-type ID | `leaderboardmap[].matchtype_id` | Separate namespace; several can map to one board |
| Website event ID | `EventList[].eventId` | Seasonal event; **not** the returned `leaderboardId` |
| Website season ladder ID | `EventList[].leaderboardId` | Website passes this into EventLeaderboard’s `matchType` field |
| Mod game title ID | `4` for AoE4 | `/api/v4/mods/Games` uses numeric game IDs; Mythology returned `1001` |
| World civilization | `holy_roman_empire` | Human-oriented match/statistics key |
| Static-data civilization slug | `hre` | Path component for AoE4 World Data; use `civs-index.json` |
| Static-data abbreviation | `hr` | Key within that civilization index; differs from slug |
| Guides civilization code | `HRE` | AoE4 Guides OpenAPI enum; yet another namespace |
| Game object ID | `horseman-2`, `baseId`, numeric `pbgid` | Age/civ-specific object, unified object family, engine identifier respectively |
| Patch identifiers | `patch:11308`, `patch_id:358` in one match | Different namespaces; record the provider and game version |

Sources: [AoE4 World](https://aoe4world.com/api), [static civilization index](https://data.aoe4world.com/civilizations/civs-index.json), [Guides schemas](https://aoe4guides.com/api/api-docs/), [dated live responses](../../evidence/2026-09-19/README.md), [official website JavaScript](https://www.ageofempires.com/wp-content/themes/ageOfEmpires/public/js/main.b0837c.js).

## Observed traps

1. The official match-detail sample placed player identifiers in `playerList[].userId` while `profileId` was zero. Do not silently use `profileId=0` as a real profile. Verify the mapping against a known participant before joining. AoE4 World and raw backend IDs are clearer in the tested samples.
2. Raw backend histories were not sorted newest-first in this check. Compare timestamps, not row position.
3. A missing rank is not zero rating; a missing replay is not zero match duration; an empty history is not proof that the player never played.
4. Match team arrays can have more than two teams, and team sizes differ by mode. Do not hard-code two participants for replay discovery or FFA analysis.
5. Numeric IDs discovered for one game, season, platform or dataset version should not be applied to another without verification.
6. A returned name, country, social link or avatar may have changed since a match was played. Store match snapshots separately from current profile enrichment.

## Suggested normalized keys

For a multi-game data store, `(provider, title, native_id)` makes provenance explicit. Use a separate identity-link table for confirmed equivalences. Store UTC timestamps, original mode names, and the original relevant metadata alongside any normalized representation. Preserve unknown enum values so a new civilization or game mode does not break ingestion.

Use the static civilization index’s `id` and `slug` to join AoE4 World match data to file paths. Map Guides’ three-letter codes explicitly; lowercasing them is insufficient (`ABB` does not become `abbasid`). A generated mapping snapshot is included at [catalog/civilizations-aoe4.json](../../catalog/civilizations-aoe4.json).

AoECenter’s [collector and identity parser](../aoecenter.md#collector-and-identity-mapping) provide another concrete join example: match member to avatar by `profile_id`, then platform-prefixed identity parsing. Preserve the original identifier string; its Steam/Xbox parser does not establish formats for every platform.
