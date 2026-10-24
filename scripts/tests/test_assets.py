"""Asset catalog and context integration, synthetic bytes in disposable workspaces only."""
import copy
import json
from pathlib import Path
import sqlite3
from contextlib import closing
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import asset_catalog as assets
import chayvideo_context as ctx
import context_routing
import chayvideo_output as output
import test_chayvideo as output_fixtures
import test_context_routing as routing_fixtures


class AssetTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name).resolve()
        self.file=self.root/'references/body.bin';self.file.parent.mkdir();self.file.write_bytes(b'not an image: synthetic reference bytes')
        self.evidence=self.root/'references/review.md';self.evidence.write_text('Synthetic declaration only; no actual animal was QAed.')
        self.record=dict(asset_id='REF-FISH-01',entity_id='K-SP-REDFISH-001',kind='organism',roles=['identity'],stage='adult',view='lateral',origin='photo',
            source={'url':'https://example.org/synthetic-fixture','rights':'fixture only'},
            file={'path':'references/body.bin','sha256':assets.file_hash(self.file)},
            review={'status':'pass','roles':['identity'],'evidence':{'path':'references/review.md','sha256':assets.file_hash(self.evidence)}})
        self.requests=[dict(entity_id='K-SP-REDFISH-001',role='identity',stage='adult')]

    def register(self,record=None,expected=None): return assets.register(self.root,record or self.record,expected)
    def select(self): return assets.selection(self.root,self.requests,[self.record['asset_id']])

    def test_derivation_tracks_parent_hash_and_closure(self):
        first=self.register();child=copy.deepcopy(self.record);child['asset_id']='REF-CROP'
        child['derivation']=dict(parent_id='REF-FISH-01',parent_record_sha256=first['record_sha256'],operation='synthetic crop fixture')
        assets.register(self.root,child)
        receipt=assets.selection(self.root,self.requests,['REF-CROP']);self.assertEqual(receipt['status'],'matched');self.assertEqual(len(receipt['records']),2)
        parent=copy.deepcopy(self.record);parent['view']='changed';self.register(parent,first['record_sha256'])
        self.assertEqual(assets.verify(self.root,receipt)['status'],'stale')
        self.assertEqual(assets.selection(self.root,self.requests,['REF-CROP'])['status'],'needs_review')

    def test_derivation_requires_real_current_parent_binding(self):
        for derivation in ({},dict(parent_id='MISSING',parent_record_sha256='bad',operation='crop'),dict(parent_id='REF-FISH-01',parent_record_sha256='bad',operation='crop')):
            r=copy.deepcopy(self.record);r['derivation']=derivation
            with self.subTest(derivation=derivation),self.assertRaises(ValueError):assets.register(self.root,r)

    def test_output_save_resolve_preserves_planned_selection(self):
        self.register();receipt=self.select();data=output_fixtures.OutputTests().good();data['asset_selection']=receipt
        base=self.root/'04-Productions/underwater/UF-0001';base.mkdir(parents=True)
        folder=output.save(self.root,'underwater','UF-0001',data)
        resolved=output.resolve(self.root,'underwater','UF-0001',folder.name)
        self.assertEqual(resolved['asset_selection'],receipt);self.assertEqual(resolved['asset_selection_status'],'planned')
        data.update(base_attempt=folder.name,base_sha256=output.sha256(folder/'OUTPUT.json'))
        first=assets.query(self.root,self.requests)
        with assets.connection(self.root) as db:sha=db.execute('SELECT sha FROM assets').fetchone()[0]
        r=copy.deepcopy(self.record);r['view']='changed';self.register(r,sha)
        with self.assertRaises(ValueError):output.save(self.root,'underwater','UF-0001',data,'revision')

    def test_pending_selection_does_not_block_honest_text_save(self):
        r=copy.deepcopy(self.record);r['review']={'status':'not_checked'};self.register(r)
        data=output_fixtures.OutputTests().good();data['asset_selection']=self.select()
        (self.root/'04-Productions/underwater/UF-0001').mkdir(parents=True)
        saved=output.save(self.root,'underwater','UF-0001',data)
        self.assertEqual(json.loads((saved/'OUTPUT.json').read_text(encoding='utf-8'))['asset_selection']['status'],'needs_review')

    def test_empty_query_does_not_create_catalog(self):
        result=assets.query(self.root,self.requests)
        self.assertTrue(result['missing']);self.assertFalse((self.root/'.nature-studio').exists())

    def test_register_query_select_verify(self):
        self.register();self.assertEqual(len(assets.query(self.root,self.requests)['assets']),1)
        receipt=self.select();self.assertEqual(assets.verify(self.root,receipt)['status'],'matched')
        self.assertEqual(assets.query(self.root,self.requests)['assets'][0]['reviewed_roles'],['identity'])

    def test_register_records_no_automatic_visual_or_public_approval(self):
        self.register()
        with assets.connection(self.root) as db: row=json.loads(db.execute('SELECT body FROM assets').fetchone()[0])
        self.assertEqual(row['publication'],dict(visibility='private',reviewed=False))

    def test_update_requires_current_sha(self):
        first=self.register()
        with self.assertRaises(ValueError): self.register()
        result=self.register(expected=first['record_sha256']);self.assertEqual(result['revision'],2)
        with self.assertRaises(ValueError): self.register(expected=first['record_sha256'])

    def test_file_and_review_hashes_required(self):
        for field in ('file','review'):
            record=copy.deepcopy(self.record)
            target=record['file'] if field=='file' else record['review']['evidence'];target['sha256']='bad'
            with self.subTest(field=field), self.assertRaises(ValueError):self.register(record)

    def test_path_escape_and_drive_paths_rejected(self):
        for path in ('../outside','C:/secrets','C:\\secrets','/absolute','references/../body.bin'):
            with self.subTest(path=path),self.assertRaises(ValueError):assets.local(self.root,path)

    def test_unreviewed_reference_not_matched(self):
        r=copy.deepcopy(self.record);r['review']={'status':'not_checked','roles':[]};self.register(r)
        self.assertEqual(self.select()['status'],'needs_review')

    def test_url_only_is_a_reference_lead_not_verified_local_file(self):
        r=copy.deepcopy(self.record);r['file']=None;r['review']={'status':'not_checked'};self.register(r)
        self.assertEqual(self.select()['status'],'needs_review')

    def test_stage_and_entity_are_exact(self):
        self.register()
        for request in ({**self.requests[0],'stage':'juvenile'},{**self.requests[0],'entity_id':'OTHER'}):
            result=assets.query(self.root,[request]);self.assertFalse(result['assets']);self.assertTrue(result['missing'])

    def test_unspecified_organism_stage_cannot_certify_adult_selection(self):
        self.register();receipt=assets.selection(self.root,[dict(entity_id='K-SP-REDFISH-001',role='identity')],['REF-FISH-01'])
        self.assertEqual(receipt['status'],'needs_review')

    def test_equipment_does_not_require_life_stage(self):
        r=copy.deepcopy(self.record);r.update(kind='equipment',entity_id='HOOK-CIRCLE',stage=None);self.register(r)
        result=assets.selection(self.root,[dict(entity_id='HOOK-CIRCLE',role='identity')],['REF-FISH-01'])
        self.assertEqual(result['status'],'matched')

    def test_wrong_selected_id_rejected(self):
        self.register()
        with self.assertRaises(ValueError):assets.selection(self.root,self.requests,['UNKNOWN'])

    def test_multi_entity_request_needs_both(self):
        self.register();requests=self.requests+[dict(entity_id='PREY',stage='adult',role='identity')]
        receipt=assets.selection(self.root,requests,['REF-FISH-01']);self.assertEqual(receipt['status'],'needs_review')

    def test_missing_dependency_then_closure(self):
        r=copy.deepcopy(self.record);r['requires']=['COMPONENT'];self.register(r)
        self.assertEqual(self.select()['status'],'needs_review')
        dep=copy.deepcopy(self.record);dep.update(asset_id='COMPONENT',kind='equipment',entity_id='HOOK',stage=None)
        self.register(dep);receipt=self.select();self.assertEqual(receipt['status'],'matched');self.assertEqual(len(receipt['records']),2)

    def test_dependency_cycles_rejected(self):
        r=copy.deepcopy(self.record);r['requires']=['DEP'];self.register(r)
        dep=copy.deepcopy(self.record);dep.update(asset_id='DEP',requires=['REF-FISH-01']);self.register(dep)
        with self.assertRaises(ValueError):self.select()

    def test_reference_edit_invalidates_receipt(self):
        first=self.register();receipt=self.select();r=copy.deepcopy(self.record);r['view']='other';self.register(r,first['record_sha256'])
        self.assertEqual(assets.verify(self.root,receipt)['status'],'stale')

    def test_file_edit_no_longer_matches_without_changing_catalog(self):
        self.register();receipt=self.select();self.file.write_bytes(b'changed')
        self.assertEqual(assets.verify(self.root,receipt)['status'],'needs_review')

    def test_modified_receipt_rejected(self):
        self.register();receipt=self.select();receipt['selected_ids']=[]
        with self.assertRaises(ValueError):assets.verify(self.root,receipt)

    def test_changed_review_evidence_no_longer_matched(self):
        self.register();receipt=self.select();self.evidence.write_text('changed')
        self.assertEqual(assets.verify(self.root,receipt)['status'],'needs_review')

    def test_generated_reference_cannot_prove_scale(self):
        r=copy.deepcopy(self.record);r.update(origin='generated',roles=['scale'],size=dict(value=100,unit='cm',basis='source_reported',source='fixture'))
        r['review']['roles']=['scale'];self.register(r)
        receipt=assets.selection(self.root,[dict(entity_id=r['entity_id'],stage='adult',role='scale')],['REF-FISH-01'])
        self.assertEqual(receipt['status'],'needs_review')

    def test_unknown_scale_does_not_prove_size(self):
        r=copy.deepcopy(self.record);r['roles']=['scale'];r['review']['roles']=['scale'];self.register(r)
        receipt=assets.selection(self.root,[dict(entity_id=r['entity_id'],stage='adult',role='scale')],['REF-FISH-01'])
        self.assertEqual(receipt['status'],'needs_review')

    def test_missing_role_review_cannot_pass(self):
        r=copy.deepcopy(self.record);r['roles']=['identity','anatomy'];self.register(r)
        receipt=assets.selection(self.root,[dict(entity_id=r['entity_id'],stage='adult',role='anatomy')],['REF-FISH-01'])
        self.assertEqual(receipt['status'],'needs_review')

    def test_pagination_and_related_changes(self):
        self.register()
        r=copy.deepcopy(self.record);r['asset_id']='REF-FISH-02';second=self.register(r)
        page=assets.query(self.root,self.requests,1);self.assertTrue(page['next_cursor'])
        self.assertEqual(len(assets.query(self.root,self.requests,1,page['next_cursor'])['assets']),1)
        r['view']='other';self.register(r,second['record_sha256'])
        with self.assertRaises(ValueError):assets.query(self.root,self.requests,1,page['next_cursor'])

    def test_unrelated_changes_preserve_query_and_selection(self):
        self.register();receipt=self.select();before=assets.query(self.root,self.requests)
        r=copy.deepcopy(self.record);r.update(asset_id='REF-DEER',entity_id='DEMO-MAMMAL',stage='young');self.register(r)
        self.assertEqual(before,assets.query(self.root,self.requests));self.assertEqual(assets.verify(self.root,receipt)['status'],'matched')

    def test_mammal_young_not_forced_into_fish_stage(self):
        r=copy.deepcopy(self.record);r.update(entity_id='DEMO-MAMMAL',stage='young');self.register(r)
        receipt=assets.selection(self.root,[dict(entity_id='DEMO-MAMMAL',stage='young',role='identity')],['REF-FISH-01'])
        self.assertEqual(receipt['status'],'matched')

    def test_corrupt_metadata_and_future_schema_rejected(self):
        self.register()
        with closing(sqlite3.connect(self.root/assets.CATALOG)) as db:
            db.execute("UPDATE assets SET sha='bad'");db.commit()
        with self.assertRaises(ValueError):assets.query(self.root,self.requests)
        with closing(sqlite3.connect(self.root/assets.CATALOG)) as db:db.execute('PRAGMA user_version=9');db.commit()
        with self.assertRaises(ValueError):assets.query(self.root,self.requests)

    def test_cli_query_no_write_and_bad_json_type(self):
        request=self.root/'request.json';request.write_text(json.dumps(dict(requests=self.requests)))
        command=[sys.executable,str(Path(assets.__file__)),'--root',str(self.root),'query',str(request)]
        result=subprocess.run(command,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
        self.assertFalse((self.root/'.nature-studio').exists());request.write_text('[]')
        result=subprocess.run(command,capture_output=True,text=True);self.assertEqual(result.returncode,1);self.assertNotIn('Traceback',result.stderr)


class AssetContextTests(unittest.TestCase):
    def setUp(self):
        self.fixture=routing_fixtures.RoutingTests();self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        self.root=self.fixture.root
        self.fixture.write('references/image.bin','Synthetic bytes, not actual media')
        self.fixture.write('references/review.md','Synthetic review, no actual QA')
        self.record=dict(asset_id='REF-1',entity_id='DEMO',kind='organism',roles=['identity'],stage='adult',origin='photo',source={'url':None},
             file=dict(path='references/image.bin',sha256=assets.file_hash(self.root/'references/image.bin')),
             review=dict(status='pass',roles=['identity'],evidence=dict(path='references/review.md',sha256=assets.file_hash(self.root/'references/review.md'))))
        assets.register(self.root,self.record);self.requests=[dict(entity_id='DEMO',stage='adult',role='identity')]

    def receipt(self):return assets.selection(self.root,self.requests,['REF-1'])

    def test_packet_view_and_source_floor(self):
        plain=self.fixture.packet();bound=self.fixture.packet(asset_selection=self.receipt())
        self.assertEqual(plain['sources'],bound['sources']);self.assertFalse(ctx.verify(self.root,bound))
        text,receipt=self.fixture.view(bound);self.assertIn('planned_asset_refs',text);self.assertIn('references/image.bin',text)
        self.fixture.write('references/image.bin','changed');self.assertIn('asset_selection',ctx.verify(self.root,bound))

    def test_pending_asset_review_does_not_fake_visual_pass_or_erase_text(self):
        r=copy.deepcopy(self.record);r['review']={'status':'not_checked'}
        first=assets.query(self.root,self.requests)
        with assets.connection(self.root) as db:sha=db.execute('SELECT sha FROM assets').fetchone()[0]
        assets.register(self.root,r,sha);bound=self.fixture.packet(asset_selection=self.receipt())
        self.assertTrue(bound['asset_review_pending']);self.assertFalse(ctx.verify(self.root,bound))
        text,receipt=self.fixture.view(bound);self.assertIn('asset_review_pending',text)

    def test_caption_without_assets_keeps_light_path(self):
        packet=self.fixture.packet(stage='write',mode='caption')
        self.assertNotIn('asset_selection',packet);self.assertFalse(ctx.verify(self.root,packet))


class ProfilePilotTests(unittest.TestCase):
    def test_three_profiles_follow_one_practical_template_with_stable_ids(self):
        import species_profiles
        root=Path(assets.ROOT)
        for name in ('redfish','muskie','walleye'):
            text=(root/f'01-Knowledge/species/{name}.md').read_text(encoding='utf-8')
            for heading in species_profiles.SECTIONS:self.assertIn(heading,text)
            self.assertEqual(species_profiles.json_block(text)['id'],f'K-SP-{name.upper()}-001')
        template=(root/'00-Standards/templates/species-profile.md').read_text(encoding='utf-8')
        for heading in species_profiles.SECTIONS:self.assertIn(heading,template)

    def test_pilots_read_only_selected_species_and_tackle_when_needed(self):
        root=Path(assets.ROOT)
        for species in ('redfish','muskie','walleye'):
            for mode in ('new','revision','reference','caption'):
                for interaction in ('natural','angling'):
                    packet=ctx.packet(root,'underwater',mode,[species],interaction,stage='all')
                    paths={r['path'] for r in packet['sources']}
                    selected={p for p in paths if p.startswith('01-Knowledge/species/')}
                    self.assertEqual(selected,set() if mode=='caption' else {f'01-Knowledge/species/{species}.md'})
                    self.assertEqual('01-Knowledge/equipment/us-angling-tackle.md' in paths,mode!='caption' and interaction=='angling')
                    modules={p for p in paths if p.startswith('01-Knowledge/equipment/species/')}
                    self.assertEqual(modules,{f'01-Knowledge/equipment/species/{species}-angling.md'} if mode!='caption' and interaction=='angling' else set())
                    for row in packet['sources']:self.assertEqual(row['text'],(root/row['path']).read_bytes().decode('utf-8-sig'))
                    self.assertFalse(ctx.verify(root,packet))


if __name__=='__main__':unittest.main()
