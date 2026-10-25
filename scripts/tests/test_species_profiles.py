"""Species profile v3 validation, alias routing and per-species isolation on fixtures."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chayvideo_context as ctx
import species_profiles as sp

REAL_ROOT = Path(__file__).resolve().parents[2]


def profile(slug, sid, scientific, names, extra='', size_kind='typical', modules=None, cite='[S1, S2]'):
    meta = dict(id=sid, slug=slug, scientific_name=scientific,
                taxonomy=dict(authority='Author, 1800', order='Order', family='Family', checked_with='S1'),
                common_names=dict(en=names), group='fish', stages=['adult'], look_alikes=[],
                modules=modules or {}, status='researched', version='3.0', updated='2026-10-25',
                review_due='2099-01-01', sources_file=f'01-Knowledge/sources/species/{slug}.md')
    body = '\n\n'.join([
        f'# {names[0]}', '```json\n' + json.dumps(meta) + '\n```',
        f'## 1. Nhận dạng\n\nDấu nhận dạng {cite}',
        f'## 2. Kích cỡ và giai đoạn\n\n| Thông số | Giá trị | Đơn vị | Phạm vi | Loại | Nguồn |\n|---|---|---|---|---|---|\n| TL | 50 | cm | adult | {size_kind} | S2 |',
        '## 3. Sinh cảnh và phân bố\n\nx', '## 4. Hành vi\n\n| Tháng | Vùng | Hành vi | Nguồn |\n|---|---|---|---|\n| T10 | US | spawn | S1 |', '## 5. Tương tác\n\nx',
        '## 6. Điểm đáng xem\n\nx', '## 7. Checklist hình ảnh\n\n- a\n- b\n- c',
        '## 8. Chưa biết và giới hạn\n\nx' + extra])
    return body


def ledger(sid, tiers=('A', 'B')):
    sources = [dict(id=f'S{i+1}', tier=t, title='t', publisher='p', url='https://example.org/', published=None,
                    accessed='2026-10-25', access='opened', supports='facts', limits='') for i, t in enumerate(tiers)]
    return '# Sổ nguồn\n\n```json\n' + json.dumps(dict(species_id=sid, sources=sources)) + '\n```\n'


class SpeciesProfileTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.write('01-Knowledge/species/alpha.md', profile('alpha', 'K-SP-ALPHA-001', 'Alpha one', ['alpha fish', 'red drum']))
        self.write('01-Knowledge/sources/species/alpha.md', ledger('K-SP-ALPHA-001'))
        self.write('01-Knowledge/species/beta.md', profile('beta', 'K-SP-BETA-001', 'Beta two', ['beta fish'],
                                                           modules={'angling': '01-Knowledge/equipment/species/beta-angling.md'}))
        self.write('01-Knowledge/sources/species/beta.md', ledger('K-SP-BETA-001'))
        self.write('01-Knowledge/equipment/species/beta-angling.md', 'beta tackle')
        self.write('01-Knowledge/species/INDEX.md', sp.render_index(self.root))

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def test_valid_library_passes(self):
        result = sp.validate(self.root)
        self.assertTrue(result['ok'], result['errors'])
        self.assertEqual(result['profiles'], 2)

    def test_alias_resolution_folds_case_diacritics_and_separators(self):
        self.assertEqual(sp.resolve(self.root, 'Red-Drum')['slug'], 'alpha')
        self.assertEqual(sp.resolve(self.root, 'alpha one')['id'], 'K-SP-ALPHA-001')
        self.assertIsNone(sp.resolve(self.root, 'gamma'))
        self.assertEqual(sp.normalize('Cá Đù Đỏ'), 'ca du do')

    def test_duplicate_alias_and_stale_index_fail(self):
        self.write('01-Knowledge/species/beta.md', profile('beta', 'K-SP-BETA-001', 'Beta two', ['beta fish', 'RED DRUM']))
        errors = sp.validate(self.root)['errors']
        self.assertTrue(any('alias' in e for e in errors))
        self.assertTrue(any('INDEX.md is stale' in e for e in errors))

    def test_unknown_citation_bad_size_kind_and_missing_ab_source(self):
        self.write('01-Knowledge/species/alpha.md', profile('alpha', 'K-SP-ALPHA-001', 'Alpha one', ['alpha fish'],
                                                            size_kind='huge', cite='[S9]'))
        self.write('01-Knowledge/sources/species/alpha.md', ledger('K-SP-ALPHA-001', tiers=('E', 'E')))
        errors = ' '.join(sp.validate(self.root, 'alpha')['errors'])
        for text in ('unknown source S9', "size kind 'huge'", 'A/B-tier', 'A-tier source ids'):
            self.assertIn(text, errors)

    def test_section_returns_only_requested_parts(self):
        found = sp.sections(self.root, 'red drum', [1, 7])
        self.assertIn('## 1. Nhận dạng', found['text'])
        self.assertIn('## 7. Checklist hình ảnh', found['text'])
        self.assertNotIn('## 4. Hành vi', found['text'])
        with self.assertRaises(ValueError):
            sp.sections(self.root, 'red drum', [9])

    def test_not_accessed_source_cannot_claim_date(self):
        data = sp.json_block(ledger('K-SP-ALPHA-001'))
        data['sources'][1]['access'] = 'not_accessed'
        self.write('01-Knowledge/sources/species/alpha.md', '```json\n' + json.dumps(data) + '\n```')
        self.assertTrue(any('not_accessed' in e for e in sp.validate(self.root, 'alpha')['errors']))

    def test_scaffold_refuses_existing_and_creates_draft(self):
        templates = REAL_ROOT / '00-Standards/templates'
        for name in ('species-profile.md', 'species-sources.md'):
            self.write('00-Standards/templates/' + name, (templates / name).read_text(encoding='utf-8'))
        with self.assertRaises(ValueError):
            sp.scaffold(self.root, 'alpha', 'K-SP-NEW-001', 'New one', 'New', 'fish')
        made = sp.scaffold(self.root, 'deer', 'K-SP-WHITETAIL-001', 'Odocoileus virginianus', 'White-tailed deer', 'mammal')
        meta = sp.metadata(self.root, made['profile'])
        self.assertEqual((meta['status'], meta['group'], meta['slug']), ('draft', 'mammal', 'deer'))

    def test_snapshot_marks_new_unchanged_changed_and_errors(self):
        pages = {'v': b'<html><script>x=1</script><p>Fact A</p></html>'}
        first = sp.snapshot(self.root, 'alpha', fetch=lambda url: pages['v'])
        self.assertEqual({r['status'] for r in first['sources']}, {'new'})
        pages['v'] = b'<html><script>x=2</script><p>Fact A</p></html>'
        self.assertEqual({r['status'] for r in sp.snapshot(self.root, 'alpha', fetch=lambda url: pages['v'])['sources']}, {'unchanged'})
        pages['v'] = b'<p>Fact B</p>'
        self.assertEqual({r['status'] for r in sp.snapshot(self.root, 'alpha', fetch=lambda url: pages['v'])['sources']}, {'changed'})
        def fail(url):
            raise OSError('offline')
        self.assertEqual({r['status'] for r in sp.snapshot(self.root, 'alpha', fetch=fail)['sources']}, {'fetch_error'})


def png(width, height):
    return b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\rIHDR' + width.to_bytes(4, 'big') + height.to_bytes(4, 'big') + b'\x08\x02\x00\x00\x00'


def jpeg(width, height):
    return (b'\xff\xd8\xff\xe0\x00\x04ab' + b'\xff\xc0\x00\x11\x08' + height.to_bytes(2, 'big')
            + width.to_bytes(2, 'big') + b'\x03' + b'\x00' * 9 + b'\xff\xd9')


class PhotoManifestTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        target = self.root / '01-Knowledge/species/alpha.md'
        target.parent.mkdir(parents=True)
        target.write_text(profile('alpha', 'K-SP-ALPHA-001', 'Alpha one', ['alpha fish']), encoding='utf-8')
        ledger_path = self.root / '01-Knowledge/sources/species/alpha.md'
        ledger_path.parent.mkdir(parents=True)
        ledger_path.write_text(ledger('K-SP-ALPHA-001'), encoding='utf-8')
        (self.root / '01-Knowledge/species/INDEX.md').write_text(sp.render_index(self.root), encoding='utf-8')
        self.raw = png(2000, 1200)

    def manifest(self, **change):
        import hashlib
        item = dict(asset_id='PH-ALPHA-ADULT-SIDE-01', entity_id='K-SP-ALPHA-001', stage='adult', variant=None, view='side',
                    roles=['identity'], page_url='https://commons.example/File', file_url='https://upload.example/a.png',
                    license='CC BY-SA 4.0', credit='Someone', sha256=hashlib.sha256(self.raw).hexdigest(), width=2000,
                    height=1200, subject_coverage='medium', quality='1080p', observed='o', species_basis='b', use='u',
                    reviewed='2026-10-25')
        item.update(change)
        path = self.root / sp.PHOTO_MANIFEST
        path.write_text(json.dumps(dict(schema=1, photos=[item])), encoding='utf-8')

    def test_tiers_and_measured_sizes(self):
        self.assertEqual(sp.photo_tier(1920, 1080, 'small'), '1080p')
        self.assertEqual(sp.photo_tier(1280, 720, 'large'), '720p')
        self.assertIsNone(sp.photo_tier(1280, 720, 'medium'))
        self.assertEqual(sp.photo_tier(1900, 1200, 'large'), '720p')
        self.assertEqual(sp.image_size(png(2000, 1200)), (2000, 1200))
        self.assertEqual(sp.image_size(jpeg(3000, 2000)), (3000, 2000))

    def test_manifest_covers_stage_and_rejects_low_quality_or_bad_license(self):
        self.manifest()
        result = sp.validate(self.root)
        self.assertTrue(result['ok'], result['errors'])
        self.assertFalse(any('no real identity photo' in w for w in result['warnings']))
        self.manifest(width=1280, height=720, quality='720p')
        self.assertTrue(any('tier None' in e for e in sp.validate(self.root)['errors']))
        self.manifest(license='All rights reserved')
        self.assertTrue(any('license' in e for e in sp.validate(self.root)['errors']))

    def test_fetch_verifies_hash_and_size_then_registers_privately(self):
        import asset_catalog
        self.manifest()
        first = sp.photos_fetch(self.root, fetch=lambda url: self.raw)
        self.assertEqual(first['photos'][0]['status'], 'registered')
        with asset_catalog.connection(self.root) as db:
            body = json.loads(db.execute('SELECT body FROM assets').fetchone()[0])
        self.assertEqual((body['origin'], body['publication']['visibility'], body['quality']['tier']), ('photo', 'private', '1080p'))
        bad = sp.photos_fetch(self.root, fetch=lambda url: png(10, 10))
        self.assertIn(bad['photos'][0]['status'], ('unchanged', 'updated'))
        (self.root / sp.PHOTO_STORE / 'PH-ALPHA-ADULT-SIDE-01.png').unlink()
        self.assertEqual(sp.photos_fetch(self.root, fetch=lambda url: png(10, 10))['photos'][0]['status'], 'error')


class SpeciesRoutingTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        for name in ['VERSION', 'START-HERE.md', 'SYSTEM.md', 'AGENTS.md', '.agents/skills/na-chayvideo/SKILL.md',
                     '.agents/skills/na-chayvideo/references/workflow.md', '00-Standards/video-prompt-workflow.md',
                     *[f'.agents/skills/na-chayvideo/references/{m}.md' for m in ('new', 'revision', 'caption', 'reference')],
                     'new.md', 'tackle.md']:
            self.write(name, 'fixture')
        self.write('03-Projects/one/PROJECT.md', 'ID: stable-one\nSlug: one\nRouting: fish project\n')
        self.write('01-Knowledge/species/alpha.md', profile('alpha', 'K-SP-ALPHA-001', 'Alpha one', ['red drum']))
        self.write('01-Knowledge/species/beta.md', profile('beta', 'K-SP-BETA-001', 'Beta two', ['beta fish'],
                                                           modules={'angling': '01-Knowledge/equipment/species/beta-angling.md'}))
        self.write('01-Knowledge/equipment/species/beta-angling.md', 'beta tackle')
        self.write('03-Projects/one/context-map.json', json.dumps(dict(
            common=['03-Projects/one/PROJECT.md'], new=['new.md'], angling=['tackle.md'],
            species={'alpha': '01-Knowledge/species/alpha.md', 'beta': '01-Knowledge/species/beta.md'})))

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def paths(self, names, interaction):
        packet = ctx.packet(self.root, 'one', 'new', names, interaction)
        self.assertEqual(ctx.verify(self.root, packet), [])
        return {s['path'] for s in packet['sources']}, packet['pending']

    def test_alias_loads_only_that_profile(self):
        paths, pending = self.paths(['Red Drum'], 'natural')
        self.assertIn('01-Knowledge/species/alpha.md', paths)
        self.assertNotIn('01-Knowledge/species/beta.md', paths)
        self.assertFalse(any('Research exact species' in p for p in pending))

    def test_angling_module_only_for_angling_and_own_species(self):
        natural, _ = self.paths(['beta fish'], 'natural')
        self.assertNotIn('01-Knowledge/equipment/species/beta-angling.md', natural)
        angling, _ = self.paths(['beta'], 'angling')
        self.assertIn('01-Knowledge/equipment/species/beta-angling.md', angling)
        alpha, _ = self.paths(['alpha'], 'angling')
        self.assertNotIn('01-Knowledge/equipment/species/beta-angling.md', alpha)

    def test_profile_not_granted_by_project_stays_pending(self):
        self.write('03-Projects/one/context-map.json', json.dumps(dict(
            common=['03-Projects/one/PROJECT.md'], new=['new.md'], species={'beta': '01-Knowledge/species/beta.md'})))
        paths, pending = self.paths(['red drum'], 'natural')
        self.assertNotIn('01-Knowledge/species/alpha.md', paths)
        self.assertTrue(any('Research exact species' in p for p in pending))


class RealLibraryTests(unittest.TestCase):
    def test_workspace_profiles_validate(self):
        result = sp.validate(REAL_ROOT)
        self.assertTrue(result['ok'], result['errors'])


if __name__ == '__main__':
    unittest.main()
