# Match an evaluated IK chain into FK before switching

Use for a discrete IK → FK handoff in a known rig. Inputs: the same armature Object, matching
rest matrices/hierarchies and a parent-first list of source/destination pose-bone names. The
destination controls have no active constraints/drivers/locked transform channels or unusual
inheritance. Do not overwrite existing animation blindly; work at an intended keyed switch.

```python
import bpy

def match_ik_to_fk(rig, pairs):
    pairs = list(pairs)
    assert pairs and rig.type == 'ARMATURE'
    bpy.context.view_layer.update()
    evaluated = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
    snapshot = [(destination, evaluated.pose.bones[source].matrix.copy())
                for source, destination in pairs]
    for destination, matrix in snapshot:
        rig.pose.bones[destination].matrix = matrix
        rig.update_tag()
        bpy.context.view_layer.update()
```

`PoseBone.matrix` is in armature object space, not world space. Snapshot outgoing evaluated
matrices before changing anything, assign incoming controls root-to-tip, then change the rig's
switch and key its supported channels. The function deliberately does not guess the switch
property. For different rigs/rest axes, use a proper rest-space conversion or existing matcher.

**Check:** compare every relevant deform bone's evaluated world matrix and visible rigid/skin
geometry before/after the switch. Test a changed target with the armature moved away from the
origin. An unmatched switch should fail the same check. Verify reset and save/reopen.

This is not FK → IK matching or certification of a continuous blend. The reverse operation
must place the target **and** pole, and match wrist orientation/stretch/roll offsets supported
by that particular rig. Prefer its matching operator when available.

[IK/FK decisions](../rigging-workflow.md#solve-ik-and-match-ikfk-deliberately) ·
[PoseBone matrix API](https://docs.blender.org/api/5.0/bpy.types.PoseBone.html) ·
[Verification](provenance.md#rig-and-deformation-extraction-batch)
