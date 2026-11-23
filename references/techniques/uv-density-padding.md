# Keep texel density and padding through packing

**Use:** related parts need comparable texture scale, a specified px/m target or bake-safe
gaps. Define image dimensions, physical units, allowed rotations/sharing and whether density
is absolute or only relative. Average Island Scale gives relative allocation; Pack with Scale
can change the absolute density again.

For already unwrapped, selected editable islands with UV selection synchronized as intended:

```python
bpy.ops.uv.average_islands_scale()
bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM', rotate=True, scale=True,
                      margin_method='FRACTION', margin=gutter_px / resolution,
                      shape_method='CONCAVE')
```

This is a square-image, freely rotatable, relative-density starting point, not an absolute
px/m guarantee. Disable rotations for directional art. For a fixed density, set island scale
and pack without changing it (or use appropriate pin restrictions); if it cannot fit, change
the texture budget/sharing/priorities explicitly. Don't silently lower density to fit.

For a triangle or island, an area estimate in pixels per physical unit is
`sqrt(sum(abs(UV triangle area)) * width * height / sum(world triangle area))`.
Use evaluated/world dimensions appropriate to the consumer, and convert scene units to meters.
Measure each relevant island/region: a whole-object average can hide local allocation errors.
An area-preserving stretch U×2, V×0.5 keeps this density but distorts the image; inspect an
oriented checker and directional/angle distortion too. A triangle's UV-to-surface Jacobian
singular-value ratio detects that anisotropy; density alone cannot.

**First proof:** two differently sized objects, changed dimensions/resolution, actual packed
coordinates, a 3D checker, and a saved/reopened layout. Compare bounds, zero-area triangles,
unintended overlaps, density and nearest **boundary** separation. UV seam marks and island
center distances are insufficient. Test a deliberately stretched patch to verify diagnosis.

Distinguish per-island gutter from the full gap between neighbors. In the tested Fraction
layout `gutter_px/resolution` produced about twice that amount between islands and one gutter
to the tile boundary; measure the actual result, don't assume every pack mode/version shares
this interpretation. Bake dilation fills pixels; UV padding reserves space. Both are needed,
with allowance for filtering/mips. For non-square textures, UDIM or lightmaps follow the
[consumer-specific guide](../uv-workflow.md#pack-to-the-actual-image-atlas-region-or-tile).

[Packing and scale](https://docs.blender.org/manual/nb/4.5/modeling/meshes/uv/editing.html) ·
[Evidence](provenance.md#bake-and-uv-extraction-batch)
