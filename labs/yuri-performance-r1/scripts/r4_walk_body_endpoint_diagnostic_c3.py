import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_walk_root_endpoint_adapter_c2 import WalkRootEndpointLane,ACTIONS
B=Path("C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs");O=B/"alpha-walk-body-endpoint-diagnostic-c3";O.mkdir(exist_ok=False)
m=json.loads((B/"alpha-walk-root-endpoint-c2b/WALK_ROOT_ENDPOINT_PRIVATE_C2.json").read_bytes());C=Path(m["candidate"]);assert hashlib.sha256(C.read_bytes()).hexdigest()==m["candidate_SHA"]
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);names=list(bpy.data.actions.keys());before=snapshot(names);a=bpy.data.actions[ACTIONS["Meshy_Fitted_Rig"]];fc=[f for l in a.layers for st in l.strips for bag in st.channelbags for f in bag.fcurves];groups={}
for f in fc:groups.setdefault(f.data_path,[]).append(f)
rank=[]
for path,fs in groups.items():
 vals=np.array([[f.evaluate(t) for f in sorted(fs,key=lambda f:f.array_index)] for t in [1,2,96,97]])
 d=(vals[3]-vals[2])-(vals[1]-vals[0]);rank.append({"path":path,"component_indices":[f.array_index for f in fs],"values_frames1_2_96_97":vals.tolist(),"derivative_mismatch_per_second":(d*24).tolist(),"norm":float(np.linalg.norm(d*24))})
rank.sort(key=lambda x:-x["norm"]);ln=WalkRootEndpointLane();ln.on();s=bpy.context.scene;rig=bpy.data.objects["Meshy_Fitted_Rig"];j={}
for t in [1,2,96,97,98]:
 s.frame_set(t);bpy.context.view_layer.update();j[t]={b.name:list(rig.matrix_world@b.head) for b in rig.pose.bones}
ln.off();assert snapshot(names)==before
(O/"BODY_ENDPOINT_DIAGNOSTIC_C3.json").write_text(json.dumps({"candidate_SHA":m["candidate_SHA"],"original87_OFF_equal":True,"rank":rank,"joints_private":j},indent=2),encoding="utf8");print(json.dumps(rank[:16],indent=2),flush=True)
