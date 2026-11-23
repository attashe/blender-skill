# Save a rigid-body solve and verify evaluated replay

Use for the selected scene's known Rigid Body World. This cache is owned by the **world**,
not a single body. Scope the scene accordingly. Set range/FPS/scale/solver settings first;
save an editable unbaked source before baking. Tested API: Blender 5.2.1 LTS.

```python
def bake_rigid_world(scene, start, end):
    import bpy
    assert scene.rigidbody_world and start <= end
    pc=scene.rigidbody_world.point_cache
    assert not pc.is_baked, 'Use the editable unbaked source for a new solve'
    scene.frame_set(start)
    pc.frame_start, pc.frame_end=start,end
    with bpy.context.temp_override(scene=scene, point_cache=pc):
        result=bpy.ops.ptcache.bake(bake=True)
    assert result == {'FINISHED'} and pc.is_baked
    return pc
```

Save the baked project, then reopen fresh and seek end → impact → start → neighboring frames.
Compare `obj.evaluated_get(depsgraph).matrix_world` against the saved baseline. Authored
location channels may still show the initial state while physics moves the body. Cache info
or an operator return alone does not prove persistence. Disk-backed cache needs its files.

Make a meaningful control change on the **unbaked source**, solve again and measure an
effect (pivot drift after disabling a hinge, travel after a friction change). Do not diagnose
an unchanged cached transform as a dead control. Include finite transforms, relevant contact
and actual images; deterministic replay is not proof of accurate physics.
For rolling, accumulated rotation×radius versus tangential travel is a useful contact check;
it is not needed for a hinge-only edit. Physics cache is distinct from baking transform keys
for export. Subframe playback and target-engine equivalence require their own checks.

[Rigid-body workflow](../rigid-body-workflow.md), [simulation](../simulation-workflow.md).
[Extraction evidence](provenance.md#state-and-motion-extraction-batch).
