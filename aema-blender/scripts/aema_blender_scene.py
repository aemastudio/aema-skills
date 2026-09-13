#!/usr/bin/env python3
"""Validate an AEMA Blender plan or build its basic scene inside Blender."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Versioned .blend destination; required with --execute")
    parser.add_argument("--execute", action="store_true", help="Build and save inside Blender; default is dry-run")
    parser.add_argument("--render-preview", action="store_true", help="Render one reduced-resolution preview frame")
    parser.add_argument("--force", action="store_true", help="Allow replacing the specified .blend output")
    return parser.parse_args(user_args())


def vector(value: Any, length: int, where: str, errors: list[str]) -> None:
    if not isinstance(value, list) or len(value) != length or not all(isinstance(v, (int, float)) for v in value):
        errors.append(f"{where} must be an array of {length} numbers")


def validate(plan: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["plan root must be an object"]
    if plan.get("schema_version") != "aema.blender-plan/v1":
        errors.append("schema_version must be 'aema.blender-plan/v1'")
    if not plan.get("scene_id"):
        errors.append("scene_id is required")
    if plan.get("aspect_ratio") != "9:16":
        errors.append("aspect_ratio must be '9:16'")
    for key in ("fps", "frame_start", "frame_end"):
        if not isinstance(plan.get(key), int) or plan[key] <= 0:
            errors.append(f"{key} must be a positive integer")
    if isinstance(plan.get("frame_start"), int) and isinstance(plan.get("frame_end"), int) and plan["frame_end"] < plan["frame_start"]:
        errors.append("frame_end must be at or after frame_start")

    render = plan.get("render")
    if not isinstance(render, dict):
        errors.append("render must be an object")
    else:
        x, y = render.get("resolution_x"), render.get("resolution_y")
        if not isinstance(x, int) or not isinstance(y, int) or x <= 0 or y <= 0 or x * 16 != y * 9:
            errors.append("render resolution must be a positive exact 9:16 pair")

    objects = plan.get("objects")
    if not isinstance(objects, list):
        errors.append("objects must be an array")
        objects = []
    seen: set[str] = set()
    cameras: set[str] = set()
    for index, item in enumerate(objects):
        where = f"objects[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{where}.id is required")
        elif item_id in seen:
            errors.append(f"duplicate object id: {item_id}")
        else:
            seen.add(item_id)
        kind = item.get("type")
        if kind not in {"camera", "light", "mesh"}:
            errors.append(f"{where}.type must be camera, light, or mesh")
        if kind == "camera" and isinstance(item_id, str):
            cameras.add(item_id)
        transform = item.get("transform", {})
        for field in ("location", "rotation_euler"):
            vector(transform.get(field, [0, 0, 0]), 3, f"{where}.transform.{field}", errors)
        vector(transform.get("scale", [1, 1, 1]), 3, f"{where}.transform.scale", errors)
        for keyframe in item.get("animation", []):
            frame = keyframe.get("frame") if isinstance(keyframe, dict) else None
            if not isinstance(frame, int) or frame < plan.get("frame_start", 1) or frame > plan.get("frame_end", 1):
                errors.append(f"{where} has animation frame outside the scene range")
    if plan.get("active_camera") not in cameras:
        errors.append("active_camera must reference a camera object")
    return errors


def cube_mesh(bpy: Any, name: str, plane: bool = False) -> Any:
    mesh = bpy.data.meshes.new(name + "_MESH")
    if plane:
        vertices = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]
        faces = [(0, 1, 2, 3)]
    else:
        vertices = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    return mesh


def apply_transform(obj: Any, transform: dict[str, Any]) -> None:
    obj.location = transform.get("location", [0, 0, 0])
    obj.rotation_euler = transform.get("rotation_euler", [0, 0, 0])
    obj.scale = transform.get("scale", [1, 1, 1])


def build(plan: dict[str, Any], output: Path, preview: bool, force: bool) -> None:
    try:
        import bpy  # type: ignore
    except ImportError as exc:
        raise RuntimeError("--execute must run inside Blender's Python") from exc

    output = output.resolve()
    if output.suffix.lower() != ".blend":
        raise ValueError("--output must end in .blend")
    if output.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)

    scene_name = f"AEMA_{plan['scene_id']}"
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes.new(scene_name)
    root_name = scene_name + "_ROOT"
    root = bpy.data.collections.get(root_name)
    if root is None:
        root = bpy.data.collections.new(root_name)
        scene.collection.children.link(root)
    elif root.name not in scene.collection.children:
        scene.collection.children.link(root)
    for obj in list(root.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    created: dict[str, Any] = {}
    for spec in plan["objects"]:
        item_id = spec["id"]
        kind = spec["type"]
        if kind == "camera":
            data = bpy.data.cameras.new(item_id + "_DATA")
            data.lens = float(spec.get("camera", {}).get("lens", 50))
        elif kind == "light":
            light_spec = spec.get("light", {})
            data = bpy.data.lights.new(item_id + "_DATA", type=light_spec.get("light_type", "AREA"))
            data.energy = float(light_spec.get("energy", 500))
            data.color = light_spec.get("color", [1, 1, 1])[:3]
            if hasattr(data, "shape") and "size" in light_spec:
                data.size = float(light_spec["size"])
        else:
            data = cube_mesh(bpy, item_id, plane=spec.get("primitive") == "plane")
        obj = bpy.data.objects.new(item_id, data)
        root.objects.link(obj)
        apply_transform(obj, spec.get("transform", {}))
        obj["aema_id"] = item_id
        obj["aema_scene_id"] = plan["scene_id"]
        if kind == "mesh" and isinstance(spec.get("material"), dict):
            material_spec = spec["material"]
            material = bpy.data.materials.new(item_id + "_MAT")
            material.diffuse_color = material_spec.get("base_color", [0.5, 0.5, 0.5, 1])
            material.metallic = float(material_spec.get("metallic", 0))
            material.roughness = float(material_spec.get("roughness", 0.5))
            obj.data.materials.append(material)
        for keyframe in spec.get("animation", []):
            for field in ("location", "rotation_euler", "scale"):
                if field in keyframe:
                    setattr(obj, field, keyframe[field])
                    obj.keyframe_insert(data_path=field, frame=keyframe["frame"])
        created[item_id] = obj

    scene.camera = created[plan["active_camera"]]
    scene.render.fps = plan["fps"]
    scene.frame_start = plan["frame_start"]
    scene.frame_end = plan["frame_end"]
    render = plan["render"]
    scene.render.resolution_x = render["resolution_x"]
    scene.render.resolution_y = render["resolution_y"]
    scene.render.resolution_percentage = 25 if preview else int(render.get("resolution_percentage", 100))
    try:
        scene.render.engine = render.get("engine", "BLENDER_EEVEE_NEXT")
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = int(render.get("samples", 64))
    if scene.world is None:
        scene.world = bpy.data.worlds.new(scene_name + "_WORLD")
    scene.world.color = plan.get("world", {}).get("color", [0.01, 0.01, 0.01, 1])[:3]
    scene["aema_scene_id"] = plan["scene_id"]
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    if preview:
        preview_path = output.with_name(output.stem + "_preview.png")
        scene.render.filepath = str(preview_path)
        scene.frame_set(scene.frame_start)
        bpy.ops.render.render(write_still=True, scene=scene.name)


def main() -> int:
    args = parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid plan JSON: {exc}", file=sys.stderr)
        return 2
    errors = validate(plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    preview = {
        "mode": "execute" if args.execute else "dry-run",
        "scene_id": plan["scene_id"],
        "objects": len(plan["objects"]),
        "frames": [plan["frame_start"], plan["frame_end"]],
        "resolution": [plan["render"]["resolution_x"], plan["render"]["resolution_y"]],
        "output": str(args.output.resolve()) if args.output else None,
        "render_preview": args.render_preview,
    }
    if not args.execute:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0
    if args.output is None:
        print("ERROR: --output is required with --execute", file=sys.stderr)
        return 2
    try:
        build(plan, args.output, args.render_preview, args.force)
    except Exception as exc:
        print(f"ERROR: Blender build failed: {exc}", file=sys.stderr)
        return 3
    print(json.dumps({**preview, "status": "complete"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
