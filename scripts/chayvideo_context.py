"""Plan 01: exact-source task packets and rebuildable local history. Stdlib only.

No model calls, semantic novelty verdicts, ID reservations or media operations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import secrets
import sys
import tempfile
import time
import memory_retrieval as memory
import context_routing as routing
import species_profiles
import bait_profiles

ROOT = Path(__file__).resolve().parents[1]
FINGERPRINT_FIELDS = ('opening', 'interaction', 'objects', 'terrain_role',
                      'trigger', 'key_action', 'consequence')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inside(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path outside workspace: {relative}')
    return path


def slug_ok(slug):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
        raise ValueError('Invalid Project slug')


def source(root, relative):
    path = inside(root, relative)
    raw = path.read_bytes()
    return dict(path=path.relative_to(root.resolve()).as_posix(),
                sha256=digest(raw), text=raw.decode('utf-8-sig'))


def catalog(root):
    """Route using compact current metadata; no frozen species-to-project map."""
    rows = []
    for path in sorted((root / '03-Projects').glob('*/PROJECT.md')):
        item = source(root, path.relative_to(root))
        text = item.pop('text')
        metadata = [line for line in text.splitlines() if re.match(
            r'^(# |ID:|Slug:|Version:|Aliases:|Routing:|Model:)', line)]
        rows.append(dict(**item, metadata='\n'.join(metadata),
                         needs_full_read=not any(x.startswith('Routing:') for x in metadata)))
    return rows


def active_files(root, slug):
    # Check real files too; an empty/stale INDEX is not proof of no lessons.
    files = []
    for base in (f'05-Memory/projects/{slug}/active', '05-Memory/shared/active'):
        directory = inside(root, base)
        if directory.exists():
            files.extend(p.relative_to(root).as_posix() for p in directory.rglob('*.md'))
    return sorted(files)


def species_sources(root, recipe, name, angling):
    """Project map grants a species; the profile resolver only maps aliases to that one profile."""
    mapped = recipe.get('species', {})
    key = name.lower()
    if key not in mapped:
        entry = species_profiles.resolve(root, name)
        key = entry['slug'] if entry else key
    profile = mapped.get(key)
    if not profile:
        return None
    module = species_profiles.module_path(root, profile, 'angling') if angling else None
    return [profile, *([module] if module else [])]


def packet(root, slug, mode, species=(), interaction='unspecified',
           memory_selection=None, lesson_ids=(), topics=(), query_text='',
           stage=None, effects=(), tasks=(), asset_selection=None):
    slug_ok(slug)
    recipe_path = f'03-Projects/{slug}/context-map.json'
    recipe_source = source(root, recipe_path)
    recipe = json.loads(recipe_source['text'])
    chosen = routing.mode_sources(recipe, mode)
    plan = routing.route(root, slug, recipe, mode, stage, effects) if stage is not None else None
    if effects and plan is None:
        raise ValueError('Effects require an explicit --stage (use all for full coverage)')
    if plan:
        chosen = plan['files']
    defaults = (plan['tasks'] if plan and not plan['fallback'] else
                memory.taxonomy(root)['modes'].get(mode, []))
    task_union = list(dict.fromkeys([*defaults, *tasks]))
    if plan:
        plan['tasks'] = task_union
    # context-map is the coverage floor and a dependency; its JSON is not reading material.
    files = recipe['common'] + chosen
    # Human-facing indexes can grow without bound; discovery returns paged descriptors.
    files = [p for p in files if not (p.startswith('05-Memory/') and p.endswith('/INDEX.md'))]
    missing, baits = [], {}
    if mode != 'caption':
        angling = interaction != 'natural' and (not plan or plan['include_angling'])
        for name in species if not plan or plan['include_species'] else ():
            profile = species_sources(root, recipe, name, angling)
            if profile:
                files += profile
                if angling:
                    # Compact rows only; the chosen bait profile is opened later, never the whole library.
                    baits[name] = bait_profiles.for_species(root, name)['baits'] if species_profiles.resolve(root, name) else []
            else:
                missing.append(f'Research exact species/context: {name}; no substitute profile')
        # Underwater is the configured species-required workflow. Optional profiles
        # in another Project's map do not make species a mandatory input there.
        if slug == 'underwater' and not species:
            missing.append('Resolve species or granted choice before producing content')
        if interaction != 'natural' and (not plan or plan['include_angling']):
            files += recipe.get('angling', [])
    selection = memory.query(root, slug, mode=mode, tasks=task_union, topics=topics, entities=species,
                             interactions=[] if interaction == 'unspecified' else [interaction],
                             text=query_text)
    if selection['errors']:
        missing.append('Memory discovery incomplete: inspect memory.errors before producing content')
    if lesson_ids:
        if memory_selection is None or memory_selection.get('request', {}).get('mode') != mode:
            raise ValueError('Supply a memory selection page for the same task mode')
        selected = memory.load_lessons(root, slug, memory_selection, list(lesson_ids))
        files += [row['path'] for row in selected]
    else:
        selected = []
    sources = [source(root, path) for path in dict.fromkeys(files)]
    dependencies = [{k: v for k, v in recipe_source.items() if k != 'text'}]
    for path in ['VERSION', 'START-HERE.md', 'SYSTEM.md', 'AGENTS.md',
                 '.agents/skills/na-chayvideo/SKILL.md',
                 '.agents/skills/na-chayvideo/references/workflow.md',
                 '00-Standards/video-prompt-workflow.md',
                 f'.agents/skills/na-chayvideo/references/{mode}.md']:
        item = source(root, path)
        item.pop('text')
        dependencies.append(item)
    # asset_catalog.py is always a dependency so adding --asset-selection keeps the digest.
    for path in ['scripts/chayvideo_context.py', 'scripts/context_routing.py',
                 'scripts/memory_retrieval.py', 'scripts/asset_catalog.py', 'scripts/species_profiles.py',
                 *(['scripts/bait_profiles.py', bait_profiles.PHOTO_MANIFEST] if baits else []), '00-Standards/memory-taxonomy.json',
                 *[f'.agents/skills/na-chayvideo/references/{m}.md'
                   for m in ('new', 'revision', 'caption', 'reference')],
                 '00-Standards/context-routing.md', *([plan['config']] if plan and plan['config'] else [])]:
        if inside(root, path).is_file():
            item = source(root, path)
            item.pop('text')
            dependencies.append(item)
    if mode == 'reference':
        for path in ['00-Standards/reference-video-adaptation.md',
                     '.agents/skills/na-clonevideo/SKILL.md',
                     '.agents/skills/na-clonevideo/references/analysis.md',
                     '.agents/skills/na-clonevideo/references/schema.md',
                     'scripts/reference_video.py']:
            item = source(root, path)
            item.pop('text')
            dependencies.append(item)
    dependencies = list({s['path']: s for s in dependencies}.values())
    result = dict(schema=3 if plan else 2, project=slug, mode=mode, species=list(species),
                interaction=interaction, memory=selection,
                selected_lessons=[{k: r[k] for k in ('id', 'status', 'path', 'sha256')} for r in selected],
                sources=sources, dependencies=dependencies, pending=missing,
                note='Exact current sources, no token truncation. Read real production/attached media '
                     'separately. Active location is discovery, not permission: inspect status and '
                         'conditions before applying. Project decides required inputs; generic packet '
                         'does not certify completeness. New facts need external research.')
    if baits:
        result['baits'] = baits
    if asset_selection is not None:
        import asset_catalog
        if asset_selection.get('schema')==2 and asset_selection.get('project_id')!=recipe.get('project_id'):
            raise ValueError('Asset selection Project mismatch')
        status = asset_catalog.verify(root, asset_selection,recipe.get('project_id') if asset_selection.get('schema')==2 else None)
        if status['status'] == 'stale': raise ValueError('Stale asset selection; refresh references')
        result['asset_selection'] = asset_selection
        result['asset_review_pending'] = status['issues']
    if plan:
        result.update(routing=plan, routing_request=dict(stage=stage, effects=list(effects), tasks=list(tasks)))
    return result


def verify(root, data):
    stale = []
    for item in data['sources'] + data.get('dependencies', []):
        path = inside(root, item['path'])
        if not path.is_file() or digest(path.read_bytes()) != item['sha256']:
            stale.append(item['path'])
        elif 'text' in item and path.read_bytes().decode('utf-8-sig') != item['text']:
            stale.append(item['path'] + ': packet text differs from source')
    if data.get('schema') == 3:
        try:
            recipe_path = f'03-Projects/{data["project"]}/context-map.json'
            recipe = json.loads(inside(root, recipe_path).read_text(encoding='utf-8-sig'))
            request = data['routing_request']
            plan = routing.route(root, data['project'], recipe, data['mode'], request['stage'], request['effects'])
            defaults = (plan['tasks'] if not plan['fallback'] else
                        memory.taxonomy(root)['modes'].get(data['mode'], []))
            plan['tasks'] = list(dict.fromkeys([*defaults, *request['tasks']]))
            if plan != data['routing']:
                stale.append('routing_plan')
            expected_tasks = plan['tasks'] or memory.taxonomy(root)['modes'].get(data['mode'], [])
            if (data['memory']['request'].get('tasks') != expected_tasks
                    or data['memory']['request'].get('mode') != data['mode']):
                stale.append('routing_memory_tasks')
            required = {*recipe['common'], *plan['files']}
            if data['mode'] != 'caption':
                if plan['include_species']:
                    angling = data['interaction'] != 'natural' and plan['include_angling']
                    for name in data['species']:
                        required.update(species_sources(root, recipe, name, angling) or [])
                if data['interaction'] != 'natural' and plan['include_angling']:
                    required.update(recipe.get('angling', []))
            required = {p for p in required if not (p.startswith('05-Memory/') and p.endswith('/INDEX.md'))}
            if required - {s['path'] for s in data['sources']}:
                stale.append('routing_sources_missing')
        except (ValueError, OSError, KeyError, TypeError):
            stale.append('routing_plan')
    if data.get('asset_selection') is not None:
        try:
            import asset_catalog
            recipe=json.loads(inside(root,f"03-Projects/{data['project']}/context-map.json").read_text(encoding='utf-8-sig'))
            check = asset_catalog.verify(root,data['asset_selection'],recipe.get('project_id') if data['asset_selection'].get('schema')==2 else None)
            if check['status'] == 'stale' or check['status'] != data['asset_selection']['status'] or check['issues'] != data.get('asset_review_pending',[]): stale.append('asset_selection')
        except (ValueError, OSError, TypeError): stale.append('asset_selection')
    if 'memory' in data:
        current = memory.scan(root, data['project'])
        if current['fingerprint'] != data['memory']['fingerprint'] or current['errors']:
            stale.append('memory_inventory')
    elif active_files(root, data['project']) != data['active_inventory']:
        stale.append('active_inventory')
    return stale


def coverage(root, packets, receipts=(), context_id=None, retained=False):
    """Conservative whole-source coverage floor; does not certify understanding."""
    if not packets:
        raise ValueError('Supply at least one current packet')
    first = packets[0]
    identity = tuple(first.get(k) for k in ('project', 'mode', 'species', 'interaction'))
    if any(tuple(p.get(k) for k in ('project', 'mode', 'species', 'interaction')) != identity for p in packets):
        raise ValueError('Coverage packets must have identical Project/mode/species/interaction')
    stale = sorted({x for p in packets for x in verify(root, p)})
    # Rebuild full baseline, including any effect-added sources and new unassigned sources.
    effects = list(dict.fromkeys(e for p in packets for e in p.get('routing_request', {}).get('effects', [])))
    full = packet(root, first['project'], first['mode'], first['species'], first['interaction'],
                  stage='all', effects=effects)
    required = {(s['path'], s['sha256']) for s in full['sources']}
    offered = {(s['path'], s['sha256']) for p in packets for s in p['sources']}
    accepted, missing_receipts = set(), []
    if receipts and (not retained or not context_id):
        raise ValueError('Read coverage requires --retained and --context-id; unknown context must reload')
    digests = {routing.dependency_digest(p) for p in packets}
    for receipt in receipts:
        if (receipt.get('schema') != 1 or receipt.get('root') != str(root.resolve())
                or receipt.get('context_id') != context_id or receipt.get('dependency_digest') not in digests):
            missing_receipts.append('Receipt stale or from another context')
            continue
        accepted.update((s['path'], s['sha256']) for s in receipt.get('sources', []))
    missing = sorted(path for path, sha in required - (accepted & offered))
    pending = sorted({x for p in packets for x in p['pending']} | set(full['pending']))
    return dict(complete=not (missing or stale or pending or missing_receipts),
                required_source_count=len(required), missing_sources=missing,
                stale=stale, pending=pending, receipt_errors=missing_receipts,
                note='Declared whole-source read coverage only; not semantic, history, lesson application or media QA. Receipts require actual retained untruncated source text.')


def history(root, slug, query=''):
    """Inspect all text files, cache derived rows; never pretend lexical search is semantic QA."""
    slug_ok(slug)
    folder = inside(root, f'04-Productions/{slug}')
    rows, inventory = [], {}
    for production in sorted(folder.iterdir()) if folder.exists() else []:
        if not production.is_dir():
            continue
        # Every text record participates in freshness, including feedback and old attempts.
        files = sorted(p for p in production.rglob('*') if p.is_file()
                       and p.suffix.lower() in ('.md', '.json', '.txt'))
        current = {}
        texts = {}
        for path in files:
            rel = path.relative_to(root).as_posix()
            raw = inside(root, rel).read_bytes()
            current[rel] = digest(raw)
            if path.name != 'HISTORY-FINGERPRINT.json':
                texts[rel] = raw.decode('utf-8-sig', errors='replace')
        inventory.update(current)
        fp_path = production / 'HISTORY-FINGERPRINT.json'
        fp, valid = None, False
        if fp_path.exists():
            try:
                fp = json.loads(fp_path.read_text(encoding='utf-8-sig'))
                if not isinstance(fp, dict):
                    raise ValueError('Fingerprint must be an object')
                refs = fp.get('source_hashes', {})
                # Capsule must cover ALL text sources. A later attempt invalidates it.
                valid = (refs == {k: v for k, v in current.items()
                                  if not k.endswith('/HISTORY-FINGERPRINT.json')}
                         and all(isinstance(fp.get(k), str) and fp[k].strip()
                                 for k in FINGERPRINT_FIELDS))
            except (ValueError, TypeError):
                pass
        terms = set(re.findall(r'\w+', query.casefold()))
        matches = [rel for rel, text in texts.items()
                   if terms and any(term in text.casefold() for term in terms)]
        rows.append(dict(production=production.name,
                         fingerprint={k: fp[k] for k in FINGERPRINT_FIELDS} if valid else None,
                         needs_read=[] if valid else sorted(texts), lexical_matches=matches,
                         source_hashes=current))
    ledger = inside(root, f'03-Projects/{slug}/idea-ledger.md')
    ledger_source = source(root, ledger.relative_to(root)) if ledger.exists() else None
    if ledger_source:
        inventory[ledger_source['path']] = ledger_source['sha256']
    cache = inside(root, f'.nature-studio/history/{slug}.json')
    try:
        previous = json.loads(cache.read_text(encoding='utf-8')) if cache.exists() else {}
    except ValueError:
        previous = {}  # Derived cache can be rebuilt; production remains authoritative.
    if not isinstance(previous, dict):
        previous = {}
    result = dict(schema=1, project=slug, inventory=inventory, records=rows,
                  ledger=ledger_source, refreshed=previous.get('inventory') != inventory,
                  limits='All records listed; lexical matches only assist retrieval. Read uncovered '
                         'records and nearest originals before novelty verdict. Chat, examples, '
                         'rejected drafts and related other Projects still require inspection.')
    write_json(cache, result)
    return result


def compact_history(result):
    """Default CLI view: production-relative paths, no per-file hashes or ledger body."""
    rows = []
    for row in result['records']:
        prefix = f"04-Productions/{result['project']}/{row['production']}/"
        trim = lambda paths: [p[len(prefix):] if p.startswith(prefix) else p for p in paths]
        rows.append(dict(production=row['production'], fingerprint=row['fingerprint'],
                         needs_read=trim(row['needs_read']), lexical_matches=trim(row['lexical_matches'])))
    ledger = result['ledger']
    return dict(schema=1, project=result['project'], inventory_count=len(result['inventory']),
                refreshed=result['refreshed'], records=rows,
                ledger={k: ledger[k] for k in ('path', 'sha256')} if ledger else None,
                limits=result['limits'])


def new_context_id():
    return 'ctx-' + time.strftime('%Y%m%dT%H%M%S') + '-' + secrets.token_hex(2)


def ledger_path(root, relative, context_id):
    path = inside(root, relative)
    if not path.relative_to(root.resolve()).as_posix().startswith('.nature-studio/context/'):
        raise ValueError('Ledger must live under .nature-studio/context/')
    if not context_id or path.name != context_id + '.json':
        raise ValueError('Ledger file must be named <context-id>.json; run context-id for a new chat')
    return path


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     suffix='.tmp', delete=False) as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
        temp = Path(out.name)
    temp.replace(path)


def preflight(root, slug, mode, species=(), interaction='unspecified', stage='all',
              effects=(), tasks=(), query_text='', out=None):
    """One call: write the packet and history cache, return only IDs, counts and paths."""
    data = packet(root, slug, mode, species, interaction, stage=stage, effects=effects,
                  tasks=tasks, query_text=query_text)
    context_id = new_context_id()
    path = inside(root, out or f'.nature-studio/context/{slug}-{mode}-{context_id}.json')
    write_json(path, data)
    selection = data['memory']
    result = dict(project=slug, mode=mode, context_id=context_id,
                  packet=path.relative_to(root.resolve()).as_posix(),
                  ledger=f'.nature-studio/context/{context_id}.json',
                  source_count=len(data['sources']), source_chars=sum(len(s['text']) for s in data['sources']),
                  pending=data['pending'],
                  memory={state: [r['id'] for r in selection.get(state, [])] for state in ('active', 'candidates')}
                  | dict(remaining=selection.get('remaining'), next_cursor=selection.get('next_cursor'),
                         errors=selection.get('errors')))
    if mode in ('new', 'reference'):
        found = history(root, slug, query_text)
        result['history'] = dict(productions=len(found['records']),
                                 fingerprinted=[r['production'] for r in found['records'] if r['fingerprint']],
                                 needs_read_files=sum(len(r['needs_read']) for r in found['records']),
                                 lexical_match_productions=[r['production'] for r in found['records'] if r['lexical_matches']],
                                 ledger=found['ledger']['path'] if found['ledger'] else None,
                                 detail=f'python scripts/chayvideo_context.py history {slug}')
    result['next'] = (f"python scripts/chayvideo_context.py view {result['packet']} --context-id {context_id} "
                      f"--ledger {result['ledger']}")
    return result


def fingerprint(root, slug, production_id, data, from_history=False):
    """Store an AI-authored capsule only against the exact history it actually reviewed."""
    if not all(isinstance(data.get(k), str) and data[k].strip() for k in FINGERPRINT_FIELDS):
        raise ValueError('Supply all causal fingerprint fields')
    if from_history and 'source_hashes' not in data:
        # Hashes come from the history output the AI reviewed; later edits still fail the match below.
        cache = inside(root, f'.nature-studio/history/{slug}.json')
        if not cache.is_file():
            raise ValueError('Run history first; no cached history to bind')
        reviewed = next((r for r in json.loads(cache.read_text(encoding='utf-8'))['records']
                         if r['production'] == production_id), None)
        if reviewed is None:
            raise ValueError('Production absent from reviewed history')
        data = dict(data, source_hashes={k: v for k, v in reviewed['source_hashes'].items()
                                         if not k.endswith('/HISTORY-FINGERPRINT.json')})
    records = history(root, slug)['records']
    record = next((r for r in records if r['production'] == production_id), None)
    if record is None:
        raise ValueError('Unknown production')
    current = {k: v for k, v in record['source_hashes'].items()
               if not k.endswith('/HISTORY-FINGERPRINT.json')}
    if not current or data.get('source_hashes') != current:
        raise ValueError('Read all source records first; supplied source_hashes must exactly match')
    payload = {k: data[k] for k in (*FINGERPRINT_FIELDS, 'source_hashes')}
    payload['schema'] = 1
    path = inside(root, f'04-Productions/{slug}/{production_id}/HISTORY-FINGERPRINT.json')
    # Derived metadata only; never modifies a source record or its status.
    write_json(path, payload)
    return dict(path=path.relative_to(root).as_posix(), note='AI-authored capsule; semantic review still required')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    subs = parser.add_subparsers(dest='command', required=True)
    subs.add_parser('projects')
    subs.add_parser('context-id', help='New context id and ledger path for a new chat or after compaction')
    p = subs.add_parser('preflight', help='Packet + history cache in one call; prints IDs, counts and paths only')
    p.add_argument('project')
    p.add_argument('--mode', choices=('new', 'revision', 'caption', 'reference'), required=True)
    p.add_argument('--species', action='append', default=[])
    p.add_argument('--interaction', choices=('natural', 'angling', 'unspecified'), default='unspecified')
    p.add_argument('--stage', choices=routing.STAGES, default='all')
    p.add_argument('--effect', action='append', default=[])
    p.add_argument('--task', action='append', default=[])
    p.add_argument('--query', default='')
    p.add_argument('--out', type=Path)
    p = subs.add_parser('packet')
    p.add_argument('project')
    p.add_argument('--mode', choices=('new', 'revision', 'caption', 'reference'), required=True)
    p.add_argument('--species', action='append', default=[])
    p.add_argument('--interaction', choices=('natural', 'angling', 'unspecified'), default='unspecified')
    p.add_argument('--out', type=Path)
    p.add_argument('--memory-selection', type=Path)
    p.add_argument('--lesson-id', action='append', default=[])
    p.add_argument('--topic', action='append', default=[])
    p.add_argument('--query', default='')
    p.add_argument('--stage', choices=routing.STAGES)
    p.add_argument('--effect', action='append', default=[])
    p.add_argument('--task', action='append', default=[])
    p.add_argument('--asset-selection',type=Path,help='Optional verified local planned-reference receipt; never whole catalog')
    p = subs.add_parser('view', help='Verify, then display exact text without JSON body escaping')
    p.add_argument('packet', type=Path)
    p.add_argument('--context-id')
    p.add_argument('--seen', type=Path, action='append', default=[])
    p.add_argument('--retained', action='store_true')
    p.add_argument('--source', action='append', default=[])
    p.add_argument('--receipt', type=Path)
    p.add_argument('--ledger', type=Path, help='Per-context reading ledger, updated in place; replaces --seen/--receipt')
    p.add_argument('--max-chars', type=int, default=18000,
                   help='Display batch target; never cuts a source unless --page-large')
    p.add_argument('--page-large', action='store_true',
                   help='Split sources longer than --max-chars into pages; a source counts only when all pages shown')
    p.add_argument('--all-sources', action='store_true', help='Explicitly display all bodies; choose adequate tool output budget')
    p = subs.add_parser('coverage', help='Check full mode source coverage across staged packets')
    p.add_argument('packets', type=Path, nargs='+')
    p.add_argument('--receipt', type=Path, action='append', default=[])
    p.add_argument('--ledger', type=Path, action='append', default=[])
    p.add_argument('--context-id')
    p.add_argument('--retained', action='store_true')
    p = subs.add_parser('verify')
    p.add_argument('packet', type=Path)
    p = subs.add_parser('history')
    p.add_argument('project')
    p.add_argument('--query', default='')
    p.add_argument('--full', action='store_true', help='Include hashes of every source file; default is compact')
    p = subs.add_parser('fingerprint')
    p.add_argument('project')
    p.add_argument('production')
    p.add_argument('input', type=Path)
    p.add_argument('--from-history', action='store_true',
                   help='Take source_hashes from the last history run instead of copying them')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == 'projects':
        result = catalog(root)
    elif args.command == 'context-id':
        context_id = new_context_id()
        result = dict(context_id=context_id, ledger=f'.nature-studio/context/{context_id}.json')
    elif args.command == 'preflight':
        result = preflight(root, args.project, args.mode, args.species, args.interaction, args.stage,
                           args.effect, args.task, args.query, args.out.as_posix() if args.out else None)
    elif args.command == 'packet':
        selection = (json.loads(inside(root, args.memory_selection.as_posix()).read_text(encoding='utf-8-sig'))
                     if args.memory_selection else None)
        result = packet(root, args.project, args.mode, args.species, args.interaction,
                        selection, args.lesson_id, args.topic, args.query,
                        args.stage, args.effect, args.task,
                        json.loads(inside(root,args.asset_selection.as_posix()).read_text(encoding='utf-8-sig')) if args.asset_selection else None)
        if args.out:
            path = inside(root, args.out)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
            print(path)
            return
    elif args.command == 'view':
        data = json.loads(inside(root, args.packet.as_posix()).read_text(encoding='utf-8-sig'))
        stale = verify(root, data)
        if stale:
            raise ValueError('Stale/incomplete packet; rebuild before view: ' + ', '.join(stale))
        seen = [json.loads(inside(root, p.as_posix()).read_text(encoding='utf-8-sig')) for p in args.seen]
        ledger = ledger_path(root, args.ledger.as_posix(), args.context_id) if args.ledger else None
        if ledger and ledger.exists():
            if not args.retained:
                raise ValueError('Ledger exists: pass --retained only if its sources are still in this chat; '
                                 'otherwise run context-id and start a new ledger')
            seen.append(json.loads(ledger.read_text(encoding='utf-8-sig')))
        rendered, receipt = routing.render(data, root, args.context_id, seen,
                                           args.retained, args.source,
                                           None if args.all_sources else args.max_chars,
                                           args.page_large and not args.all_sources)
        if ledger:
            write_json(ledger, receipt)
        if args.receipt:
            path = inside(root, args.receipt.as_posix())
            relative = path.relative_to(root).as_posix()
            if not relative.startswith(('.nature-studio/context/', '.nature-studio/audits/')) or path.exists():
                raise ValueError('Use a new local context/audit receipt path; never overwrite a source or receipt')
            if path == inside(root, args.packet.as_posix()) or path in [inside(root, p.as_posix()) for p in args.seen]:
                raise ValueError('Receipt must not overwrite packet or prior receipt')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        sys.stdout.buffer.write(rendered.encode('utf-8'))
        return
    elif args.command == 'coverage':
        packets = [json.loads(inside(root, p.as_posix()).read_text(encoding='utf-8-sig')) for p in args.packets]
        receipts = [json.loads(inside(root, p.as_posix()).read_text(encoding='utf-8-sig'))
                    for p in [*args.receipt, *[ledger_path(root, l.as_posix(), args.context_id) for l in args.ledger]]]
        result = coverage(root, packets, receipts, args.context_id, args.retained)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result['complete'] else 2)
    elif args.command == 'history':
        result = history(root, args.project, args.query)
        if not args.full:
            result = compact_history(result)
    elif args.command == 'fingerprint':
        result = fingerprint(root, args.project, args.production,
                             json.loads(args.input.read_text(encoding='utf-8-sig')), args.from_history)
    else:
        result = dict(stale=verify(root, json.loads(args.packet.read_text(encoding='utf-8-sig'))))
        if result['stale']:
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    try:
        main()
    except (ValueError, OSError) as exc:
        print(json.dumps({'errors': [str(exc)], 'scope': 'Read original sources; no silent repair'}, ensure_ascii=False))
        sys.exit(1)
