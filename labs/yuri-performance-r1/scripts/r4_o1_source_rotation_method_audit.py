"""Read frozen reference and imported scratch; never export/save/mutate source.
All 137 bones, 384 endpoint-inclusive samples. CPU factory process only.
Run Blender --factory-startup --background --disable-autoexec --python this.py.
"""
import bpy, gzip, json, math, hashlib
from pathlib import Path
import numpy as np
from mathutils import Matrix

LAB = Path(__file__).resolve().parent.parent
BASE = Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OLD = BASE/'o1-original-bind-serialization-r1'
OUT = BASE/'o1-source-rotation-method-audit-r1'
E = LAB/'evidence/o1-source-rotation-method-audit-r1'
OUT.mkdir(parents=True, exist_ok=True); E.mkdir(parents=True, exist_ok=True)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def write(name, data):
    for p in (E/name, OUT/name):p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
inputs = [LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend',
    OLD/'YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx',
    OLD/'YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx',
    OLD/'YURI_O1_R4_NATIVE_IMPORTED_QA_20261003_R1.blend',
    OLD/'reference/native_evaluated_all_frames.json.gz',
    OLD/'metadata/take_and_slot_inventory.json',
    LAB/'evidence/o1-original-bind-serialization-r1/motion_position_rotation_fidelity.json',
    Path(r'C:/YuriTransfer/outbox/YURI_O1_R4_ORIGINAL_BIND_SERIALIZATION_20261003_R1_5a04a57f3b47.zip'),
    LAB/'evidence/o1-original-bind-serialization-r1/BONE_RECONSTRUCTION_DIAGNOSTIC.json',
    LAB/'evidence/o1-original-bind-serialization-r1/EXACT_BIND_WIRE_RECEIPT.json']
