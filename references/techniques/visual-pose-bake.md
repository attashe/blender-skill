# Bake the evaluated pose, then compare between samples

Use to deliver a constrained bone result as keys. Inputs: a saved source, an independent
delivery copy, named output bones, range/rate and an explicit error tolerance. Decide which
channels the recipient needs. Ordinary transform baking does not capture shape keys, every
B-Bone behavior, simulations or arbitrary modifier output.

The native Blender 5.2 example operates on the caller-selected pose bones of the active rig.
It clears constraints on those baked bones and creates a new Action; it is therefore for the
delivery copy. Set selection through `PoseBone.select` in this runtime, not an assumed Bone API.

```python
import bpy
from bpy_extras import anim_utils

def bake_selected_pose(rig, start, end):
    assert bpy.context.object == rig and rig.mode == 'POSE'
    assert any(pb.select for pb in rig.pose.bones)
    result = bpy.ops.nla.bake(
        frame_start=start, frame_end=end, step=1, only_selected=True,
        visual_keying=True, clear_constraints=True, clear_parents=False,
        use_current_action=False, clean_curves=False, bake_types={'POSE'},
        channel_types={'LOCATION', 'ROTATION', 'SCALE'})
    assert result == {'FINISHED'}
    ad = rig.animation_data
    bag = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    assert bag is not None and len(bag.fcurves) > 0
    return bag
```

Record evaluated source world matrices/mesh samples **before** baking, on both keyed and
intermediate times. Bake all relevant animated ancestors too, or retain their supported motion;
replacing an Action with selected-bone keys can otherwise drop unrelated parent channels.
`clear_parents=False` retains hierarchy but does not bake an animated armature Object. Preserve
its motion explicitly when needed. Drivers or NLA may still override the baked keys: mute/remove
only superseded dependencies in the copy and prove that moving an old control no longer changes
the delivered result. Action/slot existence alone is not that proof.

**Check:** separate max errors on sampled frames and subframes, in common world units, and
compare the actual surface/contact. A step-1 bake can pass integers and fail halfway between.
If the target needs tighter interpolation, use supported denser sampling/retiming or revise
curves; a custom evaluated-matrix sampler is a different route, not native subframe Bake Action.
Repeat nonsequential evaluation after reopen. Keep the source and report any unmet tolerance.

[Rig delivery](../rigging-workflow.md#validate-and-deliver-the-intended-rig) ·
[Bake operator](https://docs.blender.org/api/5.0/bpy.ops.nla.html) ·
[Verification](provenance.md#rig-and-deformation-extraction-batch)
