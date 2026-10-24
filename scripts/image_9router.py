"""Fallback first-frame call through a local 9router gateway (Codex image tool, Sunburst requested).

One run sends exactly one request; reserve the budget before calling. Writes the output image and a
sidecar JSON record, never overwrites, and never prints the API key. Does not judge image quality.
"""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import base64
import hashlib
import json
import os
import re
import struct
import time
import urllib.error
import urllib.request

DEFAULT_BASE = 'http://localhost:20128/v1'
DEFAULT_MODEL = 'cx/gpt-image-2.5-sunburst'
KEY_FILE = '.nature-studio/9router.key'
ORIENTATION_WORDS = re.compile(r'\b(vertical|portrait|9:16|2:3|horizontal|landscape|16:9|3:2|square|1:1)\b', re.I)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def api_key(root):
    key = os.environ.get('NINEROUTER_API_KEY', '').strip()
    if key:
        return key, 'env:NINEROUTER_API_KEY'
    path = root / KEY_FILE
    if path.is_file() and path.read_text(encoding='utf-8').strip():
        return path.read_text(encoding='utf-8').strip(), KEY_FILE
    raise ValueError(f'Missing 9router API key: set NINEROUTER_API_KEY or save it in {KEY_FILE}')


def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        return None, None
    return struct.unpack('>II', data[16:24])


def c2pa_agent(data):
    """Provenance hint only; OpenAI currently writes a generic 'gpt-image', not the model variant."""
    match = re.search(rb'softwareAgent.{0,40}?version.{0,2}([A-Za-z0-9._-]+)', data[:200000], re.S)
    return match.group(1).decode('ascii', 'replace') if match else None


def check(root, base_url=DEFAULT_BASE, timeout=5):
    """Gateway reachable and key present; does not prove the account can generate images."""
    result = dict(base_url=base_url, gateway='unreachable', key_source=None)
    try:
        with urllib.request.urlopen(base_url.rstrip('/') + '/models', timeout=timeout) as response:
            result['gateway'] = 'ok' if response.status == 200 else f'http_{response.status}'
    except (urllib.error.URLError, OSError) as exc:
        result['error'] = str(exc)
    try:
        result['key_source'] = api_key(root)[1]
    except ValueError as exc:
        result['key_error'] = str(exc)
    result['ready'] = result['gateway'] == 'ok' and result['key_source'] is not None
    return result


def generate(root, prompt_file, out, images=(), size=None, quality=None, model=DEFAULT_MODEL,
             base_url=DEFAULT_BASE, timeout=900, opener=urllib.request.urlopen):
    out = Path(out).resolve()
    record_path = out.with_suffix('.9router.json')
    if out.exists() or record_path.exists():
        raise ValueError('Output exists; use a new attempt path, never overwrite')
    prompt = Path(prompt_file).read_text(encoding='utf-8-sig')
    key, key_source = api_key(root)
    inputs, encoded = [], []
    for path in images:
        data = Path(path).read_bytes()
        inputs.append(dict(path=str(Path(path).resolve()), sha256=sha256(data)))
        encoded.append(base64.b64encode(data).decode('ascii'))
    body = dict(model=model, prompt=prompt)
    if encoded:
        body['images'] = encoded
    if size:
        body['size'] = size
    if quality:
        body['quality'] = quality
    warnings = []
    if size and not ORIENTATION_WORDS.search(prompt):
        warnings.append('size is not enforced by this route; state orientation/aspect in the prompt')
    record = dict(schema=1, route='9router', endpoint=base_url.rstrip('/') + '/images/generations',
                  requested_model=model.split('/')[-1], model_param=model, selection_mode='9router_sunburst',
                  actual_model='unknown', model_verified=False, key_source=key_source,
                  started_at=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                  tool=dict(name='9router_image', arguments=dict(
                      prompt=prompt, referenced_image_paths=[i['path'] for i in inputs], size=size, quality=quality)),
                  prompt_sha256=sha256(prompt.encode('utf-8')), inputs=inputs, warnings=warnings)
    request = urllib.request.Request(record['endpoint'], data=json.dumps(body).encode('utf-8'), method='POST',
                                     headers={'content-type': 'application/json', 'authorization': 'Bearer ' + key})
    started = time.monotonic()
    try:
        with opener(request, timeout=timeout) as response:
            payload = json.loads(response.read())
        b64 = (payload.get('data') or [{}])[0].get('b64_json')
        if not b64:
            raise ValueError('Gateway returned no image')
        data = base64.b64decode(b64)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        width, height = png_size(data)
        record.update(outcome='success', output=dict(path=str(out), sha256=sha256(data)), width=width, height=height,
                      c2pa_software_agent=c2pa_agent(data))
    except urllib.error.HTTPError as exc:
        record.update(outcome='error', http_status=exc.code, error=exc.read()[:500].decode('utf-8', 'replace'))
    except (urllib.error.URLError, OSError, ValueError, json.JSONDecodeError) as exc:
        # Timeout or dropped connection: the remote call may still have run.
        record.update(outcome='unknown' if isinstance(exc, (urllib.error.URLError, OSError)) else 'error',
                      error=str(exc))
    record['latency_seconds'] = round(time.monotonic() - started, 1)
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    record['record'] = str(record_path)
    record['tool']['arguments'].pop('prompt')
    return record


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'generate'])
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--base-url', default=os.environ.get('NINEROUTER_BASE_URL', DEFAULT_BASE))
    parser.add_argument('--prompt-file')
    parser.add_argument('--out')
    parser.add_argument('--image', action='append', default=[], help='Ordered input image; repeat for several')
    parser.add_argument('--size', help='Hint only, e.g. 1024x1536; state orientation in the prompt too')
    parser.add_argument('--quality', choices=['low', 'medium', 'high'])
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args()
    try:
        if args.action == 'check':
            result = check(args.root, args.base_url)
        else:
            if not args.prompt_file or not args.out:
                raise ValueError('generate needs --prompt-file and --out')
            result = generate(args.root, args.prompt_file, args.out, args.image, args.size, args.quality,
                              args.model, args.base_url, args.timeout)
        print(json.dumps(result, ensure_ascii=False))
        if result.get('outcome') not in (None, 'success') or result.get('ready') is False:
            raise SystemExit(2)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'{exc}\n')
