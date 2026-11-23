# Isolate a light's role

Use when a key, fill or separation light has an unclear contribution, or a highlight/shadow
needs a different source size. Inputs: an existing framed subject, named lights and a fixed
camera/material/view transform. Choose roles from the image; three lights are not mandatory.

Aim a new unparented Area at the relevant surface; its emitting direction is local −Z.
Then compare key-only with the intended rig. The temporary isolation below restores visibility,
including after an error. It does not suppress emissive geometry or World illumination.

```python
from contextlib import contextmanager
from mathutils import Vector

def aim_area(light, target):
    assert light.type == 'LIGHT' and light.data.type == 'AREA'
    assert light.parent is None, 'Resolve parent/world transform before using this example'
    direction = Vector(target) - light.location
    assert direction.length > 1e-8
    light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

@contextmanager
def isolated_lights(scene, enabled):
    states = [(o, o.hide_render) for o in scene.objects if o.type == 'LIGHT']
    try:
        for o, old in states:
            o.hide_render = o not in enabled
        yield
    finally:
        for o, old in states:
            o.hide_render = old
```

Within `with isolated_lights(scene, [key]):`, render one diagnostic. Render the restored rig
at identical settings. Judge what the extra source reveals, whether it flattens the intended
shadow, and whether it creates an unjustified highlight. Inspect actual saved images.
For source size, vary only `light.data.size` first; record `normalize` and energy/exposure.
Normalization does not promise unchanged brightness at the receiving surface. A bigger
nearby emitter changes angular distribution as well as softness. Independently edited lights
need independent data; a shared Light datablock changes all its users.

**Check:** a measurable contribution in the intended region plus a visible useful role;
unchanged camera/material/view, restored visibility, saved/reopened baseline. A successful
rotation assignment alone does not prove that the light reaches the subject.

[Broader lighting choices](../lighting-workflow.md) ·
[Light exposure/normalization](https://docs.blender.org/api/5.2/bpy.types.Light.html) ·
[Authored verification and limits](provenance.md#light-and-image-extraction-batch)
