"""Bait library: validation, alias/variant routing, species links, compact per-species lookup and photos."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bait_profiles as bp
import chayvideo_context as ctx
import species_profiles as sp
from test_species_profiles import ledger, png, profile

REAL_ROOT = Path(__file__).resolve().parents[2]


def bait(slug, bid, kind='lure', names=('crankbait',), variants=None, legacy=(), cite='[S1]', size_variant='squarebill'):
    variants = variants or {'squarebill': {'label': 'Square-bill', 'aliases': ['square bill']},
                            'lipless': {'label': 'Lipless', 'aliases': ['rattle bait']}}
    meta = dict(id=bid, slug=slug, kind=kind, names=dict(en=list(names), vi=[]), variants=variants, species_profile=None,
                legacy_entities=list(legacy), status='researched', version='1.0', updated='2026-10-25',
                review_due='2099-01-01', sources_file=f'01-Knowledge/sources/baits/{slug}.md')
    return '\n\n'.join([
        f'# {names[0]}', '```json\n' + json.dumps(meta) + '\n```',
        f'## 1. Nhận dạng và cấu tạo\n\nLưỡi lặn {cite}',
        f'## 2. Biến thể và cỡ\n\n| Biến thể | Thông số | Giá trị | Đơn vị | Nguồn |\n|---|---|---|---|---|\n| {size_variant} | dài | 5 | cm | S1 |',
        '## 3. Chuyển động trong nước\n\nx', '## 4. Cách gắn và rig\n\nx',
        '## 5. Checklist hình ảnh\n\n- a\n- b\n- c', '## 6. Chưa biết và giới hạn\n\nx'])


def bait_ledger(bid):
    return ledger(bid).replace('"species_id"', '"bait_id"')


def module(links):
    return '# Module câu\n\n## Mồi\n\nx\n\n## Mã mồi\n\n```json\n' + json.dumps(dict(baits=links)) + '\n```\n'


class BaitLibraryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.write('01-Knowledge/species/beta.md', profile('beta', 'K-SP-BETA-001', 'Beta two', ['beta fish'],
                                                           modules={'angling': '01-Knowledge/equipment/species/beta-angling.md'}))
        self.write('01-Knowledge/sources/species/beta.md', ledger('K-SP-BETA-001'))
        self.write('01-Knowledge/equipment/species/beta-angling.md',
                   module([dict(id='EQP-LURE-CRANKBAIT', variants=['squarebill'], when='mùa thu', source='S1')]))
        self.write('01-Knowledge/equipment/baits/crankbait.md', bait('crankbait', 'EQP-LURE-CRANKBAIT', legacy=['EQP-OLD-CRANK']))
        self.write('01-Knowledge/sources/baits/crankbait.md', bait_ledger('EQP-LURE-CRANKBAIT'))
        self.write('01-Knowledge/equipment/baits/INDEX.md', bp.render_index(self.root))
        self.raw = png(1600, 900)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def manifest(self, **change):
        item = dict(asset_id='PH-LURE-CRANKBAIT-SQUAREBILL-SIDE-01', entity_id='EQP-LURE-CRANKBAIT', variant='squarebill',
                    view='side', roles=['identity'], page_url='https://example.org/p', file_url='https://example.org/f.png',
                    license='CC BY 4.0', credit='someone', sha256=hashlib.sha256(self.raw).hexdigest(), width=1600,
                    height=900, subject_coverage='medium', quality='720p', observed='square bill lip', basis='square lip',
                    use='identity only', reviewed='2026-10-25')
        item.update(change)
        self.write(bp.PHOTO_MANIFEST, json.dumps(dict(schema=1, photos=[item])))

    def test_valid_library_passes_and_warns_missing_variant_photo(self):
        result = bp.validate(self.root)
        self.assertTrue(result['ok'], result['errors'])
        self.assertEqual((result['baits'], result['linked_species']), (1, 1))
        self.assertIn('EQP-LURE-CRANKBAIT: no real identity photo for variant lipless', result['warnings'])

    def test_resolve_name_and_variant_alias(self):
        self.assertEqual(bp.resolve(self.root, 'Crankbait')['variant'], None)
        self.assertEqual(bp.resolve(self.root, 'Rattle-Bait')['variant'], 'lipless')
        self.assertIsNone(bp.resolve(self.root, 'spinnerbait'))

    def test_duplicate_alias_wrong_prefix_and_stale_index_fail(self):
        self.write('01-Knowledge/equipment/baits/rattle.md', bait('rattle', 'EQP-BAIT-RATTLE', names=('rattle bait',),
                                                                    variants={'std': {'label': 'x'}}, size_variant='std'))
        self.write('01-Knowledge/sources/baits/rattle.md', bait_ledger('EQP-BAIT-RATTLE'))
        errors = ' '.join(bp.validate(self.root)['errors'])
        for text in ('alias "rattle bait"', 'prefix EQP-LURE-', 'INDEX.md is stale'):
            self.assertIn(text, errors)

    def test_species_link_checks_id_variant_and_species_source(self):
        self.write('01-Knowledge/equipment/species/beta-angling.md', module([
            dict(id='EQP-LURE-NOPE', when='x', source='S1'),
            dict(id='EQP-LURE-CRANKBAIT', variants=['deep'], when='x', source='S9')]))
        self.write('01-Knowledge/equipment/baits/INDEX.md', bp.render_index(self.root))
        errors = ' '.join(bp.validate(self.root)['errors'])
        for text in ('unknown bait id EQP-LURE-NOPE', "unknown variants ['deep']", 'beta ledger'):
            self.assertIn(text, errors)

    def test_size_row_variant_and_citation_checked(self):
        self.write('01-Knowledge/equipment/baits/crankbait.md', bait('crankbait', 'EQP-LURE-CRANKBAIT', cite='[S7]',
                                                                     size_variant='giant'))
        errors = ' '.join(bp.validate(self.root)['errors'])
        self.assertIn('unknown source S7', errors)
        self.assertIn("variant 'giant'", errors)

    def test_photo_tier_accepts_720p_any_coverage(self):
        self.assertEqual(bp.photo_tier(1600, 900), '720p')
        self.assertEqual(bp.photo_tier(1080, 1920), '1080p')
        self.assertIsNone(bp.photo_tier(1200, 800))
        self.manifest()
        result = bp.validate(self.root)
        self.assertTrue(result['ok'], result['errors'])
        self.assertNotIn('EQP-LURE-CRANKBAIT: no real identity photo for variant squarebill', result['warnings'])
        self.manifest(width=1200, height=800)
        self.assertTrue(any('tier None' in e for e in bp.validate(self.root)['errors']))
        self.manifest(variant='deep', view='diagonal')
        errors = ' '.join(bp.validate(self.root)['errors'])
        self.assertIn('variant deep', errors)
        self.assertIn('view must be', errors)

    def test_for_species_returns_exact_requests_without_profile_text(self):
        self.manifest()
        rows = bp.for_species(self.root, 'beta fish')['baits']
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row['variants'], ['squarebill'])
        self.assertEqual(row['photos'][0]['asset_id'], 'PH-LURE-CRANKBAIT-SQUAREBILL-SIDE-01')
        self.assertEqual(row['requests']['squarebill'], dict(
            request=dict(entity_id='EQP-LURE-CRANKBAIT', role='identity', variant='squarebill'),
            assets=['PH-LURE-CRANKBAIT-SQUAREBILL-SIDE-01']))
        self.assertEqual(row['legacy_requests'], [dict(entity_id='EQP-OLD-CRANK', role='anatomy')])
        self.manifest(variant=None)
        fallback = bp.for_species(self.root, 'beta fish')['baits'][0]['requests']['squarebill']
        self.assertEqual(fallback['request'], dict(entity_id='EQP-LURE-CRANKBAIT', role='identity'))
        self.assertEqual(fallback['assets'], ['PH-LURE-CRANKBAIT-SQUAREBILL-SIDE-01'])
        self.manifest(variant='lipless', asset_id='PH-LURE-CRANKBAIT-LIPLESS-SIDE-01')
        other = bp.for_species(self.root, 'beta fish')['baits'][0]['requests']['squarebill']
        self.assertEqual(other['assets'], [], 'another variant photo must never stand in')
        self.assertNotIn('Lưỡi lặn', json.dumps(row, ensure_ascii=False))

    def test_fetch_registers_lure_as_equipment(self):
        import asset_catalog
        self.manifest()
        self.assertEqual(bp.photos_fetch(self.root, fetch=lambda url: self.raw)['photos'][0]['status'], 'registered')
        with asset_catalog.connection(self.root) as db:
            body = json.loads(db.execute('SELECT body FROM assets').fetchone()[0])
        self.assertEqual((body['kind'], body['variant'], body['publication']['visibility']), ('equipment', 'squarebill', 'private'))
        query = asset_catalog.query(self.root, [dict(entity_id='EQP-LURE-CRANKBAIT', role='identity', variant='squarebill')])
        self.assertEqual([a['asset_id'] for a in query['assets']], ['PH-LURE-CRANKBAIT-SQUAREBILL-SIDE-01'])


class BaitPacketTests(BaitLibraryTests):
    def setUp(self):
        super().setUp()
        for name in ['VERSION', 'START-HERE.md', 'SYSTEM.md', 'AGENTS.md', '.agents/skills/na-chayvideo/SKILL.md',
                     '.agents/skills/na-chayvideo/references/workflow.md', '00-Standards/video-prompt-workflow.md',
                     *[f'.agents/skills/na-chayvideo/references/{m}.md' for m in ('new', 'revision', 'caption', 'reference')],
                     'new.md']:
            self.write(name, 'fixture')
        self.write('03-Projects/one/PROJECT.md', 'ID: stable-one\nSlug: one\nRouting: fish project\n')
        self.write('03-Projects/one/context-map.json', json.dumps(dict(
            common=['03-Projects/one/PROJECT.md'], new=['new.md'], species={'beta': '01-Knowledge/species/beta.md'})))

    def test_packet_carries_compact_baits_only_for_angling(self):
        angling = ctx.packet(self.root, 'one', 'new', ['beta'], 'angling')
        self.assertEqual(ctx.verify(self.root, angling), [])
        self.assertEqual(angling['baits']['beta'][0]['id'], 'EQP-LURE-CRANKBAIT')
        self.assertNotIn('01-Knowledge/equipment/baits/crankbait.md', {s['path'] for s in angling['sources']})
        self.assertNotIn('baits', ctx.packet(self.root, 'one', 'new', ['beta'], 'natural'))


class RealBaitLibraryTests(unittest.TestCase):
    def test_workspace_baits_validate(self):
        result = bp.validate(REAL_ROOT)
        self.assertTrue(result['ok'], result['errors'])


if __name__ == '__main__':
    unittest.main()
