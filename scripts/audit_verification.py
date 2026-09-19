#!/usr/bin/env python3
"""Summarize saved publisher API probes offline; never sends network requests."""

import argparse
from collections import Counter
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLISHER_HOSTS = {
    "aoe-api.worldsedgelink.com": "worlds-edge",
    "dr-activerelease1-api.worldsedgelink.com": "worlds-edge",
    "athens-live-api.worldsedgelink.com": "worlds-edge",
    "aoe-api.reliclink.com": "worlds-edge",
    "api.ageofempires.com": "official-website",
    "auth.ageofempires.com": "official-account",
}


def read(path):
    return json.loads(path.read_text())


def relative(path):
    return str(path.resolve().relative_to(ROOT))


def summarize(evidence_dir):
    endpoints = read(ROOT / "catalog/endpoints.json")["endpoints"]
    services = read(ROOT / "catalog/services.json")["services"]
    manifest = {row["id"]: row for row in read(ROOT / "catalog/probes.json")}
    files = sorted(evidence_dir.glob("*probes.json"))
    if not files:
        raise ValueError("No saved *probes.json reports found")
    records = []
    seen = set()
    for file in files:
        for record in read(file):
            if record["id"] in seen:
                raise ValueError(f"Duplicate probe ID: {record['id']}")
            seen.add(record["id"])
            if record["id"] not in manifest:
                raise ValueError(f"Probe missing from manifest: {record['id']}")
            records.append((file, record))

    publisher_records = []
    by_endpoint = {}
    for file, row in records:
        url = urlsplit(row["url"])
        service = PUBLISHER_HOSTS.get(url.hostname)
        if service is None:
            continue
        matches = [
            endpoint for endpoint in endpoints
            if endpoint["service"] == service
            and endpoint["path"].rstrip("/") == url.path.rstrip("/")
            and row["method"] in endpoint.get(
                "documented_methods", [endpoint["method"]]
            )
        ]
        if len(matches) != 1:
            raise ValueError(f"Ambiguous/missing catalog match: {row['id']}")
        endpoint = matches[0]
        status = row.get("http_status")
        application = row.get("application_result") or row.get(
            "application_status_fields", {}
        )
        if status is None:
            outcome = "transport-error"
        elif status >= 400:
            outcome = "http-error"
        elif any(application.get(key) not in (None, 0)
                 for key in ("code", "statusCode", "errorCode")):
            outcome = "application-error"
        elif status == 200:
            outcome = "http-200-response-observed"
        else:
            outcome = "other-http-response"
        params = manifest[row["id"]].get("params", {})
        title = params.get("title") or parse_qs(url.query).get("title", [None])[0]
        sample = {
            "probe_id": row["id"],
            "endpoint_id": endpoint["id"],
            "service": service,
            "method": row["method"],
            "path": url.path,
            "host": url.hostname,
            "title_parameter": title,
            "checked_at": row["checked_at"],
            "http_status": status,
            "body_kind": row.get("body_kind"),
            "application_result": application,
            "outcome": outcome,
            "evidence_file": relative(file),
        }
        publisher_records.append(sample)
        group = by_endpoint.setdefault(endpoint["id"], {
            "endpoint_id": endpoint["id"], "service": service,
            "method": endpoint["method"], "path": endpoint["path"],
            "probe_ids": [], "http_200_probe_ids": [], "other_probe_ids": [],
        })
        group["probe_ids"].append(row["id"])
        bucket = "http_200_probe_ids" if outcome == "http-200-response-observed" else "other_probe_ids"
        group[bucket].append(row["id"])

    families = []
    for service, prefix, label in [
        ("worlds-edge", "/community/", "Publisher community namespace"),
        ("worlds-edge", "/game/", "Publisher game-client namespace"),
        ("official-website", "/", "Publisher website APIs"),
        ("official-account", "/", "Publisher account website API"),
    ]:
        subset = [e for e in endpoints if e["service"] == service and e["path"].startswith(prefix)]
        ids = {e["id"] for e in subset}
        groups = [g for eid, g in by_endpoint.items() if eid in ids]
        families.append({
            "label": label, "service": service, "prefix": prefix,
            "catalog_route_patterns": len(subset),
            "routes_with_http_200_sample": sum(bool(g["http_200_probe_ids"]) for g in groups),
            "routes_with_only_error_samples": sum(not g["http_200_probe_ids"] for g in groups),
            "routes_without_direct_probe": len(subset) - len(groups),
            "counting_note": "Counts routes assigned to this catalog service, excludes emulator-only upstream candidates; not a complete service denominator.",
        })
    candidates = [e for e in endpoints if "upstream_candidate" in e]
    coverage = read(ROOT / "catalog/agelanserver-coverage.json")
    game_protocol_requests = [
        row for _, row in records
        if (urlsplit(row["url"]).hostname or "").endswith(".playfabapi.com")
        or (
            urlsplit(row["url"]).hostname in PUBLISHER_HOSTS
            and urlsplit(row["url"]).path.startswith(("/game/", "/wss/"))
        )
    ]
    return {
        "evidence_period": {
            "first_probe_at": min(r["checked_at"] for _, r in records),
            "last_probe_at": max(r["checked_at"] for _, r in records),
        },
        "method": "Offline audit of saved observations; no new endpoint requests. Operator provenance, source existence, and runtime verification are separate.",
        "input_files": [relative(file) for file in files],
        "all_services": {
            "recorded_requests": len(records),
            "http_status_counts": dict(Counter(str(r.get("http_status") or "transport-error") for _, r in records)),
            "operator_categories": dict(Counter(s["operator"]["category"] for s in services)),
        },
        "publisher_http": {
            "recorded_requests": len(publisher_records),
            "outcome_counts": dict(Counter(r["outcome"] for r in publisher_records)),
            "distinct_catalog_routes_attempted": len(by_endpoint),
            "distinct_routes_with_http_200_sample": sum(bool(g["http_200_probe_ids"]) for g in by_endpoint.values()),
            "distinct_routes_with_only_error_samples": sum(not g["http_200_probe_ids"] for g in by_endpoint.values()),
            "route_counting_rule": "Group by catalog endpoint ID; repeated samples, game titles and release/legacy hosts do not create new route patterns. Source path casing is preserved.",
            "families": families,
            "routes": sorted(by_endpoint.values(), key=lambda g: (g["service"], g["path"])),
            "samples": sorted(publisher_records, key=lambda r: r["checked_at"]),
        },
        "emulator_upstream_candidates": {
            "route_patterns": len(candidates),
            "families": dict(Counter(e["upstream_candidate"]["family"] for e in candidates)),
            "directly_probed_route_patterns": sum(
                e["verification"].get("probe_id") in seen for e in candidates
            ),
            "endpoint_ids": [e["id"] for e in candidates],
        },
        "source_only_game_protocol": {
            "aoe4_game_router_operations_in_emulator": coverage["summary"]["game_router_per_title"]["age4"],
            "playfab_api_operations_in_emulator": coverage["summary"]["playfab_api_operations"],
            "aoe4_playfab_operations_in_emulator": coverage["summary"]["playfab_api_per_title"]["age4"],
            "live_requests_recorded": len(game_protocol_requests),
        },
        "limits": [
            "HTTP 200 is an observation, not a complete schema/correctness check. Empty/default results remain part of the evidence.",
            "A 401 establishes rejection of the submitted request, not a working authenticated operation; a TLS failure establishes no response from the intended service.",
            "No authenticated game session, PlayFab title API, WebSocket stream, relay transport or local replay gRPC was runtime-tested.",
            "Source review dates and recent commits do not refresh old runtime evidence. This report does not claim availability after the recorded probe dates.",
            "No global verification percentage is given: the total publisher API surface is unknown and emulator entries overlap other references.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=ROOT / "evidence/2026-09-19")
    parser.add_argument("--output", type=Path, default=ROOT / "catalog/verification-summary.json")
    parser.add_argument("--check", action="store_true", help="Check the saved summary without modifying it")
    args = parser.parse_args()
    summary = summarize(args.evidence_dir)
    if args.check:
        if read(args.output) != summary:
            raise SystemExit("Verification summary differs from the saved evidence")
        print("Verification summary matches the saved evidence.")
    else:
        args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
