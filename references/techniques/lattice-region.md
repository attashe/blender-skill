# Fit a lattice and lift a region

Use [fit_lattice.py](../../scripts/techniques/fit_lattice.py) to raise or lower a local feature of an existing volume while keeping its source mesh and modifier stack editable. The two operations run inside Blender. They preserve the current selection.

**Fit.** `fit_lattice(obj, resolution=(5, 4, 4), name=None)` fits a native lattice to the eight corners of the evaluated bounding box in object-local axes. It appends a Lattice modifier, parents the cage to the target and returns the cage object. All three local extents must be positive and the world transform must be invertible. Repeating the same fit reuses its cage and preserves control edits. A conflicting name or resolution raises an error.

**Lift.** `lift_region(cage, center, radii, dz)` uses world XYZ for the ellipsoid center and positive XYZ radii. Distances are Blender units. A negative `dz` lowers the controls. The weight peaks at the center and falls smoothly to zero at the ellipsoid boundary. Each call sets **every** control from rest, replacing previous lifts and manual edits. Use `dz=0` for a neutral cage. The function returns the number of rest controls inside the region.

The Lattice modifier interpolates between controls, so the mesh can move beyond the control ellipsoid. To keep designated vertices fixed, assign a target vertex group to the modifier and give those vertices zero influence. If using an existing group of fixed vertices, enable the modifier's `invert_vertex_group`. Compare evaluated positions at the contact patch or attachment as well as the feature you're moving.

## Example

For the example boulder, raising the right shoulder uses these world coordinates. Substitute the path to this skill and choose the center and radii from the evaluated target on another asset.

```python
from pathlib import Path
import runpy
import bpy

skill_dir = Path("/absolute/path/to/blender-modular-scenes")
tools = runpy.run_path(str(skill_dir / "scripts/techniques/fit_lattice.py"))
rock = bpy.context.scene.objects["Rock"]
cage = tools["fit_lattice"](rock, resolution=(7, 5, 4))
center = (0.23, -0.18, 0.317)
radii = (0.115, 0.125, 0.17)
controls = tools["lift_region"](cage, center=center, radii=radii, dz=0.162)
print(cage.name, controls)
```

Measure surface displacement with the evaluated mesh at the same vertices before and after the lift. For a fixed region and mask, if a trial moves the surface 0.08 units and the target is 0.10, call `lift_region` again with `dz=trial_dz * 0.10 / 0.08`. Check that the contact stays fixed and compare the same camera view. Save the .blend with the cage and modifier intact.

[Original shoulder](examples/rock-lattice-before.png) · [Raised shoulder](examples/rock-lattice-after.png). In this scene three controls lifted the upper-right surface by up to 0.10377 m. All 668 contact vertices retained world Z = 0, and the opposite side moved less than 0.000001 m.
