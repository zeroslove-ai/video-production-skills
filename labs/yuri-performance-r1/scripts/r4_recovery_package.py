"""Freeze additive recovery packet; reuse immutable probe instead of duplicating it."""
import json,hashlib,zipfile,shutil,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1');OLD=OUT.parent/'o1-native-unity-probe-r1'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for v in iter(lambda:f.read(1024*1024),b''):h.update(v)
    return h.hexdigest()
def load(n):return json.loads((E/n).read_text(encoding='utf8'))
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def run(args):
    r=subprocess.run(args,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace')[-1500:])
assert len(list((OUT/'manual_morph_proof').glob('frame_*.png')))==72
video=OUT/'manual_morph_proof/Existing_Blink_Smile_Jaw_24fps_3s.mp4'
run(['ffmpeg','-y','-framerate','24','-i',str(OUT/'manual_morph_proof/frame_%04d.png'),'-frames:v','72','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(video)])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=avg_frame_rate,nb_read_frames,duration','-of','json',str(video)],text=True))['streams'][0];assert probe['avg_frame_rate']=='24/1' and int(probe['nb_read_frames'])==72
first=np.array(Image.open(OUT/'manual_morph_proof/frame_0000.png'));last=np.array(Image.open(OUT/'manual_morph_proof/frame_0071.png'));assert np.array_equal(first,last)
sheet=Image.new('RGB',(384*3,368*3),(30,30,30))
for row,group in enumerate(('blink','smile','jaw')):
    for col,index in enumerate((0,11,23)):sheet.paste(Image.open(OUT/'manual_morph_proof'/f'frame_{row*24+index:04d}.png').convert('RGB'),(col*384,row*368))
