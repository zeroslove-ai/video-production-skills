"""Frozen-cache reference only; no bpy/native/mesh mutation or new private packet."""
from pathlib import Path
import gzip, hashlib, json, zipfile
import numpy as np

LAB = Path(__file__).resolve().parent.parent
BASE = Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E = LAB/'evidence/o1-head-lash-exact-cached-operands-r1'
SOURCE = LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
SOURCE_SHA = 'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert sha(SOURCE) == SOURCE_SHA
    packet = BASE/'o1-lid-owner-visibility-causal-support-r1/YURI_LID_OWNER_VISIBLE_PIGMENT_CONTRACT_R1.zip'
    assert sha(packet) == '319cc430201df5db3967c49e06de2d9e4bedc9e5b5400732ec961fc3374957e2'
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        d = json.loads(z.read('LID_GUIDE_VISIBLE_PIGMENT_INPUTS_PRIVATE_R1.json'))
    material = d['visible_material_graphs']['Face_Lash_Pigment']
    graph = material['node_graph']
    assert graph['links'] == [['Principled BSDF','BSDF','Material Output','Surface']]
    i,node = next((i,n) for i,n in enumerate(graph['nodes']) if n[1]['type']=='BSDF_PRINCIPLED')
    wanted = ['Roughness','IOR','Alpha','Thin Wall','Diffuse Roughness',
              'Subsurface Weight','Specular IOR Level','Specular Tint','Anisotropic',
              'Anisotropic Rotation','Transmission Weight','Coat Weight','Coat Roughness',
              'Coat IOR','Coat Tint','Coat Normal','Sheen Weight','Emission Strength',
              'Normal','Tangent','Thin Film Thickness']
    operands = {}
    values = {}
    for j,s in enumerate(node[5]):
        if s[0] not in wanted: continue
        props=s[1]; values[s[0]]=props['default_value']
        assert props['is_linked'] is False
        operands[s[0]] = {'private_member_JSON_pointer':f'/visible_material_graphs/Face_Lash_Pigment/node_graph/nodes/{i}/5/{j}/1/default_value',
                         'is_linked':False,'enabled':props['enabled'],'is_unavailable':props['is_unavailable']}
    assert set(operands)==set(wanted)
    assert all(values[n]==0 for n in ['Coat Weight','Transmission Weight','Subsurface Weight','Sheen Weight','Emission Strength','Anisotropic','Thin Film Thickness'])
    assert values['Alpha']==1 and values['Normal']==[0,0,0] and values['Tangent']==[0,0,0]
    assert values['Thin Wall'] is False
    slots_path=LAB/'evidence/o1-source-fidelity-recovery-r1/mesh_slot_UV_attributes_shape_deltas.json'
    slots=json.loads(slots_path.read_text());ri,r=next((i,r) for i,r in enumerate(slots) if r['renderer']=='Character_Body_Head')
    assert ri==0 and r['material_slots'][6]=='Face_Lash_Pigment'
    npz=BASE/'o1-source-fidelity-recovery-r1'/r['file']['path']
    assert sha(npz)==r['file']['sha256'] and npz.stat().st_size==r['file']['bytes']
    rawpath=BASE/'o1-original-idle-sampling-r3/RAW_FINGERPRINT_INPUTS_BEFORE_PRIVATE_R3.json.gz'
    with gzip.open(rawpath,'rt') as f:raw=json.load(f)
    obj=raw['objects']['Character_Body_Head'];meshid=obj['props']['data'][1];mesh=raw['mesh_attributes'][meshid]
    assert obj['materials'][6][0]=='Face_Lash_Pigment' and obj['materials'][6][1]['link']=='DATA'
    with np.load(npz) as n:
        mat=n['polygon_material_slot'];assert np.array_equal(mat,np.array([p[-2] for p in mesh['polygons']]))
        domain=np.flatnonzero(mat==6).astype('<i4')
        corners=np.concatenate([np.arange(n['polygon_loop_start'][p],n['polygon_loop_start'][p]+n['polygon_loop_total'][p]) for p in domain]).astype('<i4')
        verts=np.unique(n['loop_vertex_indices'][corners]).astype('<i4')
        smooth=sum(bool(mesh['polygons'][int(p)][-1]) for p in domain)
        custom=next(a for a in r['attributes'] if a['name']=='custom_normal')
        assert custom['domain']=='CORNER' and custom['data_type']=='INT16_2D'
        assert n[custom['fields'][0]['array']].shape==(len(n['loop_vertex_indices']),2)
        domain_meta={'polygons':len(domain),'source_corners':len(corners),'unique_source_vertices':len(verts),
                     'smooth_polygons':smooth,'flat_polygons':len(domain)-smooth,
                     'polygon_ids_LE_i32_SHA256':hashlib.sha256(domain.tobytes()).hexdigest(),
                     'corner_ids_LE_i32_SHA256':hashlib.sha256(corners.tobytes()).hexdigest()}
    props=material['properties']
    transparency=['surface_render_method','blend_method','alpha_threshold','use_transparency_overlap',
                  'show_transparent_back','use_backface_culling','use_backface_culling_shadow',
                  'use_transparent_shadow','use_raytrace_refraction','use_screen_refraction','displacement_method']
    result={
        'capability_delta':'새 Windows 기능 없음; 기존 head 내부 lash BSDF/domain의 exact cached reference 공급',
        'source':{'path':str(SOURCE),'sha256':SOURCE_SHA,'immutable':True},
        'existing_private_material_authority':{'Drive_id':'12F0Qz_U-c-8pzfNRvEnt9k6TgyGIhpEs',
            'ZIP_sha256':sha(packet),'member':'LID_GUIDE_VISIBLE_PIGMENT_INPUTS_PRIVATE_R1.json'},
        'material':'Face_Lash_Pigment','active_surface_link':graph['links'][0],
        'BSDF_properties':{'distribution':node[1]['distribution'],'subsurface_method':node[1]['subsurface_method']},
        'active_scalar_observations':{k:values[k] for k in ['Roughness','IOR','Specular IOR Level']},
        'operand_pointers':operands,
        'disabled_contribution_observations':'Coat/Transmission/Subsurface/Sheen/Emission/Anisotropy/ThinFilm weights or strength/thickness are zero; Alpha=1; ThinWall=false. Exact socket values in pointers. No transparent shader or image/normal/tangent links.',
        'material_flags':{k:props[k] for k in transparency},
        'viewport_property_caveat':'Material.properties.roughness is a different viewport field from active Principled Roughness; use node socket above. specular_intensity is not Specular IOR Level. HASHED/DITHERED flags do not by themselves prove translucent rendered pixels with Alpha=1.',
        'head_owner':{'object':'Character_Body_Head','hierarchy':'Armature/Character_Body_Head','original_mesh_ID':meshid,
            'slot_zero_based':6,'slot_link':'DATA','assignment_domain':'source POLYGON/FACE material index; triangle descendants must retain source polygon slot',
            'cached_NPZ':{'path':str(npz),'member_relative_path':r['file']['path'],'sha256':sha(npz),'bytes':npz.stat().st_size},
            'domain_selection':'polygon_material_slot == 6; expand polygon_loop_start/total then loop_vertex_indices; never select all head or separate14lash meshes',
            'domain':domain_meta,'UV':'UVMap / uv_0, source CORNER domain',
            'has_custom_normals':mesh['props']['has_custom_normals'],
            'normal_authority':{'custom_normal':custom,'NPZ_array':custom['fields'][0]['array'],
                'interpretation':'Original encoded corner custom normals are present. No linked Normal does not mean zero shading normal: implicit BSDF shading normal derives from geometry/smoothing/custom-normal pipeline.',
                'tangent':'No linked Tangent or tangent texture; anisotropy zero. Actual evaluated per-frame corner shading normals/tangents are not witnessed by this operand extraction.'}},
        'raw_domain_authority':{'path':str(rawpath),'sha256':sha(rawpath),
            'slot_pointer':'/objects/Character_Body_Head/materials/6',
            'polygon_pointer':'/mesh_attributes/'+meshid+'/polygons',
            'polygon_schema':'[*vertex IDs, material_index, use_smooth]; verified against frozen NPZ assignment'},
        'missing':['Actual Laptop bright-boundary pixel triangle/source-polygon/material-slot witness',
                   'Same-pose consumer evaluated custom shading normals and bound BSDF/light/view operands; this cache does not witness runtime shader behavior',
                   'No source same-pose Blink~0.962 rendered BSDF A/B or material-node evaluated pixel witness acquired'],
        'verification_methods':[
            'Pixel owner test: same camera/pose/lighting, use Laptop slot-ID diagnostic for head source slot6; preserve fallback/source; separate14lash hide is not headslot6 exclusion.',
            'BSDF binding test: record actual headslot6 shader materialID and active Roughness/IOR/SpecularIORLevel/Alpha/Coat/Normal binding against exact pointers; do not equate Blender SpecularIORLevel directly with arbitrary Unity smoothness/specular controls.',
            'Normals/light discrimination: hold geometry/camera/light fixed, verify source-corner custom-normal transport and smooth flags on slot6 domain; a Laptop diagnostic specular-only/off comparison can discriminate highlight hypothesis, but is not a source material edit or appearance PASS.'],
        'preservation':'Immutable R4/fallback/source and guard FAILED-HOLD/F2/F3 unchanged. No native capture/export/mesh edit/Unity write/upload; 5276592 recipe not rerun.',
        'validation':{'private_packet_SHA_CRC':True,'NPZ_SHA_bytes':True,'raw_NPZ_material_assignment_equal':True,'operand_pointers':len(operands),'native_runs':0}}
    E.mkdir(exist_ok=True)
    (E/'HEAD_LASH_EXACT_CACHED_OPERANDS_R1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS immutable source SHA; frozen ZIP CRC/SHA; NPZ SHA; raw/NPZ slot6 equality; 21 unlinked BSDF operands')
    print('Head slot6 domain:',domain_meta)

if __name__=='__main__':main()
