# Export a declared object set to GLB

Use for a prepared mesh/PBR/object-animation delivery representation. Caller supplies the
exact objects, required parents and active scene frame range/FPS. Include dependencies
deliberately; this does not discover or bake rigs, GN, procedural shaders or simulation.
Work on a saved source/copy; these settings describe the tested 5.2.1 exporter, not every target.

```python
def export_glb(objects, filepath):
    import bpy
    assert bpy.context.mode == 'OBJECT' and objects
    assert abs(bpy.context.scene.render.fps_base-1.0)<1e-8, 'Normalize delivery timebase first; see measured exporter limit below'
    layer=bpy.context.view_layer
    assert all(o.name in layer.objects and not o.hide_get() for o in objects)
    previous=list(bpy.context.selected_objects); active=layer.objects.active
    try:
        for o in previous:o.select_set(False)
        for o in objects:o.select_set(True)
        layer.objects.active=objects[0]
        result=bpy.ops.export_scene.gltf(
            filepath=str(filepath),export_format='GLB',use_selection=True,
            export_yup=True,export_animations=True,export_animation_mode='SCENE',
            export_anim_scene_split_object=False,
            export_frame_range=True,export_frame_step=1,export_force_sampling=True,
            export_optimize_animation_size=False,export_gpu_instances=False,
            export_materials='EXPORT',export_image_format='AUTO',export_apply=False)
        assert result == {'FINISHED'}, result
    finally:
        for o in objects:o.select_set(False)
        for o in previous:o.select_set(True)
        layer.objects.active=active
```

For static delivery turn animation export off; for other clip policies inspect the actual
operator instead of exporting unrelated Actions. The split-object flag matters:
SCENE alone defaults to separate per-object clips in the tested exporter. For one assembly motion, request a merged clip and verify channels for
all moving members; a first-clip-only import can animate the root while freezing its hinge.
Explicit source preparation and export_apply=False keep modifier conversion out of this snippet. Verify actual output names,
including absence of a deliberately unrelated selected helper. Compare the source before/after.
Inspect clip duration in seconds, especially fps_base, and start/extreme/intermediate poses
after a clean import. Sampled integer-frame agreement does not promise arbitrary interpolation.

Measured 5.2.1 exporter/importer code uses fps*fps_base for glTF time where the scene's
effective rate is fps/fps_base. Thus a same-setting round trip can hide incorrect seconds.
For an integral effective rate, prepare a delivery copy at that rate with fps_base=1 (30/1.25
becomes 24/1), retain the frame range, and compare timed output. Do not change the authoring
source or assume this fixes nonintegral retiming, drivers or simulation. Other versions need
their own duration probe; the assertion bounds this tested profile.

Direct Principled/image PBR is a small supported case. Complex procedural/view-dependent
shaders require a chosen [format/material representation](../export-formats.md), not automatic
flattening. Continue with [payload audit](glb-payload-audit.md) and
[round-trip comparison](glb-surface-roundtrip.md). Blender reimport is a declared receiver;
it does not certify a game engine or browser.

[Exporter manual](https://docs.blender.org/manual/id/5.0/addons/import_export/scene_gltf2.html).
[Extraction evidence](provenance.md#delivery-extraction-batch).
