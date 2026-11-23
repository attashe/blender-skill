# Separate linear output from display exposure

Use when EXR/PNG exports disagree or a brightness control is ambiguous. Inputs: a completed
render, explicit working color space and output paths. This small Blender 5.2 example exports
the **same Render Result** twice, then restores the scene's format settings. It does not render,
change view settings or convert a plate. Scene output color management must already be correct.

```python
from pathlib import Path
import bpy

def save_linear_and_display(scene, stem):
    stem = Path(stem)
    fmt = scene.render.image_settings
    fields = ('media_type', 'file_format', 'color_mode', 'color_depth', 'exr_codec')
    previous = {key: getattr(fmt, key) for key in fields}
    try:
        fmt.media_type = 'IMAGE'
        fmt.file_format = 'OPEN_EXR'
        fmt.color_mode = 'RGBA'
        fmt.color_depth = '32'
        fmt.exr_codec = 'ZIP'
        bpy.data.images['Render Result'].save_render(str(stem.with_suffix('.exr')), scene=scene)
        fmt.file_format = 'PNG'
        fmt.color_mode = 'RGBA'
        fmt.color_depth = '16'
        bpy.data.images['Render Result'].save_render(str(stem.with_suffix('.png')), scene=scene)
    finally:
        for key in fields:
            setattr(fmt, key, previous[key])
```

**Discriminating check:** save A; increase `scene.view_settings.exposure` by a known stop
amount, save B from the same render, then restore it. Reopened scene-linear EXR should stay
unchanged while view-transformed PNG changes. Increasing a light's `data.exposure` instead
requires a new render and changes its linear contribution by `2**stops`. Test that ratio on
an unclamped, unsaturated, fixed-seed scene illuminated only by that light. In a mixed rig,
total beauty need not scale uniformly. Cycles Film Exposure is another render-data control.

Read saved linear pixels for energy comparisons; displayed PNG brightness is not a linear
energy meter. Inspect dark and bright regions visually too. Restore settings before saving
the deliverable. This example exports a beauty RGBA, **not** a multilayer pass archive or
Cryptomatte metadata. For those, preserve and verify the required layers separately.
In Blender 5.2, select `media_type='MULTI_LAYER_IMAGE'` before choosing
`file_format='OPEN_EXR_MULTILAYER'`; the available format enum depends on that category.

[Render/output guide](../render-workflow.md) ·
[Color management](https://developer.blender.org/docs/release_notes/5.0/color_management/) ·
[Authored verification and limits](provenance.md#light-and-image-extraction-batch)
