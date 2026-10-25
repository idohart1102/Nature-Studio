"""Bait/lure library v1: validate, index, resolve, per-species lookup and photo fetch. Stdlib only.

One short profile per bait type; species angling modules link bait IDs in a ```json block, so
image references resolve to exact catalog requests without browsing the library.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import re

import species_profiles as sp

ROOT = Path(__file__).resolve().parents[1]
BAIT_DIR = '01-Knowledge/equipment/baits'
SOURCES_DIR = '01-Knowledge/sources/baits'
PHOTO_MANIFEST = SOURCES_DIR + '/photo-references.json'
KINDS = {'lure': 'EQP-LURE-', 'natural': 'EQP-BAIT-'}
CATALOG_KIND = {'lure': 'equipment', 'natural': 'other'}
ID_PATTERN = r'EQP-(?:LURE|BAIT)-[A-Z0-9]+(?:-[A-Z0-9]+)*'
VARIANT_PATTERN = r'[a-z0-9]+(?:-[a-z0-9]+)*'
SECTIONS = ('## 1. Nhận dạng và cấu tạo', '## 2. Biến thể và cỡ', '## 3. Chuyển động trong nước',
            '## 4. Cách gắn và rig', '## 5. Checklist hình ảnh', '## 6. Chưa biết và giới hạn')
PHOTO_ROLES = ('identity', 'anatomy', 'assembly')
VIEWS = ('side', 'top', 'front', 'hooked', 'in-water', 'group')
# A bait profile is opened only for the bait chosen for a scene; keep it small.
PROFILE_CHAR_BUDGET = 4500


def profiles(root):
    directory = root / BAIT_DIR
    return sorted(p for p in directory.glob('*.md') if p.name != 'INDEX.md') if directory.is_dir() else []


def scan(root):
    rows, errors = [], []
    for path in profiles(root):
        relative = path.relative_to(root).as_posix()
        try:
            meta = sp.json_block(path.read_text(encoding='utf-8-sig'))
        except json.JSONDecodeError as exc:
            errors.append(f'{relative}: invalid metadata JSON: {exc}')
            continue
        if meta is None:
            errors.append(f'{relative}: missing ```json metadata block')
            continue
        rows.append(dict(path=relative, meta=meta))
    return rows, errors


def names_of(meta):
    names = [meta.get('slug', '')]
    for values in (meta.get('names') or {}).values():
        if isinstance(values, list):
            names += values
    return [n for n in names if isinstance(n, str) and n.strip()]


def variant_names(meta):
    """Declared aliases are library-wide names; bare variant ids ('standard') are only unique inside one bait."""
    out = []
    for key, value in (meta.get('variants') or {}).items():
        aliases = value.get('aliases', []) if isinstance(value, dict) else []
        out += [(key, a) for a in aliases if isinstance(a, str) and a.strip()]
    return out


def resolve(root, name):
    """Bait name or variant alias -> {id, slug, path, variant}; None when unknown or ambiguous."""
    key = sp.normalize(name)
    found = {}
    for row in scan(root)[0]:
        meta = row['meta']
        hit = dict(id=meta.get('id'), slug=meta.get('slug'), path=row['path'], variant=None)
        if key in {sp.normalize(n) for n in names_of(meta)}:
            found[(hit['id'], None)] = hit
        for variant, alias in variant_names(meta):
            if sp.normalize(alias) == key:
                found[(hit['id'], variant)] = {**hit, 'variant': variant}
        if ' ' in key:
            # "<bait> <variant id>" such as "crankbait squarebill"
            head, _, tail = key.rpartition(' ')
            if head in {sp.normalize(n) for n in names_of(meta)} and tail in (meta.get('variants') or {}):
                found[(hit['id'], tail)] = {**hit, 'variant': tail}
    return next(iter(found.values())) if len(found) == 1 else None


def load_photos(root):
    path = root / PHOTO_MANIFEST
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if data.get('schema') != 1 or not isinstance(data.get('photos'), list):
        raise ValueError(PHOTO_MANIFEST + ': schema 1 with photos list required')
    return data['photos']


def photo_tier(width, height):
    """User decision 2026-10-25: bait references need at least 1280x720, any subject coverage."""
    short, long = min(width, height), max(width, height)
    if short >= 1080 and long >= 1920:
        return '1080p'
    return '720p' if short >= 720 and long >= 1280 else None


def species_links(root):
    """Bait links declared in species angling modules: {species slug: (module path, [links])}."""
    out, errors = {}, []
    for path in sp.profiles(root):
        relative = path.relative_to(root).as_posix()
        module = sp.module_path(root, relative, 'angling')
        if not module or not sp.local(root, module).is_file():
            continue
        text = sp.local(root, module).read_text(encoding='utf-8-sig')
        block = sp.section(text, '## Mã mồi')
        if not block:
            continue
        try:
            data = sp.json_block(block)
        except json.JSONDecodeError as exc:
            errors.append(f'{module}: invalid bait JSON: {exc}')
            continue
        links = (data or {}).get('baits')
        if not isinstance(links, list):
            errors.append(f'{module}: "## Mã mồi" needs a ```json block with a "baits" list')
            continue
        out[path.stem] = (module, relative, links)
    return out, errors


def validate_profile(root, path):
    relative = path.relative_to(root).as_posix()
    text = path.read_text(encoding='utf-8-sig')
    errors, warnings = [], []
    try:
        meta = sp.json_block(text)
    except json.JSONDecodeError as exc:
        return [f'{relative}: invalid metadata JSON: {exc}'], warnings, None
    if meta is None:
        return [f'{relative}: missing ```json metadata block'], warnings, None
    bid, kind = meta.get('id'), meta.get('kind')
    if kind not in KINDS:
        errors.append(f'{relative}: kind must be lure or natural')
    elif not isinstance(bid, str) or not re.fullmatch(ID_PATTERN, bid) or not bid.startswith(KINDS[kind]):
        errors.append(f'{relative}: id must match {ID_PATTERN} with prefix {KINDS[kind]}')
    if meta.get('slug') != path.stem:
        errors.append(f'{relative}: slug must equal file name {path.stem}')
    names = meta.get('names')
    if not isinstance(names, dict) or not isinstance(names.get('en'), list) or not names['en'] \
            or any(not isinstance(v, list) or any(not isinstance(n, str) or not n.strip() for n in v) for v in names.values()):
        errors.append(f'{relative}: names.en must be a nonempty string list')
    variants = meta.get('variants')
    if not isinstance(variants, dict) or not variants:
        errors.append(f'{relative}: variants must map variant id -> {{label, aliases}}')
        variants = {}
    for key, value in variants.items():
        if not re.fullmatch(VARIANT_PATTERN, key) or not isinstance(value, dict) or not isinstance(value.get('label'), str) \
                or not isinstance(value.get('aliases', []), list):
            errors.append(f'{relative}: variant {key!r} needs a kebab-case id, label and optional aliases list')
    linked = meta.get('species_profile')
    if linked is not None and (kind != 'natural' or not any(r['meta'].get('id') == linked for r in sp.scan(root)[0])):
        errors.append(f'{relative}: species_profile must be an existing K-SP id and only for natural baits')
    legacy = meta.get('legacy_entities', [])
    if not isinstance(legacy, list) or any(not isinstance(x, str) or not x for x in legacy):
        errors.append(f'{relative}: legacy_entities must be a list of catalog entity ids')
    if meta.get('status') not in sp.STATUSES:
        errors.append(f'{relative}: status must be one of {", ".join(sp.STATUSES)}')
    for key in ('updated', 'review_due'):
        if not isinstance(meta.get(key), str) or not re.fullmatch(sp.DATE_PATTERN, meta[key]):
            errors.append(f'{relative}: {key} must be YYYY-MM-DD')
    if not isinstance(meta.get('version'), str) or not re.fullmatch(r'[0-9]+\.[0-9]+', meta['version']):
        errors.append(f'{relative}: version must be MAJOR.MINOR')
    for heading in SECTIONS:
        if heading not in text:
            errors.append(f'{relative}: missing section "{heading}"')
    ledger, problems = sp.load_sources(root, meta, relative)
    errors += problems
    if ledger:
        known, problems = sp.check_sources(ledger, meta['sources_file'], bid, key='bait_id')
        errors += problems
        cited = {s.strip() for group in sp.CITATION.findall(text) for s in group.split(',')}
        header, rows = sp.table_rows(sp.section(text, SECTIONS[1]))
        if not header or not {'Biến thể', 'Đơn vị', 'Nguồn'} <= set(header):
            errors.append(f'{relative}: size section needs a table with Biến thể/Đơn vị/Nguồn columns')
        else:
            src, var = header.index('Nguồn'), header.index('Biến thể')
            for row in rows:
                if len(row) != len(header):
                    errors.append(f'{relative}: size row has wrong column count: {row}')
                    continue
                refs = set(re.findall(r'S[0-9]+', row[src]))
                if not refs or refs - set(known):
                    errors.append(f'{relative}: size row needs known source ids: {row}')
                if row[var] not in (*variants, 'tất cả'):
                    errors.append(f'{relative}: size row variant {row[var]!r} not in metadata variants')
                cited |= refs
        errors += [f'{relative}: cites unknown source {s}' for s in sorted(cited - set(known))]
        if not any(known[s].get('tier') in ('A', 'B') and known[s].get('access') != 'not_accessed' for s in cited & set(known)):
            errors.append(f'{relative}: needs at least one cited A/B-tier source that was accessed')
        warnings += [f'{relative}: source {s} listed but never cited' for s in sorted(set(known) - cited)]
    checklist = [l for l in sp.section(text, SECTIONS[4]).splitlines() if l.lstrip().startswith('- ')]
    if not 3 <= len(checklist) <= 8:
        errors.append(f'{relative}: visual checklist needs 3-8 bullet items')
    if len(text) > PROFILE_CHAR_BUDGET:
        warnings.append(f'{relative}: {len(text)} chars > budget {PROFILE_CHAR_BUDGET}')
    if isinstance(meta.get('review_due'), str) and meta['review_due'] < dt.date.today().isoformat():
        warnings.append(f'{relative}: review_due {meta["review_due"]} passed; re-check sources')
    return errors, warnings, meta


def check_photos(root, baits):
    """baits: {id: set(variants)}. Returns errors and {id: set(variants with an identity photo)}."""
    errors, covered, seen = [], {}, set()
    try:
        photos = load_photos(root)
    except (ValueError, json.JSONDecodeError) as exc:
        return [str(exc)], covered
    for item in photos:
        key = item.get('asset_id') if isinstance(item, dict) else None
        where = f'{PHOTO_MANIFEST} {key}'
        if not isinstance(key, str) or not re.fullmatch(r'PH-(?:LURE|BAIT)-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{2}', key) or key in seen:
            errors.append(f'{where}: invalid/duplicate asset_id (PH-LURE-... or PH-BAIT-...)')
            continue
        seen.add(key)
        bid = item.get('entity_id')
        if bid not in baits:
            errors.append(f'{where}: unknown entity_id {bid}')
        elif item.get('variant') is not None and item['variant'] not in baits[bid]:
            errors.append(f'{where}: variant {item["variant"]} not in profile variants')
        roles = item.get('roles')
        if not isinstance(roles, list) or not roles or any(r not in PHOTO_ROLES for r in roles):
            errors.append(f'{where}: roles must be a subset of {", ".join(PHOTO_ROLES)}')
            roles = []
        if item.get('view') not in VIEWS:
            errors.append(f'{where}: view must be one of {", ".join(VIEWS)}')
        for field in ('page_url', 'file_url'):
            if not isinstance(item.get(field), str) or not item[field].startswith('https://'):
                errors.append(f'{where}: https {field} required')
        if not isinstance(item.get('license'), str) or not sp.LICENSE.match(item['license']):
            errors.append(f'{where}: license must be Public domain, CC0, CC BY or CC BY-SA')
        for field in ('credit', 'observed', 'basis', 'use'):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f'{where}: {field} required')
        if not isinstance(item.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', item['sha256']):
            errors.append(f'{where}: sha256 required')
        if not isinstance(item.get('reviewed'), str) or not re.fullmatch(sp.DATE_PATTERN, item['reviewed']):
            errors.append(f'{where}: reviewed date required')
        if item.get('subject_coverage') not in sp.COVERAGE:
            errors.append(f'{where}: subject_coverage must be one of {"/".join(sp.COVERAGE)}')
        width, height = item.get('width'), item.get('height')
        if type(width) is not int or type(height) is not int:
            errors.append(f'{where}: integer width/height required')
            continue
        tier = photo_tier(width, height)
        if tier is None or item.get('quality') != tier:
            errors.append(f'{where}: {width}x{height} gives tier {tier}; quality must match and be at least 720p')
        elif 'identity' in roles and bid in baits:
            covered.setdefault(bid, set()).add(item.get('variant'))
    return errors, covered


def validate(root):
    errors, warnings, ids, aliases, baits = [], [], {}, {}, {}
    for path in profiles(root):
        problems, notes, meta = validate_profile(root, path)
        errors += problems
        warnings += notes
        if not meta:
            continue
        if meta.get('id') in ids:
            errors.append(f'duplicate id {meta["id"]}: {ids[meta["id"]]} and {path.name}')
        ids[meta.get('id')] = path.name
        baits[meta.get('id')] = set(meta.get('variants') or {})
        for name in names_of(meta) + [a for _, a in variant_names(meta)]:
            key = sp.normalize(name)
            if key in aliases and aliases[key] != path.name:
                errors.append(f'alias "{name}" used by {aliases[key]} and {path.name}')
            aliases.setdefault(key, path.name)
    links, problems = species_links(root)
    errors += problems
    used = set()
    for slug, (module, profile, rows) in sorted(links.items()):
        meta = sp.metadata(root, profile) or {}
        ledger, _ = sp.load_sources(root, meta, profile)
        known = {s.get('id') for s in (ledger or {}).get('sources', [])}
        for row in rows:
            bid = row.get('id') if isinstance(row, dict) else None
            if bid not in baits:
                errors.append(f'{module}: unknown bait id {bid}')
                continue
            used.add(bid)
            bad = [v for v in row.get('variants', []) if v not in baits[bid]]
            if bad:
                errors.append(f'{module}: {bid} unknown variants {bad}')
            if not isinstance(row.get('when'), str) or not row['when'].strip():
                errors.append(f'{module}: {bid} needs "when" (season/situation, Vietnamese)')
            refs = set(re.findall(r'S[0-9]+', str(row.get('source', ''))))
            if not refs or refs - known:
                errors.append(f'{module}: {bid} source must cite ids from the {slug} ledger')
    warnings += [f'{bid}: no species module links this bait' for bid in sorted(set(baits) - used)]
    photo_errors, covered = check_photos(root, baits)
    errors += photo_errors
    for bid, variants in sorted(baits.items()):
        have = covered.get(bid, set())
        for variant in sorted(variants):
            if variant not in have:
                warnings.append(f'{bid}: no real identity photo for variant {variant}')
    expected = render_index(root)
    current = root / BAIT_DIR / 'INDEX.md'
    if ids and (not current.is_file() or current.read_text(encoding='utf-8-sig') != expected):
        errors.append(f'{BAIT_DIR}/INDEX.md is stale; run bait_profiles.py index')
    return dict(ok=not errors, errors=errors, warnings=warnings, baits=len(ids), linked_species=len(links))


def for_species(root, name, include_photos=True):
    """Compact bait rows for one species: exact catalog requests, no profile text loaded."""
    entry = sp.resolve(root, name)
    if not entry:
        raise ValueError('Unknown or ambiguous species: ' + name)
    links, _ = species_links(root)
    rows = links.get(entry['slug'], (None, None, []))[2]
    by_id = {r['meta'].get('id'): r for r in scan(root)[0]}
    photos = load_photos(root) if include_photos else []
    out = []
    for link in rows:
        found = by_id.get(link.get('id'))
        if not found:
            continue
        meta = found['meta']
        variants = link.get('variants') or sorted(meta.get('variants') or {})
        entities = [meta['id'], *meta.get('legacy_entities', [])]
        refs = [dict(asset_id=p['asset_id'], variant=p.get('variant'), view=p['view'], roles=p['roles'])
                for p in photos if p.get('entity_id') == meta['id'] and (p.get('variant') in variants or p.get('variant') is None)]
        # Per variant: the exact identity photos that fit it (its own, else type-level photos without a
        # variant) and the catalog request that returns them. Never another variant's photo; [] = no ref.
        requests = {}
        for v in variants:
            own = [p['asset_id'] for p in refs if 'identity' in p['roles'] and p['variant'] == v]
            generic = [p['asset_id'] for p in refs if 'identity' in p['roles'] and p['variant'] is None]
            requests[v] = dict(request=dict(entity_id=meta['id'], role='identity', **({'variant': v} if own else {})),
                               assets=own or generic)
        out.append(dict(id=meta['id'], name=meta['names']['en'][0], kind=meta['kind'], variants=variants,
                        when=link.get('when'), source=link.get('source'), profile=found['path'],
                        photos=refs, requests=requests,
                        legacy_requests=[dict(entity_id=e, role='anatomy') for e in entities[1:]]))
    return dict(species=entry['slug'], baits=out,
                note='Pick the one bait/variant the scene shows; select only its listed assets (query with its request, '
                     'empty assets = no photo, use the profile checklist). Open only that bait profile. '
                     'Not every listed bait suits every scene or month.')


def render_index(root):
    rows, _ = scan(root)
    links, _ = species_links(root)
    used = {}
    for slug, (_, _, items) in links.items():
        for item in items:
            used.setdefault(item.get('id'), []).append(slug)
    lines = ['# Chỉ mục mồi câu', '',
             'Sinh bằng `python scripts/bait_profiles.py index`; không sửa tay, không nạp vào context. '
             'Skill tra `bait_profiles.py for-species <loài>` hoặc `resolve "<tên mồi>"` rồi chỉ mở đúng một hồ sơ.', '']
    for kind, title in (('lure', 'Mồi giả'), ('natural', 'Mồi tự nhiên')):
        members = sorted((r for r in rows if r['meta'].get('kind') == kind), key=lambda r: r['meta'].get('slug', ''))
        if not members:
            continue
        lines += [f'## {title}', '', '| ID | Mồi | Biến thể | Loài dùng | Hồ sơ |', '|---|---|---|---|---|']
        for r in members:
            m = r['meta']
            lines.append(f"| {m.get('id')} | {m['names']['en'][0]} | {', '.join(m.get('variants', {}))} | "
                         f"{', '.join(sorted(used.get(m.get('id'), []))) or '—'} | [{m.get('slug')}]({Path(r['path']).name}) |")
        lines.append('')
    return '\n'.join(lines)


def photos_fetch(root, slug=None, fetch=None):
    photos = load_photos(root)
    kinds = {r['meta'].get('id'): r['meta'].get('kind') for r in scan(root)[0]}
    if slug:
        wanted = [r['meta'].get('id') for r in scan(root)[0] if r['meta'].get('slug') == slug]
        if not wanted:
            raise ValueError('No bait profile: ' + slug)
        photos = [p for p in photos if p.get('entity_id') in wanted]
    return sp.fetch_and_register(root, photos, lambda item: CATALOG_KIND.get(kinds.get(item['entity_id']), 'other'), fetch)


def main():
    import ns_console
    ns_console.utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('validate')
    p = sub.add_parser('index'); p.add_argument('--check', action='store_true')
    p = sub.add_parser('resolve'); p.add_argument('name')
    p = sub.add_parser('for-species'); p.add_argument('species')
    p = sub.add_parser('photos-fetch'); p.add_argument('slug', nargs='?')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == 'validate':
            result = validate(root)
            print(json.dumps(result, ensure_ascii=False, indent=1))
            return 0 if result['ok'] else 1
        if args.action == 'index':
            target = root / BAIT_DIR / 'INDEX.md'
            expected = render_index(root)
            if args.check:
                fresh = target.is_file() and target.read_text(encoding='utf-8-sig') == expected
                print('fresh' if fresh else 'stale')
                return 0 if fresh else 1
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expected, encoding='utf-8')
            print(target.relative_to(root).as_posix())
            return 0
        if args.action == 'resolve':
            found = resolve(root, args.name)
            print(json.dumps(found or dict(found=None, note='Unknown or ambiguous bait; research it, do not substitute'),
                             ensure_ascii=False))
            return 0 if found else 1
        if args.action == 'for-species':
            print(json.dumps(for_species(root, args.species), ensure_ascii=False, indent=1))
            return 0
        result = photos_fetch(root, args.slug)
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 1 if any(r['status'] == 'error' for r in result['photos']) else 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