sheet.save(OUT/'manual_morph_proof/OFF_ON_OFF_contact_sheet.png')
write('MANUAL_PROOF_VIDEO_RECEIPT.json',{'video':video.relative_to(OUT).as_posix(),'sha256':sha(video),'probe':probe,'first_last_unequal_pixel_channels':0,'use':'Functional direct-morph diagnostic; no F2/F3 performance claim; board drivers remain muted.'})
source=load('SOURCE_DATA_RECEIPT.json');control=load('CONTROL_CAUSAL_RECEIPT.json');shader=load('MATERIAL_SHADER_DRIVER_RECEIPT.json');layers=load('DEFORMATION_LAYER_RECEIPT.json');manual=load('MANUAL_MORPH_RECEIPT.json');static=load('static-correction/roundtrip_receipt.json');causal=load('STATIC_CAUSAL_SEPARATION.json')
write('FULL_DRIVER_OWNER_COVERAGE.json',{'objects_Key_GN_material_ID_drivers':control['counts'],'additional_material_owned_ShaderNodeTree_drivers':shader['additional_driver_count'],'total_driver_count':control['counts']['total']+shader['additional_driver_count'],'muted_total':control['counts']['muted']+sum(f['mute'] for o in shader['material_shader_node_tree_owners'] for f in o['drivers']),'invalid_shader_drivers':sum(not f['valid'] for o in shader['material_shader_node_tree_owners'] for f in o['drivers']),'namespace_registration':'No nonstandard names found; no registration performed','manual_morph_owner':'Head Key data values; board13 remains original muted; linked lash/material drivers consume these direct values','source_mute_policy_author':'Unknown; original shipped state confirmed, body-only adapter does not own or change it.'})
frozen=json.loads((OLD/'PACKAGE_HASH_MANIFEST.json').read_text(encoding='utf8'));lookup={r['path']:r for r in frozen['files']};paths=['source/Character_Master_NeckSkin_R4.blend','source/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend','metadata/source_expanded_rigs.json','metadata/source_renderers_bind.json','metadata/face_board_inputs.json','metadata/source_driver_graph.json','metadata/semantic_mapping.json','reference/source_original_vertex_weights.json.gz','reference/native_evaluated_all_frames.json.gz','reference/native_evaluated_motion_geometry_0_25_50_100.json.gz','reference/source_neutral_evaluated_world_vertices.json.gz','metadata/take_and_slot_inventory.json','visual/source_vs_actual_FBX_24fps.mp4']
reuse={'frozen_package_sha256':'4ec5c10ce90d7d25c06721b7dcd3832be4b7672190c975d42912be876a5a0843','frozen_package_bytes':175204266,'required_prior_commit':'d204379bb8dbab7749a8819863437e788b9ce9ee','reused_files':[lookup[p] for p in paths],'current_packet_rule':'Additive data only. Existing original source, actions, weights, rig/constraint metadata and full normal-speed6clip proof are exact hash pointers, not duplicated.'};write('REUSE_COVERAGE_POINTERS.json',reuse)
coverage=[
 {'requirement':'Material slot→polygon/UV/texture bytes/math','status':'PROVIDED','data':['mesh_slot_UV_attributes_shape_deltas.json','executable_material_graphs.json','exact_texture_receipt.json','data/*_original_mesh.npz','textures/*'],'meaning':'Exact source slots/polygon/loop UV indices; all socket defaults/links/node operations including attributes/ramp/math; texture15 exactpacked bytes/channel/colorspace/alpha and node interpolation/mapping.'},
 {'requirement':'Neutral albedo/opacity/normal/masks','status':'PROVIDED_WITH_LIMITS','data':['NEUTRAL_BAKE_RECEIPT.json','neutral_bakes/*.exr','CORNER_BASIS_RECEIPT.json','data/*_corner_basis.npz'],'meaning':'12 CPU-derived512px scene-linear EXR neutral inputs/Alpha/tangent normals for4UV meshes; hair has no UV and constant source shader, so graph+vertex normals are authority. Exact POINT/CORNER masks and polygon slot assignments in original NPZ. No UV repack or source replacement.'},
 {'requirement':'Camera/lights/color/driver state','status':'PROVIDED','data':['neutral_camera_light_color_driver_state.json'],'meaning':'Original transforms/projection/world/lights/exposure/view/render state and neutral controls.'},
 {'requirement':'FaceBoard13/face/gaze/hair executable dependencies','status':'PROVIDED_WITH_OWNERSHIP_HOLD','data':['controls_contract.json','executable_driver_dependencies.json','executable_geometry_node_graphs.json','evaluated_driver_geometry_references.json','CONTROL_CAUSAL_RECEIPT.json','MATERIAL_SHADER_DRIVER_RECEIPT.json','MANUAL_MORPH_RECEIPT.json'],'meaning':'43 native evaluated cases;13board at.5/1 remain muted head output0; gaze cardinal ±1 nonzeroGN+geometry; hair knob poses/driver outputs. Manual Blink/Smile/Jaw/Brow direct morph measured ON/OFF, linked lash/shader output.880 drivers total including8material-node-tree drivers. No unmute/rewrite.'},
 {'requirement':'ShapeKey basis/delta/default correspondence','status':'PROVIDED','data':['mesh_slot_UV_attributes_shape_deltas.json','data/*_original_mesh.npz'],'meaning':'Every source exported renderer key name, original index, relative-key delta float32/default/range/mute.72head keys and original basis positions. Actual geometry proof, not count-only.'},
 {'requirement':'DQ/maskedLBS/GN/surface masks/order/normals','status':'PROVIDED','data':['DEFORMATION_LAYER_RECEIPT.json','exact_mask_coverage.json','data/Strong_1_49_deformation_layer_ablation.npz','data/motion_*.npz','data/gaze_*.npz'],'meaning':'Original modifiers/settings ordered, pervertex mask weights by exact frozen pointer; dense source/local/world positions+normals; staged-object-copy DQ/mask/surface ablation Strong1/49, source stack unchanged.'},
 {'requirement':'Bind/rest transport and influence support','status':'PROVIDED_GATE_FAILS','data':['*_bind_and_OFF_LBS.json','LBS_bind_motion_transport_metrics.json','worst_rest_bone_skin_support.json','full_deformation_RMS_percentiles.json','STATIC_CAUSAL_SEPARATION.json','static-correction/*'],'meaning':'Raw bind versus evaluated OFF separated; true inversebind identity residual; first-modifier LBS shadow source/import transport; max/RMS/p50/p95/p99/worstvertex; rest/rotation independent failures preserved.'},
 {'requirement':'F0/F1/F2/F3 and promotion','status':'HOLD','data':['RECOVERY_DISPOSITION.json','manual_morph_proof/Existing_Blink_Smile_Jaw_24fps_3s.mp4'],'meaning':'F0 Blender functional proof only; F1 product physics/contact unaccepted; F2 character performance/multicamera not certified; F3 not claimed. Reference quality read; no new dance/source redesign.'}]
