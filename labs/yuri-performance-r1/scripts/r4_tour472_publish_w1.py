"""Close ONE failed W1 counterfactual; no failed motion packet or quality promotion."""
from pathlib import Path
import json,hashlib
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];E=L/'evidence/tour472-wrist-w1';E.mkdir(exist_ok=True);D=B/'alpha-tour472-delivery-w1';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((B/'alpha-tour472-wrist-w1b/TOUR472_WRIST_W1_PRIVATE.json').read_bytes())
def public(x):
 if isinstance(x,dict):return {k:public(v) for k,v in x.items() if 'private' not in k}
 if isinstance(x,list):return [public(v) for v in x]
 return x
q=public(m);q['rows_scalar']=public(m['rows_private']);q['source_quality']='FAIL_HOLD_DEFAULT_OFF';q['source_packet_created']=False;q['candidate_body_surface_introduced_peak']=19;q['f472']=public(next(x for x in m['rows_private'] if x['frame']==472));q['native_guards']=[]
for n in ['wrist-intake-r1','wrist-w1','wrist-w1b','capture-front-w1b','capture-quarter-w1b','capture-side-w1b']:
 p=B/f'o1-tour472-{n}/NATIVE_GUARD_RESULT.json';g=json.loads(p.read_bytes());q['native_guards'].append({'name':n,'SHA':sha(p),'guard_status':g['guard_status'],'wall_seconds':g['wall_seconds'],'error':g.get('error')});assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' or n=='wrist-w1'
assert not m['scoped_left_wrist_QA_pass'] and sha(m['candidate'])==m['candidate_SHA'];ui=json.loads((D/'WHOLE_NORMAL1X_UI_W1.json').read_bytes());assert len(ui['videos'])==3 and all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in ui['videos']);q['whole_UI_native1x']=ui;q['OFF_RGBA_unequal_channels_each_view']=0;q['new_source_vs_native_wrist_curve_error']=0;q['causal_verdict']='One twist counterfactual failed. Original curves/pivot/rest/weights/modifiers unchanged. Not proof that weights, pivot or a specific modifier caused the source deformation.'
q['private_custody']=[{'path':str(p),'SHA':sha(p),'bytes':p.stat().st_size} for p in [B/'alpha-tour472-wrist-w1b/TOUR472_WRIST_W1_PRIVATE.json',B/'alpha-tour472-wrist-w1b/LOCAL_SURFACE_IDENTITIES_PRIVATE_W1.json.gz',B/'alpha-tour472-wrist-intake-r1/TOUR472_WRIST_INTAKE_PRIVATE_R1.json',D/'VIDEO_CUSTODY_R1.json',D/'WHOLE_NORMAL1X_UI_W1.json',D/'ACTUAL_FAIL_REVIEW_UI_W1.png']]
(E/'TOUR472_WRIST_W1_SCALAR_QA.json').write_text(json.dumps(q,indent=2),encoding='utf8');(E/'VIDEO_CUSTODY_W1.json').write_bytes((D/'VIDEO_CUSTODY_R1.json').read_bytes())
(E/'YURI_R4_TOUR472_LEFT_WRIST_W1_KO.md').write_text(f'''# Tour f472 왼손목 W1 — FAIL/HOLD

후보 `{m['candidate_SHA']}`는 원본보다 좋은 손목 교정으로 인정하지 않는다. 기본 OFF 연구 실패본만 보존하고 source packet/추가 cap sweep/rig·weights 수정/전체Tour reset/export는 없다. TierP0, Unity/F2/StageB 및 전체Tour 미승격.

기존 f472 원본 근접뷰에서 왼손목의 접힘이 더 명확해 왼쪽 하나를 선택했다. 원본 MESHY_R2_BODY_Tour와 native copy의 wrist/forearm curves는 오차0이며 adapter의 최초 차이는 없었다. source local-Y twist가 f461 약85.44도에서 f462 약88.93도로 커질 때 rest wrist65mm 지역 교차가0→5쌍으로 나타났다. 이 상관관계만으로 원인 PROVEN을 선언하지 않는다.

별도 Action copy 하나의 hand.L twist만75..95도 연속 구간,85도 상한으로 제한했다. swing, pivot 및 원본 시간/구간 밖 키·핸들/다른 joints는 유지했다. 실제 QA는453..492의40포즈, view는454..491의38프레임24fps다. f462는5→0이지만 f472는14→20, f474는15→20으로 악화했다. f472 원래14쌍 중4쌍은 남고 새16쌍이 생겼다. 전체 same-frame introduced BODY 쌍 최고19이며 나머지5개 surface 유형은0이다. BODY f472 전체 교차33→39. 각속도 크기 인접 변화 최고30.731→47.823도/초로 기존 +1 게이트를 넘었다. finite/triangle collapse0/0.1미만 면적비0, 발오차0 및 head/hair 보존은 제한적 보존 증거일 뿐 품질PASS가 아니다.

f472 손목 pivot 위치 오차0, swing오차0이지만 방향은38.116도 달라졌다. palm centroid는2.476mm 움직였고 finger/hand 실루엣·궤적도 달라진다. 정면/3⁄4/측면 동일 카메라 정상1x 전체38프레임 모두 actual geometry ledger와 일치하며 전체decode/실제UI ended/rate1/error없음. 후보는 손가락이 더 보이는 방향이지만 국소 손목 접힘 개선을 분리해 인정할 수 없다. 384pxCPU8 noisy shading으로 정확한 skin normal/intersection 깊이를 판단하지 않는다.

원본 R4 SHAa30fc513, sourceAction e70ea471, 원본81Actions 및 C1/C2/Reaction6/R2 원본 파일을 보존했다. 새candidate82Actions는 OFF 저장/재개방했으며 source81 전체signature와 기존bones/rest/geometry/weights/material/node/texture/ShapeKeys/face·gaze driver가 동일하다. 세 시점 OFF neutral decodedRGBA 차이는 모두0이다. 최초 W1 실행의 누락 BVHTree import 실패를 보존했고 같은 pose의 W1b에서 실행 dependency만 복구했다. 다른 각도 후보는 생성하지 않았다.

리뷰 `{D/'REVIEW_TOUR472_LEFT_WRIST_W1.html'}`
후보 `{m['candidate']}`

다음 실제 작업은 기존 Wave f1621cc2의 미완료 RIGHT finger/webbing 근접 QA 하나다. 기존91프레임 motion/source/hash/body baseline을 다시 만들지 않고 inclusive actual surface와 전체 hand close normal1x를 보완한다. 읽기 전용 nativeTalk 패킷 검사는 이미 끝났으나 기존 supplied 자산의 확인일 뿐 새 animation/export/transfer가 없고 새제품 진도로 세지 않는다.
''',encoding='utf8');print('WRIST_W1_FAILED_COUNTERFACTUAL_CLOSED_THREE1X_OFF0_NO_PACKET')
