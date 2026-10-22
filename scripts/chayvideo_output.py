"""Deterministic text checks and append-only attempt writes; no semantic/media QA."""
import argparse
import hashlib
from decimal import Decimal
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import uuid

from chayvideo_context import ROOT, inside, slug_ok
from video_ids import project as project_id

FIELDS = ('idea', 'first_frame_prompt', 'video_prompt', 'caption')
FRAME_FIELDS = ('subjects', 'environment', 'composition', 'initial_state')
CAPTION_STYLES = ('standard', 'humor', 'curiosity')
CAPTION_VARIANT_FIELDS = ('caption', 'caption_vi', 'hook_text', 'hook_vi')


def hook_words(text):
    """Contractions count once; hyphen/dash-separated words count separately."""
    return re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*", text)


def caption_phrase(text):
    return ' '.join(hook_words(text.split('#', 1)[0].casefold()))


def caption_bundle_errors(data, underwater=False):
    if 'caption_variants' not in data:
        return ['caption_variant requires caption_variants'] if 'caption_variant' in data else []
    bundle=data['caption_variants']
    if not isinstance(bundle,dict) or set(bundle)!={'schema','variants'} or type(bundle.get('schema')) is not int or bundle['schema']!=1:
        return ['caption_variants: schema 1 and variants required']
    variants=bundle['variants']
    if not isinstance(variants,dict) or not variants or set(variants)-set(CAPTION_STYLES):
        return ['caption_variants: nonempty standard/humor/curiosity map required']
    selected=data.get('caption_variant','standard')
    errors=[];seen_captions=set();seen_hooks=set()
    if not isinstance(selected,str) or selected not in variants:
        errors.append('caption_variant must be supplied in variants');selected=None
    for style,item in variants.items():
        label='caption_variants.'+style
        if not isinstance(item,dict) or set(item)!=set(CAPTION_VARIANT_FIELDS):
            errors.append(label+': caption/caption_vi/hook_text/hook_vi required');continue
        bad=False
        for field in CAPTION_VARIANT_FIELDS:
            text=item[field]
            if not isinstance(text,str) or not text.strip() or re.search(r'[\r\n]|\\[nr]',text):
                errors.append(label+'.'+field+': nonempty single paragraph required');bad=True
        if bad:continue
        # Reuse the same Project rules for every publishable English caption.
        errors.extend(label+': '+e for e in validate({'caption':item['caption']},mode='caption',underwater=underwater))
        hook=item['hook_text']
        if not 1<=len(hook_words(hook))<=9:errors.append(label+': hook_text requires 1–9 English words')
        if '#' in hook:errors.append(label+': hook_text must not include hashtags')
        if underwater and re.search(r'\bAI\b|\bAI[- ]generated\b',hook,re.I):errors.append(label+': hook_text AI mention')
        cap_key=caption_phrase(item['caption']);hook_key=caption_phrase(hook)
        if cap_key in seen_captions:errors.append(label+': repeated caption wording')
        if hook_key in seen_hooks:errors.append(label+': repeated hook wording')
        if cap_key==hook_key:errors.append(label+': hook repeats caption wording')
        seen_captions.add(cap_key);seen_hooks.add(hook_key)
    if selected is not None and selected in variants and isinstance(variants[selected],dict) and data.get('caption')!=variants[selected].get('caption'):
        errors.append('caption must equal the selected English caption, including hashtags')
    return errors


def merged_caption_bundle(previous, incoming):
    """Only use when caption changes without story/opening changes."""
    if previous is None:return incoming
    return dict(schema=1,variants={**previous['variants'],**incoming['variants']})


def render_caption_variants(bundle):
    labels=dict(standard='Chuẩn',humor='Hài hước',curiosity='Tò mò');lines=[]
    for style in CAPTION_STYLES:
        item=bundle['variants'].get(style)
        if item is None:continue
        lines.extend(['## '+labels[style],'',
                      '**Caption:** '+item['caption'],'',
                      '**Lược dịch caption:** '+item['caption_vi'],'',
                      '**Hook text:** '+item['hook_text'],'',
                      '**Lược dịch hook:** '+item['hook_vi'],''])
    return '\n'.join(lines)


