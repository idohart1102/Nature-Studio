"""Species profile standard v3: scaffold, validate, index, resolve and snapshot sources. Stdlib only.

Profiles stay the single source of facts. This helper parses their JSON metadata
block and source ledger; it never rewrites a profile or judges biology. Project
context-maps still decide which species a Project may use; resolve only maps an
alias to one profile so no other species is read.
"""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import unicodedata
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SPECIES_DIR = '01-Knowledge/species'
SNAPSHOT_DIR = '.nature-studio/knowledge-snapshots'
GROUPS = ('fish', 'mammal', 'bird', 'reptile', 'amphibian', 'invertebrate', 'plant', 'other')
STATUSES = ('draft', 'researched', 'reviewed', 'stale')
TIERS = ('A', 'B', 'C', 'D', 'E')
ACCESS = ('opened', 'indexed-only', 'not_accessed')
SIZE_KINDS = ('typical', 'large', 'record', 'estimate')
# Only angling is routed by chayvideo_context today; wire a module there before relying on it.
MODULES = ('angling', 'hunting', 'life-cycle', 'seasonal', 'sign')
SECTIONS = ('## 1. Nhận dạng', '## 2. Kích cỡ và giai đoạn', '## 3. Sinh cảnh và phân bố',
            '## 4. Hành vi', '## 5. Tương tác', '## 6. Điểm đáng xem',
            '## 7. Checklist hình ảnh', '## 8. Chưa biết và giới hạn')
# Soft budget: one profile is read whole for every task on that species.
PROFILE_CHAR_BUDGET = 9000
ID_PATTERN = r'K-SP-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}'
DATE_PATTERN = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
JSON_BLOCK = re.compile(r'```json\n(.*?)\n```', re.S)
CITATION = re.compile(r'\[(S[0-9]+(?:\s*,\s*S[0-9]+)*)\]')


