"""Third actual CPU candidate: MediaPipe2D -> official MotionBERT-Lite.
Reuses existing embedded PyTorch read-only. No CUDA, dataset or SMPL download.
"""
from pathlib import Path
import os,sys,urllib.request,json,hashlib,time
os.environ['CUDA_VISIBLE_DEVICES']='-1';os.environ['OMP_NUM_THREADS']='4'
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';code=L/'motionbert_source'
files=['lib/model/DSTformer.py','lib/model/drop.py','LICENSE','configs/pose3d/MB_ft_h36m_global_lite.yaml']
receipts=[]
for name in files:
    p=code/name;p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():p.write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/Walter0807/MotionBERT/main/'+name,timeout=30).read())
    receipts.append({'name':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
weight=L/'models/motionbert_lite.bin';url='https://huggingface.co/walterzhu/MotionBERT/resolve/main/checkpoint/pose3d/FT_MB_lite_MB_ft_h36m_global_lite/best_epoch.bin'
if not weight.exists():
    with urllib.request.urlopen(url,timeout=90) as r,weight.with_suffix('.partial').open('wb') as f:
        while b:=r.read(1024*1024):f.write(b)
    weight.with_suffix('.partial').replace(weight)
print('MODEL_READY',weight.stat().st_size,flush=True)
import numpy as np,torch
sys.path.insert(0,str(code));from lib.model.DSTformer import DSTformer
torch.set_num_threads(4);torch.set_num_interop_threads(1)
assert not torch.cuda.is_initialized()
model=DSTformer(dim_in=3,dim_out=3,dim_feat=256,dim_rep=512,depth=5,num_heads=8,mlp_ratio=4,norm_layer=torch.nn.LayerNorm,maxlen=243,num_joints=17,att_fuse=True).cpu()
checkpoint=torch.load(weight,map_location='cpu',weights_only=True);state=checkpoint['model_pos'];state={k.removeprefix('module.'):v for k,v in state.items()};model.load_state_dict(state,strict=True);model.eval()
a=np.load(L/'mediapipe_raw.npz');xy=a['xy'][:360:2];confidence=a['confidence'][:360:2,:,0];h=np.zeros((180,17,3),np.float32)
mapping={1:24,2:26,3:28,4:23,5:25,6:27,9:0,11:11,12:13,13:15,14:12,15:14,16:16}
for target,src in mapping.items():h[:,target,:2]=xy[:,src];h[:,target,2]=confidence[:,src]
h[:,0]=(h[:,1]+h[:,4])/2;h[:,8]=(h[:,11]+h[:,14])/2;h[:,7]=(h[:,0]+h[:,8])/2;h[:,10]=h[:,9]+(h[:,9]-h[:,8])*.25
original=h.copy();lo=h[:,:,:2].reshape(-1,2).min(0);hi=h[:,:,:2].reshape(-1,2).max(0);scale=max(hi-lo);centre=(lo+hi)/2;h[:,:,:2]=(h[:,:,:2]-centre)/scale*2
flip_indices=[0,4,5,6,1,2,3,7,8,9,10,14,15,16,11,12,13]
batch=torch.from_numpy(h)[None];flipped=batch[:,:,flip_indices].clone();flipped[:,:,:,0]*=-1;begin=time.monotonic()
with torch.inference_mode():
    p1=model(batch);p2=model(flipped)[:,:,flip_indices];p2[:,:,:,0]*=-1;p=((p1+p2)/2)[0].numpy()
elapsed=time.monotonic()-begin;assert not torch.cuda.is_initialized();p-=p[:,0:1,:]
stature=np.median(p[:,[3,6],1].max(1)-p[:,9,1]+.12);p*=1.65/stature
# Interpolate the30fps lift back onto original60fps timestamps. This temporal
# candidate does not claim independently measured60fps depth.
lift=np.empty((360,17,3));t30=np.arange(180)/30;t60=np.arange(360)/60
for j in range(17):
    for axis in range(3):lift[:,j,axis]=np.interp(t60,t30,p[:,j,axis])
out=a['xyz'][:360].copy()
for target,src in mapping.items():out[:,src]=lift[:,target]
for dst,src,ank in [(29,29,27),(31,31,27),(30,30,28),(32,32,28)]:out[:,dst]=out[:,ank]+a['xyz'][:360,src]-a['xyz'][:360,ank]
np.savez_compressed(L/'motionbert_raw.npz',xy=a['xy'][:360],xyz=out,confidence=a['confidence'][:360],timestamps=np.arange(360)/60+20)
receipt={'estimator':'MediaPipe2D + MotionBERT-Lite temporal3D','source_code':'https://github.com/Walter0807/MotionBERT','checkpoint_url':url,'checkpoint_bytes':weight.stat().st_size,'checkpoint_sha256':hashlib.sha256(weight.read_bytes()).hexdigest(),'source_files':receipts,'code_license':'Apache2.0, retained in ignored source cache','torch_version':torch.__version__,'device':'CPU_ONLY','cuda_initialized':torch.cuda.is_initialized(),'inference_seconds':elapsed,'body_input':'same selected dancer, MediaPipe2D; syntheticH36Mhead-top fromnose/shoulders; no AlphaPose model downloaded','fps_input_to_lifter':30,'fps_output_interpolated':60,'source_interval':[20,26],'flip_augmentation':True,'root':'hip-relative, reconstructed with same explicitly assumed camera/scale; no world-root claim','foot_landmarks':'heel/toe offsets inherited fromMediaPipe; temporal body model does not observe toes','head_face':'2Droll inherited, no face expression mapping','status':'THIRD_ACTUAL_EXTRACTION_COMPLETE_NOT_ACCURACY_PASS'};(E/'motionbert_extraction.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,ensure_ascii=True))
