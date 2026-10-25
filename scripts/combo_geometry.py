"""Deterministic staging-geometry check for one content set. Stdlib only.

The writer keeps positions once in geometry.json; this script checks frame/visibility/line-length/
speed arithmetic and renders geometry.md, so reviewers spend rounds on story and biology instead of
sums. It never judges whether a staging choice is good, only whether the numbers agree.
"""
import argparse
import json
import math
from pathlib import Path

# Vertical 9:16 staging model used by Underwater geometry: frame width ≈ 0.63·z, height ≈ 1.10·z.
DEFAULT_CAMERA = dict(half_width=0.31, half_height=0.55)
MINOR = 0.10  # overflow up to 10% of the limit is a reviewer "minor", not a FAIL


def span(value):
    """Number or [min, max] -> (min, max)."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value), float(value)
    if isinstance(value, list) and len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
        low, high = sorted(map(float, value))
        return low, high
    raise ValueError(f'coordinate must be a number or [min, max]: {value!r}')


def centre(value):
    low, high = span(value)
    return (low + high) / 2


def load(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    if not isinstance(data.get('items'), list) or not data['items']:
        raise ValueError('geometry.json needs a nonempty "items" list')
    return data


def check(data):
    camera = {**DEFAULT_CAMERA, **(data.get('camera') or {})}
    visibility = data.get('visibility_m')
    errors, warnings = [], []
    rows = []
    for index, item in enumerate(data['items']):
        where = f"{item.get('name', '?')} @ t={item.get('t')}"
        try:
            t = float(item['t'])
            x, y, z = span(item['x']), span(item['y']), span(item['z'])
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f'{where}: {exc}')
            continue
        if z[0] <= 0:
            errors.append(f'{where}: z must be > 0 (distance from lens)')
            continue
        rows.append(dict(item, _t=t, _x=x, _y=y, _z=z, _i=index))
        key = bool(item.get('key'))
        if not item.get('exits'):
            for axis, extent, ratio in (('x', max(abs(x[0]), abs(x[1])), camera['half_width']),
                                        ('y', max(abs(y[0]), abs(y[1])), camera['half_height'])):
                limit = ratio * z[0]
                if extent > limit:
                    over = (extent - limit) / limit
                    message = f'{where}: |{axis}| {extent:.2f} > frame limit {limit:.2f} at z {z[0]:.2f} (+{over:.0%})'
                    (errors if key or over > MINOR else warnings).append(message + ('' if key or over > MINOR else ' [minor]'))
        if visibility and item.get('readable', True) and z[1] > visibility:
            message = f'{where}: z {z[1]:.2f} m beyond readable water {visibility} m'
            (errors if key else warnings).append(message)
    by_name = {}
    for row in rows:
        by_name.setdefault(row['name'], []).append(row)
    for link in data.get('links', []):
        a, b, limit = link.get('a'), link.get('b'), link.get('max_m')
        if a not in by_name or b not in by_name or not isinstance(limit, (int, float)):
            errors.append(f'link {a}–{b}: both items and numeric max_m required')
            continue
        times_b = {r['_t']: r for r in by_name[b]}
        shared = [r for r in by_name[a] if r['_t'] in times_b]
        if not shared:
            warnings.append(f'link {a}–{b}: no shared time to check')
        for ra in shared:
            rb = times_b[ra['_t']]
            distance = math.dist([centre(ra['x']), centre(ra['y']), centre(ra['z'])],
                                 [centre(rb['x']), centre(rb['y']), centre(rb['z'])])
            if distance > limit * 1.02:
                errors.append(f"link {a}–{b} @ t={ra['_t']}: {distance:.2f} m > {link.get('label', 'max')} {limit} m")
    for rule in data.get('speeds', []):
        name, limit = rule.get('item'), rule.get('max_mps')
        track = sorted(by_name.get(name, []), key=lambda r: r['_t'])
        if not track or not isinstance(limit, (int, float)):
            errors.append(f'speed {name}: known item and numeric max_mps required')
            continue
        for previous, current in zip(track, track[1:]):
            dt = current['_t'] - previous['_t']
            if dt <= 0:
                continue
            distance = math.dist([centre(previous['x']), centre(previous['y']), centre(previous['z'])],
                                 [centre(current['x']), centre(current['y']), centre(current['z'])])
            if distance / dt > limit:
                errors.append(f"speed {name} {previous['_t']}→{current['_t']} s: {distance / dt:.2f} m/s > {limit} m/s")
    keys = [r for r in rows if r.get('key')]
    if not keys:
        errors.append('mark the key/payoff subject rows with "key": true')
    return dict(ok=not errors, errors=errors, warnings=warnings, items=len(rows), camera=camera,
                note='Arithmetic only: frame, visibility, line/leader length, speed. Staging quality stays with the reviewer.')


def fmt(value):
    low, high = span(value)
    return f'{low:+.2f}' if low == high else f'{low:+.2f}…{high:+.2f}'


def render(data, result):
    camera = result['camera']
    lines = [f"# Geometry — {data.get('title', '')}".rstrip(' —'), '',
             f"Sinh từ geometry.json bằng `python scripts/combo_geometry.py render`; sửa số trong JSON, không sửa tay file này. "
             f"Camera: nửa rộng {camera['half_width']}·z, nửa cao {camera['half_height']}·z; nước đọc được tới "
             f"{data.get('visibility_m', '—')} m.", '']
    if data.get('notes'):
        lines += [data['notes'], '']
    lines += ['| Item | t (s) | x (m) | y (m) | z (m) | Hướng | Ghi chú |', '|---|---|---|---|---|---|---|']
    for item in sorted(data['items'], key=lambda i: (float(i.get('t', 0)), i.get('name', ''))):
        flags = [f for f, on in (('KEY', item.get('key')), ('ra khung', item.get('exits'))) if on]
        lines.append(f"| {item['name']} | {item['t']} | {fmt(item['x'])} | {fmt(item['y'])} | {fmt(item['z'])} | "
                     f"{item.get('heading', '')} | {' · '.join(flags + ([item['note']] if item.get('note') else []))} |")
    if data.get('links'):
        lines += ['', 'Ràng buộc dây/khoảng cách: ' + '; '.join(f"{l['a']}–{l['b']} ≤ {l['max_m']} m ({l.get('label', '')})"
                                                          for l in data['links'])]
    lines += ['', f"Kiểm số: {'ĐẠT' if result['ok'] else 'LỖI'} — {len(result['errors'])} lỗi, {len(result['warnings'])} cảnh báo."]
    lines += [f'- LỖI: {e}' for e in result['errors']] + [f'- cảnh báo: {w}' for w in result['warnings']]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    for name in ('check', 'render'):
        p = sub.add_parser(name)
        p.add_argument('geometry', type=Path)
    args = parser.parse_args()
    try:
        data = load(args.geometry)
        result = check(data)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f'{exc}\n')
    if args.action == 'render':
        target = args.geometry.with_name('geometry.md')
        target.write_text(render(data, result), encoding='utf-8')
        result['written'] = str(target)
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
