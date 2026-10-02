"""CPU geometry ray-casts for metric depth/ID and custom proxy pose anchors.
Not OpenPose / Fun-Control compatible until a separate adapter gate passes.
"""
from pathlib import Path
import bpy,json,sys,time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/acting-r2';E=ROOT/'evidence/acting-r2'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'YURI_PERFORMANCE_ACTING_R2.blend'))
s=bpy.context.scene;r=bpy.data.objects['ProxyHumanoid']
registry=json.loads((E/'action_registry.json').read_text());cameras=json.loads((E/'camera_metadata.json').read_text())
records=[];t0=time.monotonic()
def png(path,pixels):
    h,w=pixels.shape[:2];im=bpy.data.images.new('CPU conditioning temporary',width=w,height=h,alpha=True)
    im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(np.flipud(pixels).astype(np.float32).ravel())
    im.filepath_raw=str(path);im.file_format='PNG';im.save();bpy.data.images.remove(im)
for clip in ('greeting_wave','shy_lookaway','please_tilt'):
    for o in bpy.data.objects:
        if o.animation_data:o.animation_data.action=None
        if o.type=='MESH' and o.data.shape_keys and o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
    for owner,name in registry[clip]['natural']:
        o=bpy.data.objects.get(owner) or bpy.data.shape_keys.get(owner);o.animation_data_create();o.animation_data.action=bpy.data.actions[name]
    for camera in ('full_body','face_close'):
        cam=bpy.data.objects[cameras[camera]['object']];s.camera=cam
        w,h=320,180;s.render.resolution_x=w;s.render.resolution_y=h;s.render.resolution_percentage=100
        corners=cam.data.view_frame(scene=s);xmin=min(p.x for p in corners);xmax=max(p.x for p in corners);ymin=min(p.y for p in corners);ymax=max(p.y for p in corners);z=corners[0].z
        rot=cam.matrix_world.to_3x3();origin=cam.matrix_world.translation
        for frame in (1,61,121):
            s.frame_set(frame);deps=bpy.context.evaluated_depsgraph_get();verts=[];triangles=[];ids=[];names={}
            for obj in bpy.data.objects:
                if obj.type!='MESH' or obj.hide_render or obj.name=='Stage':continue
                evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
                offset=len(verts);verts.extend(evaluated.matrix_world@v.co for v in mesh.vertices)
                object_id=len(names)+1;names[object_id]=obj.name
                triangles.extend(tuple(offset+i for i in t.vertices) for t in mesh.loop_triangles)
                ids.extend([object_id]*len(mesh.loop_triangles));evaluated.to_mesh_clear()
            tree=BVHTree.FromPolygons(verts,triangles,all_triangles=True)
            depth=np.zeros((h,w),np.float32);mask=np.zeros((h,w),np.uint16)
            for y in range(h):
                ly=ymax-(y+.5)*(ymax-ymin)/h
                for x in range(w):
                    lx=xmin+(x+.5)*(xmax-xmin)/w;direction=rot@Vector((lx,ly,z)).normalized()
                    point,normal,index,distance=tree.ray_cast(origin,direction,20)
                    if index is not None:depth[y,x]=distance;mask[y,x]=ids[index]
            assert np.isfinite(depth).all() and np.count_nonzero(mask)>w*h*.025
            d=OUT/'conditioning'/clip/camera/f'{frame:04d}';d.mkdir(parents=True,exist_ok=True)
            np.save(d/'depth_m.npy',depth);np.save(d/'object_id.npy',mask)
            normalized=np.where(mask>0,1-np.clip((depth-1)/6,0,1),0)
            rgba=np.dstack([normalized]*3+[np.ones_like(normalized)]);png(d/'depth_near_white_1_to_7m.png',rgba)
            subject=(mask>0).astype(np.float32);png(d/'subject_mask.png',np.dstack([subject]*3+[np.ones_like(subject)]))
            pose={}
            for b in r.pose.bones:
                p=r.matrix_world@b.head;uv=world_to_camera_view(s,cam,p)
                pose[b.name]={'world_m':list(p),'uv_top_left':[uv.x,1-uv.y],'in_frame':0<=uv.x<=1 and 0<=uv.y<=1 and uv.z>0,'parent':b.parent.name if b.parent else None}
            meta={'clip':clip,'frame':frame,'time_seconds':(frame-1)/24,'camera':cameras[camera],
                  'resolution':[w,h],'depth':'Euclidean camera-origin distance in meters; background 0; evaluated proxy geometry; CPU BVH, not a neural estimator',
                  'normalization':'gray=1-clamp((distance_m-1)/6), background=0; fixed 1m near / 7m far for all samples',
                  'mask':'0 background; positive original proxy object IDs; subject mask binary. Floor omitted.',
                  'object_ids':names,'pose_convention':'17 original proxy bone heads; custom schema; NOT OpenPose','pose':pose,
                  'input_to_video_model':'NOT_TESTED; no claim of control model compatibility',
                  'foreground_fraction':float(subject.mean()),'depth_min_max_foreground_m':[float(depth[mask>0].min()),float(depth.max())]}
            (d/'metadata.json').write_text(json.dumps(meta,indent=2));records.append({'path':str(d),**{k:meta[k] for k in ('clip','frame','foreground_fraction','depth_min_max_foreground_m')}})
(E/'conditioning_passes.json').write_text(json.dumps({'result':'CPU_GEOMETRY_PASSES_GENERATED_NOT_VIDEO_CONTROL_VALIDATED','elapsed_seconds':time.monotonic()-t0,'samples':records,'gpu_inference':0},indent=2))
print('CONDITIONING_PASSES_PASS',len(records))
