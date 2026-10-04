"""Offline evidence only; never launch Blender or mutate source/candidates."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
LAB=Path(__file__).resolve().parents[1]
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
P=B/'alpha-walk-head-boundary-r1'; D=B/'alpha-walk-head-boundary-delivery-r1'; D.mkdir(exist_ok=False)
E=LAB/'evidence/walk-head-boundary-r1'; E.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((P/'HEAD_BOUNDARY_DISCRIMINATOR_PRIVATE_R1.json').read_bytes())
g=json.loads((B/'o1-walk-head-boundary-r1/NATIVE_GUARD_RESULT.json').read_bytes())
assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and g['terminal_job']['active']==0 and g['terminal_exit_code']==0
assert m['minimal_candidate'] is None and m['old_source_candidate_library_bytes_unchanged'] and m['source78_prior81_OFF_raw_snapshot_equal']
frames=[]
for f in m['frames_private']:
 n=np.load(P/f"FAILED_FRAME_{f['frame']}_SAVED_ACTION_COORDINATES_PRIVATE_R1.npz")
 exact={ob:bool(np.array_equal(n['actual__'+ob],n['original_body_only__'+ob])) for ob in ['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']}
 assert all(exact.values())
 regions=[]
 for category in sorted({x['category'] for x in f['details_private']}):
  xs=[x for x in f['details_private'] if x['category']==category]
  regions.append({'category':category,'new_pairs':len(xs),'materials':sorted({z['material'] for x in xs for z in x['materials']}),'bone_groups':sorted({z[0] for x in xs for r in x['regions'] for z in r['bone_weights']}),'existing_shape_support_names':sorted({z[0] for x in xs for r in x['regions'] for z in r['source_ShapeKey_support']}),'note':'Material/weight/ShapeKey support localizes anatomy, not proof that a ShapeKey changed or caused contact.'})
 frames.append({k:v for k,v in f.items() if k!='details_private'}|{'actual_vs_original_body_only_all_vertices_exact':exact,'localized_regions':regions})
baseline=B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'
a=np.asarray(Image.open(baseline).convert('RGBA')); z=np.asarray(Image.open(P/'HEAD_BOUNDARY_OFF_SOURCE_NEUTRAL_R1.png').convert('RGBA'));assert np.array_equal(a,z)
pixel={'exact_decoded_RGBA_equal':True,'changed_pixels':0,'max_RGBA_delta':0,'dimensions':list(a.shape),'baseline_sha256':sha(baseline),'result_sha256':sha(P/'HEAD_BOUNDARY_OFF_SOURCE_NEUTRAL_R1.png')}
(D/'OFF_PIXEL_QA_R1.json').write_text(json.dumps(pixel,indent=2),encoding='utf8')
movies=[]
for view in m['views']:
 for role in ['original_body_only_control','existing_full_transport']:
  folder=P/role/view; assert len(list(folder.glob('*.png')))==24
  out=D/f'{view}_{role}_NATIVE24FPS_1x.mp4'
  subprocess.run(['ffmpeg','-v','error','-framerate','24','-start_number','74','-i',str(folder/'%04d.png'),'-frames:v','24','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-n',str(out)],check=True)
  subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True)
  q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(out)]))['streams'][0]
  assert int(q['nb_read_frames'])==24 and q['avg_frame_rate']=='24/1'
  movies.append({'file':str(out),'sha256':sha(out),'frames':24,'fps':24,'duration':float(q['duration']),'role':role,'view':view,'whole_decode':'PASS','native_speed_factor':1})
 grid=Image.new('RGB',(256*8,280*6),'white'); dr=ImageDraw.Draw(grid)
 for row,role in enumerate(['original_body_only_control','existing_full_transport']):
  for i,f in enumerate(range(74,98)):
   x=i%8*256;y=(row*3+i//8)*280;grid.paste(Image.open(P/role/view/f'{f:04}.png').resize((256,256)),(x,y+24));dr.text((x+3,y+4),f'{role[:8]} {f}',fill='black')
 grid.save(D/f'ALL24_{view}_CONTROL_VS_TRANSPORT_R1.jpg',quality=94)
 for f in range(74,98):
  aa=np.asarray(Image.open(P/'original_body_only_control'/view/f'{f:04}.png'));bb=np.asarray(Image.open(P/'existing_full_transport'/view/f'{f:04}.png'));assert np.array_equal(aa,bb)
scalar={'task':m['task'],'verdict':'ADDITIVE_HEAD_HAIR_TRANSPORT_CAUSE_EXCLUDED_NO_CANDIDATE_CONTACT_HOLD','source_SHA':m['source_SHA'],'candidate_SHA':m['old_candidate_SHA'],'action_library_SHA':m['old_library_SHA'],'failure_frames':frames,'cached_vs_actual_original_OFF_max_component_error_m':m['cached_vs_actual_original_OFF_max_component_error_m'],'cached_coordinates_warning':'Cached external neutral differs by18.457um; actual immutable source OFF was used as authority. Cache was not treated as identical.','max_head_nonrigid_residual_m':m['max_actual_head_hair_vs_mathematical_rigid_residual_m'],'cause':'At91/92 every body/head/hair world vertex equals original BODY-only control exactly. Additional transport Actions therefore do not cause the recorded contacts in these frames. Nonroot basis and ShapeKey values also equal control.','unresolved':'Head differs from ideal rigid transform by0.542mm; already present in original control. Local modifiers/skinning/boundary mechanism not isolated. Hair residual<=0.066um but contact identities alone do not establish numerical noise.','new_candidate':None,'appearance_OFF':pixel,'original78_prior81_raw_equal':True,'old_bytes_unchanged':True,'affected_segment':'74..97 only,24frames/24fps/1second; no full97 or Idle rerender','all48_matched_camera_frame_pairs_decoded_RGBA_equal':True,'guard_SHA':sha(B/'o1-walk-head-boundary-r1/NATIVE_GUARD_RESULT.json'),'native_guard':g['guard_status'],'TierP':0,'next_bounded_recommendation':'Existing native BODY_HeadGazeHair source-only continuity audit; not executed here. Existing Walk remains source-reference-only; foot plant/velocity/contact/Unity gates not promoted.'}
(E/'HEAD_BOUNDARY_SCALAR_QA_R1.json').write_text(json.dumps(scalar,indent=2),encoding='utf8')
(D/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>R4 head boundary discriminator</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex}video{width:48%}button{padding:12px}</style><h1>R4 original BODY-only vs additive head/hair transport</h1><p>Frames74–97, original24fps,1x. Left original control; right existing candidate.91/92 all actual vertices exactly equal. Contact HOLD; no new candidate. Source appearance/driver/ShapeKey/weights/rest preserved.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play matched original native 1x</button>'
for view in m['views']:
 html+=f'<h2>{view}</h2><section>'
 for x in movies:
  if x['view']==view:html+=f'<video controls preload="auto" src="{Path(x["file"]).name}"></video>'
 html+='</section>'
(D/'REVIEW_HEAD_BOUNDARY_R1.html').write_text(html,encoding='utf8')
print(json.dumps({'verdict':scalar['verdict'],'OFF':pixel,'movies':movies},indent=2))
