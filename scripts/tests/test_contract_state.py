"""Contract exceptions, reproducible save metadata and schema2 QA on temporary fixtures."""
import copy,json,hashlib,tempfile,subprocess,sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import chayvideo_output as output
import production_state as state_tool
import test_chayvideo as fixtures


class ContractTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name).resolve()
        self.base=self.root/'04-Productions/underwater/UF-0001';self.base.mkdir(parents=True)
        self.good=fixtures.OutputTests().good()

    def grant(self,data=None,mode='new',target='A01'):
        data=data or self.good
        prompt=data['video_prompt'];request=self.base/'request.md';request.write_text('Synthetic user authorization fixture only')
        grant=dict(schema=1,rule='beat_count',project='underwater',production='UF-0001',mode=mode,beat_count=len(__import__('re').findall(r'\[[0-9.]+[–-]',prompt)),confirmed_user_request=True,
             authorization=dict(path='request.md',sha256=output.sha256(request)),video_prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),target_attempt=target)
        if 'base_attempt' in data:grant.update(base_attempt=data['base_attempt'],base_sha256=data['base_sha256'])
        self.write_grant(data,grant);return grant

    def write_grant(self,data,grant):
        file=self.base/'exception.json';file.write_text(json.dumps(grant),encoding='utf-8');data['contract_exception']=dict(path='exception.json',sha256=output.sha256(file))

    def nine(self):
        # Outside the default 5–10 range (UF-D025): 11 contiguous beats, first ends by 3.0s.
        b=['0.0','1.0','2.0','3.0','4.0','5.0','6.0','7.0','8.0','8.5','9.0','10.0']
        data=copy.deepcopy(self.good);data['video_prompt']='Handheld underwater shot. '+'; '.join(f'[{x}-{y}s] fixture' for x,y in zip(b,b[1:]));return data

    def test_check_save_check_roundtrip(self):
        saved=output.save(self.root,'underwater','UF-0001',self.good);stored=json.loads((saved/'OUTPUT.json').read_text(encoding='utf-8'))
        self.assertEqual(stored['checks'],self.good['checks']);self.assertFalse(output.validate(stored,underwater=True))
        resolved=output.resolve(self.root,'underwater','UF-0001',saved.name);self.assertEqual(resolved['validation_metadata']['checks'],self.good['checks'])

    def test_default_count_and_timeline_errors_are_separate(self):
        data=self.nine();errors=output.validate(data,underwater=True)
        self.assertTrue(any('beat' in e for e in errors));self.assertFalse(any('timeline' in e for e in errors))

    def test_supported_exception_save_and_recheck(self):
        data=self.nine();self.grant(data);contract=output.effective_contract(self.root,'underwater','UF-0001',data,'new')
        self.assertFalse(output.validate(data,underwater=True,contract=contract))
        folder=output.save(self.root,'underwater','UF-0001',data);stored=json.loads((folder/'OUTPUT.json').read_text(encoding='utf-8'))
        contract=output.effective_contract(self.root,'underwater','UF-0001',stored,'new')
        self.assertFalse(output.validate(stored,underwater=True,contract=contract))
        with self.assertRaises(ValueError):output.save(self.root,'underwater','UF-0001',data)

    def test_unbound_json_override_is_not_authority(self):
        data=self.nine();data['checks']['beat_count_override']=9
        self.assertTrue(output.validate(data,underwater=True))
        self.grant(data);self.assertTrue(output.validate(data,underwater=True))

    def test_wrong_scope_and_confirmation_rejected(self):
        for key,value in [('project','other'),('production','UF-0002'),('mode','reference'),('rule','duration'),('confirmed_user_request',False)]:
            data=self.nine();grant=self.grant(data);grant[key]=value;self.write_grant(data,grant)
            with self.subTest(key=key),self.assertRaises(ValueError):output.effective_contract(self.root,'underwater','UF-0001',data,'new')

    def test_changed_request_and_prompt_rejected(self):
        data=self.nine();self.grant(data);(self.base/'request.md').write_text('changed')
        with self.assertRaises(ValueError):output.effective_contract(self.root,'underwater','UF-0001',data,'new')
        self.grant(data);data['video_prompt']+=' changed'
        with self.assertRaises(ValueError):output.effective_contract(self.root,'underwater','UF-0001',data,'new')

    def test_exception_does_not_waive_key_or_timeline(self):
        for transform in (lambda s:s.replace('[0.0-1.0s]','[0.0-1.5s]'),lambda s:s.replace('[9.0-10.0s]','[9.0-11.0s]')):
            data=self.nine();data['video_prompt']=transform(data['video_prompt']);self.grant(data)
            contract=output.effective_contract(self.root,'underwater','UF-0001',data,'new')
            self.assertTrue(any('timeline' in e for e in output.validate(data,underwater=True,contract=contract)))
        data=self.nine();data['checks']['key_onset']=4;self.grant(data)
        contract=output.effective_contract(self.root,'underwater','UF-0001',data,'new');self.assertTrue(output.validate(data,underwater=True,contract=contract))

    def test_wrong_target_does_not_create_attempt(self):
        data=self.nine();self.grant(data,target='A99')
        with self.assertRaises(ValueError):output.save(self.root,'underwater','UF-0001',data)
        self.assertFalse((self.base/'A99').exists());self.assertFalse((self.base/'A01').exists())

    def test_caption_cannot_change_reference_or_exception(self):
        for key in ('asset_selection','contract_exception'):
            data={'caption':self.good['caption'],key:{}}
            self.assertTrue(output.validate(data,'caption',True))

    def test_revision_exception_pins_base(self):
        folder=output.save(self.root,'underwater','UF-0001',self.good)
        data=self.nine();data.update(base_attempt=folder.name,base_sha256=output.sha256(folder/'OUTPUT.json'))
        grant=self.grant(data,'revision','A02');grant['base_sha256']='bad';self.write_grant(data,grant)
        with self.assertRaises(ValueError):output.save(self.root,'underwater','UF-0001',data,'revision')
        self.grant(data,'revision','A02');self.assertEqual(output.save(self.root,'underwater','UF-0001',data,'revision').name,'A02')

    def test_reference_uses_same_exception_contract(self):
        data=self.nine();self.grant(data,'reference');self.assertEqual(output.save(self.root,'underwater','UF-0001',data,'reference').name,'A01')

    def test_check_cli_uses_same_scoped_rules(self):
        data=self.nine();self.grant(data);file=self.root/'input.json';file.write_text(json.dumps(data))
        command=[sys.executable,str(Path(output.__file__)),'--root',str(self.root),'check',str(file),'--project','underwater','--production','UF-0001']
        result=subprocess.run(command,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_caption_resolve_retains_video_check_metadata(self):
        folder=output.save(self.root,'underwater','UF-0001',self.good)
        data=dict(caption=self.good['caption'],base_attempt=folder.name,base_sha256=output.sha256(folder/'OUTPUT.json'),files=self.good['files'])
        revised=output.save(self.root,'underwater','UF-0001',data,'caption')
        self.assertEqual(output.resolve(self.root,'underwater','UF-0001',revised.name)['validation_metadata']['checks'],self.good['checks'])


class StateTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name).resolve()
        for file in ('text.md','render.bin','review.md','approval.md'):(self.root/file).write_text('Synthetic binding fixture, not media or approval')
        self.state=dict(schema=2,current_text=self.bind('text.md'),reviewed_render=self.bind('render.bin'),selected_render=None,approval='none',approval_evidence=None,
              qa=dict.fromkeys(state_tool.DOMAINS,'pass'),qa_evidence=self.bind('review.md'),qa_coverage={k:dict(status='complete',method='synthetic-test-only') for k in state_tool.DOMAINS})
    def bind(self,name):return dict(path=name,sha256=output.sha256(self.root/name))
    def check(self,data=None):return state_tool.validate(data or self.state,self.root)

    def test_valid_schema2_qa_independent_of_approval(self):
        result=self.check();self.assertTrue(result['valid']);self.assertTrue(result['qa_pass']);self.assertEqual(result['approval'],'none')

    def test_no_reviewed_render_cannot_qa_pass(self):
        self.state['reviewed_render']=None;result=self.check();self.assertFalse(result['valid']);self.assertFalse(result['qa_pass'])

    def test_legacy_preserved_but_not_certified(self):
        self.state['schema']=1;result=self.check();self.assertTrue(result['valid']);self.assertFalse(result['qa_pass']);self.assertTrue(result['unverified'])

    def test_partial_coverage_not_full_pass(self):
        self.state['qa_coverage']['motion']['status']='partial';result=self.check();self.assertTrue(result['valid']);self.assertFalse(result['qa_pass'])

    def test_missing_evidence_not_pass(self):
        self.state['qa_evidence']=None;result=self.check();self.assertFalse(result['valid']);self.assertFalse(result['qa_pass'])

    def test_null_types_report_errors_without_crash(self):
        for key in ('qa','qa_coverage','current_text'):
            data=copy.deepcopy(self.state);data[key]=None
            with self.subTest(key=key):self.assertFalse(self.check(data)['valid'])
        for data in ([],None,'invalid'):
            self.assertFalse(state_tool.validate(data,self.root)['valid'])

    def test_approval_requires_selected_and_bound_evidence(self):
        self.state.update(approval='final',selected_render=self.bind('render.bin'))
        self.assertFalse(self.check()['valid']);self.state['approval_evidence']=self.bind('approval.md');self.assertTrue(self.check()['valid'])

    def test_final_approval_does_not_erase_failed_qa(self):
        self.state.update(approval='final',selected_render=self.bind('render.bin'),approval_evidence=self.bind('approval.md'))
        self.state['qa']['audio']='fail';result=self.check();self.assertTrue(result['valid']);self.assertFalse(result['qa_pass']);self.assertEqual(result['approval'],'final')

    def test_changed_file_or_review_detected(self):
        for file in ('render.bin','review.md'):
            original=(self.root/file).read_bytes();(self.root/file).write_text('changed');self.assertFalse(self.check()['valid']);(self.root/file).write_bytes(original)

    def test_paths_cannot_escape(self):
        for path in ('../outside','C:/outside','/outside'):
            self.state['reviewed_render']['path']=path;self.assertFalse(self.check()['valid'])

    def test_text_only_new_state_is_valid_and_unreviewed(self):
        self.state.update(reviewed_render=None,qa=dict.fromkeys(state_tool.DOMAINS,'not_checked'),qa_evidence=None,qa_coverage={})
        self.assertTrue(self.check()['valid']);self.assertFalse(self.check()['qa_pass'])


if __name__=='__main__':unittest.main()