write('COVERAGE_TABLE.json',coverage)
summary={'task':'YURI_O1_SOURCE_FIDELITY_RECOVERY_DATA_R1','status':'BOUNDED_PACKET_COMPLETE / PROMOTION_HOLD','parent':'d204379bb8dbab7749a8819863437e788b9ce9ee','source_SHA256':source['source_SHA256'],'source_component_differences':0,'source_saved':False,'textures_exact_count':15,'source_renderers':21,'material_graphs':19,'source_reference_cases':43,'normal_bake_references':12,'total_drivers':880,'muted_head_bridge13':True,'manual_morph_actual_geometry':{group:max(x['max_world_vertex_delta_m'] for r in manual['cases'] if r['group']==group and r['input_value']==1 for x in r['geometry']) for group in ('blink','smile','jaw','brow')},'manual_OFF_return_geometry_m':0,'manual_OFF_return_unequal_pixels':0,'serializer_effective_default_component_delta_before':causal['original_effective_defaults']['max_effective_TRS_component_delta'],'serializer_effective_default_component_delta_after':causal['corrected_effective_defaults']['max_effective_TRS_component_delta'],'candidate_static_rest_PASS':static['pair_static_contract_PASS'],'candidate_position_rotation_PASS':static['source_pose_fidelity_PASS'],'candidate_actual_motion_PASS':static['actual_motion_PASS'],'candidate_loop2cycles_PASS':static['loop_2cycles_PASS'],'F0':'Blender functional compatibility/direct-morph only; Unity pending','F1':'unaccepted; no new physics/contact verification','F2':'not certified; source expression owner ambiguity and product multicamera timing/hand/secondary review pending','F3':'not claimed','Unity_PASS':False,'next_contract':'PM/consumer: exact node/texture/UV restore; source board-muted versus direct-morph intent ownership; DQ+maskedLBS+surface/GN feasibility; exact skeleton bind/rest serialization; no consumer rest rewrite/tolerance relaxation.'};write('RECOVERY_DISPOSITION.json',summary)
table='\n'.join('| '+r['requirement']+' | '+r['status']+' | '+'; '.join(r['data'])+' |' for r in coverage)
report=f'''# R4 source fidelity recovery data R1 — 2026-10-03 KST

**Bounded source-data packet complete. Product/appearance promotion remains HOLD.** Parent research commit d204379b and immutable probe ZIP4ec5c10... remain unchanged. No canonical geometry/material/rig/driver/rest/Action changes, no Unity product edits or shared GUI edits; all jobs CPU-only.

## Coverage and immutable reuse

Prior frozen ZIP SHA256 `{reuse['frozen_package_sha256']}` is required. REUSE_COVERAGE_POINTERS.json contains exact internal paths/bytes/hashes; extract it once and use pointers. This packet adds missing executable data, not another source master or rebuilt GameRig.

| Requirement | Disposition | Exact data paths |
|---|---|---|
{table}

Texture15 files are original packed bytes without re-encoding, with image dimensions/channels/space/alpha.19 source material graphs include types/operations/socket defaults/links/image/attribute names and mapping/interpolation. Slot/polygon/loopUV/basis/relative morph deltas/attributes and corner normals/tangents have stable source indices in float32 NPZ; NPZ array names and JSON paths define correspondence. Current FBX roundtrip counts/index positions match; if a consumer splits vertices, it must retain explicit polygon-loop→source index mapping, never assume Unity vertex order.

Neutral CPU bake references are diagnostic Base Color/Alpha-input/Tangent Normal in unchanged UVs,512px32bit linear EXR, not replacement source textures or full PBR shader equivalence. Alpha is stored in RGB; A is atlas coverage. All roughness/IOR/transmission/emission/metallic/normal strengths and masks remain exact graph inputs. Where compatible scalar roughness is converted, smoothness=1-roughness reversibly, no visual retuning. Combined slot UV overlaps can limit atlas references; original polygon/UV/node/attribute semantics outrank a bake. Hair has no UV; its original constant shader and geometric normals/tangents policy are explicit rather than inventing UVs.

## Source expression ownership recovered without unmuting

Source13 head FaceBoard bridge Fcurves are muted but valid; factory `--disable-autoexec/use_scripts=False` has no autoexec error, missing custom namespace or invalid drivers. Read-only GUI confirms same13mute flags, clean/frame1.872 object/Key/GN/material-ID drivers +8material-owned ShaderNodeTree drivers =880 total,13muted. Shader-owned drivers are included separately because they are not in bpy.data.node_groups.

Board sliders LOCAL Y0..0.055m target geometry shape-key values (not shader-only controls); their head bridges remain0 in current source. Runtime DriverVariable values have no public RNA accessor; evaluated bone channels/matrices, declared variables/paths/spaces, downstream Key/GN/shader outputs are provided without pretending to access the private evaluator.

Existing direct head morph input works: Blink max16.0845mm including attached lashes; Smile2.39016mm; Jaw5.45469mm; Brow2.59992mm. Peak/RMS/affected vertices/defaults/connected shader output measured; OFF geometry0m and diagnostic first/last pixels0difference. Existing_Blink_Smile_Jaw_24fps_3s.mp4 is a72frame1x triangular control fixture (not performance design). Source driver definition/mute policy untouched. Body-only ReactionLane does not own face. No author declaration explaining original13mute policy found in relevant adapter/build/evidence reads; PM must choose manual-morph versus board-driven runtime ownership explicitly. No automatic unmute or face redesign.

## Deformation causality and bind are distinct

Frozen native versus FBX Strong1 max3.928654mm, RMS0.415242mm, p95 0.844805mm, p99 2.121519mm; worst original body vertex47693. Float64 first-armature pure LBS transport mismatch max1.231315µm across6clips×4samples×21renderers, so this transport shadow cannot explain the millimeter-scale native procedure deficit. True source native deformation remains authority; pure LBS is not promoted.

Staged read-only source-mesh object-copy ablation Strong1: DQ↔LBS max3.928732mm, DQ versus DQ+maskedLBS1.435946mm, surface stack addition1.454683mm.49 end behaves similarly. These component effects are not additive scalar allowances. Copy removed; source fingerprint diff={{}}. Exact masks/order/settings and dense layer arrays provided. Affected thigh.L descendants influence18161body vertices, Hair_Pony_03 influences1025hair vertices; face J_Bip_L_Index3 has0positive skin influences, but strict rest gate remains independent of that count.

## One bounded static correction — not promoted

Exporter input unchanged and source fingerprints0difference. Blender Model serializer uses evaluated pose (`fbx_object_tx(rest=False)`), while skin BindPose/Cluster uses raw rest; NLA animation gathering precedes Model writing. One disposable exporter correction caches original OFF Model default TRS from model and replays exactly those defaults only in animation Model serialization. Animation curve evaluation remains unchanged. Original effective default mismatch9.156722356e-5 component (Euler degrees/scale/translation depending property) becomes0. Raw wire omission-versus-explicit identity still differs, but effective defaults match exactly.

Importer uses Pose/Cluster bind matrices in model (34Pose objects/1150Cluster records), but animation-only has0Pose/0Cluster and falls back to Model default matrix. Source raw rest and evaluated neutral are not interchangeable. Bind/default paths and float decomposed/normalized bone construction are therefore separately evidenced; not every coefficient is attributed solely to precision.

Corrected candidate still FAILS strict rest: body1.050531864e-5, face4.563480616e-5, hair2.384185791e-6, board0. Rotation-inclusive pose gate still FAILS (~0.002111216° versus<0.001°). Six actual motions/2loop cycles continue PASS, which does not waive fidelity. Candidate files/versioned SHA receipts stay diagnostic. No consumer rest rewrite or tolerance relaxation. Next narrow serializer feasibility would transport original skeleton bind/rest matrices consistently into meshless motion, not change source rig; no second export trial launched.

## Quality layers and next consumer boundary

F0: native/Blender import functionality and direct existing morph references. Unity functional gate pending. F1: physical contact/root/transition acceptance unverified. F2: not certified—combined pose/timing/hands/head/gaze/face/secondary and normal1x multiple product-camera review still required. F3: not claimed. The owner anime performance North Star was read and does not authorize new dance or character redesign here.

Consumer owns exact texture/UV/slot/node restoration on isolated Unity candidate and separate driver/morph/DQ/GN/surface adapter feasibility. PM must disposition manual face ownership and strict bind/rest serialization first. Existing full normal-speed6clip video is reused by hash pointer and remains HOLD; this packet has not re-rendered or passed corrected-carrier appearance/normal-speed source fidelity. No material recoloring, approximate local-control head, shader compensation or newGameRig is authorized.

## Reproduction

Scripts preserved in research branch and scripts/; existing project paths are explicit. Order inspect→source_data→neutral_bake→static_correction(one trial)→static_analysis→bind_analysis→control_causal→corner_basis→deform_layers→manual_morph→shader_drivers→package. Fresh Blender5.2.1 LTS factory background CPU and Python313/PIL/NumPy/FFmpeg. Source originals and prior packet remain input-only; GUI only inspected.
'''
for p in (E/'YURI_O1_SOURCE_FIDELITY_RECOVERY_R1.md',OUT/'README.md'):p.write_text(report,encoding='utf8')
(OUT/'scripts').mkdir(exist_ok=True)
for p in HERE.glob('r4_recovery_*.py'):shutil.copyfile(p,OUT/'scripts'/p.name)
for name in ('r4_appearance_signature.py','r4_appearance_adapter.py','native_preservation.py'):shutil.copyfile(HERE/name,OUT/'scripts'/name)
# New metadata is copied; exact old/frozen artifacts are referenced, not duplicated.
for p in E.glob('*.json'):
    if not (OUT/'metadata'/p.name).exists():shutil.copyfile(p,OUT/'metadata'/p.name)
