# Transfer a color or numeric field without illumination

**Use:** bake a mask, scalar response or base-color field when a supported native pass does
not directly express it. Decide channel meaning and encoding first. Roughness, metallic,
masks and normal data normally use Non-Color; base color uses the intended color encoding.
Combined lighting is not a base-color substitute. A BSDF closure is not a color field.

On a caller-owned temporary source-material copy, `field` is a real node output socket,
`tree` its shader tree and `out` its active Material Output with an existing Surface link:

```python
original_surface = out.inputs['Surface'].links[0].from_socket
emission = tree.nodes.new('ShaderNodeEmission')
emission.inputs['Strength'].default_value = 1
tree.links.new(field, emission.inputs['Color'])
tree.links.new(emission.outputs[0], out.inputs['Surface'])
```

Bake `EMIT` using the chosen self-bake or [projection](bake-projection.md) setup. In a `finally`
cleanup, reconnect `original_surface` to `out.inputs['Surface']` and remove only this temporary
emission node. Discard the temporary material copy or restore its assignment. Preserve the
source graph; do not reconnect a guessed Principled node when it originally used a mix.

**First proof:** transfer known interior patches, including one nonzero scalar, at low resolution.
Save the image with its role's interpretation, load a fresh image from that file, and compare
in a declared space. Test color and numeric data separately. An encoded byte value and a
linear shader value are not interchangeable; the tested generated float sRGB bake buffer
and loaded PNG pixel buffer differed in interpretation. Calibrate with known values rather
than applying gamma conversion to every buffer. View transforms belong to presentation,
not data-map export. A deliberately wrong sRGB interpretation should fail the scalar check.

Keep real normal baking distinct: a tangent normal image is Non-Color, decoded with a Normal
Map node using the intended UV set and consumer convention; do not send it straight into a
BSDF Normal input. Save/pack edited maps before the blend, rebuild the delivery material from
reloaded maps, hide the high source, then reopen and inspect. Disk persistence is a separate
check from a successful bake.

[Texture authoring](../texture-authoring-workflow.md) · [Full bake workflow](../baking-workflow.md) ·
[Evidence](provenance.md#bake-and-uv-extraction-batch)
