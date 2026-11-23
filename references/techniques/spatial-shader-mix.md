# Expose one surface through a spatial mask

**Use:** adjacent painted/bare, wet/dry or clean/dirty regions with genuinely different
surface responses. Define what mask 0 and 1 mean. For two colors of the same surface,
mix the colors before one BSDF; a second shader is not automatically needed.

```text
Mask 0..1 → Mix Shader factor
Coated/covered BSDF → first shader    (mask 0)
Exposed/base BSDF → second shader     (mask 1)
Mix Shader → Material Output Surface
```

Small wiring example inside a caller-owned shader tree; `mask`, `covered` and `exposed`
are output sockets. This creates one node and leaves the caller to choose the output branch:

```python
mix = tree.nodes.new('ShaderNodeMixShader')
tree.links.new(mask, mix.inputs[0])
tree.links.new(covered, mix.inputs[1])
tree.links.new(exposed, mix.inputs[2])
surface = mix.outputs[0]
```

**Layer meaning:** Mix Shader selects/blends responses in space; it does not make a physical
transparent film above another surface. For clear varnish over a base, Principled Coat can
provide that layered response. In a chipped painted metal, coat can belong to the surviving
paint branch while the exposed metal has its own roughness and micro-normal. Adding two
full-strength BSDFs is a different energy model, not a shortcut for this mask.

For editable scalar/color controls, use [real shader sockets](../api-diagnostics.md#shader-controls);
a declared group interface socket cannot be linked directly.
For a silent control, [inspect its target input and upstream operands](../api-diagnostics.md#inspect-one-node-or-upstream-branch)
before writing a material-wide inspector.

**First proof:** hold geometry, light, exposure and camera fixed. Inspect mask 0, a mixed spatial
mask and mask 1. Temporarily show the mask with emission to verify its scale and distribution,
then restore the surface path. Both endpoints must visibly reach the output. A control can be linked but have no effect
when an intermediate multiply is zero or a clamp saturates; test its actual output change. A noise threshold
named "exposure" is not a calibrated area percentage; evaluate the mask to measure coverage.

Choose mask coordinates and scale for the asset; use a painted/baked mask or structured wear
rule when references require edge/contact history. Generic noise verifies mixing, not natural
damage. Normal, roughness and color can have different frequencies. Follow
[material composition](../material-composition.md) for combined effects and
[surface families](../surface-families.md) for response choices.

[Evidence](provenance.md#material-response-extraction-batch) ·
[Mix Shader semantics](https://docs.blender.org/manual/en/5.0/render/shader_nodes/shader/mix.html)
