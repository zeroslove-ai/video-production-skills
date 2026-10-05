"""Readonly source-only residual triage; a contact count is not a visible-defect acceptance."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');R=B/'alpha-tour-clavicle-source-intake-r1';L=Path(__file__).resolve().parents[1];E=L/'evidence/tour-clavicle-source-intake-r1';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
G=B/'o1-tour-clavicle-source-intake-r1/NATIVE_GUARD_RESULT.json';assert json.loads(G.read_bytes())['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
m=json.loads((R/'CLAVICLE_SOURCE_INTAKE_PRIVATE_R1.json').read_bytes());assert m['source81_OFF_restored'] and not m['candidate_created'];E.mkdir(exist_ok=False)
base=np.array(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));assert np.array_equal(base,np.array(Image.open(R/'OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA')))
weights=m['weights_private'];groups={n:sum(w.get(n,0) for w in weights.values()) for n in sorted({n for w in weights.values() for n in w})};adj=[]
for a,b in zip(m['rows_private'],m['rows_private'][1:]):
 if (a['frame'],b['frame'])!=(302,303):continue
 for n in m['rest_constraints_private']:
  x=np.array(a['joint_local_pose_private'][n]['quaternion']);y=np.array(b['joint_local_pose_private'][n]['quaternion']);angle=2*math.degrees(math.acos(min(1,abs(float(x@y)/(np.linalg.norm(x)*np.linalg.norm(y))))));adj.append({'joint':n,'source302_to303_angle_degrees':angle,'position_component_change_m':float(np.max(np.abs(np.array(a['joint_local_pose_private'][n]['location'])-np.array(b['joint_local_pose_private'][n]['location']))))})
images=[]
for view in ['front','quarter']:
 for f in [302,303,337,370]:
  grid=Image.new('RGB',(1536,538),'white');d=ImageDraw.Draw(grid)
  for col,mode in enumerate(['OFF','SOURCE_ON']):
   p=R/f'{view}_{mode}_f{f}.png';expected=next(x for x in m['captures_private'] if x['view']==view and x['mode']==mode and x['frame']==f);assert sha(p)==expected['SHA'];im=Image.open(p).convert('RGB');grid.paste(im,(col*512,26));d.text((col*512+6,6),f'{view} f{f} {mode} natural ORIGINAL materials',fill='black')
  row=next(x for x in m['captures_private'] if x['view']==view and x['mode']=='SOURCE_ON' and x['frame']==f);diagnostic=Image.open(R/f'{view}_SOURCE_ON_f{f}.png').convert('RGB');dd=ImageDraw.Draw(diagnostic)
  for tri,color in zip(m['pair_private'],['red','cyan']):
   pts=[(row['pair_projection_private'][str(i)][0]*512,(1-row['pair_projection_private'][str(i)][1])*512) for i in tri];dd.line(pts+[pts[0]],fill=color,width=2)
  grid.paste(diagnostic,(1024,26));d.text((1030,6),'DIAGNOSTIC pair projection, NO occlusion test',fill='black');out=R/f'MATCHED_{view}_f{f}_SOURCE_INTAKE.jpg';grid.save(out,quality=96);images.append({'path':str(out),'SHA':sha(out)})
q={'source_SHA':m['source_SHA'],'native_source_candidate_SHA':m['source_native_candidate_SHA'],'guard_status':'PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN','guard_SHA':sha(G),'private_intake_SHA':sha(R/'CLAVICLE_SOURCE_INTAKE_PRIVATE_R1.json'),'sampled_actual_geometry_matches_previous_source':True,'sampled_frames':[r['frame'] for r in m['rows_private']],'six_vertex_aggregate_weights':groups,'first_failure_neighbor_local_joint_differences':adj,'source_modifier_types':[x.get('type') for x in m['modifiers_private']],'source81_OFF_restored':True,'neutral_RGBA_difference':0,'natural_stills':images,'candidate_created':False,'visible_specific_pair_defect':'UNCONFIRMED: natural front/quarter close stills do not isolate the interior pair as an obvious break. Projected outlines are localization only, without occlusion/depth proof.','first_adapter_difference':'NONE: exact old source actual geometry hashes match at all 9 sampled frames; C2 residual vertex difference0 at303/337 already witnessed.','root_cause':'UNRESOLVED: original source animation plus existing skin deformation, not proven individual joint/weight/modifier defect.','decision':'Keep strict contact HOLD; no clavicle candidate or elbow C3 without direct visible defect and causal evidence.','TierP':0,'Unity_F2_StageB':'UNTESTED'}
(E/'CLAVICLE_SOURCE_SCALAR_TRIAGE_R1.json').write_text(json.dumps(q,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>R4 source clavicle intake</title><style>body{background:#222;color:#eee;font:16px system-ui}img{width:100%;max-width:1536px}</style><h1>R4 source clavicle residual · readonly intake</h1><p>OFF / SOURCE ON / projected triangle diagnostic. Same original materials and camera per view. Static triage only; no new animation or visual PASS. Specific pair visibility remains UNCONFIRMED, strict contact HOLD preserved. Diagnostic projection does not test occlusion or penetration depth.</p>'
for x in images:html+=f'<img src="{Path(x["path"]).name}">'
(R/'REVIEW_CLAVICLE_SOURCE_INTAKE_R1.html').write_text(html,encoding='utf8')
(E/'YURI_R4_CLAVICLE_SOURCE_INTAKE_R1_KO.md').write_text('''# R4 원본 쇄골 교차 읽기 전용 검수

C2의 다음 미완료 source defect로 쇄골 교차 1쌍을 선택해 확인했다. **실제 보이는 해당 결함은 미확인, 후보 생성0, strict contact HOLD 유지**다. 팔꿈치 C3나 가중치/rig/외형 수정은 수행하지 않았다.

기존 source81 Action 후보와 immutable R4 source를 그대로 사용했다. 1/289/302/303/337/370/371/385/472의 실제 BODY/HEAD/HAIR geometry SHA는 기존 원본 ledger와 모두 동일하다. source 내부에 이미 있는 교차이며 adapter 첫 차이는 없다. 최초 교차 직전302와303의 clavicle.L/neck/upper_arm.L local pose 변화, 해당6 vertex의 원본 skin weights, 원본 modifier/constraints/rest 근거를 private intake에 보존했다. 여러 관절의 동시 skin deformation이므로 한 관절이나 weight/modifier를 원인으로 단정하지 않는다.

정면/3⁄4의 OFF/ON을 원래 재질 그대로 302/303/337/370에서 같은 카메라로 렌더했다. 자연 화면에서 목·어깨 실루엣의 뚜렷한 파손이나 해당 내부 쌍만의 defect를 분리하지 못했다. 3번째 diagnostic pane은 두 triangle의 투영 위치만 표시하며 visibility/occlusion/depth 증거가 아니다. 스틸 검사이며 새 정상속도 PASS로 세지 않는다. C2 97프레임 전체1x 비교 근거는 기존 checkpoint8ea4766에 남아 있다.

읽기 전용 job은 CPU2/4GiB/600초/64MiB 및 strict live identity·terminal drain을 유지해 PASS. source81/OFF/signature와 source bytes를 복구했고 neutral RGBA 차이0이다. 새 candidate, export, product/Unity/OS/GPU 변경은 없다. TierP0, Unity/F2/StageB 미검증.

다음 방향은 해당 쌍의 원본 가시성과 원인을 증명할 때만 별도 관절 Action 후보를 하나 만드는 것이다. 검증 없이 쇄골을 재가중하거나 팔꿈치를 더 줄이지 않는다. 전체Tour 손목/head/hair HOLD도 유지한다.

Local review: '''+str(R/'REVIEW_CLAVICLE_SOURCE_INTAKE_R1.html')+'\n',encoding='utf8')
print('CLAVICLE_SOURCE_READONLY_TRIAGE_NO_CANDIDATE_VISIBLE_DEFECT_UNCONFIRMED')
