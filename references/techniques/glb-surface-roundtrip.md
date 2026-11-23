# Compare exported surfaces across vertex splits

Use after importing this run's GLB into a fresh receiving scene/process with the agreed
FPS and units. Compare evaluated world geometry at matching times, hierarchy/pivots and
required shared mesh identities. UV seams/flat normals can split exported vertices; raw
vertex count and order are not stable identity tests.

```python
def world_vertices(obj):
    import bpy
    bpy.context.view_layer.update()
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh()
    try:return [tuple(evaluated.matrix_world @ v.co) for v in mesh.vertices]
    finally:evaluated.to_mesh_clear()

def point_set_error(a,b):
    from mathutils import Vector
    assert a and b
    a,b=[Vector(v) for v in a],[Vector(v) for v in b]
    return max(max(min((v-w).length for w in b) for v in a),
               max(min((v-w).length for w in a) for v in b))
```

This bounded small-fixture comparison accepts duplicated vertices. For large meshes use
a spatial index or sampled surface distances. **Matching point sets do not prove topology,
normals or UVs.** Also compare triangle/surface extent and required corner attributes at
corresponding world positions, allowing splits. Use a normal matrix for transformed normals;
test mirrored/nonuniform transforms and winding deliberately.

Render matched views/light/color settings using an asymmetric texture witness. Perturb a UV
or reverse a face in a disposable copy: geometry may still pass while attributes/image fail.
Change a dimension or pivot to prove the spatial check catches a real error. Sample motion
start/end, extrema and in-between times; record tolerances in scene units. Pixel equivalence
under one light does not prove all materials, skin/morph, tangents or another renderer.
Keep source, derived GLB and imported verification scene distinct.

[Payload and material resources](glb-payload-audit.md), [broader export](../export-workflow.md).
[Extraction evidence](provenance.md#delivery-extraction-batch).
