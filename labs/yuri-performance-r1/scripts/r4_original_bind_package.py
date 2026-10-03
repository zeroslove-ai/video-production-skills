"""Freeze one diagnostic bind trial; no automatic Unity authorization."""
import json,hashlib,zipfile,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-original-bind-serialization-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-bind-serialization-r1');OLD=OUT.parent/'o1-native-unity-probe-r1'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def load(n):return json.loads((E/n).read_text(encoding='utf8'))
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.write_text(json.dumps(v,indent=2),encoding='utf8')
receipt=load('export_receipt.json');bind=load('EXACT_BIND_WIRE_RECEIPT.json');pair=load('pair_path_rest_comparison.json');motion=load('motion_position_rotation_fidelity.json');movement=load('roundtrip_motion.json');roundtrip=load('roundtrip_receipt.json')
source=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';assert not load('source_after_export_diff.json')
summary={'task_id':'YURI_O1_ORIGINAL_BIND_SERIALIZATION_R1','trial_count':1,'status':'BIND_TRANSPORT_AND_PAIR_REST_PASS / SOURCE_ROTATION_HOLD','parent_commit':'ab1409f33e949e053b8abc84ec6aaaef6792d0d4','source_SHA256':sha(source),'source_component_differences':0,'original_actions_preserved':78,'new_source_rigs_or_meshes':0,'raw_model_effective_bind_vs_animation_Pose_exact':bind['all_existing_model_effective_bind_equals_animation_exact'],'original_Cluster_vs_Pose_exact':bind['all_original_Cluster_TransformLink_equal_corresponding_Pose'],'source_bones':137,'animation_pose_nodes':143,'animation_geometry_or_skin':False,'ordered_names_parents_PASS':all(r['ordered_model_animation_names_equal'] and r['parents_equal'] for r in pair),'strict_pair_local_rest_PASS':roundtrip['pair_static_contract_PASS'],'pair_local_rest_delta_by_rig':{r['rig']:r['pair_max_local_rest_matrix_element_delta'] for r in pair},'source_position_max_error_m':max(r['max_position_error_m'] for r in motion['clips']),'source_rotation_max_error_deg':max(r['max_rotation_error_deg_double_dot'] for r in motion['clips']),'source_position_rotation_combined_PASS':motion['PASS'],'position_threshold_m':1e-4,'rotation_threshold_deg':.001,'rest_threshold':1e-5,'precise_rotation':'abs(dot(normalized q1,q2)) with Python double; q sign equivalent','native_unique_frames_checked':sum(r['frames'] for r in motion['clips']),'actual_motion_loop_frames_checked':sum(r['frames_sampled'] for r in movement),'six_actual_nonroot_motion_PASS':roundtrip['actual_motion_PASS'],'two_loop_cycles_PASS':roundtrip['loop_2cycles_PASS'],'model':receipt['model'],'animation':receipt['animation'],'new_performance_video_rendered':False,'Unity_PASS':False,'visual_fidelity':'HOLD / not rerendered','F2':'NOT_CERTIFIED','consumer_input_authorized':False,'next':'PM custody/disposition; separately measure consumer importer against exact raw bind/source matrices; no rest rewrite/tolerance relaxation'};write('BIND_TRIAL_DISPOSITION.json',summary)
reuse=[];omitted=[]
for p in sorted((OUT/'metadata').glob('*.json')):
    old=OLD/'metadata'/p.name
    if old.exists() and sha(old)==sha(p):omitted.append({'current_path':p.relative_to(OUT).as_posix(),'prior_frozen_path':old.relative_to(OLD).as_posix(),'sha256':sha(old)})
for path in ['source/Character_Master_NeckSkin_R4.blend','source/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend','reference/native_evaluated_all_frames.json.gz','reference/source_original_vertex_weights.json.gz','metadata/source_expanded_rigs.json','metadata/source_renderers_bind.json','metadata/semantic_mapping.json']:
    p=OLD/path;reuse.append({'path':path,'bytes':p.stat().st_size,'sha256':sha(p)})
