# Resolve dependencies against their owning library

Use for a known image/cache/library in a saved native project. A linked image's // path is
relative to its library, not necessarily the open shot. The filename existing is only one
check: verify it is the intended resource and that the consuming datablock can read it.

```python
def owned_path(filepath, owner_library=None):
    import bpy
    from pathlib import Path
    return Path(bpy.path.abspath(filepath,library=owner_library)).resolve()

def image_payload(image):
    width,height=image.size[:]
    assert width>0 and height>0, (image.name,width,height)
    pixels=list(image.pixels[:min(64,width*height*4)])
    assert pixels, image.name
    return {'size':[width,height], 'sample':pixels,
            'packed':bool(image.packed_file), 'linked_packed':image.is_linked_packed}
```

For external pixels use `owned_path(image.filepath, image.library)`; for a cache use its
own library context. For nested libraries account for the library's parent owner. Compare
resolved paths with the package root or declared external dependencies. Avoid relinking by
basename alone. Use `image.reload()` only for an intentionally external image whose file
is available; then check decoded size/pixels and the actual material/render. The short sample
is a loading witness, not proof of the entire texture or correct color-space interpretation.

Negative controls: a shot-local decoy with the same basename, missing resource and a packed
flag with zero decoded dimensions. Generated images must be saved/packed intentionally;
unsaved buffers can differ from what an exporter or reopened file reads. UDIM, sequences,
video, fonts, custom OCIO and each solver cache require their corresponding resource checks;
this single-image snippet is not an exhaustive dependency crawler.

[Clean relocation](clean-project-relocation.md), [dependency guide](../project-handoff.md).
[Extraction evidence](provenance.md#delivery-extraction-batch).