def frame_errors(state):
    if not isinstance(state, dict) or set(state) != set(FRAME_FIELDS):
        return ['frame_state: supply subjects, environment, composition, initial_state']
    return [f'frame_state.{key}: nonempty text required' for key in FRAME_FIELDS
            if not isinstance(state[key], str) or not state[key].strip()]


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def production(root, slug, production_id):
    slug_ok(slug)
    if not isinstance(production_id, str) or not re.fullmatch(r'(?:[A-Z]{3}-[0-9]{5}|[A-Z]{2}-[0-9]{4})', production_id):
        raise ValueError('Invalid production ID')
    folder = inside(root, f'04-Productions/{slug}/{production_id}')
    if not folder.is_dir():
        raise ValueError('Existing production required; no ID is allocated')
    if not re.fullmatch(r'UF-[0-9]{4}', production_id):
        identity = json.loads((folder / 'IDENTITY.json').read_text(encoding='utf-8-sig'))
        if identity.get('video_id') != production_id:
            raise ValueError('Reserved identity mismatch')
        if identity.get('project_id') not in (None, project_id(root, slug)):
            raise ValueError('Reserved Project identity mismatch')
        if re.fullmatch(r'[A-Z]{2}-[0-9]{4}', production_id):
            if production_id.endswith('-0000') or identity.get('schema') != 2 or identity.get('id_format') != 'XX-YYYY' or identity.get('project_id') != project_id(root, slug):
                raise ValueError('Invalid v2 reserved identity')
            try:
                for key in ('project_uuid', 'video_uuid'):
                    uuid.UUID(identity.get(key, ''))
            except (ValueError, TypeError, AttributeError) as exc:
                raise ValueError('Invalid v2 identity UUID') from exc
    return folder


