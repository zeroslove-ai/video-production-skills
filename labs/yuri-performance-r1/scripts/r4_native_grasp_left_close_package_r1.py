"""Separate camera-only companion; preserve closed original motion packet."""
from pathlib import Path
import json,hashlib,zipfile
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];P=B/'alpha-native-grasp-left-close-r1';D=B/'alpha-native-grasp-left-close-delivery-r1';E=L/'evidence/alpha-native-grasp-left-close-r1';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
c=load(B/'alpha-native-grasp-left-close-restore-r1b/LEFT_ACTIVE_HAND_CAMERA_RECEIPT_R1B.json');u=load(D/'WHOLE_1X_UI_QA_R1.json');v=load(D/'LEFT_ACTIVE_HAND_VISUAL_QA_R1.json');g=load(B/'o1-native-grasp-left-close-restore-r1b/NATIVE_GUARD_RESULT.json');old=load(L/'evidence/alpha-native-grasp-source-r1/PRIVATE_PACKET_RECEIPT_R1.json')
assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and c['original_OFF_snapshot_restored'] and not c['motion_changed']
assert u['end'][0]['ended'] and u['end'][0]['playbackRate']==1 and u['end'][0]['error'] is None
assert sha(old['file'])==old['SHA']=='9d23f40e7ebdb812edd939eed61fd017427d4ba02bdadcd88d5bffcc43bc74ec'
summary={k:x for k,x in c.items() if k!='camera_frames'};summary.update({'visual_QA':v,'actual_whole1x':u,'original_packet_unchanged':old,'native_guard':{'SHA':sha(B/'o1-native-grasp-left-close-restore-r1b/NATIVE_GUARD_RESULT.json'),'status':g['guard_status']},'TierP':0,'Unity_Laptop_Talk':'Independent sole Laptop lane; not blocked by source grasp visual research'})
write(E/'LEFT_ACTIVE_HAND_QA_MANIFEST_R1.json',summary)
(E/'YURI_R4_GRASP_LEFT_ACTIVE_HAND_QA_R1.md').write_text('''# Grasp original LEFT active-hand camera supplement

Same immutable candidate89a3a8ca, pure Action librarya2808d19 and source169frames24fps. No motion, rig, geometry, weights, material, light, expression, driver, exporter or physics-prop changes. Existing closed packet9d23f40e is unchanged. Additional512-square CPU8-sample close follows LEFT wrist world translation only, with constant world target offset and fixed camera rotation. Full body/root/foot verdict stays exclusively on prior fixed front/waist and actual all-frame world/geometry QA.

Entire169-frame7.041667sec movie encoded/full decoded/actually1x played through-end, supplemented by complete169-frame grid. Original LEFT gesture raises forearm and curls fingers loosely; long hold then return is readable. Thumb remains lateral/open and does not visibly oppose finger pads to form a secure grip. Loose partial curl is not a closed grasp. GRIP/THUMB VISUAL FAIL/HOLD; source technical and dominant-weight hand-body/head/hair/interdigit surface subset remain PASS. No gross hand-body crossing observed in this camera, but weak webbing, digit-palm adjacency and physical contact are not certified. Original neutral geometry at endpoints remains exact under prior fresh-source proof; close playback visibly returns open hand. No physical grasp/prop or acting/Unity/TierP approval.

Next one correction hypothesis, not executed: in a separate additive source Action COPY, adjust existing LEFT thumb opposition relative to existing finger curl during hold, preserve wrist/body/timing and original Action, then test same native axes and actual digit-palm/webbing/contact/1x close. Do not treat source-channel motion or triangle0 as grip quality. Root's sole Laptop grounded Talk implementation continues independently.

First broker invocation had wrong cwd and could not resolve a relative pinned file BEFORE native launch; same unchanged exact config/collector was then invoked from repository cwd. No native job was interrupted/restarted and Original renderer completed169 frames but payload OFF assertion failed because transient render settings were not restored; failure kept. R1b no-render replay isolated scene-only differences and restored full signature0, pinned169 finished render bytes unchanged; new strict guard PASS. No guard failure waived. This supplemental private camera packet contains movie/grid/camera metadata/workflow/guard/QA and exact pointer to original motion packet, not a regenerated character or export.
''',encoding='utf-8')
files={}
def add(p,n):p=Path(p);assert p.is_file() and n not in files;files[n]=p
for f in D.iterdir():
    if f.is_file():add(f,'review/'+f.name)
add(B/'alpha-native-grasp-left-close-restore-r1b/LEFT_ACTIVE_HAND_CAMERA_RECEIPT_R1B.json','private-camera/LEFT_ACTIVE_HAND_CAMERA_RECEIPT_R1.json')
for f in E.iterdir():add(f,'metadata/'+f.name)
for run in ['o1-native-grasp-left-close-r1','o1-native-grasp-left-close-restore-r1b']:
    for f in (B/run).rglob('*'):
        if f.is_file():add(f,'native-custody/'+run+'/'+f.relative_to(B/run).as_posix())
add(B/'alpha-native-grasp-left-close-restore-r1b/RESTORATION_DIFFERENCE_R1B.json','private-camera/RESTORATION_DIFFERENCE_R1B.json')
add(P/'COMPLETED_RENDER_SHA_INDEX_R1.json','private-camera/COMPLETED_RENDER_SHA_INDEX_R1.json')
for f in (L/'scripts').glob('r4_native_grasp_left_close*.py'):add(f,'workflow/'+f.name)
for n in ['r4_native_grasp_adapter_r1.py','r4_appearance_adapter.py','r4_appearance_signature.py']:add(L/'scripts'/n,'workflow/'+n)
idx={n:{'bytes':f.stat().st_size,'SHA':sha(f)} for n,f in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R1.json';write(ip,idx);add(ip,ip.name);zp=B/'YURI_R4_GRASP_LEFT_ACTIVE_HAND_CAMERA_QA_R1_20261005.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,f in sorted(files.items()):z.write(f,n)
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    for n,x in idx.items():raw=z.read(n);assert len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['SHA']
    receipt={'file':str(zp),'SHA':sha(zp),'bytes':zp.stat().st_size,'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all':'PASS','original_motion_packet_SHA':old['SHA'],'candidate_SHA':c['candidate_SHA'],'source_SHA':c['source_SHA'],'motion_changed':False,'visual_grasp':'FAIL/HOLD: thumb opposition missing, partial loose curl','technical_surface_subset':'PASS; no physics claim','TierP':0};write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);print(json.dumps(receipt,indent=2))
