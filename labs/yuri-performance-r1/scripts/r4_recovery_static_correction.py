"""One disposable exporter-default correction; source data and curves unchanged.
Capture each Model default TRS from original OFF export, replay only when writing
animation-file Model elements. Animation curve evaluation remains unpatched.
"""
import bpy,sys,json,hashlib
from pathlib import Path
from io_scene_fbx import export_fbx_bin as fbx
from io_scene_fbx.fbx_utils import ObjectWrapper
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1/static-correction')
E=ROOT/'evidence/o1-source-fidelity-recovery-r1/static-correction';E.mkdir(parents=True,exist_ok=True)
cache={};phase=None;real_tx=ObjectWrapper.fbx_object_tx;real_models=fbx.fbx_data_object_elements
def tx(self,scene_data,*args,**kwargs):
    if phase=='replay':
        assert self.key in cache,self.key
        return tuple(v.copy() if hasattr(v,'copy') else v for v in cache[self.key])
    result=real_tx(self,scene_data,*args,**kwargs)
    if phase=='capture':cache[self.key]=tuple(v.copy() if hasattr(v,'copy') else v for v in result)
    return result
def models(root,obj,scene_data):
    global phase
    phase='replay' if scene_data.settings.bake_anim else 'capture'
    try:return real_models(root,obj,scene_data)
    finally:phase=None
ObjectWrapper.fbx_object_tx=tx;fbx.fbx_data_object_elements=models
original=HERE/'r4_o1_native_probe_export.py';code=original.read_text(encoding='utf8')
code=code.replace("E=ROOT/'evidence/o1-native-unity-probe-r1'","E=ROOT/'evidence/o1-source-fidelity-recovery-r1/static-correction'")
code=code.replace('outputs/o1-native-unity-probe-r1','outputs/o1-source-fidelity-recovery-r1/static-correction')
code=code.replace("LIB=OUT.parent/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'","LIB=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend')")
code=code.replace("source_commit':'62f2e6b800e2aac4bda41c5341155c385c0b2f01'","source_commit':'d204379bb8dbab7749a8819863437e788b9ce9ee'")
try:exec(compile(code,str(original),'exec'),{'__file__':str(original),'__name__':'__main__'})
finally:ObjectWrapper.fbx_object_tx=real_tx;fbx.fbx_data_object_elements=real_models
for script in ('r4_o1_native_probe_roundtrip.py','r4_o1_native_probe_wire.py','r4_o1_native_probe_matrix_analysis.py'):
    p=HERE/script;code=p.read_text(encoding='utf8').replace("E=ROOT/'evidence/o1-native-unity-probe-r1'","E=ROOT/'evidence/o1-source-fidelity-recovery-r1/static-correction'").replace('outputs/o1-native-unity-probe-r1','outputs/o1-source-fidelity-recovery-r1/static-correction')
    exec(compile(code,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
(E/'correction_method.json').write_text(json.dumps({'scope':'Only FBX Model default TRS serializer; source/rest/pose/Action input unchanged; curve sampling untouched','captured_OFF_default_models':len(cache),'original_export_script_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'exporter_module_sha256':hashlib.sha256(Path(fbx.__file__).read_bytes()).hexdigest(),'tolerance_changed':False,'prior_files_changed':False},indent=2),encoding='utf8')
print('BOUNDED_DEFAULT_CORRECTION_COMPLETE')
