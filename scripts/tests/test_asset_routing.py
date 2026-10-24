"""Project routing and declared tool-input bindings; synthetic fixtures, no media calls."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import asset_catalog as a
import chayvideo_output as out
import test_assets as fixtures
import test_revision_frame as frames


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.AssetTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.root=self.f.root;self.record=copy.deepcopy(self.f.record)
        self.record['applicability']=dict(scope='shared',project_ids=[])
        self.req=self.f.requests
    def reg(self,row=None,expected=None):return a.register(self.root,row or self.record,expected)
    def select(self):return a.selection(self.root,self.req,[self.record['asset_id']],'deer-project')
    def bind(self,path):return dict(path=path.relative_to(self.root).as_posix(),sha256=a.file_hash(path))
    def actual(self):
        self.reg();receipt=self.select();p=self.root/'selection.json';p.write_text(json.dumps(receipt))
        prompt=self.root/'prompt.txt';prompt.write_text('Synthetic prompt.',encoding='utf-8')
        output=self.root/'output.bin';output.write_bytes(b'synthetic output, not media')
        return dict(schema=1,project_id='deer-project',production_id='UF-0001',attempt_id='A01',call_id='call-1',cycle_id='cycle-1',outcome='not_submitted',
          selection=self.bind(p),prompt=self.bind(prompt),inputs=[dict(**self.record['file'],asset_id=self.record['asset_id'],purpose='identity',kind='reference')],
          tool=dict(name='image_gen',arguments=dict(prompt=prompt.read_text(),referenced_image_paths=[str(self.f.file)])),output=None)

    def test_shared_project_view_filters(self):
        self.reg();self.assertEqual(self.select()['status'],'matched')
        self.assertFalse(a.query(self.root,[{**self.req[0],'view':'other'}],project_id='deer-project')['assets'])
        self.assertEqual(len(a.details(self.root,[self.record['asset_id']],'deer-project')['assets']),1)

    def test_foreign_project_excluded(self):
        self.record['applicability']=dict(scope='projects',project_ids=['fish-project']);self.reg()
        self.assertFalse(a.query(self.root,self.req,project_id='deer-project')['assets'])
        with self.assertRaises(ValueError):self.select()
        with self.assertRaises(ValueError):a.details(self.root,[self.record['asset_id']],'deer-project')

    def test_unknown_shown_but_not_certified(self):
        self.record.pop('applicability');self.reg()
        q=a.query(self.root,self.req,project_id='deer-project')
        self.assertTrue(q['assets'][0]['scope_issue']);self.assertTrue(q['missing']);self.assertEqual(self.select()['status'],'needs_review')

    def test_legacy_receipt_not_project_certified(self):
        self.reg();rec=a.selection(self.root,self.req,[self.record['asset_id']])
        self.assertEqual(a.verify(self.root,rec)['status'],'matched')
        self.assertEqual(a.verify(self.root,rec,'deer-project')['status'],'needs_review')

    def test_scope_checked_on_dependency(self):
        parent=copy.deepcopy(self.record);parent.update(asset_id='REF-PRIVATE',applicability=dict(scope='projects',project_ids=['other']))
        self.reg(parent);self.record['requires']=['REF-PRIVATE'];self.reg()
        self.assertIn('outside Project',str(self.select()['issues']))

    def test_new_matching_record_does_not_stale_selection(self):
        self.reg();rec=self.select();other=copy.deepcopy(self.record);other['asset_id']='REF-NEW';self.reg(other)
        self.assertEqual(a.verify(self.root,rec,'deer-project')['status'],'matched')

    def test_bad_scope_metadata_rejected(self):
        for value in [dict(scope='shared',project_ids=['x']),dict(scope='projects',project_ids=[]),dict(scope='all',project_ids=[])]:
            self.record['applicability']=value
            with self.assertRaises(ValueError):self.reg()

    def test_actual_inputs_and_historical_catalog_change(self):
        record=self.actual();self.assertEqual(a.inputs_check(self.root,record)['status'],'matched')
        routed=copy.deepcopy(record);routed['tool']['name']='9router_image'
        self.assertEqual(a.inputs_check(self.root,routed)['status'],'matched')
        routed['tool']['name']='other_api'
        with self.assertRaises(ValueError):a.inputs_check(self.root,routed)
        record.update(outcome='success',output=self.bind(self.root/'output.bin'))
        old=self.select()['records'][0]['record_sha256'];self.record['notes']='metadata changed';self.reg(expected=old)
        self.assertEqual(a.inputs_check(self.root,record)['status'],'needs_review')
        self.assertEqual(a.inputs_check(self.root,record,historical=True)['status'],'matched')

    def test_actual_wrong_order_prompt_or_project(self):
        record=self.actual()
        for mutate in [lambda x:x['tool']['arguments'].update(referenced_image_paths=[]),lambda x:x['tool']['arguments'].update(prompt='wrong'),lambda x:x.update(project_id='wrong')]:
            row=copy.deepcopy(record);mutate(row);self.assertEqual(a.inputs_check(self.root,row)['status'],'needs_review')

    def test_no_reference_direct_input_supported(self):
        record=self.actual();record['selection']=None;record['inputs'][0].pop('asset_id');record['inputs'][0]['kind']='edit_target'
        self.assertEqual(a.inputs_check(self.root,record)['status'],'matched')
        record['inputs']=[];record['tool']['arguments'].pop('referenced_image_paths')
        self.assertEqual(a.inputs_check(self.root,record)['status'],'matched')

    def test_conversation_inputs_not_falsely_local_verified(self):
        record=self.actual();record['tool']['arguments']['num_last_images_to_include']=1
        self.assertEqual(a.inputs_check(self.root,record)['status'],'needs_review')

    def test_preflight_before_reservation_has_no_invented_call_id(self):
        record=self.actual();record.update(call_id=None,cycle_id=None)
        self.assertEqual(a.inputs_check(self.root,record)['status'],'matched')
        record['outcome']='success'
        self.assertEqual(a.inputs_check(self.root,record)['status'],'needs_review')

    def test_modified_or_unselected_actual_asset_not_verified(self):
        record=self.actual();record['inputs'][0]['asset_id']='NOT-SELECTED'
        self.assertEqual(a.inputs_check(self.root,record)['status'],'needs_review')
        record=self.actual_without_register(record)

    def actual_without_register(self,record):
        self.f.file.write_bytes(b'changed')
        self.assertEqual(a.inputs_check(self.root,record)['status'],'needs_review')

    def test_requirements_validation(self):
        self.assertFalse(a.requirement_errors(dict(schema=1,items=[],none_reason='No reference needed.')))
        self.assertTrue(a.requirement_errors(dict(schema=1,items=[],none_reason=None)))
        self.assertTrue(a.requirement_errors(dict(schema=1,items=[{}],none_reason=None)))


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.f=frames.RevisionFrameTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
    def test_requirements_save_resolve_caption(self):
        req=dict(schema=1,items=[],none_reason='No image reference needed.')
        b=self.f.revise(self.f.a,idea='Changed story.',frame_state=self.f.state,reference_requirements=req)
        c=self.f.revise(b,mode='caption',caption='Different caption.')
        self.assertEqual(self.f.resolved(c)['reference_requirements'],req)
        with self.assertRaises(ValueError):self.f.revise(c,mode='caption',caption='Caption.',reference_requirements=req)

    def test_schema3_actual_output_binding(self):
        f=self.f;r=f.record();base=f.base;root=f.root
        prompt=base/'prompt.txt';prompt.write_text('Synthetic image prompt.',encoding='utf-8')
        def bind(p):return dict(path=p.relative_to(root).as_posix(),sha256=a.file_hash(p))
        actual=dict(schema=1,project_id='stable-one',production_id='UF-0001',attempt_id=f.a,call_id='call',cycle_id='cycle',outcome='success',selection=None,prompt=bind(prompt),inputs=[],tool=dict(name='image_gen',arguments=dict(prompt=prompt.read_text())),output=bind(base/'image.png'))
        p=base/'asset-inputs.json';p.write_text(json.dumps(actual))
        r.update(schema=3,asset_inputs=bind(p),call_id='call',cycle_id='cycle',reference_requirements_sha256=out.snapshot_hash([]));f.write_record(r)
        self.assertEqual(f.check()['status'],'matched');self.assertEqual(f.check()['asset_inputs_status'],'matched')
        actual['call_id']='wrong';p.write_text(json.dumps(actual));r['asset_inputs']=bind(p);f.write_record(r)
        self.assertEqual(f.check()['status'],'invalid')

    def test_legacy_frame_binding_stays_separate(self):
        self.f.record();self.assertEqual(self.f.check()['status'],'matched');self.assertEqual(self.f.check()['asset_inputs_status'],'unverified')

    def test_video_only_requirements_do_not_affect_opening_snapshot(self):
        base=dict(schema=1,items=[dict(subject='Visible later',entity_id=None,role='identity',variant=None,stage=None,view=None,must_preserve='Shape',reason='Reveal',essential=True,applies_to='video')],none_reason=None)
        b=self.f.revise(self.f.a,video_prompt='Changed later motion.',frame_state=self.f.state,reference_requirements=base)
        self.assertEqual(out.frame_snapshot(self.f.resolved(b)),out.frame_snapshot(self.f.resolved()))


if __name__=='__main__':unittest.main()
