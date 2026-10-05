"""Publish scalar C2 evidence and SHA pointers; keep character and motion arrays local."""
from pathlib import Path
import json,hashlib
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];E=L/'evidence/tour302-softcap-c2';E.mkdir(exist_ok=False);D=B/'alpha-tour302-delivery-c2'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((B/'alpha-tour302-softcap-c2/TOUR302_SOFTCAP_C2_PRIVATE.json').read_bytes());rows=m['local_rows_private']
def public(x):
 if isinstance(x,dict):return {k:public(v) for k,v in x.items() if 'private' not in k}
 if isinstance(x,list):return [public(v) for v in x]
 return x
q=public(m);q['local_rows_scalar']=public(rows);q['source_packet_created']=False;q['Unity_F2_StageB']='UNTESTED';q['OFF_RGBA_unequal_channels_each_view']=0
q['BODY_peak_original']=max(x['original_BODY_new_vs_OFF'] for x in rows);q['BODY_peak_candidate']=max(x['BODY_new_vs_OFF'] for x in rows);q['first7_remaining_peak']=max(x['original_first7_remaining'] for x in rows)
q['minimum_actual_triangle_area_ratio']=min(x['minimum_actual_triangle_area_ratio_vs_original'] for x in rows)
q['mean_hand_error_reduction_percent']=100*(1-m['source_pose_deviation_metrics']['source_to_C2_hand_position_error_m']['mean']/m['source_pose_deviation_metrics']['source_to_C1_hand_position_error_m']['mean'])
r=json.loads((B/'alpha-tour302-residual-localize-c2/RESIDUAL_SURFACE_OWNERSHIP_PRIVATE_C2.json').read_bytes());q['residual_first_frame']=303;q['residual_dominant_original_bones']=[x['dominant_original_bones'] for x in r['residual_original_weights_private']];q['residual_vertex_component_error_m']=r['source_to_corrected_pair_vertex_component_error_m'];q['wrist472_actual_all_three_mesh_SHA_same_original']=r['wrist472_actual_all_three_mesh_SHA_same_original']
q['guards']=[]
for n in ['softcap-c2','capture-front-c2','capture-quarter-c2','residual-localize-c2']:
 p=B/f'o1-tour302-{n}/NATIVE_GUARD_RESULT.json';g=json.loads(p.read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';q['guards'].append({'path':str(p),'SHA':sha(p),'status':g['guard_status']})
assert sha(m['candidate'])==m['candidate_SHA'] and m['source_pose_deviation_improved_gate'] and not m['scoped_local_QA_pass']
ui=json.loads((D/'WHOLE_NORMAL1X_UI_C2.json').read_bytes());assert len(ui['videos'])==2 and all(v['ended'] and v['playbackRate']==1 and abs(v['duration']-4.041667)<1e-6 and not v.get('error') for v in ui['videos'])
q['private_custody']=[{'path':str(p),'SHA':sha(p),'bytes':p.stat().st_size} for p in [B/'alpha-tour302-softcap-c2/TOUR302_SOFTCAP_C2_PRIVATE.json',B/'alpha-tour302-softcap-c2/LOCAL_SURFACE_IDENTITIES_PRIVATE_C2.json.gz',B/'alpha-tour302-residual-localize-c2/RESIDUAL_SURFACE_OWNERSHIP_PRIVATE_C2.json',D/'WHOLE_NORMAL1X_UI_C2.json',D/'WHOLE_NORMAL1X_UI_C2.png']]
(E/'TOUR302_SOFTCAP_SCALAR_QA_C2.json').write_text(json.dumps(q,indent=2),encoding='utf8');(E/'VIDEO_CUSTODY_C2.json').write_bytes((D/'VIDEO_CUSTODY_C2.json').read_bytes())
v={'candidate_SHA':m['candidate_SHA'],'native_phrase':[289,385,24],'matched_views':['front','quarter'],'original_C1_capture_reused':True,'C2_only_new_capture':True,'whole_native1x_UI':ui,'visual_observation':'f300/f372 C2 hand silhouette closer to source than C1; f337 same peak correction. Internal clavicle penetration depth not separable by rendered shading. No gross new mesh break in local phrase; no wholeTour acceptance.','review_html':str(D/'REVIEW_TOUR302_SOFTCAP_C2.html'),'actual_UI_screenshot':str(D/'WHOLE_NORMAL1X_UI_C2.png'),'next':'No third amplitude attempt for unchanged clavicle pair; retain C2 as scoped research improvement with wholeTour HOLD.'}
(E/'VISUAL_CLOSURE_C2.json').write_text(json.dumps(v,indent=2),encoding='utf8')
report=f'''# R4 Tour 팔꿈치 C2 국소 연구 결과

원본 외형을 그대로 유지하는 Action 복사본 C2에서 원본 포즈와의 차이를 줄였다. 이는 **국소 개선 후보**이며 `scoped_local_QA_pass=false`, 전체 Tour **HOLD**다. 외형 승격, Unity/F2/StageB/TierP 승인 및 source 배포 패킷은 없다.

## 외형 및 원본 보존

`Character_Master_NeckSkin_R4.blend` SHA `{m['source_SHA']}`를 불변 외형 기준으로 유지했다. 기존 08caad7, R2/R3d, C1 및 기존 자산을 덮어쓰지 않았다. geometry, skin weights, rest pose, materials/nodes/textures, ShapeKeys, face/gaze drivers 및 기존 81 Actions의 서명은 변하지 않았다. C2만 추가된 82-Action 파생본은 기본 OFF 상태로 저장했다. 원본 카메라 neutral RGBA before/after 차이는 두 시점 모두 0이다. donor geometry/새 GameRig/mesh merge는 사용하지 않았다. 기존 Reaction 6개 보존 검증은 `R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md`의 완료 근거를 유지하며 이번 Tour 검사로 Unity 검증을 대체하지 않는다.

## 하나의 보정

forearm.L의 국소 Euler Z 굽힘만 연속 soft cap으로 바꾸었다. 원본 41.255276도 이하는 그대로 두고 41.255276..81.697600도 구간을 61.476438도 상한으로 부드럽게 연결한다. 구간의 미분은 1에서 0으로 연결된다. 작은 굽힘 키 17개와 모든 구간 밖 키/핸들, 나머지 360 curves, 원본 프레임/타이밍을 보존했다. 수정 키는 298..375의 78개다. C1은 참조 Action만 읽고 저장 전에 제거했다.

## 실제 geometry QA

289..385의 정상속도 97프레임과 경계 288/386까지 총 99프레임을 원본/C2 실제 mesh 기준으로 검사했다. 원래 f302 팔꿈치 7쌍은 0, 새로 생긴 6종 교차쌍은 전 프레임 0이다. BODY 교차 최고치는 원본32에서 C2 1로 줄었다. triangle collapse 및 면적 비율 0.1 미만은 0, 최소 면적 비율은 {q['minimum_actual_triangle_area_ratio']:.9f}다. 발/지지 patch 오차, 다른 local joint/비후손 world 오차는 0이며 head/hair geometry도 그대로다.

원본 대비 손 위치 평균 오차: C1 **32.999mm → C2 28.991mm** ({q['mean_hand_error_reduction_percent']:.2f}% 감소). 최대 오차는 **41.993mm로 동일**하다. forearm 평균 각도 오차는 15.8828 → 13.9565도, 최고20.2211도는 동일하다. C2는 원본 움직임과 동일한 motion이라고 주장하지 않는다.

최대 각속도는 원본170.00755 → C2 168.64082도/초. 인접 프레임 각속도 크기 변화 최고34.83920도/초와 경계 속도는 원본과 동일하다. 기존 게이트 정의를 유지했다. subframe/signed acceleration/penetration volume/force 증거는 아니다.

## 정상속도 비교

원본/C1의 종료된 캡처와 MP4를 SHA로 확인해 재사용하고 C2만 동일 카메라·384px·CPU8samples로 새로 렌더했다. 정면/3⁄4 각각 97프레임 24fps, 4.041667초의 왼쪽 원본/중앙 C1/오른쪽 C2 MP4를 만들었다. 전체 디코드 및 실제 UI 버튼 재생 모두 1배속/끝까지/error 없음이다. f300과 f372에서 C2 손 실루엣은 C1보다 원본에 가깝다. 최고 굽힘 f337은 C1/C2가 같다. 렌더 shading만으로 내부 교차 깊이를 분리해 판정하지 않는다.

리뷰: `{D/'REVIEW_TOUR302_SOFTCAP_C2.html'}`
실제 화면: `{D/'WHOLE_NORMAL1X_UI_C2.png'}`

## 남은 결함 및 판정

f303..370의 1쌍은 clavicle.L/neck/upper_arm.L 지배 영역이다. f303/f337의 해당 6개 실제 vertex 좌표는 원본과 오차0이므로 팔꿈치 추가 축소로 해결할 대상이 아니다. f472 손목 및 BODY/HEAD/HAIR 실제 geometry는 원본 그대로다. 전체 Tour의 손목/head/hair HOLD도 유지한다. 후속 C3, rig/weight 변경, exporter, Unity/product 작업은 수행하지 않았다.

candidate SHA: `{m['candidate_SHA']}`
후보: `{m['candidate']}`
C1 checkpoint: `1640066`; 전체 Tour 근거: `9a8595e`.
4개 native job 모두 기존600초/4GiB/2CPU/64MiB/live identity/terminal drain 게이트 PASS. 공개 Git에는 scripts/scalar QA/SHA 포인터만 포함하고 blend/좌표/영상/원본 reference는 넣지 않는다.

StageA 전달 보조는 지원 API 확인 후 중복 대기열을 확인할 수 없어 NO_SEND로 종료했다. Root가 이후 기존 SSH 경로로 동일 MOUTH138 입력을 한 번 전달하고 기존 Laptop thread의 active 새 turn을 확인했다고 회신했다. 이 worker는 별도 메시지/SSH/재전송을 수행하지 않았다.
'''
(E/'YURI_R4_TOUR302_SOFTCAP_C2_KO.md').write_text(report,encoding='utf8')
p=L/'LATEST_RUN.json';j=json.loads(p.read_bytes());j['tour302_softcap_C2']={'status':'SCOPED_SOURCE_DEVIATION_IMPROVEMENT_WHOLE_TOUR_HOLD','candidate_SHA':m['candidate_SHA'],'candidate':m['candidate'],'report':str(E/'YURI_R4_TOUR302_SOFTCAP_C2_KO.md'),'scoped_local_QA_pass':False,'OFF_RGBA_difference':0,'TierP':0};p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf8')
p=L/'CODEX_HANDOFF_KO.md';old=p.read_text(encoding='utf8');p.write_text('# 2026-10-05 Tour C2 corrective checkpoint\n\n'+report.split('## 外形')[0] if False else '# 2026-10-05 Tour C2 corrective checkpoint\n\n원본 외형 및 기존81 Actions 보존, C2 기본 OFF. mean hand error32.999→28.991mm, 새 교차0, 작은 키17개 유지. source deviation subset 개선만 인정; 쇄골1쌍/전체Tour손목·head·hair HOLD. 정상1x 원본/C1/C2 97프레임 두 시점 영상 완료. 상세: evidence/tour302-softcap-c2/YURI_R4_TOUR302_SOFTCAP_C2_KO.md. C1/08caad7 보존. Unity/F2/StageB 미검증, TierP0.\n\n'+old,encoding='utf8')
print('C2_SCALAR_PUBLIC_CLOSURE_COMPLETE')
