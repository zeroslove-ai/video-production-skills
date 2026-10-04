"""One source-neutral CPU render; HDR+PNG of SAME Render Result, no source save/tuning."""
import hashlib,json,sys,time
from pathlib import Path
import bpy,numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import props,tree
LAB=HERE.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-alpha-a-source-neutral-hdr-witness-r1'
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
CLONE=BASE/'o1-morph67-native-broker-preparation-r1/SOURCE_BYTE_CLONE_R4.blend'
EXPECTED=LAB/'evidence/o1-source-fidelity-recovery-r1/neutral_camera_light_color_driver_state.json'
SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2,ensure_ascii=False)
def operands(scene):
    return {'camera':{'name':scene.camera.name,'object_world':[list(r) for r in scene.camera.matrix_world],'settings':props(scene.camera.data)},
            'lights':{o.name:{'world':[list(r) for r in o.matrix_world],'settings':props(o.data)} for o in bpy.data.objects if o.type=='LIGHT'},
            'world':{'settings':props(scene.world),'nodes':tree(scene.world.node_tree)},
            'color':{'view':props(scene.view_settings),'display':props(scene.display_settings)},
            'frame':scene.frame_current,'subframe':scene.frame_subframe,'resolution':[scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage],
            'pixel_aspect':[scene.render.pixel_aspect_x,scene.render.pixel_aspect_y],
            'compositor':{'use_nodes':scene.use_nodes,'tree':tree(scene.node_tree) if scene.use_nodes else None}}
def main():
    assert not OUT.exists();assert sha(SOURCE)==sha(CLONE)==SHA;OUT.mkdir()
    start=time.monotonic();bpy.ops.wm.open_mainfile(filepath=str(CLONE),use_scripts=False)
    s=bpy.context.scene;bpy.context.view_layer.update();before=operands(s)
    assert s.frame_current==1 and s.frame_subframe==0 and s.camera.name=='Assembly_Review_Camera'
    assert before['resolution']==[960,920,100]
    assert (s.view_settings.view_transform,s.view_settings.look,s.view_settings.exposure,s.view_settings.gamma)==('AgX','AgX - Medium High Contrast',.25,1)
    assert s.display_settings.display_device=='sRGB' and not s.view_settings.use_curve_mapping and not s.view_settings.use_white_balance
    expected=json.loads(EXPECTED.read_bytes());assert before['camera']['object_world']==expected['camera']['object_world']
    assert before['camera']['settings']==expected['camera']['settings']
    key=bpy.data.objects['Character_Body_Head'].data.shape_keys
    assert all(k.value==0 for k in key.key_blocks)
    assert bpy.data.objects['Character_Body_Head']['Face_GazeYaw']==bpy.data.objects['Character_Body_Head']['Face_GazePitch']==0
    # Reuse existing authoritative preview sampling; resource/output overrides only.
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.seed=0
    s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
    s.render.image_settings.file_format='OPEN_EXR';s.render.image_settings.color_mode='RGBA';s.render.image_settings.color_depth='32';s.render.image_settings.exr_codec='ZIP'
    s.render.filepath=str(OUT/'SOURCE_NEUTRAL_SCENE_LINEAR_20261004_R1.exr')
    dump(OUT/'SOURCE_RENDER_OPERANDS_PRIVATE_R1.json',{'before':before,'cached_expected_path':str(EXPECTED),'cached_expected_sha256':sha(EXPECTED),
        'overrides':{'engine':'CYCLES','device':'CPU','samples':8,'seed':0,'animated_seed':False,'denoising':False,'threads':2,'EXR':'RGBA32 ZIP'},
        'source_render_cycles_settings':props(s.cycles),'actual_render_settings':props(s.render)})
    bpy.ops.render.render(write_still=True)
    rr=bpy.data.images['Render Result'];raw=None
    if len(rr.pixels)==960*920*4:
        raw=np.empty(len(rr.pixels),np.float32);rr.pixels.foreach_get(raw)
    exr=Path(s.render.filepath);assert exr.exists()
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8';s.render.image_settings.color_mode='RGBA'
    png=OUT/'SOURCE_NEUTRAL_AGX_DISPLAY_20261004_R1.png';rr.save_render(str(png),scene=s)
    im=bpy.data.images.load(str(exr),check_existing=False);assert list(im.size)==[960,920]
    buf=np.empty(960*920*4,np.float32);im.pixels.foreach_get(buf)
    assert np.isfinite(buf).all()
    direct_delta=float(np.max(np.abs(raw-buf))) if raw is not None else None
    if raw is not None:assert np.array_equal(raw,buf),'EXR altered raw Render Result pixels'
    image_meta={'colorspace':props(im.colorspace_settings),'alpha_mode':im.alpha_mode,'is_float':im.is_float}
    linear=np.flipud(buf.reshape(920,960,4)).copy()
    npz=OUT/'SOURCE_NEUTRAL_LINEAR_RGBA_TOP_LEFT_PRIVATE_R1.npz';np.savez_compressed(npz,rgba=linear)
    patches={'hair_left':[320,140,380,180],'hair_top':[490,35,545,75],'face_forehead':[460,240,500,265],
             'face_cheek_left':[360,405,405,435],'face_cheek_right':[545,405,590,435]}
    patch_rows=[]
    for name,(x0,y0,x1,y1) in patches.items():
        rgb=linear[y0:y1,x0:x1,:3].reshape(-1,3);Y=rgb@np.array([.2126,.7152,.0722])
        patch_rows.append({'name':name,'ROI_top_left_xyxy':[x0,y0,x1,y1],'pixels':len(rgb),
            'RGB_mean':rgb.mean(axis=0).tolist(),'RGB_median':np.median(rgb,axis=0).tolist(),
            'Y_mean':float(Y.mean()),'Y_percentile_5_50_95':np.percentile(Y,[5,50,95]).tolist(),'max_channel':float(rgb.max()),
            'pixels_any_RGB_over1':int(np.any(rgb>1,axis=1).sum()),
            'scope':'Manually chosen image patch from source neutral framing, not object-ID segmentation;8sample noise/specular outliers retained'})
    after=operands(s);assert before==after,'Camera/light/world/color/frame/compositor changed'
    assert sha(SOURCE)==sha(CLONE)==SHA
    files=[exr,png,npz,OUT/'SOURCE_RENDER_OPERANDS_PRIVATE_R1.json']
    dump(OUT/'HDR_WITNESS_NATIVE_RECEIPT_PRIVATE_R1.json',{
        'source_sha256':SHA,'frame':1,'camera':s.camera.name,'matched_operands_before_after_exact':True,
        'color':'AgX / Medium High Contrast / +0.25EV / gamma1 / sRGB display; unchanged source',
        'HDR_semantics':'OpenEXR32 scene-linear combined image, before view/display transform; machine NPZ read fromEXR float image pixels. Exposure/look used only for display PNG.',
        'Render_Result_direct_pixel_access':raw is not None,'raw_Render_Result_to_EXR_max_abs_delta':direct_delta,
        'EXR_loaded_image_metadata':image_meta,'NPZ_orientation':'TOP_LEFT, RGBA float32; EXR loader image pixels are bottom-left and flipped once',
        'global_RGB_max':float(linear[:,:,:3].max()),'patches':patch_rows,
        'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in files},
        'wall_seconds':time.monotonic()-start,'Blender':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),
        'no_source_save_model_export_Unity_GPU':True,
        'limits':'One source neutral render,CPU2threads8samples; no light/material/pose tuning. Low-sample radiance witness, not final noise-free absolute calibration.'})
if __name__=='__main__':main()
