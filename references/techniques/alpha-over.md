# Composite with an explicit alpha convention

Use for an RGBA foreground over an image/plate. Inputs: compatible linear color spaces,
registered canvas/domain, and known foreground alpha convention. Blender compositor images
normally carry premultiplied RGB; `Straight Alpha` below describes the foreground arriving
at this node, not merely the original file before the loader's conversion.

```python
def alpha_over(tree, foreground, background, straight=False):
    n = tree.nodes.new('CompositorNodeAlphaOver')
    n.inputs['Factor'].default_value = 1.0
    n.inputs['Straight Alpha'].default_value = straight
    tree.links.new(foreground, n.inputs['Foreground'])
    tree.links.new(background, n.inputs['Background'])
    return n.outputs['Image']
```

For associated/premultiplied inputs, `Cout = Cf + (1-af)*Cb` and
`aout = af + (1-af)*ab`. A generic Mix using foreground alpha multiplies covered RGB again
and is not equivalent. Keep alpha separate from color grading. Nonlinear color operations
may require unpremultiply → grade → premultiply; a linear exposure multiply does not.

**Check:** a small analytical swatch with fractional coverage and an opaque background;
both a straight foreground and its premultiplied equivalent must produce the same expected
RGBA. Deliberately interpreting premultiplied data as straight must fail that comparison.
Also inspect real antialiased edges on light and dark backgrounds and preserve fractional
alpha when delivering a reusable element. An opaque final plate is a different contract.

[Alpha workflow](../compositing-workflow.md#treat-alpha-as-an-interface) ·
[Alpha Over inputs](https://docs.blender.org/manual/en/5.0/compositing/types/color/alpha_over.html) ·
[Authored verification and limits](provenance.md#light-and-image-extraction-batch)
