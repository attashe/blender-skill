# Repeat a source in a row, grid or ring

**Use:** editable posts, panels, seats, fasteners or similar regular layouts. Decide source
pivot/axes, count, center spacing, orientation and host-local coordinates. Source footprint
and spacing are separate: a correct point layout does not certify clearance between parts.
For a few composed objects, manual linked instances may be enough.

| Need | Small graph and invariant | Boundary |
| --- | --- | --- |
| Row | Mesh Line / Offset → Instance on Points; `p[i] = i * step` | N points span `(N-1)*step`, not `N*step`; zero must produce empty output deliberately |
| Grid | Grid → Instance on Points; size X/Y = `(count-1)*spacing` | Centered XY; counts are vertices, not faces; native Grid needs at least 2 per axis |
| Ring | Unfilled Mesh Circle → Instance on Points | N unique points at radius R; do not duplicate the closing endpoint |
| Radial/tangent ring | Position or `Z × Position` → Align Rotation to Vector → instance Rotation | Local +X forward, +Z up; uses ring centered at local origin; translation is not a direction |

**Optional implementation:** [gn_patterns.py](../../scripts/techniques/gn_patterns.py),
`create_pattern(source, layout, name=None, max_count=256, max_axis=32, orientation='FIXED')`.
Creates one editable node group. It does not create/clear a scene, attach a modifier, assign
materials, apply transforms or save files. Only mesh sources are accepted by this small helper.
Import it from the installed skill's `scripts/techniques` directory; do not run a historical
asset builder to obtain the mechanism.

```python
import sys
sys.path.insert(0, str(skill_root / 'scripts' / 'techniques'))
import gn_patterns as patterns
# source and host are distinct caller-owned objects; host is an intended generator.
group = patterns.create_pattern(source, 'RING', max_count=64, orientation='RADIAL')
modifier = host.modifiers.new('Fastener layout', 'NODES')
modifier.node_group = group
patterns.set_inputs(modifier, Count=9, Radius=0.12)
```

Other exposed inputs: ROW `Count`, `Step`; GRID `Count X`, `Count Y`, `Spacing X`,
`Spacing Y`. `Source` remains editable on the modifier. `set_inputs(modifier, **values)`
resolves interface identifiers, tags the owner for re-evaluation and uses the installed modifier API.
Use it for the changed-parameter check too; direct RNA writes without an update can leave the
evaluated output stale. See [API help](../api-diagnostics.md#geometry-nodes-modifier-inputs).
The group replaces the host's geometry output with instances; attach it to an intended
generator, or integrate its output explicitly into a larger graph. Each call creates a group;
reuse a group datablock for a shared rule instead of appending duplicate modifiers on reruns.

**Ranges are part of this implementation:** ROW count clamps to 0..max_count; GRID each axis
to 2..max_axis; RING count to 3..max_count. Radius/spacing clamp to 1e-6. These bounds occur
before generation; total grid count is bounded by max_axis². A singleton grid or one/two
radial objects needs a line/explicit angular layout; do not claim this helper produced that
request merely because Blender clamped it. Choose a sensible upper bound for the source cost.

Object Info uses **Original** and **As Instance**: reuse source-local geometry without carrying
its scene placement into each copy. Host transforms then place the assembly. If the source's
scene transform is intentionally part of the design, adapt the graph and prove that contract;
switching to Relative changes the relationship. Do not feed the consuming host into Source.

**First proof:** use an asymmetric source. Measure count and local origins; compare radial or
tangent +X and local +Z, then apply a host translation/rotation/nonuniform scale. World circles
become ellipses under nonuniform scale. Verify one changed parameter, source placement, actual
clearance and saved/reopened instances. An empty evaluated mesh can be correct for an
instance-only output; count dependency-graph instances instead of adding Realize as a repair.

For a bounded instance check, copy the values while iterating the dependency graph:

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
matrices = [item.matrix_world.copy() for item in depsgraph.object_instances
            if item.is_instance and item.parent and item.parent.original == host]
```

These are world matrices; use the host inverse for local measurements. Do not retain the
temporary iterator wrappers across graph updates. An evaluated Object's `to_mesh()` already
returns a Mesh; release temporary meshes through that Object when the mesh route is needed.

For shader variation use [instance attributes](instance-shader-attribute.md). Index follows
the primitive's element order; it is neither a universal checkerboard coordinate nor a stable
identity after filtering. For surface/path distribution continue with [scatter](../scatter-workflow.md).

For a graph/socket question use [targeted node inspection](../api-diagnostics.md#inspect-one-node-or-upstream-branch).
For modifier input values use [their actual owner](../api-diagnostics.md#geometry-nodes-modifier-inputs);
group declaration defaults do not report the current modifier value.

[Evidence and limits](provenance.md#geometry-nodes-extraction-batch) ·
[Rotation input semantics](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/utilities/rotation/align_rotation_to_vector.html)