write('REUSE_POINTERS.json',{'frozen_probe_sha256':'4ec5c10ce90d7d25c06721b7dcd3832be4b7672190c975d42912be876a5a0843','source_recovery_packet_sha256':'080352e24adb9db33e76e92d8aca9836aeaf444ed75818c29e2970a32dae47df','prior_files':reuse,'omitted_identical_metadata':omitted})
report=f'''# Original skeleton bind serialization R1 — 2026-10-03 KST

**One trial completed. Bind transport and strict model↔animation rest PASS; source rotation fidelity remains HOLD. No Unity/product/F2 promotion.** Prior source/Actions/rig/weights/materials/drivers/helper poses/ZIPs unchanged; CPU factory jobs, no GUI or product edits.

## Exact representation

Raw native rest, evaluated OFF, FBX Model default TRS and effective Pose/Cluster bind are separate. Original source OFF Model defaults are captured/replayed only for serializer consistency, never substituted for rest. The original model's actual raw BindPose matrices are emitted in meshless animation as one skeleton BindPose.143Pose nodes =137original bones +4rig objects +2existing ancestry empties. No Geometry, Mesh, Skin or Cluster is added to animation. Unbound FaceBoard13/ancestry matrices use original rest=True global getter; no new rig or rest reset. Definitions/Pose count added consistently.

Actual wire audit:1150model Cluster.TransformLink records across124bound bones are exactly equal to corresponding model Pose matrices. Every existing effective model bone bind is byte-value identical to animation Pose; source rest conversion checked independently, max coefficient residual1.192092896e-7 from float32 matrix operations. Column-major float64 wire storage and declared source→FBX axis/unit convention are retained. Trial wrapper recorded0Cluster captures because its orientation filter selected Model→Cluster; actual source edges are Cluster→Model. This is disclosed, not hidden: transported Pose equals all actual overriding Cluster matrices by independent binary audit. No second export performed.

Source SHA `{summary['source_SHA256']}` unchanged, component diff={{}},78original Actions preserved. Bone order/parents/counts identical across paired files, all57body including nondeform helpers preserved. Both loops sampled2cycles. No source scale/height ratio reapplied.

## Strict gates

- Model↔animation local rest: body0, face0, hair0, FaceBoard2.384185791e-7, all<1e-5 **PASS**. This repairs the prior bind/default representation gap.
- Source full-frame position max {summary['source_position_max_error_m']:.9g}m<0.0001m **PASS**.
- Source full-frame normalized-double quaternion rotation max {summary['source_rotation_max_error_deg']:.9g}° versus<0.001° **FAIL** (face J_Bip_L_Index3, Startle frame17). Combined position+rotation **FAIL**; no threshold relaxation.
-276unique source frames and384endpoint-inclusive motion frames tested;6actual nonroot movements **PASS**, Light/Strong2cycles **PASS**. All-frame data, not action-name existence.
- Blender/Unity visual fidelity and F2 **HOLD**. No repeated performance video; previous complete normal-speed references retain their own failures. New bytes are not authorized Unity input until PM custody/disposition.

## Remaining reconstructed-bone gap

Source and imported bones now receive the same raw FBX bind representation, but source→Blender importer reconstructed bone matrix remains measurably different. Diagnostic world-rest rotation J_Bip_L_Index3≈0.002089307°, Index2≈0.001650977°. Source/import head/tail/length/local matrices/orthogonality/determinant/singular values are recorded for all137bones, together with raw source rest and evaluated OFF references. Importer uses bind matrices, localizes hierarchy, computes correction matrices, then creates normalized Blender bones. We have isolated the residual reconstruction stage; no claim that a single float operation is the sole cause and no importer rewrite. Zero skin influence on a finger bone does not waive the all-bone gate.

Original bind can be transported with meshless FBX; that missing representation is resolved. Remaining limitation is reconstructed source-pose equivalence in this Blender roundtrip. Source-preserving fallback is canonical original .blend + existing Action/NLA + exact native evaluated matrix payload. Future consumer must independently measure its own importer raw bind/default/Transform against these references after exact custody. Blender failure is not automatic Unity failure or PASS. Do not rewrite consumer rest, offset bones, prune helpers or enlarge tolerance to hide it.

## Custody/reproduction

Versioned model: `{receipt['model']['file']}`, {receipt['model']['bytes']}bytes, SHA `{receipt['model']['sha256']}`.
Meshless animation: `{receipt['animation']['file']}`, {receipt['animation']['bytes']}bytes, SHA `{receipt['animation']['sha256']}`.
Expanded exact bind/source/rest/import/fullframe/error receipts are packaged. Original source/action/reference data reused via exact REUSE_POINTERS.json to frozen ZIP4ec5c10... and recovery ZIP080352.... No duplicated canonical master or normals/material rebake.

Run r4_original_bind_serialization.py once on fresh Blender5.2.1LTS factory background; then wire_verify and reconstruction_diagnostic are read-only checks; package freezes bytes. Runtime exporter functions are patched only inside this disposable process and restored; installed module files remain unchanged. PM dispatch blob dc5d8b09dd402382f10041c9d8540ca3022dfb45. No next trial or production work started.
'''
for p in (E/'YURI_O1_ORIGINAL_BIND_SERIALIZATION_R1.md',OUT/'README.md'):p.write_text(report,encoding='utf8')
(OUT/'scripts').mkdir(exist_ok=True)
for pattern in ('r4_original_bind_*.py','r4_o1_native_probe_export.py','r4_o1_native_probe_roundtrip.py','r4_o1_native_probe_wire.py','r4_o1_native_probe_matrix_analysis.py','r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py'):
    for p in HERE.glob(pattern):shutil.copyfile(p,OUT/'scripts'/p.name)
