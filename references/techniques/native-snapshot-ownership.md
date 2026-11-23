# Choose an independent or packed native snapshot

Use when a consumer should retain the chosen revision. Append owns a local editable copy;
Pack retains linked-data identity as a frozen snapshot where supported. Neither is a live
update route; use [linked overrides](linked-override-update.md) for that. Tested API: 5.2.1.

```python
def import_snapshot(filepath, collection_name, packed_link=False):
    import bpy
    with bpy.data.libraries.load(str(filepath),link=packed_link,
                                 pack=packed_link,relative=True) as (source,target):
        assert collection_name in source.collections
        target.collections=[collection_name]
    collection=target.collections[0]
    bpy.context.scene.collection.children.link(collection)
    bpy.context.view_layer.update()  # resolve the imported hierarchy before measuring it
    return collection
```

Call on a saved isolated consumer. For packed-linked delivery, pack supported external
resources at the editable **source owner** before importing its bundle. Resource packing,
linked datablock packing and saving are distinct. `is_linked_packed` alone can coexist
with an unavailable image; check dimensions and real pixels after reopening without source.
For Append, pack/copy the now-owned external resources according to the delivery contract.
Do not treat a packed-linked object as an editable local mesh or promise automatic updates.

## Measure the imported transform after scene evaluation

Appending a datablock does not by itself put it in the active scene. Before measuring world
bounds or baking coordinates into vertices, link the intended objects/collection and required
parents, update the view layer, and read the evaluated object in that graph. In the 5.2.1
composition trial, an unlinked translated sheet still reported an identity `matrix_world`;
using it displaced the curtain from its rail. This is an observed stale-state failure, not a
promise that every unlinked object returns identity. `matrix_basis` describes the stored
local transform before parents/constraints; it is not a general substitute for world space.

With `libraries.load`, keep requested names separate from returned datablocks, e.g.
`target.objects = list(requested_names)`. On leaving the context, the assigned sequence is
populated with Objects/None; aliasing the caller's list can turn later name lookups into type
errors. Validate returned entries, then use those references instead of rediscovering them
by names that may have acquired suffixes.

For a width variant, decide which dimensions change before scaling: cabinet panel span can
grow while stile thickness, bevel radius and metric texture features stay fixed. A rigid
placement and a shape edit are different operations. Review the host-space bounds and the
actual image after either.

[Object transform semantics](https://docs.blender.org/api/5.1/bpy.types.Object.html#bpy.types.Object.matrix_basis).
[Apartment integration checks](provenance.md#apartment-composition-integration).

Check a source geometry change propagates to live consumers but not either snapshot.
Verify appended data has no library owner, packed-linked data keeps the intended status,
and both load independently with correct textures. Asset marking/catalog UUIDs organize
discovery; they do not establish this ownership or dependency guarantee. Adding an asset
library to user preferences is unnecessary for this bounded import.

[Path and resource proof](owner-relative-resources.md), [handoff](../project-handoff.md).
[Extraction evidence](provenance.md#delivery-extraction-batch).
