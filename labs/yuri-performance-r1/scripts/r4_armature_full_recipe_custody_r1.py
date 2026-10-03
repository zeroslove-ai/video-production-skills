"""Exact existing local Git-blob custody and future arming files; no bpy/download/build."""
from pathlib import Path
import hashlib,json,math,struct,sys
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence/o1-native-armature-full-recipe-custody-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-armature-full-recipe-custody-r1')
assert not OUT.exists() and not (E/'RECIPE_CUSTODY_R1.json').exists()
original=Path(r'C:/Users/JAEWAN/projects/yuri-root-pm-r1/artifacts/pm-custody/r7-source-recipe/SourceBodyArmatureInput_0cd0bdd7.json')
expected='0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'
raw=original.read_bytes()
assert len(raw)==18390792 and hashlib.sha256(raw).hexdigest()==expected
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
assert blob=='95d18fbd9ae0a58da2e28b60b24f1e77a51752b2'
recipe=json.loads(raw)
assert len(recipe['positions'])==63561 and len(recipe['boneNames'])==len(recipe['rest'])==57
offsets,indices,weights=recipe['offsets'],recipe['indices'],recipe['weights']
assert len(offsets)==63562 and offsets[0]==0 and offsets[-1]==len(indices)==len(weights)==304799
assert all(type(v) is int and 0<=v<=304799 for v in offsets)
assert all(a<=b for a,b in zip(offsets,offsets[1:]))
assert len(recipe['groups'])==len(recipe['groupToBone'])==58 and recipe['maskGroup']==52
assert all(type(v) is int and 0<=v<58 for v in indices)
assert all(type(v) is int and -1<=v<57 for v in recipe['groupToBone'])
assert all(len(v)==3 and all(math.isfinite(x) for x in v) for v in recipe['positions'])
assert all(len(v)==16 and all(math.isfinite(x) for x in v) for v in recipe['rest'])
assert all(math.isfinite(v) and v>=0 for v in weights)
def bits(values):return struct.pack('<'+'f'*len(values),*values)
BASE=OUT.parent
request_path=BASE/'o1-native-armature-canonical-validation-r4/request-inputs-exact.json'
assert hashlib.sha256(request_path.read_bytes()).hexdigest()=='a46c693c28e09a93729bbe433a522d47c7a452c740a6af6ceb8868ddec370b17'
request=json.loads(request_path.read_bytes())
assert recipe['boneNames']==request['bone_names']
assert all(bits(a)==bits(b) for a,b in zip(recipe['rest'],request['original_rest_57']))
assert bits(recipe['sourceWorld'])==bits(request['original_source_world'])
for sample in request['selected_vertices']:
    vertex=sample['source_vertex'];start,end=offsets[vertex:vertex+2]
    assert bits(recipe['positions'][vertex])==bits(sample['original_position'])
    assert end-start==len(sample['ordered_CSR'])
    for entry,record in zip(range(start,end),sample['ordered_CSR']):
        group=indices[entry]
        assert entry==record['csr_entry'] and group==record['group_index']
        assert recipe['groupToBone'][group]==record['bone_index']
        assert bits([weights[entry]])==bits([record['weight']])
OUT.mkdir();copy=OUT/'SourceBodyArmatureInput_0cd0bdd7_EXACT.json'
with copy.open('xb') as stream:stream.write(raw)
assert copy.read_bytes()==raw and hashlib.sha256(copy.read_bytes()).hexdigest()==expected
sys.path.insert(0,str(ROOT/'scripts/native_readback_proposal'))
from armature_canonical_validate_r7 import verify_arming_inputs,CASES
files={
 'source':str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),
 'actions':str(BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'),
 'pose':str(BASE/'o1-native-unity-probe-r1/reference/native_evaluated_all_frames.json.gz'),
 'recipe':str(copy),'request':str(request_path)}
checks=[]
for row,(action,frame) in enumerate(CASES):
    gate=verify_arming_inputs(files,row,action,frame,'Meshy_Fitted_Rig','Meshy_Body_NeutralCovered')
    checks.append({'row':row,'action':action,'frame':frame,'status':gate['status'],'file_sha256':gate['file_sha256']})
custody={'status':'EXACT_FULL_RECIPE_FILE_CUSTODY_RESOLVED_NO_LIVE_OR_NATIVE_PASS','source_commit':'5dd8712e0a711bd6f8dccd1036f1e28a0827257f',
 'source_git_path':'unity/YuriAvatarSandboxU0/Assets/AvatarCandidates/O1_ExactBindWeight_080352_R1/SourceBodyArmatureInput.json',
 'source_git_blob_SHA1':blob,'source_git_blob_metadata_independently_checked':'GitHub contents metadata size18390792/blob95d18...; encodingnone; recipe body not downloaded',
 'PM_existing_local_source':str(original),'owned_exact_copy':str(copy),'bytes':len(raw),'sha256':expected,
 'counts':{'positions':63561,'bone_slots':57,'CSR_offsets':63562,'ordered_CSR_entries':304799,'groups':58,'mask_group':52},
 'zero_weight_entries_preserved':sum(v==0 for v in weights),
 'request_subset_checks':'PASS original57rest/name order/sourceWorld/five original positions and exact original ordered CSR indices/group/mapping/float32 weight bytes',
 'original_raw_bytes_preserved':True,'normalize_prune_fit_rewrite':False,
 'file_arming_checks':checks,'live_source_verifier':'IMPLEMENTED_NOT_RUN; must compare full bpy63561/57/304799 AFTER source load and BEFORE Action/arming',
 'native_numeric_acceptance':False,'source_or_GUI_mutation':False,'acquisition_approval':False,'build_capture_approval':False}
invocation={'status':'REVIEWED_ACTUAL_FILE_INPUTS_ONLY_NOT_EXECUTION_APPROVAL','files':files,
 'recipe_custody_sha256':expected,'recipe_source_git_blob_SHA1':blob,'cases':[{'row':i,'action':a,'frame':f} for i,(a,f) in enumerate(CASES)],
 'invocation_adapter':'armature_owned_invocation_r7.invoke(bpy,native,files,row,approved_build)',
 'expected_patch_sha256':'b2ba72354e36d96f87ef98f7f7c2b1dba39a95338bff2a91f4cdeb48d64989e2',
 'actual_owner_capture_approval':False,'acquisition_approval':False,
 'pending':['separate real owner approvals/resource/build/compiler/guard custody','compiled _yuri_armature_trace_r5 module','actual full live source recipe/Action/slot/B pose verification','joined capture+restore and numeric/consumer gates'],
 'no_automatic_invocation':'This receipt only resolves files. Its false approval fields cannot authorize execution; use separate approved_build receipt.'}
E.mkdir(parents=True,exist_ok=True)
for name,data in (('RECIPE_CUSTODY_R1.json',custody),('FUTURE_INVOCATION_INPUTS_NOT_APPROVED_R1.json',invocation)):
    p=E/name;p.write_text(json.dumps(data,indent=2),encoding='utf8')
    (OUT/name).write_bytes(p.read_bytes())
print(json.dumps({'status':custody['status'],'bytes':len(raw),'sha256':expected,'zero_weight_entries':custody['zero_weight_entries_preserved'],'pure_file_arming_rows':len(checks),'no_bpy_build_capture_download':True}))
