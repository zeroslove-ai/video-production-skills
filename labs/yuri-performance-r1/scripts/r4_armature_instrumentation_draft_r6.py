"""Generate additive, source-applicable debug patch. No bpy/build/capture/download."""
from pathlib import Path
import difflib,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-native-armature-instrumentation-draft-r1'
E=ROOT/'evidence/o1-native-armature-instrumentation-draft-r6'
assert not E.exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={
 'source/blender/modifiers/intern/MOD_armature.cc':BASE/'o1-body-modifier-source-contract-r1/upstream/MOD_armature.cc',
 'source/blender/blenkernel/intern/armature_deform.cc':BASE/'o1-body-modifier-source-contract-r1/upstream/armature_deform.cc',
 'source/blender/blenkernel/intern/armature_update.cc':OUT/'upstream/armature_update.cc',
 'source/blender/blenlib/intern/math_rotation_c.cc':OUT/'upstream/math_rotation_c.cc',
}
old={k:p.read_text(encoding='utf8') for k,p in sources.items()};new=dict(old)
def replace(path,a,b):
    expected=2 if path.endswith('MOD_armature.cc') and a.startswith(('  /* if next modifier needs original vertices */','  /* free cache */')) else 1
    assert new[path].count(a)==expected,(path,a[:80],new[path].count(a))
    new[path]=new[path].replace(a,b,1)
def guarded(code):return '\n#ifdef WITH_YURI_ARMATURE_TRACE_R1\n'+code+'\n#endif\n'
mod,arm,pose,rot=list(sources)
for k in sources:
    anchor = '#include <cstring>' if '#include <cstring>' in new[k] else '#include "BLI_math_rotation.h"'
    replace(k,anchor,anchor+guarded('#include "BLI_yuri_armature_trace_r1.hh"'))
replace(mod,'#include "BKE_modifier.hh"','#include "BKE_modifier.hh"'+guarded('#include "DEG_depsgraph_query.hh"'))
replace(pose,'#include "BKE_scene.hh"','#include "BKE_scene.hh"'+guarded('#include "DEG_depsgraph_query.hh"'))
for k in (mod,pose):
    replace(k,'#include "DNA_armature_types.h"','#include "DNA_armature_types.h"'+guarded('#include "DNA_anim_types.h"\n#include "DNA_action_types.h"'))
# Ordinary nullopt caller only; editmesh/crazyspace are not instrumented.
replace(mod,'  /* if next modifier needs original vertices */\n  MOD_previous_vcos_store(md, reinterpret_cast<float (*)[3]>(positions.data()));',
'''  /* if next modifier needs original vertices */
  MOD_previous_vcos_store(md, reinterpret_cast<float (*)[3]>(positions.data()));'''+guarded('''  const int trace_modifier = std::strcmp(md->name,"Armature")==0 ? 0 :
    (std::strcmp(md->name,"R3 neck and joints - local linear blend")==0 ? 1 : -1);
  yuri_armature_trace_r1::Scope trace_scope(DEG_get_ctime(ctx->depsgraph), amd->object->id.name, trace_modifier, nullptr,
    amd->object->adt && amd->object->adt->action ? amd->object->adt->action->id.name : nullptr);
  if(trace_modifier<0 || std::strcmp(ctx->object->id.name,"OBMeshy_Body_NeutralCovered")!=0 || positions.size()!=63561)
    yuri_armature_trace_r1::context = {};
  yuri_armature_trace_r1::matrix("object_world",ctx->object->object_to_world(),4);
  yuri_armature_trace_r1::matrix("rig_world",amd->object->object_to_world(),4);
  yuri_armature_trace_r1::scalar("deformflag",float(amd->deformflag));
  for(int v:yuri_armature_trace_r1::vertices) {
    if(v>=positions.size())continue;
    yuri_armature_trace_r1::context.vertex=v;
    yuri_armature_trace_r1::event("caller_input_local",&positions[v][0],3);
    const float3 world=math::transform_point(ctx->object->object_to_world(),positions[v]);
    yuri_armature_trace_r1::event("caller_input_world",&world[0],3);
  }
  yuri_armature_trace_r1::context.vertex=-1;'''))
