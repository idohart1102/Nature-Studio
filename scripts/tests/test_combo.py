import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import combo_sheet as cs  # noqa: E402
import combo  # noqa: E402
import validate_memory  # noqa: E402


class FakeDrive:
    """Stands in for rclone: keeps the 'uploaded' sheet as a local xlsx."""
    def __init__(self, store):
        self.store = store

    def upload_sheet(self, local, name):
        Path(self.store).write_bytes(Path(local).read_bytes())

    def download_sheet(self, name, dest):
        Path(dest).write_bytes(Path(self.store).read_bytes())

    def list(self):
        return [dict(Name='Combo.xlsx', ID='SHEET-1')]


class ComboTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = root = Path(temp.name)
        (root / '03-Projects/underwater').mkdir(parents=True)
        (root / '03-Projects/underwater/PROJECT.md').write_text('# U\n\nID: under-fishing-us\nSlug: underwater\n')
        memory = root / '05-Memory'
        for ns in ('projects/underwater', 'shared'):
            for d in ('active', 'candidates', 'retired'):
                (memory / ns / d).mkdir(parents=True)
            (memory / ns / 'INDEX.md').write_text('# Index\n')
        (memory / 'INDEX.md').write_text('[p](projects/underwater/INDEX.md) [s](shared/INDEX.md)\n')
        (root / 'evidence.md').write_text('evidence')
        prod = root / '04-Productions/underwater/UW-0001/A01'
        prod.mkdir(parents=True)
        (prod / 'OUTPUT.json').write_text(json.dumps(dict(
            idea='Ý tưởng', first_frame_prompt='ff', video_prompt='vp', checks=dict(hook_signal=1.5, key_onset=5.5),
            caption_variants=dict(schema=1, variants=dict(standard=dict(caption='Cap #A #B #C', caption_vi='vi', hook_text='h', hook_vi='hv'))))))
        combo.save_json(combo.state(root, 'config.json'), dict(
            project='underwater', prefix='UW', remote='r', folder_id='F', sheet_name='Combo', page_size=50, lessons_tab='Bài học'))
        self.store = root / 'drive.xlsx'
        patcher = mock.patch.object(combo, 'drive', lambda cfg: FakeDrive(self.store))
        patcher.start(); self.addCleanup(patcher.stop)

    def spec(self, **kw):
        base = dict(kind='procedural', action='Ghi rõ hình học móc tròn từ lượt đầu', tasks=['image-generation'],
                    evidence=['evidence.md'], summary='Móc tròn', type='Ràng buộc', group='First frame/ảnh',
                    applies='QA ảnh', basis='5 lượt ra móc J')
        base.update(kw)
        return base

    def valid(self):
        result = validate_memory.validate(self.root)
        self.assertEqual(result['errors'], [])

    def test_xlsx_roundtrip_keeps_text_dropdown_and_highlight(self):
        path = self.root / 'x.xlsx'
        cs.write_xlsx(path, [dict(name='A', rows=[['Mã', 'Kết quả'], ['UW-0001', 'CHƯA ĐẠT "x" & <y>']],
                                  dropdowns=[dict(range='B2:B9', options=['Dùng', 'Bỏ'])],
                                  highlights=[dict(column='B', contains='CHƯA ĐẠT')], min_rows=8)])
        self.assertEqual(cs.read_xlsx(path)['A'][1], ['UW-0001', 'CHƯA ĐẠT "x" & <y>'])
        import zipfile
        sheet = zipfile.ZipFile(path).read('xl/worksheets/sheet1.xml').decode()
        self.assertIn('dataValidation', sheet)
        self.assertIn('A2:B9', sheet)

    def test_new_lesson_and_user_approval_pass_memory_validator(self):
        created = combo.new_lesson(self.root, 'underwater', self.spec())
        self.valid()
        lesson = combo.lessons(self.root, 'underwater')[0]
        receipt = combo.state(self.root, 'approvals', 'r.json'); receipt.write_text('{}')
        combo.set_status(self.root, lesson, 'Đã duyệt', by='user', authority=str(receipt.relative_to(self.root)))
        self.assertTrue((self.root / '05-Memory/projects/underwater/active' / (created['id'] + '.md')).is_file())
        self.valid()
        combo.set_status(self.root, lesson, 'Không duyệt', by='user', authority=str(receipt.relative_to(self.root)))
        self.assertEqual(combo.sheet_status(lesson['meta']), 'Không duyệt')
        self.valid()

    def test_windows_style_authority_is_stored_with_forward_slashes(self):
        combo.new_lesson(self.root, 'underwater', self.spec())
        lesson = combo.lessons(self.root, 'underwater')[0]
        receipt = combo.state(self.root, 'approvals', 'w.json'); receipt.write_text('{}')
        windows = str(receipt.relative_to(self.root)).replace('/', '\\')
        combo.set_status(self.root, lesson, 'Đã duyệt', by='user', authority=windows)
        self.assertNotIn('\\', lesson['meta']['activation']['authority'])
        self.valid()

    def test_ai_cannot_mark_approved_without_objective_activation(self):
        combo.new_lesson(self.root, 'underwater', self.spec())
        lesson = combo.lessons(self.root, 'underwater')[0]
        with self.assertRaises(ValueError):
            combo.set_status(self.root, lesson, 'Đã duyệt', by='ai')

    def test_creative_lessons_never_auto_approved(self):
        with self.assertRaises(ValueError):
            combo.new_lesson(self.root, 'underwater', self.spec(type='Định hướng sáng tạo', status='active',
                                                                 activation=dict(method='automatic', date='2026-10-25', authority='x')))

    def test_confirm_increments_instead_of_duplicating(self):
        combo.new_lesson(self.root, 'underwater', self.spec())
        lesson = combo.lessons(self.root, 'underwater')[0]
        combo.confirm_lesson(self.root, lesson, source='UW-0009')
        again = combo.lessons(self.root, 'underwater')
        self.assertEqual(len(again), 1)
        self.assertEqual(again[0]['meta']['sheet']['confirmations'], 2)
        self.valid()

    def test_push_then_pull_detects_only_user_edits(self):
        combo.new_lesson(self.root, 'underwater', self.spec())
        result = combo.push(self.root)
        self.assertEqual(result['tabs'], ['UW-0001 – UW-0050', 'Bài học'])
        tabs = cs.read_xlsx(self.store)
        self.assertEqual(tabs['UW-0001 – UW-0050'][1][0], 'UW-0001')
        lessons_tab = tabs['Bài học']
        status_i = lessons_tab[0].index('Trạng thái')
        lessons_tab[1][status_i] = 'Đã duyệt'
        lessons_tab.append(['', 'Định hướng sáng tạo', 'Ý tưởng', '', 'Bài mới của người dùng'])
        sheets = [dict(name=n, rows=r) for n, r in tabs.items()]
        cs.write_xlsx(self.store, sheets)
        pulled = combo.pull(self.root)
        self.assertEqual([c['changes'].keys() for c in pulled['lesson_changes']][0], {'status'})
        self.assertEqual(pulled['new_lessons'][0]['action'], 'Bài mới của người dùng')
        combo.apply_user(self.root, pulled)
        self.assertEqual(combo.lessons(self.root, 'underwater')[0]['meta']['status'], 'active')
        self.valid()

    def test_failed_row_marked_for_red_highlight(self):
        combo.write_row(self.root, 'UW-0001', dict(qa_image='CHƯA ĐẠT (5/5)'), 'underwater', 'UW')
        row = combo.build_row(self.root, self.root / '04-Productions/underwater/UW-0001', {})
        self.assertEqual(row['qa_overall'], 'CHƯA ĐẠT')
        self.assertEqual(row['cap_standard'], 'Cap #A #B #C')


if __name__ == '__main__':
    unittest.main()
