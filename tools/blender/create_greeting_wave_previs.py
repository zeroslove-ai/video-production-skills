"""Create a small Blender greeting-wave previs, not a production Yuri rig.

Run with:
  blender --background --factory-startup --python create_greeting_wave_previs.py -- --output-dir <dir>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import glob
import shutil
import subprocess
import sys

import bpy
from mathutils import Vector


def arguments() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args(argv)


def material(name: str, color: tuple[float, float, float, float], roughness: float = 0.75):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = color
    principled.inputs["Roughness"].default_value = roughness
    return mat


def ellipsoid(name: str, loc, scale, mat, segments: int = 20, rings: int = 12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj


def cylinder(name: str, loc, radius: float, depth: float, mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("Soft edges", "BEVEL")
    bevel.width = 0.08
    bevel.segments = 2
    obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return obj


def empty(name: str, loc, parent=None):
    obj = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    if parent is not None:
        preserve_parent(obj, parent)
    return obj


def preserve_parent(child, parent):
    bpy.context.view_layer.update()
    world = child.matrix_world.copy()
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()
    child.matrix_basis = world
    bpy.context.view_layer.update()


def animate_rotation(obj, frames):
    for frame, rotation_y in frames:
        obj.rotation_euler[1] = rotation_y
        obj.keyframe_insert(data_path="rotation_euler", index=1, frame=frame)


def parent_keep_world(child, parent):
    preserve_parent(child, parent)
    return child


def add_smile(mat):
    curve = bpy.data.curves.new("soft smile curve", type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.018
    curve.bevel_resolution = 3
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(2)
    for point, co in zip(spline.bezier_points, [(-0.12, -0.405, 2.96), (0, -0.44, 2.925), (0.12, -0.405, 2.96)]):
        point.co = co
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    mouth = bpy.data.objects.new("subtle smile", curve)
    bpy.context.scene.collection.objects.link(mouth)
    curve.materials.append(mat)
    return mouth


def main():
    args = arguments()
    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 448
    scene.render.resolution_y = 768
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.film_transparent = False
    scene.render.filepath = os.path.join(output_dir, "frame_")
    scene.frame_start = 1
    scene.frame_end = 73
    scene.render.image_settings.color_depth = "8"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.render.image_settings.color_mode = "RGB"
    scene.world.color = (0.09, 0.12, 0.2)

    skin = material("warm skin", (0.92, 0.55, 0.38, 1))
    hair = material("dark brown hair", (0.12, 0.055, 0.048, 1))
    blouse = material("ivory blouse", (0.93, 0.9, 0.82, 1))
    skirt_mat = material("deep teal skirt", (0.055, 0.28, 0.32, 1))
    shoe_mat = material("dark shoes", (0.045, 0.06, 0.085, 1))
    eye_mat = material("eyes", (0.09, 0.045, 0.055, 1), 0.25)
    smile_mat = material("smile", (0.4, 0.09, 0.12, 1))
    backdrop_mat = material("soft lilac backdrop", (0.21, 0.25, 0.37, 1))

    # Simple low-poly human proxy in frontal view.
    ellipsoid("torso", (0, 0, 2.03), (0.53, 0.32, 0.69), blouse)
    ellipsoid("skirt", (0, 0, 1.32), (0.54, 0.34, 0.42), skirt_mat)
    cylinder("neck", (0, 0, 2.7), 0.16, 0.25, skin)
    ellipsoid("head", (0, -0.025, 3.17), (0.43, 0.37, 0.53), skin)
    ellipsoid("hair cap", (0, 0.005, 3.49), (0.455, 0.395, 0.31), hair)
    ellipsoid("front fringe", (0, -0.302, 3.37), (0.39, 0.12, 0.18), hair)
    for x in (-0.155, 0.155):
        ellipsoid("eye", (x, -0.367, 3.17), (0.045, 0.032, 0.067), eye_mat, segments=16, rings=10)
    add_smile(smile_mat)

    for x in (-0.22, 0.22):
        ellipsoid("leg", (x, 0, 0.64), (0.15, 0.18, 0.52), skin)
        ellipsoid("shoe", (x, -0.085, 0.16), (0.19, 0.29, 0.13), shoe_mat)

    # Relaxed left arm, made from separate pieces for an editable previs gesture.
    left_shoulder = (-0.49, 0, 2.47)
    left_pivot = empty("left shoulder pivot", left_shoulder)
    left_upper = ellipsoid("left upper arm", (-0.68, 0, 2.12), (0.145, 0.16, 0.39), blouse)
    parent_keep_world(left_upper, left_pivot)
    left_elbow = empty("left elbow pivot", (-0.75, 0, 1.77), left_pivot)
    left_forearm = ellipsoid("left forearm", (-0.79, -0.005, 1.47), (0.12, 0.135, 0.34), skin)
    parent_keep_world(left_forearm, left_elbow)
    left_hand = ellipsoid("left hand", (-0.81, -0.03, 1.19), (0.14, 0.10, 0.16), skin)
    parent_keep_world(left_hand, left_elbow)

    # Right arm rises from a relaxed pose, then waves from the elbow/forearm.
    right_shoulder = (0.49, 0, 2.47)
    right_pivot = empty("right shoulder pivot", right_shoulder)
    right_upper = ellipsoid("right upper arm", (0.68, 0, 2.12), (0.145, 0.16, 0.39), blouse)
    parent_keep_world(right_upper, right_pivot)
    right_elbow = empty("right elbow pivot", (0.75, 0, 1.77), right_pivot)
    right_forearm = ellipsoid("right forearm", (0.79, -0.005, 1.47), (0.12, 0.135, 0.34), skin)
    parent_keep_world(right_forearm, right_elbow)
    right_hand = ellipsoid("right hand", (0.81, -0.03, 1.19), (0.14, 0.10, 0.16), skin)
    parent_keep_world(right_hand, right_elbow)

    # Three small separated finger hints, visible at portrait scale without detailed rigging.
    for offset in (-0.085, 0, 0.085):
        finger = ellipsoid("right fingertip hint", (0.81 + offset, -0.055, 1.075), (0.035, 0.045, 0.115), skin, segments=12, rings=8)
        parent_keep_world(finger, right_elbow)

    animate_rotation(right_pivot, [(1, 0), (12, 0), (23, -2.28), (61, -2.28), (72, 0), (73, 0)])
    wave = [(23, 0.15)]
    for frame, angle in [(29, -0.46), (35, 0.46), (41, -0.46), (47, 0.46), (53, -0.46), (59, 0.15), (61, 0.15), (72, 0.15), (73, 0.15)]:
        wave.append((frame, angle))
    animate_rotation(right_elbow, wave)

    # Small breathing / weight shift, kept subtle enough for a clean blockout.
    torso = bpy.data.objects.get("torso")
    for frame, z in [(1, 2.03), (18, 2.06), (36, 2.03), (54, 2.06), (73, 2.03)]:
        torso.location.z = z
        torso.keyframe_insert(data_path="location", index=2, frame=frame)

    # Blink by scaling the eye meshes vertically at two brief points.
    eyes = [obj for obj in scene.objects if obj.name == "eye"]
    for eye in eyes:
        for frame, factor in [(1, 1), (17, 1), (19, 0.12), (21, 1), (50, 1), (52, 0.12), (54, 1), (73, 1)]:
            eye.scale.z = 0.067 * factor
            eye.keyframe_insert(data_path="scale", index=2, frame=frame)

    # Floor and graphic-free studio background.
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "floor"
    floor.data.materials.append(backdrop_mat)
    floor.modifiers.new("Ground normal", "WEIGHTED_NORMAL")

    world = bpy.data.worlds.new("studio world") if not bpy.data.worlds else bpy.data.worlds[0]
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.16, 0.19, 0.28, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45

    def area_light(name, loc, power, size, color):
        data = bpy.data.lights.new(name, type="AREA")
        data.energy = power
        data.shape = "DISK"
        data.size = size
        data.color = color
        obj = bpy.data.objects.new(name, data)
        scene.collection.objects.link(obj)
        obj.location = loc
        obj.rotation_euler = (Vector((0, 0, 2)) - obj.location).to_track_quat("-Z", "Y").to_euler()

    area_light("large key", (-3.8, -4.5, 6.0), 460, 4.2, (1.0, 0.83, 0.72))
    area_light("soft fill", (3.4, -2.8, 4.1), 300, 3.2, (0.69, 0.81, 1.0))
    area_light("hair rim", (0, 2.4, 4.9), 500, 2.5, (0.74, 0.82, 1.0))

    camera_data = bpy.data.cameras.new("previs camera")
    camera = bpy.data.objects.new("previs camera", camera_data)
    scene.collection.objects.link(camera)
    camera.location = (0, -9, 1.93)
    target = Vector((0, 0, 1.82))
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 4.55
    camera_data.lens = 50
    scene.camera = camera

    scene.render.filepath = os.path.join(output_dir, "frame_")
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = os.path.join(output_dir, "greeting_wave_blender_previs")
    scene.render.image_settings.media_type = "VIDEO"
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "HIGH"
    scene.render.ffmpeg.ffmpeg_preset = "GOOD"

    blend_path = os.path.join(output_dir, "greeting_wave_blender_previs.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    stills = []
    for frame, filename in ((1, "blender_start.png"), (42, "blender_wave_peak.png"), (73, "blender_end.png")):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        scene.render.filepath = os.path.join(output_dir, filename)
        bpy.ops.render.render(write_still=True)
        stills.append(filename)
    scene.render.filepath = os.path.join(output_dir, "greeting_wave_blender_previs.mp4")
    scene.render.image_settings.media_type = "VIDEO"
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    bpy.ops.render.render(animation=True)
    candidates = sorted(glob.glob(os.path.join(output_dir, "greeting_wave_blender_previs*")))
    video_candidates = [path for path in candidates if path.lower().endswith((".mkv", ".mp4", ".mov"))]
    source_video = max(video_candidates, key=os.path.getmtime, default=None)
    if source_video is None:
        raise RuntimeError(f"Blender did not produce a recognized video file: {candidates}")
    output_path = os.path.join(output_dir, "greeting_wave_blender_previs.mp4")
    if os.path.abspath(source_video) != os.path.abspath(output_path):
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            raise RuntimeError("ffmpeg was not found on PATH; Blender output is preserved at " + source_video)
        subprocess.run(
            [ffmpeg, "-y", "-i", source_video, "-map", "0:v:0", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    digest = hashlib.sha256()
    with open(output_path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    metadata = {
        "purpose": "blender_greeting_wave_previs_proxy_only",
        "blender_version": bpy.app.version_string,
        "render_engine": scene.render.engine,
        "resolution": [scene.render.resolution_x, scene.render.resolution_y],
        "fps": scene.render.fps,
        "frames": scene.frame_end - scene.frame_start + 1,
        "duration_seconds": round((scene.frame_end - scene.frame_start + 1) / scene.render.fps, 6),
        "keyframe_preview_images": stills,
        "editable_blend_file": os.path.basename(blend_path),
        "motion_representation": "keyframed_empty_pivots_and_separate_meshes_not_a_humanoid_armature",
        "output_file": os.path.basename(output_path),
        "blender_intermediate_file": os.path.basename(source_video),
        "output_bytes": os.path.getsize(output_path),
        "output_sha256": digest.hexdigest(),
    }
    with open(os.path.join(output_dir, "blender_metrics.json"), "w", encoding="utf-8") as stream:
        json.dump(metadata, stream, indent=2, ensure_ascii=False)
    print(f"PREVIS_OUTPUT={output_dir}")


if __name__ == "__main__":
    main()
