# Editable sweep

For a horn, root, hose or rail whose visible shape follows a path, use
[editable_sweep.py](../../scripts/techniques/editable_sweep.py). It returns two native
Bézier objects: an open path carrying a Geometry Nodes modifier and a hidden closed profile.
The group and both curves are stored in the .blend. Creating a sweep uses a new name;
revise an existing sweep through its spline points.

Run in Blender with the actual directory containing this skill's SKILL.md:

```python
from pathlib import Path
import runpy

skill_dir = Path("/absolute/path/to/blender-modular-scenes")
create_sweep = runpy.run_path(str(skill_dir / "scripts/techniques/editable_sweep.py"))["create_sweep"]
horn, section = create_sweep(
    "Horn",
    [(0, 0, 0), (0.02, 0, 0.5), (0.36, 0.08, 1.1), (0.23, 0.17, 1.7)],
    profile=[(0.28, 0), (0.02, 0.16), (-0.21, 0.04), (-0.10, -0.14), (0.13, -0.11)],
    radii=[1.0, 0.87, 0.52, 0.055],
    tilts=[0, 0.05, 0.14, 0.28],
)
```

**Controls.** Path points are local XYZ. Supply the profile as a simple loop in local XY;
omit its repeated endpoint and place its origin at the intended center of rotation.
Its coordinates determine the base section size. Each positive radius scales that section,
and each tilt rolls it in radians. The default twist mode is `MINIMUM`; `Z_UP` suits
sections that need a consistent up direction away from vertical tangents.
`path_resolution` and `profile_resolution` control samples per segment independently.
`path_handles="VECTOR"` or `profile_handles="VECTOR"` preserves straight segments.
The modifier exposes **Profile** and **Fill Caps**. The profile is hidden for display
and render; edit its spline coordinates to change the section.

**One useful revision.** In a later MCP call, reacquire the object by name:

```python
horn = bpy.context.scene.objects["Horn"]
knots = horn.data.splines[0].bezier_points
knots[-1].co.x += 0.35
```

The helper preserves the user's selection. Address the returned or named object directly.
If you need evaluated geometry in the same script, call `bpy.context.view_layer.update()`
after the edit.

Capture the same front or three-quarter view before and after the edit. Check the base
section and the new tip position. To diagnose roll, use an asymmetric profile and inspect
an oblique view. A tight turn can make the surface cross itself; change the bend or its
radius. Branch junctions require a separate construction. The helper builds geometry
and caps; UVs and materials are separate authoring decisions.

[Sample before](examples/editable-sweep-before.png) · [After moving only the tip](examples/editable-sweep-after.png).
In these front views the last knot moved 0.50 local units along X. Reopening both files
confirmed that the evaluated base ring occupied the same positions.
