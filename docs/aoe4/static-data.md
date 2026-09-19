# AoE4 World Data: static game definitions

**Hosted data:** `https://data.aoe4world.com`  
**Source and generation pipeline:** [aoe4world/data](https://github.com/aoe4world/data)  
**Inspected revision:** [`b2cd38222deae40ba2db18171edf494f81410c69`](https://github.com/aoe4world/data/tree/b2cd38222deae40ba2db18171edf494f81410c69)

This is static JSON published from game-data extraction and curation, rather than a player-statistics REST service. It is especially useful for unit databases, tech trees, build planners and game-object lookup. It has no player accounts, match results, or inferred live army state.

## Paths and formats

The repository tree provides stronger path evidence than the README alone; for example, the README mentions `/upgrade/**`, while the inspected files use **`/upgrades/`**.

| Path pattern | Meaning |
| --- | --- |
| `/civilizations/civs-index.json` | Civilization index keyed by abbreviation; objects contain `id`, name, abbreviation, slug, attribute name and expansion |
| `/civilizations/{slug}.json` | Civilization metadata, e.g. `english` or `hre` |
| `/{category}/{slug}/{object-id}.json` | One civ/age-specific object; e.g. `/units/english/horseman-2.json` |
| `/{category}/{slug}.json` | All category objects for one civilization |
| `/{category}/unified/{baseId}.json` | Variants grouped by base object |
| `/{category}/all.json` | Full category list |
| `/{category}/all-unified.json` | All unified objects |
| `/{category}/all-baseids.json` | Base-ID index where present |
| `/{category}/all-optimized.json` | Optimized representation where present; inspect before consuming |
| `/{category}/{slug}-unified.json` | Per-civilization unified representation |
| `/{category}/{slug}-optimized.json` | Per-civilization optimized representation |

Categories observed in the repository: `units`, `buildings`, `technologies`, `upgrades`, `abilities`. Existence of these patterns in the source tree does not prove every conceivable category/path combination exists. Prefer the repository tree or actual index rather than manufacturing filenames. [Pinned tree](https://github.com/aoe4world/data/tree/b2cd38222deae40ba2db18171edf494f81410c69).

```bash
curl --fail-with-body \
  'https://data.aoe4world.com/civilizations/civs-index.json'

curl --fail-with-body \
  'https://data.aoe4world.com/units/english/horseman-2.json'
```

Both requests returned JSON in this research. They carried `Access-Control-Allow-Origin: *`, `Cache-Control: max-age=600`, ETag and Last-Modified headers. The latter timestamp was May 4, 2026; this does **not** independently establish alignment with the current installed game patch. No authentication or numerical rate-limit requirement was found for these reads. Cache or vendor the small definitions you need. [Live evidence](../../evidence/2026-09-19/initial-probes.json).

## Object model

The sampled horseman object includes `id`, `baseId`, `type`, name, `pbgid`, `attribName`, age, civilizations, classes, costs, hit points, weapons, armor, sight and movement. Treat available properties as category-dependent rather than forcing technologies and abilities into a unit schema.

| Field | Interpretation |
| --- | --- |
| `id` | Particular exported object/age variant, such as `horseman-2` |
| `baseId` | Object family, such as `horseman` |
| `pbgid` | Numeric engine property-bag identifier |
| `attribName` | Underlying attribute object name |
| `civs` | Exported civilization abbreviations; consult the index |
| `costs`, weapon/armor fields | Base exported properties; do not assume all situational modifiers are already applied |

The source includes parser logic and corrective workarounds. [AoE4 World Explorer](https://github.com/aoe4world/explorer) is a related consumer with additional presentation/calculation logic; a tooltip export alone should not be treated as a complete combat simulator. Images/icons are also present in the data project; use recorded asset paths rather than guessing extensions or naming conventions. [Data README and generation notes](https://github.com/aoe4world/data/blob/b2cd38222deae40ba2db18171edf494f81410c69/README.md).

## Civilization mapping

The fetched civilization index had 23 entries. Use it as an export snapshot, not a hard-coded current-game count. It explicitly links AoE4 World-style IDs to path slugs:

| Match/API ID | Static slug | Static abbreviation | Guides code |
| --- | --- | --- | --- |
| `english` | `english` | `en` | `ENG` |
| `holy_roman_empire` | `hre` | `hr` | `HRE` |
| `abbasid_dynasty` | `abbasid` | `ab` | `ABB` |
| `jeanne_darc` | `jeannedarc` | `je` | `JDA` |
| `order_of_the_dragon` | `orderofthedragon` | `od` | `DRA` |
| `house_of_lancaster` | `lancaster` | `hl` | `HOL` |

[The complete mapping snapshot](../../catalog/civilizations-aoe4.json) preserves the original static-data fields and an explicitly constructed Guides-code mapping. [Index](https://data.aoe4world.com/civilizations/civs-index.json), [Guides enum](https://aoe4guides.com/api/api-docs/).

## Reproducibility, rights and adjacent tools

For reproducible analysis, pin a repository commit and record its associated game patch when known. A `main` URL can change under you. The project documents extracting SGA archives and attribute data with [AOEMods.Essence](https://github.com/aoemods/AOEMods.Essence), then converting it into its opinionated JSON structure. Raw source game files are not shipped in the data repository.

The provider explicitly points consumers to Microsoft’s [Game Content Usage Rules](https://www.xbox.com/en-US/developers/rules). Public downloadability of data and images does not establish unrestricted redistribution or commercial rights; refer to the provider’s license/rights section for your intended reuse.

[enisn/aoe4world-mcp](https://github.com/enisn/aoe4world-mcp) adds an MCP interface around a cached normalized data snapshot. Its stated scope is factual objects and relations, not strategy generation or live match analysis. It is an optional adapter, not a new upstream game-data source, and was source-reviewed rather than installed here.
