# AEMA Blender Plan

Use `schema_version: "aema.blender-plan/v1"`. The portable plan describes a basic reproducible scene; it does not replace a project-specific production script for rigs, simulations, geometry nodes, compositing, or complex imports.

## Example

```json
{
  "schema_version": "aema.blender-plan/v1",
  "scene_id": "E01-S001",
  "aspect_ratio": "9:16",
  "fps": 24,
  "frame_start": 1,
  "frame_end": 144,
  "render": {
    "resolution_x": 1080,
    "resolution_y": 1920,
    "resolution_percentage": 100,
    "engine": "BLENDER_EEVEE_NEXT",
    "samples": 64,
    "output_path": "06_blender/renders/E01-S001/v001/frame.png"
  },
  "world": {"color": [0.01, 0.02, 0.05, 1.0]},
  "active_camera": "CAM-E01-S001",
  "objects": [
    {
      "id": "CAM-E01-S001",
      "type": "camera",
      "transform": {"location": [0, -8, 2], "rotation_euler": [1.35, 0, 0]},
      "camera": {"lens": 50},
      "animation": []
    },
    {
      "id": "LIGHT-KEY",
      "type": "light",
      "transform": {"location": [2, -2, 5], "rotation_euler": [0, 0, 0]},
      "light": {"light_type": "AREA", "energy": 800, "color": [0.3, 0.5, 1.0], "size": 3.0},
      "animation": []
    },
    {
      "id": "CHAR-001-STANDIN",
      "type": "mesh",
      "primitive": "cube",
      "transform": {"location": [0, 0, 1], "rotation_euler": [0, 0, 0], "scale": [0.4, 0.4, 1.0]},
      "material": {"base_color": [0.8, 0.7, 0.1, 1.0], "metallic": 0.0, "roughness": 0.6},
      "animation": [{"frame": 1, "location": [0, 0, 1]}, {"frame": 144, "location": [1, 0, 1]}]
    }
  ]
}
```

## Invariants

- `scene_id` and object `id` values are stable and unique.
- Resolution is exactly 9:16 for this workflow; previews reduce `resolution_percentage` or use another exact-ratio pair.
- Frames and fps are positive, and `frame_end >= frame_start`.
- Transform values are three-number arrays; colors are RGB or RGBA arrays from 0 to 1.
- Every animation key has a frame inside the scene range.
- A camera named by `active_camera` exists.
- External assets, if added by a project-specific script, carry source paths, AEMA asset versions, hashes, rights/consent status, and explicit missing-file behavior.

The helper creates only cameras, lights, and cube/plane stand-in meshes. Those meshes are visibly provisional. Advanced scene features belong in a versioned project script under `06_blender/scripts/`.
