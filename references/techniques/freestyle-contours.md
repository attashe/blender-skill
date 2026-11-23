# Tune contours independently of cel tones

Use for a separate outline around a clean stylized silhouette. Inputs: a View Layer, an owned
Freestyle line set/style and an intended output resolution. Preserve existing line sets; the
example only configures the one supplied. A line set may select a specific character collection
so the floor and unrelated props do not acquire the same outline.

```python
def configure_contour(scene, line_set, width_px, color):
    assert width_px > 0
    assert line_set.linestyle is not None, 'Assign an owned LineStyle first'
    scene.render.use_freestyle = True
    scene.render.line_thickness_mode = 'ABSOLUTE'
    scene.render.line_thickness = 1.0
    line_set.select_silhouette = True
    line_set.select_border = True
    line_set.select_contour = True
    line_set.select_crease = False
    line_set.select_material_boundary = False
    line_set.linestyle.thickness = width_px
    line_set.linestyle.color = color
```

An empty startup may have a line set with no style. Assign a new `bpy.data.linestyles.new(name)`
to that set before calling the example; do not replace a supplied style just to initialize it.
Existing line-style thickness/color modifiers or drivers can override the intended result;
inspect only those relevant channels before configuring a supplied asset. For an independently
controlled copy, copy the style and deliberately remove/replace those channels on the copy.
The constant-width example assumes no such modifiers. Line selection and render engine/build
support also need a real render. Freestyle is not a portable material shader.

**Check:** render outline-off, thin and thicker variants at identical size and framing. The
line should aid silhouette/overlap reading without hiding eyes, fingers or color patches.
Inspect neighboring animation frames for popping and internal clutter. At another resolution,
choose whether to preserve pixel width or relative visual weight; `ABSOLUTE` alone does not
make a 2 px stroke look equally heavy in a small thumbnail and a large frame. An inverted hull
uses geometry/world thickness and has a different contract.

For soft character art, smooth restrained forms and large shadow regions remain the priority.
Disable unnecessary crease/material-boundary edges instead of compensating with more detail.
[Contour choices](../cel-shading-workflow.md) ·
[Freestyle render controls](https://docs.blender.org/manual/en/latest/render/freestyle/render.html) ·
[Authored verification and limits](provenance.md#light-and-image-extraction-batch)