def local_file(folder, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Use a production-relative path with forward slashes')
    rel = Path(relative)
    path = (folder / rel).resolve()
    if rel.is_absolute() or '..' in rel.parts or not path.is_relative_to(folder.resolve()):
        raise ValueError('Path outside production')
    if not path.is_file():
        raise ValueError(f'Missing file: {relative}')
    return path


def attempt_file(folder, ref):
    if not isinstance(ref, str) or not re.fullmatch(r'(?:attempts/)?A\d+', ref):
        raise ValueError('Explicit attempt required: A01 or attempts/A01; never latest')
    file = local_file(folder, ref + '/OUTPUT.json')
    if (file.parent / 'SAVE-INCOMPLETE.txt').exists():
        raise ValueError(f'Incomplete attempt: {ref}')
    return file


def resolve(root, slug, production_id, attempt):
    """Read an explicit revision chain, without selecting, approving or writing anything."""
    folder = production(root, slug, production_id)
    chain, seen = [], set()
    ref = attempt
    while True:
        file = attempt_file(folder, ref)
        if file in seen:
            raise ValueError('Revision cycle')
        if len(chain) >= 128:
            raise ValueError('Revision chain too deep; inspect sources')
        seen.add(file)
        data = json.loads(file.read_text(encoding='utf-8-sig'))
        if not isinstance(data, dict):
            raise ValueError(f'Invalid OUTPUT: {ref}')
        if 'state_schema' in data and data['state_schema'] != 1:
            raise ValueError(f'Unsupported state_schema: {ref}')
        for key in FIELDS:
            if key in data and (not isinstance(data[key], str) or not data[key].strip()):
                raise ValueError(f'Invalid {key}: {ref}')
        if 'frame_state' in data and frame_errors(data['frame_state']):
            raise ValueError(f'Invalid frame_state: {ref}')
        if 'reference_requirements' in data:
            import asset_catalog
            if asset_catalog.requirement_errors(data['reference_requirements']): raise ValueError('Invalid reference requirements: '+ref)
        if caption_bundle_errors(data,underwater=(slug=='underwater')):
            raise ValueError('Invalid caption bundle: '+ref)
        chain.append((ref, file, data))
        parent = data.get('base_attempt')
        if parent is None:
            if not all(key in data for key in FIELDS):
                raise ValueError(f'Legacy/partial attempt {ref} has no explicit base; inspect original sources')
            if data.get('mode') in {'revision', 'caption'}:
                raise ValueError(f'Missing revision base: {ref}')
            break
        base = attempt_file(folder, parent)
        if data.get('base_sha256') != sha256(base):
            raise ValueError(f'Base changed: {parent}; inspect sources before reuse')
        ref = parent
    values, sources, state = {}, {}, None
    metadata, assets, requirements = {}, None, None
    caption_bundle, caption_variant = None, None
    for ref, file, data in reversed(chain):
        changed = set(FIELDS).intersection(data)
        if data.get('mode') == 'caption' and (changed != {'caption'} or any(k in data for k in ('frame_state','reference_requirements','asset_selection'))):
            raise ValueError('Caption attempt must not change story or frame state')
        if changed.intersection(FIELDS[:3]):
            # A semantic revision cannot silently certify unchanged t=0.
            state = data.get('frame_state')
            caption_bundle, caption_variant = None, None
        if 'video_prompt' in changed:
            metadata = {k:data[k] for k in ('checks','contract_exception','contract_version') if k in data}
        if changed.intersection(FIELDS[:3]):
            assets = data.get('asset_selection')
            requirements = data.get('reference_requirements')
        if 'caption' in changed:
            if 'caption_variants' in data:
                caption_bundle=merged_caption_bundle(caption_bundle,data['caption_variants'])
                caption_variant=data.get('caption_variant','standard')
            else:
                caption_bundle,caption_variant=None,None
        for key in changed:
            values[key] = data[key]
            sources[key] = dict(attempt=ref, sha256=sha256(file))
    if caption_bundle is not None and caption_bundle_errors(dict(caption=values.get('caption'),caption_variants=caption_bundle,caption_variant=caption_variant),underwater=(slug=='underwater')):
        raise ValueError('Invalid resolved caption bundle')
    result = dict(production_id=production_id, project=slug, attempt=attempt,
                attempt_sha256=sha256(chain[0][1]),
                output=values, sources=sources, frame_state=state,
                validation_metadata=metadata, validation_status='recorded' if metadata.get('checks') else 'unverified',
                asset_selection=assets, asset_selection_status='planned' if assets else 'unverified',
                reference_requirements=requirements, reference_status='recorded' if requirements is not None else 'unverified',
                caption_variants=caption_bundle, caption_variant=caption_variant,
                caption_variants_status='recorded' if caption_bundle else 'unverified',
                frame_state_status='recorded' if state else 'unverified',
                scope='Explicit inputs only; no selection, approval or semantic QA')
    if state:
        result['frame_inputs'] = frame_snapshot(result)
        result['frame_inputs_sha256'] = snapshot_hash(result['frame_inputs'])
    return result


def with_resolved_base(root, slug, production_id, resolved, data):
    """Fill the base from the resolve output the AI reviewed; save still rejects a base changed since."""
    if (resolved.get('project'), resolved.get('production_id')) != (slug, production_id):
        raise ValueError('Resolve output belongs to another Project/production')
    data = dict(data)
    for key, value in (('base_attempt', resolved.get('attempt')), ('base_sha256', resolved.get('attempt_sha256'))):
        if data.setdefault(key, value) != value:
            raise ValueError(f'{key} differs from the reviewed resolve output')
    return data


def frame_snapshot(resolved):
    """Only opening-state inputs; caption and later motion do not invalidate an image."""
    state = resolved.get('frame_state')
    if frame_errors(state):
        raise ValueError('Opening state unverified; record/review frame_state first')
    return dict(frame_state=state, first_frame_prompt=resolved['output']['first_frame_prompt'])


def snapshot_hash(snapshot):
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def check_frame(root, slug, production_id, attempt, handoff='FIRST-FRAME.json'):
    """Verify recorded bindings, never infer image quality from metadata."""
    folder = production(root, slug, production_id)
    current = resolve(root, slug, production_id, attempt)
    record = json.loads(local_file(folder, handoff).read_text(encoding='utf-8-sig'))
    if not isinstance(record, dict):
        raise ValueError('Invalid handoff object')
    errors, review, unknown = [], [], []
    if record.get('production_id') != production_id or record.get('project_id') != project_id(root, slug):
        errors.append('Handoff production/Project mismatch')
    if record.get('qa_status') != 'qa_pass':
        review.append('No recorded qa_pass')
    for path_key, hash_key in [('image_path', 'sha256'), ('review_path', 'review_sha256')]:
        try:
            path = local_file(folder, record.get(path_key))
            expected = record.get(hash_key)
            if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
                unknown.append(f'Missing/invalid {hash_key}')
            elif sha256(path) != expected:
                errors.append(f'{path_key} hash changed')
        except ValueError as exc:
            errors.append(str(exc))
    snapshot = record.get('frame_inputs')
    if not isinstance(snapshot, dict) or set(snapshot) != {'frame_state', 'first_frame_prompt'}:
        unknown.append('Legacy/missing frame_inputs; review actual image against current opening state')
    elif frame_errors(snapshot['frame_state']) or not isinstance(snapshot['first_frame_prompt'], str) or not snapshot['first_frame_prompt'].strip():
        errors.append('Malformed frame_inputs')
    elif record.get('frame_inputs_sha256') != snapshot_hash(snapshot):
        errors.append('Recorded frame_inputs hash mismatch')
    else:
        try:
            if snapshot != frame_snapshot(current):
                review.append('Opening inputs changed; inspect actual image, do not automatically regenerate')
        except ValueError as exc:
            unknown.append(str(exc))
    # Bind the QA snapshot to the exact source attempt; do not require current==QA attempt.
    if record.get('schema') in (2,3):
        image_attempt = record.get('attempt_id')
        if not isinstance(image_attempt, str) or not re.fullmatch(r'(?:attempts/)?A\d+', image_attempt):
            errors.append('Explicit image attempt_id required')
        else:
            directory = (folder / image_attempt).resolve()
            if not directory.is_relative_to(folder.resolve()) or not directory.is_dir():
                errors.append('Image attempt missing/outside production')
            elif (directory / 'SAVE-INCOMPLETE.txt').exists():
                errors.append('Image attempt incomplete')
        try:
            reviewed = resolve(root, slug, production_id, record.get('source_attempt'))
            if record.get('source_attempt_sha256') != sha256(attempt_file(folder, record.get('source_attempt'))):
                errors.append('QA source attempt changed')
            if frame_snapshot(reviewed) != snapshot:
                errors.append('QA snapshot does not match its source attempt')
        except (ValueError, FileNotFoundError) as exc:
            unknown.append(str(exc))
    else:
        unknown.append('Legacy handoff needs explicit provenance review; never silently upgraded')
    asset_status='unverified'
    if record.get('schema') == 3 or record.get('asset_inputs') is not None:
        try:
            import asset_catalog
            bind=record.get('asset_inputs')
            problems=asset_catalog.binding_errors(root,bind,'asset_inputs')
            if problems: raise ValueError('; '.join(problems))
            inputs=json.loads(asset_catalog.local(root,bind['path']).read_text(encoding='utf-8-sig'))
            checked=asset_catalog.inputs_check(root,inputs,project_id(root,slug),historical=True)
            if inputs.get('production_id')!=production_id or inputs.get('attempt_id')!=record.get('attempt_id'):
                raise ValueError('Actual input production/attempt mismatch')
            for key in ('call_id','cycle_id'):
                if inputs.get(key)!=record.get(key): raise ValueError('Actual input '+key+' mismatch')
            expected_output=dict(path=local_file(folder,record['image_path']).relative_to(root.resolve()).as_posix(),sha256=record['sha256'])
            if inputs.get('output')!=expected_output:raise ValueError('Actual input receipt output differs from handoff image')
            if checked['status']!='matched':raise ValueError('; '.join(checked['issues']))
            asset_status='matched'
            req=current.get('reference_requirements')
            opening=[r for r in (req or {}).get('items',[]) if r['applies_to'] in ('first_frame','both')]
            if record.get('reference_requirements_sha256')!=snapshot_hash(opening):
                review.append('Opening reference requirements changed/unbound; review actual image')
        except (ValueError,TypeError,KeyError,OSError) as exc:
            errors.append('Asset input evidence: '+str(exc));asset_status='invalid'
    criteria = record.get('qa_sources')
    if not isinstance(criteria, dict) or not criteria:
        unknown.append('Missing QA criteria hashes')
    else:
        required = {'00-Standards/first-frame.md', '00-Standards/quality-review.md',
                    f'03-Projects/{slug}/PROJECT.md'}
        if not required.issubset(criteria):
            unknown.append('Missing common/Project QA source bindings')
        for rel, expected in criteria.items():
            try:
                if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or '..' in Path(rel).parts:
                    raise ValueError('Use workspace-relative QA source paths')
                path = inside(root, rel)
                if not path.is_file() or sha256(path) != expected:
                    review.append(f'QA criteria missing/changed: {rel}')
            except (ValueError, TypeError):
                errors.append('Invalid QA criteria path')
    status = 'invalid' if errors else 'needs_review' if review else 'unverified' if unknown else 'matched'
    return dict(status=status, errors=errors, needs_review=review, unverified=unknown,
                asset_inputs_status=asset_status,
                scope='Recorded file/input bindings only; image QA and user approval remain independent')


def handoff(root, slug, production_id, source_attempt, image_attempt, image, review, qa_status,
            width, height, qa_sources=(), asset_inputs=None, call_id=None, cycle_id=None,
            limitations=(), actual_model='unknown', promote=False):
    """Write a schema-3 handoff from files the AI already reviewed; every hash is computed, none copied."""
    folder = production(root, slug, production_id)
    if qa_status not in ('qa_pass', 'qa_incomplete', 'qa_fail'):
        raise ValueError('qa_status must be qa_pass, qa_incomplete or qa_fail')
    attempt_dir = (folder / image_attempt).resolve()
    if not re.fullmatch(r'(?:attempts/)?A\d+', image_attempt) or not attempt_dir.is_dir():
        raise ValueError('Existing image attempt required, e.g. A05')
    current = resolve(root, slug, production_id, source_attempt)
    opening = [r for r in (current.get('reference_requirements') or {}).get('items', [])
               if r['applies_to'] in ('first_frame', 'both')]
    criteria = ['00-Standards/first-frame.md', '00-Standards/quality-review.md',
                f'03-Projects/{slug}/PROJECT.md', *qa_sources]
    # Schema 3 adds actual asset-input evidence; without it the record is schema 2.
    record = dict(schema=3 if asset_inputs else 2, production_id=production_id, project_id=project_id(root, slug),
                  attempt_id=image_attempt, source_attempt=source_attempt,
                  source_attempt_sha256=current['attempt_sha256'], cycle_id=cycle_id, qa_status=qa_status,
                  image_path=image, sha256=sha256(local_file(folder, image)),
                  measured_width=width, measured_height=height,
                  review_path=review, review_sha256=sha256(local_file(folder, review)),
                  frame_inputs=frame_snapshot(current), frame_inputs_sha256=None,
                  qa_sources={rel: sha256(inside(root, rel)) for rel in dict.fromkeys(criteria)},
                  requested_model='gpt-image-2.5-sunburst', actual_model=actual_model,
                  model_verified=False, user_approved=False, user_approval_path=None,
                  limitations=list(limitations), call_id=call_id,
                  reference_requirements_sha256=snapshot_hash(opening))
    record['frame_inputs_sha256'] = snapshot_hash(record['frame_inputs'])
    if asset_inputs:
        import asset_catalog
        record['asset_inputs'] = dict(path=asset_inputs, sha256=asset_catalog.file_hash(asset_catalog.local(root, asset_inputs)))
    else:
        record['asset_inputs'] = None
    target = attempt_dir / 'FIRST-FRAME-HANDOFF.json'
    if target.exists():
        raise ValueError('Handoff already written for this attempt; never overwrite QA history')
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    relative = target.relative_to(folder.resolve()).as_posix()
    checked = check_frame(root, slug, production_id, source_attempt, relative)
    promoted, main_record = False, folder / 'FIRST-FRAME.json'
    if promote and qa_status == 'qa_pass' and checked['status'] == 'matched':
        # Replace only a FIRST-FRAME.json that is preserved byte-for-byte in some attempt's handoff.
        kept = not main_record.exists() or any(
            p.read_bytes() == main_record.read_bytes() for p in folder.rglob('FIRST-FRAME-HANDOFF.json') if p != target)
        if not kept:
            raise ValueError('Existing FIRST-FRAME.json has no per-attempt copy; preserve it before promoting')
        shutil.copyfile(target, main_record)
        promoted = True
    return dict(handoff=relative, promoted=promoted, check=checked)


def effective_contract(root, slug, production_id, data, mode, for_save=False):
    """Verify scoped bindings, not the authorship of the saved user request."""
    contract = dict(version='underwater-3' if slug == 'underwater' else 'common-1', beat_count=None)
    selection = data.get('asset_selection') if isinstance(data, dict) else None
    if selection is not None:
        import asset_catalog
        if not isinstance(selection,dict):raise ValueError('Asset selection must be object')
        expected_project=project_id(root,slug) if selection.get('schema')==2 else None
        if expected_project is not None and selection.get('project_id')!=expected_project:raise ValueError('Asset selection Project mismatch')
        status = asset_catalog.verify(root, selection,expected_project)
        if status['status'] == 'stale': raise ValueError('Asset selection stale; select/review current references')
    exception = data.get('contract_exception') if isinstance(data, dict) else None
    if exception is None: return contract
    if slug != 'underwater' or mode == 'caption' or not production_id:
        raise ValueError('Beat exception requires explicit Underwater production and non-caption scope')
    base = production(root, slug, production_id)
    if not isinstance(exception, dict): raise ValueError('Exception must bind path/sha256')
    file = local_file(base, exception.get('path'))
    if sha256(file) != exception.get('sha256'): raise ValueError('Exception record changed')
    grant = json.loads(file.read_text(encoding='utf-8-sig'))
    if not isinstance(grant, dict) or grant.get('schema') != 1 or grant.get('rule') != 'beat_count':
        raise ValueError('Unsupported exception rule/schema')
    if (grant.get('project'), grant.get('production'), grant.get('mode')) != (slug, production_id, mode):
        raise ValueError('Exception scope mismatch')
    count = grant.get('beat_count')
    if type(count) is not int or count < 1: raise ValueError('Exception beat count must be a positive integer')
    if grant.get('confirmed_user_request') is not True:
        raise ValueError('Agent must first confirm the real user request, not merely a file declaration')
    authorization = grant.get('authorization')
    if not isinstance(authorization, dict): raise ValueError('Saved request binding required')
    request = local_file(base, authorization.get('path'))
    if sha256(request) != authorization.get('sha256'): raise ValueError('User request evidence changed')
    text = data.get('video_prompt')
    if not isinstance(text, str) or grant.get('video_prompt_sha256') != hashlib.sha256(text.encode('utf-8')).hexdigest():
        raise ValueError('Exception does not match this video prompt')
    if mode in ('revision','reference') and data.get('base_attempt') is not None:
        if (grant.get('base_attempt'),grant.get('base_sha256')) != (data.get('base_attempt'),data.get('base_sha256')):
            raise ValueError('Exception base scope mismatch')
    elif mode == 'revision':
        raise ValueError('Revision exception requires base binding')
    target = grant.get('target_attempt')
    if not isinstance(target,str) or not re.fullmatch(r'(?:attempts/)?A[0-9]+',target):
        raise ValueError('Exception requires one explicit target attempt')
    if for_save and (base / target).exists(): raise ValueError('Exception target already exists; never reuse a grant for a new attempt')
    contract.update(beat_count=count, target_attempt=target)
    return contract


def location_tag_errors(data, required):
    """UF-D023: one declared location hashtag, shared by every caption; choosing it stays semantic QA."""
    checks = data.get('checks') if isinstance(data.get('checks'), dict) else {}
    tag, reason = checks.get('location_tag'), checks.get('location_none_reason')
    if tag is None:
        if required and 'caption' in data and not (isinstance(reason, str) and reason.strip()):
            return ['checks.location_tag: declare the location hashtag, or location_none_reason for legacy without a locked setting']
        return []
    if not isinstance(tag, str) or not re.fullmatch(r'#\w+', tag):
        return ['checks.location_tag: one hashtag such as #LouisianaFishing']
    captions = [data['caption']] if isinstance(data.get('caption'), str) else []
    bundle = data.get('caption_variants')
    if isinstance(bundle, dict) and isinstance(bundle.get('variants'), dict):
        captions += [v['caption'] for v in bundle['variants'].values() if isinstance(v, dict) and isinstance(v.get('caption'), str)]
    return [f'caption: location tag {tag} must appear exactly once in every caption' for caption in captions
            if [t.casefold() for t in re.findall(r'#\w+', caption)].count(tag.casefold()) != 1][:1]


def validate(data, mode='new', underwater=False, contract=None):
    if not isinstance(data, dict):
        return ['Output must be a JSON object']
    errors = []
    errors.extend(caption_bundle_errors(data,underwater))
    if any(k in data for k in ('caption_variants','caption_variant')) and 'caption' not in data:
        errors.append('caption bundle changes require the selected caption field')
    if data.get('contract_exception') is not None and contract is None:
        errors.append('Exception requires bound Project/production context')
    if mode == 'caption' and any(k in data for k in ('asset_selection','contract_exception','reference_requirements')):
        errors.append('caption: must not change reference or contract bindings')
    if mode == 'caption' and (any(k in data for k in FIELDS[:3]) or 'frame_state' in data):
        errors.append('caption: only caption may change')
    if 'frame_state' in data:
        errors.extend(frame_errors(data['frame_state']))
    if 'reference_requirements' in data:
        import asset_catalog
        errors.extend(asset_catalog.requirement_errors(data['reference_requirements']))
    required = (('caption',) if mode == 'caption' else
                tuple(k for k in FIELDS if k in data) if mode == 'revision' else FIELDS)
    if not required:
        errors.append('revision: supply at least one output field')
    for key in required:
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f'Missing/non-string {key}')
    for key in FIELDS[1:]:
        if key in data and isinstance(data[key], str) and re.search(r'[\r\n]|\\[nr]', data[key]):
            errors.append(f'{key}: must be one paragraph')
    caption = data.get('caption')
    if underwater and isinstance(caption, str):
        tags = re.findall(r'#[\w]+', caption)
        if not 3 <= len(tags) <= 5 or len({x.casefold() for x in tags}) != len(tags):
            errors.append('caption: require 3–5 distinct hashtags')
        if not caption.split('#', 1)[0].strip():
            errors.append('caption: missing hook')
        if re.search(r'\bAI\b|\bAI[- ]generated\b', caption, re.I) or any(
                re.match(r'#(?:ai(?:generated|video|art|content)?|generativeai)$', t, re.I) for t in tags):
            errors.append('caption: AI mention/tag')
        if any(t.casefold() == '#underwater' for t in tags):
            errors.append('caption: #Underwater excluded')
    if underwater and mode != 'caption':
        errors.extend(location_tag_errors(data, required=mode in ('new', 'reference')))
    if underwater and mode != 'caption' and isinstance(data.get('video_prompt'), str):
        text = data['video_prompt']
        beats = re.findall(r'\[(\d+(?:\.\d+)?)\s*[–—-]\s*(\d+(?:\.\d+)?)s\]', text)
        beats = [(Decimal(a), Decimal(b)) for a, b in beats]
        count = contract.get('beat_count') if isinstance(contract, dict) else None
        if not (len(beats) == count if count is not None else 5 <= len(beats) <= 10):
            errors.append('video_prompt: beat count must match explicit exception' if count is not None else 'video_prompt: 5–10 beats required')
        if (not beats or beats[0][0] != 0 or beats[-1][1] != 10
                or any(a >= b for a, b in beats)
                or any(beats[i][1] != beats[i+1][0] for i in range(len(beats)-1))):
            errors.append('video_prompt: positive contiguous timeline from 0 to 10s required')
        checks = data.get('checks', {})
        if mode in ('new', 'reference') and not re.search(r'\bhand-?held\b', text, re.I):
            errors.append('video_prompt: handheld camera (UF-D021) required for new/reference sets')
        key = checks.get('key_onset') if isinstance(checks, dict) else None
        try:
            onset = Decimal(str(key))
            if not onset.is_finite() or not 5 < onset < 10:
                raise ValueError()
        except (ValueError, ArithmeticError):
            errors.append('checks.key_onset: provide actual intended onset >5 and <10')
        # UF-D025: hook 0–3s is a declared, early, non-decisive signal; a beat must close by 3.0s.
        if beats and beats[0][1] > 3:
            errors.append('video_prompt: first beat must end by 3.0s (UF-D025 hook)')
        hook = checks.get('hook_signal') if isinstance(checks, dict) else None
        try:
            signal = Decimal(str(hook))
            if isinstance(hook, bool) or not signal.is_finite() or not 0 < signal <= 3:
                raise ValueError()
        except (ValueError, ArithmeticError):
            errors.append('checks.hook_signal: provide intended first new signal time within (0, 3.0]s')
    return errors


