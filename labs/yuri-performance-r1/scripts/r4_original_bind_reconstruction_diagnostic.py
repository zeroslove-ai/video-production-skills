"""Read original/rest versus imported reconstructed bone geometry; no edits."""
import bpy,json,sys,math
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-original-bind-serialization-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-bind-serialization-r1')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),use_scripts=False)
def angle(a,b):
    qa=np.array(a.to_quaternion(),dtype=np.float64);qb=np.array(b.to_quaternion(),dtype=np.float64);v=abs(float(qa@qb)/(np.linalg.norm(qa)*np.linalg.norm(qb)));return math.degrees(2*math.acos(min(1,v)))
def info(o,b):
    m=o.matrix_world@b.matrix_local;basis=np.array(b.matrix_local)[:3,:3];return {'head_local':list(b.head_local),'tail_local':list(b.tail_local),'length':b.length,'matrix_armature':[[v for v in r] for r in b.matrix_local],'matrix_world':[[v for v in r] for r in m],'basis_determinant':float(np.linalg.det(basis)),'basis_orthogonality_residual':float(np.max(np.abs(basis.T@basis-np.eye(3)))),'basis_singular_values':np.linalg.svd(basis,compute_uv=False).tolist()}
original={n:{b.name:info(bpy.data.objects[n],b) for b in bpy.data.objects[n].data.bones} for n in ('Meshy_Fitted_Rig','Armature','Hair_Rig_R4','AVATAR_FaceBoard')}
bpy.ops.wm.open_mainfile(filepath=str(OUT/'YURI_O1_R4_NATIVE_IMPORTED_QA_20261003_R1.blend'),use_scripts=False)
from mathutils import Matrix
rows=[]
for rig,bones in original.items():
    obj=bpy.data.objects[rig]
    for name,source in bones.items():
        imported=info(obj,obj.data.bones[name]);sm=Matrix(source['matrix_world']);im=Matrix(imported['matrix_world'])
        rows.append({'rig':rig,'bone':name,'source':source,'imported_reconstructed':imported,'world_rest_rotation_error_deg':angle(sm,im),'world_rest_position_delta_m':(sm.translation-im.translation).length,'source_import_tail_local_delta_m':float(np.linalg.norm(np.array(source['tail_local'])-np.array(imported['tail_local']))),'source_import_head_local_delta_m':float(np.linalg.norm(np.array(source['head_local'])-np.array(imported['head_local'])))})
result={'source_file_unchanged':True,'raw_bind_rest_transported':'EXACT_BIND_WIRE_RECEIPT verified separately; no native rig edits','basis_measurement':'Original Blender stored bone geometry versus fresh FBX importer reconstructed bones, armature-local plus world; double normalized quaternion dot','largest_world_rest_rotation_discrepancies':sorted(rows,key=lambda x:x['world_rest_rotation_error_deg'],reverse=True)[:10],'all_bones':rows,'causal_limit':'Importer builds normalized bones from bind/head/child direction and decomposed correction matrices; this records the observable reconstruction residual. Does not claim a specific single float operation is the complete cause or change Blender importer.','source_preserving_alternative':'Retain original .blend Action/NLA and exact native sampled matrices as authoring fallback. For future Unity custody, consumer measures its own importer raw bind/default/reconstructed Transform against source; Blender reconstruction failure is not proof of Unity equivalence or failure. No rest rewrite/offset compensation authorized.'}
for p in (E/'BONE_RECONSTRUCTION_DIAGNOSTIC.json',OUT/'metadata/BONE_RECONSTRUCTION_DIAGNOSTIC.json'):p.write_text(json.dumps(result,indent=2),encoding='utf8')
print('RECONSTRUCTION_DIAGNOSTIC',[(r['rig'],r['bone'],r['world_rest_rotation_error_deg']) for r in result['largest_world_rest_rotation_discrepancies'][:3]])
