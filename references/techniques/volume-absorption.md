# Color a transmitting solid through its thickness

**Use:** transparent resin, colored glass or liquid whose tint strengthens with path length.
Inputs: a closed boundary, outward normals, intentional dimensions/transforms, transmitting
surface and interior absorption. An open sheet has no well-defined solid interior.

```text
White transmitting boundary / Principled → Material Output Surface
Volume Absorption (color, density)        → Material Output Volume
```

For an owned material tree with an existing Principled `boundary` and Material Output `out`:
the value assignments below assume unlinked inputs. If an existing group/texture drives one,
edit that upstream control instead; a linked input ignores its default value.

```python
boundary.inputs['Base Color'].default_value = (1, 1, 1, 1)
boundary.inputs['Transmission Weight'].default_value = 1
boundary.inputs['IOR'].default_value = ior
volume = tree.nodes.new('ShaderNodeVolumeAbsorption')
volume.inputs['Color'].default_value = absorption_color
volume.inputs['Density'].default_value = density
tree.links.new(boundary.outputs['BSDF'], out.inputs['Surface'])
tree.links.new(volume.outputs['Volume'], out.inputs['Volume'])
```

Color/density belong to the intended material and scale, not a fixed amber preset. Start with
a white boundary when isolating the effect; tinting both surface and volume compounds color.
Unit labels alone do not calibrate optical density. Verify the actual world thickness and
transforms, then tune density at that scale. A scaled-up copy can have a different optical path.

For editable scalar/color controls, use [real shader sockets](../api-diagnostics.md#shader-controls);
a declared group interface socket cannot be linked directly.

**First proof:** render two or more known thicknesses over a readable background. At fixed
camera/light, compare density 0 with a useful nonzero value. Increased path length should
produce the expected attenuation/tint; inspect channels as well as brightness. Reflections,
refraction and changed ray paths can prevent a simple global "thicker is darker" comparison.
Use central, unobstructed regions for the controlled check and inspect edges separately.

Keep enough transmission bounces for the nested boundaries; black regions may come from
geometry, overlap or transport limits. Absorption alone is not scattering, SSS, frosted surface
roughness or thin-film interference. Engine-specific transmission needs its own test; the
extracted evidence is Cycles. Save the material with both output branches and verify reopen.

[Composition choices](../material-composition.md) · [Evidence](provenance.md#material-response-extraction-batch) ·
[Volume Absorption](https://docs.blender.org/manual/en/2.91/render/shader_nodes/shader/volume_absorption.html)
