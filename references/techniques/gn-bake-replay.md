# Bake one owned GN state and prove replay

Use for a known Simulation Zone or Bake node on a saved, editable project. Simulation
Zones retain history; a Bake node can cache stateless geometry. Texture baking is separate.
The caller owns the object/modifier and chooses the specific entry from modifier.bakes.
Inspect this small interface in the actual runtime; do not guess bake IDs or enumerate
unrelated nodes. Tested API: Blender 5.2.1 LTS.

```python
def bake_one_gn(obj, modifier, bake, start, end):
    import bpy
    assert bpy.data.filepath and start <= end
    assert obj.modifiers.get(modifier.name) == modifier
    assert bake.bake_id in {b.bake_id for b in modifier.bakes}
    modifier.bake_target = 'PACKED'
    bake.bake_target = 'PACKED'
    bake.use_custom_simulation_frame_range = True
    bake.frame_start, bake.frame_end = start, end
    bake.bake_mode = 'ANIMATION'
    with bpy.context.temp_override(object=obj, active_object=obj):
        result = bpy.ops.object.geometry_node_bake_single(
            session_uid=obj.session_uid, modifier_name=modifier.name, bake_id=bake.bake_id)
    assert result == {'FINISHED'}, result
```

Save again **after** completion. A FINISHED return alone is not replay evidence. Capture
IDs/count/position/age before baking; reopen in a fresh process and seek end → early → middle
without sequential warm-up. Compare the same compact output, not merely the node settings.
Inspect a rendered sample separately when the deliverable includes appearance.

For an authorized rebake, delete only the owned bake via
`bpy.ops.object.geometry_node_bake_delete_single(session_uid=obj.session_uid,
modifier_name=modifier.name, bake_id=bake.bake_id)` inside the same active-object override,
then edit upstream controls, rebuild and save. Supplying session_uid does not remove the
operator's active-object poll requirement.
On a disposable copy, changing a control behind a preserved cache versus deleting/rebaking
it is a useful causal test. A cached output can legitimately hide the upstream edit.
The broad selected-object operator can include other modifiers; avoid it for a bounded edit.

Packed data trades convenience for file size; large disk caches need relocation/dependency
checks. Bake formats are version dependent. This card makes no cross-version or subframe
interpolation guarantee. [Baking manual](https://docs.staging.blender.org/manual/en/latest/modeling/geometry_nodes/baking.html).
[Extraction evidence](provenance.md#state-and-motion-extraction-batch).
