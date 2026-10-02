"""Dependency-free asset packaging and ComfyUI/fal REST adapters. No submission retries."""
import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
FAL_MODELS = {
    'seedance15': 'fal-ai/bytedance/seedance/v1.5/pro/image-to-video',
    'seedance2': 'bytedance/seedance-2.0/reference-to-video',
    'seedance25': 'bytedance/seedance-2.5/reference-to-video',
}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def manifest(path):
    m = read(path)
    if m.get('schema_version') != 1 or not re.fullmatch(r'[A-Za-z0-9_-]+', m.get('shot_id', '')):
        raise ValueError('Invalid schema_version or shot_id')
    if not isinstance(m.get('prompt'), str) or not m['prompt'].strip():
        raise ValueError('Nonempty prompt required')
    for key in ['width', 'height', 'fps', 'frame_count', 'provider_duration_seconds']:
        if type(m.get(key)) is not int or m[key] <= 0:
            raise ValueError(f'{key} must be a positive integer')
    if m['width'] % 16 or m['height'] % 16 or m['frame_count'] % 4 != 1:
        raise ValueError('Wan dimensions must be multiples of 16; frame_count must be 4n+1')
    if not 4 <= m['provider_duration_seconds'] <= 12:
        raise ValueError('Shared Seedance duration range is 4..12')
    if not 0 < m.get('depth_near', 0) < m.get('depth_far', 0):
        raise ValueError('Require 0 < depth_near < depth_far')
    if type(m.get('seed')) is not int or not 0 <= m['seed'] < 2**31:
        raise ValueError('Shared seed must be an integer in 0..2^31-1')
    return m


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames',
        '-show_streams', '-show_format', '-of', 'json', str(path)], text=True))


def prepare(m, assets):
    assets = Path(assets)
    state = read(assets / 'scene-state.json')
    count = state['frame_count']
    for stream in ['beauty', 'depth']:
        expected = [assets / stream / f'{i:04d}.png' for i in range(1, count + 1)]
        if len(list((assets / stream).glob('*.png'))) != count or not all(p.is_file() for p in expected):
            raise ValueError(f'Missing or surplus {stream} frames')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate',
            str(state['fps']), '-start_number', '1', '-i', str(assets / stream / '%04d.png'),
            '-frames:v', str(count), '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
            str(assets / f'{stream}.mp4')], check=True)
    shutil.copyfile(assets / 'beauty' / '0001.png', assets / 'first.png')
    shutil.copyfile(assets / 'beauty' / f'{count:04d}.png', assets / 'last.png')
    # External reference-video limits differ from local Wan conditioning. Preserve
    # composition with padding and resample to 24 fps, without speed changes.
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i',
        str(assets / 'beauty.mp4'), '-vf',
        'scale=640:640:force_original_aspect_ratio=decrease,pad=640:640:(ow-iw)/2:(oh-ih)/2,fps=24',
        '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
        str(assets / 'reference-video.mp4')], check=True)
    files = ['beauty.mp4', 'depth.mp4', 'reference-video.mp4', 'first.png', 'last.png', 'previz.blend', 'scene-state.json']
    result = {'shot_id': m['shot_id'], 'source_duration_seconds': count / state['fps'],
        'provider_duration_seconds': m['provider_duration_seconds'], 'smoke': state['smoke'],
        'sha256': {f: hashlib.sha256((assets / f).read_bytes()).hexdigest() for f in files},
        'ffprobe': {f: probe(assets / f) for f in ['beauty.mp4', 'depth.mp4', 'reference-video.mp4']}}
    for file in ['beauty.mp4', 'depth.mp4']:
        metadata = result['ffprobe'][file]
        video = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
        if int(video['nb_read_frames']) != count or video['width'] != state['width'] or video['height'] != state['height']:
            raise ValueError('Encoded video differs from scene state')
    ref = result['ffprobe']['reference-video.mp4']
    result['reference_video_eligible'] = (2 <= float(ref['format']['duration']) <= 15
        and int(ref['format']['size']) < 50_000_000)
    write(assets / 'assets.json', result)
    return result


