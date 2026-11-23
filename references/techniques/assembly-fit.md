# Measure the relationship between parts

**Use:** a mirrored pair, seam, sliding clearance, blocked opening or a plausible image
whose dimensions disagree with the intended assembly. Select the smallest relevant pair
or group of parts and choose the direction of the intended clearance.

[spatial_probe.py](../../scripts/spatial_probe.py) runs inside Blender, read-only. Its
`pair_clearance(first_objects, second_objects, axis=(1,0,0))` measures evaluated mesh
vertices in world space. A group may contain several objects: include all relevant rails,
panels or protrusions instead of reporting one side's bounds as the assembly's size.
Record the same complete target groups and axis before and after an edit. A panel's width
does not establish its door assembly's width; a reported source defect needs its own
measurement rather than an inference from the corrected result.
Order FIRST then SECOND along the positive axis. Positive signed clearance is separation;
negative is overlap of their projected intervals. For a rotated assembly, supply its
world-space axis rather than assuming global X. Values are Blender world units; the report
includes the scene's length conversion. Decide the intended gap/tolerance from the design.

```text
blender --background --factory-startup --disable-autoexec INPUT.blend --python-exit-code 1 --python SKILL/scripts/spatial_probe.py -- --expect-file INPUT.blend --first LEFT_PART --second RIGHT_PART --axis 1 0 0 --output-json OUTPUT/fit.json
```

For a script that already identifies the relevant objects, import the measurement rather
than rewriting its geometry math. The caller supplies `skill_scripts`, `input_file`,
`first_parts`, `second_parts`, `world_axis`, `expected_gap` and `tolerance` for this task:

```python
import sys
sys.path.insert(0, skill_scripts)
from api_probe import identity
from spatial_probe import pair_clearance
identity(input_file, [o.name for o in first_parts + second_parts])
measured = pair_clearance(first_parts, second_parts, world_axis)
gap = measured['signed_clearance']
print({'measurement': measured, 'expected': expected_gap, 'tolerance': tolerance,
       'matches': abs(gap - expected_gap) <= tolerance})
```

Keep the geometric measurement generic and the design expectation local. Use a near-zero
gap for intended butt contact, a positive target/minimum for clearance, and inclusive bounds
with tolerance for containment. Strict `inside` inequalities incorrectly reject a panel
intended to meet its frame exactly. Read the predicate result and resolve a mismatch; merely
printing coordinates does not execute the expected-relation check. A small custom probe is
appropriate for a different question; no need to recreate an available measurement for
different object names or report wording.

Repeat `--first`/`--second` for multi-part groups. The perpendicular projected intervals
help locate mismatched extents. This is a directional extent measurement: for flat aligned
mating faces it is useful evidence of fit, but overlapping projections do not prove actual
intersection of curved, hollow or offset shapes. Negative clearance also occurs if the
groups were supplied in reverse order. Inspect the actual intended contact region; use
sections, local samples or a dedicated collision test when extent overlap is ambiguous.
The helper does not certify thickness, shortest surface distance or unrealized instances.

**An opening that seems blocked:** use `first_hit(origin, direction, distance)` with
world coordinates, or CLI `--ray OX OY OZ DX DY DZ DIST`. Cast through the intended opening
and through adjacent retained material. A few rays at center and near the edges discriminate
a blocked cavity from a shading problem; they do not certify the entire opening. Report the
first actual object, including unexpected occluders; do not filter to the object you hope
to hit. Scene ray casting uses the current viewport graph, so hidden cutters, instances,
render-only modifiers and visibility differences require a corresponding section/render.
Never automatically alter visibility to make a measurement pass.

**Close the loop:** compare measurements with the expected relation, change only owned
sources, and repeat the same observation. Open a useful image too. A successful script,
positive mesh volume or printed coordinate list is not an assembly check by itself.
For saved render readiness, `api_probe.identity()` reports active scene/camera, engine and
resolution. Inspect these after reopening, before assigning a camera or changing settings;
such setup edits would conceal a missing saved camera. A named camera object is insufficient.

The probes keep selection, geometry, frame and file unchanged. CLI exit 0 means the
measurement completed, not that the asset passed. Object Mode mesh targets and the current
scene/frame are required; `--scene` asserts identity, and `--max-vertices` bounds the sample
after evaluation (it cannot prevent a costly modifier from evaluating).

Author-tested in Blender 5.2.1 LTS: separated/overlapping/offset boxes, rotated assemblies,
negative scale, evaluated Array, multi-part groups, ray hit/miss/range, save/reopen camera
state, invalid input rejection and an actual assembly with overlapping door parts.
These measurements do not establish visual quality or independent agent adoption.

[Evaluated mesh lifetime](https://docs.blender.org/api/current/bpy.types.Object.html) ·
[Scene ray casting](https://docs.blender.org/api/5.2/bpy.types.Scene.html) ·
[Shell orientation](mesh-orientation.md) · [API diagnostics](../api-diagnostics.md)
