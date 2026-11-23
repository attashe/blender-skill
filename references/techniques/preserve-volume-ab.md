# Compare Preserve Volume on the same deformation

Use for twist collapse or volume loss after the skeleton and weights are correct. Inputs:
the same evaluated pose, geometry, weights and one intended Armature modifier. Read/bypass
an existing driver through its public control; a direct boolean assignment to a driven
modifier may be overwritten at evaluation.

```python
import bpy

def evaluated_vertices(mesh_object):
    bpy.context.view_layer.update()
    obj = mesh_object.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = obj.to_mesh()
    try:
        return [v.co.copy() for v in mesh.vertices]
    finally:
        obj.to_mesh_clear()
```

On an undriven working copy, set `modifier.use_deform_preserve_volume=False`, sample/render,
then True and sample/render at the same pose. Restore the intended delivery setting. This
uses quaternion skinning rather than ordinary linear blending; it may restore twist area
while producing bulges or leaving a bad inner fold. Do not treat the toggle as a skin repair.

**Check:** compare the suspect cross-section in its deformed plane (or use a 3D polygon area),
not a fixed world XY projection that shrinks merely because the limb tilted. Ensure stable
vertex correspondence; a downstream topology-changing modifier invalidates ring indices.
For pure twist of equal-radius sections, compare area ratios to rest. For bent/combined poses,
also inspect silhouette, compression and intersections; area near 100% is not sufficient.
Test neutral and a rigid one-bone region as controls. Reopen and evaluate a different pose order.

[Deformation diagnosis](../deformation-workflow.md#diagnose-bending-and-twisting-before-adding-corrections) ·
[Preserve Volume](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/armature.html) ·
[Verification](provenance.md#rig-and-deformation-extraction-batch)
