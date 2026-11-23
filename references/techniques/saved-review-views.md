# Reproducible review views

Use when a saved overview, plan or section reopens with the wrong camera, hidden geometry
or framing. Keep one scene for a single view when sufficient. For several structural
reviews with different visibility, separate named Scenes can persist each complete state.
This is a small view-state operation, not a building generator.

## State and ownership

The view contract includes camera, object/collection membership, enabled View Layers,
frame, output size/aspect, engine and display/lighting settings. `Scene.camera` selects the
camera. `ViewLayer.use` enables rendering of that layer; it does not select the current
viewport layer. A View Layer has no `camera` or `use_render` property in Blender 5.2.
For a query on the viewport depsgraph, select the intended scene/layer separately.

Do not implement a local cutaway by changing `Object.hide_render` on objects shared by
several scenes: that flag belongs to the object. Link an explicit subset into a review
scene, or use scene-specific layer exclusions. Keep the complete construction available.

Minimal static review, with existing objects and a dedicated camera supplied by the caller:

```python
review = bpy.data.scenes.new('Review_Overview')
contents = bpy.data.collections.new('Review_Contents')
review.collection.children.link(contents)
for obj in [*review_objects, review_camera]:
    contents.objects.link(obj)
review.camera = review_camera
review.render.engine = 'BLENDER_WORKBENCH'
review.render.resolution_x, review.render.resolution_y = 1200, 900
review.render.resolution_percentage = 100
review.render.image_settings.file_format = 'PNG'
review.render.filepath = output_png
```

`review_objects` is an explicit set, including dependencies that affect evaluation.
Linked objects retain their geometry, transforms, materials and object visibility flags;
they are not independent copies. This new scene does **not** inherit the source's World,
color management, compositor, simulation setup or render configuration. Set the required
state explicitly. For an existing beauty/animation setup, preserve its dependencies through
an appropriate scene copy or View Layer rather than treating this static example as a clone.
For Cycles/EEVEE, include the intended lights/World and engine settings.

Set the intended startup scene in an owned Blender session before saving:
`bpy.context.window.scene = review`. Render a named scene with
`bpy.ops.render.render(scene=review.name, write_still=True)`; this need not change the
window's active scene. Save after the final configuration, not after restoring different
temporary visibility or leaving the last section's resolution on the overview.

## A section must explain what was cut

A camera clip plane does not close a cut mesh. For a capped snapshot, copy the relevant
**evaluated** geometry, cut in a declared common space, fill the cut boundary and check
the resulting shell. Do not mistake the untouched base mesh for a modifier's result.
Distinguish cut faces from geometry seen beyond them; check that labels and dimensions fit
at delivery resolution. Preserve source geometry and mark snapshots with source identity
and cut plane. They must be regenerated after layout changes; linked overview objects update
with the model, but copied section meshes do not. Use a live sectional setup when needed.

## Verify the saved state

Reopen the actual output in a fresh process, select the named review scene and render,
changing only the destination path. Compare with the delivered image and inspect the pixels.
If reproducing it requires hiding walls, switching cameras or fixing resolution manually,
the saved contract is incomplete. For structural probes, use the complete construction
scene and verify an expected hit before interpreting misses from a cutaway.

Author-tested in Blender 5.2.1 on a repaired stair assembly: two different review scenes,
shared overview geometry, a capped section snapshot and pixel-identical fresh reopen renders.
The preceding Pi output failed view-state reproduction. Independent use of this card remains
unverified; this evidence does not validate an arbitrary production scene's dependencies.
