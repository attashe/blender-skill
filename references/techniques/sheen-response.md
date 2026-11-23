# Add a grazing fiber response with sheen

**Use:** a soft fiber/dust response where silhouette geometry does not need individual hairs.
Start from the required base BSDF, surface curvature and lighting. Sheen adds a reflection
layer; it does not create fabric weave, fuzz silhouettes or groomed fibers. For backlit
curtains and weave openings, use [thin-sheet scattering and coverage](sheer-fabric.md).

For an existing caller-owned Principled node with unlinked sheen inputs:

```python
surface.inputs['Sheen Weight'].default_value = weight
surface.inputs['Sheen Roughness'].default_value = roughness
surface.inputs['Sheen Tint'].default_value = tint
```

Choose these values for the reference and view, not a universal cloth preset. Keep base
roughness/specular distinct from sheen roughness/tint. Do not connect emission to imitate
grazing reflection: emission removes the dependence on incident light.
For linked inputs, trace and edit the group/texture control that drives the socket; assigning
its default value does not replace the incoming field.

For editable scalar/color controls, use [real shader sockets](../api-diagnostics.md#shader-controls);
a declared group interface socket cannot be linked directly.

**First proof:** compare weight 0 and a nonzero value with identical light, camera, exposure
and geometry. Curved or folded geometry supplies both face-on and grazing regions. Inspect
the changed response near grazing angles and under useful light; a socket value alone is
not proof. A conspicuous diagnostic tint may reveal the layer, then return to the intended
color. Preserve that base look while tuning the layer.

Add textile microstructure only when visible at the requested image scale, with physical
frequency/amplitude and sufficient sampling. This extraction does not certify the source
asset's weak weave detail as a production fabric recipe. If close-up silhouette fibers matter,
continue with [grooming](../grooming-workflow.md); for material families use
[surface families](../surface-families.md). Reopen the saved material and repeat a meaningful view.

[Evidence](provenance.md#material-response-extraction-batch) ·
[Principled layers](https://docs.blender.org/manual/en/4.0/render/shader_nodes/shader/principled.html)
