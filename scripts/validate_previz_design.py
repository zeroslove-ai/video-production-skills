"""Offline R1 contract checks. Requires Python 3.10+ and jsonschema 4.x.

This checks design fixtures, not Blender rendering or asset readiness.
Use --production to additionally reject placeholder / unapproved manifests.
"""
import argparse
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_map(items, key):
    result = {item[key]: item for item in items}
    require(len(result) == len(items), f"Duplicate {key}")
    return result


def end(frame_range):
    return frame_range["start"] + frame_range["duration"]


def within(selected, available):
    return selected["start"] >= available["start"] and end(selected) <= end(available)


def schema_check(data, schema, label):
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: str(e.path))
    require(not errors, f"{label}: " + "; ".join(f"{list(e.path)} {e.message}" for e in errors))


def validate_sequence(seq, shots, cameras, lights, production=False):
    require(math.gcd(seq["fps"]["numerator"], seq["fps"]["denominator"]) == 1, "FPS not reduced")
    assets = unique_map(seq["assets"], "asset_id")
    entries = unique_map(seq["shots"], "shot_id")
    intervals = []
    for sid, entry in entries.items():
        shot = shots[sid]
        require(shot["sequence_id"] == seq["sequence_id"], f"{sid}: sequence mismatch")
        require(shot["revision"] == entry["revision"], f"{sid}: stale revision")
        for key in ("fps", "resolution", "production_mode", "reference_packs"):
            require(shot[key] == seq[key], f"{sid}: {key} mismatch")
        require(shot["source_range"] == entry["source_range"], f"{sid}: source selection mismatch")
        camera = cameras[shot["camera"]["preset_id"]]
        light = lights[shot["lighting"]["preset_id"]]
        require(shot["camera"]["preset_revision"] == camera["revision"] and shot["lighting"]["preset_revision"] == light["revision"], f"{sid}: preset revision")
        require(seq["production_mode"] in camera["allowed_modes"] and seq["production_mode"] in light["allowed_modes"], f"{sid}: preset mode")
        local_assets = unique_map(shot["assets"], "asset_id")
        for aid, asset in local_assets.items():
            require(asset == assets.get(aid), f"{sid}: asset revision differs for {aid}")
        placements = unique_map(shot["placements"], "instance_id")
        for placement in placements.values():
            require(placement["asset_id"] in local_assets, f"{sid}: placement asset missing")
            require(local_assets[placement["asset_id"]]["kind"] in ("character", "set", "prop"), f"{sid}: non-spatial placement")
        require(shot["camera"]["overrides"]["subject_id"] in placements, f"{sid}: camera subject missing")
        for animation in shot["animations"]:
            require(animation["entity_id"] in placements, f"{sid}: clip entity missing")
            entity_asset = local_assets[placements[animation["entity_id"]]["asset_id"]]
            require(entity_asset["kind"] == "character", f"{sid}: clip entity is not character")
            require(entity_asset.get("binding_id") == animation["binding_id"], f"{sid}: character binding mismatch")
            clip = local_assets[animation["clip_asset_id"]]
            require(clip["kind"] == "animation_clip", f"{sid}: invalid clip kind")
            require(clip["fps"] == seq["fps"], f"{sid}: retime needs explicit future contract")
            require(clip["binding_id"] == animation["binding_id"], f"{sid}: incompatible binding")
            require(entity_asset["root_motion_policy"] == clip["root_motion_policy"] == animation["root_motion_policy"], f"{sid}: root motion mismatch")
            require(animation["clip_range"]["duration"] == shot["source_range"]["duration"], f"{sid}: clip duration mismatch")
            available = clip["available_range"]
            selected = animation["clip_range"]
            with_handles = {"start": selected["start"] - shot["handles"]["in"],
                            "duration": selected["duration"] + shot["handles"]["in"] + shot["handles"]["out"]}
            require(within(with_handles, available), f"{sid}: clip/handles outside availability")
            if "facial_clip_asset_id" in animation:
                face = local_assets[animation["facial_clip_asset_id"]]
                require(face["kind"] == "facial_expression_clip", f"{sid}: invalid facial input")
                require(face["binding_id"] == animation["binding_id"] and face["fps"] == seq["fps"], f"{sid}: incompatible facial binding/rate")
                require(within(with_handles, face["available_range"]), f"{sid}: facial clip/handles outside availability")
        require(all(shot["source_range"]["start"] <= frame < end(shot["source_range"]) for frame in shot["board"]["panel_source_frames"]), f"{sid}: panel out of range")
        require(shot["export_contract"]["depth_near_m"] < shot["export_contract"]["depth_far_m"], f"{sid}: depth bounds reversed")
        require(shot["export_contract"]["view_transform"] == light["color"]["view_transform"], f"{sid}: look mismatch")
        for prop in shot["continuity"]["prop_states"]:
            require(prop in placements, f"{sid}: prop state entity missing")
        intervals.append((entry["timeline_start"], entry["timeline_start"] + entry["source_range"]["duration"]))
        if production:
            require(shot["status"] == "locked" and shot["art_review"]["status"] == "approved", f"{sid}: not approved/locked")
    intervals.extend((g["timeline_start"], g["timeline_start"] + g["duration"]) for g in seq["gaps"])
    cursor = 0
    for start, finish in sorted(intervals):
        require(start == cursor, f"{seq['sequence_id']}: overlap or undeclared gap at {cursor}")
        cursor = finish
    require(cursor == seq["duration_frames"], "Sequence duration mismatch")
    if "duration_target_frames" in seq:
        require(cursor == seq["duration_target_frames"], "Design duration target mismatch")
    unique_map(seq["audio_tracks"], "track_id")
    clip_ids = []
    for track in seq["audio_tracks"]:
        previous_end = 0
        for clip in sorted(track["clips"], key=lambda c: c["timeline_start"]):
            asset = assets[clip["asset_id"]]
            require(asset["kind"] == "audio" and asset["fps"] == seq["fps"], "Audio asset/rate mismatch")
            require(within(clip["source_range"], asset["available_range"]), "Audio source outside availability")
            finish = clip["timeline_start"] + clip["source_range"]["duration"]
            require(previous_end <= clip["timeline_start"] and finish <= cursor, "Audio overlap/outside sequence")
            previous_end = finish
            clip_ids.append(clip["clip_id"])
    require(len(set(clip_ids)) == len(clip_ids), "Duplicate audio clip ID")
    for event in seq["handoff"]["event_markers"]:
        require(event["timeline_frame"] < cursor, "Event outside timeline")
    for cue in seq.get("subtitle_cues", []):
        require(cue["timeline_start"] + cue["duration"] <= cursor, "Subtitle outside timeline")
    if production:
        require(seq["status"] == "locked" and seq["art_review"]["status"] == "approved", "Sequence not approved/locked")
        require(all(a["intake_status"] == "verified" and a["sha256"] != "0" * 64 for a in assets.values()), "Placeholder assets")
        require(all("PLACEHOLDER" not in r["revision"] for r in seq["reference_packs"]), "Placeholder references")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    shot_schema = read(ROOT / "schemas/shot_manifest.schema.json")
    seq_schema = read(ROOT / "schemas/sequence_manifest.schema.json")
    for schema in (shot_schema, seq_schema):
        Draft202012Validator.check_schema(schema)
    cameras = unique_map(read(ROOT / "presets/camera_presets.json")["presets"], "preset_id")
    lights = unique_map(read(ROOT / "presets/lighting_presets.json")["presets"], "preset_id")
    modes = unique_map(read(ROOT / "presets/production_modes.json")["modes"], "mode_id")
    require(set(modes) == {"CHARACTER_SHORT", "WEB_DRAMA", "GAME_CUTSCENE"}, "Production modes incomplete")
    for camera in cameras.values():
        for key in ("shot_size", "lens_mm", "camera_height", "camera_pitch", "camera_yaw", "subject_position", "headroom", "DOF", "movement", "movement_speed", "intended_emotion", "recommended_lighting"):
            require(key in camera, f"{camera['preset_id']}: missing camera metadata {key}")
        require(camera["recommended_lighting"] in lights, "Unknown recommended lighting")
        require(camera["allowed_lens_mm_range"][0] <= camera["lens_mm"] <= camera["allowed_lens_mm_range"][1], "Lens outside allowed range")
        require(camera["movement"] == camera["motion"]["type"], "Motion representations differ")
        require(camera["movement_speed"]["translation_m_per_sec"] <= camera["motion"]["translation_speed_m_per_sec_max"], "Motion speed exceeds limit")
    for lighting in lights.values():
        for key in ("key", "fill", "rim", "background_light", "environment", "eye_catchlight", "face_readability", "skin_toon_readability", "hair_rim", "background_separation"):
            require(key in lighting, f"{lighting['preset_id']}: missing look component {key}")
    templates = unique_map(read(ROOT / "presets/shot_templates.json")["templates"], "template_id")
    for template in templates.values():
        require(template["camera_preset_id"] in cameras and template["lighting_preset_id"] in lights, "Unknown template preset")
        require(template["duration_frames_range"][0] <= template["duration_frames_range"][1], "Invalid template duration range")
    used = set()
    sequence_count = 0
    for path in sorted((ROOT / "examples/previz").glob("*.sequence.json")):
        seq = read(path)
        require(seq["production_mode"] in modes, "Unknown mode")
        schema_check(seq, seq_schema, path.name)
        shots = {}
        for entry in seq["shots"]:
            target = (path.parent / entry["manifest_uri"]).resolve()
            require(target.is_relative_to(path.parent.resolve()), "Fixture URI escapes directory")
            shot = read(target)
            schema_check(shot, shot_schema, target.name)
            require(shot["shot_id"] == entry["shot_id"], "Referenced shot ID differs")
            require(shot["shot_id"] not in used, "Duplicate global shot ID")
            used.add(shot["shot_id"])
            shots[shot["shot_id"]] = shot
        validate_sequence(seq, shots, cameras, lights, args.production)
        sequence_count += 1
        print(f"PASS {seq['sequence_id']}: {len(shots)} shots, {seq['duration_frames']} frames")
    require(sequence_count > 0, "No sequences found")
    require(len(list((ROOT / "examples/previz").glob("*.shot.json"))) == len(used), "Orphan fixture shots")
    print(f"DESIGN PASS: {sequence_count} sequences / {len(used)} shots / {len(cameras)} cameras / {len(lights)} looks / {len(templates)} templates")
    print("Media existence, hashes, render alignment, approved reference index and Blender/OTIO execution require R2 evidence.")


if __name__ == "__main__":
    main()
