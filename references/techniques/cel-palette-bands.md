# Separate the light signal from the cel palette

Use for an EEVEE material with controlled flat tone bands. Inputs: an owned, empty material
node tree, three scene-linear palette colors and two ordered scalar thresholds in (0, 1).
First prove the character's simple smooth silhouette and major color regions; bands cannot
repair busy forms. This is a material technique, not a complete character recipe.

```python
def cel_palette(material, colors, thresholds):
    assert len(colors) == 3 and 0 < thresholds[0] < thresholds[1] < 1
    tree = material.node_tree
    assert tree is not None and len(tree.nodes) == 0, 'Use an owned empty tree'
    diffuse = tree.nodes.new('ShaderNodeBsdfDiffuse')
    diffuse.inputs['Color'].default_value = (1, 1, 1, 1)
    signal = tree.nodes.new('ShaderNodeShaderToRGB')
    scalar = tree.nodes.new('ShaderNodeRGBToBW')
    palette = tree.nodes.new('ShaderNodeValToRGB')
    palette.color_ramp.interpolation = 'CONSTANT'
    palette.color_ramp.elements.remove(palette.color_ramp.elements[1])
    for position, color in zip((0, *thresholds), colors):
        element = palette.color_ramp.elements[0] if position == 0 else palette.color_ramp.elements.new(position)
        element.color = (*color[:3], 1)
    emission = tree.nodes.new('ShaderNodeEmission')
    output = tree.nodes.new('ShaderNodeOutputMaterial')
    for a, b in ((diffuse.outputs[0], signal.inputs[0]),
                 (signal.outputs['Color'], scalar.inputs[0]),
                 (scalar.outputs[0], palette.inputs['Fac']),
                 (palette.outputs['Color'], emission.inputs['Color']),
                 (emission.outputs[0], output.inputs['Surface'])):
        tree.links.new(a, b)
    return palette
```

Neutral diffuse drives the scalar; object pigment belongs in the downstream palette. Feeding
the palette into a lit BSDF would light it a second time. Thresholds depend on illumination:
use a controlled light first, then test the shot rig and occluders. Avoid noisy bump details
that fragment broad shadow shapes. Preserve color/view settings while comparing variants.

**Check:** three occupied palette regions away from antialiasing edges, changed boundaries
when thresholds or light direction change, and neighboring motion frames. Do not require
exactly three unique PNG colors: edge filtering and the view transform add intermediate values.
Test a one-color palette as a negative control for the region-count check. Save/reopen and
render a previously checked frame. Shader to RGB is EEVEE-specific and does not support the
conventional Cycles pass reconstruction above; use Combined for this tested path.

[Cel decisions and temporal checks](../cel-shading-workflow.md) ·
[Shader to RGB](https://docs.blender.org/manual/en/5.1/render/shader_nodes/color/shader_to_rgb.html) ·
[Authored verification and limits](provenance.md#light-and-image-extraction-batch)
