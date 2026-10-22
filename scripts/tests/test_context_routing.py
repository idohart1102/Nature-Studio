"""Information preservation, independent config updates and context lifecycle.

Disposable fixtures only; no writes to real production, lesson or ID registries.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chayvideo_context as ctx
import context_routing as routing


class RoutingTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        for rel in ['VERSION', 'START-HERE.md', 'SYSTEM.md', 'AGENTS.md',
                    '.agents/skills/na-chayvideo/SKILL.md',
                    '.agents/skills/na-chayvideo/references/workflow.md',
                    '00-Standards/video-prompt-workflow.md',
                    '00-Standards/context-routing.md',
                    'scripts/chayvideo_context.py', 'scripts/context_routing.py',
                    '00-Standards/reference-video-adaptation.md',
                    '.agents/skills/na-clonevideo/SKILL.md',
                    '.agents/skills/na-clonevideo/references/analysis.md',
                    '.agents/skills/na-clonevideo/references/schema.md', 'scripts/reference_video.py',
                    *['.agents/skills/na-chayvideo/references/' + m + '.md' for m in ('new', 'revision', 'caption', 'reference')]]:
            self.write(rel, 'Fixture dependency\n')
        self.write('03-Projects/one/PROJECT.md', 'ID: one\nSlug: one\nRouting: fixture\n')
        self.write('00-Standards/memory-taxonomy.json',
                   (ctx.ROOT/'00-Standards/memory-taxonomy.json').read_text(encoding='utf-8'))
        self.recipe = dict(common=['03-Projects/one/PROJECT.md'],
            new=['concept.md', 'write.md', 'quality.md', 'save.md'],
            revision=['write.md', 'quality.md', 'save.md'], caption=['caption.md'], reference='new',
            species={'muskie': 'muskie.md'}, angling=['tackle.md'],
            routing='03-Projects/one/context-routing.json')
        stage = lambda sources, tasks, dynamic=True: dict(sources=sources, tasks=tasks,
                                                       species=dynamic, angling=dynamic)
        profile = dict(stages={
            'orient': stage([], [], False),
            'concept': stage(['concept.md'], ['video-idea', 'research']),
            'write': stage(['write.md'], ['video-prompt']),
            'review': stage(['quality.md'], ['video-prompt']),
            'save': stage(['save.md'], [], False)})
        self.config = dict(schema=1, modes=dict(new=profile, reference='new',
            revision=dict(stages={k: v for k, v in profile['stages'].items() if k != 'concept'}),
            caption=dict(stages={'write': stage(['caption.md'], ['caption'], False)})),
            effects={'camera': dict(sources=['camera.md'], tasks=['first-frame-prompt'], requires=[]),
                     'video-review': dict(sources=['review.md'], tasks=['video-review'], requires=[]),
                     'audio-review': dict(sources=['audio.md'], tasks=['generated-audio-review'], requires=['video-review'])})
        for name in ['concept', 'write', 'quality', 'save', 'caption', 'muskie', 'tackle', 'camera', 'review', 'audio']:
            self.write(name+'.md', '# '+name+'\r\nĐiều kiện và ngoại lệ bắt buộc: '+name+'\r\n')
        self.sync()

    def write(self, rel, text):
        p = self.root/rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode('utf-8'))
        return p

    def sync(self):
        self.write('03-Projects/one/context-map.json', json.dumps(self.recipe))
        self.write('03-Projects/one/context-routing.json', json.dumps(self.config))

    def packet(self, stage='all', mode='new', **kw):
        return ctx.packet(self.root, 'one', mode, ['muskie'], 'angling', stage=stage, **kw)

    def view(self, packet, **kw):
        return routing.render(packet, self.root, context_id='epoch-1', **kw)

    def test_all_stages_conserve_original_source_text_and_hash(self):
        for mode in ('new', 'revision', 'caption', 'reference'):
            old = ctx.packet(self.root, 'one', mode, ['muskie'], 'angling')
            new = self.packet(mode=mode)
            self.assertEqual({s['path']: s for s in old['sources']}, {s['path']: s for s in new['sources']})
            self.assertFalse(ctx.verify(self.root, new))

    def test_stage_union_covers_whole_baseline_before_fullset(self):
        packets = [self.packet(stage=s) for s in ('concept','write','review','save')]
        offered = {s['path'] for p in packets for s in p['sources']}
        required = {s['path'] for s in self.packet()['sources']}
        self.assertEqual(offered, required)
        self.assertNotIn('write.md', {s['path'] for s in packets[0]['sources']})

    def test_reference_inherits_new_sources_but_keeps_adaptation_tasks(self):
        self.config['task_overrides']={'reference':{'concept':['reference-video-adaptation','research']}}
        self.config['modes']['new']['stages']['concept']['sources'].append('new-common.md')
        self.write('new-common.md','New source shared by independent concept and reference')
        self.sync()
        p=self.packet('concept',mode='reference')
        self.assertIn('new-common.md',{s['path'] for s in p['sources']})
        self.assertIn('reference-video-adaptation',p['memory']['request']['tasks'])
        self.assertNotIn('video-idea',p['memory']['request']['tasks'])

    def test_new_unclassified_source_cannot_disappear(self):
        self.recipe['new'].append('new-safety.md'); self.write('new-safety.md', 'Important new rule'); self.sync()
        for stage in routing.STAGES:
            p=self.packet(stage=stage)
            self.assertIn('new-safety.md',p['routing']['unassigned'])
            self.assertIn('new-safety.md',{s['path'] for s in p['sources']})

    def test_effect_dependency_closure_unions_all_real_tasks(self):
        p=self.packet('write', mode='revision', effects=['audio-review'], tasks=['caption'])
        self.assertTrue({'write.md','audio.md','review.md'} <= {s['path'] for s in p['sources']})
        self.assertTrue({'video-prompt','video-review','generated-audio-review','caption'} <= set(p['memory']['request']['tasks']))

    def test_unknown_effect_broadens_instead_of_dropping_writing_tasks(self):
        p=self.packet('write',mode='revision',effects=['unfamiliar'],tasks=['video-review'])
        self.assertEqual(p['routing']['effective_stage'],'all')
        self.assertTrue({'video-prompt-revision','video-review'}<=set(p['memory']['request']['tasks']))
        self.assertIn('save.md',{s['path'] for s in p['sources']})

    def test_missing_stage_or_config_falls_back_to_full_sources(self):
        p=self.packet('concept',mode='caption')
        self.assertEqual(p['routing']['effective_stage'],'all')
        (self.root/self.recipe['routing']).unlink()
        p=self.packet('concept')
        self.assertEqual(p['routing']['effective_stage'],'all')
        self.assertIn('write.md',{s['path'] for s in p['sources']})

    def test_invalid_config_and_missing_required_source_do_not_silently_skip(self):
        self.write(self.recipe['routing'],'{}')
        with self.assertRaises(ValueError):self.packet()
        self.sync();(self.root/'concept.md').unlink()
        with self.assertRaises(FileNotFoundError):self.packet('concept')

    def test_alias_cycle_and_effect_dependency_missing_rejected(self):
        self.config['modes']['new']='reference';self.sync()
        with self.assertRaises(ValueError):self.packet()
        self.config['modes']['new']=self.config['modes']['revision']
        self.config['effects']['camera']['requires']=['not-configured'];self.sync()
        with self.assertRaises(ValueError):self.packet(effects=['camera'])

    def test_config_source_and_builder_changes_invalidate(self):
        for rel in ('03-Projects/one/context-routing.json','scripts/chayvideo_context.py',
                    'scripts/context_routing.py','concept.md'):
            p=self.packet('concept')
            path=self.root/rel;old=path.read_bytes();path.write_bytes(old+b' ')
            self.assertTrue(ctx.verify(self.root,p),rel)
            path.write_bytes(old)

    def test_missing_packet_source_or_modified_body_rejected(self):
        p=self.packet('concept');p['sources']=[s for s in p['sources'] if s['path']!='concept.md']
        self.assertIn('routing_sources_missing',ctx.verify(self.root,p))
        p=self.packet('concept');p['sources'][0]['text']='Forged display'
        self.assertTrue(ctx.verify(self.root,p))

    def test_stage_request_tampering_invalidates(self):
        p=self.packet('concept');p['routing_request']['stage']='write'
        self.assertIn('routing_plan',ctx.verify(self.root,p))
        p=self.packet('concept');p['memory']['request']['tasks']=['caption']
        self.assertIn('routing_memory_tasks',ctx.verify(self.root,p))

    def test_view_preserves_exact_unicode_newlines_and_conditions(self):
        p=self.packet('concept')
        p['memory']['active']=[dict(id='L-unknown',sha256='a'*64,status='active',scope='shared',
            conditions=dict(tasks=['research'],models=['unknown-model']),summary='Original exception',
            condition_match='unknown',relation='needs_review')]
        rendered,receipt=self.view(p)
        for s in p['sources']:self.assertIn(s['text'],rendered)
        for word in ('unknown-model','unknown','needs_review','remaining','next_cursor','errors','Original exception'):
            self.assertIn(word,rendered)
        self.assertEqual({s['path'] for s in receipt['sources']},{s['path'] for s in p['sources']})

    def test_reuse_requires_retention_assertion(self):
        p=self.packet();_,receipt=self.view(p)
        with self.assertRaises(ValueError):self.view(p,seen=[receipt])
        rendered,_=self.view(p,seen=[receipt],retained=True)
        self.assertNotIn('SOURCE ',rendered)

    def test_compaction_or_other_workspace_forces_full_reload(self):
        p=self.packet();_,receipt=self.view(p)
        for key,value in [('context_id','epoch-previous'),('root','another-root'),('dependency_digest','old')]:
            changed=receipt|{key:value}
            rendered,_=self.view(p,seen=[changed],retained=True)
            for s in p['sources']:self.assertIn(s['text'],rendered)

    def test_new_to_revision_reuses_only_originals_still_retained(self):
        initial=self.packet();_,receipt=self.view(initial)
        revision=self.packet('write',mode='revision')
        rendered,new_receipt=self.view(revision,seen=[receipt],retained=True)
        self.assertNotIn('SOURCE ',rendered)
        self.assertIn('REUSED IN ASSERTED CURRENT CONTEXT',rendered)
        self.assertTrue(new_receipt['sources'])

    def test_partial_display_does_not_grant_whole_packet_coverage(self):
        p=self.packet();_,receipt=self.view(p,paths=['concept.md'])
        self.assertEqual(len(receipt['sources']),1)
        result=ctx.coverage(self.root,[p],[receipt],'epoch-1',True)
        self.assertFalse(result['complete'])
        self.assertIn('write.md',result['missing_sources'])

    def test_whole_source_batches_never_cut_or_mark_unshown_sources_read(self):
        p=self.packet();seen=[];displayed=set()
        for _ in range(len(p['sources'])):
            body,receipt=self.view(p,seen=seen,retained=True,max_chars=10)
            newly={r['path'] for r in receipt['sources']}-displayed
            self.assertEqual(len(newly),1)
            path=next(iter(newly));source=next(s for s in p['sources'] if s['path']==path)
            self.assertIn(source['text'],body)
            displayed.add(path);seen=[receipt]
            if not receipt['remaining_sources']:break
            self.assertFalse(ctx.coverage(self.root,[p],seen,'epoch-1',True)['complete'])
        self.assertEqual(displayed,{s['path'] for s in p['sources']})
        self.assertTrue(ctx.coverage(self.root,[p],seen,'epoch-1',True)['complete'])

    def test_coverage_closes_only_after_all_stages_read_in_same_context(self):
        packets=[];receipts=[]
        for stage in ('concept','write','review','save'):
            p=self.packet(stage);packets.append(p)
            _,receipt=self.view(p,seen=receipts,retained=True);receipts.append(receipt)
        self.assertTrue(ctx.coverage(self.root,packets,[receipts[-1]],'epoch-1',True)['complete'])
        self.assertFalse(ctx.coverage(self.root,packets,[receipts[-1]],'different-epoch',True)['complete'])
        with self.assertRaises(ValueError):ctx.coverage(self.root,packets,receipts,'epoch-1',False)

    def test_source_changed_after_read_makes_coverage_incomplete(self):
        p=self.packet();_,receipt=self.view(p)
        self.write('concept.md','changed source')
        result=ctx.coverage(self.root,[p],[receipt],'epoch-1',True)
        self.assertFalse(result['complete']);self.assertIn('concept.md',result['stale'])

    def test_coverage_cannot_mix_modes_or_species(self):
        with self.assertRaises(ValueError):ctx.coverage(self.root,[self.packet(),self.packet(mode='revision')])

    def test_new_unknown_species_keeps_research_pending(self):
        p=ctx.packet(self.root,'one','new',['other-species'],'natural',stage='concept')
        self.assertTrue(p['pending']);self.assertNotIn('muskie.md',{s['path'] for s in p['sources']})
        self.assertNotIn('tackle.md',{s['path'] for s in p['sources']})

    def test_caption_never_navigates_species_tackle_or_brainstorm(self):
        p=self.packet('write',mode='caption')
        self.assertTrue({'muskie.md','tackle.md','concept.md'}.isdisjoint({s['path'] for s in p['sources']}))

    def test_cross_platform_config_path_escape_rejected(self):
        for path in ('../outside','C:/outside','C:relative','//server/share/file'):
            self.recipe['routing']=path
            with self.assertRaises(ValueError):routing.route(self.root,'one',self.recipe,'new','write')

    def test_plain_cli_view_emits_verified_text_and_protects_source_files(self):
        p=self.packet('concept')
        self.write('.nature-studio/context/p.json',json.dumps(p))
        command=[sys.executable,'-X','utf8',str(ctx.ROOT/'scripts/chayvideo_context.py'),
                 '--root',str(self.root),'view','.nature-studio/context/p.json']
        result=subprocess.run(command,capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout)
        self.assertIn((self.root/'concept.md').read_bytes(),result.stdout)
        original=(self.root/'concept.md').read_bytes()
        result=subprocess.run(command+['--receipt','concept.md'],capture_output=True)
        self.assertNotEqual(result.returncode,0);self.assertEqual((self.root/'concept.md').read_bytes(),original)


if __name__=='__main__':unittest.main()
