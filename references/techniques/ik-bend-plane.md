# Keep a two-bone IK bend in its intended plane

Use for an elbow/knee or planar mechanism whose endpoint is right but intermediate joint is
wrong. Inputs: a two-bone chain, reachable target, deliberate rest bend/roll and stable pole.
Set chain_count=2 and disable intended stretching on the constraint and both pose bones.
Endpoint orientation is a separate control; this operation does not solve a wrist.

For a nonstraight reference pose, derive a pole position from its bend side. All points and
the distance below must use the **same** space. The example rejects singular geometry instead
of inventing a pole that can flip. For straight motion, retain a known pole/plane from the rig.

```python
from mathutils import Vector

def pole_from_bend(root, joint, tip, distance):
    root, joint, tip = map(Vector, (root, joint, tip))
    axis = tip - root
    if distance <= 0 or axis.length < 1e-8:
        raise ValueError('Positive pole distance and distinct root/tip required')
    projection = root + axis * ((joint-root).dot(axis) / axis.length_squared)
    side = joint - projection
    if side.length < axis.length * 1e-5:
        raise ValueError('Near-straight pose: use the established bend plane')
    return joint + side.normalized() * distance
```

Pole position does not determine a universal `pole_angle`: rest-bone roll participates in the
solve. Calibrate against a known joint pose/axis, then keep that convention while animating.
Do not replace this with an arbitrary copied angle or a dense scan on every frame. Inspect
one intermediate joint and its transverse axes when an otherwise correct endpoint twists.

**Check:** evaluated world tip-target distance, both segment lengths, signed bend side and
joint distance to the intended plane. Transform the plane with the asset root. Repeat at
several reachable targets and after translated/rotated/uniformly scaled root movement.
A deliberately wrong pole angle should fail the plane check even if its endpoint still passes.
Handle straight/folded/reach-limit configurations as boundaries, not ordinary passing cases.

[Rig/IK decisions](../rigging-workflow.md#solve-ik-and-match-ikfk-deliberately) ·
[IK manual](https://docs.blender.org/manual/nl/5.2/animation/constraints/tracking/ik_solver.html) ·
[Bone roll](https://docs.blender.org/manual/en/latest/animation/armatures/bones/editing/bone_roll.html) ·
[Verification](provenance.md#rig-and-deformation-extraction-batch)
