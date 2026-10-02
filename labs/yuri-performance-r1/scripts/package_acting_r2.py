"""CPU H.264 encoding, camera contacts and review HTML; no model generation."""
from pathlib import Path
import subprocess,json,hashlib,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/acting-r2';E=ROOT/'evidence/acting-r2'
FFMPEG=shutil.which('ffmpeg');FFPROBE=shutil.which('ffprobe')
if not FFMPEG or not FFPROBE:raise RuntimeError('Use the already installed FFmpeg runtime')
records=[];contacts=[]
completed=json.loads((E/'render_jobs.json').read_text()) if (E/'render_jobs.json').exists() else {'jobs':{}}
for clip in ('greeting_wave','shy_lookaway','please_tilt'):
    for variant in ('natural','exaggerated_head','simultaneous'):
        for camera in ('full_body','waist_threequarter','face_close','hand_face','vertical'):
            d=OUT/clip/variant/camera
            if not d.exists():continue
            key=f'{clip}__{variant}__{camera}'
            if completed['jobs'].get(key,{}).get('returncode')!=0:continue
            if completed['jobs'][key]['candidate_sha256']!=completed['candidate_sha256']:continue
            frames=sorted(d.glob('*.png'))
            contact=Image.new('RGB',(640*4,385*2),'#252934');draw=ImageDraw.Draw(contact)
            for i,f in enumerate((1,13,25,43,61,85,109,121)):
                p=d/f'{f:04d}.png'
                if not p.exists():continue
                im=Image.open(p).convert('RGB');im.thumbnail((640,360));x=(i%4)*640;y=(i//4)*385
                contact.paste(im,(x,y));draw.text((x+8,y+362),f'{clip} / {variant} / {camera} f{f} t={(f-1)/24:.2f}s',fill='white')
            name=f'{clip}__{variant}__{camera}'
            contact.save(OUT/(name+'_contact.jpg'),quality=88)
            contacts.append(OUT/(name+'_contact.jpg'))
            if not all((d/f'{f:04d}.png').exists() for f in range(1,122)):continue
            mp4=OUT/(name+'.mp4')
            subprocess.run([FFMPEG,'-y','-framerate','24','-start_number','1','-i',str(d/'%04d.png'),'-frames:v','120','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True,capture_output=True)
            info=json.loads(subprocess.check_output([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',str(mp4)]))
            stream=info['streams'][0]
            assert abs(float(info['format']['duration'])-5)<.01 and stream['avg_frame_rate']=='24/1'
            records.append({'clip':clip,'variant':variant,'camera':camera,'file':mp4.name,'sha256':hashlib.sha256(mp4.read_bytes()).hexdigest(),'duration_seconds':5,'fps':24,'width':stream['width'],'height':stream['height'],'codec':stream['codec_name'],'audio':'INTENTIONALLY_SILENT','classification':'BLENDER_PROXY_REFERENCE_NOT_AI_VIDEO_NOT_YURI_3D_ANIMATION'})
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>Yuri Acting R2 — Desktop R&D</title><style>body{background:#20242d;color:#eee;font:16px system-ui;max-width:1200px;margin:auto;padding:24px}video,img{max-width:100%;width:720px}section{margin:30px 0}a{color:#aacbff}</style><h1>Desktop Acting R2</h1><p>Original R1 proxy extended for semantic acting/timing. 실제 Yuri 얼굴/손 품질 승인이 아닙니다. CPU Blender renders, 24fps / 1x. AI video inference 없음.</p><p>Anticipation 0–.65 → motion .65–1.55 → emotional peak 1.55–2.2 → hold 2.2–3 → follow-through 3–3.75 → recovery 3.75–5s. 다섯 카메라는 같은 연기 데이터입니다.</p>'''
for r in records:
    label=f'{r["clip"]} / {r["variant"]} / {r["camera"]}'
    html+=f'<section><h2>{label}</h2><video controls preload="metadata" src="{r["file"]}"></video><p><button onclick="const v=this.closest(\'section\').querySelector(\'video\');v.currentTime=0;v.playbackRate=1;v.play()">Play 1x: {label}</button></p><p>5s, 24fps, {r["width"]}×{r["height"]}</p></section>'
html+='<h2>Representative contacts</h2>'
for p in contacts:html+=f'<details><summary>{p.stem}</summary><img src="{p.name}"></details>'
html+='</html>';(OUT/'REVIEW_ACTING_R2.html').write_text(html,encoding='utf-8')
(E/'video_delivery.json').write_text(json.dumps({'videos':records,'count_is_derived_previs_not_completed_performances':True},indent=2))
print('PACKAGE_R2_PASS',len(records))
