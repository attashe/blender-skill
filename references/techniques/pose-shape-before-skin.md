# Drive a rest-space shape before Armature deformation

Use for a designed pose-dependent shape with stable vertex correspondence. Inputs: an owned
relative key whose reference is known, a suitable bone-local Euler channel and a positive
activation angle in radians. Author its delta in the mesh's base/reference space. A sculpt of
already deformed coordinates needs inverse deformation; copying it into the key can bend twice.

```python
import bpy

def drive_shape_from_bend(key, rig, bone_name, activation_radians):
    assert activation_radians > 0 and bone_name in rig.pose.bones
    path = key.path_from_id('value')
    ad = key.id_data.animation_data
    assert not ad or (not ad.action and not ad.nla_tracks and
                     not any(fc.data_path == path for fc in ad.drivers))
    curve = key.driver_add('value')
    driver = curve.driver
    variable = driver.variables.new()
    variable.name = 'bend'
    variable.type = 'TRANSFORMS'
    target = variable.targets[0]
    target.id = rig
    target.bone_target = bone_name
    target.transform_type = 'ROT_Z'
    target.transform_space = 'LOCAL_SPACE'
    target.rotation_mode = 'XYZ'
    driver.expression = f'min(max(bend/{activation_radians!r},0),1)'
    return curve
```

This bounded example reads positive local Z bending with XYZ decomposition. Select a meaningful
axis/rotation representation for the actual rig; wrapped Euler components are not generic
swing/twist measures. Keep the activation range away from wrapping and check negative bends.
The example rejects existing animation ownership instead of replacing it. For a simple
explicit-property driver, reuse [driven blink](driven-blink.md), rather than building another
driver framework.

**Check:** key weight zero/full/intermediate, neutral/negative bend, and matched key off/on
at the target pose. With ordinary linear skinning, a small analytic fixture can compare
`skin(base + value * delta)` against the evaluated mesh and reject `skin(base) + value * delta`.
Then inspect the actual asset: a measurable displacement proves data flow, not an improved
anatomical joint. Test neighboring poses/combinations before calling a designed shape corrective.

[Shape spaces](../deformation-workflow.md#author-shape-keys-and-corrections-in-the-right-space) ·
[Shape-key workflow](https://docs.blender.org/manual/en/5.2/animation/shape_keys/workflow.html) ·
[Driver target API](https://docs.blender.org/api/5.0/bpy.types.DriverTarget.html) ·
[Verification](provenance.md#rig-and-deformation-extraction-batch)