for p in E.glob('*.json'):
    target=OUT/'metadata'/p.name
    if not target.exists():shutil.copyfile(p,target)
shutil.copyfile(E/'TRIAL_CONTRACT.md',OUT/'TRIAL_CONTRACT.md')
omit={r['current_path'] for r in omitted};files=[p for p in sorted(OUT.rglob('*')) if p.is_file() and p.relative_to(OUT).as_posix() not in omit and not p.relative_to(OUT).as_posix().startswith('reference/') and p.suffix!='.blend' and p.name not in ('PACKAGE_HASH_MANIFEST.json','PACKAGE_RECEIPT.json')]
manifest={'scope':'Diagnostic bind trial, no automatic Unity intake','requires_prior_frozen_probe':'4ec5c10ce90d7d25c06721b7dcd3832be4b7672190c975d42912be876a5a0843','files':[{'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]};mf=OUT/'PACKAGE_HASH_MANIFEST.json';mf.write_text(json.dumps(manifest,indent=2),encoding='utf8');files.append(mf)
archive=OUT.parent/'YURI_O1_R4_ORIGINAL_BIND_SERIALIZATION_20261003_R1.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for r in manifest['files']:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
h=sha(archive);outbox=Path('C:/YuriTransfer/outbox');dest=outbox/f'YURI_O1_R4_ORIGINAL_BIND_SERIALIZATION_20261003_R1_{h[:12]}.zip';assert not dest.exists();shutil.copyfile(archive,dest);assert sha(dest)==h;dest.chmod(0o444)
package={'archive':str(dest),'sha256':h,'bytes':dest.stat().st_size,'members':len(files),'CRC_all_member_hashes_verified':True,'model':receipt['model'],'animation':receipt['animation'],'trial_count':1,'source_preservation_PASS':True,'exact_original_bind_transport_PASS':True,'strict_model_animation_rest_PASS':True,'source_position_rotation_combined_PASS':False,'visual_F2_promotion':'HOLD','Unity_input_authorized':False,'Unity_PASS':False};write('PACKAGE_RECEIPT.json',package);dest.with_suffix('.receipt.json').write_text(json.dumps(package,indent=2),encoding='utf8')
print(json.dumps(package,indent=2))
