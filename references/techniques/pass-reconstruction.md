# Recombine conventional Cycles lobes

Use for a bounded pass edit or to diagnose missing/doubled contributions. Inputs: **raw**
linear passes from one Cycles render, selected View Layer and frame; Diffuse, Glossy,
Transmission Color/Direct/Indirect, Emission and Alpha. The example assumes Film Transparent,
no volume or special shadow-catcher path. Do not apply it to EEVEE Shader to RGB.

```python
def recombine_lobes(tree, source):
    def vector(operation, a, b):
        n = tree.nodes.new('ShaderNodeVectorMath')
        n.operation = operation
        tree.links.new(a, n.inputs[0])
        tree.links.new(b, n.inputs[1])
        return n.outputs['Vector']
    terms = []
    for lobe in ('Diffuse', 'Glossy', 'Transmission'):
        light = vector('ADD', source.outputs[lobe+' Direct'], source.outputs[lobe+' Indirect'])
        terms.append(vector('MULTIPLY', light, source.outputs[lobe+' Color']))
    terms.append(source.outputs['Emission'])
    total = terms[0]
    for term in terms[1:]:
        total = vector('ADD', total, term)
    alpha = tree.nodes.new('CompositorNodeSetAlpha')
    alpha.inputs['Type'].default_value = 'Replace Alpha'
    tree.links.new(total, alpha.inputs['Image'])
    tree.links.new(source.outputs['Alpha'], alpha.inputs['Alpha'])
    return alpha.outputs['Image']
```

Sum RGB contributions, then restore original alpha once. For transparent film, camera-visible
Environment is excluded; World illumination is already present in the lighting lobes. For an
opaque background or additional paths, derive the appropriate equation from the actual passes.
Do not add AO again or compare raw reconstruction against a denoised Combined.

**Check:** first reconstruct with no creative edit and compare with saved Combined at float
precision. Measure interior and fractional-alpha edges separately, with nonempty regions.
Remove a known nonzero term as a negative control: the comparison must detect the error.
Then reopen the EXR and comp in a fresh process and repeat. A graph with correctly named
nodes is insufficient if the source pass is black, absent or from a different layer.

Blender 5.x stores the comp in `scene.compositing_node_group`; its Group Output receives the
result. Existing source layer/socket names should be inspected, not guessed from this example.
[Pass guide](../compositing-passes-and-mattes.md) ·
[Official pass definitions](https://docs.blender.org/manual/en/latest/render/layers/passes.html) ·
[5.0 compositor migration](https://developer.blender.org/docs/release_notes/5.0/migration/compositor_migration/) ·
[Authored verification and limits](provenance.md#light-and-image-extraction-batch)
