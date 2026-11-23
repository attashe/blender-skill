# Make every receiving material write to the intended image

**Use:** a Cycles image bake writes nothing, only one material region, or an old image.
Contract: a receiver with the intended UV map, writable destination image(s), and one
explicit top-level Image Texture target in each receiving material used by the baked faces.
The Image Editor's displayed image is not the bake destination.

For caller-owned `targets = [(material, image_texture_node), ...]` and `image`:

```python
for material, node in targets:
    tree = material.node_tree
    assert node.type == 'TEX_IMAGE' and node.id_data == tree
    for other in tree.nodes:
        other.select = False
    node.image = image
    node.select = True
    tree.nodes.active = node
```

Reuse dedicated target nodes when changing maps; don't append another on every retry.
The target need not connect to the surface shader. Keep it out of the field/material being
sampled, otherwise the bake can read its own destination. Shared materials also share active
node state: make a derived setup when another object must keep a different destination.

Blender 5.0 changed baking to selected **and active** images. Merely assigning
`nodes.active` is insufficient in the tested 5.2 runtime; the
[release note](https://developer.blender.org/docs/release_notes/5.0/rendering/) confirms the change.
For an interactive edit, preserve/restore unrelated editor selection as appropriate.

**First proof:** bake a known nonzero field into two material regions at small resolution.
Sample both RGB regions, save/reload the map and check again. Deliberately deselect one target
to distinguish destination failure from projection. In the extracted fixture the skipped
region was black **and opaque**; alpha alone did not prove coverage. Legitimate black data
needs a different known diagnostic value. A FINISHED operator is not pixel evidence.

Clear a fresh image; for an atlas clear once, then accumulate disjoint regions deliberately,
including their dilation. Set interpretation by [field semantics](bake-field-transfer.md).
For source/receiver selection use [projection](bake-projection.md); for multiple tiles,
overlapping writers or nested materials continue with [baking](../baking-workflow.md).

[Evidence](provenance.md#bake-and-uv-extraction-batch)
