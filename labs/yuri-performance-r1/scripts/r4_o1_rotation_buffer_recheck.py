"""Independent NumPy-only check of frozen audit NPZ; no Blender/source access.
Usage: python this.py <frozen_evaluated_matrix_buffers.npz>
Requires NumPy (Blender bundled Python is also sufficient).
"""
import sys, json, hashlib
from pathlib import Path
import numpy as np
p=Path(sys.argv[-1]);data=np.load(p,allow_pickle=False)
s=data['source_world'][:,:3,:3];a=data['imported_world_float32_product'][:,:3,:3]
def polar(m):
    u,_,v=np.linalg.svd(m);d=np.linalg.det(u@v);fix=np.ones((len(m),3));fix[:,2]=d
    return (u*fix[:,None,:])@v
def angle(s,a):
    d=np.swapaxes(polar(s),1,2)@polar(a)
    skew=np.stack((d[:,2,1]-d[:,1,2],d[:,0,2]-d[:,2,0],d[:,1,0]-d[:,0,1]),axis=1)/2
    return np.degrees(np.arctan2(np.linalg.norm(skew,axis=1),(np.trace(d,axis1=1,axis2=2)-1)/2))
e=angle(s,a);i=int(np.argmax(e))
# Test fixed orthogonal left/right factors (including reflection) on BOTH inputs.
# This is an invariance check, not a claim about the consumer's particular P/H.
p_basis=np.array([[1.,0,0],[0,0,1],[0,1,0]])
h_basis=np.diag([1.,1.,-1.])
cross=angle(p_basis@s@h_basis,p_basis@a@h_basis)
position=np.linalg.norm(data['source_world'][:,:3,3]-data['imported_world_float32_product'][:,:3,3],axis=1)
result={'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bone_samples':len(e),
    'matrix_angle_max_deg':float(e[i]),'worst_id_clip_sample_frame_bone':data['ids'][i].tolist(),
    'position_max_m':float(position.max()),'rotation_threshold_deg':.001,'rotation_PASS':bool(e.max()<.001),
    'basis_invariance_max_delta_deg':float(np.max(np.abs(e-cross))),
    'test_left_P':p_basis.tolist(),'test_right_H':h_basis.tolist(),
    'consumer_basis_caveat':'These are explicit test matrices, not inferred Unity conversion. Actual consumer buffers are separate.'}
target=p.parent/'INDEPENDENT_BUFFER_RECHECK.json';target.write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
