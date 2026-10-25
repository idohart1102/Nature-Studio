"""Staging geometry arithmetic: frame limits, minor tolerance, visibility, line length, speed, render."""
from pathlib import Path
import sys
import tempfile
import json
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import combo_geometry as cg


def scene(**change):
    data = dict(title='test', visibility_m=2.5, items=[
        dict(name='Shiner', t=0, x=0, y=0.4, z=1.2),
        dict(name='Sinker', t=0, x=0, y=-0.05, z=1.2),
        dict(name='Perch', t=4.2, x=-0.45, y=-0.45, z=1.8),
        dict(name='Perch', t=5.6, x=-0.10, y=-0.25, z=1.25, key=True),
        dict(name='School', t=0, x=[-0.4, 0.4], y=[0.45, 0.75], z=[1.4, 1.9])],
        links=[dict(a='Shiner', b='Sinker', max_m=0.45, label='leader 45 cm')],
        speeds=[dict(item='Perch', max_mps=1.5)])
    data.update(change)
    return data


class GeometryTests(unittest.TestCase):
    def test_valid_scene_passes(self):
        result = cg.check(scene())
        self.assertTrue(result['ok'], result['errors'])

    def test_key_out_of_frame_fails_but_small_overflow_is_minor(self):
        data = scene()
        data['items'][3]['x'] = 0.60
        self.assertTrue(any('frame limit' in e for e in cg.check(data)['errors']))
        data = scene()
        data['items'][2]['x'] = -0.59  # limit 0.558 at z 1.8 -> +6%
        result = cg.check(data)
        self.assertTrue(result['ok'], result['errors'])
        self.assertTrue(any('[minor]' in w for w in result['warnings']))
        data['items'][2]['exits'] = True
        data['items'][2]['x'] = -2.0
        self.assertTrue(cg.check(data)['ok'])

    def test_line_length_speed_and_visibility(self):
        data = scene()
        data['items'][1]['y'] = -0.30
        self.assertTrue(any('leader 45 cm' in e for e in cg.check(data)['errors']))
        data = scene()
        data['items'][2]['t'] = 5.4
        self.assertTrue(any('m/s' in e for e in cg.check(data)['errors']))
        data = scene()
        data['items'][3]['z'] = 3.0
        data['items'][3]['x'] = 0
        data['items'][3]['y'] = 0
        self.assertTrue(any('readable water' in e for e in cg.check(data)['errors']))

    def test_key_required_and_render_writes_table(self):
        data = scene()
        data['items'][3].pop('key')
        self.assertIn('mark the key/payoff', ' '.join(cg.check(data)['errors']))
        text = cg.render(scene(), cg.check(scene()))
        self.assertIn('| Perch | 5.6 | -0.10 | -0.25 | +1.25 |  | KEY |', text)
        self.assertIn('Kiểm số: ĐẠT', text)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'geometry.json'
            path.write_text(json.dumps(scene()), encoding='utf-8')
            self.assertEqual(cg.load(path)['title'], 'test')


if __name__ == '__main__':
    unittest.main()