def verify_assets(m, assets, live=False):
    assets = Path(assets)
    a = read(assets / 'assets.json')
    state = read(assets / 'scene-state.json')
    if a['shot_id'] != m['shot_id']:
        raise ValueError('Shot id mismatch')
    required = {'beauty.mp4', 'depth.mp4', 'reference-video.mp4', 'first.png', 'last.png', 'previz.blend', 'scene-state.json'}
    if live and not required.issubset(a['sha256']):
        raise ValueError('Incomplete asset inventory')
    for f, digest in a['sha256'].items():
        if hashlib.sha256((assets / f).read_bytes()).hexdigest() != digest:
            raise ValueError(f'Asset hash mismatch: {f}')
    if live and (a['smoke'] or any(state[k] != m[k] for k in ['width', 'height', 'fps', 'frame_count'])):
        raise ValueError('Smoke or mismatched assets cannot be submitted')
    return a


def bind(graph, m):
    values = {'prompt': m['prompt'], 'negative_prompt': m.get('negative_prompt', ''),
              'width': m['width'], 'height': m['height'], 'length': m['frame_count'],
              'fps': m['fps'], 'seed': m['seed'], 'prefix': 'previz/' + m['shot_id'],
              'first': 'previz/' + m['shot_id'] + '/first.png',
              'depth_video': 'previz/' + m['shot_id'] + '/depth.mp4'}
    def replace(value):
        if isinstance(value, dict):
            return {k: replace(v) for k, v in value.items()}
        if isinstance(value, list):
            return [replace(v) for v in value]
        if isinstance(value, str) and value.startswith('$'):
            return values[value[1:]]
        return value
    return replace(copy.deepcopy(graph))


def http(url, body=None, headers=None, method=None):
    req = Request(url, data=body, headers=headers or {}, method=method)
    with urlopen(req, timeout=60) as r:
        return json.load(r)


def json_http(url, data, headers=None):
    return http(url, json.dumps(data).encode(), {'Content-Type': 'application/json', **(headers or {})})


def preflight(graph, info):
    errors = []
    for node_id, node in graph.items():
        cls = node['class_type']
        if cls not in info:
            errors.append(f'{node_id}: missing node {cls}')
            continue
        inputs = info[cls].get('input', {})
        for name, spec in inputs.get('required', {}).items():
            if name not in node['inputs']:
                errors.append(f'{node_id}: missing input {name}')
        for name, value in node['inputs'].items():
            spec = inputs.get('required', {}).get(name, inputs.get('optional', {}).get(name))
            if spec is None:
                errors.append(f'{node_id}: unknown input {name}')
            elif (cls, name) in [('LoadImage', 'image'), ('LoadVideo', 'file')]:
                # Upload follows preflight; these filenames cannot exist in input enums yet.
                # ComfyUI's file validators check existence when the graph is queued.
                continue
            elif isinstance(spec[0], list) and not isinstance(value, list) and value not in spec[0]:
                errors.append(f'{node_id}: unavailable {name}={value}')
    if errors:
        raise ValueError('\n'.join(errors))


def upload(base, path, subfolder):
    boundary = uuid.uuid4().hex
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="subfolder"\r\n\r\n{subfolder}\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\nfalse\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{path.name}"\r\n'
            'Content-Type: application/octet-stream\r\n\r\n').encode() + path.read_bytes() + f'\r\n--{boundary}--\r\n'.encode()
    return http(base + '/upload/image', body, {'Content-Type': f'multipart/form-data; boundary={boundary}'})


