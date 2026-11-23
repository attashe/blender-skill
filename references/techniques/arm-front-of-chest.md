# Fit an elbow and check a forearm across the chest

In the **rest mesh**, locate the shoulder socket, elbow hinge and narrow wrist in front **and** side orthographic views. Trace the upper-arm and forearm centerlines through successive cross-sections. Where the lines meet, pick a ring around the elbow and use its center. For evenly spaced world-space ring points, this is `sum(ring, Vector()) / len(ring)` from `mathutils`. A silhouette corner can sit a whole radius away from the hinge. In armature space, fit the upper-arm head, forearm head and hand head to these three centers. Check their world-space distances to the mesh landmarks after leaving Edit Mode.

Choose two disjoint sets of rest **face indices** on the mesh, one covering the full sleeve/forearm from elbow through wrist, the other the trunk front, sides and back across the heights swept by the arm. On a straight forearm, project face centers onto the elbow–wrist line and collect faces along that interval within the sleeve's measured radius, including the end loops. Alternatively use Edit Mode selections. Check the sets in rest, where they should be separate. They must identify the same faces after deformation. Include the hand when it also needs clearance.

The snippet reads `mesh`, `rig`, `forearm_faces`, `torso_faces` and the character's world-space forward vector `forward`. It measures the saved pose on the stock left arm.

```python
from math import degrees
from mathutils.bvhtree import BVHTree
dg = bpy.context.evaluated_depsgraph_get()
r, obj = rig.evaluated_get(dg), mesh.evaluated_get(dg)
names = ["ORG-upper_arm.L", "ORG-forearm.L", "ORG-hand.L"]
pose = [r.matrix_world @ r.pose.bones[n].head for n in names]
rest = [r.matrix_world @ r.data.bones[n].head_local for n in names]
u, v = pose[1]-pose[0], pose[2]-pose[1]
print("bend degrees", degrees(u.angle(v)), "length ratios",
      u.length/(rest[1]-rest[0]).length, v.length/(rest[2]-rest[1]).length)

m = obj.data
m.calc_loop_triangles()
xyz = [obj.matrix_world @ vert.co for vert in m.vertices]
def region(ids):
    tris = [tuple(t.vertices) for t in m.loop_triangles if t.polygon_index in ids]
    assert tris, "No triangles in the selected region"
    return BVHTree.FromPolygons(xyz, tris, all_triangles=True), {i for tri in tris for i in tri}
arm, ids = region(forearm_faces)
chest, _ = region(torso_faces)
f = forward.normalized()
depth = [p.dot(f) for p in xyz]
span = 1.01 * (max(depth) - min(depth))
gaps = []
for i in ids:
    p = xyz[i]
    hit = chest.ray_cast(p + f*span, -f, 2*span)[0]
    if hit is not None:
        gaps.append((p-hit).dot(f))
print("triangle crossings", len(arm.overlap(chest)), "projected vertices", len(gaps),
      "minimum front clearance", min(gaps, default=None))
```

A straight arm measures 0° and a right angle 90°. For an unstretched limb both length ratios should stay near 1. Clearance is measured along the forward axis. A negative value puts that sample behind the visible chest surface. An empty projection gives no depth evidence. Check wrist height against the intended chest landmark as well. If the wrist reaches its target but the forearm crosses the trunk, guide the elbow outward with the rig's bend-plane control or move the wrist target forward, update, and recheck the full surface from both views. [IK bend plane](ik-bend-plane.md)
