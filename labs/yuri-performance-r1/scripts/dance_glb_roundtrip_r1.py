"""Import all exported clips into fresh private Blender scenes and sample motion."""
from pathlib import Path
import bpy, json, hashlib,sys
R=Path(__file__).resolve().parents[1]; L=R/'local/dance-benchmark-r1'; E=R/'evidence/dance-benchmark-r1'
reports=[]
for method in (['motionbert_reprojection','motionbert_reprojection_stable'] if 'r2' in sys.argv else ['mediapipe','rtmw3d','motionbert']):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    path=L/(method+'_DANCE_R1.glb')
    bpy.ops.import_scene.gltf(filepath=str(path))
    rigs=[o for o in bpy.data.objects if o.type=='ARMATURE']; assert len(rigs)==1
    rig=rigs[0]; assert len(rig.data.bones)==17 and rig.animation_data.action
    samples=[]
    # glTF uses seconds; Blender importer maps onto the fresh scene's24fps.
    for seconds in [0,1,3,5.9]:
        bpy.context.scene.frame_set(1+int(seconds*24))
        samples.append({n:list(rig.matrix_world@rig.pose.bones[n].head) for n in ['hips','hand.L','hand.R','foot.L','foot.R']})
    changed=max(sum((samples[-1][n][i]-samples[0][n][i])**2 for i in range(3))**.5 for n in samples[0])
    assert changed>.01
    reports.append({'method':method,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bones':17,'action':rig.animation_data.action.name,'sample_seconds':[0,1,3,5.9],'positions':samples,'maximum_first_last_joint_displacement_m':changed,'verdict':'PASS_IMPORTED_ANIMATED_NOT_CHOREOGRAPHY_ACCURACY'})
(E/('glb_roundtrip_r2.json' if 'r2' in sys.argv else 'glb_roundtrip.json')).write_text(json.dumps(reports,indent=2))
print(json.dumps(reports))
