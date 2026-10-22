"""Plan 01 invariants on isolated fixtures; never reserve/edit real productions."""
from concurrent.futures import ThreadPoolExecutor
import copy
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chayvideo_context as ctx
import chayvideo_output as output


class ContextTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        for name in ['VERSION', 'START-HERE.md', 'SYSTEM.md', 'AGENTS.md',
                     '.agents/skills/na-chayvideo/SKILL.md',
                     '.agents/skills/na-chayvideo/references/workflow.md',
                     '00-Standards/video-prompt-workflow.md',
                     *[f'.agents/skills/na-chayvideo/references/{m}.md' for m in ('new','revision','caption','reference')],
                     '00-Standards/reference-video-adaptation.md',
                     '.agents/skills/na-clonevideo/SKILL.md',
                     '.agents/skills/na-clonevideo/references/analysis.md',
                     '.agents/skills/na-clonevideo/references/schema.md',
                     'scripts/reference_video.py']:
            self.write(name, 'fixture')
        self.write('03-Projects/one/PROJECT.md', 'ID: stable-one\nSlug: one\nRouting: fish project\n')
        self.write('03-Projects/two/PROJECT.md', 'ID: stable-two\n')
        self.recipe = dict(common=['03-Projects/one/PROJECT.md'],
                           new=['new.md'], revision=['revision.md'], caption=['caption.md'],
                           species={'muskie':'muskie.md'}, angling=['tackle.md'])
        self.write('03-Projects/one/context-map.json', json.dumps(self.recipe))
        for name in ('new','revision','caption','muskie','tackle'):
            self.write(name+'.md', name)

    def write(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return p

    def test_catalog_uses_all_projects_and_flags_missing_metadata(self):
        rows = ctx.catalog(self.root)
        self.assertEqual(len(rows), 2)
        self.assertFalse(rows[0]['needs_full_read'])
        self.assertTrue(rows[1]['needs_full_read'])

    def test_caption_excludes_story_tackle_and_species(self):
        packet = ctx.packet(self.root, 'one', 'caption', ['muskie'])
        paths = {x['path'] for x in packet['sources']}
        self.assertIn('caption.md', paths)
        self.assertTrue(paths.isdisjoint({'new.md','muskie.md','tackle.md'}))

    def test_generic_project_does_not_require_species_even_with_optional_profiles(self):
        for mode in ('new', 'revision', 'reference'):
            result = ctx.packet(self.root, 'one', mode, [], 'natural')
            self.assertEqual(result['pending'], [])
            self.assertNotIn('tackle.md', [x['path'] for x in result['sources']])

    def test_underwater_still_requires_species_or_granted_choice(self):
        self.write('03-Projects/underwater/PROJECT.md', 'ID: under-fishing-us\nSlug: underwater\n')
        recipe = {**self.recipe, 'common': ['03-Projects/underwater/PROJECT.md']}
        self.write('03-Projects/underwater/context-map.json', json.dumps(recipe))
        result = ctx.packet(self.root, 'underwater', 'new', [], 'natural')
        self.assertTrue(any('Resolve species' in x for x in result['pending']))

    def test_unknown_species_requires_research_not_muskie(self):
        packet = ctx.packet(self.root, 'one', 'new', ['channel catfish'], 'natural')
        self.assertTrue(packet['pending'])
        self.assertNotIn('muskie.md', [x['path'] for x in packet['sources']])
        self.assertNotIn('tackle.md', [x['path'] for x in packet['sources']])

    def test_multiple_species_and_unspecified_interaction(self):
        p = ctx.packet(self.root, 'one', 'new', ['muskie','bass'])
        self.assertIn('muskie.md', [x['path'] for x in p['sources']])
        self.assertIn('tackle.md', [x['path'] for x in p['sources']])
        self.assertTrue(any('bass' in x for x in p['pending']))

    def test_freshness_detects_same_length_content(self):
        p = ctx.packet(self.root, 'one', 'caption')
        self.write('caption.md', 'CAPTION')
        self.assertIn('caption.md', ctx.verify(self.root, p))

    def test_freshness_includes_dispatcher(self):
        p = ctx.packet(self.root, 'one', 'caption')
        self.write('.agents/skills/na-chayvideo/SKILL.md','changed')
        self.assertIn('.agents/skills/na-chayvideo/SKILL.md', ctx.verify(self.root, p))

    def test_active_discovery_ignores_candidates(self):
        self.write('05-Memory/projects/one/candidates/L-a.md','candidate')
        p = ctx.packet(self.root, 'one', 'caption')
        self.write('05-Memory/shared/active/L-b.md','invalid legacy body must surface an error')
        self.assertIn('memory_inventory', ctx.verify(self.root,p))
        updated = ctx.packet(self.root, 'one', 'caption')
        self.assertTrue(updated['memory']['errors'])
        self.assertFalse(updated['memory']['candidates'])
        self.assertNotIn('05-Memory/shared/active/L-b.md', [x['path'] for x in updated['sources']])

    def test_missing_source_fails_instead_of_silent_omission(self):
        (self.root/'new.md').unlink()
        with self.assertRaises(FileNotFoundError):
            ctx.packet(self.root, 'one', 'new')

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            ctx.inside(self.root, '../outside')
        with self.assertRaises(ValueError):
            ctx.packet(self.root, '../one', 'new')

    def test_history_new_deleted_and_legacy_without_concept(self):
        path = self.write('04-Productions/one/UF-0001/A01/video-prompt.md','turn caused a miss')
        a = ctx.history(self.root,'one','turn')
        self.assertEqual(len(a['records']), 1)
        self.assertTrue(a['records'][0]['needs_read'])
        self.assertTrue(a['records'][0]['lexical_matches'])
        self.assertFalse(ctx.history(self.root,'one')['refreshed'])
        path.unlink()
        self.assertTrue(ctx.history(self.root,'one')['refreshed'])

    def test_capsule_matches_sources_and_expires_on_new_attempt(self):
        self.write('04-Productions/one/UF-0001/concept.md','bait turns away')
        row = ctx.history(self.root,'one')['records'][0]
        data = {k:'specific causal detail '+k for k in ctx.FINGERPRINT_FIELDS}
        data['source_hashes'] = row['source_hashes']
        ctx.fingerprint(self.root,'one','UF-0001',data)
        self.assertIsNotNone(ctx.history(self.root,'one')['records'][0]['fingerprint'])
        self.write('04-Productions/one/UF-0001/A02/review.md','new feedback')
        self.assertIsNone(ctx.history(self.root,'one')['records'][0]['fingerprint'])
        with self.assertRaises(ValueError):
            ctx.fingerprint(self.root,'one','UF-0001',data)

    def test_lexical_no_match_does_not_hide_causal_capsule(self):
        self.write('04-Productions/one/UF-0001/concept.md','different animal name')
        row = ctx.history(self.root,'one')['records'][0]
        data = {k:'direction changes force prey into cover' for k in ctx.FINGERPRINT_FIELDS}
        data['source_hashes'] = row['source_hashes']
        ctx.fingerprint(self.root,'one','UF-0001',data)
        rows = ctx.history(self.root,'one','muskie')['records']
        self.assertEqual(len(rows),1)
        self.assertFalse(rows[0]['lexical_matches'])
        self.assertIsNotNone(rows[0]['fingerprint'])

    def test_corrupt_derived_cache_rebuilt(self):
        self.write('.nature-studio/history/one.json','broken json')
        self.assertTrue(ctx.history(self.root,'one')['refreshed'])

    def test_ledger_only_history_is_retained_without_id_allocation(self):
        self.write('03-Projects/one/idea-ledger.md','Rejected draft: a prey reverses behind cover')
        result=ctx.history(self.root,'one')
        self.assertIn('Rejected draft',result['ledger']['text'])
        self.assertFalse((self.root/'.nature-studio/video-ids.sqlite3').exists())

    def test_wrong_type_capsule_falls_back_to_sources(self):
        self.write('04-Productions/one/UF-0001/concept.md','story')
        self.write('04-Productions/one/UF-0001/HISTORY-FINGERPRINT.json','[]')
        row=ctx.history(self.root,'one')['records'][0]
        self.assertIsNone(row['fingerprint'])
        self.assertTrue(row['needs_read'])

    def test_reference_inherits_new_recipe_and_later_source_changes(self):
        self.recipe['reference']='new'
        self.write('03-Projects/one/context-map.json',json.dumps(self.recipe))
        old=ctx.packet(self.root,'one','reference',['muskie'])
        self.assertIn('new.md',[x['path'] for x in old['sources']])
        self.write('new.md','updated requirement shared by both modes')
        self.assertIn('new.md',ctx.verify(self.root,old))
        for mode in ('new','reference'):
            updated=ctx.packet(self.root,'one',mode,['muskie'])
            self.assertTrue(any('updated requirement' in x['text'] for x in updated['sources']))

    def test_reference_fallback_and_core_freshness(self):
        p=ctx.packet(self.root,'one','reference',['bass'])
        self.write('00-Standards/video-prompt-workflow.md','changed shared core')
        self.assertIn('00-Standards/video-prompt-workflow.md',ctx.verify(self.root,p))

    def test_alias_cycle_does_not_loop(self):
        self.recipe.update(reference='new',new='reference')
        self.write('03-Projects/one/context-map.json',json.dumps(self.recipe))
        with self.assertRaises(ValueError):
            ctx.packet(self.root,'one','reference')


class OutputTests(unittest.TestCase):
    def good(self):
        return dict(idea='Ý tưởng', first_frame_prompt='A real initial frame.',
                    video_prompt='One continuous handheld underwater shot. [0.0–1.2s] Setup; [1.2–3.1s] Track; '
                                 '[3.1–5.6s] React; [5.6–6.3s] Key action; [6.3–10.0s] Aftermath.',
                    caption='Not buying it. #Muskie #MuskyFishing #WisconsinFishing',
                    checks={'key_onset':5.6,'hook_signal':1.2,'location_tag':'#WisconsinFishing'},
                    files={'INPUTS.md':'Source paths and hashes; no media generated.',
                           'settings.md':'Not executed; settings unknown.',
                           'review.md':'Prompt-only; media QA pending.'})

    def test_good_fullset(self):
        self.assertEqual(output.validate(self.good(),underwater=True),[])

    def test_reference_uses_same_output_rules_as_new(self):
        self.assertEqual(output.validate(self.good(),'reference',True),[])
        data=self.good();data['checks']['key_onset']=2
        self.assertTrue(output.validate(data,'reference',True))

    def test_early_key_gaps_and_fewer_beats_rejected(self):
        for key in [5,4.9,10,'NaN',None]:
            data=self.good(); data['checks']['key_onset']=key
            self.assertTrue(output.validate(data,underwater=True))
        data=self.good(); data['video_prompt']=data['video_prompt'].replace('[1.2','[1.3')
        self.assertTrue(output.validate(data,underwater=True))

    def test_ten_beats_allowed_eleven_rejected(self):
        bounds=['0.0','0.6','1.2','2.0','2.8','3.6','4.6','5.6','6.3','8.0','10.0']
        data=self.good();data['video_prompt']='One continuous handheld underwater shot. '+' '.join(f'[{a}–{b}s] beat' for a,b in zip(bounds,bounds[1:]))
        self.assertEqual(output.validate(data,underwater=True),[])
        bounds.insert(1,'0.3');data['video_prompt']='One continuous handheld underwater shot. '+' '.join(f'[{a}–{b}s] beat' for a,b in zip(bounds,bounds[1:]))
        self.assertTrue(any('5–10 beats' in e for e in output.validate(data,underwater=True)))

    def test_hook_signal_window_and_first_beat(self):
        for value in [0,3.01,4,'NaN',None,True]:
            with self.subTest(value=value):
                data=self.good();data['checks']['hook_signal']=value
                self.assertTrue(any('hook_signal' in e for e in output.validate(data,underwater=True)))
        data=self.good();data['checks']['hook_signal']=3
        self.assertEqual(output.validate(data,underwater=True),[])
        data=self.good();data['video_prompt']=data['video_prompt'].replace('[0.0–1.2s] Setup; [1.2–3.1s] Track; ','[0.0–3.1s] Setup and track; ')
        self.assertTrue(any('first beat' in e for e in output.validate(data,underwater=True)))
        data=self.good();del data['checks']['hook_signal']
        self.assertEqual(output.validate({'caption':data['caption']},'caption',True),[])

    def test_caption_tags_and_newlines(self):
        for caption in ['Watch. #Muskie #Muskie #Fish',
                        'Watch. #muskie #fish #UNDERwater',
                        'AI scene. #Muskie #Fishing #Lake',
                        'Watch. #Muskie\n#Fishing #Lake',
                        '#Muskie #Fishing #Lake']:
            self.assertTrue(output.validate({'caption':caption},'caption',True))

    def test_other_project_has_no_underwater_timing_or_tag_rule(self):
        data=self.good(); data['video_prompt']='A different length and format.'
        data['caption']='Watch. #Fish #Underwater #Nature'
        self.assertFalse(output.validate(data,underwater=False))

    def test_generic_caption_contract_can_allow_zero_two_tags_or_ai_disclosure(self):
        for caption in ['Clouds cross the ridge.', 'Look. #Clouds #Weather',
                        'AI-assisted visualization. #Clouds #Weather #Climate', '#Clouds #Weather']:
            with self.subTest(caption=caption):
                self.assertEqual(output.validate({'caption': caption}, 'caption', False), [])
        self.assertTrue(output.validate({'caption': 'Two\nparagraphs.'}, 'caption', False))
        self.assertTrue(output.validate({'caption': ' '}, 'caption', False))

    def test_underwater_still_rejects_zero_or_two_tags_and_ai_disclosure(self):
        for caption in ['Look.', 'Look. #Fish #Fishing',
                        'AI-assisted scene. #Fish #Fishing #Lake']:
            self.assertTrue(output.validate({'caption': caption}, 'caption', True))

    def test_check_cli_selects_project_scope_without_writing_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'caption.json'
            source.write_text(json.dumps({'caption': 'Clouds cross the ridge.'}), encoding='utf-8')
            for slug, expected in [('landscape', 0), ('underwater', 1)]:
                result = subprocess.run([sys.executable, '-X', 'utf8', str(Path(output.__file__)),
                                         '--root', str(root), 'check', str(source),
                                         '--project', slug, '--mode', 'caption'],
                                        capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertEqual(bool(json.loads(result.stdout)['errors']), bool(expected))
            self.assertEqual(list(root.iterdir()), [source])

    def test_partial_revision_is_allowed(self):
        self.assertFalse(output.validate({'first_frame_prompt':'A revised t=0.'},'revision',True))
        self.assertTrue(output.validate({},'revision',True))

    def test_caption_only_does_not_require_full_prompts(self):
        self.assertFalse(output.validate({'caption':self.good()['caption']},'caption',True))

    def test_nonobject_rejected(self):
        self.assertTrue(output.validate([]))

    def test_save_keeps_prior_attempt_and_image_quota(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            base=root/'04-Productions/underwater/UF-0001'
            (base/'A01').mkdir(parents=True)
            old=base/'A01/video-prompt.md'; old.write_text('old')
            quota=base/'.image-qa.sqlite3'; quota.write_bytes(b'quota bytes')
            with ThreadPoolExecutor(max_workers=2) as pool:
                paths=list(pool.map(lambda _:output.save(root,'underwater','UF-0001',self.good()),range(2)))
            self.assertEqual(len(set(paths)),2)
            self.assertEqual(old.read_text(),'old')
            self.assertEqual(quota.read_bytes(),b'quota bytes')
            self.assertTrue(all((p/'INPUTS.md').exists() for p in paths))

    def test_save_requires_existing_identity_and_blocks_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(ValueError):
                output.save(root,'underwater','ABC-00001',self.good())
            base=root/'04-Productions/underwater/ABC-00001'; base.mkdir(parents=True)
            with self.assertRaises(FileNotFoundError):
                output.save(root,'underwater','ABC-00001',self.good())
            project = root / '03-Projects/underwater/PROJECT.md'
            project.parent.mkdir(parents=True)
            project.write_text('ID: under-fishing-us\nSlug: underwater\n', encoding='utf-8')
            (base/'IDENTITY.json').write_text(json.dumps({'video_id':'ABC-00001'}))
            data=self.good(); data['files']['../bad.md']='bad'
            with self.assertRaises(ValueError):
                output.save(root,'underwater','ABC-00001',data)


if __name__ == '__main__':
    unittest.main()
