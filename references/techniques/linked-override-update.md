# Update a linked collection while retaining shot edits

Use when consumers should follow source revisions and retain supported local transforms or
animation. Source internals share a coherent collection root and stable identity. A local
editable copy that must stay independent belongs to [snapshot ownership](native-snapshot-ownership.md).
This example loads one known collection into a saved scene; it is not a whole library importer.

```python
def link_override_collection(filepath, collection_name):
    import bpy
    scene=bpy.context.scene
    assert bpy.data.filepath, 'Save the consumer before making relative library paths'
    with bpy.data.libraries.load(str(filepath),link=True,relative=True) as (source,target):
        assert collection_name in source.collections
        target.collections=[collection_name]
    reference=target.collections[0]
    scene.collection.children.link(reference)
    override=reference.override_hierarchy_create(
        scene,bpy.context.view_layer,do_fully_editable=True)
    if override.name not in scene.collection.children:scene.collection.children.link(override)
    if reference.name in scene.collection.children:scene.collection.children.unlink(reference)
    return override
```

Find local members by `obj.override_library.reference`, not a guessed .001 suffix. Edit the
intended local root/control, save, then change the owned source in a separate process/copy.
Reopen two consumers with different local transforms/animation. Verify updated geometry and
an added hierarchy member **and** preserved local channels at several times. Record revision
and resolved library identity. Avoid recreating all source datablocks just to change a size.

Automatic hierarchy resync on open can differ from a superficial library reload. Compare
warnings and local edits before accepting it. Resync Enforce can discard pointer overrides;
it is not a default refresh command. This small prop test does not certify nested character
rigs, pointer edits or every overridable property. UI Asset Browser discovery is separate.

[Library overrides](https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html),
[native packaging](clean-project-relocation.md).
[Extraction evidence](provenance.md#delivery-extraction-batch).