replace(mod,'#include "BLI_utildefines.h"','#include "BLI_utildefines.h"'+guarded('#include "BLI_math_matrix.hh"'))
replace(mod,'  /* free cache */\n  MEM_SAFE_DELETE(amd->vert_coords_prev);',guarded('''  for(int v:yuri_armature_trace_r1::vertices) {
    if(v>=positions.size())continue;
    yuri_armature_trace_r1::context.vertex=v;
    yuri_armature_trace_r1::event("caller_output_local",&positions[v][0],3);
    const float3 world=math::transform_point(ctx->object->object_to_world(),positions[v]);
    yuri_armature_trace_r1::event("caller_output_world",&world[0],3);
  }
  yuri_armature_trace_r1::context.vertex=-1;''')+'  /* free cache */\n  MEM_SAFE_DELETE(amd->vert_coords_prev);')
# Immutable rest/inverse/evaluated pose/deform captured at actual pose completion.
replace(pose,'  if (bone) {\n    invert_m4_m4(imat, bone->arm_mat);','  if (bone) {'+guarded('''    yuri_armature_trace_r1::Scope trace_bone(DEG_get_ctime(depsgraph),object->id.name,-1,pchan->name,
      object->adt && object->adt->action ? object->adt->action->id.name : nullptr);
    yuri_armature_trace_r1::matrix("rest",bone->arm_mat,4);
    yuri_armature_trace_r1::matrix("evaluated_pose",pchan->pose_mat,4);
    yuri_armature_trace_r1::scalar("bone_no_deform",float(bool(bone->flag & BONE_NO_DEFORM)));''')+'    invert_m4_m4(imat, bone->arm_mat);'+guarded('    yuri_armature_trace_r1::matrix("inverse_rest",imat,4);'))
replace(pose,'    mul_m4_m4m4(pchan->chan_mat, pchan->pose_mat, imat);','    mul_m4_m4m4(pchan->chan_mat, pchan->pose_mat, imat);'+guarded('    yuri_armature_trace_r1::matrix("deform_matrix",pchan->chan_mat,4);'))
# Propagate copied context into actual parallel vertex workers; do not log unrelated paths.
replace(arm,'  float4x4 target_to_armature;','  float4x4 target_to_armature;'+guarded('  yuri_armature_trace_r1::Context trace_context;'))
replace(arm,'  return deform_params;',''+guarded('''  deform_params.trace_context=yuri_armature_trace_r1::context;
  yuri_armature_trace_r1::matrix("premat",deform_params.target_to_armature,4);
  yuri_armature_trace_r1::matrix("postmat",deform_params.armature_to_target,4);
  yuri_armature_trace_r1::scalar("full_deform",float(vert_deform_mats.has_value()));
  yuri_armature_trace_r1::scalar("armature_mask_group",float(deform_params.armature_def_nr));''')+'  return deform_params;')
replace(arm,'  const bool full_deform = params.vert_deform_mats.has_value();','  const bool full_deform = params.vert_deform_mats.has_value();'+guarded('''  auto trace_context=params.trace_context;
  if(!yuri_armature_trace_r1::selected(i) || full_deform)trace_context={};
  trace_context.vertex=i;
  yuri_armature_trace_r1::Scope trace_vertex(trace_context);
  yuri_armature_trace_r1::event("vertex_input_local",&params.vert_coords[i][0],3);
  if(params.vert_coords_prev)yuri_armature_trace_r1::event("previous_cached_local",&(*params.vert_coords_prev)[i][0],3);
  if(dvert) {int n=0;for(const auto &dw:Span<MDeformWeight>(dvert->dw,dvert->totweight)) {
    yuri_armature_trace_r1::context.entry=n++;
    const float entry[2]={float(dw.def_nr),dw.weight};
    yuri_armature_trace_r1::event("csr_original_group_weight",entry,2);
  }}
  yuri_armature_trace_r1::context.entry=-1;'''))
