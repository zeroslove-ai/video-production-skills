"""Inspect full LIVE original bpy body/rest/CSR against exact verified kernel recipe.
No bpy import at module load. Read only; never prune or normalize weights.
"""
import json
from pathlib import Path
from armature_canonical_validate_r4 import require,fbytes,sha,RECIPE_SHA

def verify_live_recipe(bpy,path):
    require(sha(path)==RECIPE_SHA,'actual full recipe identity mismatch')
    recipe=json.loads(Path(path).read_bytes())
    rig=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered']
    names=[b.name for b in rig.data.bones]
    require(names==recipe['boneNames'] and len(names)==57,'live original57 slot order drift')
    for index,b in enumerate(rig.data.bones):
        require(fbytes([b.matrix_local[r][c] for r in range(4) for c in range(4)])==fbytes(recipe['rest'][index]),'live original rest drift')
    require(fbytes([body.matrix_world[r][c] for r in range(4) for c in range(4)])==fbytes(recipe['sourceWorld']),'live original source world drift')
    offsets,indices,weights,mapping=recipe['offsets'],recipe['indices'],recipe['weights'],recipe['groupToBone']
    require(len(body.data.vertices)==len(recipe['positions'])==63561,'live full vertex cardinality')
    require(len(offsets)==63562 and offsets[0]==0 and offsets[-1]==len(indices)==len(weights)==304799,'live full CSR cardinality')
    require(recipe['maskGroup']==52 and len(mapping)==len(body.vertex_groups),'live mask/group contract')
    for g in body.vertex_groups:
        require(mapping[g.index]==(names.index(g.name) if g.name in names else -1),'original full group mapping drift')
    count=0
    for index,v in enumerate(body.data.vertices):
        require(fbytes(list(v.co))==fbytes(recipe['positions'][index]),'live original coordinate drift '+str(index))
        groups=list(v.groups);start,end=offsets[index:index+2]
        require(0<=start<=end<=304799 and len(groups)==end-start,'live CSR offset/order cardinality '+str(index))
        for local,g in enumerate(groups):
            entry=start+local
            require(g.group==indices[entry] and fbytes([g.weight])==fbytes([weights[entry]]),'live full ordered CSR drift '+str(entry))
            count+=1
    require(count==304799,'full live CSR not exhausted')
    return {'status':'LIVE_ORIGINAL_FULL_RECIPE_BYTE_IDENTICAL','vertices':63561,'slots':57,'CSR_entries':count,'zero_helpers_masks':'PRESERVED'}
