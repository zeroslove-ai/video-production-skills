"""CPU evaluated native geometry depth/mask/57-bone reference, no neural/control claims."""
from pathlib import Path
import bpy,json,numpy as np,time,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/native-camera-r4';meta=json.loads((E/'build_receipt.json').read_text());p=Path(meta['candidate']);assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['candidate_sha256']
bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;r=bpy.data.objects['Armature'];OUT=ROOT/'local/native-conditioning-r4';OUT.mkdir(exist_ok=True);records=[];start=time.monotonic()
def png(path,pixels):
    h,w=pixels.shape[:2];im=bpy.data.images.new('R4 CPU conditioning temporary',width=w,height=h,alpha=True);im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(np.flipud(pixels).astype(np.float32).ravel());im.filepath_raw=str(path);im.file_format='PNG';im.save();bpy.data.images.remove(im)
for clip,name in meta['action_registry'].items():
    r.animation_data.action=bpy.data.actions[name];r.animation_data.action_slot=r.animation_data.action.slots[0]
    for frame in (1,61,121):
        s.frame_set(frame);deps=bpy.context.evaluated_depsgraph_get();verts=[];triangles=[];ids=[];names={}
        for o in bpy.data.objects:
            if o.type!='MESH' or o.hide_render:continue
            evaluated=o.evaluated_get(deps);mesh=evaluated.to_mesh();mesh.calc_loop_triangles();offset=len(verts);verts.extend(evaluated.matrix_world@v.co for v in mesh.vertices);object_id=len(names)+1;names[object_id]=o.name;triangles.extend(tuple(offset+i for i in t.vertices) for t in mesh.loop_triangles);ids.extend([object_id]*len(mesh.loop_triangles));evaluated.to_mesh_clear()
        tree=BVHTree.FromPolygons(verts,triangles,all_triangles=True)
        for camera,c in meta['cameras'].items():
            cam=bpy.data.objects[c['object']];s.camera=cam;w,h=(180,320) if camera=='vertical' else (320,180);s.render.resolution_x=w;s.render.resolution_y=h;s.render.resolution_percentage=100
            corners=cam.data.view_frame(scene=s);xmin=min(v.x for v in corners);xmax=max(v.x for v in corners);ymin=min(v.y for v in corners);ymax=max(v.y for v in corners);z=corners[0].z;origin=cam.matrix_world.translation;rot=cam.matrix_world.to_3x3();depth=np.zeros((h,w),np.float32);mask=np.zeros((h,w),np.uint16)
            for y in range(h):
                ly=ymax-(y+.5)*(ymax-ymin)/h
                for x in range(w):
                    direction=rot@Vector((xmin+(x+.5)*(xmax-xmin)/w,ly,z)).normalized();point,normal,index,distance=tree.ray_cast(origin,direction,10)
                    if index is not None:depth[y,x]=distance;mask[y,x]=ids[index]
            assert np.isfinite(depth).all() and np.count_nonzero(mask)>w*h*.01
            out=OUT/clip/camera/f'{frame:04d}';out.mkdir(parents=True,exist_ok=True);np.save(out/'depth_m.npy',depth);np.save(out/'object_id.npy',mask);subject=(mask>0).astype(np.float32);normalized=np.where(mask>0,1-np.clip((depth-.75)/3.25,0,1),0);png(out/'depth_near_white.png',np.dstack([normalized]*3+[np.ones_like(normalized)]));png(out/'subject_mask.png',np.dstack([subject]*3+[np.ones_like(subject)]))
            pose={}
            for b in r.pose.bones:
                world=r.matrix_world@b.head;uv=world_to_camera_view(s,cam,world);pose[b.name]={'world_m':list(world),'uv_top_left':[uv.x,1-uv.y],'in_frame':0<=uv.x<=1 and 0<=uv.y<=1 and uv.z>0,'parent':b.parent.name if b.parent else None}
            data={'clip':clip,'frame':frame,'time_seconds':(frame-1)/24,'candidate_sha256':meta['candidate_sha256'],'camera':c,'resolution':[w,h],'depth':'Euclidean camera-origin distance in meters, background=0; evaluated geometry CPU BVH','normalization':'fixed near .75m/far4m; near white; no per-frame contrast renormalization','mask':'binary subject; object IDs separate; only render-visible source meshes, no background/floor','object_ids':names,'pose':pose,'pose_convention':'57 native bone head anchors Z-up meters; custom schema NOT OpenPose; no retarget/engine integration','face':'NEUTRAL; actual A/O gate failed','model_control_compatibility':'UNTESTED','foreground_fraction':float(subject.mean()),'depth_range_m':[float(depth[mask>0].min()),float(depth.max())]};(out/'metadata.json').write_text(json.dumps(data,indent=2));records.append({k:data[k] for k in ('clip','frame','resolution','foreground_fraction','depth_range_m')}|{'camera':camera,'path':str(out)});print('NATIVE_CONDITION',clip,frame,camera,flush=True)
(E/'conditioning.json').write_text(json.dumps({'samples':records,'candidate_sha256':meta['candidate_sha256'],'elapsed_seconds':time.monotonic()-start,'status':'CPU_GEOMETRY_REFERENCE_ONLY; VIDEO_MODEL_NOT_TESTED','gpu_model_jobs':0},indent=2))
