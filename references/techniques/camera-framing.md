# Check that the diagnostic view shows the intended feature

**Use:** an empty/cropped close-up, a rotated sample seen only from its edge, or a camera
that exists but cannot establish the requested comparison. Start with the target geometry
and the surface/joint the image must show, not only a camera location and look-at point.

[camera_probe.py](../../scripts/camera_probe.py) runs read-only inside Blender:
`inspect_frame(camera, objects)` projects evaluated mesh bounds into a perspective/orthographic
camera; `face_angle(camera, object, local_normal)` measures the viewing angle of a caller-known
surface normal at the bounds center. It does not guess which surface should be visible.

```text
blender --background --factory-startup --disable-autoexec INPUT.blend --python-exit-code 1 --python SKILL/scripts/camera_probe.py -- --expect-file INPUT.blend --camera DETAIL_CAMERA --object TARGET --face TARGET 0 1 0 --output-json OUTPUT/framing.json
```

Replace the normal with the actual target's local direction; `0 1 0` is only an example.
Repeat `--object` for the joint's relevant parts. Without `--camera`, the probe uses the
loaded active camera and fails if none is assigned. `--scene` asserts the active scene.
Import the functions when the caller already has the target objects; choose the smallest
set that contains the evidence, not every object in the scene.

NDC X/Y from 0 to 1 spans the full frame. Depth is along the camera's viewing axis; corners
behind or crossing its plane do not have a useful combined 2D rectangle. Bounds outside the
frame or clip range identify a framing concern, not necessarily a clipped mesh silhouette.
The projected pixel extent is a bounding rectangle, not occupied pixel count. Surface angle
near 90 degrees means an edge-on view; moving farther away or changing focal length alone
does not expose the face. Choose azimuth/elevation for the feature, then frame it with margin.

The measurement uses current scene/frame and viewport evaluation. It does not establish
occlusion, render visibility, crop borders/compositor crops, DOF or material readability.
Do not infer a deformed surface normal from its undeformed object axis. Panoramic cameras
and unrealized instances are outside this helper. CLI success means a measurement completed.
Open a small actual image before spending on finish; retain a reproducible saved review view.

Author-tested in Blender 5.2.1 LTS on perspective/orthographic framing, off-frame and behind
targets, far clipping, lens shift, front/edge-on directions, evaluated Array, invalid inputs
and the actual poorly framed rotated AV08 sample. No scene edits by the measurements;
independent agent adoption of this helper remains untested.

[Projection utility](https://docs.blender.org/api/5.2/bpy_extras.object_utils.html) ·
[Camera/light workflow](../blockout-camera-light.md) · [Production lighting](../lighting-workflow.md)
