# Open a cylindrical surface into a useful UV strip

**Use:** a tube, canister or other cylindrical region needs coherent texture direction.
Choose the longitudinal cut on a hidden/back/construction line. Separate end caps where
appropriate. A simple closed cylinder then has one side strip plus two cap islands; this
is a shape-specific expectation, not a universal island-count rule.

Assign seams on the intended edges, then unwrap selected faces into an explicit UV map.
UVs belong to face corners: a seam vertex has different coordinates on its two sides.
Removing a seam flag does not itself erase an existing UV split. After leaving Edit Mode,
reacquire the mesh's UV layer before reading its corner data; cached RNA wrappers can be stale.
Preserve existing paint/bake dependencies or work on a derived layout. Do not detect a
general mesh's seams by vertex index or assume every horizontal edge is a cap boundary.

For a caller-selected object/face region in Edit Mode, with the intended UV layer active:

```python
bpy.ops.uv.unwrap(method='MINIMUM_STRETCH', iterations=20,
                  correct_aspect=True, margin=0.005)
```

This tested method is an option; Conformal, Angle Based, cylindrical projection or Follow
Active Quads may suit another topology. Selection, pins, active image/aspect and mode affect
the operation. Unwrap margin here is provisional; [final packing](uv-density-padding.md)
determines actual density and gaps.

**First proof:** inspect both the strip/caps and an oriented checker on the 3D surface.
Measure directional scale on the strip; cutting caps alone leaves a closed side band and
does not establish a low-distortion strip. Compare one deliberate missing/changed seam.
The extracted case uses flat-faceted cylinders and a box with separate face islands; the
box's all-edge seam scheme is not a general recommendation for a painted prop.

Keep grain/text upright where it matters; free island rotation can break that requirement.
Save the UV name and named UV Map consumer, reopen and compare corner coordinates and the
checker. Blender's generated COLOR_GRID is a generated image, not a missing external file.
For organic surfaces, trim sheets, UDIM or mirrored normal maps use the [UV guide](../uv-workflow.md).

[Seam planning](https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/unwrapping/seams.html) ·
[Evidence](provenance.md#bake-and-uv-extraction-batch)
