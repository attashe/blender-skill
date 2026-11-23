# Attach and release a rigid object without a space-switch jump

Use for a prop picked up by a hand/tool. Inputs: an owned unparented object with no active
constraints, an independent target Object, full transform channels, no shear and invertible
target transform. This bounded example does not implement bone owners/subtargets, partial
axes, stacked spaces or continuous influence blends. Preserve the editable source first.

```python
import bpy

def attach_object(owner, target):
    assert owner.parent is None and len(owner.constraints) == 0
    assert owner != target
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    target_world = target.evaluated_get(dg).matrix_world.copy()
    before = owner.evaluated_get(dg).matrix_world.copy()
    inverse = target_world.inverted()  # Reject a singular target, do not silently substitute.
    c = owner.constraints.new('CHILD_OF')
    c.target = target
    c.inverse_matrix = inverse
    c.influence = 1.0
    bpy.context.view_layer.update()
    return c, before

def release_object(owner, constraint):
    assert owner.parent is None and constraint.type == 'CHILD_OF'
    bpy.context.view_layer.update()
    world = owner.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.copy()
    constraint.influence = 0.0
    owner.matrix_world = world
    bpy.context.view_layer.update()
    return world
```

At attach, the new mapping is identity; subsequent target motion preserves the relative
offset. At release, first capture the current evaluated world transform, then turn off the
constraint and write that transform into the owner's channels. An influence toggle alone loses
the inherited pose. Key the switch and the matching base channels at the same event; for a
discrete handoff use constant influence keys and avoid interpolating the base offset across
the hold. Keep the pre-attach base transform keyed during the hold. Match at the actual release
time, not a previous frame if the carrier moves between them. The functions do not insert keys.

**Check:** same-time before/after world matrices at both switches, constant
`target_world.inverted() @ owner_world` during the hold, and stationary owner after release
while the target continues moving. Check neighboring times/subframes separately: natural
motion between frames is not a switch error. Wrong inverse/unmatched release must be detected.

[Spaces and constraints](../rigging-workflow.md#make-spaces-and-constraints-explicit) ·
[Child Of](https://docs.blender.org/manual/it/5.2/animation/constraints/relationship/child_of.html) ·
[Verification](provenance.md#rig-and-deformation-extraction-batch)
