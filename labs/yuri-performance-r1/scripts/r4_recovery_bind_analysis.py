"""Separate rest transport, pure LBS, and native procedural deformation effects.
Uses preserved original arrays/weights and native/FBX saved matrices, not rig edits.
"""
import bpy,sys,json,gzip,math,hashlib
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1');OLD=OUT.parent/'o1-native-unity-probe-r1'
def load(p):return json.loads(p.read_text(encoding='utf8'))
def gz(p):
    with gzip.open(p,'rt',encoding='utf8') as f:return json.load(f)
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.write_text(json.dumps(v,indent=2),encoding='utf8')
source_rigs=load(OLD/'metadata/source_expanded_rigs.json');renderers=load(OLD/'metadata/source_renderers_bind.json');imported={r['name']:r for r in load(OLD/'metadata/imported_renderer_bind.json')};weights=gz(OLD/'reference/source_original_vertex_weights.json.gz');refs=gz(OLD/'reference/native_evaluated_all_frames.json.gz')
meshmeta={r['renderer']:r for r in load(E/'mesh_slot_UV_attributes_shape_deltas.json')}
matrices={n:{b['name']:np.array(b['world_rest']) for b in r['bones']} for n,r in source_rigs.items()};neutral={n:{b['name']:np.array(b['neutral_evaluated_world']) for b in r['bones']} for n,r in source_rigs.items()}
driver_refs=load(E/'evaluated_driver_geometry_references.json');neutraldata=np.load(OUT/'data/neutral.npz')
def stats(d):
    norm=np.linalg.norm(d,axis=1);return {'max_m':float(norm.max()),'RMS_m':float(np.sqrt(np.mean(norm*norm))),'p50_m':float(np.percentile(norm,50)),'p95_m':float(np.percentile(norm,95)),'p99_m':float(np.percentile(norm,99)),'worst_vertex':int(norm.argmax())}
contexts=[];mask=[];support=[]
for r in renderers:
    n=r['name'];meta=meshmeta[n];p=np.load(OUT/meta['file']['path'])['positions'].astype(np.float64);points=np.column_stack([p,np.ones(len(p))]);m=np.array(r['matrix_world']);im=np.array(imported[n]['matrix_world']);first=r['armature_bindings'][0];rig=first['target'];active={b['name'] for b in source_rigs[rig]['bones'] if b['deform']};g=weights[n]['groups'];influences=weights[n]['influences'];bybone={};tot=np.zeros(len(p));sourcebind={b['name']:np.array(b['inverse_bind_rest_mesh_to_bone']) for b in first['bone_indices']};ib=imported[n]['armature_bindings'][0];importbind={b['name']:np.array(b['inverse_bind_rest_mesh_to_bone']) for b in ib['bone_indices']}
    for index,rows in enumerate(influences):
        for group,w in rows:
            name=g[group]
            if name in active and w>0:bybone.setdefault(name,[]).append((index,w));tot[index]+=w
    bybone={b:(np.array([x[0] for x in a]),np.array([x[1] for x in a])) for b,a in bybone.items()}
    bind_residual=[]
    modelbones={b['name']:np.array(b['world_rest']) for b in load(OLD/'metadata/imported_model_expanded_rigs.json')[rig]['bones']}
    for b,bind in importbind.items():
        relation=np.linalg.inv(im)@modelbones[b]@bind;converted_source=sourcebind[b]
        bind_residual.append({'bone':b,'bind_identity_matrix_max_element_delta':float(np.max(np.abs(relation-np.eye(4)))),'import_inversebind_vs_source_max_element_delta':float(np.max(np.abs(bind-converted_source)))})
    def lbs(poses,binds,meshworld):
        result=np.zeros((len(p),4));used=tot>0
        for b,(ids,w) in bybone.items():result[ids]+=(points[ids]@(poses[b]@binds[b]).T)*(w/tot[ids])[:,None]
        result[~used]=points[~used]@meshworld.T;return result[:,:3]
    contexts.append((r,points,bybone,tot,lbs,sourcebind,importbind,m,im,rig))
    # Bind/OFF use closure immediately. ON later rebuilds local closure explicitly.
    rawworld=points@m.T;bindout=lbs(matrices[rig],sourcebind,m);offout=lbs(neutral[rig],sourcebind,m)
    write(n+'_bind_and_OFF_LBS.json',{'renderer':n,'bind_identity_residual_by_bone':bind_residual,'source_pure_LBS_at_raw_rest_vs_undeformed_world':stats(bindout-rawworld[:,:3]),'source_pure_LBS_at_evaluated_OFF_vs_native_evaluated_geometry':stats(offout-neutraldata[n+'_world_position']),'method':'normalized positive deform-bone weights; first armature only; pure LBS diagnostic, not DQ/masked second armature/GN/surface replay'})
    for group in g:
        if group in active:continue
        values=np.zeros(len(p))
        for index,a in enumerate(influences):
            for gi,w in a:
                if g[gi]==group:values[index]=w
        if group.startswith('R3_'):mask.append({'renderer':n,'group':group,'nonzero_vertices':int(np.count_nonzero(values)),'min':float(values.min()),'max':float(values.max()),'exact_pointer':'frozen ZIP4ec5c10... reference/source_original_vertex_weights.json.gz; groups index→influences pervertex','usage':[mod['name'] for mod in meta['modifiers'] if mod['settings'].get('vertex_group')==group]})
    for target_rig,bone in [('Meshy_Fitted_Rig','thigh.L'),('Armature','J_Bip_L_Index3'),('Hair_Rig_R4','Hair_Pony_03')]:
        if rig!=target_rig:continue
        descendants={bone};changed=True
        while changed:
            prior=len(descendants);descendants.update(b['name'] for b in source_rigs[rig]['bones'] if b['parent'] in descendants);changed=len(descendants)>prior
        influenced=set()
        for b in descendants:
            if b in bybone:influenced.update(bybone[b][0].tolist())
        support.append({'rig':rig,'bone':bone,'renderer':n,'descendants':sorted(descendants),'positive_skin_influenced_vertex_count':len(influenced),'bone_deform':next(b['deform'] for b in source_rigs[rig]['bones'] if b['name']==bone),'matrix_gate_is_independent_of_influence_count':True})
