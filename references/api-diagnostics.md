# Diagnose one Blender operation

For an existing asset, start with its named interface and the next operation. A control's
current channel and evaluated effect are usually enough to start; full scene serialization
can cost more than the edit. If a reporting field fails, omit it when irrelevant. If needed,
query its actual owning type once before changing code.

## Choose the smallest discriminating check

State the question, the observation that would distinguish its causes, and the next action.
Expand the inspection when the result calls for it; a scene-wide dump is rarely a useful
first test. Diagnosis may need several steps, but each should resolve a concrete uncertainty.
Once the target, its output path and the suspect operand are known, move to a controlled
response test. Do not replace a successful scoped probe with a full-tree inspector to
"confirm the full picture". Collect only remaining render prerequisites or dependencies
needed by the next test; widen scope when a specific unresolved question requires it.

| Uncertainty | First check | What it establishes |
| --- | --- | --- |
| Wrong scene, missing target or missing saved render camera? | Loaded filepath, named IDs and active scene/camera before setup edits | Input and saved-state identity |
| Wrong gap or blocked opening? | [Spatial probe](techniques/assembly-fit.md): a selected pair or first-hit ray | Directional extents / sampled occluder, not full collision coverage |
| Empty/cropped close-up or rotated sample seen only from its edge? | [Camera probe](techniques/camera-framing.md): target bounds and caller-known face angle | Framing concern, not visibility/material proof |
| Member, enum or owning API type? | `member()` / `--rna` | Declared RNA members/choices; dynamic lists may be incomplete |
| Need a polygon's mesh edge indices? | Check `polygon.loop_indices` and `mesh.loops[i].edge_index` in the installed API | `polygon.edge_keys` gives vertex-index pairs, not indices into `mesh.edges`; do not assume `MeshPolygon.edges` exists |
| Solid looks plausible but a cut/refraction fails? | [One source/evaluated mesh](techniques/mesh-orientation.md) | Dimensions, component topology/winding; not a thickness or opening certificate |
| Needed render engine available? | Select that documented engine in a disposable scene and read it back; then a tiny render if backend readiness matters | Selection, rendering and visual quality are separate claims |
| Which node/input actually drives this value? | [One node or upstream branch](#inspect-one-node-or-upstream-branch) | Stored graph, flags and operands |
| Changed property, unchanged geometry/motion? | Read actual owner input, update owner/depsgraph, sample one meaningful output | Evaluated response at that sample |
| Linked shader control, unchanged appearance? | One control at two distinct values, fixed camera/light/exposure; expose the affected branch if masked | Visible response in that view |
| Works only before saving? | Reopen the checkpoint and repeat the decisive check | Persistence |

For dynamic enums such as `RenderSettings.engine`, an `enum_items` listing can show only
the current choice. A missing entry or an unrelated property error does not establish that
an engine was removed. Use the [scoped capability check](blender-methods.md#keep-capability-checks-and-recovery-small)
for the needed operation; record selection/read-back separately from a render test.

Separate **passed**, **confirmed mismatch**, **not verified (probe error)** and **not applicable**.
An inspector exception does not prove the asset is broken; a successful inspector does not
prove the requested effect. Keep completed measurements and the editable checkpoint when an
optional report/cleanup field fails. Record the error; repair required checks before claiming
completion. Do not mask a failed script with a later successful command.
A required custom check needs an executed, falsifiable predicate: what measured fact would
make it fail? Recording ID names or writing a verification script is not that check. For a
new or suspect detector, try one deliberate mismatch. Never force success with an unconditional
truthy value; keep an unexecuted or broken check marked not verified.

## Short read-only probe

[api_probe.py](../scripts/api_probe.py) runs inside Blender, including through an execution
connector. For background use, it can run directly without writing an inspector:

```text
blender --background --factory-startup INPUT.blend --python-exit-code 1
  --python SKILL/scripts/api_probe.py -- --expect-file INPUT.blend --object CONTROL
  --output-json OUTPUT/probe.json
```

This is one command split for readability; substitute actual paths and quote spaces.
Use `--bone RIG BONE` for a PoseBone, `--rna FCurve extrapolation` for one API member.
Object/bone/member options may be combined/repeated. A mesh `--object` also reports
its effective material slots/ownership, UV names, dimensions and modifier types. Read that
result before writing another inventory. A missing required member is a failed query;
`getattr(obj, 'materials', [])` would invent an empty assignment instead of repairing the
owner error. Use `obj.material_slots` or `surface(obj)` for those assignments. Blender also prints its own logs to
stdout: `--output-json` writes clean JSON directly to the specified report in your output
folder; do not parse a redirected full Blender log as JSON. Omitting it writes no report file.
A wrong input or missing
control raises an error; a queried absent member reports `found: false`. Keep
`--python-exit-code 1` and the process exit code when capturing logs; use the
[exit-status pattern](blender-methods.md#scripted-execution-and-inspection) if displaying a log afterward.

For an execution connector or an existing script, import the same module. Importing it does
nothing to the scene. Set `skill_root`, `input_file` and the control name from the environment:

```python
import sys, json, bpy
sys.path.insert(0, str(skill_root / 'scripts'))
import api_probe
print(api_probe.identity(input_file, objects=[control_name]))
obj = bpy.data.objects[control_name]
print(json.dumps(api_probe.control(obj), ensure_ascii=False))
```

For a pose control, pass `rig.pose.bones[bone_name]`. For a ShapeKey, call
`api_probe.animation(mesh.data.shape_keys.key_blocks[key_name])` to find its owning Key
datablock, curve and driver sources. Output defaults to 12 entries per collection and reports
`total/truncated`; request a larger `limit` only when needed. The inspection functions never
change frames, create animation or write files. Verify the selected input before trusting the output;
[background execution](blender-methods.md#scripted-execution-and-inspection) explains loading order.

For an unfamiliar or failed API access:

```python
print(api_probe.member(bpy.types.FCurve, 'extrapolation'))
# Actual enum identifiers from this runtime; read these before assigning a value.
print(api_probe.member(bpy.types.Bone, 'roll'))
# A missing member reports the real type and candidates, not a substitute assignment.
```

For a Python utility outside RNA, use its local `help()`/source or matching official API
documentation. Do not copy an entire catalog into context. RNA describes available members;
it does not establish whether they solve the intended visual/functional problem.

## Find a registered operator

Use `api_probe.find_ops("metarig basic human", limit=4)` in the current Blender session to find an unfamiliar operator exposed by an enabled add-on. Every word must occur in the identifier or RNA label. Results show the callable ID (under `bpy.ops`), parameter names and types, and `poll` in the current context. An exact ID such as `api_probe.find_ops("object.parent_set")` also lists declared enum identifiers. Large parameter and enum lists show the first 16 entries. Dynamic enum choices can depend on the context.

For an identification-only request, report a single match immediately when it supplies all requested fields and stop there. `poll=False` is a complete availability result. Narrow the query for ambiguous matches or inspect the particular detail still missing.

The probe reads the registry and calls only `poll()`. A false poll means the operator is registered but currently unavailable. A poll exception is recorded as `poll_error`. A true poll checks availability; verify the result of the eventual call on the target. For example, before automatic armature parenting, inspect the selected mesh and active armature, then check for a modifier and positive deform weights afterward.

For a CLI search, append `-- --find-ops "rigify generate" --limit 4` after `--python SKILL/scripts/api_probe.py`. Search the Blender session with the intended add-on already enabled. Use `--expect-file INPUT.blend` when file identity matters.

## Ownership matters

| Question | Correct scope |
| --- | --- |
| Assigned materials on an object? | Inspect `object.material_slots` for effective assignments and each slot's `link` ownership. Mesh-owned slots are on `object.data.materials`; Object has no `materials` collection. |
| Rest skeleton, posed transform, edit-mode roll? | `rig.data.bones`, `rig.pose.bones`, `rig.data.edit_bones` respectively. Query PoseBone for pose constraints and transforms; enter Edit Mode only when deliberately editing the rest skeleton. |
| Where are this target's keys? | `target.id_data.animation_data` owns them; `target.path_from_id(...)` identifies its channel. PoseBone keys belong to the rig Object, ShapeKey keys to the Key datablock. |
| Where are Action curves in Blender 5.x? | Assigned Action **and assigned slot**, then `anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)`. It may return `None`; it returns the first matching bag, not a flattened NLA result. |
| Interpolate, extrapolate, repeat? | Keyframe `interpolation` controls intervals; FCurve `extrapolation` controls outside-key behavior; a Cycles modifier repeats. These are distinct operations. |
| Where is a driver's source? | Its variables' `targets`; inspect target ID, data path or transform/bone space according to variable type. |
| Which collections contain an object, or belong to a scene? | `object.users_collection` lists direct memberships. Traverse `scene.collection.children` recursively for the scene's collection tree. A Collection has `children` and `objects`; do not transfer Object membership attributes to it. |

After a node-construction failure, test one instance in the intended tree before rerunning
the full builder. Geometry/shader node types are not interchangeable; a Normal value uses a
vector interface socket, not an invented `NodeSocketNormal`. Inspect actual RNA properties
and available inputs/outputs with the node probe. A missing name in this runtime does not
by itself establish that a feature was removed in a Blender release.

Node settings can be RNA properties rather than sockets. For example, inspect a Brick Texture's
actual inputs and [`offset` property](https://docs.blender.org/api/main/bpy.types.ShaderNodeTexBrick.html)
instead of assuming an input named `Offset`. Probe the
owning node once; replacing a missing name with another guess does not resolve that distinction.

The legacy `Action.fcurves` interface was removed in Blender 5.0; see the
[official migration notes](https://developer.blender.org/docs/release_notes/5.0/python_api/).
The [channelbag utility](https://docs.blender.org/api/5.4/bpy_extras.anim_utils.html) documents
first-match behavior; verify availability in the actual runtime. The included probe was
executed on Blender 5.2.1 LTS, not certified for all releases or complex layered/NLA evaluation.

## Geometry Nodes modifier inputs

Resolve the input's identifier from `modifier.node_group.interface.items_tree`; it is not the
visible socket label. Blender 5.2 changed the owner of input values. In the tested runtime,
`modifier[identifier] = value` raises TypeError; use
`getattr(modifier.properties.inputs, identifier).value`. Check that entry's `type` before
assuming a constant value is active; an attribute-driven input uses its attribute name/mode.
Earlier releases use the modifier's ID-property interface. See the [official migration](https://developer.blender.org/docs/release_notes/5.2/python_api/).

The [pattern helper](../scripts/techniques/gn_patterns.py) provides `set_inputs(modifier, **values)`
for its constant inputs, resolving identifiers and choosing that API branch. It is not a
universal setter for menus, fields, animation or arbitrary asset modifiers. Tag/update the
owner, read back the actual input, and inspect the evaluated count/spacing/radius. Changing a
group socket's default is not the same as changing one existing modifier's value.

## Shader controls

For a simple owned material tree, a named Value or RGB node exposes a live control without
group-interface plumbing. `destination` is a real input socket in `tree`:

```python
control = tree.nodes.new('ShaderNodeValue')
control.name = 'Response amount'
control.outputs[0].default_value = 0.6
tree.links.new(control.outputs[0], destination)
```

Use ShaderNodeRGB for a color. Value-node output sockets do not expose arbitrary min/max
bounds; enforce needed ranges with a Clamp node or an intentional graph operation. For a
reusable group, declare its interface on a separate ShaderNodeTree, then link **Group Input
node outputs**, not the NodeTreeInterfaceSocket returned by `interface.new_socket`:

```python
group = bpy.data.node_groups.new('Response controls', 'ShaderNodeTree')
declared = group.interface.new_socket(name='Amount', in_out='INPUT', socket_type='NodeSocketFloat')
declared.default_value = 0.6
declared.min_value, declared.max_value = 0, 1
group.interface.new_socket(name='Value', in_out='OUTPUT', socket_type='NodeSocketFloat')
group_input = group.nodes.new('NodeGroupInput')
group_output = group.nodes.new('NodeGroupOutput')
group.links.new(group_input.outputs['Amount'], group_output.inputs['Value'])
instance = tree.nodes.new('ShaderNodeGroup')
instance.node_tree = group
tree.links.new(instance.outputs['Value'], destination)
instance.inputs['Amount'].default_value = 0.4
```

The declaration describes the interface; the group-input socket participates inside it;
the instance input controls one use in the material. Existing callers need their instance
values changed, not just the declaration default. Name the material or group you own; a
material's embedded node-tree name is not a freely assignable group name in the tested runtime.
Check the actual socket/enum with RNA when needed. A link proves connectivity only: vary one
control and check its evaluated response before adding secondary texture detail or reporting
all controls as working. A zero multiplier can silently cancel a correctly linked input.

## Constant procedural pattern after grouping

Before retuning frequency or contrast, follow the coordinate signal into the actual group
instance. A plain shader-group Vector socket uses its instance default when unlinked;
`(0, 0, 0)` then samples one location. Creating Texture Coordinate and Mapping nodes beside
the group does not connect them. A texture node's implicit coordinates are a different case.

For a known instance/input, append one query to the probe command (names are examples):

```text
--input "material:Board" "Grain instance" "Vector" --depth 2 --max-nodes 8
```

Read `is_linked`, the stored default and upstream links. For group internals, inspect the
reported `group:NAME` separately, retaining the caller's input. If wiring looks correct but
the cause remains uncertain, expose one relevant scalar/color output as emission in a
disposable diagnostic copy: does it vary across the intended face? Change only the suspected
connection/control and compare under the same view. This separates a constant signal from
surface/lighting suppression. Restore the actual material and review it afterward: visible
variation establishes signal flow, not natural grain or a correct finish.

This route was checked on an actual missing-coordinate group in Blender 5.2.1 LTS.
The [group socket default](https://docs.blender.org/manual/en/5.1/interface/controls/nodes/groups.html)
describes the interface behavior; inspect the installed runtime for other socket types.

## Move from diagnosis to the edit

After resolving the owner/channel, use [motion techniques](technique-index.md) for a small
tested operation, or implement the corresponding API directly. The helpers are optional;
they avoid rewriting slot/FCurve plumbing for ordinary keys, rotation or property drivers.
Evaluate one meaningful changed frame, save the editable checkpoint, then add measurements
or presentation. Diagnostics describe stored state; only evaluated samples and reopened
outputs establish that the requested change works.

## Inspect one node or upstream branch

Use the same entrypoint for an existing material, world or node group. Replace these example
names with actual IDs; start with a tree summary only if the relevant node is unknown:

```text
--tree "material:Painted Metal" --limit 12
--node "material:Painted Metal" "Base BSDF" --limit 32
--input "material:Painted Metal" "Base BSDF" "Roughness" --depth 2 --max-nodes 8
```

Append the chosen query to the background command above, with `--expect-file` and a report
path. `group:Pattern` selects a standalone node group; `world:Studio` selects a World tree.
Options may repeat. Tree/node summaries include `total/truncated`; increase only the bound
that hid needed evidence. A socket selector is a unique exact name, `#0` for an observed
index, or `id:IDENTIFIER` from the report. Duplicate labels raise instead of choosing a
possibly inactive socket. The error includes a bounded list of real selectors from that node;
choose the intended one without rebuilding an inspector. Shader and Geometry sockets need
not have `default_value`.

For a connector/script, the optional [node_probe.py](../scripts/node_probe.py) exposes the
same read-only inspection after the identity check and scripts-path setup above:

```python
import node_probe
tree = node_probe.resolve_tree('material:Painted Metal')
print(json.dumps(node_probe.trace_input(tree.nodes['Base BSDF'], 'Roughness'), ensure_ascii=False))
```

The branch report shows physical links, enabled/unavailable flags, mute state, operations,
stored operands and upstream nodes. `hide` describes UI visibility, not whether a socket
works. A linked input's stored default is **not its evaluated value**. Muted/invalid links
are flagged; the helper does not decide which shader/field branch executes. Tracing stops at
the configured depth/node count and group boundaries; inspect the named group separately and
retain its caller's input values. It does not prove that the inspected BSDF reaches the
active Material Output. Check that path before interpreting a render.

For a nonresponding control, follow its target input through the short chain. A zero gain,
saturated clamp, constant mix endpoint or inactive branch may explain the result. Treat it
as a hypothesis until changing that one control produces the intended evaluated/visual
response. If the branch is intentionally hidden, temporarily isolate it, then restore the
original composition. Save the tested values and verify reopening when delivery requires it.

Independent node queries retain individual `ok`/`probe_error` results. Any failed requested
node query still makes the CLI fail after writing partial JSON; it is not silently skipped.
Wrong input identity remains fatal before inspection. These are stored-state probes, tested
on Blender 5.2.1 LTS; use actual RNA for fields that differ in another runtime. See
[NodeSocket API](https://docs.blender.org/api/5.2/bpy.types.NodeSocket.html) and
[data lifetime cautions](https://docs.blender.org/api/main/info_gotchas_crashes.html).
