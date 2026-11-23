# Project the intended high surface onto a receiver

**Use:** transfer geometric normals or a source field from high to low. Stabilize the
receiver's UVs, topology/triangulation and shading normals for its actual consumer. Inspect
both surfaces in the same pose/space. A normal map cannot replace silhouette or parallax.

Start on one isolated pair. The high must lie inside a useful ray envelope; increase reach
only enough to catch it. Nearby parts can become wrong hits when reach increases. An explicit
cage requires matching receiver topology/face correspondence, not just a similar silhouette.
For a self-bake, Selected to Active is off: it is a different route.

Small automatic-cage example, with Object Mode, `sources` and `receiver` available in the
current view layer, a configured [image target](bake-image-target.md), Cycles, and a caller
chosen `reach`, `margin_px`, `pass_type` and `uv_name`:

```python
for obj in bpy.context.selected_objects:
    obj.select_set(False)
for obj in sources:
    obj.select_set(True)
receiver.select_set(True)
bpy.context.view_layer.objects.active = receiver
result = bpy.ops.object.bake(
    type=pass_type, target='IMAGE_TEXTURES', save_mode='INTERNAL',
    use_selected_to_active=True, use_cage=True, cage_object='',
    cage_extrusion=reach, max_ray_distance=0, uv_layer=uv_name,
    normal_space='TANGENT', normal_r='POS_X', normal_g='POS_Y', normal_b='POS_Z',
    use_clear=True, margin=margin_px, margin_type='EXTEND')
assert result == {'FINISHED'}
```

This intentionally sets the bake destination/projection rather than inheriting UI settings.
It changes selection and writes image pixels; it neither saves images nor certifies the cage.
Do not blindly unhide/select unrelated objects. `NORMAL` uses geometric normal transfer;
for a raw color/scalar field use [Emit routing](bake-field-transfer.md).

**First proof:** a tilted or gently curved high patch with known normal above a flat UV receiver.
Compare decoded `2*RGB-1` against the expected tangent-space direction, including green sign.
Try insufficient reach as a negative control, then restore the useful reach. Inspect actual
pixel content and log warnings; a miss can still return FINISHED. Check corners and seams
under grazing light on the receiver with the high hidden. Save maps and reopen the receiver.

Before a complex asset, test adjacent pieces and difficult concavities; isolate/explode bake
groups or use a suitable cage when necessary. The extracted test covers automatic extrusion
on simple patches, not a production custom cage or every exporter tangent convention.

[Bake API](https://docs.blender.org/api/5.1/bpy.ops.object.html#bpy.ops.object.bake) ·
[Projection concepts](https://docs.blender.org/manual/es/4.0/render/cycles/baking.html) ·
[Evidence](provenance.md#bake-and-uv-extraction-batch)
