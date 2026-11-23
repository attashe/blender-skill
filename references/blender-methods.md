# Choose Blender methods by the asset problem

Choose for the reference-derived shape, required editability and target output. Verify the
runtime and probe only the capability needed next. Record a consequential method choice
in the project notes (or `method` in the manifest profile). Revisit it when visual comparison
or measured output misses the brief. Do not turn this table into a feature checklist.

## Route by the next unresolved question

Read only the branch needed for the current task. Each branch covers decisions, practical
tool use and observable checks; its diagrams are guidance, not compulsory steps.

| Need | Read |
| --- | --- |
| Evaluate layout, framing, scale or mood cheaply | [Blockout, camera and light](blockout-camera-light.md) |
| Develop mesh/sculpt forms, topology or modifier structure | [Modeling workflow](modeling-workflow.md) |
| Build rock families with geological form and weathering | [Rock recipes](rock-recipes.md) |
| Develop plant morphology, foliage or compact shrubs | [Vegetation](vegetation-workflow.md); [shrubs and dense crowns](shrub-recipes.md) |
| Construct, debug, reorder or apply an evaluated modifier stack | [Modifiers](modifiers-workflow.md) |
| Build or debug procedural geometry, fields, attributes or reusable generators | [Geometry Nodes](geometry-nodes-workflow.md) |
| Place objects in rows, grids, rings, along paths or over surfaces | [Patterns and scatter](scatter-workflow.md) |
| Develop materials, procedural textures, map connections or GN-driven shading | [Shader nodes](shader-nodes-workflow.md) |
| Compose multiple surface responses, coatings, transmission/scattering or stylized effects | [Material composition](material-composition.md) |
| Design cel/toon light bands, graphic highlights or contours | [Cel shading and contours](cel-shading-workflow.md) |
| Author maps, paint/projection, layer masks or prepare texture channels | [Texture authoring](texture-authoring-workflow.md) |
| Choose/create UV layouts, seam strategy, density, trims/tiles or packing | [UV layout](uv-workflow.md) |
| Transfer geometry/material information, mesh maps or lighting into textures | [Baking](baking-workflow.md) |
| Shape paths, profiles, cables, rails or curve-driven systems | [Curves and profiles](curves-workflow.md) |
| Build poseable controls, mechanisms, IK/FK or rig attachments | [Rigging](rigging-workflow.md) |
| Skin a mesh, repair joint shape, create morphs/correctives or bind cages | [Deformation](deformation-workflow.md) |
| Develop motion, timing, reusable clips or simulation | [Animation](animation-workflow.md) |
| Emit or animate particles, debris, motes, precipitation or trails | [Particle effects](particles-workflow.md); [stateful GN](particle-simulation-nodes.md) when history matters |
| Develop rigid contact, cloth, liquid, smoke or fire | [Specialist simulation](simulation-workflow.md), then only the relevant solver branch |
| Build short fur, long hair, brows or strand dynamics | [Grooming](grooming-workflow.md) |
| Develop shot lighting, camera presentation, reflections or a focused relight | [Lighting](lighting-workflow.md) |
| Choose/diagnose an engine, render quality/cost or saved image/sequence output | [Rendering](render-workflow.md) |
| Assemble images, grade selected regions, add image effects or deliver a finished shot | [Compositing](compositing-workflow.md); [passes and mattes](compositing-passes-and-mattes.md) for AOVs/Cryptomatte/reconstruction |
| Extract a foreground, track a plate or attach an element to footage | [Footage integration](footage-integration-workflow.md) |
| Export geometry/materials/motion to another consumer | [Export workflow](export-workflow.md), then the selected [format profile](export-formats.md) |
| Reduce measured cost, create LODs or prepare collision/lightmaps | [Performance](performance-workflow.md) |
| Choose newer tools or adapt a version-sensitive API | [Recent features and capability checks](recent-blender-features.md) |

The [procedural geometry contract](procedural-geometry.md) remains the common source for
topology bounds, extrema tests and viewport/render divergence; do not duplicate it per branch.

