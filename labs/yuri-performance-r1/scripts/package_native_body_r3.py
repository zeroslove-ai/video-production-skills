"""Verified contact sheets first; completed movie jobs only, no stale candidate reuse."""
from pathlib import Path
import json,hashlib,subprocess,shutil,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];folder='native-camera-r4' if 'camera_r4' in sys.argv else 'native-body-r3-please-elbow' if 'please_elbow' in sys.argv else 'native-body-r3-please-hands' if 'please_hands' in sys.argv else 'native-body-r3';OUT=ROOT/('local/'+folder);E=ROOT/('evidence/'+folder);meta=json.loads((E/'build_receipt.json').read_text());candidate=Path(meta['candidate'])
assert hashlib.sha256(candidate.read_bytes()).hexdigest()==meta['candidate_sha256']
qa=json.loads((E/'structural_qa.json').read_text());assert qa['candidate_sha256']==meta['candidate_sha256'] and all(c['technical']=='PASS' for c in qa['clips'])
records=[]
jobs=json.loads((E/'video_jobs.json').read_text())['jobs'] if (E/'video_jobs.json').exists() else {}
movies=[]
for clip in meta['action_registry']:
    for view in ('full_body','waist_threequarter','hand_face','face_close','vertical'):
        d=OUT/clip/view;frames=[d/f'{f:04d}.png' for f in (1,25,49,73,97,121)]
        if not all(p.exists() for p in frames):continue
        assert all(p.stat().st_mtime>=candidate.stat().st_mtime for p in frames),'Archive old-candidate renders before reuse'
        im=Image.new('RGB',(1920,770),'#20242d');draw=ImageDraw.Draw(im)
        for i,p in enumerate(frames):
            tile=Image.open(p).convert('RGB');tile.thumbnail((640,360));x=i%3*640;y=i//3*385;im.paste(tile,(x,y));draw.text((x+6,y+362),f'{clip}/{view} f{p.stem} t={(int(p.stem)-1)/24:.2f}s',fill='white')
        contact=OUT/f'{clip}__{view}_contact.jpg';im.save(contact,quality=91)
        records.append({'clip':clip,'camera':view,'contact':str(contact),'candidate_sha256':meta['candidate_sha256'],'frames':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in frames]})
        key=f'{clip}__{view}'
        if jobs.get(key,{}).get('returncode')!=0 or jobs[key]['candidate_sha256']!=meta['candidate_sha256']:continue
        assert all((d/f'{f:04d}.png').exists() for f in range(1,122))
        mp4=OUT/(key+'.mp4')
        subprocess.run([shutil.which('ffmpeg'),'-y','-framerate','24','-start_number','1','-i',str(d/'%04d.png'),'-frames:v','120','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],capture_output=True,check=True)
        probe=json.loads(subprocess.check_output([shutil.which('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(mp4)]));assert abs(float(probe['format']['duration'])-5)<.01
        movies.append({'clip':clip,'camera':view,'file':mp4.name,'duration':5,'fps':24,'width':probe['streams'][0]['width'],'height':probe['streams'][0]['height'],'sha256':hashlib.sha256(mp4.read_bytes()).hexdigest()})
(E/'contact_delivery.json').write_text(json.dumps({'contacts':records,'classification':'PRIVATE_NATIVE_BODY_REFERENCE_FACE_NEUTRAL_NO_PRODUCT_APPROVAL'},indent=2))
(E/'video_delivery.json').write_text(json.dumps({'videos':movies,'actual_yuri_approved_performances':0},indent=2))
html='<!doctype html><html lang="ko"><meta charset="utf-8"><title>Native Body R3 research</title><style>body{font:16px system-ui;background:#20242d;color:#eee;max-width:1100px;margin:auto;padding:24px}img,video{max-width:100%;width:900px}section{margin:24px 0}</style><h1>R2 native body timing R3</h1><p>Private research source reference. Face neutral: A/O gate failed. Original 66 actions/mesh/skin/rest rig fingerprints preserved. 실제 완성 Yuri animation 또는 product integration 아님.</p>'
for r in movies:
    label=f'{r["clip"]} / {r["camera"]}'
    html+=f'<section><h2>{label}</h2><video controls src="{r["file"]}"></video><p><button onclick="const v=this.closest(\'section\').querySelector(\'video\');v.currentTime=0;v.playbackRate=1;v.play()">Play 1x: {label}</button></p></section>'
for r in records:html+=f'<section><h2>{r["clip"]} / {r["camera"]} — contact</h2><img src="{Path(r["contact"]).name}"></section>'
(OUT/'REVIEW_NATIVE_BODY_R3.html').write_text(html+'</html>',encoding='utf-8');print('NATIVE_PACKAGE',len(records),'contacts',len(movies),'movies')
