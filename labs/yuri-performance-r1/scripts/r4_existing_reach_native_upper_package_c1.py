"""Close one private source-only Reach gate/correction packet; never repack prior ZIPs."""
from pathlib import Path
import json,hashlib,zipfile
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');LAB=Path(__file__).resolve().parents[1];O=B/'c1-existing-reach-native-upper-c1';D=B/'c1-existing-reach-native-upper-delivery-c1';E=LAB/'evidence/existing-reach-contact-closure-r1';E2=LAB/'evidence/existing-reach-native-upper-c1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(p):return json.loads(p.read_bytes())
def write(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
m=js(O/'NATIVE_UPPER_SOURCE_CORRECTION_PRIVATE_C1.json');assert m['verdict']=='SCOPED_ALL61_CONTACT_PASS_VISUAL_PENDING';assert js(D/'OFF_PIXEL_QA_C1.json')['changed_pixels']==0
for run in ['o1-existing-reach-contact-closure-r1','o1-existing-reach-native-upper-c1']:
 g=js(B/run/'NATIVE_GUARD_RESULT.json');assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
E2.mkdir(exist_ok=True)
qa={k:v for k,v in m.items() if k not in ['rows_private','phase_rows']};qa['rows_scalar']=[{k:v for k,v in r.items() if k!='locations_private'} for r in m['rows_private']];qa['retiming_scope']=js(D/'NATIVE_REACH_RETIMING_SCOPE_C1.json');qa['OFF_RGBA_changed_pixels']=0;qa['surface_oracle_limit']='weak ANY relevant weight>.01 nonadjacent triangles versus all body/head/hair; no volume/containment/depth or adjacent deformation certification';qa['visual_verdict']='See full normal-speed and every-frame review receipt';write(E2/'NATIVE_UPPER_SCALAR_QA_C1.json',qa)
# No raw mesh, numeric quaternion motion, triangle identities, pixels or videos enter public Git.
entries={}
def add(p,arc):
 p=Path(p);assert p.is_file() and arc not in entries;entries[arc]=p
add(m['source'],'source/Character_Master_NeckSkin_R4.blend');add(m['candidate'],'candidate/'+Path(m['candidate']).name);add(m['library']['file'],'actions/'+Path(m['library']['file']).name)
for folder,prefix in [(O,'new-native'),(B/'c1-existing-reach-contact-closure-r1','old-gate'),(D,'review'),(E,'public-old-gate'),(E2,'public-new-gate')]:
 for p in folder.rglob('*'):
  if p.is_file() and p.suffix!='.blend':add(p,prefix+'/'+str(p.relative_to(folder)).replace('\\','/'))
for view in ['front','quarter','side']:
 add(B/'alpha-c1-reach-delivery-r1'/f'C1_REACH_RETURN_{view}_1x.mp4',f'old-reference/C1_REACH_RETURN_{view}_1x.mp4')
for run in ['o1-existing-reach-contact-closure-r1','o1-existing-reach-native-upper-c1']:
 for p in (B/run).rglob('*'):
  if p.is_file():add(p,'guards/'+run+'/'+str(p.relative_to(B/run)).replace('\\','/'))
for n in ['r4_existing_reach_contact_closure_r1.py','r4_existing_reach_closure_owned_prepare_r1.py','r4_existing_reach_native_upper_correction_c1.py','r4_existing_reach_upper_correction_owned_prepare_c1.py','r4_existing_reach_native_upper_video_c1.py','r4_existing_reach_native_upper_package_c1.py','r4_appearance_signature.py','r4_appearance_adapter.py']:
 add(LAB/'scripts'/n,'workflow/'+n)
readme=D/'HANDOFF_SOURCE_ONLY_C1.md';readme.write_text('# R4 existing Reach source-only handoff C1\n\nThe immutable source is the visual authority. The new candidate is an animation experiment, not a canonical character or Unity approval. Original78 and prior82 Actions remain unchanged. The library has four Actions and no objects/meshes/armatures. Preserve face/gaze drivers, weights, rest, materials and packed textures.\n\nUse Blender5.2. Open source/Character_Master_NeckSkin_R4.blend and append only the four Action datablocks from actions/. Use workflow/r4_appearance_adapter.py ReactionLane for Meshy_Fitted_Rig, Armature and Hair_Rig_R4 with the mapping in new-native/NATIVE_UPPER_SOURCE_CORRECTION_PRIVATE_C1.json. Assembly_Root uses the existing root Action; save/restore its binding/location too as shown in the collector. Playback frames1..61 at30fps candidate-authored1x; native source phase1..97 at24fps (4.0s endpoint span) is compressed to2.0s, exact2x native speed. Encoded61/30=2.033333s; native inclusive97/24=4.041667s. source scene24fps is preserved. candidate/ opens animation OFF with source appearance. Do not append objects/geometry/materials or reset drivers.\n\nThe original C1 upper path FAIL has left hand/thigh intersections and minority right neck/clavicle intersections. A single source-native-upper reuse removes measured all61 intersections while keeping existing lower/root/actual feet identical. This changes the upper trajectory. New neutral RGBA is byte-decoded exact to source baseline. Full three-view normal-speed and matched old-left/new-right movies are in review/. The old candidate and sealed953b993a packet remain unchanged. No further angle/IK retry was performed.\n\nTriangle contact0 does not certify adjacent skin strain, volume penetration, floor/prop physics, Unity state/time/weight/AlwaysAnimate, Humanoid, MUG/F2/F3 or TierP (0). Research collector guard files retain Desktop absolute pins; portable playback uses this source/library/adapter, without running the research broker. Never overwrite the source or prior checkpoints.\n',encoding='utf8');add(readme,'HANDOFF_SOURCE_ONLY_C1.md')
index={'members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())],'source_sha256':m['source_SHA'],'candidate_sha256':m['candidate_SHA'],'action_sha256':m['library']['sha256'],'closed_once':True,'TierP':0};ip=D/'PACKET_INDEX_C1.json';write(ip,index);add(ip,'PACKET_INDEX_C1.json')
z=B/'YURI_R4_EXISTING_REACH_CONTACT_CLOSURE_SOURCE_C1_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None and len(f.infolist())==len(entries)
 for v in index['members']:
  data=f.read(v['path']);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
receipt={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(index['members']),'CRC_SHA_size_all_verified':True,'closed_once':True,'source_SHA':m['source_SHA'],'candidate_SHA':m['candidate_SHA'],'action_SHA':m['library']['sha256'],'verdict':'SCOPED_SOURCE_CONTACT_OFF_PASS_RUNTIME_HOLD'};write(E2/'PRIVATE_PACKET_RECEIPT_C1.json',receipt);print(json.dumps(receipt,indent=2))