def local(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative or relative.startswith('/'):
        raise ValueError('Use a workspace-relative path with forward slashes: ' + str(relative))
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Path outside workspace: ' + relative)
    return path


def normalize(name):
    """Alias key: case/diacritics/separators folded; đ is not decomposed by NFKD."""
    text = unicodedata.normalize('NFKD', name.replace('đ', 'd').replace('Đ', 'D'))
    text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
    return ' '.join(re.split(r'[\s_\-/]+', text)).strip()


def json_block(text):
    match = JSON_BLOCK.search(text)
    if not match:
        return None
    value = json.loads(match.group(1))
    return value if isinstance(value, dict) else None


def metadata(root, relative):
    """Metadata of a v3 profile, or None for a legacy/fixture profile without the block."""
    path = local(root, relative)
    if not path.is_file():
        return None
    try:
        return json_block(path.read_text(encoding='utf-8-sig'))
    except json.JSONDecodeError:
        return None


def profiles(root):
    directory = root / SPECIES_DIR
    return sorted(p for p in directory.glob('*.md') if p.name != 'INDEX.md') if directory.is_dir() else []


def names_of(meta):
    names = [meta.get('slug', ''), meta.get('scientific_name', '')]
    for values in (meta.get('common_names') or {}).values():
        if isinstance(values, list):
            names += values
    return [n for n in names if isinstance(n, str) and n.strip()]


def scan(root):
    rows, errors = [], []
    for path in profiles(root):
        relative = path.relative_to(root).as_posix()
        try:
            meta = json_block(path.read_text(encoding='utf-8-sig'))
        except json.JSONDecodeError as exc:
            errors.append(f'{relative}: invalid metadata JSON: {exc}')
            continue
        if meta is None:
            errors.append(f'{relative}: missing ```json metadata block (legacy profile)')
            continue
        rows.append(dict(path=relative, meta=meta))
    return rows, errors


def resolve(root, name):
    """Return {id, slug, path} for one alias; None when unknown or ambiguous."""
    key = normalize(name)
    found = {}
    for row in scan(root)[0]:
        if key in {normalize(n) for n in names_of(row['meta'])}:
            found[row['meta'].get('id')] = dict(id=row['meta'].get('id'), slug=row['meta'].get('slug'),
                                                path=row['path'])
    return next(iter(found.values())) if len(found) == 1 else None


def module_path(root, profile, module):
    meta = metadata(root, profile)
    value = ((meta or {}).get('modules') or {}).get(module)
    return value if isinstance(value, str) and value else None


def section(text, heading):
    start = text.find(heading)
    if start < 0:
        return ''
    end = text.find('\n## ', start + len(heading))
    return text[start:] if end < 0 else text[start:end]


def table_rows(block):
    lines = [l.strip() for l in block.splitlines() if l.strip().startswith('|')]
    if len(lines) < 3:
        return None, []
    cells = lambda line: [c.strip() for c in line.strip('|').split('|')]
    return cells(lines[0]), [cells(l) for l in lines[2:]]


def load_sources(root, meta, profile_path):
    relative = meta.get('sources_file')
    if not isinstance(relative, str):
        return None, [f'{profile_path}: metadata.sources_file required']
    path = local(root, relative)
    if not path.is_file():
        return None, [f'{profile_path}: sources_file missing: {relative}']
    try:
        ledger = json_block(path.read_text(encoding='utf-8-sig'))
    except json.JSONDecodeError as exc:
        return None, [f'{relative}: invalid JSON: {exc}']
    if not ledger or not isinstance(ledger.get('sources'), list):
        return None, [f'{relative}: ```json block with "sources" list required']
    return ledger, []


def check_sources(ledger, label, species_id):
    errors, ids = [], {}
    if ledger.get('species_id') != species_id:
        errors.append(f'{label}: species_id must be {species_id}')
    for item in ledger['sources']:
        sid = item.get('id') if isinstance(item, dict) else None
        if not isinstance(sid, str) or not re.fullmatch(r'S[0-9]+', sid) or sid in ids:
            errors.append(f'{label}: invalid/duplicate source id {sid!r}')
            continue
        ids[sid] = item
        where = f'{label} {sid}'
        if item.get('tier') not in TIERS:
            errors.append(f'{where}: tier must be one of {"/".join(TIERS)}')
        if item.get('access') not in ACCESS:
            errors.append(f'{where}: access must be one of {"/".join(ACCESS)}')
        if not isinstance(item.get('title'), str) or not item['title'].strip():
            errors.append(f'{where}: title required')
        url = item.get('url')
        if not isinstance(url, str) or not url.startswith('https://'):
            errors.append(f'{where}: https url required')
        accessed = item.get('accessed')
        if item.get('access') == 'not_accessed':
            if accessed is not None:
                errors.append(f'{where}: not_accessed source cannot carry an access date')
        elif not isinstance(accessed, str) or not re.fullmatch(DATE_PATTERN, accessed):
            errors.append(f'{where}: real access date YYYY-MM-DD required')
        if not isinstance(item.get('supports'), str) or not item['supports'].strip():
            errors.append(f'{where}: supports (what it backs) required')
    return ids, errors


def validate_profile(root, path):
    relative = path.relative_to(root).as_posix()
    text = path.read_text(encoding='utf-8-sig')
    errors, warnings = [], []
    try:
        meta = json_block(text)
    except json.JSONDecodeError as exc:
        return [f'{relative}: invalid metadata JSON: {exc}'], warnings, None
    if meta is None:
        return [f'{relative}: missing ```json metadata block'], warnings, None
    sid = meta.get('id')
    if not isinstance(sid, str) or not re.fullmatch(ID_PATTERN, sid):
        errors.append(f'{relative}: id must match {ID_PATTERN}')
    if meta.get('slug') != path.stem:
        errors.append(f'{relative}: slug must equal file name {path.stem}')
    if not isinstance(meta.get('scientific_name'), str) or not re.fullmatch(r'[A-Z][a-z]+ [a-z]+(?: [a-z]+)?', meta['scientific_name']):
        errors.append(f'{relative}: scientific_name must be a binomial/trinomial')
    taxonomy = meta.get('taxonomy')
    if not isinstance(taxonomy, dict) or not all(isinstance(taxonomy.get(k), str) and taxonomy[k] for k in ('authority', 'family', 'checked_with')):
        errors.append(f'{relative}: taxonomy needs authority, family, checked_with')
    names = meta.get('common_names')
    if not isinstance(names, dict) or not isinstance(names.get('en'), list) or not names['en']:
        errors.append(f'{relative}: common_names.en must be a nonempty list')
    elif any(not isinstance(v, list) or any(not isinstance(n, str) or not n.strip() for n in v) for v in names.values()):
        errors.append(f'{relative}: common_names values must be string lists')
    if meta.get('group') not in GROUPS:
        errors.append(f'{relative}: group must be one of {", ".join(GROUPS)}')
    if not isinstance(meta.get('stages'), list) or not meta['stages'] or any(not isinstance(s, str) or not s for s in meta['stages']):
        errors.append(f'{relative}: stages must be a nonempty label list')
    if meta.get('status') not in STATUSES:
        errors.append(f'{relative}: status must be one of {", ".join(STATUSES)}')
    for key in ('updated', 'review_due'):
        if not isinstance(meta.get(key), str) or not re.fullmatch(DATE_PATTERN, meta[key]):
            errors.append(f'{relative}: {key} must be YYYY-MM-DD')
    if not isinstance(meta.get('version'), str) or not re.fullmatch(r'[0-9]+\.[0-9]+', meta['version']):
        errors.append(f'{relative}: version must be MAJOR.MINOR')
    look = meta.get('look_alikes', [])
    if not isinstance(look, list) or any(not isinstance(x, dict) or not x.get('scientific_name') for x in look):
        errors.append(f'{relative}: look_alikes entries need scientific_name (id optional)')
    modules = meta.get('modules', {})
    if not isinstance(modules, dict):
        errors.append(f'{relative}: modules must map module -> workspace path')
    else:
        for name, target in modules.items():
            if name not in MODULES:
                errors.append(f'{relative}: unknown module {name}')
            elif not isinstance(target, str) or not local(root, target).is_file():
                errors.append(f'{relative}: module {name} file missing: {target}')
    for heading in SECTIONS:
        if heading not in text:
            errors.append(f'{relative}: missing section "{heading}"')
    ledger, problems = load_sources(root, meta, relative)
    errors += problems
    if ledger:
        known, problems = check_sources(ledger, meta['sources_file'], sid)
        errors += problems
        # Modules share the profile's source ledger, so their citations count too.
        targets = modules.values() if isinstance(modules, dict) else ()
        module_texts = [local(root, t).read_text(encoding='utf-8-sig') for t in targets
                        if isinstance(t, str) and local(root, t).is_file()]
        cited = {s.strip() for body in [text, *module_texts] for group in CITATION.findall(body) for s in group.split(',')}
        errors += [f'{relative}: cites unknown source {s}' for s in sorted(cited - set(known))]
        if not any(known[s].get('tier') in ('A', 'B') and known[s].get('access') != 'not_accessed' for s in cited & set(known)):
            errors.append(f'{relative}: needs at least one cited A/B-tier source that was accessed')
        tax = (taxonomy or {}).get('checked_with', '')
        tax_ids = {s.strip() for s in tax.split(',')} if isinstance(tax, str) else set()
        if not tax_ids or any(known.get(s, {}).get('tier') != 'A' for s in tax_ids):
            errors.append(f'{relative}: taxonomy.checked_with must list A-tier source ids')
        header, rows = table_rows(section(text, SECTIONS[1]))
        if header and 'Nguồn' in header:
            column = header.index('Nguồn')
            cited |= {s for row in rows if len(row) == len(header) for s in re.findall(r'S[0-9]+', row[column])}
        warnings += [f'{relative}: source {s} listed but never cited' for s in sorted(set(known) - cited - tax_ids)]
        if not header or 'Loại' not in header or 'Nguồn' not in header or 'Đơn vị' not in header:
            errors.append(f'{relative}: size section needs a table with Đơn vị/Loại/Nguồn columns')
        else:
            kind, unit, src = header.index('Loại'), header.index('Đơn vị'), header.index('Nguồn')
            for row in rows:
                if len(row) != len(header):
                    errors.append(f'{relative}: size row has wrong column count: {row}')
                    continue
                if row[kind] not in SIZE_KINDS:
                    errors.append(f'{relative}: size kind {row[kind]!r} not in {"/".join(SIZE_KINDS)}')
                if not row[unit]:
                    errors.append(f'{relative}: size row needs a unit: {row}')
                refs = set(re.findall(r'S[0-9]+', row[src]))
                if not refs or refs - set(known):
                    errors.append(f'{relative}: size row needs known source ids: {row}')
            if not any(row[kind] == 'typical' for row in rows if len(row) == len(header)):
                warnings.append(f'{relative}: no "typical" size row; large/record values must not become defaults')
    checklist = [l for l in section(text, SECTIONS[6]).splitlines() if l.lstrip().startswith('- ')]
    if not 3 <= len(checklist) <= 12:
        errors.append(f'{relative}: visual checklist needs 3-12 bullet items')
    if len(text) > PROFILE_CHAR_BUDGET:
        warnings.append(f'{relative}: {len(text)} chars > budget {PROFILE_CHAR_BUDGET}; move module detail out')
    if isinstance(meta.get('review_due'), str) and meta['review_due'] < dt.date.today().isoformat():
        warnings.append(f'{relative}: review_due {meta["review_due"]} passed; re-check sources')
    return errors, warnings, meta


def validate(root, slug=None):
    errors, warnings, seen_ids, aliases = [], [], {}, {}
    paths = profiles(root)
    if slug:
        paths = [p for p in paths if p.stem == slug]
        if not paths:
            raise ValueError('No profile: ' + slug)
    for path in profiles(root):
        problems, notes, meta = validate_profile(root, path)
        if not slug or path.stem == slug:
            errors += problems
            warnings += notes
        if not meta:
            continue
        if meta.get('id') in seen_ids:
            errors.append(f'duplicate id {meta["id"]}: {seen_ids[meta["id"]]} and {path.name}')
        seen_ids[meta.get('id')] = path.name
        for name in names_of(meta):
            key = normalize(name)
            if key in aliases and aliases[key] != path.name:
                errors.append(f'alias "{name}" used by {aliases[key]} and {path.name}')
            aliases.setdefault(key, path.name)
    for recipe in sorted((root / '03-Projects').glob('*/context-map.json')):
        mapping = json.loads(recipe.read_text(encoding='utf-8-sig')).get('species', {})
        for key, target in mapping.items():
            if not local(root, target).is_file():
                errors.append(f'{recipe.relative_to(root).as_posix()}: species {key} -> missing {target}')
    if not slug:
        expected = render_index(root)
        current = root / SPECIES_DIR / 'INDEX.md'
        if not current.is_file() or current.read_text(encoding='utf-8-sig') != expected:
            errors.append(f'{SPECIES_DIR}/INDEX.md is stale; run species_profiles.py index')
    return dict(ok=not errors, errors=errors, warnings=warnings, profiles=len(seen_ids))


def render_index(root):
    rows, _ = scan(root)
    lines = ['# Chỉ mục hồ sơ loài', '',
             'Sinh bằng `python scripts/species_profiles.py index`; không sửa tay. Chỉ mục để người đọc tra cứu, '
             'không nạp vào context. Skill resolve tên loài bằng `species_profiles.py resolve` rồi chỉ mở đúng một hồ sơ.', '']
    for group in GROUPS:
        members = sorted((r for r in rows if r['meta'].get('group') == group), key=lambda r: r['meta'].get('slug', ''))
        if not members:
            continue
        lines += [f'## {group}', '', '| ID | Loài | Tên khoa học | Stage | Trạng thái | Duyệt lại | Hồ sơ |', '|---|---|---|---|---|---|---|']
        for r in members:
            m = r['meta']
            name = ', '.join((m.get('common_names') or {}).get('en', [])[:2])
            lines.append(f"| {m.get('id')} | {name} | *{m.get('scientific_name')}* | {', '.join(m.get('stages', []))} | "
                         f"{m.get('status')} | {m.get('review_due')} | [{m.get('slug')}]({Path(r['path']).name}) |")
        lines.append('')
    return '\n'.join(lines)


def scaffold(root, slug, species_id, scientific, name, group):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
        raise ValueError('Invalid slug')
    if not re.fullmatch(ID_PATTERN, species_id):
        raise ValueError('Invalid id')
    if group not in GROUPS:
        raise ValueError('Invalid group')
    profile = root / SPECIES_DIR / f'{slug}.md'
    ledger = root / '01-Knowledge/sources/species' / f'{slug}.md'
    if profile.exists() or ledger.exists():
        raise ValueError('Profile or source ledger already exists; edit it instead')
    if any(m['meta'].get('id') == species_id for m in scan(root)[0]):
        raise ValueError('ID already used')
    today = dt.date.today().isoformat()
    fill = lambda text: (text.replace('<slug>', slug).replace('<ID>', species_id).replace('<Scientific name>', scientific)
                         .replace('<Common name>', name).replace('<group>', group).replace('<YYYY-MM-DD>', today))
    template = root / '00-Standards/templates'
    profile.write_text(fill((template / 'species-profile.md').read_text(encoding='utf-8')), encoding='utf-8')
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(fill((template / 'species-sources.md').read_text(encoding='utf-8')), encoding='utf-8')
    return dict(profile=profile.relative_to(root).as_posix(), sources=ledger.relative_to(root).as_posix(),
                note='Draft scaffold only; research, then validate and index. Add to a Project context-map to grant use.')


def visible_text(raw):
    text = raw.decode('utf-8', 'replace')
    text = re.sub(r'(?is)<(script|style|noscript)\b.*?</\1>', ' ', text)
    text = html.unescape(re.sub(r'(?s)<[^>]+>', ' ', text))
    return ' '.join(text.split())


def snapshot(root, slug, fetch=None):
    """Fetch each accessed source once and keep a local hash; content stays out of Git."""
    path = root / SPECIES_DIR / f'{slug}.md'
    meta = metadata(root, path.relative_to(root).as_posix()) if path.is_file() else None
    if not meta:
        raise ValueError('No v3 profile: ' + slug)
    ledger, errors = load_sources(root, meta, slug)
    if errors:
        raise ValueError('; '.join(errors))
    fetch = fetch or (lambda url: urllib.request.urlopen(urllib.request.Request(
        url, headers={'User-Agent': 'NatureStudio-source-check/1.0'}), timeout=30).read())
    directory = root / SNAPSHOT_DIR / slug
    directory.mkdir(parents=True, exist_ok=True)
    manifest_path = directory / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.is_file() else {}
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    report = []
    for item in ledger['sources']:
        if item.get('access') == 'not_accessed':
            report.append(dict(id=item['id'], status='skipped_not_accessed'))
            continue
        try:
            raw = fetch(item['url'])
        except Exception as exc:  # network errors are reported, never fatal for the batch
            report.append(dict(id=item['id'], status='fetch_error', error=type(exc).__name__ + ': ' + str(exc)[:160]))
            continue
        text_sha = hashlib.sha256(visible_text(raw).encode()).hexdigest()
        previous = manifest.get(item['id'], [])
        last = previous[-1] if previous else None
        status = 'new' if not last else ('unchanged' if last['text_sha256'] == text_sha and last['url'] == item['url'] else 'changed')
        if status != 'unchanged':
            name = f"{item['id']}-{stamp}.bin"
            (directory / name).write_bytes(raw)
            previous.append(dict(url=item['url'], fetched=stamp, raw_sha256=hashlib.sha256(raw).hexdigest(),
                                 text_sha256=text_sha, bytes=len(raw), file=name))
            manifest[item['id']] = previous
        report.append(dict(id=item['id'], status=status))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return dict(slug=slug, sources=report,
                note='changed = visible page text differs from the last local snapshot; re-read that source, '
                     'do not assume the profile fact is wrong. Snapshots are local only.')


def listing(root, group=None):
    rows, errors = scan(root)
    out = [dict(id=r['meta'].get('id'), slug=r['meta'].get('slug'), group=r['meta'].get('group'),
                scientific_name=r['meta'].get('scientific_name'), stages=r['meta'].get('stages'),
                status=r['meta'].get('status'), path=r['path'])
           for r in rows if not group or r['meta'].get('group') == group]
    return dict(species=out, errors=errors)


def main():
    import ns_console
    ns_console.utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('validate'); p.add_argument('slug', nargs='?')
    p = sub.add_parser('index'); p.add_argument('--check', action='store_true')
    p = sub.add_parser('resolve'); p.add_argument('name')
    p = sub.add_parser('list'); p.add_argument('--group', choices=GROUPS)
    p = sub.add_parser('new')
    for flag in ('slug', 'id', 'scientific', 'name'):
        p.add_argument('--' + flag, required=True)
    p.add_argument('--group', choices=GROUPS, required=True)
    p = sub.add_parser('snapshot'); p.add_argument('slug')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == 'validate':
            result = validate(root, args.slug)
            print(json.dumps(result, ensure_ascii=False, indent=1))
            return 0 if result['ok'] else 1
        if args.action == 'index':
            target = root / SPECIES_DIR / 'INDEX.md'
            expected = render_index(root)
            if args.check:
                fresh = target.is_file() and target.read_text(encoding='utf-8-sig') == expected
                print('fresh' if fresh else 'stale')
                return 0 if fresh else 1
            target.write_text(expected, encoding='utf-8')
            print(target.relative_to(root).as_posix())
            return 0
        if args.action == 'resolve':
            found = resolve(root, args.name)
            print(json.dumps(found or dict(found=None, note='Unknown or ambiguous name; research the exact species, '
                                                         'do not substitute another profile'), ensure_ascii=False))
            return 0 if found else 1
        if args.action == 'list':
            print(json.dumps(listing(root, args.group), ensure_ascii=False, indent=1))
            return 0
        if args.action == 'new':
            print(json.dumps(scaffold(root, args.slug, args.id, args.scientific, args.name, args.group), ensure_ascii=False, indent=1))
            return 0
        print(json.dumps(snapshot(root, args.slug), ensure_ascii=False, indent=1))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