| Problem | Candidate method | Check the result |
| --- | --- | --- |
| Repeated panels, seats, bolts, facade units | Collection instances; linked mesh data; Geometry Nodes instances | Count, spacing, orientation, unique data cost and expanded triangles; preserve instances |
| Configurable wall, cabin lining, vents, equipment families | Reusable Geometry Nodes group with a small interface | Change a useful parameter, test minimum/typical/maximum values, verify bounds and material slots |
| Hoses, cables, rails, road edges | Bézier/poly/NURBS curves, Curve to Tube, Curve to Mesh, custom profiles | Bound path and profile resolution independently; check ends, tilt, bend radius and evaluated triangles |
| Smooth rational profiles or controlled surface patches | NURBS curve or U/V NURBS surface; retain editable control structure | Order/weights/continuity where relevant, U/V tessellation, trim/export needs and mesh cost |
| Machined/hard-surface components | Bevel/Solidify/Mirror/Boolean stack; explicit mesh where appropriate | Modifier order, scale effects, pinching/normals, silhouette, evaluation cost |
| Organic/hero form | Sculpting/subdivision followed by retopology and baking for a realtime target | Silhouette, deformation, clean runtime topology, bake artifacts |
| Dense visual surface detail | Shader nodes, decals, normal/displacement maps or baked detail | Camera-distance readability, shader/export support, material count; geometry only when silhouette needs it |
| Spatial scatter/placement rules | Geometry Nodes fields, raycasts, attributes, source instances | Consumer domain, deterministic seed, spacing/exclusion masks, unintended overlaps |
| Iterative growth or stateful effect | Repeat/Simulation zones and caching/bake where suitable | Frame range, cache validity, deterministic replay and an actual scene outcome |
| Reusable kit | Asset Browser, catalogs, node-group/collection assets | Asset identity, root hierarchy, dependencies, previews and save/reopen persistence |
| Shots/looks requiring alternatives | View Layers, collections, light controls, compositor | Final render, color management, deliberate exclusions and render-time cost |

For frequent material types and reusable look-development routes, use
[surface families](surface-families.md). For a plant's construction, silhouette and leaf response,
use [vegetation](vegetation-workflow.md); route to scatter only after its source works.

## Version-sensitive features

Use the actual runtime and project's target version. Earlier examples in this package were
written for 5.2; that is not evidence of the current session's version. Read
[bounded procedural geometry](procedural-geometry.md) before path-driven or parametric work.

Consult matching official manuals/release notes for unfamiliar features, then probe the live
RNA, node modes and sockets. Resolve modifier inputs by the actual interface/property identity
and read back writes; a remembered `Socket_N` or property layout may belong to another version.
Check shader, smoothing, render-engine and exporter properties the same way. Connection-tool
compatibility and feature availability are separate questions. Use experimental features only
for a concrete task need with an isolated test and a workable fallback.

A missing name proves only that this lookup failed in this runtime. Check spelling, owning
type and documented signature before calling it a removed feature. Claim a version change
only with evidence from the previous API or release notes, not from an unsuccessful guess.