replace(arm,'    const float mask_weight = BKE_defvert_find_weight(dvert, params.armature_def_nr);','    const float mask_weight = BKE_defvert_find_weight(dvert, params.armature_def_nr);'+guarded('    yuri_armature_trace_r1::scalar("mask_weight",mask_weight);'))
replace(arm,'      if (prevco_weight == 1.0f) {\n        return;','      if (prevco_weight == 1.0f) {'+guarded('        yuri_armature_trace_r1::scalar("skip_previous_mask",prevco_weight);')+'        return;')
replace(arm,'      if (armature_weight == 0.0f) {\n        return;','      if (armature_weight == 0.0f) {'+guarded('        yuri_armature_trace_r1::scalar("skip_zero_mask",armature_weight);')+'        return;')
replace(arm,'  co = math::transform_point(params.target_to_armature, co);','  co = math::transform_point(params.target_to_armature, co);'+guarded('''  yuri_armature_trace_r1::event("co_armature",&co[0],3);
  yuri_armature_trace_r1::scalar("armature_weight",armature_weight);
  yuri_armature_trace_r1::scalar("previous_co_weight",prevco_weight);'''))
replace(arm,'    for (const auto &dw : dweights) {',''+guarded('    int trace_entry=0;')+'    for (const auto &dw : dweights) {'+guarded('      yuri_armature_trace_r1::context.entry=trace_entry++;'))
replace(arm,'      if (pchan == nullptr) {\n        continue;','      if (pchan == nullptr) {'+guarded('''        yuri_armature_trace_r1::scalar("eligibility",0.0f);
        yuri_armature_trace_r1::scalar("mapped_bone",-1.0f);
        yuri_armature_trace_r1::scalar("running_total",contrib);
        mixer.trace_state();''')+'        continue;')
replace(arm,'      float weight = dw.weight;','      float weight = dw.weight;'+guarded('''      yuri_armature_trace_r1::scalar("mapped_bone",float(yuri_armature_trace_r1::slot(pchan->name)));
      yuri_armature_trace_r1::scalar("eligibility",float(weight!=0.0f));
      yuri_armature_trace_r1::scalar("bone_segments",float(pchanbone.bone->segments));'''))
replace(arm,'      contrib += pchan_bone_deform(pchanbone, weight, co, mixer);','      contrib += pchan_bone_deform(pchanbone, weight, co, mixer);'+guarded('''      yuri_armature_trace_r1::scalar("effective_weight",weight);
      yuri_armature_trace_r1::scalar("running_total",contrib);
      mixer.trace_state();'''))
replace(arm,'  if (!deformed && params.use_envelope) {','  if (!deformed && params.use_envelope) {'+guarded('    yuri_armature_trace_r1::scalar("unexpected_envelope_fallback",1.0f);'))
replace(arm,'  constexpr float contrib_threshold = 0.0001f;',guarded('  yuri_armature_trace_r1::context.entry=-1;')+'  constexpr float contrib_threshold = 0.0001f;')
replace(arm,'    co += delta_co;',''+guarded('''    yuri_armature_trace_r1::event("finalize_delta",&delta_co[0],3);
    yuri_armature_trace_r1::event("transformed_co_before_update",&co[0],3);''')+'    co += delta_co;'+guarded('    yuri_armature_trace_r1::event("co_after_update",&co[0],3);'))
replace(arm,'  co = math::transform_point(params.armature_to_target, co);','  co = math::transform_point(params.armature_to_target, co);'+guarded('    yuri_armature_trace_r1::event("pre_mask_local",&co[0],3);'))
replace(arm,'    copy_v3_v3(params.vert_coords[i], co);\n  }','    copy_v3_v3(params.vert_coords[i], co);\n  }'+guarded('  yuri_armature_trace_r1::event("vertex_output_local",&params.vert_coords[i][0],3);'))
replace(arm,'  float3x3 deform = float3x3::zero();','  float3x3 deform = float3x3::zero();'+guarded('  void trace_state(){yuri_armature_trace_r1::event("running_lbs_delta",&position_delta[0],3);}'))
replace(arm,'  DualQuat dq = {};','  DualQuat dq = {};'+guarded('''  void trace_state(){
    yuri_armature_trace_r1::event("running_real_q",dq.quat,4);
    yuri_armature_trace_r1::event("running_dual_q",dq.trans,4);
  }'''))
replace(arm,'    normalize_dq(&dq, total);','    normalize_dq(&dq, total);'+guarded('''    yuri_armature_trace_r1::event("normalized_real_q",dq.quat,4);
    yuri_armature_trace_r1::event("normalized_dual_q",dq.trans,4);'''))
