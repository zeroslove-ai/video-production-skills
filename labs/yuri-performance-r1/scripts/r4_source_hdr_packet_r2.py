"""Cache-only HDR audit/packet. No Blender launch, source save or exporter."""
import hashlib,json,zipfile
from pathlib import Path
import numpy as np
from PIL import Image

LAB=Path(__file__).resolve().parents[1]
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-alpha-a-source-neutral-hdr-witness-r2'
BROKER=BASE/'o1-alpha-a-source-hdr-broker-r2'
EVIDENCE=LAB/'evidence/o1-alpha-a-source-neutral-hdr-witness-r2'
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf8') as f: json.dump(v,f,indent=2,ensure_ascii=False)

def main():
    EVIDENCE.mkdir(exist_ok=False)
    receipt=json.loads((OUT/'HDR_WITNESS_NATIVE_RECEIPT_PRIVATE_R1.json').read_bytes())
    guard=json.loads((BROKER/'NATIVE_HDR_GUARD_RESULT_R2.json').read_bytes())
    operands=json.loads((OUT/'SOURCE_RENDER_OPERANDS_PRIVATE_R1.json').read_bytes())
    assert sha(SOURCE)==receipt['source_sha256']
    assert guard['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
    assert guard['terminal_exit_code']==0 and guard['terminal_job']['active']==0 and not guard['cleanup_errors']
    for name,row in receipt['files'].items(): assert sha(OUT/name)==row['sha256']
    baseline=BASE/'r4-appearance-preserve-correction-r1/neutral/authority_source_camera_before.png'
    current=OUT/'SOURCE_NEUTRAL_AGX_DISPLAY_20261004_R2.png'
    a=np.array(Image.open(baseline));b=np.array(Image.open(current))
    assert np.array_equal(a,b)
    rgba=np.load(OUT/'SOURCE_NEUTRAL_LINEAR_RGBA_TOP_LEFT_PRIVATE_R1.npz')['rgba']
    assert rgba.shape==(920,960,4) and rgba.dtype==np.float32 and np.isfinite(rgba).all()
    assert float(rgba[:,:,:3].max())==receipt['global_RGB_max']
    for patch in receipt['patches']:
        x0,y0,x1,y1=patch['ROI_top_left_xyxy'];rgb=rgba[y0:y1,x0:x1,:3].reshape(-1,3)
        assert np.allclose(rgb.mean(axis=0),patch['RGB_mean'],rtol=0,atol=0)
        assert int(np.any(rgb>1,axis=1).sum())==patch['pixels_any_RGB_over1']
    assert operands['before']['compositor']['tree'] is None
    # Packet includes source operands privately, never the source model or mesh.
    files=[(p,'witness/'+p.name) for p in sorted(OUT.iterdir()) if p.is_file()]
    files += [(p,'execution/r2/'+str(p.relative_to(BROKER)).replace('\\','/')) for p in sorted(BROKER.rglob('*')) if p.is_file()]
    failed=BASE/'o1-alpha-a-source-hdr-broker-r1'
    files += [(failed/n,'execution/r1-failed/'+n) for n in ['FAILED_COLLECTOR_FROZEN_R1.py','FIXED_HDR_CONFIG_R1.json','NEW_ALPHA_A_HDR_APPROVAL_R1.json','NATIVE_HDR_GUARD_RESULT_R1.json']]
    files += [(failed/'native-gates-r1/PAYLOAD_DONE.json','execution/r1-failed/PAYLOAD_DONE.json')]
    files += [(LAB/'scripts'/n,'workflow/'+n) for n in ['r4_source_neutral_hdr_witness_r2.py','r4_source_hdr_packet_r2.py','r4_appearance_signature.py','native_preservation.py']]
    runtime=BASE/'o1-morph67-native-broker-preparation-r4/workflow'
    files += [(runtime/n,'workflow/'+n) for n in ['r4_two_input_owned_barrier_broker_r1.py','r4_two_input_live_barrier_wrapper_r1.py']]
    files += [(baseline,'baseline/authority_source_camera_before.png')]
    index={name:{'sha256':sha(p),'bytes':p.stat().st_size} for p,name in files}
    packet=BASE/'YURI_R4_SOURCE_NEUTRAL_HDR_WITNESS_R2_20261004.zip'
    assert not packet.exists()
    with zipfile.ZipFile(packet,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p,name in files:z.write(p,name)
        z.writestr('FILE_INDEX.json',json.dumps(index,indent=2))
    with zipfile.ZipFile(packet) as z:
        for name,row in index.items():assert hashlib.sha256(z.read(name)).hexdigest()==row['sha256']
    public={'scope':'R4 immutable source-neutral HDR witness only; no appearance promotion or Unity validation',
        'source_sha256':sha(SOURCE),'source_changes':0,'frame':1,'resolution':[960,920],
        'OFF_baseline_pixel_exact':True,'OFF_max_channel_difference':0,'OFF_changed_pixels':0,
        'baseline_sha256':sha(baseline),'new_display_sha256':sha(current),
        'scene_linear_RGB_max':receipt['global_RGB_max'],
        'native_guard':guard['guard_status'],'native_pid':guard['pid'],
        'native_wall_seconds':guard['wall_seconds'],'native_exit':0,'terminal_job_active':0,
        'guard_receipt_sha256':sha(BROKER/'NATIVE_HDR_GUARD_RESULT_R2.json'),
        'direct_Render_Result_float_access':False,'raw_to_EXR_pixel_equality_claimed':False,
        'original_compositor_tree':None,'same_Render_Result_EXR_and_PNG':True,
        'patch_statistics_recomputed':True,
        'packet':{'path':str(packet),'sha256':sha(packet),'bytes':packet.stat().st_size,'members':len(index)+1},
        'limitations':['8-sample CPU witness retains noise/specular outliers','EXR loader colorspace name not captured by generic RNA serializer; no claimed direct Render Result float equality','Manual image rectangles are not object segmentation','Absolute cross-engine source-area-light calibration remains HOLD'],
        'R1_failure':'Scene.node_tree absent in Blender5.2; failed before render, preserved separately; R2 uses compositing_node_group',
        'next':'Receiver matches source camera/world/area-light operands and scene-linear ROI before judging absolute response; keep source visual authority immutable'}
    write(EVIDENCE/'HDR_PACKET_RECEIPT_R2.json',public)
    print(json.dumps(public,indent=2))

if __name__=='__main__':main()
