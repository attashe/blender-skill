# Prove the constructed shell before repeating it

**Use:** a new mesh helper, suspected reversed faces, a failed Boolean operand or a solid
part that shades plausibly despite bad topology. Begin with one representative source part
and its evaluated result. Prefer a built-in primitive or checked source over a new face list
when it supplies the needed construction; still measure the requested dimensions.

**Small read-only implementation:** [mesh_probe.py](../../scripts/mesh_probe.py),
`inspect_mesh(object, evaluated=True, epsilon=1e-6)`. Import inside Blender; it neither
repairs nor selects anything. `epsilon` is a length tolerance in the mesh's local units.
The default sample limit is 100,000 evaluated faces; choose a small target before evaluation.
For a saved file, use the CLI (substitute and quote real paths):

```text
blender --background --factory-startup --disable-autoexec INPUT.blend --python-exit-code 1 --python SKILL/scripts/mesh_probe.py -- --expect-file INPUT.blend --object PANEL --output-json OUTPUT/probe.json
```

Repeat `--object` for another named part; `--source` inspects base geometry. The optional
`--scene` asserts the active scene; it does not switch scenes. A completed probe is a report,
not a PASS. It uses the current frame/viewport depsgraph; render-only modifier differences
need a separate check. Importing the helper lets the caller deliberately choose scene/frame.

| Observation | Next discriminating action |
| --- | --- |
| Closed coherent component, negative local volume | For an ordinary exterior solid, inspect face orientation and repair the source winding; then retest the same sample. Nested cavity boundaries can intentionally point inward. |
| Inconsistent shared-edge winding | Inspect the reported component before recalculating. A positive total volume cannot establish coherent face directions. |
| Boundary, non-manifold or degenerate geometry | Decide whether this is an intentional sheet/profile or a damaged solid. Repair the construction when a solid is required; normals alone cannot close a hole or give a flat cylinder thickness. |
| Positive and negative disconnected components | Inspect them separately. A large positive component can conceal a smaller inverted part in an aggregate-volume test. |
| Negative transform determinant | Distinguish reflected object transform from source face winding. Inspect the evaluated/exported representation before applying or flipping anything. |
| Dimensions differ from the requested sample | Correct primitive size/scale or helper coordinates before repeating it. Bounds do not prove physical wall thickness. |

For an owned, intended simple shell, Blender's Recalculate Outside or
`bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))` can repair coherent direction.
Choose the affected geometry explicitly and verify afterward. Preserve intended sheet sides,
cavity interfaces and source ownership. Do not append a blind scene-wide flip/recalculate
to every generator; a malformed construction can remain malformed afterward.

For a freshly constructed BMesh, cached face normals can still be zero. Before a
normal-dependent operation such as `bmesh.ops.solidify`, update them with
`bm.normal_update()` after creating/editing the source faces. A nonzero thickness argument
with zero normals can produce coincident front/back faces and degenerate sides while every
edge still has two linked faces. Recalculate Outside on that collapsed result cannot restore
thickness: rebuild from the valid source, then measure the resulting separation and check
degenerate faces. This mechanism was reproduced on vertical and inclined sheets in 5.2.1;
the bundled probe detects the degeneration without treating edge closure as a pass.

**First proof:** check expected dimensions, component topology/direction, and a useful
exterior/interior view. For a cut, compare one ray/section through the intended opening with
one through retained solid; include obstructing assembly parts. A successful Boolean or a
hole in the countertop alone does not prove an unobstructed basin below it.

A duplicate face using the same vertex cycle is counted explicitly. For a non-closed,
incoherent, degenerate or duplicated component, `raw_signed_volume_local` is `null` and
`volume_sign` is `uninterpreted`; inspect the topology findings instead of its volume.

**Boundary:** the helper does not detect self-intersections, overlapping duplicate shells,
physical thickness or custom shading-normal errors. It reports missing checks explicitly.
Signed volume is interpreted only for closed, coherent, nondegenerate components; it is
not a general certification of a solid. An intentional open sheet is not a failed asset.

Verified on Blender 5.2.1 LTS with outward/inward/mixed-component cubes, one reversed face,
an open plane, zero-depth cylinder, mirrored transform, source versus evaluated Solidify,
and actual reversed/degenerate parts from the AV05 kitchen. Source meshes stayed unchanged.
This author verification does not establish agent discovery/use of the helper.

[BMesh measurements](https://docs.blender.org/api/current/bmesh.types.html) ·
[Face orientation versus custom normals](https://docs.blender.org/manual/id/5.2/modeling/meshes/editing/mesh/normals.html) ·
[Cut and bevel](cut-bevel.md) · [Surface/fit](../modeling-workflow.md#surface-quality-and-handoff)
