"""Local reference asset catalog (stdlib). Never downloads, generates or approves media."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import math
from pathlib import Path, PureWindowsPath
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
CATALOG = '.nature-studio/assets/catalog.sqlite3'
ID = r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''): h.update(block)
    return h.hexdigest()


def local(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative or PureWindowsPath(relative).drive:
        raise ValueError('Use a workspace-relative path with forward slashes')
    rel = Path(relative)
    path = (Path(root).resolve() / rel).resolve()
    if rel.is_absolute() or '..' in rel.parts or not path.is_relative_to(Path(root).resolve()):
        raise ValueError('Path outside workspace')
    return path


def binding_errors(root, binding, label):
    if not isinstance(binding, dict): return [label + ': local path/sha256 binding required']
    try:
        path = local(root, binding.get('path'))
        if not path.is_file(): return [label + ': file unavailable']
        if file_hash(path) != binding.get('sha256'): return [label + ': hash mismatch']
    except (ValueError, OSError) as exc:
        return [label + ': ' + str(exc)]
    return []


@contextmanager
def connection(root, write=False):
    path = local(root, CATALOG)
    if not write and not path.is_file():
        yield None
        return
    if write: path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path if write else path.as_uri() + '?mode=ro', uri=not write, timeout=30)
    try:
        if db.execute('PRAGMA user_version').fetchone()[0] > 1:
            raise ValueError('Asset catalog newer than this helper')
        if write:
            db.execute('BEGIN IMMEDIATE')
            db.execute('CREATE TABLE IF NOT EXISTS assets (id TEXT PRIMARY KEY, entity TEXT NOT NULL, stage TEXT, body TEXT NOT NULL, sha TEXT NOT NULL)')
            db.execute('CREATE INDEX IF NOT EXISTS asset_entity_stage ON assets(entity,stage)')
            db.execute('PRAGMA user_version=1')
        yield db
        if write: db.commit()
    except sqlite3.Error as exc:
        if write: db.rollback()
        raise ValueError('Asset catalog error: ' + str(exc)) from exc
    except BaseException:
        if write: db.rollback()
        raise
    finally:
        db.close()


def identifier(value, label):
    if not isinstance(value, str) or not re.fullmatch(ID, value):
        raise ValueError(label + ': stable ID required')
    return value


def applicability(record):
    value = record.get('applicability', {'scope':'unknown', 'project_ids':[]})
    if not isinstance(value, dict) or set(value) != {'scope','project_ids'} or value['scope'] not in ('shared','projects','unknown'):
        raise ValueError('Invalid applicability')
    ids = value['project_ids']
    if not isinstance(ids,list) or len(set(ids)) != len(ids): raise ValueError('Unique Project IDs required')
    for key in ids: identifier(key,'Project ID')
    if bool(ids) != (value['scope'] == 'projects'): raise ValueError('Project IDs only required for projects scope')
    return value


def scope_issue(record, project_id):
    if project_id is None: return None  # Legacy discovery is not Project certification.
    value = applicability(record)
    if value['scope'] == 'unknown': return 'confirm applicability for Project ' + project_id
    if value['scope'] == 'projects' and project_id not in value['project_ids']: return 'outside Project scope: ' + project_id
    return None


def register(root, record, expected_sha=None):
    if not isinstance(record, dict): raise ValueError('Asset record must be an object')
    value = json.loads(canonical(record))
    if 'applicability' in value: applicability(value)
    for key in ('asset_id', 'entity_id'): identifier(value.get(key), key)
    if value.get('kind') not in ('organism', 'equipment', 'scene', 'other'): raise ValueError('Asset kind required')
    roles = value.get('roles')
    if not isinstance(roles, list) or not roles or any(not isinstance(r, str) or not r for r in roles):
        raise ValueError('Nonempty roles required')
    if len(set(roles)) != len(roles): raise ValueError('Duplicate roles')
    if value.get('stage') is not None and (not isinstance(value['stage'], str) or not value['stage']):
        raise ValueError('Stage must be a nonempty label or null')
    if value.get('origin') not in ('photo', 'specimen', 'diagram', 'generated', 'unknown'): raise ValueError('Origin required')
    source = value.get('source')
    if not isinstance(source, dict): raise ValueError('Source metadata required, unknown values allowed')
    if source.get('url') is not None and (not isinstance(source['url'], str) or not source['url'].startswith(('https://','http://'))):
        raise ValueError('Source URL must be HTTP(S) or null')
    publication = value.get('publication', {'visibility':'private','reviewed':False})
    if not isinstance(publication, dict) or publication.get('visibility') not in ('private', 'public') or type(publication.get('reviewed')) is not bool:
        raise ValueError('Invalid publication metadata')
    value['publication'] = publication
    review = value.get('review')
    if not isinstance(review, dict) or review.get('status') not in ('pass','fail','not_checked'):
        raise ValueError('Review must be pass/fail/not_checked; this records a human/AI declaration, not automatic visual QA')
    checked = review.get('roles', [])
    if not isinstance(checked, list) or any(r not in roles for r in checked): raise ValueError('Reviewed roles must belong to asset roles')
    if value.get('file') is not None:
        errors = binding_errors(root, value['file'], 'asset file')
        if errors: raise ValueError('; '.join(errors))
    elif not source.get('url'): raise ValueError('Local binding or source URL required')
    if review['status'] == 'pass':
        errors = binding_errors(root, review.get('evidence'), 'review evidence')
        if not checked: errors.append('Pass requires explicit reviewed roles')
        if errors: raise ValueError('; '.join(errors))
    required = value.get('requires', [])
    if not isinstance(required, list): raise ValueError('requires must be an ID list')
    for key in required: identifier(key, 'dependency')
    if value['asset_id'] in required or len(required) != len(set(required)): raise ValueError('Self/duplicate dependency')
    derivation = value.get('derivation')
    if derivation is not None:
        if not isinstance(derivation, dict) or not isinstance(derivation.get('operation'), str) or not derivation['operation'].strip():
            raise ValueError('Derivation needs parent_id, parent_record_sha256 and operation')
        parent = identifier(derivation.get('parent_id'), 'parent_id')
        if parent == value['asset_id']: raise ValueError('Asset cannot derive from itself')
        with connection(root) as db:
            found = db.execute('SELECT sha FROM assets WHERE id=?', (parent,)).fetchone() if db else None
        if not found or found[0] != derivation.get('parent_record_sha256'):
            raise ValueError('Derivation parent unavailable or changed; inspect parent before registering')
        if parent not in required: required.append(parent)
    value['requires'] = required
    # Validate optional size shape without claiming the measurement is truthful.
    size = value.get('size')
    if size is not None:
        if not isinstance(size, dict): raise ValueError('Size must be an object or null')
        if size.get('value') is not None and (type(size['value']) not in (int,float) or not math.isfinite(size['value']) or size['value'] <= 0):
            raise ValueError('Size value must be positive and finite')
    with connection(root, True) as db:
        old = db.execute('SELECT body,sha FROM assets WHERE id=?', (value['asset_id'],)).fetchone()
        if old and expected_sha != old[1]: raise ValueError('Existing asset requires current expected record SHA; no silent overwrite')
        if not old and expected_sha is not None: raise ValueError('Expected asset does not exist')
        value['revision'] = json.loads(old[0])['revision'] + 1 if old else 1
        sha = digest(value)
        db.execute('INSERT OR REPLACE INTO assets VALUES(?,?,?,?,?)', (value['asset_id'],value['entity_id'],value.get('stage'),canonical(value),sha))
    return dict(asset_id=value['asset_id'], revision=value['revision'], record_sha256=sha,
                note='Registered provenance and declared review only; not independent visual/biological verification')


def requests_checked(requests):
    if not isinstance(requests, list) or not requests: raise ValueError('Supply explicit entity/role requests')
    result = []
    for row in requests:
        if not isinstance(row, dict) or set(row) - {'entity_id','role','stage','variant','view'}: raise ValueError('Invalid asset request fields')
        identifier(row.get('entity_id'), 'entity_id')
        if not isinstance(row.get('role'), str) or not row['role']: raise ValueError('Role required')
        for key in ('stage','variant','view'):
            if key in row and row[key] is not None and (not isinstance(row[key], str) or not row[key]): raise ValueError('Invalid ' + key)
        if row not in result: result.append(row)
    return result


def matches(row, request):
    return (row['entity_id'] == request['entity_id'] and request['role'] in row['roles']
            and all(request.get(k) is None or row.get(k) == request[k] for k in ('stage','variant','view')))


def candidates(root, requests, project_id=None):
    if project_id is not None: identifier(project_id,'Project ID')
    requests = requests_checked(requests)
    rows = []
    with connection(root) as db:
        if db:
            entities = sorted({r['entity_id'] for r in requests})
            for body, sha in db.execute('SELECT body,sha FROM assets WHERE entity IN (' + ','.join('?' for _ in entities) + ') ORDER BY id', entities):
                row = json.loads(body)
                if digest(row) != sha: raise ValueError('Corrupt asset metadata hash')
                issue = scope_issue(row,project_id)
                if any(matches(row,r) for r in requests) and not (issue and issue.startswith('outside')): rows.append((row,sha))
    return requests, rows


def query(root, requests, limit=20, cursor=None, project_id=None):
    if type(limit) is not int or not 1 <= limit <= 100: raise ValueError('Page size must be 1..100')
    requests, rows = candidates(root, requests, project_id)
    fingerprint = digest(dict(requests=requests, project_id=project_id, matches=[(r['asset_id'],s) for r,s in rows]))
    offset = 0
    if cursor:
        if not isinstance(cursor, dict) or cursor.get('fingerprint') != fingerprint or type(cursor.get('offset')) is not int or cursor['offset'] < 0:
            raise ValueError('Asset query changed/invalid cursor; restart lookup')
        offset = cursor['offset']
    page = rows[offset:offset+limit]
    descriptors = [{**{k:r.get(k) for k in ('asset_id','entity_id','kind','stage','variant','roles','view','size','origin')},
                    'review':r['review']['status'], 'reviewed_roles':r['review'].get('roles',[]),
                    'source':{k:r['source'].get(k) for k in ('url','rights')},
                    'local_available':r.get('file') is not None,
                    'applicability':applicability(r), 'scope_issue':scope_issue(r,project_id)} for r,s in page]
    missing = [r for r in requests if not any(matches(row,r) and not scope_issue(row,project_id) for row,s in rows)]
    next_cursor = dict(offset=offset+limit, fingerprint=fingerprint) if offset+limit < len(rows) else None
    return dict(schema=1, assets=descriptors, missing=missing, next_cursor=next_cursor,
                scope='Matching metadata only. Select explicit IDs, verify bindings and open actual references before QA.')


def selection(root, requests, asset_ids, project_id=None):
    requests, rows = candidates(root, requests, project_id)
    if not isinstance(asset_ids, list) or len(set(asset_ids)) != len(asset_ids): raise ValueError('Explicit unique asset IDs required')
    choices = {r['asset_id']:(r,s) for r,s in rows}
    if any(key not in choices for key in asset_ids): raise ValueError('Selected asset is outside the requested scope')
    records, issues, visiting = {}, [], set()
    def add(key):
        if key in visiting: raise ValueError('Cyclic asset dependency')
        if key in records: return
        with connection(root) as db:
            found = db.execute('SELECT body,sha FROM assets WHERE id=?',(key,)).fetchone() if db else None
        if not found:
            issues.append('Missing component: ' + key)
            return
        row = json.loads(found[0])
        if digest(row) != found[1]: raise ValueError('Corrupt asset metadata hash')
        issue = scope_issue(row,project_id)
        if issue: issues.append(key + ': ' + issue)
        if len(visiting) >= 128: raise ValueError('Asset dependency chain too deep')
        visiting.add(key)
        for dep in row['requires']: add(dep)
        visiting.remove(key)
        derivation = row.get('derivation')
        if derivation and (derivation['parent_id'] not in records or records[derivation['parent_id']]['record_sha256'] != derivation['parent_record_sha256']):
            issues.append(key + ': derivation parent changed; review lineage')
        records[key] = dict(asset_id=key, record_sha256=found[1], file=row.get('file'), review_evidence=row['review'].get('evidence'))
        issues.extend(key + ': ' + e for e in binding_errors(root, row.get('file'), 'asset file'))
        needed = [r['role'] for r in requests if matches(row,r)] if key in asset_ids else row['roles']
        if row['kind']=='organism' and key in asset_ids and any(matches(row,r) and r.get('stage') is None for r in requests):
            issues.append(key + ': confirm intended life stage; do not auto-select adult')
        if row['review']['status'] != 'pass' or any(role not in row['review'].get('roles',[]) for role in needed):
            issues.append(key + ': required role review incomplete')
        else: issues.extend(key + ': ' + e for e in binding_errors(root,row['review'].get('evidence'),'review evidence'))
        if any(role in ('scale','biological-evidence') for role in needed):
            if row['origin']=='generated': issues.append(key + ': generated image cannot establish real size/biology')
        if 'scale' in needed:
            size = row.get('size') or {}
            if size.get('basis') not in ('measured','source_reported') or not size.get('value') or not size.get('unit') or not size.get('source'):
                issues.append(key + ': scale evidence incomplete')
    for key in asset_ids: add(key)
    for request in requests:
        if not any(matches(choices[key][0],request) for key in asset_ids): issues.append('Uncovered request: ' + canonical(request))
    result = dict(schema=1, requests=requests, selected_ids=asset_ids, records=list(records.values()), issues=issues,
                  status='needs_review' if issues else 'matched',
                  scope='Planned references only; hash and recorded review do not prove model use, perception or biological truth')
    if project_id is not None: result.update(schema=2, project_id=project_id)
    result['receipt_sha256'] = digest(result)
    return result


def verify(root, receipt, project_id=None):
    if not isinstance(receipt, dict) or receipt.get('schema') not in (1,2): raise ValueError('Unsupported asset selection')
    unsigned = {k:v for k,v in receipt.items() if k != 'receipt_sha256'}
    if digest(unsigned) != receipt.get('receipt_sha256'): raise ValueError('Modified asset selection receipt')
    bound_project = receipt.get('project_id') if receipt['schema']==2 else None
    if receipt['schema']==2: identifier(bound_project,'Project ID')
    if project_id is not None and bound_project != project_id:
        return dict(status='needs_review',issues=['Selection Project missing/mismatch; reselect for current Project'],scope='Legacy/other Project receipt is not Project-certified')
    rebuilt = selection(root, receipt.get('requests'), receipt.get('selected_ids'),bound_project)
    stale = rebuilt['records'] != receipt.get('records')
    if stale:
        return dict(status='stale', issues=['Selected asset metadata/file bindings changed; select and QA again'], scope=rebuilt['scope'])
    return dict(status=rebuilt['status'], issues=rebuilt['issues'], scope=rebuilt['scope'])


def details(root, asset_ids, project_id=None):
    if not isinstance(asset_ids,list) or not asset_ids: raise ValueError('Explicit asset IDs required')
    result=[]
    with connection(root) as db:
        for key in asset_ids:
            identifier(key,'asset ID')
            found=db.execute('SELECT body,sha FROM assets WHERE id=?',(key,)).fetchone() if db else None
            if not found: raise ValueError('Missing asset: '+key)
            row=json.loads(found[0])
            if digest(row)!=found[1]: raise ValueError('Corrupt metadata')
            issue=scope_issue(row,project_id)
            if issue and issue.startswith('outside'): raise ValueError(issue)
            result.append(dict(record=row,record_sha256=found[1],scope_issue=issue))
    return dict(assets=result,scope='Selected metadata only; inspect actual images')


def requirement_errors(value):
    if not isinstance(value,dict) or set(value)!={'schema','items','none_reason'} or value.get('schema')!=1:
        return ['reference_requirements: schema/items/none_reason required']
    items=value['items']
    if not isinstance(items,list): return ['reference_requirements.items: list required']
    if not items and (not isinstance(value['none_reason'],str) or not value['none_reason'].strip()):
        return ['reference_requirements: explain no reference needed']
    errors=[]
    for item in items:
        if not isinstance(item,dict): errors.append('reference requirement must be object');continue
        for field in ('subject','role','must_preserve','reason'):
            if not isinstance(item.get(field),str) or not item[field].strip():errors.append('reference requirement: '+field+' required')
        if item.get('applies_to') not in ('first_frame','video','both') or type(item.get('essential')) is not bool:
            errors.append('reference requirement: applies_to/essential required')
        for field in ('entity_id','variant','stage','view'):
            if item.get(field) is not None and (not isinstance(item[field],str) or not item[field].strip()):errors.append('Invalid requirement '+field)
    return errors


def import_bundle(root, manifest):
    """Import reviewed public references without overwriting local IDs or provenance."""
    data=read(local(root,manifest))
    if not isinstance(data,dict) or data.get('schema')!=1 or data.get('reviewed_for_publication') is not True or not isinstance(data.get('assets'),list):
        raise ValueError('Unsupported public asset bundle')
    records={};existing={};issues=[]
    for item in data['assets']:
        if not isinstance(item,dict):raise ValueError('Bundle record must be object')
        key=identifier(item.get('asset_id'),'asset ID')
        if key in records:raise ValueError('Duplicate bundle asset ID')
        if item.get('publication')!={'visibility':'public','reviewed':True} or item.get('review',{}).get('status')!='pass':raise ValueError('Bundle asset is not reviewed for publication')
        for bind in (item.get('file'),item.get('review',{}).get('evidence')):
            if not isinstance(bind,dict) or not isinstance(bind.get('path'),str) or not bind['path'].startswith('08-Assets/'):
                raise ValueError('Bundle file/evidence must be under 08-Assets')
            issues.extend(binding_errors(root,bind,key))
        applicability(item)
        records[key]=item
    if issues:raise ValueError('; '.join(issues))
    with connection(root) as db:
        if db:
            for key in records:
                found=db.execute('SELECT body,sha FROM assets WHERE id=?',(key,)).fetchone()
                if found:
                    row=json.loads(found[0])
                    if digest(row)!=found[1]:raise ValueError('Corrupt local metadata')
                    existing[key]=(row,found[1])
    # Preflight conflicts before any registration. Preserve existing local provenance.
    semantic=('entity_id','kind','stage','variant','view','roles','origin','source','requires','dimensions','reference_use','qa_scope')
    for key,(row,sha) in existing.items():
        incoming=records[key]
        same=(all(row.get(k)==incoming.get(k) for k in semantic)
              and applicability(row)==applicability(incoming)
              and (row.get('file') or {}).get('sha256')==incoming['file']['sha256']
              and row['review'].get('status')==incoming['review'].get('status')
              and row['review'].get('roles',[])==incoming['review'].get('roles',[]))
        problems=binding_errors(root,row.get('file'),key)+binding_errors(root,row['review'].get('evidence'),key)
        if not same or problems:raise ValueError('Local asset conflict; preserved without overwrite: '+key)
    order=[];visiting=set();done=set()
    def visit(key):
        if key in visiting:raise ValueError('Cyclic bundle dependency')
        if key in done:return
        if key not in records:raise ValueError('Bundle dependency absent: '+key)
        visiting.add(key)
        row=records[key]
        deps=list(row.get('requires',[]))
        parent=row.get('derived_from')
        if parent:
            if not isinstance(parent,dict) or not isinstance(parent.get('operation'),str) or not parent['operation'].strip():raise ValueError('Invalid bundle derivation')
            deps.append(identifier(parent.get('parent_id'),'derivation parent'))
        for dep in deps:visit(dep)
        visiting.remove(key);done.add(key);order.append(key)
    for key in records:visit(key)
    hashes={key:sha for key,(row,sha) in existing.items()};imported=[]
    for key in order:
        if key in existing:continue
        row=json.loads(canonical(records[key]));parent=row.pop('derived_from',None)
        row.pop('revision',None);row.pop('derivation',None)
        if parent:row['derivation']=dict(parent_id=parent['parent_id'],parent_record_sha256=hashes[parent['parent_id']],operation=parent['operation'])
        hashes[key]=register(root,row)['record_sha256'];imported.append(key)
    return dict(status='imported',imported=len(imported),kept_existing=len(existing),total=len(records),
                scope='Public references registered; no local IDs, files, approval or generation history overwritten')


def inputs_check(root, record, project_id=None, historical=False):
    """Check declared local tool arguments, not perception or proof a remote call ran."""
    errors=[]
    if not isinstance(record,dict) or record.get('schema')!=1: raise ValueError('Unsupported actual input record')
    identifier(record.get('project_id'),'Project ID')
    if project_id is not None and record['project_id']!=project_id:errors.append('Actual input Project mismatch')
    for key in ('production_id','attempt_id'):
        if not isinstance(record.get(key),str) or not record[key].strip():errors.append(key+' required')
    for key in ('call_id','cycle_id'):
        if record.get('outcome')=='not_submitted' and record.get(key) is None: continue
        if not isinstance(record.get(key),str) or not record[key].strip():errors.append(key+' required after reservation/dispatch')
    if record.get('outcome') not in ('not_submitted','success','error','cancelled','unknown'):errors.append('Invalid call outcome')
    tool=record.get('tool')
    if not isinstance(tool,dict) or tool.get('name') not in ('image_gen','9router_image') or not isinstance(tool.get('arguments'),dict):
        raise ValueError('Record actual image_gen/9router_image arguments')
    args=tool['arguments'];errors.extend(binding_errors(root,record.get('prompt'),'prompt'))
    if not errors:
        if local(root,record['prompt']['path']).read_text(encoding='utf-8-sig')!=args.get('prompt'):errors.append('Prompt differs from tool arguments')
    inputs=record.get('inputs')
    if not isinstance(inputs,list):raise ValueError('Explicit ordered inputs list required')
    paths=[];selection_record=None
    if record.get('selection') is not None:
        errors.extend(binding_errors(root,record['selection'],'selection receipt'))
        if not binding_errors(root,record['selection'],'selection receipt'):
            selection_record=read(local(root,record['selection']['path']))
            if not isinstance(selection_record,dict):raise ValueError('Selection receipt must be object')
            unsigned={k:v for k,v in selection_record.items() if k!='receipt_sha256'}
            if digest(unsigned)!=selection_record.get('receipt_sha256'):errors.append('Modified selection receipt')
            if selection_record.get('project_id')!=record['project_id']:errors.append('Selection Project mismatch')
            if selection_record.get('status')!='matched':errors.append('Selection is not matched')
            if not historical:
                check=verify(root,selection_record,record['project_id'])
                if check['status']!='matched':errors.extend(check['issues'])
    for item in inputs:
        if not isinstance(item,dict): errors.append('Invalid input entry');continue
        errors.extend(binding_errors(root,item,'actual input'))
        if item.get('kind') not in ('reference','edit_target','supporting') or not isinstance(item.get('purpose'),str) or not item['purpose'].strip():errors.append('Input kind/purpose required')
        paths.append(str(local(root,item.get('path'))))
        if item.get('asset_id') is not None:
            selected=next((r for r in (selection_record or {}).get('records',[]) if r['asset_id']==item['asset_id']),None)
            if not selected or selected.get('file')!={k:item.get(k) for k in ('path','sha256')}:errors.append('Input not bound to selected asset: '+str(item['asset_id']))
    supplied=args.get('referenced_image_paths',[])
    if not isinstance(supplied,list) or any(not isinstance(p,str) for p in supplied):errors.append('Invalid referenced_image_paths')
    elif [str(Path(p).resolve()) for p in supplied]!=paths:errors.append('Ordered actual paths differ from tool arguments')
    if args.get('num_last_images_to_include') is not None:
        errors.append('Conversation references need manual evidence; local-path verifier cannot certify them')
    if historical and record.get('outcome')!='success':errors.append('Handoff needs successful call outcome')
    if record.get('output') is not None:errors.extend(binding_errors(root,record['output'],'output'))
    elif historical:errors.append('Handoff needs output binding')
    return dict(status='needs_review' if errors else 'matched',issues=errors,
                scope='Declared arguments and file bindings only; does not prove tool dispatch, model adherence or QA')


def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('action',choices=['init','register','query','read','select','verify','inputs-check','import-bundle'])
    parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--asset',action='append',default=[])
    parser.add_argument('--expected-sha')
    parser.add_argument('--project-id')
    parser.add_argument('--historical',action='store_true',help='Validate pinned actual inputs without re-resolving current catalog')
    parser.add_argument('--limit',type=int,default=20)
    parser.add_argument('--cursor',help='JSON cursor returned by previous query')
    parser.add_argument('--out')
    args=parser.parse_args();root=args.root.resolve()
    if args.action=='init':
        with connection(root,True): pass
        result={'catalog':CATALOG,'status':'initialized','note':'No assets or video IDs allocated'}
    elif args.action=='import-bundle':
        if args.input is None:parser.error('Public bundle manifest required')
        result=import_bundle(root,args.input.as_posix())
    else:
        if args.input is None: parser.error('input JSON required')
        data=read(args.input)
        if not isinstance(data,dict): raise ValueError('Input must be a JSON object')
        if args.action=='register':result=register(root,data,args.expected_sha)
        elif args.action=='query':result=query(root,data.get('requests'),args.limit,json.loads(args.cursor) if args.cursor else None,args.project_id)
        elif args.action=='read':result=details(root,args.asset,args.project_id)
        elif args.action=='verify':result=verify(root,data,args.project_id)
        elif args.action=='inputs-check':result=inputs_check(root,data,args.project_id,args.historical)
        else:result=selection(root,data.get('requests'),args.asset,args.project_id)
    if args.out:
        target=local(root,args.out);rel=target.relative_to(root).as_posix()
        if not rel.startswith(('.nature-studio/context/','.nature-studio/audits/')): raise ValueError('Save receipts only under local context/audits; never overwrite source or production history')
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('x',encoding='utf-8',newline='\n') as stream: stream.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'path':rel,'status':result.get('status'),'issues':result.get('issues',[])},ensure_ascii=False))
    else:print(json.dumps(result,ensure_ascii=False,indent=2))
    if result.get('status') in ('needs_review','stale'): raise SystemExit(2)


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    try:main()
    except (ValueError, OSError, sqlite3.Error, TypeError) as exc:
        print(json.dumps({'errors':[str(exc)]},ensure_ascii=False));raise SystemExit(1)
