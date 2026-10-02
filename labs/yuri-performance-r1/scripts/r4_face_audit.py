"""Reuse native calibration recipe on R4, no facial re-authoring."""
from pathlib import Path
source=(Path(__file__).parent/'calibrate_r2_source_face.py').read_text(encoding='utf8')
source=source.replace("local/source-face-r2","local/model-handoff-r4/face-audit").replace("evidence/source-face-r2","evidence/model-handoff-r4/face-audit")
source=source.replace("C:\\Users\\JAEWAN\\Downloads\\Character_Master_R2_20261002.blend","C:\\Users\\JAEWAN\\Documents\\Codex\\2026-10-02\\files-pasted-by-the-user-yuri\\outputs\\r4-model-handoff\\Character_Master_Reaction_R4_20261002.blend")
source=source.replace(";assert fingerprint=='5e88819a61120b74c9a0e3de03f90b9890b7ac13eea2113e10fcada321d21d2e'",'')
source=source.replace("r=bpy.data.objects['Armature']","r=bpy.data.objects['Meshy_Fitted_Rig']")
source=source.replace("R2_SOURCE_CALIBRATION_COPY.blend","R4_FACE_CALIBRATION_COPY.blend")
source=source.replace("MOTION5H_WeightShift_Loop_8s","YRA_R4_QA_MilestoneA_Sequence")
source=source.replace("m.object==r","m.object and m.object.type=='ARMATURE'")
source=source.replace("s.cycles.samples=12","s.cycles.samples=4").replace("resolution_x=384","resolution_x=256").replace("resolution_y=512","resolution_y=384")
exec(compile(source,str(Path(__file__).parent/'calibrate_r2_source_face.py'),'exec'))
