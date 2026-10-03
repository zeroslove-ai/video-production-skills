"""Read frozen FBX/source and actual Unity raw Git blob, no scene/product writes.
Geometry basis candidates from declared matrices, not fitted bone/rest edits.
"""
import sys,types,json,gzip,hashlib,subprocess,base64,collections
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
N=BASE/'o1-native-unity-probe-r1';B=BASE/'o1-original-bind-serialization-r1';R=BASE/'o1-source-fidelity-recovery-r1'
E=LAB/'evidence/o1-renderer-basis-diagnostic-r1';OUT=BASE/'o1-renderer-basis-diagnostic-r1'
E.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
PMROOT=Path(r'C:/Users/JAEWAN/projects/yuri-root-pm-r1');PM=PMROOT/'docs/evidence/root-pm-o1'
ref='fd19f8d6cd4efa897ec5338afacfd7939c25b10d';rawpath='docs/evidence/root-pm-o1-original-bind/raw-inventory.json.gz'
addon=Path(r'C:/Program Files/Blender Foundation/Blender 5.2/5.2/scripts/addons_core/io_scene_fbx')
pkg=types.ModuleType('io_scene_fbx');pkg.__path__=[str(addon)];sys.modules['io_scene_fbx']=pkg
from io_scene_fbx.parse_fbx import parse
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf8'))
def write(n,v):
    for p in (E/n,OUT/n):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
inputs=[B/'YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx',N/'metadata/source_renderers_bind.json',N/'metadata/source_expanded_rigs.json',
    PM/'LAPTOP_ORIGINAL_BIND_bind-rest-summary.json',PM/'PM_UNITY_ALL_STORED_RAW_BIND_REVIEW_R1.json',R/'metadata/mesh_slot_UV_attributes_shape_deltas.json']
