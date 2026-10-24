"""/na-combo runtime: fixed Google Sheet (videos paged by 50 IDs + lessons tab), lesson sync and media handoff.

Never generates content or judges quality. AI decides semantics (dedupe, lesson wording, QA); this tool keeps
the sheet, the lesson files and the local media state consistent and records who changed what.
"""
from datetime import date, datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

import combo_sheet as cs

ROOT = Path(__file__).resolve().parents[1]
STATE = '.nature-studio/combo'
STATUS_DIRS = {'active': 'active', 'candidate': 'candidates', 'retired': 'retired'}
SHEET_STATUS = {'active': 'Đã duyệt', 'candidate': 'Chờ duyệt'}
RETIRED_LABELS = ('Không duyệt', 'Ngừng áp dụng')
STATUS_OPTIONS = ['Đã duyệt', 'Chờ duyệt', *RETIRED_LABELS]
RATING_OPTIONS = ['Dùng', 'Sửa', 'Bỏ']
LESSON_TYPES = ['Ràng buộc', 'Định hướng sáng tạo']
VIDEO_COLUMNS = [
    ('id', 'Mã video', 11), ('date', 'Ngày tạo', 11), ('slot', 'Suất', 12), ('species', 'Loài', 11), ('setting', 'Bối cảnh', 22),
    ('direction', 'Hướng chủ đề', 14), ('idea', 'Ý TƯỞNG', 60), ('first_frame_prompt', 'FIRST FRAME PROMPT', 60),
    ('video_prompt', 'VIDEO PROMPT', 70),
    ('cap_standard', 'Caption Chuẩn (EN + hashtag)', 34), ('cap_standard_vi', 'Lược dịch Chuẩn', 26),
    ('hook_standard', 'Hook Chuẩn', 20), ('hook_standard_vi', 'Lược dịch hook Chuẩn', 20),
    ('cap_humor', 'Caption Hài hước (EN + hashtag)', 34), ('cap_humor_vi', 'Lược dịch Hài hước', 26),
    ('hook_humor', 'Hook Hài hước', 20), ('hook_humor_vi', 'Lược dịch hook Hài hước', 20),
    ('cap_curiosity', 'Caption Tò mò (EN + hashtag)', 34), ('cap_curiosity_vi', 'Lược dịch Tò mò', 26),
    ('hook_curiosity', 'Hook Tò mò', 20), ('hook_curiosity_vi', 'Lược dịch hook Tò mò', 20),
    ('gear', 'Mồi/dụng cụ/con mồi', 30), ('hook_signal', 'Tín hiệu 3s đầu (s)', 9), ('key_onset', 'Key onset (s)', 9),
    ('qa_text', 'QA văn bản', 20), ('qa_image', 'QA ảnh first frame', 20), ('qa_overall', 'Kết quả', 12),
    ('image_info', 'Ảnh (attempt · kích thước · lượt)', 22), ('qa_notes', 'Ghi chú QA', 40),
    ('lessons_applied', 'Bài học đã áp dụng', 30), ('image_link', 'Link ảnh first frame', 34),
    ('user_rating', 'Bạn chấm', 10), ('user_note', 'Ghi chú của bạn', 30)]
USER_VIDEO_KEYS = ('user_rating', 'user_note')
LESSON_COLUMNS = [
    ('id', 'Mã', 14), ('type', 'Loại', 16), ('group', 'Nhóm', 16), ('applies', 'Áp dụng cho', 26), ('action', 'Bài học', 70),
    ('basis', 'Căn cứ', 40), ('sources', 'Video nguồn', 18), ('confirmations', 'Số lần xác nhận', 9), ('status', 'Trạng thái', 14),
    ('author', 'Người tạo', 9), ('user_note', 'Ý kiến của bạn', 34), ('updated', 'Cập nhật', 11), ('merged', 'Trùng/gộp với', 18)]
USER_LESSON_KEYS = ('type', 'group', 'applies', 'action', 'status', 'user_note')


