import base64
import importlib.util
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
import urllib.error
from unittest import mock

SPEC = importlib.util.spec_from_file_location('image_9router',Path(__file__).resolve().parents[1]/'image_9router.py')
r9 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r9)

PNG = b'\x89PNG\r\n\x1a\n' + struct.pack('>I',13) + b'IHDR' + struct.pack('>II',1024,1536) + b'rest'


class Response(io.BytesIO):
    status = 200
    def __enter__(self): return self
    def __exit__(self, *exc): return False


class Image9RouterTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        (self.root/'.nature-studio').mkdir()
        (self.root/r9.KEY_FILE).write_text('sk-test\n')
        self.prompt = self.root/'prompt.txt'
        self.prompt.write_text('A clownfish in an anemone, vertical 2:3 composition')
        self.ref = self.root/'ref.png'
        self.ref.write_bytes(PNG)
        self.sent = []
        patcher = mock.patch.dict('os.environ',{'NINEROUTER_API_KEY':''})
        patcher.start();self.addCleanup(patcher.stop)

    def opener(self, payload):
        def fake(request, timeout):
            self.sent.append((request, json.loads(request.data)))
            if isinstance(payload, Exception): raise payload
            return Response(json.dumps(payload).encode())
        return fake

    def test_success_writes_image_and_record_without_key(self):
        out = self.root/'A01/out.png'
        result = r9.generate(self.root,self.prompt,out,[self.ref],'1024x1536',
                             opener=self.opener({'data':[{'b64_json':base64.b64encode(PNG).decode()}]}))
        request, body = self.sent[0]
        self.assertEqual(body['model'],'cx/gpt-image-2.5-sunburst')
        self.assertEqual(len(body['images']),1)
        self.assertEqual(request.get_header('Authorization'),'Bearer sk-test')
        self.assertEqual((result['outcome'],result['width'],result['height']),('success',1024,1536))
        record = json.loads(Path(result['record']).read_text())
        self.assertEqual(record['actual_model'],'unknown')
        self.assertFalse(record['model_verified'])
        self.assertEqual(record['tool']['arguments']['referenced_image_paths'],[str(self.ref)])
        self.assertNotIn('sk-test',Path(result['record']).read_text())
        self.assertEqual(out.read_bytes(),PNG)

    def test_never_overwrites(self):
        out = self.root/'out.png'
        out.write_bytes(b'old')
        with self.assertRaises(ValueError):
            r9.generate(self.root,self.prompt,out,opener=self.opener({}))
        self.assertEqual(self.sent,[])

    def test_http_error_recorded_as_error(self):
        error = urllib.error.HTTPError('u',429,'busy',{},io.BytesIO(b'{"error":"rate"}'))
        result = r9.generate(self.root,self.prompt,self.root/'e.png',opener=self.opener(error))
        self.assertEqual((result['outcome'],result['http_status']),('error',429))
        self.assertFalse((self.root/'e.png').exists())

    def test_timeout_is_unknown_outcome(self):
        result = r9.generate(self.root,self.prompt,self.root/'t.png',opener=self.opener(TimeoutError('timed out')))
        self.assertEqual(result['outcome'],'unknown')

    def test_warns_when_prompt_lacks_orientation(self):
        self.prompt.write_text('A clownfish in an anemone')
        result = r9.generate(self.root,self.prompt,self.root/'w.png',size='1024x1536',
                             opener=self.opener({'data':[{'b64_json':base64.b64encode(PNG).decode()}]}))
        self.assertTrue(result['warnings'])

    def test_missing_key(self):
        (self.root/r9.KEY_FILE).unlink()
        with self.assertRaises(ValueError):
            r9.generate(self.root,self.prompt,self.root/'k.png',opener=self.opener({}))


if __name__ == '__main__':
    unittest.main()
