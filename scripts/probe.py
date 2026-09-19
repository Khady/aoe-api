#!/usr/bin/env python3
"""Small, opt-in, read-only HTTP probes. Python 3.10+, standard library only."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib

ROOT = Path(__file__).resolve().parents[1]
UA = 'aoe-api-research/0.1 (public API documentation research)'
MAX_BYTES = 2_000_000

def shape(value, depth=0):
    """Sample structure only: do not retain player data or signed URLs."""
    if depth >= 7:
        return type(value).__name__
    if isinstance(value, dict):
        return {k: shape(v, depth + 1) for k, v in value.items()}
    if isinstance(value, list):
        return {'type': 'array', 'length': len(value),
                'first_item_shape': shape(value[0], depth + 1) if value else None}
    return 'null' if value is None else type(value).__name__

def safe_url(url):
    parts = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    if any(k.lower() in {'sig', 'signature', 'token', 'api_key', 'key', 'access_token'} for k, _ in query):
        return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, 'REDACTED', ''))
    return url

def probe(item):
    url = item['url']
    if item.get('params'):
        url += ('&' if '?' in url else '?') + urllib.parse.urlencode(item['params'])
    method = item.get('method', 'GET')
    if method not in {'GET', 'HEAD'} and not (method == 'POST' and item.get('read_only')):
        raise ValueError('Only read-only probes are supported')
    body = json.dumps(item['json']).encode() if 'json' in item else None
    headers = {'User-Agent': UA, 'Accept': 'application/json', 'Accept-Encoding': 'identity',
               'Origin': 'https://example.org'}
    if body is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    out = {'id': item['id'], 'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(),
           'method': method, 'url': safe_url(url)}
    start = time.monotonic()
    try:
        try:
            response = urllib.request.urlopen(req, timeout=20)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            data = response.read(MAX_BYTES + 1)
            out.update(http_status=response.status, final_url=safe_url(response.url),
                       headers={k.lower(): v for k, v in response.headers.items()
                                if k.lower() in {'content-type', 'content-encoding', 'cache-control',
                                                 'etag', 'last-modified', 'retry-after', 'content-disposition',
                                                 'access-control-allow-origin', 'content-length'}
                                or k.lower().startswith(('x-ratelimit', 'ratelimit'))},
                       bytes_read=len(data), truncated=len(data) > MAX_BYTES,
                       sha256=hashlib.sha256(data).hexdigest())
        try:
            parsed = json.loads(data)
        except (ValueError, UnicodeError):
            if data.startswith(b'\x1f\x8b'):
                try:
                    prefix = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data, 65536)
                    out['gzip_prefix_contains_aoe4_signature'] = b'AOE4_RE' in prefix
                except zlib.error:
                    out['gzip_prefix_valid'] = False
            out['body_kind'] = ('html' if b'<html' in data[:2000].lower()
                                or b'<!doctype html' in data[:2000].lower() else 'non-json')
        else:
            out['body_kind'] = 'json'
            out['sampled_shape'] = shape(parsed)
            if isinstance(parsed, dict) and isinstance(parsed.get('result'), dict):
                out['application_result'] = {k: parsed['result'][k] for k in ('code', 'message')
                                             if k in parsed['result']}
            if isinstance(parsed, dict):
                status_fields = ('statusCode', 'errorCode', 'errorMessage', 'error', 'message')
                out['application_status_fields'] = {k: parsed[k] for k in status_fields
                                                    if k in parsed and not isinstance(parsed[k], (dict, list))}
            if item.get('metadata_fields') and isinstance(parsed, dict):
                out['metadata'] = {k: parsed[k] for k in item['metadata_fields'] if k in parsed}
            if item.get('save_metadata_body'):
                # Only non-personal discovery metadata is opted into by the manifest.
                out['discovery_metadata'] = parsed
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        out['transport_error'] = str(exc)
    out['duration_ms'] = round((time.monotonic() - start) * 1000)
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT/'catalog/probes.json')
    parser.add_argument('--only', help='Comma-separated probe ids; omit for the entire small manifest')
    parser.add_argument('--live', action='store_true', help='Actually send requests; default is dry run')
    parser.add_argument('--output', type=Path, help='JSON results destination; required with --live')
    parser.add_argument('--delay', type=float, default=2.0, help='Seconds between requests, minimum 1')
    args = parser.parse_args()
    items = json.loads(args.manifest.read_text())
    if args.only:
        selected = set(args.only.split(','))
        missing = selected - {i['id'] for i in items}
        if missing:
            parser.error(f'Unknown probe ids: {sorted(missing)}')
        items = [i for i in items if i['id'] in selected]
    if not args.live:
        for item in items:
            print(item['id'], item.get('method', 'GET'), item['url'])
        return
    if not args.output:
        parser.error('--output is required for live runs')
    if args.output.exists():
        parser.error('Output already exists; choose a new path to preserve prior evidence')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    results = []
    for index, item in enumerate(items):
        if index:
            time.sleep(max(1.0, args.delay))
        result = probe(item)
        results.append(result)
        args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False)+'\n')
        print(item['id'], result.get('http_status', 'transport-error'),
              result.get('body_kind', ''), result.get('application_result', ''), flush=True)
        if result.get('http_status') == 429:
            print('Stopping on rate limit; no automatic retries.', flush=True)
            break

if __name__ == '__main__':
    main()