write('exact_mask_coverage.json',mask);write('worst_rest_bone_skin_support.json',support)
# Fresh existing scratch carrier. No additional export or source mutation.
bpy.ops.wm.open_mainfile(filepath=str(OLD/'YURI_O1_R4_NATIVE_IMPORTED_QA_20261003_R1.blend'),use_scripts=False);s=bpy.context.scene;inv=load(OLD/'metadata/take_and_slot_inventory.json');reports=[]
for clip in inv:
    action=clip['authored_Action']
    for v in clip['imported_rig_actions']:
        o=bpy.data.objects[v['rig']];a=bpy.data.actions[v['action']];o.animation_data_create();o.animation_data.action=a;o.animation_data.action_slot=next(x for x in a.slots if x.identifier==v['slot'])
    end=len(refs[action]);samples=sorted({1,1+round((end-1)*.25),1+round((end-1)*.5),end})
    for f in samples:
        s.frame_set(f);bpy.context.view_layer.update()
        for r,points,bybone,tot,unused,sbind,ibind,m,im,rig in contexts:
            nativepose={b:np.array(v['world_matrix']) for b,v in refs[action][f-1][rig].items()};o=bpy.data.objects[rig];targetpose={b.name:np.array(o.matrix_world@b.matrix) for b in o.pose.bones}
            def compute(poses,binds,matrix):
                result=np.zeros_like(points);used=tot>0
                for b,(ids,w) in bybone.items():result[ids]+=(points[ids]@(poses[b]@binds[b]).T)*(w/tot[ids])[:,None]
                result[~used]=points[~used]@matrix.T;return result[:,:3]
            source=compute(nativepose,sbind,m);target=compute(targetpose,ibind,im);row={'action':action,'frame':f,'renderer':r['name'],'pure_LBS_source_vs_import_transport':stats(target-source)}
            # Match full native evaluated geometry from frozen packet, independent
            # of pure LBS transport; original stable vertex indices used.
            reports.append(row)
write('LBS_bind_motion_transport_metrics.json',{'method':'float64 numpy matrix products; source weights and original mesh-local vertices; first-armature LBS shadow only; source DQ/GN are separate','samples':reports,'scale_policy':'original matrices include0.535 exactly once; world-space meters','normal_speed_fidelity':'Existing complete videos remain HOLD; these matrices do not waive visual/rotation/static gates'})
# Quantify the known full-native-versus-FBX mesh deficit beyond only max error.
native_geometry=gz(OLD/'reference/native_evaluated_motion_geometry_0_25_50_100.json.gz');full=[];deps=bpy.context.evaluated_depsgraph_get()
for clip in inv:
    action=clip['authored_Action']
    for v in clip['imported_rig_actions']:
        o=bpy.data.objects[v['rig']];a=bpy.data.actions[v['action']];o.animation_data.action=a;o.animation_data.action_slot=next(x for x in a.slots if x.identifier==v['slot'])
    for frame,meshes in native_geometry[action].items():
        s.frame_set(int(frame));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        for n,reference in meshes.items():
            o=bpy.data.objects[n];ev=o.evaluated_get(deps);mesh=ev.to_mesh();p=np.empty((len(mesh.vertices),3),np.float32);mesh.vertices.foreach_get('co',p.reshape(-1));mw=np.array(ev.matrix_world);world=p@mw[:3,:3].T+mw[:3,3];row={'action':action,'frame':int(frame),'renderer':n,**stats(world-np.array(reference))};full.append(row);ev.to_mesh_clear()
write('full_deformation_RMS_percentiles.json',{'method':'same indexed source/import world vertices; source native DQ+maskedLBS/GN versus actual frozen FBX modifier state','samples':full,'largest':sorted(full,key=lambda r:r['max_m'],reverse=True)[:10]})
print('BIND_DEFORMATION_ANALYSIS_COMPLETE',len(reports),len(full))
