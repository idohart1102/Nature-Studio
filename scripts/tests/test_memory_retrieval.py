"""Retrieval contracts on isolated source fixtures; no production or activation writes."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import memory_retrieval as mem
import chayvideo_context as ctx


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.write('03-Projects/one/PROJECT.md', 'ID: one\n')
        self.write('03-Projects/two/PROJECT.md', 'ID: two\n')
        self.write('00-Standards/memory-taxonomy.json',
                   (mem.ROOT/'00-Standards/memory-taxonomy.json').read_text(encoding='utf-8'))

    def write(self, rel, text):
        path=self.root/rel; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding='utf-8'); return path

    def lesson(self, name, task='video-review', topic='tackle-continuity', status='active',
               scope='project', project='one', retrieval=True, **conditions):
        data=dict(id='L-'+name,version='0.1',status=status,scope=scope,
                  project_id=project if scope=='project' else None,
                  action='Inspect '+topic,conditions=dict(tasks=[task],models=[],interfaces=[],formats=[]))
        data['conditions'].update(conditions)
        if retrieval:
            data['retrieval']=dict(schema=1,summary='Check '+topic+'; inspect exceptions.',
                                   topics=[topic],entities=['muskie'],interactions=['angling'])
        namespace='05-Memory/shared' if scope=='shared' else '05-Memory/projects/'+project
        path=self.write(namespace+'/'+mem.STATUSES[status]+'/L-'+name+'.md',
                        '---\n'+json.dumps(data)+'\n---\n'+'Original evidence and exceptions. '*200)
        return path

    def query(self, **kw):
        return mem.query(self.root,'one',**kw)

    def test_aliases_conditions_and_scope(self):
        self.lesson('line');self.lesson('motion',topic='animal-motion');self.lesson('shared',scope='shared')
        self.lesson('caption',task='caption-writing',topic='caption');self.lesson('other',project='two')
        q=self.query(tasks=['đánh giá video'],topics=['dây câu'],entities=['Esox masquinongy'])
        self.assertEqual({r['id'] for r in q['active']},{'L-line','L-motion','L-shared'})
        self.assertEqual(q['active'][0]['condition_match'],'match')
        self.assertTrue(any('topics:tackle-continuity' in r['reasons'] for r in q['active']))
        self.assertEqual(q['excluded_conditions'],1)

    def test_unknown_legacy_and_empty_dimensions(self):
        self.lesson('legacy',retrieval=False);self.lesson('model',models=['specific-backend'])
        self.lesson('custom',task='custom-task',topic='custom-label')
        q=self.query(tasks=['video-review'])
        rows={r['id']:r for r in q['active']}
        self.assertEqual(rows['L-model']['condition_match'],'unknown')
        self.assertEqual(rows['L-custom']['condition_match'],'unknown')
        self.assertEqual(rows['L-legacy']['relation'],'needs_review')
        q=self.query(tasks=['video-review'],models=['different-backend'])
        self.assertNotIn('L-model',{r['id'] for r in q['active']})

    def test_topics_rank_without_exclusion(self):
        self.lesson('line');self.lesson('unfamiliar',topic='another-topic')
        q=self.query(tasks=['video-review'],topics=['dây câu'])
        self.assertEqual(q['active'][0]['id'],'L-line')
        self.assertEqual(len(q['active']),2)
        self.assertEqual(q['active'][1]['relation'],'deferred')
        self.assertTrue(all(r['relation']=='needs_review' for r in self.query(tasks=['video-review'],broad=True)['active']))

    def test_statuses_separate_and_never_activated(self):
        self.lesson('active'); c=self.lesson('candidate',status='candidate');self.lesson('old',status='retired')
        before=c.read_bytes();q=self.query(tasks=['video-review'])
        self.assertEqual(len(q['active']),1);self.assertFalse(q['candidates']);self.assertFalse(q['retired'])
        q=self.query(tasks=['video-review'],candidates=True,retired=True)
        self.assertEqual(len(q['candidates']),1);self.assertEqual(len(q['retired']),1)
        self.assertEqual(mem.load_lessons(self.root,'one',q,['L-candidate'])[0]['status'],'candidate')
        self.assertEqual(c.read_bytes(),before)

    def test_pagination_freshness_and_cache_rebuild(self):
        for i in range(7):self.lesson(str(i))
        kw=dict(tasks=['video-review'],page_size=2);q=self.query(**kw);seen=set()
        while True:
            seen.update(r['id'] for r in q['active'])
            if not q['next_cursor']:break
            q=self.query(**kw,cursor=q['next_cursor'])
        self.assertEqual(len(seen),7);self.assertTrue(q['discovery_complete'])
        old=self.query(**kw);self.lesson('new')
        with self.assertRaises(ValueError):self.query(**kw,cursor=old['next_cursor'])
        with self.assertRaises(ValueError):mem.load_lessons(self.root,'one',old,[old['active'][0]['id']])
        fresh=self.query(**kw);shutil.rmtree(self.root/'.nature-studio/memory')
        self.assertEqual(self.query(**kw)['fingerprint'],fresh['fingerprint'])

    def test_edit_delete_move_taxonomy_invalidate(self):
        p=self.lesson('a');first=self.query()
        p.write_text(p.read_text(encoding='utf-8')+'changed',encoding='utf-8');second=self.query()
        self.assertNotEqual(first['fingerprint'],second['fingerprint'])
        p.unlink();third=self.query();self.assertNotEqual(second['fingerprint'],third['fingerprint'])
        self.lesson('a',status='candidate');fourth=self.query()
        self.assertNotEqual(third['fingerprint'],fourth['fingerprint'])
        t=self.root/'00-Standards/memory-taxonomy.json';d=json.loads(t.read_text(encoding='utf-8'));d['topics']['custom']=['new'];t.write_text(json.dumps(d),encoding='utf-8')
        self.assertNotEqual(fourth['fingerprint'],self.query()['fingerprint'])

    def test_bad_metadata_duplicate_status_and_paths(self):
        self.lesson('a');self.lesson('a',scope='shared')
        q=self.query();self.assertTrue(q['errors']);self.assertFalse(q['discovery_complete'])
        with self.assertRaises(ValueError):mem.load_lessons(self.root,'one',q,['L-a'])
        for path in ('../outside','C:/outside','C:relative','//server/share/outside','../one'):
            with self.assertRaises(ValueError):mem.local(self.root,path)
        with self.assertRaises(ValueError):mem.scan(self.root,'../one')
        self.write('05-Memory/projects/one/active/L-bad.md','broken JSON')
        self.assertGreaterEqual(len(self.query()['errors']),2)
        p=self.lesson('moved');p.rename(p.with_name('L-relocated.md').parent.parent/'L-moved.md')
        self.assertTrue(any('directory' in e['error'] for e in self.query()['errors']))

    def test_selection_tampering_rejected(self):
        self.lesson('a');q=self.query();q['active'][0]['path']='VERSION'
        with self.assertRaises(ValueError):mem.load_lessons(self.root,'one',q,['L-a'])
        q=self.query();q['active'][0]['status']='candidate'
        with self.assertRaises(ValueError):mem.load_lessons(self.root,'one',q,['L-a'])

    def test_packet_omits_indexes_and_body_until_selected(self):
        self.lesson('a',task='video-prompt-revision')
        for rel in ['VERSION','START-HERE.md','SYSTEM.md','AGENTS.md',
                    '.agents/skills/na-chayvideo/SKILL.md','.agents/skills/na-chayvideo/references/workflow.md',
                    '00-Standards/video-prompt-workflow.md','.agents/skills/na-chayvideo/references/revision.md']:
            self.write(rel,'fixture')
        index='05-Memory/projects/one/INDEX.md';self.write(index,'massive private index '*1000)
        self.write('03-Projects/one/context-map.json',json.dumps(dict(common=[index],revision=[])))
        p=ctx.packet(self.root,'one','revision');self.assertNotIn(index,[s['path'] for s in p['sources']])
        self.assertFalse(any(s['path'].startswith('05-Memory/') for s in p['sources']))
        p=ctx.packet(self.root,'one','revision',memory_selection=p['memory'],lesson_ids=['L-a'])
        self.assertIn('05-Memory/projects/one/active/L-a.md',[s['path'] for s in p['sources']])
        self.assertFalse(ctx.verify(self.root,p));self.lesson('new')
        self.assertIn('memory_inventory',ctx.verify(self.root,p))

    def test_optional_retrieval_validation(self):
        self.assertTrue(mem.retrieval_errors({}))
        self.assertTrue(mem.retrieval_errors(dict(schema=1,summary='x',topics='wrong',entities=[],interactions=[])))
        self.assertFalse(mem.retrieval_errors(dict(schema=1,summary='x',topics=['novel'],entities=[],interactions=[])))


if __name__=='__main__':unittest.main()
