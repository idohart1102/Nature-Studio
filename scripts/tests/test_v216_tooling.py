"""v2.1.6 tooling: fewer round-trips without weaker gates. Disposable fixtures only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chayvideo_context as ctx
import chayvideo_output as out
import context_routing as routing

SCRIPTS = Path(__file__).resolve().parents[1]


class Fixture(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        for name in ['VERSION', 'START-HERE.md', 'SYSTEM.md', 'AGENTS.md',
                     '.agents/skills/na-chayvideo/SKILL.md', '.agents/skills/na-chayvideo/references/workflow.md',
                     '00-Standards/video-prompt-workflow.md', 'scripts/asset_catalog.py',
                     *[f'.agents/skills/na-chayvideo/references/{m}.md' for m in ('new', 'revision', 'caption', 'reference')]]:
            self.write(name, 'fixture')
        self.write('00-Standards/memory-taxonomy.json', (ctx.ROOT / '00-Standards/memory-taxonomy.json').read_text(encoding='utf-8'))
        self.write('03-Projects/one/PROJECT.md', 'ID: stable-one\nSlug: one\nRouting: cá nước ngọt\n')
        self.long = '# Đầu\n' + 'Dòng nguyên văn có dấu.\n' * 40 + '## Phần hai\n' + 'Câu tiếp theo.\n' * 40
        self.write('long.md', self.long)
        self.write('short.md', '# Ngắn\nMột luật.\n')
        self.write('03-Projects/one/context-map.json', json.dumps(dict(
            common=['03-Projects/one/PROJECT.md'], new=['long.md', 'short.md'], revision=['short.md'],
            caption=['short.md'], species={}, angling=[])))

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def run_cli(self, script, *args, env=None):
        return subprocess.run([sys.executable, str(SCRIPTS / script), '--root', str(self.root), *args],
                              capture_output=True, env=env)


class ContextTooling(Fixture):
    def test_context_map_is_dependency_not_reading_material(self):
        packet = ctx.packet(self.root, 'one', 'new', [], 'natural')
        self.assertNotIn('03-Projects/one/context-map.json', {s['path'] for s in packet['sources']})
        deps = {d['path'] for d in packet['dependencies']}
        self.assertTrue({'03-Projects/one/context-map.json', 'scripts/asset_catalog.py'} <= deps)
        self.assertFalse(ctx.verify(self.root, packet))
        self.write('03-Projects/one/context-map.json', json.dumps(dict(
            common=['03-Projects/one/PROJECT.md'], new=['short.md'], revision=['short.md'], caption=['short.md'])))
        self.assertTrue(ctx.verify(self.root, packet))

    def test_pages_rejoin_exactly_and_prefer_headings(self):
        parts = routing.pages(self.long, 700)
        self.assertGreater(len(parts), 1)
        self.assertEqual(''.join(parts), self.long)
        self.assertTrue(all(len(p) <= 700 for p in parts))
        self.assertTrue(any(p.startswith('## Phần hai') for p in parts))
        self.assertEqual(routing.pages('x' * 50, 7)[0], 'x' * 7)

    def test_paged_source_counts_only_after_every_page(self):
        packet = ctx.packet(self.root, 'one', 'new', [], 'natural')
        seen, shown = [], ''
        for _ in range(20):
            body, receipt = routing.render(packet, self.root, 'ctx-a', seen, bool(seen), max_chars=700, page_large=True)
            shown += body
            if 'long.md' not in {s['path'] for s in receipt['sources']}:
                self.assertFalse(ctx.coverage(self.root, [packet], [receipt], 'ctx-a', True)['complete'])
            seen = [receipt]
            if not receipt['remaining_sources']:
                break
        self.assertIn('PAGE 1/', shown)
        self.assertNotIn('partial_sources', receipt)
        self.assertTrue(ctx.coverage(self.root, [packet], [receipt], 'ctx-a', True)['complete'])

    def test_ledger_is_per_context_and_needs_retention(self):
        packet_path = '.nature-studio/context/p.json'
        self.write(packet_path, json.dumps(ctx.packet(self.root, 'one', 'new', [], 'natural')))
        made = json.loads(self.run_cli('chayvideo_context.py', 'context-id').stdout)
        args = ['view', packet_path, '--context-id', made['context_id'], '--ledger', made['ledger'], '--max-chars', '50']
        first = self.run_cli('chayvideo_context.py', *args)
        self.assertEqual(first.returncode, 0, first.stdout)
        self.assertTrue((self.root / made['ledger']).is_file())
        refused = self.run_cli('chayvideo_context.py', *args)
        self.assertEqual(refused.returncode, 1)
        second = self.run_cli('chayvideo_context.py', *args, '--retained')
        self.assertEqual(second.returncode, 0)
        wrong = self.run_cli('chayvideo_context.py', 'view', packet_path, '--context-id', 'ctx-other',
                             '--ledger', made['ledger'])
        self.assertIn(b'named <context-id>.json', wrong.stdout)

    def test_preflight_returns_paths_and_counts_only(self):
        result = ctx.preflight(self.root, 'one', 'new', [], 'natural')
        self.assertTrue((self.root / result['packet']).is_file())
        self.assertEqual(result['source_count'], 3)
        self.assertNotIn('Dòng nguyên văn', json.dumps(result, ensure_ascii=False))
        self.assertIn('--ledger', result['next'])
        self.assertEqual(result['history']['productions'], 0)

    def test_fingerprint_from_history_still_rejects_later_edits(self):
        self.write('04-Productions/one/UF-0001/concept.md', 'prey turns away')
        ctx.history(self.root, 'one')
        data = {k: 'causal detail ' + k for k in ctx.FINGERPRINT_FIELDS}
        ctx.fingerprint(self.root, 'one', 'UF-0001', data, from_history=True)
        self.assertIsNotNone(ctx.history(self.root, 'one')['records'][0]['fingerprint'])
        ctx.history(self.root, 'one')
        self.write('04-Productions/one/UF-0001/feedback.md', 'new note after history')
        with self.assertRaises(ValueError):
            ctx.fingerprint(self.root, 'one', 'UF-0001', data, from_history=True)

    def test_compact_history_uses_production_relative_paths(self):
        self.write('04-Productions/one/UF-0001/A01/review.md', 'turn')
        compact = ctx.compact_history(ctx.history(self.root, 'one', 'turn'))
        self.assertEqual(compact['records'][0]['needs_read'], ['A01/review.md'])
        self.assertNotIn('source_hashes', json.dumps(compact))

    def test_cli_survives_cp1252_console(self):
        env = dict(os.environ, PYTHONIOENCODING='cp1252')
        result = self.run_cli('chayvideo_context.py', 'projects', env=env)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('cá nước ngọt', result.stdout.decode('utf-8'))


class OutputTooling(Fixture):
    def setUp(self):
        super().setUp()
        self.base = self.root / '04-Productions/one/UF-0001'
        self.base.mkdir(parents=True)
        for rel, text in [('00-Standards/first-frame.md', 'Frame criteria.'),
                          ('00-Standards/quality-review.md', 'Review policy.'),
                          ('03-Projects/one/first-frame-qa.md', 'Project frame criteria.')]:
            self.write(rel, text)
        self.docs = {'INPUTS.md': 'Fixture.', 'settings.md': 'Prompt only.', 'review.md': 'Syntax only.'}
        state = dict(subjects='One fish.', environment='Clear lake.', composition='Handheld low view.',
                     initial_state='Fish away from lure.')
        self.a = out.save(self.root, 'one', 'UF-0001', dict(
            idea='Ý tưởng', first_frame_prompt='Fish near lure.', video_prompt='Fish misses.',
            caption='Watch. #Fish #Lake #Fishing', frame_state=state, files=self.docs)).relative_to(self.base).as_posix()

    def test_from_resolve_fills_base_and_rejects_mismatch(self):
        resolved = out.resolve(self.root, 'one', 'UF-0001', self.a)
        data = out.with_resolved_base(self.root, 'one', 'UF-0001', resolved, dict(caption='New. #Fish #Lake #Bass'))
        self.assertEqual(data['base_sha256'], resolved['attempt_sha256'])
        with self.assertRaises(ValueError):
            out.with_resolved_base(self.root, 'one', 'UF-0001', resolved, dict(base_sha256='0' * 64))
        with self.assertRaises(ValueError):
            out.with_resolved_base(self.root, 'two', 'UF-0001', resolved, {})

    def test_handoff_computes_hashes_matches_and_never_overwrites(self):
        attempt = self.base / 'A02'
        attempt.mkdir()
        (attempt / 'first-frame.png').write_bytes(b'fixture image bytes')
        (attempt / 'review.md').write_text('Fixture QA.', encoding='utf-8')
        result = out.handoff(self.root, 'one', 'UF-0001', self.a, 'A02', 'A02/first-frame.png', 'A02/review.md',
                             'qa_pass', 941, 1672, ['03-Projects/one/first-frame-qa.md'], promote=True)
        self.assertEqual(result['check']['status'], 'matched', result)
        self.assertTrue(result['promoted'])
        record = json.loads((self.base / 'FIRST-FRAME.json').read_text(encoding='utf-8'))
        self.assertIn('03-Projects/one/first-frame-qa.md', record['qa_sources'])
        with self.assertRaises(ValueError):
            out.handoff(self.root, 'one', 'UF-0001', self.a, 'A02', 'A02/first-frame.png', 'A02/review.md',
                        'qa_pass', 941, 1672)

    def test_promote_refuses_unpreserved_main_record(self):
        (self.base / 'FIRST-FRAME.json').write_text('{"legacy": true}', encoding='utf-8')
        attempt = self.base / 'A02'
        attempt.mkdir()
        (attempt / 'img.png').write_bytes(b'x')
        (attempt / 'review.md').write_text('QA', encoding='utf-8')
        with self.assertRaises(ValueError):
            out.handoff(self.root, 'one', 'UF-0001', self.a, 'A02', 'A02/img.png', 'A02/review.md',
                        'qa_pass', 10, 10, promote=True)
        self.assertEqual((self.base / 'FIRST-FRAME.json').read_text(encoding='utf-8'), '{"legacy": true}')

    def test_location_tag_gate(self):
        data = dict(caption='Gone. #Redfish #MosquitoLagoon #InshoreFishing')
        self.assertTrue(out.location_tag_errors(data, required=True))
        self.assertFalse(out.location_tag_errors(dict(data, checks=dict(location_none_reason='Legacy, no setting')), True))
        self.assertFalse(out.location_tag_errors(dict(data, checks=dict(location_tag='#MosquitoLagoon')), True))
        variants = dict(schema=1, variants=dict(humor=dict(caption='Nope. #Redfish #Fishing #Florida')))
        self.assertTrue(out.location_tag_errors(dict(data, caption_variants=variants,
                                                     checks=dict(location_tag='#MosquitoLagoon')), True))
        self.assertFalse(out.location_tag_errors(data, required=False))


if __name__ == '__main__':
    unittest.main()
