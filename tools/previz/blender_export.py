"""Disposable background Blender scene; never run this in a production .blend."""
import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value = (*color, 1)
    return mat


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--smoke', action='store_true', help='9 frames at 320x192; not production conditioning')
    args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
    m = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Output directory must be empty; choose a new run directory')
    out.mkdir(parents=True, exist_ok=True)
    # A new process started with --factory-startup is required by the runbook.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = 4
    s.cycles.use_denoising = True
    s.render.resolution_x = 320 if args.smoke else m['width']
    s.render.resolution_y = 192 if args.smoke else m['height']
    s.render.resolution_percentage = 100
    s.render.fps = m['fps']
    s.frame_start = 1
    s.frame_end = 9 if args.smoke else m['frame_count']
    s.render.image_settings.file_format = 'PNG'
    s.world = bpy.data.worlds.new('PrevizWorld')
    s.world.use_nodes = True
    s.world.node_tree.nodes.get('Background').inputs[0].default_value = (0.12, 0.16, 0.24, 1)
    bpy.ops.mesh.primitive_plane_add(size=200)
    floor = bpy.context.object
    floor.name = 'PrevizFloor'
    floor.data.materials.append(material('FloorBlue', (0.03, 0.16, 0.3)))
    bpy.ops.mesh.primitive_cube_add(size=1.6, location=(-1.3, 0, 0.8))
    cube = bpy.context.object
    cube.name = 'PrevizCube'
    cube.data.materials.append(material('CubeOrange', (0.9, 0.18, 0.025)))
    for frame, x in [(1, -1.3), (s.frame_end, 1.3)]:
        cube.location.x = x
        cube.keyframe_insert('location', frame=frame)
    bpy.ops.object.camera_add(location=(6, -9, 5))
    camera = bpy.context.object
    camera.name = 'PrevizCamera'
    camera.data.lens = 45
    s.camera = camera
    for frame, x in [(1, 6), (s.frame_end, 4)]:
        camera.location.x = x
        camera.rotation_euler = (Vector((0, 0, 0.8)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
        camera.keyframe_insert('location', frame=frame)
        camera.keyframe_insert('rotation_euler', frame=frame)
    bpy.ops.object.light_add(type='AREA', location=(2, -3, 7))
    bpy.context.object.data.energy = 1100
    bpy.context.object.data.shape = 'DISK'
    bpy.context.object.data.size = 5
    state = {'blender': bpy.app.version_string, 'objects': sorted(o.name for o in s.objects),
             'engine': s.render.engine, 'fps': s.render.fps, 'frame_count': s.frame_end,
             'width': s.render.resolution_x, 'height': s.render.resolution_y,
             'smoke': args.smoke, 'samples': []}
    for frame in [1, (s.frame_end + 1)//2, s.frame_end]:
        s.frame_set(frame)
        state['samples'].append({'frame': frame, 'cube_location': list(cube.location),
                                 'camera_matrix_world': [list(row) for row in camera.matrix_world]})
    s.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'previz.blend'))
    for stream in ['beauty', 'depth']:
        (out / stream).mkdir()
    s.render.filepath = str(out / 'beauty' / '') + '/'
    bpy.ops.render.render(animation=True)
    # Fixed camera-space depth: near=white, far/background=black. No per-frame normalization.
    depth = bpy.data.materials.new('FixedCameraDepth')
    depth.use_nodes = True
    n = depth.node_tree.nodes
    n.clear()
    camera_data = n.new('ShaderNodeCameraData')
    mapping = n.new('ShaderNodeMapRange')
    mapping.inputs['From Min'].default_value = m['depth_near']
    mapping.inputs['From Max'].default_value = m['depth_far']
    mapping.inputs['To Min'].default_value = 1
    mapping.inputs['To Max'].default_value = 0
    mapping.clamp = True
    emission = n.new('ShaderNodeEmission')
    output = n.new('ShaderNodeOutputMaterial')
    links = depth.node_tree.links
    links.new(camera_data.outputs['View Z Depth'], mapping.inputs['Value'])
    links.new(mapping.outputs[0], emission.inputs['Color'])
    links.new(emission.outputs[0], output.inputs['Surface'])
    s.view_layers[0].material_override = depth
    s.world.node_tree.nodes.get('Background').inputs[0].default_value = (0, 0, 0, 1)
    s.view_settings.view_transform = 'Standard'
    s.view_settings.look = 'None'
    s.view_settings.exposure = 0
    s.view_settings.gamma = 1
    s.cycles.use_denoising = False
    s.render.filepath = str(out / 'depth') + '/'
    bpy.ops.render.render(animation=True)
    state['depth'] = {'kind': 'camera-space-z-shader', 'near': m['depth_near'], 'far': m['depth_far'],
                      'encoding': 'PNG display-encoded grayscale, near white; not metric EXR Z pass'}
    (out / 'scene-state.json').write_text(json.dumps(state, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
