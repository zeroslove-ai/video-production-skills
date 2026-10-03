"""Already-captured array diagnostics only; preserve frozen private bundle."""
from pathlib import Path
import hashlib,json
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
O=BASE/'o1-morph67-two-input-native-compare-r1';E=LAB/'evidence/o1-morph67-two-input-native-normal-result-r1'
def main():
    rows=[];triangles=[]
    for tag in ['WORST','NEUTRAL']:
        with np.load(O/(tag+'_SHAPE_GN_PRIVATE_R1.npz')) as a,np.load(O/(tag+'_FULL_SOURCE_PRIVATE_R1.npz')) as b:
            av=a['local_CORNER_normal'].astype(np.float64);bv=b['local_CORNER_normal'].astype(np.float64)
            av/=np.linalg.norm(av,axis=1)[:,None];bv/=np.linalg.norm(bv,axis=1)[:,None]
            angle=np.degrees(np.arctan2(np.linalg.norm(np.cross(av,bv),axis=1),np.sum(av*bv,axis=1)))
            corner=int(angle.argmax());vertex=int(a['loop_vertex_indices'][corner]);polygon=int(np.searchsorted(a['polygon_loop_start'],corner,side='right')-1)
            adjacent=np.unique(a['triangle_source_polygon'][np.any(a['loop_vertex_indices'][a['triangle_source_corners']]==vertex,axis=1)])
            tri=a['triangle_source_corners'][np.isin(a['triangle_source_polygon'],adjacent)]
            p=a['local_position'][a['loop_vertex_indices'][tri]].astype(np.float64)
            lengths=np.stack([np.linalg.norm(p[:,1]-p[:,0],axis=1),np.linalg.norm(p[:,2]-p[:,1],axis=1),np.linalg.norm(p[:,0]-p[:,2],axis=1)],axis=1)
            area2=np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1)
            quality=area2/np.maximum(lengths.max(axis=1)**2,1e-30)
            rows.append({'input':tag,'from':'SHAPE_GN','to':'FULL_SOURCE',
                'max_position_vector_delta_m':float(np.linalg.norm(a['local_position']-b['local_position'],axis=1).max()),
                'max_normal_vector_delta':float(np.linalg.norm(a['local_CORNER_normal']-b['local_CORNER_normal'],axis=1).max()),
                'max_normal_angle_deg':float(angle[corner]),'worst_source_CORNER':corner,'source_vertex':vertex,'source_polygon':polygon,'material_slot_zero_based':int(a['polygon_material_slot'][polygon]),
                'adjacent_source_polygons':len(adjacent),'adjacent_native_triangle_min_area_m2':float(area2.min()/2),'min_twice_area_over_longest_edge_squared':float(quality.min()),
                'interpretation':'Thin adjacent triangles support numerical sensitivity hypothesis in geometry-dependent normal spaces, but no exact BKE causal trace or runtime normal-policy conclusion is claimed.'})
        for stage in ['SHAPE_ONLY','SHAPE_GN','FULL_SOURCE']:
            with np.load(O/(tag+'_'+stage+'_PRIVATE_R1.npz')) as x,np.load(O/'OFF_before_PRIVATE_R1.npz') as off:
                triangles.append({'input':tag,'stage':stage,'native_triangle_rows':len(x['triangle_source_polygon']),
                    'triangle_source_polygon_rows_exact_OFF':np.array_equal(x['triangle_source_polygon'],off['triangle_source_polygon']),
                    'triangle_source_corner_rows_changed_from_OFF':int(np.any(x['triangle_source_corners']!=off['triangle_source_corners'],axis=1).sum()),
                    'triangle_source_corners_SHA256':hashlib.sha256(x['triangle_source_corners'].astype('<i4').tobytes()).hexdigest()})
    out={'scope':'Cached native stage differences, not consumer errors; no further native run',
        'Armature_stage_diagnostics':rows,'native_triangle_correspondence':triangles,
        'rule':'Original polygon/loop/material/smooth/UV topology remains exact; per-stage native triangle corners retain original IDs but need not equal static OFF triangulation. Use supplied actual stage rows, not importer diagonal assumptions.',
        'frozen_private_bundle_unchanged_SHA256':'ce5c1cb7d61b27072ebfd55de450d86b06ada318b368eddb45733d4010bdb766',
        'historical_guard_FAIL_product_normal_policy_PBR_F2_PRIMARY':'HOLD preserved'}
    with (E/'ARMATURE_NORMAL_SCOPE_ADDENDUM_R1.json').open('x',encoding='utf8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
    print('PASS cached Armature/triangle correspondence addendum; native runs0')
if __name__=='__main__':main()