RNA enum inspection may omit dynamically registered or context-dependent choices. The
[EnumProperty API](https://docs.blender.org/api/5.0/bpy.types.EnumProperty.html) distinguishes
static items from dynamic generation; even `enum_items` is not a complete capability test in
every context. Before declaring a needed engine unavailable, check the active setting and
runtime registration or try the documented choice in an isolated disposable scene. Selecting
an engine proves selection, not render/backend readiness; test a small render only when needed.

## Keep capability checks and recovery small

Start with the session identity, version and the scene state needed for the next change.
Inspect a feature when it is about to be used; avoid surveying unrelated preferences, devices,
installation paths or the entire node catalog before a working blockout exists. A connected
execution channel does not require locating another executable unless the task actually needs it.

### Scripted execution and inspection

Save a substantial generated script through a file-writing tool, then invoke that file with
a short command. Long inline shell payloads can be truncated by the launch path (observed
with a Windows Bash here-document); the shell can return success after writing only part
of the source. If the expected job never starts, inspect the saved script/log before
debugging Blender. Keep source creation and execution separately reviewable.

For background adaptation of an existing file, check `bpy.data.filepath` and the few
required object/control names before reading measurements or editing. Stop if they do not
match the intended input; a startup cube is not evidence about the supplied asset.
Blender executes CLI actions in [argument order](https://docs.staging.blender.org/manual/en/latest/advanced/command_line/arguments.html#argument-order):
load the input before the script that inspects it. For example,
`blender --background --factory-startup input.blend --python-exit-code 1 --python job.py`;
alternatively open the intended file explicitly inside the script before querying it.
For an isolated background job, `--factory-startup` avoids loading unrelated user startup
state/add-ons; add `--disable-autoexec` when automatic file scripts are not needed. If the
workflow requires a particular add-on, load that dependency deliberately. An unrelated add-on
startup/shutdown traceback is not evidence that the inspected mesh or the job's API failed.

For a new scene, omit `input.blend`. Script arguments belong **after** Blender's `--`;
the script itself belongs to `--python` before that boundary. For example:

```text
blender --background --factory-startup --python-exit-code 1 --python job.py -- --stage 1 output_dir
```

Inside the script, pass `sys.argv[sys.argv.index("--") + 1:]` to its parser when `--` is
present (otherwise an empty custom-argument list). Parsing the full `sys.argv` can treat the
Blender executable or its options as input/output paths. Verify a small job's save/read-back
before expanding it; a successful process that never ran the script proves nothing.
The installed `blender --help` documents these options; use that for a launch ambiguity.

Adapt paths/startup options to the environment. Keep the original exception/exit status
when shortening output; a later `tail`, `grep` or successful log read does not validate the job.
For a Bash pipeline, `set -o pipefail` preserves a failing Blender stage through `| tail`;
it does not preserve that status through a subsequent successful command. Capture/check the
Blender process result when continuing with other commands. For Bash, immediately after
your Blender command has written to the caller-owned `log_path`:

```bash
job_status=$?
tail -n 20 "$log_path"
exit "$job_status"
```

Do not run `echo` before capturing `$?`. When scripting the launcher in Python, retain
`subprocess.run(...).returncode` instead. Dependent stages must stop on a nonzero result;
reading an existing JSON/checkpoint is allowed as partial evidence, with its failed checks
still marked unverified.

For a bounded edit, probe only the owning control, affected dependencies and current
animation/modifier relation. If a diagnostic field fails, confirm that field is needed before
repairing it. Inspect the live property/type or documentation once rather than growing an
inventory through successive guessed attribute names.
The optional [API probe](api-diagnostics.md) resolves a named control, its owning animation
data, an individual RNA member or a scoped node branch without changing the scene.

Use the execution tool's documented input and output contract; Python running at top level
does not accept a function-style `return`. Inspect returned error text as well as transport
success. A stage runner must return an explicit failure or re-raise after logging; printing
`FAILED` and leaving the loop can make the outer tool report success. Stop dependent stages
when their input stage fails. For CLI Python jobs, propagate exceptions to the runner; Blender's
[`--python-exit-code`](https://docs.blender.org/manual/de/5.0/advanced/command_line/arguments.html)
can supply a nonzero exit status. If a probe fails, isolate the first failing access,
inspect the actual API/RNA or matching documentation, and rerun that small case.
In code executed inside a persistent Blender/MCP process, do not use `raise SystemExit` to
signal a failed stage: if unhandled, it can terminate the host without a traceback and close
the connection. Report failure through the connector's contract or raise an ordinary exception;
use `return` only inside a function. A closed socket alone does not prove a native crash:
compare the process exit, stage log and timestamps of any crash dump with the failed call.
A guessed fallback that stores a value
without affecting evaluated geometry is not a repair.

Build a small working element before a large assembly: prove its geometry, modifier/node
inputs and one useful variation, then expand. A single reusable script is fine when it can
execute and inspect scoped stages. Keep temporary data identifiable and restore the previous
scene/state even after failure. Do not delete or rebuild unrelated data as error recovery.

For a shared construction helper, define accepted argument names, units and coordinate space.
Reject unsupported supplied arguments instead of silently falling back to defaults. Before
reuse, pass a meaningful non-default dimension/count and measure its evaluated effect; for
example, verify whether a radius input produces the intended radius or diameter. Check the
caller-to-helper mapping as well as the Blender API. A helper that returns geometry without an
exception may still ignore the control that defines the asset's proportions.

An extra scene isolates ownership, not the Blender process: a crash can lose all unsaved work.
Checkpoint working geometry before complex diagnostics. Use a separate process/copy for risky
batch experiments when available. After connection loss, confirm session identity and saved
state before retrying; restarting an application is not proof that its previous state survived.

Evaluated data and dependency-graph iteration have limited lifetimes. Consume each
`object_instances` item during iteration and copy needed matrices/scalars; do not keep iterator
items in a list for later access. Reacquire evaluated data after graph updates or topology
changes, and release temporary `to_mesh()` results with their owner's `to_mesh_clear()`.
See the [dependency-graph API](https://docs.blender.org/api/4.5/bpy.types.Depsgraph.html) and
its invalidation/lifetime rules, then check the installed API. A process crash during a probe
needs an isolated reproducer before attributing it to a particular node or add-on.

## Assemble a local asset or preserve world placement

For ordinary object parenting, decide whether child coordinates describe the new asset's
local space or an existing world placement. Local assembly uses that local basis under the
root with no unintended Parent Inverse compensation; moving the root should place the
assembled parts. Preserving an existing world transform while reparenting is a different
operation: keep-world/inverse compensation deliberately offsets the new parent's transform.
Copying that compensation into local assembly can leave children near the origin while
the root and camera target move elsewhere. See [Parenting Objects](https://docs.blender.org/manual/en/5.0/scene_layout/object/editing/parent.html).
Verify evaluated child/instance bounds after translating and rotating the root; frame the
actual subject. Do not clear inverses blindly on an existing rig or animated hierarchy.

## Probe a node in a disposable test group

This is an implementation pattern to adapt after consulting the installed API, not a certified
cross-version recipe. Run inside the intended Blender, restore what you temporarily create,
and use the identifiers that Blender returns:

```python
import bpy

print(bpy.app.version_string)
group = bpy.data.node_groups.new("TMP_probe", "GeometryNodeTree")
try:
    node_type = "GeometryNodeInstanceOnPoints"  # candidate, not a guessed socket layout
    node = group.nodes.new(node_type)
    print([(s.name, s.identifier, s.type) for s in node.inputs])
    print([(s.name, s.identifier, s.type) for s in node.outputs])
    print([p.identifier for p in node.bl_rna.properties])
finally:
    bpy.data.node_groups.remove(group)
```

Set a node mode before inspecting the sockets affected by that mode. Resolve duplicate labels
by identifier. Read the graph after wiring, and measure its evaluated output. Inspect a render:
correct sockets and nonzero polygons alone do not establish correct shape or placement.

## Resolve active node sockets and prove their effect

Mode enums and socket types are different namespaces. For example, a Random Value node's
data_type can be FLOAT or FLOAT_VECTOR while the corresponding socket.type is VALUE or VECTOR
in the tested 5.2 runtime. Set the mode first, inspect the current sockets, and reject missing
or ambiguous matches. An assignment to an unavailable socket can succeed without affecting
evaluation. Hidden UI sockets are not necessarily unavailable; do not filter by hide alone.

This pattern resolves an unlinked constant input by observed label/type; use the actual
identifier too when labels repeat. Adapt to the installed API rather than freezing indices:

```python
def active_input(node, name, socket_type, identifier=None):
    matches = [s for s in node.inputs
               if s.name == name and s.type == socket_type
               and not s.is_unavailable
               and (identifier is None or s.identifier == identifier)]
    if len(matches) != 1:
        raise ValueError(f"Expected one active {name}/{socket_type}: {len(matches)}")
    if matches[0].is_linked:
        raise ValueError(f"{name} is linked; its default is not the controlling value")
    return matches[0]

random_node.data_type = 'FLOAT'
lower = active_input(random_node, 'Min', 'VALUE')
upper = active_input(random_node, 'Max', 'VALUE')
lower.default_value, upper.default_value = 0.75, 1.30
assert abs(lower.default_value - 0.75) < 1e-6
assert abs(upper.default_value - 1.30) < 1e-6
```

These are illustrative bounds, not a prescribed leaf size. Check the evaluated instance scales
on a bounded sample, including actual variation and an unintended near-zero tail; finite random
samples need not reach the exact endpoints. For Vector Math SCALE, inspect its active scalar
Scale input instead of assuming the second Vector input controls it. Verify an output change
with a constant diagnostic vector before attaching a wind system. Restore intended values.
For linked inputs trace the controlling upstream value. Socket correctness, evaluated behavior
and visual quality are three different checks. The [NodeSocket API](https://docs.blender.org/api/main/bpy.types.NodeSocket.html)
and [5.2 API notes](https://developer.blender.org/docs/release_notes/5.2/python_api/) document
availability and changed interfaces; moving documentation is not a version guarantee.

## Set a current GN modifier input without guessing its identifier

For Blender 5.2's constant-input RNA API, this is a small pattern after selecting `modifier`
and establishing a bounded `requested_count`. Inspect the actual interface first. When labels
repeat, also resolve by panel/type/identifier; reject ambiguity rather than taking the first.

```python
matches = [s for s in modifier.node_group.interface.items_tree
           if s.item_type == 'SOCKET' and s.in_out == 'INPUT'
           and s.name == 'Amount' and s.socket_type == 'NodeSocketInt']
if len(matches) != 1:
    raise ValueError('Expected one integer Amount input in this asset')
control = getattr(modifier.properties.inputs, matches[0].identifier)
control.value = requested_count
assert control.value == requested_count
modifier.id_data.update_tag()
animation_path = control.path_from_id('value')
```

This verifies a property write, not its geometry. Evaluate and measure the output next. For
menu inputs inspect the live enum identifiers; for attribute-driven inputs inspect their mode
and attribute binding. Other versions require their own documented access pattern. Never
write a guessed legacy custom property and infer success merely because it stored a number.

## Link a child collection into its parent

Create the parent file at its intended destination before relying on relative paths. Obtain the
actual linked collection from the `data_to` result; do not retrieve a colliding name globally.
Keep its source geometry immutable in the parent. Inspect the installed API before using this
pattern and test save/reopen/update propagation on the project:

```python
import bpy

with bpy.data.libraries.load(child_file_absolute, link=True, relative=True) as (source, target):
    if child_root not in source.collections:
        raise ValueError(f"Missing public collection: {child_root}")
    target.collections = [child_root]
child = target.collections[0]
instance = bpy.data.objects.new(instance_name, None)
instance.instance_type = "COLLECTION"
instance.instance_collection = child
instance["asset_id"] = child_id
parent_root.objects.link(instance)
instance.location = placement_m
```

Collection linking and library overrides require a clean root hierarchy. Use overrides narrowly
for rig/pose/instance configuration that must vary. Source mesh edits belong in the source file.
Append can intentionally create an independent owned variant; declare its new identity and reason.

## Measurement rules

For command-line Python jobs, configure a nonzero Python-error exit status (for example
`--python-exit-code 1` before `--python`) and propagate the process result through the caller.
Inspect the log and reopen the output from this run; an old file and a successful shell status
can otherwise conceal a script failure. This is specific to the CLI execution route; see the
[documented option](https://docs.blender.org/manual/de/5.0/advanced/command_line/arguments.html).

- Count evaluated triangles after modifiers and GN, including repeated instances. Also measure
  unique evaluated geometry so repeated content is not mistaken for many unique meshes.
- Read final evaluated bounds; `obj.data` and control-point counts can miss generated geometry.
- Scope measurements to the asset and its evaluated instances; exclude presentation ground,
  lights and unrelated scene objects. An instance-only GN output can have an empty local mesh
  while its occurrences occupy real space. Do not report that as zero size.
- Derive acceptance from output independently of requested settings. A positive distance between
  centers does not prove non-overlap: compare actual extents/clearances, or use a suitable
  intersection test for complex shapes. For contact, measure both participating surfaces;
  assigning the same expected coordinate to both sides cannot test the joint.
- Keep viewport timings, render timings, export geometry, and runtime GPU draw calls distinct.
  Offline Blender measurements do not certify Unity or WebGPU frame rate.
- Use meaningful behavior checks: socket separation, walkway clearance, door swing, repetition
  count, empty scatter exclusion zone, parameter extrema. Use an output derived from the request.
- Optimize the largest measured cost. Reduce repeated data with instancing; reduce silhouette-
  invisible detail with maps/LOD; bake expensive static procedural systems into an export variant.

Official references: [4.5 release](https://www.blender.org/download/releases/4-5/),
[5.2 Geometry Nodes](https://developer.blender.org/docs/release_notes/5.2/geometry_nodes/),
[5.2 Python API changes](https://developer.blender.org/docs/release_notes/5.2/python_api/),
[compatibility notes](https://developer.blender.org/docs/release_notes/compatibility/),
[Link & Append](https://docs.blender.org/manual/en/5.2/files/linked_libraries/link_append.html),
[Library Overrides](https://docs.blender.org/manual/en/5.2/files/linked_libraries/library_overrides.html).
