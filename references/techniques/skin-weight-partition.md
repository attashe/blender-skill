# Separate bend weights, twist weights and rigid regions

Use for an interpretable tubular limb/sleeve study. Inputs: aligned rest skeleton and mesh,
three intended deform groups and longitudinal coordinates in a declared rest space. This
analytic profile is a starting mechanism, not anatomical auto-weighting for arbitrary shapes.
Choose transition spans from joint radius/topology and the supported poses, not copied numbers.

```python
def three_way_weights(coordinate, bend_span, twist_span):
    def smooth(span, x):
        a, b = span
        assert b > a
        t = min(1.0, max(0.0, (x-a)/(b-a)))
        return t*t*(3.0-2.0*t)
    bend = smooth(bend_span, coordinate)
    twist = smooth(twist_span, coordinate)
    return (1.0-bend, bend*(1.0-twist), bend*twist)

def replace_owned_weights(mesh_object, names, rows):
    rows = list(rows)
    assert len(names) == 3 and len(set(names)) == 3
    assert len(rows) == len(mesh_object.data.vertices)
    assert all(len(w) == 3 and min(w) >= 0 and abs(sum(w)-1) < 1e-6 for w in rows)
    groups = [mesh_object.vertex_groups.get(n) or mesh_object.vertex_groups.new(name=n) for n in names]
    ids = list(range(len(rows)))
    for group in groups:
        group.remove(ids)  # Clear old memberships, including now-zero influences.
    for index, weights in enumerate(rows):
        for group, weight in zip(groups, weights):
            if weight > 0:
                group.add([index], weight, 'REPLACE')
```

Call only for owned groups after checking their bone-name correspondence and excluding other
unintended deform groups/envelopes. Preserve unrelated mask groups. For an offset mesh, convert
mesh coordinates into the rig's rest space before deriving the longitudinal parameter.
Repeated assignment must clear weights that became zero; adding only new nonzero values can
leave old influences behind. Keep a rigid cuff/housing on one intended bone at weight 1.

**Check:** no unweighted vertices, expected deform influences, sum near 1, and actual bend,
reverse bend, twist and combined poses. Inspect inner compression separately from cross-section
area. For the rigid island compare pairwise distances/world placement. A normalized distribution
can still fold or intersect; compare a narrower/wider transition at matched poses before
claiming improvement. A wrong nondeform group name must fail the influence check.

[Skinning decisions](../deformation-workflow.md#skin-with-interpretable-influences) ·
[Armature modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/armature.html) ·
[Verification](provenance.md#rig-and-deformation-extraction-batch)