hashes={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
rawbytes=subprocess.check_output(['git','show',ref+':'+rawpath],cwd=PMROOT)
raw=json.loads(gzip.decompress(rawbytes));unity={r['name']:r for r in raw['carrier']['renderers']}
actual_world={v['path']:np.array(v['world']).reshape(4,4) for v in raw['carrier']['transforms']}
weightfile=N/'reference/source_original_vertex_weights.json.gz';hashes[str(weightfile)]={'sha256':sha(weightfile),'bytes':weightfile.stat().st_size}
with gzip.open(weightfile,'rt',encoding='utf8') as f:source_weights=json.load(f)
source=load(inputs[1]);rigs=load(inputs[2]);basis=load(inputs[3])['basis'];P=np.array(basis['P'],dtype=np.float64);H=np.array(basis['H'],dtype=np.float64)
root,_=parse(str(inputs[0]));sections={x.id:x for x in root.elems};objects={o.props[0]:o for o in sections[b'Objects'].elems}
cons=[tuple(c.props) for c in sections[b'Connections'].elems if c.props[0]==b'OO']
def name(o):return o.props[1].decode(errors='replace').split('\x00')[0]
models={uid:name(o) for uid,o in objects.items() if o.id==b'Model' and o.props[-1]==b'Mesh'}
model_ids={n:uid for uid,n in models.items()}
parent_model={child:parent for _,child,parent,*_ in cons if child in objects and objects[child].id==b'Model' and parent in objects and objects[parent].id==b'Model'}
geometries={models[parent]:objects[child] for _,child,parent,*_ in cons if parent in models and child in objects and objects[child].id==b'Geometry' and objects[child].props[-1]==b'Mesh'}
def field(o,n):return next(c.props[0] for c in o.elems if c.id==n)
def model_properties(uid):
    node=next((c for c in objects[uid].elems if c.id==b'Properties70'),None)
    values={c.props[0].decode():list(c.props[4:]) for c in node.elems if c.id==b'P'} if node else {}
    return {k:values.get(k,default) for k,default in [('Lcl Translation',[0,0,0]),('Lcl Rotation',[0,0,0]),('Lcl Scaling',[1,1,1]),
        ('GeometricTranslation',[0,0,0]),('GeometricRotation',[0,0,0]),('GeometricScaling',[1,1,1]),('RotationOrder',[0]),('PreRotation',[0,0,0]),('PostRotation',[0,0,0]) ]}
def points(p,m):return p@m[:3,:3].T+m[:3,3]
arrays={};reports=[];stored=0;modifierrows=0
def rotation_delta(a,b):
    def polar(m):
        U,_,V=np.linalg.svd(m[:3,:3]);return U@np.diag([1,1,np.linalg.det(U@V)])@V
    D=polar(a).T@polar(b);s=np.array([D[2,1]-D[1,2],D[0,2]-D[2,0],D[1,0]-D[0,1]])/2
    return float(np.degrees(np.arctan2(np.linalg.norm(s),(np.trace(D)-1)/2)))
for r in source:
    n=r['name'];u=unity[n];M=np.array(r['matrix_world']);Mu=np.array(u['world']).reshape(4,4)
    meshfile=R/'data'/f'{n}_original_mesh.npz';hashes[str(meshfile)]={'sha256':sha(meshfile),'bytes':meshfile.stat().st_size}
    orig=np.load(meshfile,allow_pickle=False);sp=orig['positions'].astype(np.float64)
    fp=np.array(field(geometries[n],b'Vertices'),dtype=np.float64).reshape(-1,3);up=np.array(u['vertices'],dtype=np.float64)
    sourcewire=np.max(np.abs(fp-sp)) if fp.shape==sp.shape else None
    poly=np.array(field(geometries[n],b'PolygonVertexIndex'),dtype=np.int64);loopindices=np.where(poly<0,-poly-1,poly)
    topology_equal=np.array_equal(loopindices,orig['loop_vertex_indices'])
    # A world-derived geometry candidate, not fitted from these positions.
    Kworld=np.linalg.inv(Mu)@P@M
    candidates={'local_X_mirror_H':H,'global_source_axis_P':P,'actual_renderer_world_derived':Kworld}
    candidate_results={};maps={}
    for label,K in candidates.items():
        kp=points(sp,K);tree=cKDTree(kp);dist,idx=tree.query(up,workers=1)
        world_delta=np.linalg.norm(points(up,Mu)-points(kp[idx],Mu),axis=1)
        candidate_results[label]={'matrix_K':K.tolist(),'max_mesh_local_nearest_distance':float(dist.max()),
            'max_world_nearest_distance_m':float(world_delta.max()),'RMS_world_m':float(np.sqrt(np.mean(world_delta**2)))}
        maps[label]=(idx,kp,tree)
    selected=min(candidate_results,key=lambda x:candidate_results[x]['max_world_nearest_distance_m'])
    idx,kp,tree=maps[selected];K=candidates[selected];res=candidate_results[selected]
    # Exact spatial ambiguity remains explicit; never silently choose one seam ID.
    hits=tree.query_ball_point(up,1e-6,workers=1);ambiguous=sum(len(v)>1 for v in hits);unmatched=sum(not v for v in hits)
    offsets=[0];candidate_ids=[]
    for v in hits:candidate_ids.extend(sorted(v));offsets.append(len(candidate_ids))
    arrays[n+'_nearest_source_vertex']=idx.astype(np.int32)
    arrays[n+'_candidate_offsets']=np.array(offsets,np.int32);arrays[n+'_candidate_source_vertices']=np.array(candidate_ids,np.int32)
    arrays[n+'_validated_position_candidate_K']=K
    nativeBones=sum(len(x['bone_indices']) for x in r['armature_bindings']);actualBones=len(u['bindposes']);stored+=actualBones;modifierrows+=nativeBones
    primary=r['armature_bindings'][0];native={v['name']:v for v in rigs[primary['target']]['bones']}
    sw=source_weights[n];positive_support=collections.Counter(sw['groups'][g] for row in sw['influences'] for g,v in row if v>0)
    bind_direct=[]
    source_matrices=[];target_matrices=[];bone_name_to_index={}
    for bi,(bone,ub,upath) in enumerate(zip(primary['bone_indices'],u['bindposes'],u['bones'])):
        Bs=np.array(bone['inverse_bind_rest_mesh_to_bone']);Bu=np.array(ub).reshape(4,4)
        bind_direct.append({'bone':bone['name'],'Unity_bone_path':upath,'source_bone_index':bone['index'],
            'positive_source_vertices':positive_support.get(bone['name'],0),
            'inverse_bind_translation_vector_delta':float(np.linalg.norm(Bu[:3,3]-(H@Bs@H)[:3,3])),
            'inverse_bind_rotation_deg':rotation_delta(Bu,H@Bs@H),
            'inverse_bind_max_elements':float(np.max(np.abs(Bu-H@Bs@H)))})
        source_matrices.append(np.array(native[bone['name']]['neutral_evaluated_world'])@Bs)
        target_matrices.append(actual_world[upath]@Bu)
        bone_name_to_index[bone['name']]=bi
    # Bone-normalized first-armature LBS shadows, NOT full DQ/masked/surface proof.
    source_shadow=np.zeros((len(sp),3));totals=np.zeros(len(sp))
    for vi,row in enumerate(sw['influences']):
        for gi,value in row:
            bname=sw['groups'][gi]
            if value>0 and bname in bone_name_to_index:
                source_shadow[vi]+=value*points(sp[vi:vi+1],source_matrices[bone_name_to_index[bname]])[0];totals[vi]+=value
    weighted=totals>0;source_shadow[weighted]/=totals[weighted,None];source_shadow[~weighted]=points(sp[~weighted],M)
    source_shadow=points(source_shadow,P)
    counts=np.frombuffer(base64.b64decode(u['weightCounts']),dtype=np.uint8);assert len(counts)==len(up) and int(counts.sum())==len(u['weights'])
    target_shadow=np.zeros((len(up),3));target_totals=np.zeros(len(up));offset=0
    for vi,count in enumerate(counts):
        for item in u['weights'][offset:offset+int(count)]:
            value=item['weight'];target_shadow[vi]+=value*points(up[vi:vi+1],target_matrices[item['bone']])[0];target_totals[vi]+=value
        offset+=int(count)
    weighted_target=target_totals>0;target_shadow[weighted_target]/=target_totals[weighted_target,None]
    target_shadow[~weighted_target]=points(up[~weighted_target],Mu)
    lbs_error=np.linalg.norm(target_shadow-source_shadow[idx],axis=1)
    sourceworld_error=np.linalg.norm(points(up,Mu)-points(sp[idx],P@M),axis=1)
    canonical_renderer=P@M@H
    canonical_geometry_error=np.linalg.norm(points(up,canonical_renderer)-points(sp[idx],P@M),axis=1)
    ancestor=[];uid=model_ids[n]
    while uid in objects:
        ancestor.append({'name':name(objects[uid]),'properties':model_properties(uid)})
        if uid not in parent_model:break
        uid=parent_model[uid]
    reports.append({'renderer':n,'source_vertices':len(sp),'FBX_control_points':len(fp),'Unity_split_vertices':len(up),
        'actual_FBX_Model_properties_and_ancestry':ancestor,
        'source_raw_positions_vs_FBX_control_point_max_delta':float(sourcewire) if sourcewire is not None else None,
        'FBX_polygon_loop_indices_match_source_exact':bool(topology_equal),'source_mesh_file':str(meshfile),
        'source_modifier_bind_rows':nativeBones,'actual_Unity_stored_bind_rows':actualBones,
        'source_modifier_stages':[{'modifier':m['modifier'],'rig':m['target'],'rows':len(m['bone_indices'])} for m in r['armature_bindings']],
        'basis_candidates':candidate_results,'selected_position_candidate':selected,'position_candidate_max_world_distance_m':res['max_world_nearest_distance_m'],
        'candidate_vertices_without_match_within1e-6_world_local_query':unmatched,'ambiguous_position_only_Unity_vertices':ambiguous,
        'source_geometry_index_verified_at_FBX_stage':sourcewire==0 and topology_equal,
        'Unity_full_vertex_identity_status':'POSITION_CANDIDATE_ONLY; exact split-corner/UV/triangle/ShapeKey correspondence required for ambiguous seams and bind acceptance',
        'actual_renderer_world':Mu.tolist(),'source_renderer_world':M.tolist(),
        'renderer_basis_closure_matrix_max_delta':float(np.max(np.abs(Mu@K-P@M))),
        'raw_unskinned_rendererWorld_geometry_vs_source_world_max_m':float(sourceworld_error.max()),
        'source_unskinned_rest_geometry_diagnostic_NOT_renderer_move_proposal':{'expected_unskinned_source_world':canonical_renderer.tolist(),
            'all_raw_geometry_H_vertices_world_source_nearest_max_m':float(canonical_geometry_error.max()),
            'scope':'UNSKINNED rest geometry condition only. Do NOT move Hair/Body renderer to force this condition or use inverse(Wsource)@actualMu as bind correction without bone/local geometry derivation. Skinned world output and full mapping are separate.'},
        'first_Armature_LBS_shadow_world_diagnostic':{'max_m':float(lbs_error.max()),'RMS_m':float(np.sqrt(np.mean(lbs_error**2))),
            'actual_Unity_zero_weight_vertices':int(np.count_nonzero(~weighted_target)),
            'scope':'Actual carrier OFF raw transforms/weights/bindposes/vertices vs source evaluatedOFF firstArmature bone-normalized LBS. Excludes source DQ/secondArmature/corrective/surface/GN; positional ambiguity not full split-corner/ShapeKey identity proof.'},
        'actual_bind_vs_source_H_bind_H_diagnostic':bind_direct,
        'verdict':'NO_RUNTIME_BIND_FIDELITY_VERDICT; basis and full vertex identity must be validated, both source body passes retained'})
assert stored==1150 and modifierrows==1207
p=OUT/'R4_Renderer_Position_Basis_Candidates_And_Source_Index_Sets.npz';np.savez_compressed(p,**arrays)
manifest={'task_id':'YURI_O1_ALL_BIND_ROW_COUNT_AND_RENDERER_BASIS_DIAGNOSTIC_R1','inputs':hashes,
    'method_sha256':sha(Path(__file__)),
    'corrective_report_sha256':sha(E/'YURI_O1_SKINNED_WORLD_FRAME_AND_ROW_COUNT_CORRECTION_R1.md'),
    'actual_Unity_raw_blob':{'repo_readonly':str(PMROOT),'commit':ref,'path':rawpath,'sha256':hashlib.sha256(rawbytes).hexdigest(),'bytes':len(rawbytes)},
    'actual_Unity_stored_rows':stored,'source_modifier_binding_rows':modifierrows,'body_second_Armature_rows':57,
    'direct_H_bind_rotation_diagnostic_NOT_runtime_verdict':{
        'rows_over_unchanged_0_001_deg':sum(v['inverse_bind_rotation_deg']>.001 for r in reports for v in r['actual_bind_vs_source_H_bind_H_diagnostic']),
        'positive_rows_over':sum(v['inverse_bind_rotation_deg']>.001 and v['positive_source_vertices']>0 for r in reports for v in r['actual_bind_vs_source_H_bind_H_diagnostic']),
        'maximum_firstArmature_LBS_shadow_world_error_m':max(r['first_Armature_LBS_shadow_world_diagnostic']['max_m'] for r in reports)},
    'storage_policy':'1150 distinct stored rows; body secondArmature57 is an additional original deformation pass over same rig, not duplicate storage. Require source DQ+maskedLBS stages independently.',
    'renderers':reports,'files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}],
    'candidate_search_policy':'Declared H/P and exact actual-renderer/source-world-derived affine K candidates. No fitted per-bone corrections; nearest/candidate spatial maps are diagnostics, not an assumed identity remap. All vertices retained; ambiguity sets preserved.',
    'skinning_frame_policy':'Mu@inverse(bindpose) describes renderer-frame recovered bind, not by itself physical skinned world output. For firstArmature LBS, world output is sum(Wbone@bindpose@meshVertex * normalized bone weights); renderer Mu cancels with renderer-local skinning conversion. Actual raw unskinned Mu geometry and actual skinning world shadow are reported separately. Do not change Mu/K/bind based on algebra alone.',
    'corrects_prior_source_contract':'9375af8 Mu*K=G*P*Ms condition is UNSKINNED rest geometry, not a required skinned binding gate by itself. Historical receipt remains; general Bu=Hb*Bs*inverse(K) remains from verified bone/local geometry basis. Mu inversion closure alone is not source-fidelity proof. No renderer move proposed.',
    'missing_full_mapping_fields':'Actual Unity split-corner triangles+UVs/normals/ShapeKey delta and source-FBX-control-point correspondence (existing consumer mapping may supply them). Raw inventory has vertices/weights/bindposes but no triangles/UV/corner data.',
    'raw143_policy':'PM raw 143 rows are diagnostic differences under unvalidated mesh-local/exportbasis. No runtime FAIL assignment from that table. Specific captured R_Middle3 rotation mismatch retained in its verified case context; isolated clone restoration and all1150+bodysecondpass proofs pending.',
    'source_preservation':'No Blender/source/Unity scenes loaded; existing FBX/sourceNPZ and actual frozen Git blob read only. No export/render/bake/product repo writes. No source rig/rest/bones/weights/material changes.',
    'all_input_sha_unchanged':all(sha(x)==v['sha256'] for x,v in ((Path(k),v) for k,v in hashes.items()))}
assert manifest['all_input_sha_unchanged'];write('RENDERER_BASIS_DIAGNOSTIC_MANIFEST.json',manifest)
print('RENDERER_BASIS_COMPLETE',stored,modifierrows,[(r['renderer'],r['selected_position_candidate'],r['position_candidate_max_world_distance_m'],r['ambiguous_position_only_Unity_vertices']) for r in reports],flush=True)