def save(root, slug, production_id, data, mode='new'):
    """Only an existing reserved/legacy production; the ID allocator remains authoritative.

    Data.files supplies AI-authored attempt documents, not fake generated metadata.
    Root brief/concept/ledger updates remain explicit workflow steps, never overwritten here.
    """
    base = production(root, slug, production_id)
    data=dict(data)
    if ('caption_variants' in data and mode in ('caption','revision')
            and not any(k in data for k in FIELDS[:3])):
        # Validate the supplied patch before merging; never inherit a stale selection.
        patch_errors=caption_bundle_errors(data,underwater=(slug=='underwater'))
        if patch_errors:raise ValueError('; '.join(patch_errors))
        previous=resolve(root,slug,production_id,data.get('base_attempt'))
        data['caption_variants']=merged_caption_bundle(previous.get('caption_variants'),data['caption_variants'])
    contract = effective_contract(root, slug, production_id, data, mode, for_save=True)
    errors = validate(data, mode, underwater=(slug == 'underwater'), contract=contract)
    if errors:
        raise ValueError('; '.join(errors))
    provenance = dict(state_schema=1, mode=mode, contract_version=contract['version'])
    if mode in {'revision', 'caption'}:
        ref = data.get('base_attempt')
        resolve(root, slug, production_id, ref)
        base_file = attempt_file(base, ref)
        expected = data.get('base_sha256')
        if expected != sha256(base_file):
            raise ValueError('Supply current base_sha256 from resolve; base missing or changed')
        provenance.update(base_attempt=ref, base_sha256=expected)
    docs = data.get('files', {})
    required = ('INPUTS.md', 'settings.md', 'review.md')
    if not isinstance(docs, dict) or any(not isinstance(docs.get(k), str) or not docs[k].strip() for k in required):
        raise ValueError('Supply INPUTS.md, settings.md, review.md with true prompt-only provenance')
    allowed = set(required) | {'revision.md'}
    if set(docs) - allowed:
        raise ValueError('Unexpected attempt document/path')
    # Respect actual local layout, do not relocate legacy attempts.
    parent = inside(root, (base / 'attempts').relative_to(root)) if (base / 'attempts').is_dir() else base
    stage = Path(tempfile.mkdtemp(prefix='.chayvideo-', dir=parent))
    try:
        payload = dict(docs)
        for key, name in [('first_frame_prompt', 'first-frame-prompt.md'),
                          ('video_prompt', 'video-prompt.md'), ('caption', 'caption.md')]:
            if key in data:
                payload[name] = data[key]
        if 'caption_variants' in data:
            data.setdefault('caption_variant','standard')
            payload['caption-variants.md']=render_caption_variants(data['caption_variants'])
        payload['OUTPUT.json'] = json.dumps({**{k: data[k] for k in (*FIELDS, 'frame_state', 'checks', 'contract_exception', 'asset_selection', 'reference_requirements','caption_variants','caption_variant') if k in data}, **provenance},
                                          ensure_ascii=False, indent=2)
        for name, text in payload.items():
            (stage / name).write_text(text.rstrip() + '\n', encoding='utf-8')
        numbers = [int(p.name[1:]) for p in parent.iterdir()
                   if p.is_dir() and re.fullmatch(r'A\d+', p.name)]
        number = max(numbers, default=0) + 1
        while True:
            dest = parent / f'A{number:02d}'
            if contract.get('target_attempt') and dest.relative_to(base).as_posix() != contract['target_attempt']:
                raise ValueError('Exception target is not the next attempt; review scope before saving')
            # mkdir(exist_ok=False) reserves the destination without replacing old attempts.
            try:
                dest.mkdir()
                break
            except FileExistsError:
                if contract.get('target_attempt'): raise ValueError('Exception attempt was concurrently consumed')
                number += 1
        try:
            for path in stage.iterdir():
                path.rename(dest / path.name)
        except BaseException:
            # Keep incomplete attempt visible for recovery; never overwrite a prior attempt.
            (dest / 'SAVE-INCOMPLETE.txt').write_text('Inspect interrupted save before reuse.', encoding='utf-8')
            raise
        return dest
    finally:
        shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('command', choices=('check', 'save', 'resolve', 'check-frame', 'handoff'))
    parser.add_argument('input', type=Path, help='JSON output, or the source attempt for resolve/check-frame/handoff')
    parser.add_argument('--mode', choices=('new', 'revision', 'caption', 'reference'), default='new')
    parser.add_argument('--project', required=True)
    parser.add_argument('--production')
    parser.add_argument('--handoff', default='FIRST-FRAME.json')
    parser.add_argument('--frame-inputs', action='store_true', help='Include QA snapshot only when preparing a handoff')
    parser.add_argument('--out', type=Path, help='resolve: also write the JSON shown, for save --from-resolve')
    parser.add_argument('--from-resolve', type=Path, help='save: take base_attempt/base_sha256 from a resolve output already reviewed')
    group = parser.add_argument_group('handoff (paths relative to production)')
    group.add_argument('--image-attempt')
    group.add_argument('--image')
    group.add_argument('--review')
    group.add_argument('--qa-status')
    group.add_argument('--width', type=int)
    group.add_argument('--height', type=int)
    group.add_argument('--qa-source', action='append', default=[], help='Extra Project QA criteria, workspace-relative')
    group.add_argument('--asset-inputs', help='Actual asset input record, workspace-relative')
    group.add_argument('--call-id')
    group.add_argument('--cycle-id')
    group.add_argument('--limitation', action='append', default=[])
    group.add_argument('--actual-model', default='unknown')
    group.add_argument('--promote', action='store_true', help='Also copy a matched qa_pass handoff to FIRST-FRAME.json')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command in {'resolve', 'check-frame', 'handoff'}:
        if not args.production:
            parser.error('--production required')
        if args.command == 'resolve':
            result = resolve(root, args.project, args.production, args.input.as_posix())
            if not args.frame_inputs:
                result.pop('frame_inputs', None)
                result.pop('frame_inputs_sha256', None)
            if args.out:
                out = inside(root, args.out.as_posix())
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        elif args.command == 'handoff':
            missing = [k for k in ('image_attempt', 'image', 'review', 'qa_status', 'width', 'height') if getattr(args, k) is None]
            if missing:
                parser.error('handoff requires --' + ', --'.join(m.replace('_', '-') for m in missing))
            result = handoff(root, args.project, args.production, args.input.as_posix(), args.image_attempt,
                             args.image, args.review, args.qa_status, args.width, args.height, args.qa_source,
                             args.asset_inputs, args.call_id, args.cycle_id, args.limitation, args.actual_model, args.promote)
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(0 if result['check']['status'] == 'matched' else 2)
        else:
            result = check_frame(root, args.project, args.production, args.input.as_posix(), args.handoff)
        # resolve stays complete: the AI must see the full inherited text it builds on.
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.command == 'resolve' else None))
        sys.exit(0 if args.command == 'resolve' or result['status'] == 'matched' else 2)
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    if args.from_resolve:
        data = with_resolved_base(root, args.project, args.production,
                                  json.loads(inside(root, args.from_resolve.as_posix()).read_text(encoding='utf-8-sig')), data)
    if args.command == 'check':
        contract = effective_contract(args.root.resolve(), args.project, args.production, data, args.mode)
        errors = validate(data, args.mode, args.project == 'underwater', contract=contract)
        scope = ('Syntax and declared Underwater gates; no semantic/media QA' if args.project == 'underwater'
                 else 'Common syntax only; AI must review the actual Project contract')
        print(json.dumps(dict(errors=errors, scope=scope), ensure_ascii=False))
        sys.exit(bool(errors))
    if not args.production:
        parser.error('--production required for save')
    print(save(args.root.resolve(), args.project, args.production, data, args.mode))


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    try:
        main()
    except (ValueError, OSError) as exc:
        print(json.dumps({'errors': [str(exc)], 'scope': 'No automatic source repair'}, ensure_ascii=False))
        sys.exit(1)
