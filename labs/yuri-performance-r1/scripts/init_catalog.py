"""Create versioned planning data; never label planned recipes as finished animation."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
def dump(name, value):
    p = ROOT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

groups = {
 'signature': [('greeting_wave','반갑게 작은 손인사'),('shy_lookaway','눈을 맞추다가 수줍게 피하기'),('please_tilt','고개를 기울여 부탁하기'),('cheek_puff','볼을 부풀려 장난스럽게 삐치기'),('playful_pout','삐친 척하다 웃기'),('finger_heart','작은 손가락 하트'),('double_cheek_frame','두 손으로 볼 옆을 감싸기'),('wink_smile','한쪽 윙크 후 웃기'),('peek_behind_hands','손 뒤로 얼굴을 숨겼다가 보기'),('proud_ta_da','잘했지 하고 자랑하기'),('happy_shoulder_bounce','기쁜 어깨 들썩임'),('lean_in_attention','관심을 끌며 살짝 다가오기')],
 'conversation': [('listen_soft','편안하게 경청'),('agree_small','작은 동의 끄덕임'),('curious_tilt','궁금한 고개 기울임'),('thinking_glance','생각하며 시선 이동'),('surprised_recover','놀랐다가 진정'),('amused_chuckle','작게 웃음'),('embarrassed_smile','민망한 미소'),('gentle_disagree','부드럽게 고개 젓기'),('reassure','안심시키는 손짓'),('expectant_pause','대답을 기다리는 표정'),('tease_then_soften','장난친 뒤 다정하게 풀기'),('apology_small','조심스러운 사과')],
 'room': [('sit_settle','앉아서 자세 정돈'),('stand_settle','일어나 자세 정돈'),('seated_shift','앉은 자세 체중 이동'),('stretch_small','작은 기지개'),('read_page','책 읽고 페이지 넘기기'),('look_up_from_book','책에서 눈을 들어 보기'),('mug_pickup','컵 잡아 들기'),('mug_sip','한 모금 마시기'),('mug_putdown','컵을 내려놓기'),('offer_item','물건을 건네려 내밀기'),('reach_table','탁자 위 물건에 손 뻗기'),('return_to_activity','대화 후 하던 일로 돌아가기')],
 'continuity': [('neutral_breath','자연스러운 호흡'),('blink_soft','편안한 눈깜빡임'),('gaze_acquire','관심 대상으로 시선 정착'),('gaze_release','시선 풀기'),('idle_weight_shift','선 자세 체중 이동'),('tiny_yawn','작은 하품'),('sleepy_nod','졸린 끄덕임'),('startled_blink','놀라서 눈깜빡임'),('motion_interrupt','진행 중 동작 부드럽게 중단'),('hands_to_rest','손을 기본 위치로 복귀'),('attention_return','주변을 보다 다시 집중'),('farewell_wave','아쉬운 작별 손인사')]
}
contact_ids = {'double_cheek_frame','peek_behind_hands','mug_pickup','mug_sip','mug_putdown','offer_item','reach_table','read_page'}
items = []
for category, rows in groups.items():
    for id_, label in rows:
        items.append({'id':id_,'label_ko':label,'category':category,'status':'PLANNED_NOT_PRODUCED','priority':1 if category=='signature' else 2,'source':'original_authored_recipe','license_review':'original_recipe_only_target_asset_separate','fps':24,'duration_seconds':4.0,'posture':'seated' if id_ in {'sit_settle','seated_shift','read_page','look_up_from_book'} else 'standing','root_motion':'in_place','entry_pose':'neutral_same_posture','exit_pose':'neutral_same_posture','face_profile':'anime_soft','contact_required':id_ in contact_ids,'contact_windows':[],'requires_finger_rig':id_ in {'finger_heart','double_cheek_frame','peek_behind_hands','mug_pickup','mug_sip','mug_putdown','offer_item','read_page'},'interrupt_policy':'release_contacts_then_blend_to_neutral','interrupt_markers_seconds':[0.0,4.0],'gaze_track':'independent_semantic_target','intensities_to_audition':[0.35,0.65,1.0],'retarget_status':'NOT_TESTED','runtime_status':'NOT_TESTED','visual_acceptance':'NOT_REVIEWED','artifacts':[]})
dump('catalog/motions.json',{'schema_version':'1.0','planned_base_count':len(items),'completed_production_count':0,'proxy_seeds':['greeting_wave','shy_lookaway','please_tilt'],'items':items})
recipes = {
 'soft_smile':{'smile_l':.30,'smile_r':.26,'eye_squint_l':.08,'eye_squint_r':.06},
 'bright_smile':{'smile_l':.65,'smile_r':.60,'eye_squint_l':.25,'eye_squint_r':.22,'jaw_open':.08},
 'shy':{'smile_l':.18,'smile_r':.12,'brow_inner_up':.16,'blush':.35},
 'please':{'brow_inner_up':.22,'smile_l':.12,'smile_r':.12,'lip_pucker':.10},
 'playful_pout':{'lip_pucker':.35,'mouth_down_l':.18,'mouth_down_r':.12,'brow_down_l':.15},
 'cheek_puff':{'cheek_puff_l':.65,'cheek_puff_r':.65,'lip_press':.35},
 'wink_l':{'blink_l':1.0,'smile_l':.38,'smile_r':.32},
 'wink_r':{'blink_r':1.0,'smile_l':.32,'smile_r':.38},
 'curious':{'brow_up_l':.24,'brow_up_r':.12,'jaw_open':.04},
 'surprise_small':{'eye_wide_l':.25,'eye_wide_r':.25,'brow_inner_up':.30,'jaw_open':.15},
 'amused':{'smile_l':.42,'smile_r':.36,'eye_squint_l':.18,'eye_squint_r':.15,'jaw_open':.10},
 'sleepy':{'blink_l':.35,'blink_r':.32,'jaw_open':.02},
 'proud':{'smile_l':.25,'smile_r':.30,'brow_up_r':.13},
 'apologetic':{'brow_inner_up':.25,'mouth_down_l':.1,'mouth_down_r':.1},
 'reassuring':{'smile_l':.22,'smile_r':.22,'eye_squint_l':.1,'eye_squint_r':.1},
 'neutral':{}
}
dump('catalog/face_recipes.json',{'status':'SEMANTIC_RECIPES_NOT_TARGET_RIG_VALIDATED','unit':'normalized_intent_not_universal_blendshape_weight','profiles':{'natural_soft':{'hold_seconds':[.2,.5],'overshoot':'minimal'},'anime_soft':{'hold_seconds':[.35,.8],'overshoot':'controlled_after_mesh_collision_QA'}},'composition_order':['mood','acting_envelope','gaze_eyelid_follow','blink_override','speech_viseme_budget','correctives','clamp_to_calibrated_limits'],'conflicts':['blink overrides eyeWide','cheekPuff requires calibrated lipSeal; speech reduces cheekPuff','speech reserves jaw/mouth range; smile must not break lip closure','eyeLookAt has single writer','spring bones applied once, not baked and simulated twice'],'recipes':recipes})
cameras = [
 {'id':'room_wide','lens_mm':35,'location':[2.6,-4.8,2.4],'target':[0,0,.95],'resolution':[1280,720]},
 {'id':'full_front','lens_mm':50,'location':[0,-5.2,1.15],'target':[0,0,.95],'resolution':[1280,720]},
 {'id':'waist_threequarter','lens_mm':65,'location':[1.45,-3.5,1.7],'target':[0,0,1.28],'resolution':[1280,720]},
 {'id':'face_close','lens_mm':85,'location':[0,-2.55,1.64],'target':[0,0,1.58],'resolution':[1280,720]},
 {'id':'hand_face','lens_mm':65,'location':[-.9,-2.6,1.6],'target':[0,0,1.4],'resolution':[1280,720]},
 {'id':'vertical_medium','lens_mm':50,'location':[.1,-3.6,1.5],'target':[0,0,1.15],'resolution':[720,1280]}
]
for c in cameras:c.update({'sensor_width_mm':36,'coordinate_space':'Blender_Z_up_meters_front_negative_Y','status':'BLOCKING_PRESET_REQUIRES_TARGET_FRAMING_QA','runtime_auto_camera':False})
dump('catalog/cameras.json',{'schema_version':'1.0','cameras':cameras})
dump('catalog/shot_manifest.template.json',{'schema_version':'1.0','shot_id':'greeting_wave__A01','status':'TEMPLATE_NOT_RENDERED','character_count':1,'character_asset_hash':None,'rig_profile':None,'source_license_review':None,'fps':24,'duration_seconds':4,'aspect_ratio':'16:9','camera_id':'waist_threequarter','frame_domain':'inclusive_start_exclusive_end','beats':[{'at':0,'intent':'notice'},{'at':.45,'intent':'anticipate'},{'at':.8,'intent':'wave'},{'at':2.0,'intent':'smile_hold'},{'at':3.0,'intent':'settle'},{'at':4.0,'intent':'neutral'}],'passes':{'beauty':None,'previz_mp4':None,'first_frame':None,'last_frame':None,'depth':None,'pose':None,'mask_id':None,'camera_metadata':'catalog/cameras.json'},'video_provider':{'selected':None,'billing_authorized':False,'job_id':None,'input_manifest_hash':None},'acceptance':{'one_subject':None,'identity':None,'eye_mouth':None,'hands':None,'feet_contact':None,'camera_continuity':None,'loop_or_return':None}})
(ROOT/'.gitignore').write_text('local/\n__pycache__/\n*.pyc\n',encoding='utf-8')
(ROOT/'AGENTS.md').write_text('''# Yuri Performance Lab R1\n\nOne writer in this isolated worktree. Preserve Yuri Room and Avatar E2E workers.\nDo not merge or alter main. No scheduler/orchestrator development.\nRead ../../skills/video-blender-production/SKILL.md and ../../skills/video-production-qa/SKILL.md.\nMCP: inspect/live correction. Saved bpy: reproducible authoring/export. A listed backend is NOT a live app pass.\nNo circumvention of blocked tools. Do not alter shared MCP settings.\nGPU lease at C:/YuriEmbodiedLab/runtime/gpu-lease.json must be honored; do not reclaim PRODUCT_EXCLUSIVE.\nCPU-only native Blender validation is allowed. No video-model inference until product lease is resolved by its owner.\nNo paid API calls, partner nodes, large downloads, updates, credentials, third-party models or source videos in Git.\nNever call recipe count completed animation count. A procedural proxy is NOT Yuri or a face-quality acceptance.\nUse existing UAL/retargeting/contact infrastructure, not an engine migration.\nVRM sample with modification prohibited / redistribution false is excluded from authoring.\nNeutral/blink L/R/eye direction/A/O must pass on the actual target face before elaborate facial recipes.\nReport absolute paths, hashes, tested commands, technical vs visual verdicts and one next bounded task.\n''',encoding='utf-8')
(ROOT/'CODEX_HANDOFF_KO.md').write_text('''# 유리룸 연기·프리비즈 병행 작업 지시\n\n## 목표\n영상 파일만 늘리지 말고 몸·손·얼굴·시선·호흡·카메라·소품 접촉을 분리한 연기 라이브러리를 만든다. 최종 목표는 자연스러운 애니메이션 주인공 같은 반응이며, 52개 키 존재만으로 완료 처리하지 않는다.\n\n## 작업 순서\n1. 현재 product/Avatar canonical 문서와 검증된 대상 아바타 해시를 확인한다. 기존 실행은 중지하지 않는다. proxy를 최종 아바타로 대체했다고 보고하지 않는다.\n2. 이미 있는 UAL 클립/VRM retarget/AnimationMixer/접촉/손가락 프리셋을 읽고 재사용한다. 엔진 변경 금지.\n3. 승인된 대상의 neutral, blink L/R, gaze, A/O를 정면·3/4·측면에서 검증한다. 눈꺼풀 접힘, 입꼬리 찢김, 치아/혀 관통, 눈 시선 writer 충돌을 먼저 해결한다.\n4. 인사/수줍게 시선 피하기/고개 기울여 부탁하기 3개를 실제 대상에 연출한다. 준비→동작→감정 정점→여운→복귀를 별도 타이밍으로 만든다. 시선이 머리보다 먼저 이동하도록 소량의 lead를 시험하고, 모든 클립에 같은 지연을 강제하지 않는다.\n5. 각 동작 3강도, 정면/3/4/클로즈업 검수. 완성된 3개가 통과하면 signature 12개로 확장, 이후 전체 계획 48개로 확장한다. 강도/속도 조합 수를 제작 완료 수로 세지 않는다.\n6. 손-볼/손-컵/발-바닥 접촉과 중단/복귀를 확인한다. 기존 스켈레톤 매핑/초기 자세를 기록한다.\n7. .blend 원본, glTF bone/morph 또는 개별 face curves, adapter별 런타임 테스트를 남긴다. FBX의 shape animation은 별도 검증한다. 단순 GLB 파일명 변경을 VRMA라고 부르지 않는다.\n8. 동일 shot manifest로 beauty/previz/first-last/depth/pose/mask/camera 패키지를 준비한다. 생성영상과 리깅 데이터는 별개 산출물이다.\n9. GPU 승인이 확인된 후 기존 Wan 5B smoke를 재현한다. Fun Control/Animate는 별도 weight/노드/VRAM 검증 과제이며 현재 5B 설치를 그 기능 완료로 간주하지 않는다.\n10. H3는 과거 1인→3인 증식 문제가 남아 있다. 새 얼굴 reference와 1인 구도를 고정한 1샷을 먼저 검증하고, 기존 실패를 무시한 대량 T2V를 하지 않는다.\n\n## 영상 공부를 남길 형식\n매 실험마다 질문/가설, 고정 변수, 하나의 변경 변수, first-middle-last 프레임, MP4, 손·얼굴·인원·구도·시간 일관성 판정, 비용/VRAM/RAM, 다음 결정 1개를 기록한다. 렌즈, 시선축, 포즈 silhouette, anticipation/hold/follow-through, 컷 연결, 자막·오디오·libx264 인코딩을 차례로 검증한다.\n\n## 외부 도구\nHiggsfield: motion/camera/표현 참고 또는 최종 픽셀 제작 후보. 사용 전 현재 MCP 모델/입력 역할/비용을 다시 확인한다. 이번 준비에서 유료/무료 quota 모두 소비하지 않는다.\nTripo/Meshy/AccuRIG: 기존 몸/리깅 자산 재사용. facial topology와 expression system의 자동 완성으로 가정하지 않는다.\nAudio-to-face: 입모양 보조 후보일 뿐 감정/시선/제스처 전체의 연출자가 아니다. 새로운 대형 설치보다 현재 rig mapping 우선.\n''',encoding='utf-8')
print(json.dumps({'planned_motions':len(items),'face_recipes':len(recipes),'camera_presets':len(cameras),'production_clips_completed':0,'root':str(ROOT)},ensure_ascii=False))