replace(arm,'    mul_v3m3_dq(dco, dmat.ptr(), &dq);','    mul_v3m3_dq(dco, dmat.ptr(), &dq);'+guarded('    yuri_armature_trace_r1::event("dq_transformed_armature_co",&dco[0],3);'))
# Actual native locals from conversion and accumulation; no parallel math reimplementation.
replace(rot,'  normalize_m3(unit_mat_abs);\n  mat3_normalized_to_quat_with_checks(q, unit_mat_abs);','  normalize_m3(unit_mat_abs);'+guarded('  blender::yuri_armature_trace_r1::matrix("normalized_rotation_columns",unit_mat_abs,3);')+'  mat3_normalized_to_quat_with_checks(q, unit_mat_abs);')
replace(rot,'    dq->scale_weight = 1.0f;\n  }\n  else {\n    /* matrix does not contain scaling */','    dq->scale_weight = 1.0f;'+guarded('    blender::yuri_armature_trace_r1::scalar("no_scale_branch",0.0f);')+'  }\n  else {\n    /* matrix does not contain scaling */')
replace(rot,'    dq->scale_weight = 0.0f;\n  }\n\n  /* non-dual part */','    dq->scale_weight = 0.0f;'+guarded('    blender::yuri_armature_trace_r1::scalar("no_scale_branch",1.0f);')+'  }\n\n  /* non-dual part */')
replace(rot,'  /* dual part */\n  const float *t = R[3];',''+guarded('  blender::yuri_armature_trace_r1::matrix("quat_conversion_R",R,4);')+'  /* dual part */\n  const float *t = R[3];')
replace(rot,'  dq->trans[3] = 0.5f * (t[0] * q[2] - t[1] * q[1] + t[2] * q[0]);','  dq->trans[3] = 0.5f * (t[0] * q[2] - t[1] * q[1] + t[2] * q[0]);'+guarded('''  blender::yuri_armature_trace_r1::event("real_q",dq->quat,4);
  blender::yuri_armature_trace_r1::event("dual_q",dq->trans,4);'''))
replace(rot,'  /* interpolate rotation and translation */',''+guarded('  blender::yuri_armature_trace_r1::scalar("hemisphere_sign",flipped?-1.0f:1.0f);')+'  /* interpolate rotation and translation */')
replace(rot,'  len2 = dot_qtqt(dq->quat, dq->quat);','  len2 = dot_qtqt(dq->quat, dq->quat);'+guarded('  blender::yuri_armature_trace_r1::scalar("quaternion_length_squared",len2);'))
replace(rot,'  /* translation */\n  t[0] = 2 * (-t0 * x + w * t1 - t2 * z + y * t3);',''+guarded('  blender::yuri_armature_trace_r1::scalar("reciprocal_length_squared",len2);')+'  /* translation */\n  t[0] = 2 * (-t0 * x + w * t1 - t2 * z + y * t3);')
replace(rot,'  /* apply scaling */\n  if (dq->scale_weight) {',''+guarded('''  blender::yuri_armature_trace_r1::matrix("dq_rotation_matrix",M,3);
  blender::yuri_armature_trace_r1::event("dq_translation",t,3);''')+'  /* apply scaling */\n  if (dq->scale_weight) {')