def now():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def state(root, *parts):
    path = root.joinpath(STATE, *parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else default


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def config(root):
    data = load_json(state(root, 'config.json'))
    if not data:
        raise ValueError('Run combo.py init first')
    return data


def drive(cfg):
    return cs.Drive(cfg['remote'], cfg['folder_id'])


# ── lessons ────────────────────────────────────────────────────────────────

def project_slug(root, project_id):
    for path in (root / '03-Projects').glob('*/PROJECT.md'):
        text = path.read_text(encoding='utf-8-sig')
        if re.search(rf'^ID:\s*{re.escape(project_id)}\s*$', text, re.M):
            return path.parent.name
    raise ValueError('Unknown Project ID')


def read_lesson(path):
    text = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    _, meta, body = text.split('---', 2)
    return json.loads(meta), body


def _write_keep_eol(path, text, crlf=None):
    """Write text keeping the file's existing line endings (CRLF lessons stay CRLF)."""
    if crlf is None:
        crlf = path.is_file() and b'\r\n' in path.read_bytes()
    path.write_bytes((text.replace('\r\n', '\n').replace('\n', '\r\n') if crlf else text).encode('utf-8'))


def write_lesson(path, meta, body, crlf=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_keep_eol(path, '---\n' + json.dumps(meta, ensure_ascii=False, indent=2) + '\n---' + body, crlf)


def namespaces(root, slug):
    return [('project', root / '05-Memory/projects' / slug), ('shared', root / '05-Memory/shared')]


def lessons(root, slug):
    found = []
    for scope, base in namespaces(root, slug):
        for status, folder in STATUS_DIRS.items():
            for path in sorted((base / folder).glob('L-*.md')):
                meta, body = read_lesson(path)
                found.append(dict(path=path, scope=scope, meta=meta, body=body))
    return found


def sheet_status(meta):
    if meta['status'] == 'retired':
        return meta.get('sheet', {}).get('retired_as', 'Ngừng áp dụng')
    return SHEET_STATUS[meta['status']]


def _index_line(meta, folder, name):
    return f"- [{meta['id']} v{meta['version']} — {meta['status']}]({folder}/{name})"


def _reindex(base, meta, old_rel, new_rel):
    index = base / 'INDEX.md'
    text = index.read_text(encoding='utf-8') if index.is_file() else '# Bộ nhớ\n'
    lines = [l for l in text.splitlines() if not (old_rel and f']({old_rel})' in l) and f']({new_rel})' not in l]
    folder, name = new_rel.split('/')
    lines.append(_index_line(meta, folder, name))
    _write_keep_eol(index, '\n'.join(lines) + '\n')


def bump(version):
    parts = version.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)


def set_status(root, lesson, target, *, by, authority=None, reason='', today=None):
    """Move a lesson to the status chosen in the sheet. `by` is 'user' or 'ai'."""
    meta, path = lesson['meta'], lesson['path']
    today = today or date.today().isoformat()
    base = path.parent.parent
    old_rel = f'{path.parent.name}/{path.name}'
    new_status = {'Đã duyệt': 'active', 'Chờ duyệt': 'candidate'}.get(target, 'retired')
    if target not in STATUS_OPTIONS:
        raise ValueError('Unknown sheet status: ' + target)
    if new_status == 'active':
        if by == 'user':
            if not authority:
                raise ValueError('User approval needs an approval receipt file')
            meta['activation'] = dict(method='user', date=today, authority=authority)
            meta['validation']['unresolved_conflicts'] = []
        elif meta.get('activation', {}).get('method') != 'automatic':
            raise ValueError('AI activation must be recorded by the objective gate (automatic) before moving')
    sheet = meta.setdefault('sheet', {})
    if new_status == 'retired':
        sheet['retired_as'] = target
        meta['retirement'] = dict(date=today, by=by, reason=reason or target, authority=authority)
    meta['status'] = new_status
    meta['version'] = bump(meta['version'])
    sheet['updated'] = today
    body = lesson['body'].rstrip('\n') + f"\n\n{today} — v{meta['version']}: {target} ({'người dùng qua sheet' if by == 'user' else 'AI'})" \
        + (f'; {reason}' if reason else '') + '.\n'
    new_path = base / STATUS_DIRS[new_status] / path.name
    write_lesson(new_path, meta, body, crlf=b'\r\n' in path.read_bytes())
    if new_path != path:
        path.unlink()
    _reindex(base, meta, old_rel, f'{STATUS_DIRS[new_status]}/{path.name}')
    lesson.update(path=new_path, meta=meta, body=body)
    return lesson


def new_lesson(root, slug, spec, *, today=None):
    """Create a lesson from an AI/user spec after the AI has checked for duplicates."""
    today = today or date.today().isoformat()
    cfg_project = None
    for path in (root / '03-Projects' / slug).glob('PROJECT.md'):
        cfg_project = re.search(r'^ID:\s*(\S+)', path.read_text(encoding='utf-8-sig'), re.M).group(1)
    scope = spec.get('scope', 'project')
    status = spec.get('status', 'candidate')
    meta = dict(
        id=spec.get('id') or f'L-{uuid.uuid4()}', version='0.1', status=status, kind=spec['kind'], action=spec['action'],
        transfer_rationale=spec.get('transfer_rationale') if scope == 'shared' else None, scope=scope,
        project_id=cfg_project if scope == 'project' else None, origin_project_ids=[cfg_project],
        production_ids=spec.get('production_ids', []), publication=dict(visibility='private', reviewed=False),
        conditions=dict(tasks=spec['tasks'], models=spec.get('models', []), interfaces=spec.get('interfaces', []), formats=spec.get('formats', [])),
        evidence=spec['evidence'],
        validation=dict(result=spec.get('validation_result', 'not_checked'), method=spec.get('validation_method', 'not_checked'),
                        records=spec.get('validation_records', []), regression_checked=spec.get('regression_checked', False),
                        unresolved_conflicts=[], changes_policy=False),
        activation=spec.get('activation', dict(method='none', date=None, authority=None)),
        retrieval=dict(schema=1, summary=spec['summary'], topics=spec.get('topics', []), entities=spec.get('entities', []),
                       interactions=spec.get('interactions', [])),
        sheet=dict(type=spec['type'], group=spec['group'], applies=spec['applies'], basis=spec['basis'],
                   confirmations=spec.get('confirmations', 1), author=spec.get('author', 'AI'), updated=today,
                   user_note=spec.get('user_note', ''), merged=spec.get('merged', '')))
    if meta['sheet']['type'] not in LESSON_TYPES:
        raise ValueError('type must be one of ' + ', '.join(LESSON_TYPES))
    if meta['sheet']['type'] == 'Định hướng sáng tạo' and status == 'active' and meta['activation']['method'] == 'automatic':
        raise ValueError('Creative-direction lessons are never auto-approved')
    base = dict(namespaces(root, slug))[scope]
    path = base / STATUS_DIRS[status] / f"{meta['id']}.md"
    if path.exists():
        raise ValueError('Lesson ID exists')
    body = f"\n\n# {spec.get('title', spec['summary'])}\n\n{spec.get('detail', spec['action'])}\n\n{today} — v0.1: tạo bởi {meta['sheet']['author']} qua /na-combo.\n"
    write_lesson(path, meta, body)
    _reindex(base, meta, None, f'{STATUS_DIRS[status]}/{path.name}')
    return dict(id=meta['id'], path=str(path.relative_to(root)))


def confirm_lesson(root, lesson, *, source, note='', today=None):
    """Record a repeat observation instead of creating a duplicate lesson."""
    meta = lesson['meta']
    sheet = meta.setdefault('sheet', {})
    sheet['confirmations'] = int(sheet.get('confirmations', 1)) + 1
    sheet['updated'] = today or date.today().isoformat()
    if source and source not in meta['production_ids']:
        meta['production_ids'].append(source)
    meta['version'] = bump(meta['version'])
    body = lesson['body'].rstrip('\n') + f"\n\n{sheet['updated']} — v{meta['version']}: xác nhận lại ({source}). {note}\n"
    write_lesson(lesson['path'], meta, body)
    base = lesson['path'].parent.parent
    rel = f"{lesson['path'].parent.name}/{lesson['path'].name}"
    _reindex(base, meta, rel, rel)


def lesson_row(lesson):
    meta, sheet = lesson['meta'], lesson['meta'].get('sheet', {})
    return dict(id=meta['id'], type=sheet.get('type', 'Ràng buộc'), group=sheet.get('group', ''),
                applies=sheet.get('applies', ', '.join(meta['conditions']['tasks'])), action=meta['action'],
                basis=sheet.get('basis', meta['retrieval']['summary']), sources=', '.join(meta.get('production_ids', [])),
                confirmations=sheet.get('confirmations', 1), status=sheet_status(meta),
                author=sheet.get('author', 'AI'), user_note=sheet.get('user_note', ''),
                updated=sheet.get('updated', ''), merged=sheet.get('merged', '') or ('shared' if lesson['scope'] == 'shared' else ''))


# ── videos ─────────────────────────────────────────────────────────────────

def productions(root, slug, prefix):
    base = root / '04-Productions' / slug
    return sorted(p for p in base.glob(f'{prefix}-[0-9][0-9][0-9][0-9]') if p.is_dir())


def latest_output(prod):
    attempts = sorted((p for p in prod.glob('A[0-9]*') if (p / 'OUTPUT.json').is_file()),
                      key=lambda p: int(re.sub(r'\D', '', p.name)))
    return load_json(attempts[-1] / 'OUTPUT.json') if attempts else None


def build_row(root, prod, extra):
    """Merge OUTPUT.json + media.json + COMBO-ROW.json overrides into one sheet row (dict)."""
    out = latest_output(prod) or {}
    variants = (out.get('caption_variants') or {}).get('variants', {})
    row = dict(id=prod.name, idea=out.get('idea', ''), first_frame_prompt=out.get('first_frame_prompt', ''),
               video_prompt=out.get('video_prompt', ''), hook_signal=(out.get('checks') or {}).get('hook_signal', ''),
               key_onset=(out.get('checks') or {}).get('key_onset', ''))
    for style in ('standard', 'humor', 'curiosity'):
        v = variants.get(style, {})
        row.update({f'cap_{style}': v.get('caption', ''), f'cap_{style}_vi': v.get('caption_vi', ''),
                    f'hook_{style}': v.get('hook_text', ''), f'hook_{style}_vi': v.get('hook_vi', '')})
    if not variants and out.get('caption'):
        row['cap_standard'] = out['caption']
    media = load_json(prod / 'media.json', {})
    if media:
        row['image_link'] = media.get('link', '')
        row['image_info'] = f"{media.get('attempt', '')} · {media.get('width', '')}x{media.get('height', '')} · {media.get('calls', '')}"
    row.update(load_json(prod / 'COMBO-ROW.json', {}))
    row.update({k: v for k, v in extra.items() if v not in (None, '')})
    failed = 'CHƯA ĐẠT' in str(row.get('qa_text', '')).upper() or 'CHƯA ĐẠT' in str(row.get('qa_image', '')).upper()
    row.setdefault('qa_overall', 'CHƯA ĐẠT' if failed else ('ĐẠT' if row.get('qa_image') else ''))
    if failed:
        row['qa_overall'] = 'CHƯA ĐẠT'
    return row


def write_row(root, video_id, fields, slug, prefix):
    prod = root / '04-Productions' / slug / video_id
    if not prod.is_dir() or not video_id.startswith(prefix + '-'):
        raise ValueError('Unknown production ' + video_id)
    current = load_json(prod / 'COMBO-ROW.json', {})
    unknown = set(fields) - {k for k, _, _ in VIDEO_COLUMNS}
    if unknown:
        raise ValueError('Unknown row fields: ' + ', '.join(sorted(unknown)))
    current.update(fields)
    save_json(prod / 'COMBO-ROW.json', current)
    return current


def page_name(prefix, number, size):
    start = (number - 1) // size * size + 1
    return f'{prefix}-{start:04d} – {prefix}-{start + size - 1:04d}'


# ── sheet sync ─────────────────────────────────────────────────────────────

def rows_by_header(rows, columns):
    if not rows:
        return []
    header = {h: i for i, h in enumerate(rows[0])}
    out = []
    for raw in rows[1:]:
        item = {key: (raw[header[title]] if title in header and header[title] < len(raw) else '').strip()
                for key, title, _ in columns}
        if any(item.values()):
            out.append(item)
    return out


def pull(root):
    """Download the live sheet and diff it against what /na-combo last pushed (= edits made by the user)."""
    cfg = config(root)
    stamp = now()
    result = dict(stamp=stamp, sheet=None, video_feedback={}, lesson_changes=[], new_lessons=[], removed_rows=[])
    if not cfg.get('sheet_file_id'):
        return result
    snap = state(root, 'snapshots', f'{stamp}.xlsx')
    drive(cfg).download_sheet(cfg['sheet_name'], snap)
    tabs = cs.read_xlsx(snap)
    last = load_json(state(root, 'last-push.json'), {'videos': {}, 'lessons': {}})
    for name, rows in tabs.items():
        if name == cfg['lessons_tab']:
            continue
        for item in rows_by_header(rows, VIDEO_COLUMNS):
            vid = item.get('id')
            if vid:
                result['video_feedback'][vid] = {k: item[k] for k in USER_VIDEO_KEYS}
    sheet_lessons = rows_by_header(tabs.get(cfg['lessons_tab'], []), LESSON_COLUMNS)
    seen = set()
    for item in sheet_lessons:
        lid = item.get('id')
        if not lid:
            if item.get('action'):
                result['new_lessons'].append(item)
            continue
        seen.add(lid)
        before = last['lessons'].get(lid)
        if before is None:
            result['new_lessons'].append(item)
            continue
        changed = {k: dict(before=before.get(k, ''), after=item[k]) for k in USER_LESSON_KEYS if item[k] != str(before.get(k, ''))}
        if changed:
            result['lesson_changes'].append(dict(id=lid, changes=changed))
    result['removed_rows'] = sorted(set(last['lessons']) - seen)
    result['sheet'] = str(snap.relative_to(root))
    receipt = dict(schema=1, kind='combo-sheet-user-edits', pulled_at=stamp, sheet_file_id=cfg['sheet_file_id'],
                   snapshot=result['sheet'], snapshot_sha256=sha(snap), lesson_changes=result['lesson_changes'],
                   new_lessons=result['new_lessons'], removed_rows=result['removed_rows'])
    if result['lesson_changes'] or result['new_lessons'] or result['removed_rows']:
        receipt_path = state(root, 'approvals', f'{stamp}.json')
        save_json(receipt_path, receipt)
        result['receipt'] = str(receipt_path.relative_to(root))
    save_json(state(root, 'last-pull.json'), result)
    return result


def apply_user(root, pull_result):
    """Apply status/text/note edits the user made in the sheet. New rows are left to the AI (dedupe first)."""
    cfg = config(root)
    slug = cfg['project']
    index = {l['meta']['id']: l for l in lessons(root, slug)}
    applied = []
    for change in pull_result['lesson_changes']:
        lesson = index.get(change['id'])
        if not lesson:
            applied.append(dict(id=change['id'], skipped='not in memory'))
            continue
        meta, sheet = lesson['meta'], lesson['meta'].setdefault('sheet', {})
        c = change['changes']
        dirty = False
        for key in ('type', 'group', 'applies', 'user_note'):
            if key in c:
                sheet[key] = c[key]['after']
                dirty = True
        if 'action' in c and c['action']['after']:
            meta['action'] = c['action']['after']
            sheet['author'] = 'AI + Bạn' if sheet.get('author', 'AI') == 'AI' else sheet['author']
            dirty = True
        if dirty:
            meta['version'] = bump(meta['version'])
            sheet['updated'] = date.today().isoformat()
            lesson['body'] = lesson['body'].rstrip('\n') + f"\n\n{sheet['updated']} — v{meta['version']}: người dùng sửa trong sheet ({', '.join(sorted(c))}); biên nhận {pull_result['receipt']}.\n"
            write_lesson(lesson['path'], meta, lesson['body'])
        if 'status' in c and c['status']['after'] in STATUS_OPTIONS:
            set_status(root, lesson, c['status']['after'], by='user', authority=pull_result['receipt'],
                       reason=sheet.get('user_note', ''))
        applied.append(dict(id=change['id'], fields=sorted(c)))
    return applied


def push(root, extra_rows=None):
    """Rebuild the workbook from production records and lesson files, keep user columns, upload as the same sheet."""
    cfg = config(root)
    slug, prefix, size = cfg['project'], cfg['prefix'], cfg['page_size']
    feedback = (load_json(state(root, 'last-pull.json'), {}) or {}).get('video_feedback', {})
    pages = {}
    pushed_videos = {}
    for prod in productions(root, slug, prefix):
        number = int(prod.name.split('-')[1])
        row = build_row(root, prod, {**feedback.get(prod.name, {}), **(extra_rows or {}).get(prod.name, {})})
        pages.setdefault(page_name(prefix, number, size), []).append([row.get(k, '') for k, _, _ in VIDEO_COLUMNS])
        pushed_videos[prod.name] = {k: row.get(k, '') for k in USER_VIDEO_KEYS}
    rating_col = cs.col_name([k for k, _, _ in VIDEO_COLUMNS].index('user_rating'))
    overall_col = cs.col_name([k for k, _, _ in VIDEO_COLUMNS].index('qa_overall'))
    sheets = []
    for name in sorted(pages):
        sheets.append(dict(name=name, rows=[[t for _, t, _ in VIDEO_COLUMNS], *pages[name]], widths=[w for _, _, w in VIDEO_COLUMNS],
                           min_rows=size, dropdowns=[dict(range=f'{rating_col}2:{rating_col}{size + 1}', options=RATING_OPTIONS)],
                           highlights=[dict(column=overall_col, contains='CHƯA ĐẠT', color='red')]))
    lesson_rows, pushed_lessons = [], {}
    for lesson in sorted(lessons(root, slug), key=lambda l: (l['meta']['status'] != 'candidate', l['meta']['id'])):
        row = lesson_row(lesson)
        lesson_rows.append([row[k] for k, _, _ in LESSON_COLUMNS])
        pushed_lessons[row['id']] = {k: row[k] for k in USER_LESSON_KEYS}
    status_col = cs.col_name([k for k, _, _ in LESSON_COLUMNS].index('status'))
    type_col = cs.col_name([k for k, _, _ in LESSON_COLUMNS].index('type'))
    sheets.append(dict(name=cfg['lessons_tab'], rows=[[t for _, t, _ in LESSON_COLUMNS], *lesson_rows],
                       widths=[w for _, _, w in LESSON_COLUMNS], min_rows=300,
                       dropdowns=[dict(range=f'{status_col}2:{status_col}300', options=STATUS_OPTIONS),
                                  dict(range=f'{type_col}2:{type_col}300', options=LESSON_TYPES)],
                       highlights=[dict(column=status_col, contains='Chờ duyệt', color='yellow'),
                                   dict(column=status_col, contains='Không duyệt', color='red')]))
    with tempfile.TemporaryDirectory() as tmp:
        local = Path(tmp) / 'combo.xlsx'
        cs.write_xlsx(local, sheets)
        drv = drive(cfg)
        drv.upload_sheet(local, cfg['sheet_name'])
        file_id = next((x['ID'] for x in drv.list() if x['Name'] == cfg['sheet_name'] + '.xlsx'), None)
    if cfg.get('sheet_file_id') and file_id != cfg['sheet_file_id']:
        raise RuntimeError('Sheet file ID changed; refusing to continue without review')
    cfg['sheet_file_id'] = file_id
    save_json(state(root, 'config.json'), cfg)
    save_json(state(root, 'last-push.json'), dict(pushed_at=now(), videos=pushed_videos, lessons=pushed_lessons))
    return dict(sheet_file_id=file_id, url=f'https://docs.google.com/spreadsheets/d/{file_id}/edit',
                tabs=[s['name'] for s in sheets], videos=len(pushed_videos), lessons=len(pushed_lessons))


def media(root, items):
    """Upload QA'd first frames, verify checksums, record location, then delete local generated images."""
    cfg = config(root)
    slug = cfg['project']
    done = []
    with tempfile.TemporaryDirectory() as tmp:
        upload = Path(tmp)
        plan = []
        for item in items:  # {'id','attempt','status','calls'}; status qa_pass|qa_fail
            prod = root / '04-Productions' / slug / item['id']
            image = prod / item['attempt'] / 'first-frame.png'
            if not image.is_file():
                raise ValueError(f'Missing {image}')
            tag = 'QA-DAT' if item['status'] == 'qa_pass' else 'CHUA-DAT'
            name = f"{item['id']}_first-frame_{item['attempt']}_{tag}.png"
            shutil.copy(image, upload / name)
            plan.append((item, prod, image, name))
        drv = drive(cfg)
        drv.upload_files(upload)
        drv.check(upload)
        ids = {x['Name']: x['ID'] for x in drv.list()}
    for item, prod, image, name in plan:
        record = load_json(image.with_suffix('.9router.json'), {}) or load_json(image.parent / 'FIRST-FRAME-HANDOFF.json', {})
        record.setdefault('width', record.get('measured_width'))
        record.setdefault('height', record.get('measured_height'))
        link = f'https://drive.google.com/file/d/{ids[name]}/view'
        deleted = [(str(p.relative_to(prod)), sha(p)) for p in sorted(prod.glob('A*/*.png'))]
        save_json(prod / 'media.json', dict(link=link, drive_file_id=ids[name], name=name, attempt=item['attempt'],
                                            status=item['status'], width=record.get('width'), height=record.get('height'),
                                            calls=item.get('calls', ''), uploaded_sha256=sha(image), deleted_local=deleted))
        (prod / 'MEDIA-LOCATION.md').write_text(
            f"# Media location\nProduction ID: {item['id']}\nUploaded {name} → {link} (rclone check: match).\n"
            'Generated images were deleted locally after upload per user instruction; hashes in media.json allow verification '
            'after re-download. Local image paths in FIRST-FRAME.json/handoffs now point to deleted files.\n', encoding='utf-8')
        for rel, _ in deleted:
            (prod / rel).unlink()
        done.append(dict(id=item['id'], link=link, deleted=len(deleted)))
    return done


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('init'); p.add_argument('--project', required=True); p.add_argument('--prefix', required=True)
    p.add_argument('--remote', required=True); p.add_argument('--folder-id', required=True); p.add_argument('--sheet-name', required=True)
    p.add_argument('--sheet-file-id'); p.add_argument('--page-size', type=int, default=50); p.add_argument('--lessons-tab', default='Bài học')
    sub.add_parser('pull')
    p = sub.add_parser('apply-user'); p.add_argument('--pull', type=Path)
    p = sub.add_parser('lessons'); p.add_argument('--status', choices=['active', 'candidate', 'retired'])
    p = sub.add_parser('lesson-new'); p.add_argument('spec', type=Path)
    p = sub.add_parser('lesson-confirm'); p.add_argument('id'); p.add_argument('--source', required=True); p.add_argument('--note', default='')
    p = sub.add_parser('lesson-status'); p.add_argument('id'); p.add_argument('status', choices=STATUS_OPTIONS)
    p.add_argument('--reason', default='')
    p = sub.add_parser('row'); p.add_argument('id'); p.add_argument('fields', type=Path)
    p = sub.add_parser('media'); p.add_argument('items', type=Path)
    sub.add_parser('push')
    args = parser.parse_args()
    root = ROOT
    if args.action == 'init':
        current = load_json(state(root, 'config.json'), {})
        current.update(project=args.project, prefix=args.prefix, remote=args.remote, folder_id=args.folder_id,
                       sheet_name=args.sheet_name, page_size=args.page_size, lessons_tab=args.lessons_tab)
        if args.sheet_file_id:
            current['sheet_file_id'] = args.sheet_file_id
        save_json(state(root, 'config.json'), current)
        result = current
    elif args.action == 'pull':
        result = pull(root)
    elif args.action == 'apply-user':
        result = apply_user(root, load_json(args.pull or state(root, 'last-pull.json')))
    elif args.action == 'lessons':
        result = [dict(lesson_row(l), scope=l['scope'], path=str(l['path'].relative_to(root)), summary=l['meta']['retrieval']['summary'])
                  for l in lessons(root, config(root)['project']) if not args.status or l['meta']['status'] == args.status]
    elif args.action == 'lesson-new':
        result = new_lesson(root, config(root)['project'], load_json(args.spec))
    elif args.action in ('lesson-confirm', 'lesson-status'):
        lesson = next((l for l in lessons(root, config(root)['project']) if l['meta']['id'] == args.id), None)
        if not lesson:
            raise ValueError('Unknown lesson ' + args.id)
        if args.action == 'lesson-confirm':
            confirm_lesson(root, lesson, source=args.source, note=args.note)
        else:
            set_status(root, lesson, args.status, by='ai', reason=args.reason)
        result = dict(id=args.id, path=str(lesson['path'].relative_to(root)), status=lesson['meta']['status'])
    elif args.action == 'row':
        cfg = config(root)
        result = write_row(root, args.id, load_json(args.fields), cfg['project'], cfg['prefix'])
    elif args.action == 'media':
        result = media(root, load_json(args.items))
    else:
        result = push(root)
    print(json.dumps(result, ensure_ascii=False, indent=1, default=str))


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ns_console
    ns_console.utf8()
    try:
        main()
    except (ValueError, OSError, RuntimeError, KeyError) as exc:
        sys.exit(f'{type(exc).__name__}: {exc}')
