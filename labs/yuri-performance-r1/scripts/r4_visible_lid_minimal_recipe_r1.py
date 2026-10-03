"""Read cached graphs only; publish formulas and private field pointers, not numeric recipes."""
from pathlib import Path
import hashlib, json, zipfile

LAB = Path(__file__).resolve().parent.parent
E = LAB / 'evidence/o1-visible-lid-shader-minimal-recipe-r1'
BASE = Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
PACKET = BASE / 'o1-lid-owner-visibility-causal-support-r1/YURI_LID_OWNER_VISIBLE_PIGMENT_CONTRACT_R1.zip'
SHA = '319cc430201df5db3967c49e06de2d9e4bedc9e5b5400732ec961fc3374957e2'
MEMBER = 'LID_GUIDE_VISIBLE_PIGMENT_INPUTS_PRIVATE_R1.json'

def main():
    assert hashlib.sha256(PACKET.read_bytes()).hexdigest() == SHA
    with zipfile.ZipFile(PACKET) as z:
        assert z.testzip() is None
        private = json.loads(z.read(MEMBER))
    graphs = private['visible_material_graphs']
    textures = json.loads((LAB / 'evidence/model-handoff-r4/materials_textures.json').read_text())['textures']
    rows = []
    for side in 'LR':
        material = 'ContinuousEyeSkin.' + side
        graph = graphs[material]['node_graph']
        nodes = {n[0]: (i,n) for i,n in enumerate(graph['nodes'])}
        def field(name, socket):
            i,n = nodes[name]
            j,x = next((j,x) for j,x in enumerate(n[5]) if x[0] == socket)
            return {'private_JSON_pointer': f'/visible_material_graphs/{material}/node_graph/nodes/{i}/5/{j}/1/default_value'}
        def value(name, socket):
            return next(x[1]['default_value'] for x in nodes[name][1][5] if x[0] == socket)
        edges = graph['links']
        chain = [
            ['Texture Coordinate','UV','Mapping','Vector'],
            ['Mapping','Vector','Image Texture','Vector'],
            ['Mapping','Vector','Image Texture.001','Vector'],
            ['R3 broad upper-lid pigment mask','Fac','R3 smooth closed skin field','Fac'],
            ['Image Texture.001','Color','R3 smooth closed skin field','Color1'],
            ['Image Texture','Color','Blink texture corrective','Color1'],
            ['R3 smooth closed skin field','Color','Blink texture corrective','Color2'],
            ['Neck Rest Position','Vector','Separate XYZ.001','Vector'],
            ['Separate XYZ.001','Z','Map Range.001','Value'],
            ['Map Range.001','Result','Mix (Legacy).001','Fac'],
            ['Blink texture corrective','Color','Mix (Legacy).001','Color1'],
            ['R3 anatomical fold only','Fac','Math','Value'],
            ['Math','Value','R3 soft warm fold','Fac'],
            ['Mix (Legacy).001','Color','R3 soft warm fold','Color1'],
            ['R3 soft warm fold','Color','Principled BSDF','Base Color'],
        ]
        # Socket identifier can differ from the displayed Base Color name.
        for edge in chain:
            assert edge in edges, (material,edge)
        for name in ['R3 smooth closed skin field','Blink texture corrective','Mix (Legacy).001']:
            assert nodes[name][1][1]['blend_type'] == 'MIX'
            assert nodes[name][1][1]['use_clamp'] is False
        assert nodes['R3 soft warm fold'][1][1]['blend_type'] == 'MULTIPLY'
        assert nodes['Math'][1][1]['operation'] == 'MULTIPLY'
        assert nodes['Map Range.001'][1][1]['interpolation_type'] == 'SMOOTHERSTEP'
        assert nodes['Map Range.001'][1][1]['clamp'] is True
        drivers = graph['animation']['drivers']
        assert [d[3]['expression'] for d in drivers] == ['min(1,blink*4)','min(1,blink*4)*0.60']
        assert all(d[4][0][1][0]['data_path'] == f'key_blocks["Blink.{side}"].value' for d in drivers)
        assert value('Mapping','Location') == [0,0,0]
        assert value('Mapping','Rotation') == [0,0,0]
        assert value('Mapping','Scale') == [1,1,1]
        sampled = []
        for name in ['Image Texture','Image Texture.001']:
            props = nodes[name][1][1]
            t = next(t for t in textures if t['blender_image'] == props['image'][1])
            assert t['colorspace'] == 'sRGB'
            sampled.append({'node':name, 'image':t['blender_image'], 'file':t['file'],
                            'sha256':t['sha256'], 'colorspace':t['colorspace'],
                            'sampling':{k:props[k] for k in ['projection','interpolation','extension']}})
        rows.append({'side':side,'material':material,'Blink_owner':'Key FaceControls_TEST_Jaw_Smile.001',
            'Blink_path':f'key_blocks["Blink.{side}"].value',
            'driver_targets':[d[0] for d in drivers],
            'mapping':'Texture Coordinate.UV -> Mapping(TEXTURE, identity) -> both images; no invented UV flip',
            'textures':sampled,
            'POINT_attributes':{'p':'R3_LidPigmentMask.'+side,'q':'R3_AnatomicalFold.'+side,'z':'neck_rest_position.Z'},
            'constants':{'Cskin':field('R3 smooth closed skin field','Color2'),
                         'Cneck':field('Mix (Legacy).001','Color2'),
                         'Cwarm':field('R3 soft warm fold','Color2'),
                         'a':field('Map Range.001','From Min'),'c':field('Map Range.001','From Max'),
                         'ToMin':field('Map Range.001','To Min'),'ToMax':field('Map Range.001','To Max')},
            'active_BaseColor_edges':[f'{a}.{b} -> {c}.{d}' for a,b,c,d in chain],
            'excluded_dead_branch':'Unnumbered Separate XYZ -> Map Range -> Mix (Legacy) does not feed BSDF BaseColor'})
    lashes = {}
    for material in ['Face_Lash_Pigment','Face_LowerLash_Pigment']:
        nodes = graphs[material]['node_graph']['nodes']
        i,n = next((i,n) for i,n in enumerate(nodes) if n[1]['type'] == 'BSDF_PRINCIPLED')
        lashes[material] = {x[0]:{'private_JSON_pointer':f'/visible_material_graphs/{material}/node_graph/nodes/{i}/5/{j}/1/default_value'}
                           for j,x in enumerate(n[5]) if x[0] in ['Base Color','Metallic','Roughness']}
    recipe = {
        'capability_delta':'새 Windows 기능 없음; 기존 원본 visible eyelid 연결식의 consumer mapping만 추가',
        'scope':'cached-only RGB BaseColor recipe; no new capture, export, source edit, upload or Unity write',
        'private_constant_authority':{'existing_Drive_id':'12F0Qz_U-c-8pzfNRvEnt9k6TgyGIhpEs','ZIP_sha256':SHA,'member':MEMBER},
        'formula_order':[
            'b = min(1, Blink*4); d = b*0.60 (original expressions; do not add lower clamp)',
            'N = sample neutral image at source UV in scene-linear color; D = sample closed image likewise',
            'closed = mix(D, Cskin, p)', 'corrective = mix(N, closed, b)',
            't = clamp((z-a)/(c-a),0,1); s = t*t*t*(t*(t*6-15)+10)',
            'm = ToMin + s*(ToMax-ToMin); neck = mix(corrective,Cneck,m)',
            'f = q*d; BaseColor_RGB = neck * (1 + f*(Cwarm-1))'],
        'formula_domain':'mix(A,B,f)=(1-f)*A+f*B for nominal factors 0..1; output clamp disabled. Out-of-domain native factor behavior not established by this cache-only algebra.',
        'color_transport':'Image sRGB is decoded into scene-linear before color mixing; constant socket values are scene-linear, not sRGB swatches. Display/view transform is separate. Reproduce POINT attribute interpolation on original source corners; do not use animated world Z for rest-position attribute.',
        'fixed_input_expected':[{'Blink':0,'b':0,'d':0,'result':'mix(N,Cneck,m); fold contribution zero'},
                                {'Blink':0.25,'b':1,'d':0.6,'result':'closed-corrective saturated'},
                                {'Blink':1,'b':1,'d':0.6,'result':'mix(mix(D,Cskin,p),Cneck,m)*(1+0.6*q*(Cwarm-1))'}],
        'sides':rows,'dark_lash_uniform_pointers':lashes,
        'consumer_comparison':'Identify actual white boundary renderer/material-slot first. For eyelid compare N,D,p,q,z,b,d,neck and final scene-linear RGB at same source corner; for lashes compare exact original dark uniform pointers. Preserve hidden guides hide_render=true.',
        'unknowns':['No chosen fragment UV, interpolated mask/rest values or sampled texture RGB supplied; final pixel RGB is not invented.',
                    'Existing145 sample does not witness material node-tree driver outputs; fixed-input algebra is not native evaluated readback.',
                    'Runtime consumer actual slot/color-space/attribute binding and closed-eye visual comparison remain unverified.'],
        'guard_F2_F3_visual_status':'FAILED-HOLD unchanged; no canonical appearance promotion',
        'validation':{'both_side_active_edges':30,'driver_expressions_checked':4,'existing_packet_CRC_SHA':True,'native_executions':0}}
    E.mkdir(exist_ok=True)
    (E/'VISIBLE_LID_MINIMAL_CONSUMER_RECIPE_R1.json').write_text(json.dumps(recipe,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS cached active edges, driver targets, private constant pointers and texture identity; no native execution')

if __name__ == '__main__':
    main()
