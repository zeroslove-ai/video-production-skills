"""All-frame evaluated mesh health and sampled hand surface overlaps.
No physics/contact implementation; BVH overlap is a diagnostic, not penetration depth.
"""
from pathlib import Path
import bpy,json,math,sys,numpy as np
from collections import Counter
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];reports=[]
experiment='please_elbow' in sys.argv or 'please_wrist_delay' in sys.argv
experiment_folder='native-body-r4-wrist-delay' if 'please_wrist_delay' in sys.argv else 'native-body-r3-please-elbow'
configs=[(experiment_folder,('please_tilt',))] if experiment else [('native-body-r3',('greeting_wave','shy_lookaway')),('native-body-r3-please-hands',('please_tilt',))]
for folder,clips in configs:
    E=ROOT/('evidence/'+folder);meta=json.loads((E/'build_receipt.json').read_text());bpy.ops.wm.open_mainfile(filepath=meta['candidate']);s=bpy.context.scene;r=bpy.data.objects['Armature'];head=bpy.data.objects['Character_Body_Head']
    meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.hide_render]
    hand_sets={}
    for side in ('L','R'):
        groups={g.index for g in head.vertex_groups if g.name.startswith('J_Bip_'+side+'_') and any(x in g.name for x in ('Hand','Index','Middle','Ring','Little','Thumb'))}
        hand_sets[side]={v.index for v in head.data.vertices if any(g.group in groups and g.weight>.2 for g in v.groups)}
    polygons={side:[list(p.vertices) for p in head.data.polygons if all(v in hand_sets[side] for v in p.vertices)] for side in ('L','R')}
    hand_union=hand_sets['L']|hand_sets['R'];polygons['body']=[list(p.vertices) for p in head.data.polygons if not any(v in hand_union for v in p.vertices)]
    for clip in clips:
        r.animation_data.action=bpy.data.actions[meta['action_registry'][clip]];previous={};bounds=[];max_step=0.;contacts=[];tested=0
        for frame in range(1,122):
            s.frame_set(frame);deps=bpy.context.evaluated_depsgraph_get();lo=np.array([np.inf]*3);hi=-lo
            for o in meshes:
                evaluated=o.evaluated_get(deps);data=evaluated.data
                xyz=np.empty(len(data.vertices)*3,dtype=np.float32);data.vertices.foreach_get('co',xyz);xyz=xyz.reshape(-1,3)
                assert np.isfinite(xyz).all(),(clip,frame,o.name)
                m=np.array(evaluated.matrix_world,dtype=np.float32);xyz=xyz@m[:3,:3].T+m[:3,3]
                if o.name in previous:
                    assert xyz.shape==previous[o.name].shape,'Unexpected topology change'
                    max_step=max(max_step,float(np.linalg.norm(xyz-previous[o.name],axis=1).max()))
                previous[o.name]=xyz.copy();lo=np.minimum(lo,xyz.min(axis=0));hi=np.maximum(hi,xyz.max(axis=0));tested+=len(xyz)
                if o==head and frame in (1,25,49,61,73,97,121):
                    assert len(xyz)==len(head.data.vertices)
                    trees={name:BVHTree.FromPolygons(xyz.tolist(),faces,all_triangles=False,epsilon=0.) for name,faces in polygons.items()}
                    record={'frame':frame,'left_right_hand_triangle_overlap_pairs':len(trees['L'].overlap(trees['R']))}
                    for side,label in (('L','left'),('R','right')):
                        pairs=trees[side].overlap(trees['body']);regions=Counter()
                        for _,body_id in pairs:
                            weights=Counter()
                            for index in polygons['body'][body_id]:
                                for g in head.data.vertices[index].groups:
                                    name=head.vertex_groups[g.group].name
                                    if name in r.data.bones and r.data.bones[name].use_deform:weights[name]+=g.weight
                            regions[weights.most_common(1)[0][0] if weights else 'NO_DEFORM_GROUP']+=1
                        record[label+'_hand_body_overlap_pairs']=len(pairs);record[label+'_body_regions_by_dominant_skin_group']=dict(regions)
                    contacts.append(record)
            bounds.append({'frame':frame,'min_m':lo.tolist(),'max_m':hi.tolist()})
        height0=bounds[0]['max_m'][2]-bounds[0]['min_m'][2];max_height=max(b['max_m'][2]-b['min_m'][2] for b in bounds)
        reports.append({'clip':clip,'candidate_sha256':meta['candidate_sha256'],'frames':121,'mesh_objects':len(meshes),'evaluated_vertex_samples':tested,'max_vertex_step_m_per_frame':max_step,'max_height_vs_start':max_height/height0,'finite_and_fixed_topology':'PASS','gross_bound_health':'PASS' if max_height/height0<1.15 and max_step<.06 else 'REVIEW','sampled_hand_overlap':contacts,'collision_scope':'Triangle surface overlaps only; shared wrist boundary omitted; no penetration depth/no physics/contact acceptance','visual_quality':'PENDING_FULL_PLAYBACK_AND_HAND_DETAIL_REVIEW','bounds':bounds})
out=ROOT/('evidence/'+experiment_folder if experiment else 'evidence/native-body-video-r3');out.mkdir(parents=True,exist_ok=True);(out/'mesh_qa.json').write_text(json.dumps({'clips':reports,'actual_yuri_approved_performances':0},indent=2));print(json.dumps([{k:v for k,v in r.items() if k!='bounds'} for r in reports]))
