# Inspect GLB resources and delivery cost

Use for targeted checks of a known GLB 2.0 export. An embedded container is not by itself
proof that images/buffers are embedded. Inspect actual JSON/binary payload and recipient
material/image data. The small parser below is a local inspection aid, not a full validator.

```python
def glb_document(path):
    import json,struct
    from pathlib import Path
    data=Path(path).read_bytes()
    assert len(data)>=20
    magic,version,length=struct.unpack_from('<4sII',data)
    assert (magic,version,length)==(b'glTF',2,len(data))
    offset=12;document=None
    while offset<len(data):
        assert offset+8<=len(data)
        size,kind=struct.unpack_from('<II',data,offset);offset+=8
        assert size%4==0 and offset+size<=len(data)
        if kind==0x4E4F534A:document=json.loads(data[offset:offset+size])
        offset+=size
    assert document is not None
    return document,len(data)
```

Check intended names, mesh sharing, primitive attributes/indices, material factors, image
MIME/size and actual decoded pixels. For the self-contained profile, buffers/images must not
depend on external paths; embedded bufferViews or data URIs need their own content checks.
List extensionsRequired separately from extensionsUsed and confirm receiver support.
Trace the material's baseColorTexture/UV and PBR fields rather than counting texture files.
Inspect animation input accessor ranges for duration; accessor metadata is not a motion test.

Report file bytes, unique primitives/triangles, instantiated triangles and split GPU vertex
counts separately. For a measured image W×H, W·H·4 estimates only uncompressed RGBA8 base
level, not mips/compression/driver allocation. A smaller GLB is not proof of fewer draw calls
or better frame time. Use [performance](../performance-workflow.md) for real receiver budgets.
Copy the actual export to a new directory and test loading without source resources.
Use a Khronos validator when format conformance is required; do not label these targeted
checks as validator certification.

[Clean surface comparison](glb-surface-roundtrip.md).
[Extraction evidence](provenance.md#delivery-extraction-batch).
