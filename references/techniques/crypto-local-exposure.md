# Use a saved Cryptomatte for local exposure

Use for a modest linear grade of one object in a saved render. Inputs: a persisted multilayer
EXR containing Cryptomatte channels **and metadata**, selected Image node layer, the exact
CryptoObject layer name and object ID/name from that render. Renaming the scene object later
does not rename an ID in the saved EXR. This example operates on premultiplied beauty.
When saving a copy elsewhere, use the [relative-path check](../existing-file-workflow.md#relative-image-paths-on-save)
so the new comp still resolves the intended EXR.

```python
def crypto_exposure(tree, source, crypto_layer, object_name, stops):
    matte = tree.nodes.new('CompositorNodeCryptomatteV2')
    matte.source = 'IMAGE'
    matte.image = source.image
    matte.layer_name = crypto_layer
    matte.matte_id = object_name
    factor = tree.nodes.new('ShaderNodeMath')
    factor.operation = 'DIVIDE'
    factor.use_clamp = True
    tree.links.new(matte.outputs['Matte'], factor.inputs[0])
    tree.links.new(source.outputs['Alpha'], factor.inputs[1])
    grade = tree.nodes.new('CompositorNodeExposure')
    grade.inputs['Exposure'].default_value = stops
    tree.links.new(source.outputs['Combined'], grade.inputs['Image'])
    mix = tree.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    a = next(s for s in mix.inputs if s.identifier == 'A_Color')
    b = next(s for s in mix.inputs if s.identifier == 'B_Color')
    tree.links.new(factor.outputs[0], mix.inputs[0])
    tree.links.new(source.outputs['Combined'], a)
    tree.links.new(grade.outputs['Image'], b)
    return next(s for s in mix.outputs if s.identifier == 'Result_Color'), matte
```

The derived factor `clamp(matte/alpha, 0, 1)` avoids applying coverage twice at a selected
object's open silhouette. Blender Math Divide returns zero at a zero denominator. Only this
derived mix factor is clamped; preserve HDR beauty and encoded IDs. On pixels containing
multiple objects, this is a coverage-weighted **approximation**, not isolated object beauty,
relighting, deep compositing or exact recoloring behind refraction.

**Check:** nonempty selected and protected interiors, a nonempty fractional silhouette;
interior RGB changes by `2**stops`, protected RGB and alpha remain unchanged. Zero stops is
identity; an absent ID gives an empty matte. Compare the edge against the desired grade and
against the deliberately wrong raw-matte factor. Reopen using the saved EXR, not Render Result.
For arbitrary names/IDs, use the node's picker/manifest instead of inventing an escaped list.

[Passes/mattes limits](../compositing-passes-and-mattes.md) ·
[Cryptomatte file input](https://docs.blender.org/manual/en/4.2/compositing/types/mask/cryptomatte.html) ·
[Authored verification and limits](provenance.md#light-and-image-extraction-batch)
