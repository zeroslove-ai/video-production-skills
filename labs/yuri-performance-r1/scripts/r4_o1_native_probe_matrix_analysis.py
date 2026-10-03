"""Analyze saved matrices and scratch imported Actions, no re-export or source edit.
Double-precision normalized quaternion dot avoids Quaternion.angle float floor.
Position budget 1e-4m unchanged; independent rotation budget 0.001 degree.
"""
import bpy,json,sys,gzip,math
from pathlib import Path
from mathutils import Matrix
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-native-unity-probe-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-unity-probe-r1')
def load(n):return json.loads((E/n).read_text(encoding='utf8'))
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.write_text(json.dumps(v,indent=2),encoding='utf8')
def angle(a,b):
    qa=list(a.to_quaternion());qb=list(b.to_quaternion());na=math.sqrt(sum(v*v for v in qa));nb=math.sqrt(sum(v*v for v in qb))
    dot=abs(sum(x*y for x,y in zip(qa,qb))/(na*nb));return math.degrees(2*math.acos(min(1,max(0,dot))))
def delta(a,b):
    a=Matrix(a);b=Matrix(b);pa,qa,sa=a.decompose();pb,qb,sb=b.decompose();index=max(((i,j) for i in range(4) for j in range(4)),key=lambda ij:abs(a[ij[0]][ij[1]]-b[ij[0]][ij[1]]))
    return {'max_matrix_element_delta':abs(a[index[0]][index[1]]-b[index[0]][index[1]]),'element_row_column':list(index),'translation_delta_m':(pa-pb).length,'rotation_delta_deg_double_dot':angle(a,b),'max_scale_component_delta':max(abs(x-y) for x,y in zip(sa,sb))}
source=load('source_expanded_rigs.json');model=load('imported_model_expanded_rigs.json');animation=load('imported_animation_expanded_rigs.json');rigs=list(source);comparisons=[]
for n in rigs:
    native={b['name']:b for b in source[n]['bones']};mb={b['name']:b for b in model[n]['bones']};ab={b['name']:b for b in animation[n]['bones']}
    for name in native:
        row={'rig':n,'bone':name,'source_vs_model_local_rest':delta(native[name]['local_rest'],mb[name]['local_rest']),'model_vs_animation_local_rest':delta(mb[name]['local_rest'],ab[name]['local_rest']),'source_vs_model_world_rest':delta(native[name]['world_rest'],mb[name]['world_rest']),'source_vs_animation_world_rest':delta(native[name]['world_rest'],ab[name]['world_rest']),'model_vs_animation_world_rest':delta(mb[name]['world_rest'],ab[name]['world_rest'])}
        comparisons.append(row)
write('rest_matrix_decomposed_by_bone.json',{'method':'matrix translation in meters, normalized quaternion dot computed with Python double, decomposed scale; bone-axis geometry also retained in full input matrices','unchanged_local_rest_threshold':1e-5,'bones':comparisons,'largest_local_pair_discrepancies':sorted(comparisons,key=lambda r:r['model_vs_animation_local_rest']['max_matrix_element_delta'],reverse=True)[:10]})
with gzip.open(OUT/'reference/native_evaluated_all_frames.json.gz','rt',encoding='utf8') as f:refs=json.load(f)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'YURI_O1_R4_NATIVE_IMPORTED_QA_20261003_R1.blend'),use_scripts=False)
s=bpy.context.scene;objects={n:bpy.data.objects[n] for n in rigs};inv=load('take_and_slot_inventory.json');reports=[]
for clip in inv:
    name=clip['authored_Action']
    for v in clip['imported_rig_actions']:
        o=objects[v['rig']];a=bpy.data.actions[v['action']];o.animation_data_create();o.animation_data.action=a;o.animation_data.action_slot=next(x for x in a.slots if x.identifier==v['slot'])
    maximum_position=0;maximum_rotation=0;worst=None;per_rig={n:{'position_m':0,'rotation_deg':0} for n in rigs}
    for f,frame in enumerate(refs[name],1):
        s.frame_set(f);bpy.context.view_layer.update()
        for n,o in objects.items():
            for b in o.pose.bones:
                a=o.matrix_world@b.matrix;r=Matrix(frame[n][b.name]['world_matrix']);position=(a.translation-r.translation).length;rotation=angle(a,r)
                if rotation>maximum_rotation:maximum_rotation=rotation;worst={'rig':n,'bone':b.name,'frame':f}
                maximum_position=max(maximum_position,position);per_rig[n]['position_m']=max(per_rig[n]['position_m'],position);per_rig[n]['rotation_deg']=max(per_rig[n]['rotation_deg'],rotation)
    reports.append({'action':name,'frames':len(refs[name]),'max_position_error_m':maximum_position,'max_rotation_error_deg_double_dot':maximum_rotation,'worst_rotation_sample':worst,'by_rig':per_rig,'position_threshold_m':1e-4,'rotation_threshold_deg':.001,'PASS':maximum_position<1e-4 and maximum_rotation<.001})
write('motion_position_rotation_fidelity.json',{'method':'normalized quaternion dot in Python double; q and -q equivalent; Blender matrix/quat storage remains float32; budget fixed before these measurements','clips':reports,'PASS':all(r['PASS'] for r in reports)})
receipt=load('roundtrip_receipt.json');receipt['source_pose_fidelity_PASS']=all(r['PASS'] for r in reports);receipt['source_pose_fidelity_criteria']={'max_world_position_error_m_less_than':1e-4,'max_world_rotation_error_degrees_less_than':.001,'rotation_measurement':'normalized quaternion double dot; absolute sign'};write('roundtrip_receipt.json',receipt)
print('MATRIX_ANALYSIS_COMPLETE',[(r['action'],r['max_rotation_error_deg_double_dot'],r['PASS']) for r in reports],flush=True)
