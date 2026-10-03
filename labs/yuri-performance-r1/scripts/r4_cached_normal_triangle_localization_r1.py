"""Narrow cached localization; original IDs private, top3 check IDs public metadata."""
from pathlib import Path
import hashlib,json
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
O=BASE/'o1-morph67-two-input-native-compare-r1';E=LAB/'evidence/o1-cached-normal-triangle-localization-r1'
P=BASE/'o1-cached-normal-triangle-localization-r1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,ensure_ascii=False,indent=2)
def angles(a,b):
    a=a.astype(np.float64);b=b.astype(np.float64)
    a/=np.linalg.norm(a,axis=1)[:,None];b/=np.linalg.norm(b,axis=1)[:,None]
    return np.degrees(np.arctan2(np.linalg.norm(np.cross(a,b),axis=1),np.sum(a*b,axis=1)))
def main():
    assert not E.exists() and not P.exists();E.mkdir();P.mkdir()
    source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
    static=BASE/'o1-source-fidelity-recovery-r1/data/Character_Body_Head_original_mesh.npz'
    metadata=LAB/'evidence/o1-source-fidelity-recovery-r1/mesh_slot_UV_attributes_shape_deltas.json'
    original=json.loads(metadata.read_bytes())[0]
    result=json.loads((O/'TWO_INPUT_NATIVE_RESULT_PRIVATE_R1.json').read_bytes())
    paths=[source,static,metadata,*[O/r['file'] for r in result['records']+result['OFF_records']]]
    hashes={str(p):sha(p) for p in paths}
    assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    assert sha(static)=='1a48cf823cb6cf0c95c7eee6d4b7e7e8a952cbaadd50d1d9ad18d909be34f473'
    for r in result['records']+result['OFF_records']:assert sha(O/r['file'])==r['sha256']
    with np.load(static) as s,np.load(O/'WORST_SHAPE_GN_PRIVATE_R1.npz') as a,np.load(O/'WORST_FULL_SOURCE_PRIVATE_R1.npz') as b,np.load(O/'OFF_before_PRIVATE_R1.npz') as off:
        cp=np.repeat(np.arange(21701),s['polygon_loop_total']);cv=s['loop_vertex_indices'];slots=s['polygon_material_slot'][cp]
        changed=np.flatnonzero(np.any(a['triangle_source_corners']!=off['triangle_source_corners'],axis=1))
        polys=np.unique(a['triangle_source_polygon'][changed]);vertices=np.unique(cv[a['triangle_source_corners'][changed]])
        assert len(changed)==34 and len(polys)==17
        assert np.array_equal(a['triangle_source_corners'],b['triangle_source_corners'])
        assert np.array_equal(a['world_matrix'],b['world_matrix'])
        nextc=np.arange(66861)+1;nextc[s['polygon_loop_start']+s['polygon_loop_total']-1]=s['polygon_loop_start']
        ce=s['attribute_18_value'];edges=s['edge_vertex_indices'];sharp=s['attribute_14_value']
        assert not np.any(sharp) and 'sharp_face' not in [x['name'] for x in original['attributes']]
        assert np.array_equal(np.sort(edges[ce],axis=1),np.sort(np.stack([cv,cv[nextc]],axis=1),axis=1))
        # Topological smooth-fan components, no numerical BKE decoder/traversal claim.
        parent=np.arange(66861)
        def root(x):
            while parent[x]!=x:parent[x]=parent[parent[x]];x=int(parent[x])
            return int(x)
        def union(x,y):
            assert cv[x]==cv[y];rx,ry=root(int(x)),root(int(y));parent[rx]=ry
        ec=[[] for _ in range(len(edges))]
        for corner,edge in enumerate(ce):ec[edge].append(corner)
        boundary=nonmanifold=winding=0
        for edge,corners in enumerate(ec):
            if len(corners)==1:boundary+=1;continue
            if len(corners)!=2:nonmanifold+=1;continue
            x,y=corners
            if cv[x]!=cv[nextc[y]] or cv[nextc[x]]!=cv[y]:winding+=1;continue
            if sharp[edge] or not a['polygon_use_smooth'][cp[x]] or not a['polygon_use_smooth'][cp[y]]:continue
            union(x,nextc[y]);union(nextc[x],y)
        roots=np.array([root(i) for i in range(66861)])
        ang=angles(a['local_CORNER_normal'],b['local_CORNER_normal'])
        ids=np.flatnonzero(np.isin(cp,polys));lash=np.flatnonzero(slots==6)
        checks=[int(ang.argmax()),int(ids[np.argmax(ang[ids])]),int(lash[np.argmax(ang[lash])])]
        graph=[set() for _ in range(12928)]
        for x,y in edges:graph[x].add(int(y));graph[y].add(int(x))
        def hops(vertex):
            frontier={vertex};seen=frontier.copy();targets=set(vertices.tolist())
            for depth in range(12928):
                if frontier&targets:return depth
                if not frontier:return None
                frontier=set().union(*(graph[x] for x in frontier))-seen;seen|=frontier
        private_checks=[];public_checks=[]
        for rank,c in enumerate(checks,1):
            vertex=int(cv[c]);polygon=int(cp[c]);fan=np.flatnonzero(roots==roots[c]);fanpolys=np.unique(cp[fan])
            polycorners=np.arange(s['polygon_loop_start'][polygon],s['polygon_loop_start'][polygon]+s['polygon_loop_total'][polygon]);pv=cv[polycorners]
            supports=[k['name'] for k in original['ShapeKeys'] if np.any(s[k['array']][pv]!=0)]
            fanedges=np.unique(np.concatenate([ce[fan],ce[np.array([s['polygon_loop_start'][cp[f]]+s['polygon_loop_total'][cp[f]]-1 if f==s['polygon_loop_start'][cp[f]] else f-1 for f in fan])]]))
            check={'priority':rank,'source_CORNER':c,'source_vertex':vertex,'source_polygon':polygon,'source_slot_zero_based':int(slots[c]),
                'material':original['material_slots'][int(slots[c])],'GN_to_FULL_normal_angle_deg':float(ang[c]),
                'is_changed_quad':bool(polygon in polys),'peak_fan_intersects_changed_polygons':bool(np.intersect1d(fanpolys,polys).size),
                'fan_CORNERs':len(fan),'fan_source_polygons':len(fanpolys),'fan_boundary_edges':sum(len(ec[e])==1 for e in fanedges),
                'fan_nonmanifold_edges':sum(len(ec[e])>2 for e in fanedges),'fan_sharp_edges':int(sharp[fanedges].sum()),
                'fan_alpha_zero_CORNERs':int((s['attribute_19_value'][fan,0]==0).sum()),
                'shape_support_names':supports,'region_caveat':'Slot/shape names are source semantic hints, not confirmed bright pixel or exact anatomical patch segmentation.'}
            public_checks.append(check);private_checks.append({**check,'fan_CORNER_IDs':fan.tolist(),'fan_polygon_IDs':fanpolys.tolist(),'fan_edge_IDs':fanedges.tolist(),
                'native_triangles_on_polygon_rows':np.flatnonzero(a['triangle_source_polygon']==polygon).tolist()})
        changedrows=[]
        for row in changed:
            polygon=int(a['triangle_source_polygon'][row]);c=a['triangle_source_corners'][row]
            changedrows.append({'native_triangle_row':int(row),'source_polygon':polygon,'slot':int(s['polygon_material_slot'][polygon]),
                'OFF_source_CORNERs':off['triangle_source_corners'][row].tolist(),'WORST_source_CORNERs':c.tolist(),'source_vertices':cv[c].tolist()})
        upper_count=0
        for polygon in polys:
            vc=cv[s['polygon_loop_start'][polygon]:s['polygon_loop_start'][polygon]+s['polygon_loop_total'][polygon]]
            upper_count+=any(k['name'].startswith('CORR_Upper') and np.any(s[k['array']][vc]!=0) for k in original['ShapeKeys'])
        slot_distribution=[]
        for slot,name in enumerate(original['material_slots']):
            values=ang[slots==slot]
            if values.size:slot_distribution.append({'slot':slot,'material':name,'CORNERs':len(values),'max_angle_deg':float(values.max()),'CORNERs_over_0_1deg':int((values>.1).sum()),'CORNERs_over_1deg':int((values>1).sum())})
        primary=checks[0];primaryvertex=int(cv[primary]);nearest=float(np.linalg.norm(a['local_position'][vertices]-a['local_position'][primaryvertex],axis=1).min())
        summary={'changed_triangle_rows':34,'changed_source_quad_polygons':17,'slot3_polygons':int((s['polygon_material_slot'][polys]==3).sum()),'slot4_polygons':int((s['polygon_material_slot'][polys]==4).sum()),
            'source_Upper_corrective_support_polygons':int(upper_count),'max_GN_to_FULL_angle_on_changed_polygon_CORNERs_deg':float(ang[ids].max()),
            'global_peak_polygon_or_vertex_direct_overlap':bool(cp[primary] in polys or primaryvertex in vertices),'global_peak_to_changed_vertex_min_distance_m':nearest,'global_peak_to_changed_vertex_edge_hops':hops(primaryvertex),
            'GN_to_FULL_triangle_source_CORNER_arrays_exact':True,'GN_to_FULL_object_world_matrices_exact':True,
            'global_original_adjacency':{'sharp_edges':0,'sharp_face_attribute':'absent/defaultfalse','boundary_edges':boundary,'nonmanifold_or_unused_edges':nonmanifold,'opposite_winding_fail_edges':winding},
            'normal_change_distribution_WORST':slot_distribution}
        private={'cached_index':changedrows,'consumer_check_fans':private_checks,'inputs_SHA':hashes,'summary':summary}
        pp=P/'CHANGED_TRIANGLE_FAN_INDEX_PRIVATE_R1.json';dump(pp,private)
    for path,h in hashes.items():assert sha(Path(path))==h
    receipt={'capability_delta':'새 Windows 기능 없음; existing2input cached triangle/normal localization only','status':'READY_SUPPORT_WAIT',
        'reuse':'5440445 native custody + ARMATURE_NORMAL_SCOPE_ADDENDUM_R1 reused; no new baseline/native/ZIP/transport',
        'neutral_peak_reuse':'Existing ARMATURE_NORMAL_SCOPE_ADDENDUM_R1.json: CORNER23318/vertex4082/polygon7766/slot1/max6.9352016deg. Distinct from17changed lid polygons/slots3-4; no duplicate native measurement requested.',
        'original_source_SHA':hashes[str(source)],'cached_inputs_SHA':hashes,'summary':summary,'top3_consumer_checks':public_checks,
        'exact_private_index':{'path':str(pp),'bytes':pp.stat().st_size,'sha256':sha(pp),'reconstructable_from_receiver_bundle':'ce5c1cb7d61b27072ebfd55de450d86b06ada318b368eddb45733d4010bdb766'},
        'causal_discrimination':'34diagonals occur already at SHAPE_ONLY vsOFF and remain identical through GN/FULL. Global WORST GN→FULL normal peak is a different polygon/vertex/topological fan; same left eyelid material region and2.25mm proximity do not prove coincidence. Local CORNER comparison and exactly equal object matrices exclude an extra exporter object-local/world conversion here. Intrinsic evaluated modifier output difference is observed; Armature internal normal handling vs fan recomputation needs BKE trace to establish cause.',
        'only_missing_actionable_mapping':'For one actual bright pixel from existing writer: actor renderer/material/submesh+triangle and its3original source CORNER IDs (or verified split-vertex→source-loop mapping), with sameinput/pre-vs-postskin normal scope. Current PM pixel counts/screens lack these IDs; cannot assert the known bright triangles equal these17source quads or normal peak fans.',
        'next_minimum_checks':'Compare the3listed native locations in same consumer pre-skin/source-GN local scope: global normal peak, changed upper-lid quad, internal lash peak. Preserve actual per-stage triangles, original polygon/fan adjacency, smooth/material/UV; no vertex averaging/static diagonal substitute.',
        'normal_policy_PBR_F2_F3_PRIMARY':'HOLD preserved','Blender_launches_Unity_writes':0}
    dump(E/'CACHED_TRIANGLE_NORMAL_LOCALIZATION_R1.json',receipt)
    print(json.dumps({'summary':summary,'top3':[(r['source_CORNER'],r['source_polygon'],r['source_slot_zero_based'],r['fan_CORNERs']) for r in public_checks],'private_index_SHA':sha(pp)}))
if __name__=='__main__':main()
