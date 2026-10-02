import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('pipeline', ROOT / 'tools/previz/pipeline.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.m = p.manifest(ROOT / 'examples/previz/shot.json')

    def test_graph_references_and_binding(self):
        graph = p.bind(p.read(ROOT / 'workflows/previz/wan22_fun_control.api.json'), self.m)
        self.assertEqual(graph['10']['inputs']['length'], 81)
        self.assertEqual(graph['13']['inputs']['noise_seed'], 101)
        self.assertNotIn('"$', json.dumps(graph))
        for node in graph.values():
            for value in node['inputs'].values():
                if isinstance(value, list):
                    self.assertIn(value[0], graph)
        self.assertEqual(graph['10']['inputs']['control_video'], ['7', 0])
        self.assertEqual(graph['10']['inputs']['ref_image'], ['5', 0])
        self.assertNotIn('start_image', graph['10']['inputs'])

    def test_missing_model_prevents_submission(self):
        graph = {'1': {'class_type': 'UNETLoader', 'inputs': {'unet_name': 'missing.safetensors'}}}
        with self.assertRaisesRegex(ValueError, 'unavailable'):
            p.preflight(graph, {'UNETLoader': {'input': {'required': {'unet_name': [['other.safetensors']]}}}})
        with self.assertRaisesRegex(ValueError, 'missing node'):
            p.preflight(graph, {})

    def test_asset_tamper_and_smoke_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a = Path(d)
            (a / 'first.png').write_bytes(b'fixture')
            p.write(a / 'scene-state.json', {k: self.m[k] for k in ['width', 'height', 'fps', 'frame_count']})
            p.write(a / 'assets.json', {'shot_id': self.m['shot_id'], 'smoke': True,
                'sha256': {'first.png': p.hashlib.sha256(b'fixture').hexdigest()}})
            p.verify_assets(self.m, a)
            with self.assertRaisesRegex(ValueError, 'Incomplete'):
                p.verify_assets(self.m, a, live=True)
            hashes = {}
            for name in ['beauty.mp4', 'depth.mp4', 'reference-video.mp4', 'first.png', 'last.png', 'previz.blend']:
                (a / name).write_bytes(b'fixture')
                hashes[name] = p.hashlib.sha256(b'fixture').hexdigest()
            hashes['scene-state.json'] = p.hashlib.sha256((a / 'scene-state.json').read_bytes()).hexdigest()
            p.write(a / 'assets.json', {'shot_id': self.m['shot_id'], 'smoke': True, 'sha256': hashes})
            with self.assertRaisesRegex(ValueError, 'Smoke'):
                p.verify_assets(self.m, a, live=True)
            (a / 'first.png').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                p.verify_assets(self.m, a)

    def test_reference_provider_requires_real_urls(self):
        with self.assertRaisesRegex(ValueError, 'requires hosted'):
            p.fal_payload(self.m, '.', 'seedance2')
        self.m['reference_images'] = ['https://example.com/character.png']
        self.m['reference_video_url'] = 'https://example.com/previz.mp4'
        payload = p.fal_payload(self.m, '.', 'seedance2')
        self.assertIn('@Video1', payload['prompt'])
        self.assertNotIn('seed', payload)  # Not in the inspected Seedance2 schema.
        self.assertEqual(payload['duration'], '5')
        self.m['reference_images'] = ['file:///private.png']
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            p.fal_payload(self.m, '.', 'seedance2')

    def test_fal_status_never_sends_key_to_foreign_host(self):
        with patch.dict(p.os.environ, {'FAL_KEY': 'test-only'}):
            with self.assertRaisesRegex(ValueError, 'Unexpected'):
                p.fal_status({'status_url': 'https://evil.invalid', 'response_url': 'https://queue.fal.run/a'})

    def test_preflight_accepts_pending_upload_names(self):
        graph = {'1': {'class_type': 'LoadVideo', 'inputs': {'file': 'new-run/depth.mp4'}}}
        p.preflight(graph, {'LoadVideo': {'input': {'required': {'file': [['old.mp4']]}}}})

    def test_seedance25_uses_reference_task(self):
        self.m['reference_video_url'] = 'https://example.com/reference.mp4'
        payload = p.fal_payload(self.m, '.', 'seedance25')
        self.assertEqual(payload['task'], 'reference')
        self.assertEqual(payload['video_urls'], [self.m['reference_video_url']])

    def test_frame_layout_rejected_before_ffmpeg(self):
        with tempfile.TemporaryDirectory() as d:
            a = Path(d)
            p.write(a / 'scene-state.json', {'frame_count': 9})
            (a / 'beauty').mkdir()
            with self.assertRaisesRegex(ValueError, 'Missing'):
                p.prepare(self.m, a)


if __name__ == '__main__':
    unittest.main()
