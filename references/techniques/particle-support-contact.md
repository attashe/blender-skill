# Put the actual particle shape on its support plane

Use for settled instanced grains on a known stationary plane, with a fixed orientation
and scale at the evaluated instant. The collision point/nominal radius is not necessarily
the rendered lower surface. Inputs below are evaluated source-local vertices, instance
rotation×scale without translation, unit plane normal, and a point on the plane.

```python
def supported_center(vertices, linear, center, normal, plane_point):
    from mathutils import Vector
    n=Vector(normal).normalized(); c=Vector(center); q=Vector(plane_point)
    support=min(n.dot(linear @ Vector(v)) for v in vertices)
    return c + n * (n.dot(q)-n.dot(c)-support)
```

For the common horizontal plane, identity rotation and positive uniform scale s, the GN
equivalent is center.z = floor_z − s·Bounding Box(source).Min.z. Keep x/y. If orientation
or anisotropic scale changes, measure the transformed support; a local AABB rotated afterward
can overestimate the occupied shape and leave a gap. Realize a small diagnostic sample when
needed. Treat procedural displacement after placement as a separate surface dependency.

## Check

Measure min signed distance of **evaluated rendered vertices**, not just point centers.
Compare two sizes/orientations and a floor offset. A point clamped at z=radius should fail
for a source whose actual minimum is not -1. Verify settled flags and neighboring times.
The formula corrects geometric support; it does not solve dynamics, friction or interparticle
collision. In the source sparks, settled grains become unrotated/uniformly scaled; airborne
dashes keep an approximate one-bounce proxy. Do not advertise that as general shape collision.

[State/contact design](../particle-simulation-nodes.md#collisions-and-forces-are-explicit-parts-of-the-graph).
[Extraction evidence](provenance.md#state-and-motion-extraction-batch).
