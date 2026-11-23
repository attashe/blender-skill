# Carry a scalar from instances into their material

**Use:** vary paint, roughness or a surface mask per repeated object while retaining shared
geometry. Contract: a task-owned attribute name, FLOAT on INSTANCE domain, defined range,
and a material on the actual source that reads the same name in **Instancer** mode.

```text
Instances → Store Named Attribute (INSTANCE, FLOAT, owned name) → output
                                      ↑ scalar field
Source material: Attribute (Instancer, same name) → Fac → chosen response → Surface
```

The [small helper](../../scripts/techniques/gn_patterns.py) exposes
`store_instance_value(tree, instances_socket, name, number_or_field_socket)` and
`shader_instance_value(shader_tree, name)`. The first returns the geometry socket that must
continue to output; the second returns Fac for a caller-chosen ramp/mix/BSDF input. Neither
chooses an artistic material, assigns it, nor modifies unrelated graph branches.

Compose these return values as sockets, not nodes:

```python
stored_geometry = patterns.store_instance_value(tree, instances_socket, attribute_name, field_socket)
tree.links.new(stored_geometry, output_node.inputs['Geometry'])
stored_geometry.node.location = (600, 0)  # Optional node layout uses socket.node.
factor_socket = patterns.shader_instance_value(shader_tree, attribute_name)
shader_tree.links.new(factor_socket, response_input)
```

`patterns` is the imported helper; the other variables are the caller's actual sockets/nodes.
For a deliberately ordered alternating pattern, Index → Math Modulo 2 can feed the store.
It is evaluated on the store's instance domain. On a grid this may make stripes rather than
a checkerboard, depending on vertex ordering. A checkerboard needs logical row/column parity;
persistent variation through filtering needs captured identity, not a newly evaluated Index.
Document what the field means before multiplying an asset.

**First proof:** route the scalar to two strongly different emission colors on a few copies.
Inspect actual rendered objects, then change the field or temporarily use a deliberately
missing reader name. The intended variation should disappear in the negative control.
A zero value alone cannot distinguish a valid zero from a missing attribute. If another
object/custom property supplies the same name, Instancer fallback can mask a missing writer;
use a deliberate namespace and inspect the producing geometry branch.

Once the bridge works, route it into the intended material response and inspect that response
under useful lighting. Emission-color validation does not prove metal, roughness or wear looks
right. Keep attributes needed only temporarily anonymous; a named attribute is an interface.

**Limits:** keep instances on this route. Realization changes the geometry/domain and may need
a different shader lookup; inspect propagation instead of blindly retaining Instancer mode.
The author check covers a single instancing layer in EEVEE; the later Pi scene was independently
reopened/rendered in Cycles (see provenance). Nested layers, export and
animated topology require the corresponding consumer check. The [Attribute manual](https://docs.blender.org/manual/en/latest/render/shader_nodes/input/attribute.html)
documents Instancer lookup/fallback; do not infer arbitrary nesting support.

[GN fields/domains](../geometry-nodes-workflow.md) · [Shader boundary](../shader-nodes-workflow.md#connect-geometry-and-materials) ·
[Evidence](provenance.md#geometry-nodes-extraction-batch)