before={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
with gzip.open(inputs[4],'rt',encoding='utf8') as f:refs=json.load(f)
inventory=json.loads(inputs[5].read_text(encoding='utf8'))
bpy.ops.wm.open_mainfile(filepath=str(inputs[3]),use_scripts=False)
rigs=['Meshy_Fitted_Rig','Armature','Hair_Rig_R4','AVATAR_FaceBoard']
objects={n:bpy.data.objects[n] for n in rigs}
bones=[(n,b.name) for n,o in objects.items() for b in o.pose.bones]
assert len(bones)==137
source=[];actual=[];actual64=[];qs=[];qt=[];ids=[]
for ci,clip in enumerate(inventory):
    name=clip['authored_Action'];frames=refs[name];end=len(frames)
    for o in objects.values():
        if o.animation_data:o.animation_data.action=None
        for b in o.pose.bones:b.matrix_basis=Matrix.Identity(4)
    for item in clip['imported_rig_actions']:
        o=objects[item['rig']];a=bpy.data.actions[item['action']]
        o.animation_data_create();o.animation_data.action=a
        o.animation_data.action_slot=next(s for s in a.slots if s.identifier==item['slot'])
    count=2*(end-1)+1 if 'Loop' in name else end
    for sample in range(1,count+1):
        local=1+(sample-1)%(end-1) if 'Loop' in name and sample>end else sample
        bpy.context.scene.frame_set(local);bpy.context.view_layer.update()
        for bi,(rig,bone) in enumerate(bones):
            o=objects[rig];b=o.pose.bones[bone]
            a=o.matrix_world@b.matrix;r=Matrix(frames[local-1][rig][bone]['world_matrix'])
            source.append(np.array(r,dtype=np.float64));actual.append(np.array(a,dtype=np.float64))
            actual64.append(np.array(o.matrix_world,dtype=np.float64)@np.array(b.matrix,dtype=np.float64))
            qs.append(list(r.to_quaternion()));qt.append(list(a.to_quaternion()));ids.append((ci,sample,local,bi))
    print('CAPTURED',name,count,flush=True)
source=np.array(source);actual=np.array(actual);actual64=np.array(actual64)
qs=np.array(qs);qt=np.array(qt);ids=np.array(ids,dtype=np.int32)
assert len(ids)==137*384
np.savez_compressed(OUT/'frozen_evaluated_matrix_buffers.npz',source_world=source,
    imported_world_float32_product=actual,imported_world_float64_product=actual64,
    source_mathutils_quaternion_wxyz=qs,imported_mathutils_quaternion_wxyz=qt,ids=ids)
def polar(m):
    u,s,vh=np.linalg.svd(m[:,:3,:3]);d=np.linalg.det(u@vh)
    fix=np.ones((len(m),3));fix[:,2]=d
    return (u*fix[:,None,:])@vh,s,d
def quaternion(r):
    # Stable double matrix-to-quaternion; no mathutils float conversion.
    out=np.empty((len(r),4))
    for i,m in enumerate(r):
        tr=np.trace(m)
        if tr>0:
            s=2*math.sqrt(tr+1);q=[s/4,(m[2,1]-m[1,2])/s,(m[0,2]-m[2,0])/s,(m[1,0]-m[0,1])/s]
        else:
            k=int(np.argmax(np.diag(m)));j=(k+1)%3;l=(k+2)%3
            s=2*math.sqrt(max(0,1+m[k,k]-m[j,j]-m[l,l]));q=[0.,0.,0.,0.]
            q[0]=(m[l,j]-m[j,l])/s;q[k+1]=s/4;q[j+1]=(m[j,k]+m[k,j])/s;q[l+1]=(m[l,k]+m[k,l])/s
        out[i]=q
    return out/np.linalg.norm(out,axis=1)[:,None]
def qangle(a,b):
    a=a/np.linalg.norm(a,axis=1)[:,None];b=b/np.linalg.norm(b,axis=1)[:,None]
    return np.degrees(2*np.arccos(np.clip(np.abs(np.sum(a*b,axis=1)),0,1)))
rs,ss,ds=polar(source);ra,sa,da=polar(actual);ra64,_,_=polar(actual64)
new=qangle(quaternion(rs),quaternion(ra));new64=qangle(quaternion(rs),quaternion(ra64))
relative=np.transpose(rs,(0,2,1))@ra
skew=np.stack((relative[:,2,1]-relative[:,1,2],relative[:,0,2]-relative[:,2,0],relative[:,1,0]-relative[:,0,1]),axis=1)/2
matrix_angle=np.degrees(np.arctan2(np.linalg.norm(skew,axis=1),(np.trace(relative,axis1=1,axis2=2)-1)/2))
legacy=qangle(qs,qt)
# Exact earlier Python reduction order, so Index3 receipt reproduces bit-for-bit.
legacy_python=np.array([math.degrees(2*math.acos(min(1,max(0,abs(sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(y*y for y in b)))))))) for a,b in zip(qs,qt)])
position=np.linalg.norm(actual[:,:3,3]-source[:,:3,3],axis=1)
# Stable small-angle independent quaternion distance: avoids acos near-one floor.
qa=quaternion(rs);qb=quaternion(ra);qb*=np.where(np.sum(qa*qb,axis=1)<0,-1,1)[:,None]
stable_q=np.degrees(4*np.arctan2(np.linalg.norm(qa-qb,axis=1),np.linalg.norm(qa+qb,axis=1)))
# Rest reconstruction evidence was already frozen. Read matrices, no source open.
rest=json.loads(inputs[8].read_text(encoding='utf8'))['all_bones']
rsource=np.array([v['source']['matrix_world'] for v in rest],dtype=np.float64)
rimport=np.array([v['imported_reconstructed']['matrix_world'] for v in rest],dtype=np.float64)
rp,_,_=polar(rsource);ri,_,_=polar(rimport);re=qangle(quaternion(rp),quaternion(ri))
write('REST_RECONSTRUCTION_METHOD_COMPARISON.json',{'all_bones':[{'rig':v['rig'],'bone':v['bone'],
    'legacy_deg':v['world_rest_rotation_error_deg'],'polar_float64_deg':float(re[i])} for i,v in enumerate(rest)],
    'worst':{'rig':rest[int(np.argmax(re))]['rig'],'bone':rest[int(np.argmax(re))]['bone'],'polar_float64_deg':float(re.max())},
    'meaning':'Residual exists in saved imported reconstructed rest matrices too. Exact FBX bind transport is independently verified by unchanged wire receipt; no rest/bind offset correction applied.'})
def case(i):
    ci,sample,frame,bi=map(int,ids[i]);rig,bone=bones[bi]
    return {'action':inventory[ci]['authored_Action'],'sample':sample,'frame':frame,'rig':rig,'bone':bone,
        'legacy_float32_decomposition_double_dot_deg':float(legacy_python[i]),
        'polar_float64_quaternion_2acos_deg':float(new[i]),'polar_matrix_atan2_deg':float(matrix_angle[i]),
        'polar_double_product_quaternion_deg':float(new64[i]),'position_m':float(position[i])}
old_index=next(i for i,row in enumerate(ids) if tuple(row)==(0,17,17,bones.index(('Armature','J_Bip_L_Index3'))))
details=case(old_index)
details.update({'source_world':source[old_index].tolist(),'imported_world':actual[old_index].tolist(),
    'source_legacy_quaternion_wxyz':qs[old_index].tolist(),'imported_legacy_quaternion_wxyz':qt[old_index].tolist(),
    'source_polar_quaternion_wxyz':quaternion(rs[old_index:old_index+1])[0].tolist(),
    'imported_polar_quaternion_wxyz':quaternion(ra[old_index:old_index+1])[0].tolist(),
    'source_singular_values':ss[old_index].tolist(),'imported_singular_values':sa[old_index].tolist(),
    'source_axis_normalized_orthogonality_residual':float(np.max(np.abs((source[old_index,:3,:3]/np.linalg.norm(source[old_index,:3,:3],axis=0)).T@(source[old_index,:3,:3]/np.linalg.norm(source[old_index,:3,:3],axis=0))-np.eye(3))))})
