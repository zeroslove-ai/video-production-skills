"""Fixed installed-Blender source identity check. Read only; no action/pose/save."""
from pathlib import Path
import hashlib,json,struct,traceback
import bpy

SOURCE=Path(r'C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1/local/model-handoff-r4/Character_Master_NeckSkin_R4.blend')
RECIPE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json')
OUT=RECIPE.parent.parent/'o1-readonly-source-job-r4/source-identity.json'
SOURCE_SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
RECIPE_SHA='0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
def bits(x):return struct.pack('<'+'f'*len(x),*x)
def matrix(m):return [m[r][c] for r in range(4) for c in range(4)]
def inspect():
    require(Path(bpy.data.filepath).resolve()==SOURCE.resolve(),'wrong actual loaded source')
    require(sha(SOURCE)==SOURCE_SHA and sha(RECIPE)==RECIPE_SHA,'file identity mismatch')
    q=json.loads(RECIPE.read_bytes())
    rig=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered']
    names=[b.name for b in rig.data.bones]
    require(names==q['boneNames'] and len(names)==len(q['rest'])==57,'57 original bone order')
    for i,b in enumerate(rig.data.bones):
        require(bits(matrix(b.matrix_local))==bits(q['rest'][i]),f'rest matrix slot {i}')
    require(bits(matrix(body.matrix_world))==bits(q['sourceWorld']),'body source world')
    offsets,indices,weights,mapping=q['offsets'],q['indices'],q['weights'],q['groupToBone']
    require(len(body.data.vertices)==len(q['positions'])==63561,'63561 original positions')
    require(len(offsets)==63562 and offsets[0]==0 and offsets[-1]==len(indices)==len(weights)==304799,'full CSR cardinality')
    require(q['maskGroup']==52 and len(mapping)==len(q['groups'])==len(body.vertex_groups)==58,'mask52/groups58')
    for g in body.vertex_groups:
        require(g.name==q['groups'][g.index] and mapping[g.index]==(names.index(g.name) if g.name in names else -1),f'group mapping {g.index}')
    count=zeros=0
    for i,v in enumerate(body.data.vertices):
        require(bits(list(v.co))==bits(q['positions'][i]),f'basis position {i}')
        groups=list(v.groups);start,end=offsets[i:i+2]
        require(0<=start<=end<=304799 and len(groups)==end-start,f'CSR offsets vertex {i}')
        for local,g in enumerate(groups):
            entry=start+local
            require(g.group==indices[entry] and bits([g.weight])==bits([weights[entry]]),f'ordered CSR entry {entry}')
            count+=1;zeros+=int(g.weight==0)
    require(count==304799,'full CSR exhausted')
    return {'status':'LIVE_ORIGINAL_FULL_RECIPE_BYTE_IDENTICAL','vertices':63561,'slots':57,'CSR_entries':count,'groups':58,'mask_group':52,'zero_weight_entries':zeros}
row={'scope':'SOURCE_DATA_IDENTITY_ONLY','native_numeric_acceptance':False,'render_export_save_action_pose_mutation':False,'blender_version':bpy.app.version_string,'blender_build_hash':bpy.app.build_hash.decode()}
try:row.update(inspect())
except Exception:
    row.update(status='FAIL_FIRST_MISMATCH_NO_REPAIR',error=traceback.format_exc())
finally:
    row['source_post_sha256']=sha(SOURCE);row['recipe_post_sha256']=sha(RECIPE)
    with OUT.open('x',encoding='utf8') as f:json.dump(row,f,indent=2)
    print(json.dumps(row),flush=True)
if row['status']!='LIVE_ORIGINAL_FULL_RECIPE_BYTE_IDENTICAL':raise RuntimeError(row['status'])