def fal_payload(m, assets, model):
    aspect = '16:9' if m['width'] * 9 == m['height'] * 16 else 'auto'
    common = {'prompt': m['prompt'], 'duration': str(m['provider_duration_seconds']),
              'aspect_ratio': aspect, 'resolution': '720p', 'generate_audio': m.get('generate_audio', False)}
    if model == 'seedance15':
        import base64
        common['seed'] = m['seed']
        for field, file in [('image_url', 'first.png'), ('end_image_url', 'last.png')]:
            common[field] = 'data:image/png;base64,' + base64.b64encode((Path(assets) / file).read_bytes()).decode()
    else:
        refs = m.get('reference_images', [])
        video = m.get('reference_video_url')
        if not refs and not video:
            raise ValueError('Seedance2 requires hosted reference_images or reference_video_url')
        if len(refs) > 9 or len(refs) + bool(video) > 12:
            raise ValueError('Seedance2 reference count exceeds documented limits')
        for url in [*refs, *([video] if video else [])]:
            if not isinstance(url, str) or urlparse(url).scheme != 'https' or not urlparse(url).hostname:
                raise ValueError('Reference assets require HTTPS URLs')
        if refs:
            common['image_urls'] = refs
        if video:
            common['video_urls'] = [video]
            common['prompt'] += ' Use @Video1 for motion and camera reference; retain subject identity from @Image1.' if refs else ' Use @Video1 for motion and camera reference.'
        if model == 'seedance25':
            common['task'] = 'reference'
    return common


def fal_status(state):
    token = os.environ.get('FAL_KEY')
    if not token:
        raise ValueError('Set FAL_KEY in the environment')
    for field in ['status_url', 'response_url']:
        url = urlparse(state[field])
        if url.scheme != 'https' or url.netloc != 'queue.fal.run':
            raise ValueError('Unexpected fal queue URL')
    headers = {'Authorization': 'Key ' + token}
    status = http(state['status_url'], headers=headers)
    result = {'status': status}
    if status['status'] == 'COMPLETED':
        result['result'] = http(state['response_url'], headers=headers)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['prepare', 'comfy', 'comfy-status', 'fal', 'fal-status'])
    p.add_argument('--manifest', default=str(ROOT / 'examples/previz/shot.json'))
    p.add_argument('--assets', default='work/previz')
    p.add_argument('--out', required=True, help='New request/evidence JSON file')
    p.add_argument('--base', default='http://127.0.0.1:8188')
    p.add_argument('--model', choices=FAL_MODELS, default='seedance15')
    p.add_argument('--state', help='Previously saved submission state')
    p.add_argument('--submit', action='store_true', help='Explicit live submission, potentially billable')
    args = p.parse_args()
    if Path(args.out).exists():
        raise ValueError('Output already exists; preserve checkpoint and use a new path')
    if args.command == 'fal-status':
        result = fal_status(read(args.state))
    elif args.command == 'comfy-status':
        state = read(args.state)
        result = http(args.base.rstrip('/') + '/history/' + state['prompt_id'])
    else:
        m = manifest(args.manifest)
        if args.command == 'prepare':
            result = prepare(m, args.assets)
        else:
            verify_assets(m, args.assets, live=args.submit)
            if args.command == 'comfy':
                graph = bind(read(ROOT / 'workflows/previz/wan22_fun_control.api.json'), m)
                result = {'mode': 'dry-run', 'prompt': graph}
                if args.submit:
                    base = args.base.rstrip('/')
                    preflight(graph, http(base + '/object_info'))
                    folder = 'previz/' + m['shot_id'] + '/' + uuid.uuid4().hex
                    for file, node_id, field in [('first.png', '5', 'image'), ('depth.mp4', '6', 'file')]:
                        uploaded = upload(base, Path(args.assets) / file, folder)
                        graph[node_id]['inputs'][field] = uploaded['subfolder'] + '/' + uploaded['name']
                    result = json_http(base + '/prompt', {'prompt': graph, 'client_id': uuid.uuid4().hex})
                    if result.get('node_errors') or not result.get('prompt_id'):
                        raise ValueError('ComfyUI rejected graph: ' + json.dumps(result))
                    result['shot_id'] = m['shot_id']
            else:
                payload = fal_payload(m, args.assets, args.model)
                result = {'mode': 'dry-run', 'model': FAL_MODELS[args.model], 'input': payload}
                if args.submit:
                    token = os.environ.get('FAL_KEY')
                    if not token:
                        raise ValueError('Set FAL_KEY in the environment')
                    result = json_http('https://queue.fal.run/' + FAL_MODELS[args.model], payload,
                                       {'Authorization': 'Key ' + token})
                    result['model'] = FAL_MODELS[args.model]
    write(args.out, result)
    print('Saved ' + args.out)


if __name__ == '__main__':
    main()