files=[];deduplicated=[]
for p in sorted(OUT.rglob('*')):
    if not p.is_file() or p.name.startswith('frame_') or p.name in ('PACKAGE_HASH_MANIFEST.json','PACKAGE_RECEIPT.json'):continue
    rel=p.relative_to(OUT).as_posix()
    if rel.startswith('static-correction/reference/') or p.suffix=='.blend':continue
    if rel.startswith('static-correction/metadata/'):
        prior=OLD/'metadata'/p.name
        if prior.exists() and sha(prior)==sha(p):deduplicated.append({'omitted_current_path':rel,'reuse_exact_prior_path':prior.relative_to(OLD).as_posix(),'sha256':sha(prior)});continue
    files.append(p)
write('DUPLICATE_OMISSION_POINTERS.json',deduplicated);files.append(OUT/'metadata/DUPLICATE_OMISSION_POINTERS.json')
manifest={'dependency':reuse['frozen_package_sha256'],'files':[{'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]};mf=OUT/'PACKAGE_HASH_MANIFEST.json';mf.write_text(json.dumps(manifest,indent=2),encoding='utf8');files.append(mf)
archive=OUT.parent/'YURI_O1_R4_SOURCE_FIDELITY_RECOVERY_20261003_R1.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for r in manifest['files']:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
h=sha(archive);outbox=Path('C:/YuriTransfer/outbox');dest=outbox/f'YURI_O1_R4_SOURCE_FIDELITY_RECOVERY_20261003_R1_{h[:12]}.zip';assert not dest.exists();shutil.copyfile(archive,dest);assert sha(dest)==h;dest.chmod(0o444)
parts=[]
with archive.open('rb') as f:
    index=1
    while chunk:=f.read(64*1024*1024):
        part=outbox/(dest.name+f'.part{index:02d}');assert not part.exists();part.write_bytes(chunk);part.chmod(0o444);parts.append({'path':str(part),'bytes':len(chunk),'sha256':sha(part)});index+=1
receipt={'archive':str(dest),'sha256':h,'bytes':dest.stat().st_size,'members':len(files),'CRC_all_member_SHA_verified':True,'requires_frozen_probe':reuse['frozen_package_sha256'],'raw_split_parts':parts,'reassemble':'binary concatenate parts in ascending order, then assert archive SHA before extraction; not independent ZIPs','status':'PACKET_COMPLETE / PROMOTION_HOLD','source_preservation':'PASS','static_rest':'FAIL','position_rotation':'FAIL','F2':'NOT_CERTIFIED','Unity_PASS':False};write('PACKAGE_RECEIPT.json',receipt);dest.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt,indent=2))