rigs=BASE/'o1-native-unity-probe-r1/metadata/source_expanded_rigs.json'
assert sha(rigs)=='d3b556a0c7adbedaccb6c55c0914ea9b92dc8b3cc2f3e84594725d50dbb89694'
bones=json.loads(rigs.read_text(encoding='utf8'))['Meshy_Fitted_Rig']['bones'];assert len(bones)==57
header=ROOT/'scripts/native_readback_proposal/armature_trace_r4.hh.in'
new['source/blender/blenlib/BLI_yuri_armature_trace_r1.hh']=header.read_text(encoding='utf8').replace('@BONES@',','.join(json.dumps(b['name']) for b in bones))
cmake=OUT/'upstream/CMakeLists.txt'
old['CMakeLists.txt']=cmake.read_text(encoding='utf8')
anchor='cmake_minimum_required(VERSION 3.21)'
assert old['CMakeLists.txt'].count(anchor)==1
new['CMakeLists.txt']=old['CMakeLists.txt'].replace(anchor,anchor+'''\n
option(WITH_YURI_ARMATURE_TRACE_R1 "Owned research armature trace (never installed ABI hooks)" OFF)
if(WITH_YURI_ARMATURE_TRACE_R1)
  add_compile_definitions(WITH_YURI_ARMATURE_TRACE_R1)
endif()
''')
bridge=ROOT/'scripts/native_readback_proposal/bpy_yuri_armature_trace_r5.hh'
new['source/blender/python/intern/bpy_yuri_armature_trace_r5.hh']=bridge.read_text(encoding='utf8')
binding_source=BASE/'o1-native-armature-binding-r5/bpy_interface.cc'
binding_name='source/blender/python/intern/bpy_interface.cc'
old[binding_name]=binding_source.read_text(encoding='utf8')
new[binding_name]=old[binding_name]
replace(binding_name,'#include <optional>','#include <optional>'+guarded('#include "bpy_yuri_armature_trace_r5.hh"'))
replace(binding_name,'static _inittab bpy_internal_modules[] = {','static _inittab bpy_internal_modules[] = {'+guarded('    {"_yuri_armature_trace_r5", BPyInit_yuri_armature_trace_r5},'))
sources[binding_name]=binding_source
E.mkdir(parents=True)
diff=''.join(''.join(difflib.unified_diff(old.get(k,'').splitlines(True),v.splitlines(True),fromfile='a/'+k if k in old else '/dev/null',tofile='b/'+k)) for k,v in new.items())
(E/'native_armature_typed_r6.patch').write_text(diff,encoding='utf8')
fixture=OUT/'apply-check-r6';assert not fixture.exists();fixture.mkdir()
for k,v in old.items():p=fixture/k;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(v,encoding='utf8')
check=subprocess.run(['git','apply','--check',str(E/'native_armature_typed_r6.patch')],cwd=fixture,capture_output=True,text=True)
assert check.returncode==0,check.stderr
result={'status':'SOURCE_APPLY_CHECK_PASS_NOT_COMPILED_OR_EXECUTED','source_commit':'9e2066aef7ef7e20c142ad7bd3303138a4304c93','patch_SHA256':sha(E/'native_armature_typed_r6.patch'),'sources':{k:{'cached_path':str(p),'sha256':sha(p)} for k,p in sources.items()},'bone_slots':[{'slot':i,'name':b['name'],'deform':b['deform']} for i,b in enumerate(bones)],'vertices':[11189,14918,21485,22227,40817],'ordinary_nullopt_caller':True,'apply_check':{'exit_code':check.returncode,'stderr':check.stderr,'fixture':str(fixture)},'pending':['Owned adapter verifies actual active Action and pose recipe then arms BEFORE pose dependency graph evaluation; begin/finish API has no RNA binding yet','Default-OFF macro build wiring and compiler/API validation','Full request NPZ packing and complete per-event cardinality checks','Non-deforming bone helper quaternion branch never executed; mark missing/not-applicable rather than fabricate','Normalized conversion matrix multiple events on scale branch require quat_conversion_R selection; matrix inverse backend/FP flags to be recorded','Actual runtime sampling, capture process guard closure, original 63561/all304799 gates and source/Unity PBR acceptance'],'logging':{'format':'YRA1 binary events, 8-byte magic/version then 8 little-endian uint32 context/header fields and UTF8 tag plus float32 raw payload','context_fields':['row','modifier','bone','vertex','entry','tag_bytes','float_count','reserved'],'float32_signed_zero':'memcpy IEEE bits; no decimal serialization','matrix_layout':'row-major copied once from native column-major','limits':'64MiB/100000records/count<=64/tag<=96; mutex; fail-latched; exclusive new file per case','cleanup':'finish only after workers joined; flush+close; no dangling pointers retained','world':'forward transform actual caller LOCAL only; never inverse WORLD','CSR':'original order logged including unmapped/zero/masks; post entry running state unchanged for noncontributing entries; integer group/slot emitted as exact small float diagnostic values, offline int32 schema conversion pending'}}
(E/'PATCH_APPLY_AND_SCOPE.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({'patch_sha256':result['patch_SHA256'],'apply_check':result['status'],'bones':len(bones)}))
