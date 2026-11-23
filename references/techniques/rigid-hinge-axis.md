# Orient and verify a rigid-body hinge

Use for one shape-preserving hinged body. Two existing rigid bodies belong to the intended
Rigid Body World; rest transforms/scale and collision proxies are already checked. The empty
is owned, unparented and unconstrained; choose its pivot and world axis explicitly. Hinge
uses local **Z**; do not copy the X-axis convention of other constraint types.

```python
def configure_hinge(empty, body_a, body_b, pivot, axis, limits):
    import bpy
    from mathutils import Vector
    assert body_a.rigid_body and body_b.rigid_body
    axis=Vector(axis); assert axis.length > 1e-8 and limits[0] <= limits[1]
    empty.location=pivot
    empty.rotation_mode='QUATERNION'
    empty.rotation_quaternion=Vector((0,0,1)).rotation_difference(axis.normalized())
    if empty.rigid_body_constraint is None:
        with bpy.context.temp_override(object=empty, active_object=empty):
            assert bpy.ops.rigidbody.constraint_add() == {'FINISHED'}
    c=empty.rigid_body_constraint; c.type='HINGE'
    c.object1, c.object2 = body_a, body_b
    c.disable_collisions=True; c.enabled=True
    c.use_limit_ang_z=True
    c.limit_ang_z_lower, c.limit_ang_z_upper=limits
    return c
```

Limits are radians relative to the constraint's reference configuration, not arbitrary world
Euler angles. A measured B-relative-to-A angle may have the opposite sign from the constraint
limits; validate object order/sign with one asymmetric limit instead of comparing unsigned
quaternion angles or assuming a world Euler convention. Disabling mutual collisions suits
overlapping anchor/rod proxies, not every assembly. Verify constraint collection membership.
Change a baked system on an unbaked copy.

## Check

Store each body's local attachment point from the authored rest state. Across the solve,
compare its evaluated world location with the opposite attachment, transformed local axis
alignment, signed relative rotation and bounds. Translation alone can look plausible even
with the wrong axis. Compare disabled-hinge and rotated-axis controls on fresh solves.
Increase solver quality only after rest placement, frames, scale and contact are correct.
This is not a motor, multi-link stability recipe or rig IK constraint.

[Cached world replay](rigid-cache-replay.md),
[Hinge manual](https://docs.blender.org/manual/en/5.4/physics/rigid_body/constraints/types/hinge.html).
[Extraction evidence](provenance.md#state-and-motion-extraction-batch).