write('INDEX3_STARTLE_FRAME17_METHOD_COMPARISON.json',details)
clips=[]
for ci,clip in enumerate(inventory):
    ix=np.flatnonzero(ids[:,0]==ci)
    clips.append({'action':clip['authored_Action'],'samples':len(ix)//137,
        'legacy_worst':case(int(ix[np.argmax(legacy_python[ix])])),
        'polar_worst':case(int(ix[np.argmax(new[ix])])),
        'matrix_angle_max_deg':float(matrix_angle[ix].max()),'position_max_m':float(position[ix].max()),
        'rotation_PASS':bool(new[ix].max()<.001),'position_PASS':bool(position[ix].max()<1e-4)})
per_bone=[]
for bi,(rig,bone) in enumerate(bones):
    ix=np.flatnonzero(ids[:,3]==bi)
    per_bone.append({'rig':rig,'bone':bone,'samples':len(ix),'polar_worst':case(int(ix[np.argmax(new[ix])])),
        'legacy_max_deg':float(legacy_python[ix].max()),'position_max_m':float(position[ix].max())})
write('ALL_137_BONES_384_SAMPLES.json',{'clips':clips,'per_bone':per_bone})
after={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
assert before==after
receipt={'task_id':'YURI_O1_SOURCE_ROTATION_METHOD_AUDIT_R1','inputs':before,'input_bytes_unchanged':True,
    'actions':6,'bones':137,'clip_samples':384,'bone_samples':len(ids),'unique_clip_frames':sum(map(len,refs.values())),
    'buffers':{'path':str(OUT/'frozen_evaluated_matrix_buffers.npz'),'sha256':sha(OUT/'frozen_evaluated_matrix_buffers.npz'),'dtype':'float64 container of exact float32 evaluated source/import values; separate float64 multiplication diagnostic; ids int32','index_bones':bones,'index_actions':[v['authored_Action'] for v in inventory]},
    'thresholds_unchanged':{'position_m_less_than':1e-4,'rotation_deg_less_than':.001},
    'legacy_worst':case(int(np.argmax(legacy_python))),'polar_worst':case(int(np.argmax(new))),
    'matrix_angle_worst':case(int(np.argmax(matrix_angle))),
    'polar_float64_product_max_deg':float(new64.max()),'position_max_m':float(position.max()),
    'quaternion_matrix_angle_max_absolute_difference_deg':float(np.max(np.abs(new-matrix_angle))),
    'stable_quaternion_matrix_angle_max_absolute_difference_deg':float(np.max(np.abs(stable_q-matrix_angle))),
    'stable_quaternion_max_deg':float(stable_q.max()),
    'causal_verdict':'Blender reconstructed/evaluated transform residual remains after float64 polar/SVD. Float32 quaternion decomposition artifact does not explain the failure. Exact earlier worst reproduced; polar vs legacy at that case differs about 1.1e-6 degree. Saved rest reconstruction also retains discrepancy. Unity uses a different importer; its lower independently reported result is not contradicted or certified by this Blender audit.',
    'determinant_signs_source':sorted(set(np.sign(ds).tolist())),'determinant_signs_import':sorted(set(np.sign(da).tolist())),
    'minimum_singular_value_source':float(ss.min()),'minimum_singular_value_import':float(sa.min()),
    'method':'SVD in numpy float64: U diag(1,1,det(U Vt)) Vt; stable normalized float64 wxyz quaternion; 2acos(abs(dot)); independent relative-matrix atan2 skew/trace angle. Original float32 matrices and legacy quaternions retained.',
    'coordinate_policy':'Common Blender world basis (Z-up, meters) unchanged, full hierarchy/scale evaluated before decomposition. No Unity P/H assumed. Orthogonal basis conjugation preserves SO(3) distance; source P*world*H vs Unity actual Transform requires consumer buffers for direct numerical comparison.',
    'operations':'read frozen native matrices + load original-bind importer scratch read-only; assign existing Actions in disposable process; no exporter/render/bake/save/source file load',
    'rotation_PASS':bool(new.max()<.001),'position_PASS':bool(position.max()<1e-4),
    'scope':'Measurement-method audit only; previous FAIL record retained. No appearance, Unity, F2/F3, foot contact or material certification.'}
write('ROTATION_METHOD_AUDIT_RECEIPT.json',receipt)
print('AUDIT_COMPLETE',receipt['legacy_worst'],receipt['polar_worst'],flush=True)
